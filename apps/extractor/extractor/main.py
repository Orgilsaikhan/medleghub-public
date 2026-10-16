"""Задлагч үйлчилгээний HTTP API.

Зөвхөн MedlegHub API хандана — хэрэглэгчийн хөтөч шууд хандахгүй. Нэвтрэлт,
эрх, квот, хурдны хязгаарыг API шалгана. Энэ үйлчилгээ зөвхөн задална.

  POST /extract?kind=pdf|pptx|docx   (бие нь файлын байт)

Хүсэлт бүр:
  • Бие нь хэмжээ тоолж уншигдана — Content-Length-д сохроор итгэхгүй.
  • /tmp (tmpfs)-д түр файл болж, дууссаны дараа ҮРГЭЛЖ устгагдана.
  • Тусдаа дэд процесст (`extractor.worker`) задрагдана: цөөн орчин,
    нөөцийн хязгаар, нийт хугацаа хэтэрвэл процессын бүлгийг устгана.
  • Зэрэг ажиллах тоо хязгаартай, дараалалд удаан хүлээвэл 503.
"""

import asyncio
import contextlib
import json
import logging
import os
import re
import signal
import sys
import tempfile
import time
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from extractor.settings import SERVICE_ROOT, settings

logger = logging.getLogger("uvicorn.error")

KINDS = frozenset({"pdf", "pptx", "docx"})
RESULT_FIELDS = ("kind", "page_count", "pages", "truncated")
# 422-ийн алдааны кодууд — API эдгээрийг л мэднэ. Дэд процесс өөр код буцаавал `corrupt`.
FILE_ERRORS = frozenset(
    {"too_many_pages", "encrypted", "macro_enabled", "legacy_format", "corrupt", "timeout"}
)
_SAFE_DETAIL = re.compile(r"[A-Za-z0-9_\-]{1,64}")


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    if os.access(SERVICE_ROOT, os.W_OK):
        logger.warning(
            "Задлагчийн код (%s) бичигдэх боломжтой байна — контейнерийг read-only root "
            "filesystem-тэй ажиллуулна уу (docker run --read-only --tmpfs /tmp).",
            SERVICE_ROOT,
        )
    yield


app = FastAPI(
    title="MedlegHub Extractor",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
    lifespan=lifespan,
)

slots = asyncio.Semaphore(settings.max_concurrency)


def worker_command(kind: str, path: str) -> list[str]:
    return [sys.executable, "-m", "extractor.worker", kind, path]


def _error(status: int, code: str, page_count: int | None = None) -> JSONResponse:
    content: dict[str, Any] = {"error": code}
    if page_count is not None:
        content["page_count"] = page_count
    return JSONResponse(status_code=status, content=content)


def _failure(code: str, detail: str | None = None) -> dict[str, Any]:
    return {"ok": False, "error": code, "page_count": None, "detail": detail}


async def _read_body(request: Request) -> bytes | None:
    """Биеийг хэмжээ тоолж уншина. Хязгаараас их бол None (үлдсэнийг уншихгүй)."""
    declared = request.headers.get("content-length")
    if declared and declared.isdigit() and int(declared) > settings.max_bytes:
        return None
    body = bytearray()
    async for chunk in request.stream():
        if len(body) + len(chunk) > settings.max_bytes:
            return None
        body.extend(chunk)
    return bytes(body)


def _write_temp(data: bytes) -> str:
    # mkstemp: 0600, давтагдашгүй нэр. Файлын нэр, агуулга log-д орохгүй.
    fd, path = tempfile.mkstemp(prefix="extract-", suffix=".bin", dir=settings.work_dir)
    try:
        with os.fdopen(fd, "wb") as file:
            file.write(data)
    except BaseException:
        with contextlib.suppress(OSError):
            os.unlink(path)
        raise
    return path


def _remove(path: str) -> None:
    with contextlib.suppress(FileNotFoundError):
        os.unlink(path)


def _kill(process: asyncio.subprocess.Process) -> None:
    # `start_new_session` тул pid нь бүлгийн дугаар — хүүхдүүд нь хамт үхнэ.
    with contextlib.suppress(ProcessLookupError):
        os.killpg(process.pid, signal.SIGKILL)


