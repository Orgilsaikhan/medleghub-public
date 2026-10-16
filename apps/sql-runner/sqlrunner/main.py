"""SQL ажиллуулагч үйлчилгээний HTTP API.

Зөвхөн MedlegHub API хандана — сурагчийн хөтөч шууд хандахгүй. Нэвтрэлт ба
хурдны хязгаарыг API шалгана. Энэ үйлчилгээ зөвхөн ажиллуулна.
"""

import logging
import time
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from sqlrunner.executor import empty_outcome, failure, run_script
from sqlrunner.pool import BusyError, SlotPool
from sqlrunner.settings import settings
from sqlrunner.splitter import SplitError, split_statements

logger = logging.getLogger("uvicorn.error")

pool: SlotPool | None = None


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    global pool
    started = SlotPool(settings.slots)
    await started.start()
    pool = started
    try:
        yield
    finally:
        pool = None
        await started.stop()


app = FastAPI(
    title="MedlegHub SQL Runner",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
    lifespan=lifespan,
)


class RunRequest(BaseModel):
    source: str


def _error(status: int, code: str) -> JSONResponse:
    return JSONResponse(status_code=status, content={"code": code})


@app.post("/run")
async def run_endpoint(request: RunRequest) -> JSONResponse:
    if len(request.source.encode("utf-8")) > settings.max_source_bytes:
        return _error(413, "SOURCE_TOO_LARGE")

    # Сурагчийн алдаа (DELIMITER, хэт олон statement) нь хэвийн хариу — console
    # дээр SQL алдаатай адил харагдана.
    try:
        statements = split_statements(request.source)
    except SplitError as error:
        return JSONResponse(failure(error.line, error.message))
    if len(statements) > settings.max_statements:
        return JSONResponse(
            failure(
                statements[settings.max_statements].line,
                f"Скриптэд хэт олон statement байна (дээд тал нь {settings.max_statements}).",
            )
        )
    if not statements:
        return JSONResponse(empty_outcome())

    if pool is None:
        return _error(503, "SQL_RUNNER_UNAVAILABLE")

    started = time.perf_counter()
    try:
        async with pool.acquire() as instance:
            outcome = await run_script(instance, statements)
    except BusyError:
        return _error(503, "SQL_RUNNER_BUSY")

    error = outcome["error"]
    logger.info(
        "run statements=%d results=%d error=%s timed_out=%s truncated=%s ms=%.0f",
        len(statements),
        len(outcome["results"]),
        error["code"] if error else None,
        outcome["timed_out"],
        outcome["output_truncated"],
        (time.perf_counter() - started) * 1000,
    )
    return JSONResponse(outcome)


@app.get("/health")
async def health() -> JSONResponse:
    if pool is None or not any(instance.alive() for instance in pool.instances):
        return JSONResponse(status_code=503, content={"status": "starting"})
    return JSONResponse({"status": "ok", "ready_slots": pool.ready_count})
