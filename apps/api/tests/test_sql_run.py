"""MySQL ажиллуулагчийн proxy.

Жинхэнэ MySQL шаардахгүй — `apps/sql-runner` үйлчилгээг
`httpx.MockTransport`-оор орлуулна. Ажиллуулагчийн өөрийн тестүүд нь
`apps/sql-runner/tests` дотор байна.
"""

import json
from collections.abc import AsyncGenerator, Callable
from pathlib import Path

import httpx
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.content.sql import SQL_COURSE
from app.core.config import settings
from app.main import app
from app.services.sql_run_service import get_sql_runner_client
from tests.conftest import login_as, make_user

Handler = Callable[[httpx.Request], httpx.Response]

RESULT = {
    "results": [
        {
            "type": "ok",
            "line": 1,
            "affected_rows": 0,
            "warnings": [],
            "duration_ms": 0,
        },
        {
            "type": "rows",
            "line": 2,
            "columns": ["n"],
            "rows": [["12"]],
            "row_count": 1,
            "truncated": False,
            "warnings": [],
            "duration_ms": 1,
        },
    ],
    "error": None,
    "timed_out": False,
    "output_truncated": False,
    "duration_ms": 3,
}

SQL_ERROR = {
    "results": [],
    "error": {
        "line": 2,
        "code": 1146,
        "sqlstate": "42S02",
        "message": "Table 'delguur.baihgui' doesn't exist",
    },
    "timed_out": False,
    "output_truncated": False,
    "duration_ms": 1,
}

RUNNER_SANDBOX = Path(__file__).resolve().parents[2] / "sql-runner" / "sandbox"


def use_runner(handler: Handler) -> list[httpx.Request]:
    """Ажиллуулагчийн хариуг загварчилж, түүн рүү очсон хүсэлтүүдийг цуглуулна."""
    seen: list[httpx.Request] = []

    def record(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return handler(request)

    async def override() -> AsyncGenerator[httpx.AsyncClient, None]:
        async with httpx.AsyncClient(
            transport=httpx.MockTransport(record), base_url="http://sql-runner"
        ) as client:
            yield client

    # `client` fixture нь teardown-д бүх override-ыг цэвэрлэнэ.
    app.dependency_overrides[get_sql_runner_client] = override
    return seen


async def _signed_in(client: httpx.AsyncClient, api: str, db: AsyncSession) -> None:
    await make_user(db, "sql@suralts.mn")
    await login_as(client, api, "sql@suralts.mn")


def _ok(_: httpx.Request) -> httpx.Response:
    return httpx.Response(200, json=RESULT)


async def test_run_requires_login(client: httpx.AsyncClient, api: str) -> None:
    seen = use_runner(_ok)

    response = await client.post(f"{api}/sql/run", json={"source": "SELECT 1;"})

    assert response.status_code == 401
    assert seen == [], "Нэвтрээгүй хэрэглэгчийн код ажиллуулагч руу очих ёсгүй"


async def test_run_returns_results(client: httpx.AsyncClient, api: str, db: AsyncSession) -> None:
    seen = use_runner(_ok)
    await _signed_in(client, api, db)

    source = "USE delguur;\nSELECT COUNT(*) AS n FROM baraa;"
    response = await client.post(f"{api}/sql/run", json={"source": source})

    assert response.status_code == 200
    assert response.json() == RESULT

    # Хүсэлт ажиллуулагч руу өөрчлөгдөөгүй хүрсэн эсэх.
    assert len(seen) == 1
    assert json.loads(seen[0].content) == {"source": source}


async def test_sql_error_is_a_normal_response(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    use_runner(lambda _: httpx.Response(200, json=SQL_ERROR))
    await _signed_in(client, api, db)

    response = await client.post(f"{api}/sql/run", json={"source": "SELECT * FROM baihgui;"})

    assert response.status_code == 200
    assert response.json()["error"] == SQL_ERROR["error"]


async def test_source_too_large_is_not_forwarded(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    seen = use_runner(_ok)
    await _signed_in(client, api, db)

    # Кирилл үсэг UTF-8-д 2 байт — тэмдэгтийн тоо хязгаараас бага ч байт нь их.
    source = "Ө" * (settings.sql_run_max_source_bytes // 2 + 1)
    response = await client.post(f"{api}/sql/run", json={"source": source})

    assert response.status_code == 413
    assert response.json()["detail"]["code"] == "SOURCE_TOO_LARGE"
    assert seen == []


@pytest.mark.parametrize(
    ("runner_response", "status", "code"),
    [
        (httpx.Response(503, json={"code": "SQL_RUNNER_BUSY"}), 503, "SQL_RUNNER_BUSY"),
        (httpx.Response(413, json={"code": "SOURCE_TOO_LARGE"}), 413, "SOURCE_TOO_LARGE"),
        (httpx.Response(500, text="Internal Server Error"), 502, "SQL_RUNNER_ERROR"),
        # Эвдэрсэн хариу хөтөч рүү очих ёсгүй.
        (httpx.Response(200, json={"unexpected": True}), 502, "SQL_RUNNER_ERROR"),
    ],
)
async def test_runner_failures_are_mapped(
    client: httpx.AsyncClient,
    api: str,
    db: AsyncSession,
    runner_response: httpx.Response,
    status: int,
    code: str,
) -> None:
    use_runner(lambda _: runner_response)
    await _signed_in(client, api, db)

    response = await client.post(f"{api}/sql/run", json={"source": "SELECT 1;"})

    assert response.status_code == status
    assert response.json()["detail"]["code"] == code


@pytest.mark.parametrize(
    ("exception", "status", "code"),
    [
        (httpx.ConnectError("refused"), 503, "SQL_RUNNER_UNAVAILABLE"),
        (httpx.ReadTimeout("slow"), 504, "SQL_RUN_TIMEOUT"),
    ],
)
async def test_unreachable_runner(
    client: httpx.AsyncClient,
    api: str,
    db: AsyncSession,
    exception: httpx.HTTPError,
    status: int,
    code: str,
) -> None:
    def fail(_: httpx.Request) -> httpx.Response:
        raise exception

    use_runner(fail)
    await _signed_in(client, api, db)

    response = await client.post(f"{api}/sql/run", json={"source": "SELECT 1;"})

    assert response.status_code == status
    assert response.json()["detail"]["code"] == code


@pytest.mark.skipif(not RUNNER_SANDBOX.is_dir(), reason="apps/sql-runner байхгүй")
@pytest.mark.parametrize(
    ("slug", "script"),
    [
        ("delguur-san-mysql", "delguur.sql"),
        # Модул 20-ын «Тайлан ба индекс» энэ санг урьдчилсан нөхцөл болгодог.
        ("nomiin-san-zagvar-mysql", "nomiin_san.sql"),
    ],
)
def test_runner_sample_databases_match_the_lessons(slug: str, script: str) -> None:
    """Ажиллуулагч жишээ сангуудыг өөрийн хуулбараас ачаалдаг — хичээлтэй ижил байх ёстой."""
    lesson = next(
        lesson for module in SQL_COURSE.modules for lesson in module.lessons if lesson.slug == slug
    )

    runner_copy = (RUNNER_SANDBOX / script).read_text(encoding="utf-8").replace("\r\n", "\n")
    assert runner_copy == lesson.initial_code, (
        f"Хичээлийн {slug} скрипт өөрчлөгдсөн — "
        f"apps/sql-runner/sandbox/{script}-ийг мөн шинэчилнэ үү."
    )
