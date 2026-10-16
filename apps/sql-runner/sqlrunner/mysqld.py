"""Нэг MySQL сервер (slot)-ийн амьдралын мөчлөг.

Slot бүр өөрийн datadir, socket-тэй тусдаа `mysqld` процесс. Сүлжээ огт
нээхгүй (`skip-networking`) — зөвхөн энэ контейнер доторх unix socket.

ХОЁР ТҮВШНИЙ ЦЭВЭРЛЭГЭЭ
───────────────────────
`reset()` (~0.2 сек) — ажиллагаа бүрийн дараа. Сурагчийн холболт, XA
transaction, сан, хэрэглэгчийг устгаж, `student`-ийг анхны эрхтэй нь дахин
үүсгээд жишээ сангуудыг ачаална. Дараа нь үр дүнг ШАЛГАНА.

`start()` (~1 сек) — процессыг алж, datadir-ийг image доторх цэвэр загвараас
хуулж дахин эхлүүлнэ. `reset()` амжилтгүй, шалгалт тэнцээгүй, процесс унасан
эсвэл `restart_every` удаа ажилласны дараа. Datadir-ийг хаядаг тул mysqld-ийг
зөв унтраах шаардлагагүй — шууд SIGKILL.
"""

import contextlib
import logging
import shutil
import subprocess
import time
from functools import cache
from pathlib import Path

import pymysql

from sqlrunner.settings import settings
from sqlrunner.splitter import split_statements

logger = logging.getLogger("uvicorn.error")

ADMIN_USER = "root"
STUDENT_USER = "student"
# Ажиллагаа бүрийн өмнө бэлэн байх жишээ сангууд, ачаалах дарааллаар. Хичээлийн
# анхны кодын хуулбар — `apps/api/tests/test_sql_run.py` тэнцүү эсэхийг шалгана.
# `nomiin_san`: Модул 20-ын «Тайлан ба индекс» өмнөх хичээлийн санг шаарддаг.
# `medleg_hot` — «Өгөгдлийн Сангийн Үндэс (MySQL)» сургалтын мөрдөгчийн хэргүүдийн
# сан (`apps/api/app/content/sql/cases.py`). Ажиллуулалт бүрийн дараа бүх сан
# дахин ачаалагддаг тул жижиг байлгана (~45 KB).
SAMPLE_SCRIPTS = ("delguur.sql", "nomiin_san.sql", "medleg_hot.sql")
SAMPLE_SCHEMAS = frozenset({"delguur", "nomiin_san", "medleg_hot"})

SYSTEM_SCHEMAS = frozenset({"mysql", "sys", "information_schema", "performance_schema"})
SYSTEM_ACCOUNTS = frozenset({"root", "mysql.sys", "mysql.session", "mysql.infoschema"})
# SHOW PROCESSLIST-д харагдах, сурагчийнх биш холболтууд.
SYSTEM_THREAD_USERS = frozenset({ADMIN_USER, "event_scheduler", "system user"})

# Сурагчийн эрх. Хичээлүүд сан, хэрэглэгч, role үүсгэж GRANT хийдэг тул эдгээр
# хэрэгтэй. ЗОРИУД ХАССАН нь:
#   - SYSTEM_USER — байхгүй тул root-ийг өөрчлөх, устгах, root-ийг role болгон
#     өөртөө олгох, root-ийн холболтыг KILL хийх боломжгүй.
#   - `mysql`, `sys` схем дээрх partial revoke — эрхийн хүснэгтийг шууд засахгүй.
#     `mysql`-ийг зөвхөн УНШИНА: Модул 18-ийн `SHOW GRANTS FOR 'бусад'@'…'`,
#     `SELECT … FROM mysql.user`. Sandbox-д нууц мэдээлэл байхгүй.
#   - FILE, SUPER, SYSTEM_VARIABLES_ADMIN, SET_ANY_DEFINER, RELOAD, SHUTDOWN,
#     PROCESS, CREATE TABLESPACE — файл, глобал тохиргоо, бусдын DEFINER.
# Сурагч өөрийн эрхийг REVOKE хийж чадна — тиймээс `reset()` бүрт дахин үүсгэнэ.
STUDENT_SETUP = (
    f"CREATE USER '{STUDENT_USER}'@'localhost' WITH MAX_USER_CONNECTIONS 2",
    "GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, REFERENCES, INDEX, ALTER, "
    "CREATE TEMPORARY TABLES, LOCK TABLES, EXECUTE, CREATE VIEW, SHOW VIEW, "
    "CREATE ROUTINE, ALTER ROUTINE, EVENT, TRIGGER, CREATE USER, CREATE ROLE, DROP ROLE "
    f"ON *.* TO '{STUDENT_USER}'@'localhost' WITH GRANT OPTION",
    # Модул 18: `GRANT 'role' TO 'user'`. SYSTEM_USER-гүй тул системийн данс
    # (root г.м.)-ыг role болгон олгож чадахгүй — `tests/test_sandbox.py` шалгана.
    f"GRANT ROLE_ADMIN ON *.* TO '{STUDENT_USER}'@'localhost'",
    f"REVOKE ALL ON mysql.* FROM '{STUDENT_USER}'@'localhost'",
    f"GRANT SELECT ON mysql.* TO '{STUDENT_USER}'@'localhost'",
    f"REVOKE ALL ON sys.* FROM '{STUDENT_USER}'@'localhost'",
)


