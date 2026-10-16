"""FastAPI application entrypoint."""

import asyncio
import contextlib
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text

from app.api.router import api_router
from app.core.config import settings
from app.core.middleware import SecurityHeadersMiddleware
from app.db.session import SessionFactory, engine
from app.live import worker as live_worker
from app.live.pipeline import LiveContext
from app.live.storage import get_storage
from app.services import maintenance
from app.services.ai.service import AIService


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    settings.validate_production_secrets()
    tasks: list[asyncio.Task[None]] = []
    ai = AIService(SessionFactory)
    # Тестэд эдгээрийг тусад нь дуудна.
    if settings.environment != "test":
        # Товлосон бүртгэл устгах, хадгалах хугацаа мөрдүүлэх.
        tasks.append(asyncio.create_task(maintenance.run_forever()))
        # MedlegHub Live: материал задлах, AI-аар заавар, тест үүсгэх дараалал.
        context = LiveContext(sessions=SessionFactory, ai=ai, storage=get_storage())
        tasks.append(asyncio.create_task(live_worker.run_forever(context)))
    yield
    for task in tasks:
        task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await task
    await ai.aclose()
    await engine.dispose()


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    debug=settings.debug,
    lifespan=lifespan,
    docs_url=None if settings.is_production else "/docs",
    redoc_url=None,
    openapi_url=None if settings.is_production else "/openapi.json",
)

app.add_middleware(SecurityHeadersMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,  # httpOnly auth cookie дамжуулахад шаардлагатай
    # PUT — /me/avatar, /me/showcase, /billing/price, /community/posts/{id}/like
    # (локал вэб API-г өөр origin-оос дууддаг).
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
    max_age=600,
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
    """Pydantic-ийн алдааг бусад алдаатай ижил бүтэцтэй болгоно."""
    return JSONResponse(
        status_code=422,
        content={
            "detail": {
                "code": "VALIDATION_ERROR",
                "message": "Оруулсан утга буруу байна.",
                "fields": [
                    {
                        "field": ".".join(str(part) for part in err["loc"][1:]),
                        "message": err["msg"],
                    }
                    for err in exc.errors()
                ],
            }
        },
    )


@app.get("/health", tags=["system"])
async def health() -> dict[str, str]:
    """Liveness probe — гадаад хамаарал шалгахгүй."""
    return {"status": "ok", "environment": settings.environment}


@app.get("/health/db", tags=["system"])
async def health_db() -> dict[str, str]:
    """Readiness probe — өгөгдлийн сантай холбогдож чадаж байгааг шалгана."""
    async with engine.connect() as conn:
        await conn.execute(text("SELECT 1"))
    return {"status": "ok", "database": "reachable"}


app.include_router(api_router, prefix=settings.api_v1_prefix)
