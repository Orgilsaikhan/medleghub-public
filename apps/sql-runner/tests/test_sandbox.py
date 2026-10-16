"""Жинхэнэ MySQL-тэй тестүүд — зөвхөн Docker image дотор ажиллана.

    docker build --target test -t medleghub-sql-runner-test apps/sql-runner
    docker run --rm --read-only --tmpfs /tmp:size=2g medleghub-sql-runner-test

`mysqld` эсвэл `prewarm`-ийн загвар байхгүй орчинд бүгд алгасагдана.
"""

import asyncio
import shutil
from collections.abc import AsyncGenerator, Iterator
from pathlib import Path

import httpx
import pymysql
import pytest

from sqlrunner import main
from sqlrunner.executor import run_script
from sqlrunner.mysqld import ADMIN_USER, STUDENT_USER, MysqlInstance
from sqlrunner.pool import SlotPool
from sqlrunner.settings import settings
from sqlrunner.splitter import split_statements

pytestmark = pytest.mark.skipif(
    shutil.which(settings.mysqld) is None or not settings.template_dir.is_dir(),
    reason="mysqld эсвэл загвар байхгүй — Docker image дотор ажиллуулна",
)


@pytest.fixture(scope="module")
def instance(tmp_path_factory: pytest.TempPathFactory) -> Iterator[MysqlInstance]:
    server = MysqlInstance(0, base=tmp_path_factory.mktemp("slot"))
    server.start()
    yield server
    server.kill()


@pytest.fixture(autouse=True)
def clean_slot(request: pytest.FixtureRequest) -> Iterator[None]:
    """Тест бүр цэвэр серверээс эхэлнэ — `reset()`-ийг давхар шалгана."""
    yield
    if "instance" in request.fixturenames:
        request.getfixturevalue("instance").reset()


def query(instance: MysqlInstance, sql: str, user: str = STUDENT_USER) -> tuple:
    with instance.connect(user) as connection, connection.cursor() as cursor:
        cursor.execute(sql)
        return cursor.fetchall()


async def run(instance: MysqlInstance, source: str) -> dict:
    return await run_script(instance, split_statements(source))


# --- Эрх ----------------------------------------------------------------------


def test_student_can_do_what_lessons_need(instance: MysqlInstance) -> None:
    with instance.connect(STUDENT_USER) as connection, connection.cursor() as cursor:
        cursor.execute("CREATE DATABASE tur_zagvar")
        cursor.execute("CREATE USER 'delguur_app'@'localhost' IDENTIFIED BY 'Jishee#NuutsUg2024'")
        cursor.execute("CREATE ROLE 'delguur_unshigch'")
        cursor.execute("GRANT SELECT ON delguur.* TO 'delguur_unshigch'")
        cursor.execute("GRANT 'delguur_unshigch' TO 'delguur_app'@'localhost'")
        cursor.execute("GRANT INSERT ON delguur.zahialga TO 'delguur_app'@'localhost'")
        cursor.execute("SHOW GRANTS FOR 'delguur_app'@'localhost'")
        assert len(cursor.fetchall()) >= 2
        cursor.execute("SELECT COUNT(*) FROM mysql.user")
        assert cursor.fetchone()[0] > 0
        # Жишээ санг устгаж дахин үүсгэх нь Модул 1-ийн хичээл.
        cursor.execute("DROP DATABASE delguur")


@pytest.mark.parametrize(
    "sql",
    [
        "ALTER USER 'root'@'localhost' IDENTIFIED BY 'x'",
        "DROP USER 'root'@'localhost'",
        "GRANT 'root'@'localhost' TO 'student'@'localhost'",
        "GRANT SYSTEM_USER ON *.* TO 'student'@'localhost'",
        "UPDATE mysql.user SET authentication_string = '' WHERE user = 'root'",
        "CREATE TABLE mysql.evil (id INT)",
        "SET GLOBAL max_connections = 1000",
        "SET PERSIST max_connections = 1000",
        "SELECT 1 INTO OUTFILE '/tmp/x.txt'",
        "CREATE DEFINER = 'root'@'localhost' PROCEDURE delguur.p() SELECT 1",
        "CREATE TABLESPACE ts ADD DATAFILE 'ts.ibd'",
        "SHUTDOWN",
    ],
)
def test_student_cannot_escape_the_sandbox(instance: MysqlInstance, sql: str) -> None:
    with pytest.raises(pymysql.err.MySQLError):
        query(instance, sql)