def quote_identifier(name: str) -> str:
    return "`" + name.replace("`", "``") + "`"


def config_text(*, datadir: Path, socket: Path, pid_file: Path, tmp_dir: Path, log: Path) -> str:
    """Бага санах ой, сүлжээгүй, файлын импорт/экспортгүй сервер."""
    return f"""\
[mysqld]
datadir={datadir}
socket={socket}
pid-file={pid_file}
tmpdir={tmp_dir}
log-error={log}
log_error_verbosity=2
skip-networking
skip-name-resolve
mysqlx=OFF
skip-log-bin
performance_schema=OFF
event_scheduler=OFF
partial_revokes=ON
local_infile=OFF
secure_file_priv=NULL
max_connections=6
max_allowed_packet=4M
max_execution_time=30000
innodb_buffer_pool_size=32M
innodb_redo_log_capacity=16M
innodb_log_buffer_size=4M
innodb_temp_data_file_path=ibtmp1:12M:autoextend:max:128M
temptable_max_ram=32M
temptable_max_mmap=64M
tmp_table_size=16M
max_heap_table_size=16M
table_open_cache=256
thread_cache_size=0
"""


@cache
def sample_statements() -> tuple[str, ...]:
    statements: list[str] = []
    for name in SAMPLE_SCRIPTS:
        text = (settings.sample_dir / name).read_text(encoding="utf-8")
        statements.extend(statement.text for statement in split_statements(text))
    return tuple(statements)


class SandboxError(RuntimeError):
    """Сервер эхлэх, цэвэрлэх, шалгалт давахад алдаа гарлаа."""


