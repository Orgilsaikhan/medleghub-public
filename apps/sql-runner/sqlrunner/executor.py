"""Сурагчийн statement-үүдийг `student` данстай ажиллуулж, үр дүнг цуглуулна.

`mysql` CLI шиг: statement бүрийг дарааллаар ажиллуулж, эхний алдаан дээр
зогсоно. Хугацаа хэтэрвэл админ холболтоос `KILL` хийнэ — `SLEEP`, удаан
JOIN, түгжээ хүлээх зэрэг бүгдийг хамарна.

Үр дүнг `SSCursor`-оор (unbuffered) мөр мөрөөр уншина — сая мөртэй хүснэгтийг
санах ойд бүтнээр нь ачаалахгүй. Харуулах мөрөөс илүүг зөвхөн тоолно.
"""

import asyncio
import contextlib
import datetime
import logging
import threading
import time
from dataclasses import dataclass, field
from typing import Any

import pymysql
import pymysql.cursors

from sqlrunner.mysqld import STUDENT_USER, MysqlInstance
from sqlrunner.settings import settings
from sqlrunner.splitter import Statement

logger = logging.getLogger("uvicorn.error")

# KILL-ийн дараа ажиллагаа дуусахыг хүлээх хугацаа. Хэтэрвэл сервер гацсан гэж
# үзээд процессыг алж, pool нь цэвэр загвараас дахин эхлүүлнэ.
KILL_GRACE_SECONDS = 5.0
MAX_WARNINGS = 20

JSON = dict[str, Any]


class OutputLimitError(Exception):
    """Гаралт хэт их — үлдсэн statement-ийг ажиллуулахгүй."""


@dataclass
class RunState:
    results: list[JSON] = field(default_factory=list)
    error: JSON | None = None
    timed_out: bool = False
    output_truncated: bool = False
    thread_id: int | None = None
    output_chars: int = 0

    def to_json(self, duration_ms: int) -> JSON:
        return {
            "results": list(self.results),
            "error": self.error,
            "timed_out": self.timed_out,
            "output_truncated": self.output_truncated,
            "duration_ms": duration_ms,
        }


def failure(line: int | None, message: str) -> JSON:
    """Серверт очихоос өмнөх алдаа (хуваалт, statement-ийн тоо)."""
    state = RunState(error={"line": line, "code": None, "sqlstate": None, "message": message})
    return state.to_json(0)


def empty_outcome() -> JSON:
    return RunState().to_json(0)


def _format_time(value: datetime.timedelta) -> str:
    """MySQL TIME — `str(timedelta)`-ээс ялгаатай нь 24 цагаас их, сөрөг утгатай."""
    micros = (value.days * 86_400 + value.seconds) * 1_000_000 + value.microseconds
    sign = "-" if micros < 0 else ""
    seconds, micros = divmod(abs(micros), 1_000_000)
    hours, rest = divmod(seconds, 3600)
    minutes, seconds = divmod(rest, 60)
    text = f"{sign}{hours:02d}:{minutes:02d}:{seconds:02d}"
    return f"{text}.{micros:06d}" if micros else text


def format_cell(value: object) -> str | None:
    if value is None:
        return None
    if isinstance(value, bytes | bytearray):
        # BINARY, BLOB, BIT. Текст бол текстээр, үгүй бол `mysql` CLI-ийн
        # `--binary-as-hex` шиг.
        try:
            text = bytes(value).decode("utf-8")
            if any(ord(char) < 32 and char not in "\t\n\r" for char in text):
                raise UnicodeDecodeError("utf-8", b"", 0, 1, "control character")
        except UnicodeDecodeError:
            text = "0x" + bytes(value).hex().upper()
    elif isinstance(value, datetime.timedelta):
        text = _format_time(value)
    elif isinstance(value, datetime.datetime):
        text = value.isoformat(sep=" ")
    elif isinstance(value, float):
        text = repr(value)
    elif isinstance(value, set | frozenset):
        text = ",".join(sorted(str(item) for item in value))
    else:
        text = str(value)

    if len(text) > settings.max_cell_chars:
        text = text[: settings.max_cell_chars] + "…"
    return text


def _error_payload(line: int | None, error: pymysql.err.MySQLError) -> JSON:
    args = error.args
    code = args[0] if args and isinstance(args[0], int) else None
    message = str(args[1]) if len(args) > 1 else str(error)
    return {
        "line": line,
        "code": code,
        "sqlstate": getattr(error, "sqlstate", None),
        "message": message,
    }


def _add_result(state: RunState, result: JSON) -> None:
    if len(state.results) >= settings.max_result_sets:
        raise OutputLimitError
    state.results.append(result)