def test_student_cannot_read_files(instance: MysqlInstance) -> None:
    assert query(instance, "SELECT LOAD_FILE('/etc/passwd')") == ((None,),)


def test_student_cannot_kill_admin_connections(instance: MysqlInstance) -> None:
    with instance.connect(ADMIN_USER) as admin, pytest.raises(pymysql.err.MySQLError):
        query(instance, f"KILL {admin.thread_id()}")


# --- Цэвэрлэгээ ---------------------------------------------------------------


def test_reset_discards_everything_the_student_did(instance: MysqlInstance) -> None:
    with instance.connect(STUDENT_USER) as connection, connection.cursor() as cursor:
        cursor.execute("DELETE FROM delguur.zahialgiin_mur")
        cursor.execute("CREATE DATABASE tur_dadlaga")
        cursor.execute("CREATE USER 'hen_negen'@'%'")
        cursor.execute("REVOKE CREATE USER ON *.* FROM 'student'@'localhost'")
        # Холболт тасарсны дараа ч үлдэж, түгжээ барьдаг.
        cursor.execute("XA START 'uldsen'")
        cursor.execute("UPDATE delguur.baraa SET une = 0 WHERE baraa_id = 1")
        cursor.execute("XA END 'uldsen'")
        cursor.execute("XA PREPARE 'uldsen'")

    instance.reset()

    assert query(instance, "SELECT COUNT(*) FROM delguur.zahialgiin_mur") == ((19,),)
    assert query(instance, "SELECT une FROM delguur.baraa WHERE baraa_id = 1")[0][0] > 0
    # Модул 20-ын хоёр дахь төсөл өмнөх хичээлийн санг шаарддаг.
    assert query(instance, "SELECT COUNT(*) > 0 FROM nomiin_san.nom") == ((1,),)
    schemas = {row[0] for row in query(instance, "SHOW DATABASES")}
    assert "tur_dadlaga" not in schemas
    # Хассан эрх сэргэсэн.
    query(instance, "CREATE USER 'dahiad'@'localhost'")


def test_reset_restores_the_detective_case_database(instance: MysqlInstance) -> None:
    # Хэргүүд `medleg_hot`-ийн өгөгдлийг засаж (Хэрэг №6, 7), view-г солиж (№13),
    # trigger, функц, эрх (№16–18) нэмдэг — дараагийн ажиллагаанд үлдэх ёсгүй.
    with instance.connect(STUDENT_USER) as connection, connection.cursor() as cursor:
        cursor.execute("DELETE FROM medleg_hot.duudlaga")
        cursor.execute("DROP VIEW medleg_hot.v_sejigten")
        cursor.execute("DROP PROCEDURE medleg_hot.shono_ajil")
        cursor.execute("CREATE FUNCTION medleg_hot.f() RETURNS INT DETERMINISTIC RETURN 1")
        cursor.execute("CREATE ROLE 'hereg_unshigch'")

    instance.reset()

    assert query(instance, "SELECT COUNT(*) > 0 FROM medleg_hot.duudlaga") == ((1,),)
    objects = query(
        instance,
        "SELECT ROUTINE_NAME FROM information_schema.ROUTINES"
        " WHERE ROUTINE_SCHEMA = 'medleg_hot'"
        " UNION ALL SELECT TABLE_NAME FROM information_schema.VIEWS"
        " WHERE TABLE_SCHEMA = 'medleg_hot'",
    )
    assert sorted(row[0] for row in objects) == ["shono_ajil", "v_sejigten"]
    assert query(instance, "SELECT COUNT(*) FROM medleg_hot.v_sejigten")[0][0] > 0