async def _read_bounded(stream: asyncio.StreamReader, limit: int) -> tuple[bytes, bool]:
    data = bytearray()
    while chunk := await stream.read(65536):
        data.extend(chunk)
        if len(data) > limit:
            return bytes(data[:limit]), True
    return bytes(data), False


async def run_worker(kind: str, path: str) -> dict[str, Any]:
    """Дэд процессыг ажиллуулж JSON үр дүнг (эсвэл алдааг) буцаана."""
    process = await asyncio.create_subprocess_exec(
        *worker_command(kind, path),
        cwd=SERVICE_ROOT,
        env=settings.child_environment(),
        stdin=asyncio.subprocess.DEVNULL,
        stdout=asyncio.subprocess.PIPE,
        # PDFium-ийн анхааруулга, traceback-д файлын хэсэг орж болзошгүй — хаяна.
        stderr=asyncio.subprocess.DEVNULL,
        start_new_session=True,
    )
    assert process.stdout is not None

    try:
        async with asyncio.timeout(settings.timeout_seconds):
            output, flooded = await _read_bounded(process.stdout, settings.max_output_bytes)
            if flooded:
                _kill(process)
            returncode = await process.wait()
    except TimeoutError:
        return _failure("timeout", "wall_clock")
    finally:
        if process.returncode is None:
            _kill(process)
            await process.wait()

    if flooded:
        return _failure("corrupt", "output_too_large")
    # RLIMIT_CPU: soft хязгаарт SIGXCPU, hard-д SIGKILL. SIGKILL нь контейнерийн
    # санах ой дуусахад (OOM) ч ирдэг — хоёуланг нь «хэт удаан/хүнд» гэж үзнэ.
    if returncode in (-signal.SIGXCPU, -signal.SIGKILL):
        return _failure("timeout", "cpu")
    if returncode != 0:
        return _failure("corrupt", f"exit_{returncode}")
    try:
        result = json.loads(output)
    except ValueError:
        return _failure("corrupt", "bad_json")
    if not isinstance(result, dict) or not isinstance(result.get("ok"), bool):
        return _failure("corrupt", "bad_json")
    if result["ok"] and not all(key in result for key in RESULT_FIELDS):
        return _failure("corrupt", "bad_json")
    if not result["ok"] and not isinstance(result.get("error"), str):
        return _failure("corrupt", "bad_json")
    return result


@app.post("/extract")
async def extract_endpoint(request: Request, kind: str = "") -> JSONResponse:
    if kind not in KINDS:
        return _error(422, "unsupported")

    body = await _read_body(request)
    if body is None:
        logger.info("extract kind=%s outcome=too_large", kind)
        return _error(413, "too_large")
    size = len(body)

    try:
        path = await asyncio.to_thread(_write_temp, body)
    except OSError as error:
        # tmpfs дүүрсэн — олон том файл дараалалд хүлээж байна.
        logger.warning("extract kind=%s bytes=%d outcome=busy detail=%s", kind, size, error.errno)
        return _error(503, "busy")
    del body

    started = time.perf_counter()
    try:
        try:
            async with asyncio.timeout(settings.queue_timeout_seconds):
                await slots.acquire()
        except TimeoutError:
            logger.warning("extract kind=%s bytes=%d outcome=busy", kind, size)
            return _error(503, "busy")
        try:
            result = await run_worker(kind, path)
        finally:
            slots.release()
    finally:
        _remove(path)

    elapsed = (time.perf_counter() - started) * 1000
    if result["ok"]:
        logger.info(
            "extract kind=%s bytes=%d outcome=ok pages=%d truncated=%s ms=%.0f",
            kind,
            size,
            result["page_count"],
            result["truncated"],
            elapsed,
        )
        return JSONResponse({key: result[key] for key in RESULT_FIELDS})

    code = result["error"] if result["error"] in FILE_ERRORS else "corrupt"
    page_count = result.get("page_count")
    page_count = page_count if type(page_count) is int else None
    detail = result.get("detail")
    # Дэд процессын мөр log-д шууд орохгүй — зөвхөн энгийн тэмдэгт.
    detail = detail if isinstance(detail, str) and _SAFE_DETAIL.fullmatch(detail) else None
    logger.info(
        "extract kind=%s bytes=%d outcome=%s detail=%s ms=%.0f",
        kind,
        size,
        code,
        detail,
        elapsed,
    )
    return _error(422, code, page_count)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
