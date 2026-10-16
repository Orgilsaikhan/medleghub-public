"""MySQL кодыг тусдаа SQL ажиллуулагч үйлчилгээ рүү дамжуулна.

Backend өөрөө SQL ажиллуулдаггүй. `apps/sql-runner` нь нууц мэдээлэлгүй,
гадагшаа сүлжээгүй тусдаа контейнерт MySQL сервер ажиллуулж, ажиллагаа бүрийн
дараа цэвэрлэдэг. Тиймээс сурагчийн SQL нь API-ийн PostgreSQL сан, JWT нууцад
хүрэхгүй.
"""

from collections.abc import AsyncGenerator

import httpx
from pydantic import ValidationError

from app.core.config import settings
from app.core.errors import AppError
from app.schemas.sql_run import SqlRunResponse

RUNNER_ERROR_MESSAGE = "Кодыг ажиллуулахад алдаа гарлаа. Дараа дахин оролдоно уу."


async def get_sql_runner_client() -> AsyncGenerator[httpx.AsyncClient, None]:
    """Ажиллуулагч руу хандах client. Тестэд `httpx.MockTransport`-оор солино."""
    async with httpx.AsyncClient(
        base_url=settings.sql_runner_url,
        timeout=settings.sql_run_timeout_seconds,
    ) as client:
        yield client


async def run_sql(client: httpx.AsyncClient, source: str) -> SqlRunResponse:
    try:
        response = await client.post("/run", json={"source": source})
    except httpx.TimeoutException as exc:
        raise AppError(
            504,
            "SQL_RUN_TIMEOUT",
            "Код хэт удаан ажиллалаа. Кодоо хялбарчлаад дахин оролдоно уу.",
        ) from exc
    except httpx.HTTPError as exc:
        raise AppError(
            503,
            "SQL_RUNNER_UNAVAILABLE",
            "SQL сервертэй холбогдож чадсангүй. Түр хүлээгээд дахин оролдоно уу.",
        ) from exc

    if response.status_code == 200:
        try:
            return SqlRunResponse.model_validate_json(response.content)
        except ValidationError as exc:
            raise AppError(502, "SQL_RUNNER_ERROR", RUNNER_ERROR_MESSAGE) from exc
    if response.status_code == 413:
        raise AppError(413, "SOURCE_TOO_LARGE", "Код хэт урт байна.")
    if response.status_code == 503:
        raise AppError(
            503,
            "SQL_RUNNER_BUSY",
            "SQL сервер завгүй байна. Түр хүлээгээд дахин оролдоно уу.",
        )

    raise AppError(502, "SQL_RUNNER_ERROR", RUNNER_ERROR_MESSAGE)