def test_reset_survives_an_open_connection(instance: MysqlInstance) -> None:
    connection = instance.connect(STUDENT_USER)
    with connection.cursor() as cursor:
        cursor.execute("START TRANSACTION")
        cursor.execute("SELECT * FROM delguur.baraa FOR UPDATE")
        cursor.fetchall()

    instance.reset()  # Холболтыг KILL хийж, түгжээг чөлөөлнө.
    assert query(instance, "SELECT COUNT(*) FROM delguur.baraa") == ((12,),)
    connection.close()


# --- Ажиллуулагч --------------------------------------------------------------


async def test_select_returns_a_table(instance: MysqlInstance) -> None:
    outcome = await run(
        instance, "USE delguur;\n\nSELECT baraa_id, ner, une\nFROM baraa WHERE baraa_id <= 2;"
    )

    assert outcome["error"] is None
    use, select = outcome["results"]
    assert use["type"] == "ok"
    assert select["type"] == "rows"
    assert select["line"] == 3
    assert select["columns"] == ["baraa_id", "ner", "une"]
    assert select["rows"] == [
        ["1", "Ухаалаг утас", "1250000.00"],
        ["2", "Зөөврийн компьютер", "3200000.00"],
    ]
    assert select["row_count"] == 2
    assert select["truncated"] is False


async def test_procedure_with_delimiter_and_several_result_sets(instance: MysqlInstance) -> None:
    source = """\
USE delguur;
DELIMITER $$
CREATE PROCEDURE hoyor()
BEGIN
    SELECT COUNT(*) AS angilal FROM angilal;
    SELECT COUNT(*) AS baraa FROM baraa;
END$$
DELIMITER ;
CALL hoyor();
"""
    outcome = await run(instance, source)

    assert outcome["error"] is None
    tables = [result for result in outcome["results"] if result["type"] == "rows"]
    assert [table["rows"] for table in tables] == [[["5"]], [["12"]]]
    assert all(table["line"] == 9 for table in tables)


async def test_stops_at_the_first_error(instance: MysqlInstance) -> None:
    outcome = await run(instance, "USE delguur;\nSELECT * FROM baihgui;\nSELECT 1;")

    assert len(outcome["results"]) == 1
    assert outcome["error"]["line"] == 2
    assert outcome["error"]["code"] == 1146
    assert outcome["error"]["sqlstate"] == "42S02"
    assert "baihgui" in outcome["error"]["message"]


