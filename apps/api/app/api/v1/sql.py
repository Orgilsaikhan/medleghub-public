"""MySQL хичээлийн кодыг ажиллуулах."""

from typing import Annotated

import httpx
from fastapi import APIRouter, Depends

from app.core import rate_limit
from app.core.config import settings
from app.core.deps import CurrentUser
from app.core.errors import AppError, RateLimitError
from app.schemas.sql_run import SqlRunRequest, SqlRunResponse
from app.services.sql_run_service import get_sql_runner_client, run_sql

router = APIRouter(tags=["sql"])

SqlRunnerClient = Annotated[httpx.AsyncClient, Depends(get_sql_runner_client)]


async def limit_per_user(user: CurrentUser) -> None:
    """IP-гаар биш ХЭРЭГЛЭГЧЭЭР — нэг ангийн сурагчид нэг IP-ийн ард байдаг.

    `rate_limit.backend`-ийг дуудах мөчид нь уншина — тестэд солих боломжтой.
    """
    if not settings.rate_limit_enabled:
        return
    allowed, retry_after = rate_limit.backend.hit(
        f"sql:{user.id}",
        settings.sql_run_rate_limit_max,
        settings.sql_run_rate_limit_window_seconds,
    )
    if not allowed:
        raise RateLimitError(retry_after)


@router.post(
    "/sql/run",
    dependencies=[Depends(limit_per_user)],
    response_model=SqlRunResponse,
)
async def run_sql_code(
    payload: SqlRunRequest, _user: CurrentUser, client: SqlRunnerClient
) -> SqlRunResponse:
    """MySQL кодыг тусгаарлагдсан сервер дээр ажиллуулж үр дүнг буцаана.

    Backend кодыг АЖИЛЛУУЛАГЧ рүү дамжуулна, өөрөө ажиллуулахгүй. Ажиллагаа
    бүрийн дараа сервер жишээ сангуудтайгаа анхны төлөвт буцна — сурагчийн
    өөрчлөлт дараагийн ажиллагаанд үлдэхгүй.
    """
    if len(payload.source.encode("utf-8")) > settings.sql_run_max_source_bytes:
        raise AppError(413, "SOURCE_TOO_LARGE", "Код хэт урт байна.")

    return await run_sql(client, payload.source)