class MysqlInstance:
    def __init__(self, index: int, *, base: Path | None = None, datadir: Path | None = None):
        self.index = index
        self.base = base or settings.work_dir / f"sqlrunner-slot{index}"
        self.datadir = datadir or self.base / "data"
        self.process: subprocess.Popen[bytes] | None = None
        self.runs = 0

    @property
    def socket(self) -> Path:
        return self.base / "mysqld.sock"

    @property
    def config(self) -> Path:
        return self.base / "my.cnf"

    @property
    def log(self) -> Path:
        return self.base / "error.log"

    def connect(self, user: str, **kwargs: object) -> pymysql.connections.Connection:
        return pymysql.connect(
            unix_socket=str(self.socket),
            user=user,
            password="",
            charset="utf8mb4",
            autocommit=True,
            **kwargs,
        )

    # --- Процесс ---------------------------------------------------------------

    def _write_config(self) -> None:
        (self.base / "tmp").mkdir(parents=True, exist_ok=True)
        self.config.write_text(
            config_text(
                datadir=self.datadir,
                socket=self.socket,
                pid_file=self.base / "mysqld.pid",
                tmp_dir=self.base / "tmp",
                log=self.log,
            ),
            encoding="utf-8",
        )

    def initialize(self) -> None:
        """Хоосон datadir үүсгэнэ. Зөвхөн image бүтээх үед (`prewarm`)."""
        shutil.rmtree(self.datadir, ignore_errors=True)
        self._write_config()
        result = subprocess.run(
            [settings.mysqld, f"--defaults-file={self.config}", "--initialize-insecure"],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            raise SandboxError(f"mysqld --initialize амжилтгүй:\n{self._log_tail()}")

    def launch(self) -> None:
        self._write_config()
        self.process = subprocess.Popen(
            [settings.mysqld, f"--defaults-file={self.config}"],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        deadline = time.monotonic() + settings.startup_timeout_seconds
        while True:
            if self.process.poll() is not None:
                raise SandboxError(
                    f"slot {self.index}: mysqld эхэлж чадсангүй:\n{self._log_tail()}"
                )
            try:
                self.connect(ADMIN_USER, connect_timeout=2).close()
                return
            except pymysql.err.OperationalError:
                if time.monotonic() > deadline:
                    self.kill()
                    raise SandboxError(
                        f"slot {self.index}: mysqld хугацаандаа бэлэн болсонгүй"
                    ) from None
            time.sleep(0.05)

    def start(self) -> None:
        """Цэвэр загвараас эхлүүлнэ. Өмнөх процесс, datadir-ийг хаяна."""
        self.kill()
        shutil.rmtree(self.base, ignore_errors=True)
        self.base.mkdir(parents=True)
        shutil.copytree(settings.template_dir, self.datadir, symlinks=True)
        self.launch()
        self.runs = 0

    def kill(self) -> None:
        if self.process is None:
            return
        if self.process.poll() is None:
            self.process.kill()
            self.process.wait()
        self.process = None

    def shutdown(self) -> None:
        """Зөв унтраана — datadir-ийг загвар болгон хадгалах үед (`prewarm`)."""
        if self.process is None:
            return
        with self.connect(ADMIN_USER) as connection, connection.cursor() as cursor:
            cursor.execute("SHUTDOWN")
        try:
            self.process.wait(timeout=60)
        except subprocess.TimeoutExpired:
            self.kill()
            raise SandboxError("mysqld зөв унтарсангүй") from None
        self.process = None

    def alive(self) -> bool:
        return self.process is not None and self.process.poll() is None

    def _log_tail(self, lines: int = 20) -> str:
        try:
            return "\n".join(self.log.read_text(errors="replace").splitlines()[-lines:])
        except OSError:
            return "(error log байхгүй)"

    # --- Сурагчийн ажиллагаа ---------------------------------------------------

    def kill_query_connection(self, thread_id: int) -> None:
        """Хугацаа хэтэрсэн сурагчийн холболтыг таслана."""
        # Аль хэдийн дууссан (1094 Unknown thread id) бол алдаа биш.
        with (
            contextlib.suppress(pymysql.err.MySQLError),
            self.connect(ADMIN_USER, connect_timeout=2) as connection,
            connection.cursor() as cursor,
        ):
            cursor.execute("KILL %s", (thread_id,))

    def reset(self) -> None:
        """Сурагчийн өөрчлөлтийг бүгдийг устгаж, анхны төлөвт оруулна."""
        admin = self.connect(ADMIN_USER, connect_timeout=2, read_timeout=15, write_timeout=15)
        with admin, admin.cursor() as cursor:
            # Түгжээ хүлээж гацвал хурдан унаж, `start()` руу шилжинэ.
            cursor.execute("SET SESSION lock_wait_timeout = 5")

            cursor.execute("SHOW PROCESSLIST")
            for row in cursor.fetchall():
                thread_id, user = row[0], row[1]
                if user not in SYSTEM_THREAD_USERS and thread_id != admin.thread_id():
                    with contextlib.suppress(pymysql.err.MySQLError):
                        cursor.execute("KILL %s", (thread_id,))

            # Холболт тасарсны дараа ч үлддэг, түгжээ барьдаг цорын ганц зүйл.
            cursor.execute("XA RECOVER CONVERT XID")
            for format_id, gtrid_length, _bqual_length, data in cursor.fetchall():
                xid = bytes.fromhex(str(data)[2:])
                gtrid, bqual = xid[:gtrid_length], xid[gtrid_length:]
                cursor.execute(f"XA ROLLBACK X'{gtrid.hex()}',X'{bqual.hex()}',{int(format_id)}")

            cursor.execute("SELECT SCHEMA_NAME FROM information_schema.SCHEMATA")
            for (schema,) in cursor.fetchall():
                if schema not in SYSTEM_SCHEMAS:
                    cursor.execute(f"DROP DATABASE {quote_identifier(schema)}")

            cursor.execute("SELECT User, Host FROM mysql.user")
            for user, host in cursor.fetchall():
                if user not in SYSTEM_ACCOUNTS:
                    cursor.execute("DROP USER %s@%s", (user, host))

            for statement in STUDENT_SETUP:
                cursor.execute(statement)

        # Сурагч өөрөө ачаалвал жишээ сангийн объектууд «энгийн» данснынх болж,
        # хичээлд `DROP DATABASE delguur` хийж дахин үүсгэх боломжтой хэвээр.
        student = self.connect(STUDENT_USER, connect_timeout=2, read_timeout=15)
        with student, student.cursor() as cursor:
            for statement in sample_statements():
                cursor.execute(statement)

        self.verify()

    def verify(self) -> None:
        admin = self.connect(ADMIN_USER, connect_timeout=2, read_timeout=15)
        with admin, admin.cursor() as cursor:
            cursor.execute("SELECT SCHEMA_NAME FROM information_schema.SCHEMATA")
            schemas = {row[0] for row in cursor.fetchall()}
            cursor.execute("SELECT User FROM mysql.user")
            users = {row[0] for row in cursor.fetchall()}
            cursor.execute("XA RECOVER")
            prepared = cursor.fetchall()

        expected_schemas = SYSTEM_SCHEMAS | SAMPLE_SCHEMAS
        # performance_schema=OFF үед ч INFORMATION_SCHEMA-д харагддаг.
        if schemas != expected_schemas:
            raise SandboxError(f"slot {self.index}: сан зөрүүтэй: {sorted(schemas)}")
        if users != SYSTEM_ACCOUNTS | {STUDENT_USER}:
            raise SandboxError(f"slot {self.index}: хэрэглэгч зөрүүтэй: {sorted(users)}")
        if prepared:
            raise SandboxError(f"slot {self.index}: XA transaction үлдсэн")