async def test_timeout_kills_the_query(
    instance: MysqlInstance, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(settings, "run_timeout_seconds", 1.0)

    outcome = await run(instance, "SELECT 1;\nSELECT SLEEP(30);")

    assert outcome["timed_out"] is True
    assert outcome["error"] is None
    assert len(outcome["results"]) == 1
    assert outcome["duration_ms"] < 8000


async def test_rows_beyond_the_limit_are_only_counted(
    instance: MysqlInstance, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(settings, "max_rows", 5)

    outcome = await run(
        instance,
        "WITH RECURSIVE n (i) AS (SELECT 1 UNION ALL SELECT i + 1 FROM n WHERE i < 50) "
        "SELECT i FROM n;",
    )

    (table,) = outcome["results"]
    assert len(table["rows"]) == 5
    assert table["row_count"] == 50
    assert table["truncated"] is True
    assert outcome["output_truncated"] is False


async def test_huge_results_stop_the_run(
    instance: MysqlInstance, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(settings, "max_counted_rows", 100)

    outcome = await run(
        instance,
        "WITH RECURSIVE n (i) AS (SELECT 1 UNION ALL SELECT i + 1 FROM n WHERE i < 900) "
        "SELECT i FROM n;\nSELECT 'ажиллах ёсгүй';",
    )

    assert outcome["output_truncated"] is True
    (table,) = outcome["results"]
    assert table["row_count"] is None


async def test_cells_are_formatted_like_the_mysql_client(instance: MysqlInstance) -> None:
    outcome = await run(
        instance,
        "SELECT NULL, CAST('2024-01-02 03:04:05' AS DATETIME), CAST('-01:02:03' AS TIME), "
        "1.50, b'101', 'текст', 0.1e0, CAST('{\"a\": 1}' AS JSON);",
    )

    (table,) = outcome["results"]
    assert table["rows"] == [
        [None, "2024-01-02 03:04:05", "-01:02:03", "1.50", "0x05", "текст", "0.1", '{"a": 1}']
    ]


async def test_warnings_are_reported(instance: MysqlInstance) -> None:
    outcome = await run(instance, "SELECT CAST('12abc' AS SIGNED) AS too;")

    (table,) = outcome["results"]
    assert table["rows"] == [["12"]]
    assert table["warnings"][0]["code"] == 1292


# --- Pool ба HTTP -------------------------------------------------------------


@pytest.fixture
async def pool(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> AsyncGenerator[SlotPool, None]:
    monkeypatch.setattr(settings, "work_dir", tmp_path)
    slots = SlotPool(1)
    await slots.start()
    monkeypatch.setattr(main, "pool", slots)
    yield slots
    await slots.stop()


@pytest.fixture
async def client() -> AsyncGenerator[httpx.AsyncClient, None]:
    transport = httpx.ASGITransport(app=main.app)
    async with httpx.AsyncClient(
        transport=transport, base_url="http://sqlrunner", timeout=60
    ) as http:
        yield http


async def test_run_endpoint(pool: SlotPool, client: httpx.AsyncClient) -> None:
    response = await client.post(
        "/run", json={"source": "SELECT COUNT(*) AS n FROM delguur.baraa;"}
    )

    assert response.status_code == 200
    body = response.json()
    assert body["results"][0]["rows"] == [["12"]]
    assert body["error"] is None


async def test_changes_do_not_leak_to_the_next_run(
    pool: SlotPool, client: httpx.AsyncClient
) -> None:
    await client.post("/run", json={"source": "DELETE FROM delguur.zahialgiin_mur;"})

    response = await client.post(
        "/run", json={"source": "SELECT COUNT(*) FROM delguur.zahialgiin_mur;"}
    )

    assert response.json()["results"][0]["rows"] == [["19"]]


async def test_dead_server_is_restarted(pool: SlotPool, client: httpx.AsyncClient) -> None:
    await asyncio.sleep(0)
    pool.instances[0].kill()

    response = await client.post("/run", json={"source": "SELECT 1;"})

    assert response.status_code == 200
    assert response.json()["results"][0]["rows"] == [["1"]]


async def test_source_too_large(pool: SlotPool, client: httpx.AsyncClient) -> None:
    response = await client.post("/run", json={"source": "-" * (settings.max_source_bytes + 1)})

    assert response.status_code == 413
    assert response.json() == {"code": "SOURCE_TOO_LARGE"}


async def test_split_error_is_a_normal_result(pool: SlotPool, client: httpx.AsyncClient) -> None:
    response = await client.post("/run", json={"source": "DELIMITER\nSELECT 1;"})

    assert response.status_code == 200
    assert response.json()["error"]["line"] == 1


async def test_busy_when_every_slot_is_taken(
    pool: SlotPool, client: httpx.AsyncClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(settings, "queue_timeout_seconds", 0.2)

    async with pool.acquire():
        response = await client.post("/run", json={"source": "SELECT 1;"})

    assert response.status_code == 503
    assert response.json() == {"code": "SQL_RUNNER_BUSY"}


async def test_health(pool: SlotPool, client: httpx.AsyncClient) -> None:
    response = await client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