def _run_statement(
    connection: pymysql.connections.Connection,
    cursor: pymysql.cursors.SSCursor,
    statement: Statement,
    state: RunState,
    cancelled: threading.Event,
) -> None:
    started = time.perf_counter()
    cursor.execute(statement.text)
    added = False

    # `CALL` олон үр дүнгийн олонлог буцааж болно.
    while True:
        elapsed = lambda: round((time.perf_counter() - started) * 1000)  # noqa: E731
        if cursor.description is not None:
            columns = [column[0] for column in cursor.description]
            rows: list[list[str | None]] = []
            count = 0
            limited = False
            while (row := cursor.fetchone()) is not None:
                count += 1
                if count <= settings.max_rows:
                    cells = [format_cell(value) for value in row]
                    rows.append(cells)
                    state.output_chars += len(cells) + sum(len(cell) for cell in cells if cell)
                    if state.output_chars > settings.max_output_chars:
                        limited = True
                        break
                elif count >= settings.max_counted_rows:
                    limited = True
                    break

            if cancelled.is_set():
                return
            _add_result(
                state,
                {
                    "type": "rows",
                    "line": statement.line,
                    "columns": columns,
                    "rows": rows,
                    # Бүгдийг уншиж амжаагүй бол нийт тоо тодорхойгүй.
                    "row_count": None if limited else count,
                    "truncated": limited or count > settings.max_rows,
                    "warnings": [],
                    "duration_ms": elapsed(),
                },
            )
            added = True
            if limited:
                raise OutputLimitError
        else:
            if cancelled.is_set():
                return
            _add_result(
                state,
                {
                    "type": "ok",
                    "line": statement.line,
                    "affected_rows": cursor.rowcount or 0,
                    "warnings": [],
                    "duration_ms": elapsed(),
                },
            )
            added = True

        if not cursor.nextset():
            break

    # Бүх үр дүнг уншсаны дараа л асууна — дараагийнх хүлээгдэж байхад өөр
    # тушаал илгээвэл «Commands out of sync».
    if added and cursor.warning_count:
        state.results[-1]["warnings"] = [
            {"level": level, "code": code, "message": message}
            for level, code, message in connection.show_warnings()[:MAX_WARNINGS]
        ]


def _abandon(connection: pymysql.connections.Connection) -> None:
    """Socket-ийг шууд хаана — `cursor.close()` шиг үлдсэн мөрийг ЭЦЭС ХҮРТЭЛ уншихгүй.

    Дуусаагүй unbuffered үр дүнг дууссан гэж тэмдэглэнэ. Эс бөгөөс PyMySQL
    garbage collection-ий үед хаагдсан socket-оос уншихыг оролдож алдаа
    хэвлэдэг. Серверийн талын холболтыг `reset()` KILL хийнэ.
    """
    result = getattr(connection, "_result", None)
    if result is not None:
        result.unbuffered_active = False
    with contextlib.suppress(Exception):
        connection.close()


def execute(
    instance: MysqlInstance,
    statements: list[Statement],
    state: RunState,
    cancelled: threading.Event,
) -> None:
    """Thread дотор ажиллана. Үр дүнг `state`-д шууд бичнэ — тасалсан ч үлдэнэ."""
    try:
        connection = instance.connect(
            STUDENT_USER,
            cursorclass=pymysql.cursors.SSCursor,
            connect_timeout=5,
            # KILL ажиллахгүй тохиолдлын хамгаалалт.
            read_timeout=int(settings.run_timeout_seconds) + 30,
            write_timeout=30,
        )
    except pymysql.err.MySQLError as error:
        if not cancelled.is_set():
            state.error = _error_payload(None, error)
        return

    state.thread_id = connection.thread_id()
    try:
        cursor = connection.cursor()
        for statement in statements:
            if cancelled.is_set():
                return
            try:
                _run_statement(connection, cursor, statement, state, cancelled)
            except OutputLimitError:
                state.output_truncated = True
                return
            except pymysql.err.MySQLError as error:
                if not cancelled.is_set():
                    state.error = _error_payload(statement.line, error)
                return
    except Exception:
        logger.exception("SQL ажиллуулахад санаандгүй алдаа")
        if not cancelled.is_set():
            state.error = {
                "line": None,
                "code": None,
                "sqlstate": None,
                "message": "Үр дүнг уншихад алдаа гарлаа.",
            }
    finally:
        _abandon(connection)


async def run_script(instance: MysqlInstance, statements: list[Statement]) -> JSON:
    state = RunState()
    cancelled = threading.Event()
    started = time.perf_counter()
    task = asyncio.create_task(asyncio.to_thread(execute, instance, statements, state, cancelled))

    try:
        await asyncio.wait_for(asyncio.shield(task), settings.run_timeout_seconds)
    except TimeoutError:
        cancelled.set()
        state.timed_out = True
        if state.thread_id is not None:
            await asyncio.to_thread(instance.kill_query_connection, state.thread_id)
        try:
            await asyncio.wait_for(asyncio.shield(task), KILL_GRACE_SECONDS)
        except TimeoutError:
            logger.error("slot %d: KILL-д хариу өгсөнгүй — серверийг алж байна", instance.index)
            await asyncio.to_thread(instance.kill)

    return state.to_json(round((time.perf_counter() - started) * 1000))
