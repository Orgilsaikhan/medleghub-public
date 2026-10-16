"""Хөрвүүлэгч үйлчилгээний HTTP API.

Зөвхөн MedlegHub API хандана — сурагчийн хөтөч шууд хандахгүй. Нэвтрэлт ба
хурдны хязгаарыг API шалгана. Энэ үйлчилгээ зөвхөн хөрвүүлнэ.
"""

import asyncio
import logging
import os
import shutil
import time
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Literal

from fastapi import FastAPI
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel

from compiler.cache import SizedLRUCache, cache_key
from compiler.runner import Compiled, CompileTimeoutError, Outcome, compile_source
from compiler.settings import settings
from compiler.toolchain import TOOLCHAINS

logger = logging.getLogger("uvicorn.error")


def toolchain_root() -> Path | None:
    emcc = shutil.which("emcc")
    return Path(emcc).resolve().parent if emcc else None


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    # Upstream emsdk image хөрвүүлэгчийг хэн ч бичих эрхтэй ирүүлдэг. Зөвхөн
    # уншигдах файлын системгүй бол эвдэрсэн хөрвүүлэлт дараагийн сурагчдын
    # хөрвүүлэгчийг өөрчилж чадна.
    root = toolchain_root()
    if root is not None and os.access(root, os.W_OK):
        logger.warning(
            "Хөрвүүлэгч (%s) бичигдэх боломжтой байна — контейнерийг read-only root "
            "filesystem-тэй ажиллуулна уу (docker run --read-only --tmpfs /tmp).",
            root,
        )
    yield


app = FastAPI(
    title="MedlegHub Compiler",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
    lifespan=lifespan,
)

cache: SizedLRUCache[Outcome] = SizedLRUCache(settings.cache_bytes)
slots = asyncio.Semaphore(settings.max_concurrency)
in_flight: dict[str, asyncio.Task[Outcome]] = {}


class CompileRequest(BaseModel):
    language: Literal["c", "cpp"]
    source: str


class BusyError(Exception):
    """Бүх слот завгүй бөгөөд дараалалд хэт удаан хүлээлээ."""


def _error(status: int, code: str) -> JSONResponse:
    return JSONResponse(status_code=status, content={"code": code})


async def _compile(language: str, source: str) -> Outcome:
    try:
        async with asyncio.timeout(settings.queue_timeout_seconds):
            await slots.acquire()
    except TimeoutError:
        raise BusyError from None

    started = time.perf_counter()
    try:
        outcome = await compile_source(TOOLCHAINS[language], source)
    finally:
        slots.release()

    logger.info(
        "compile language=%s outcome=%s ms=%.0f",
        language,
        type(outcome).__name__,
        (time.perf_counter() - started) * 1000,
    )
    return outcome


async def _compile_and_remember(key: str, language: str, source: str) -> Outcome:
    outcome = await _compile(language, source)
    cache.put(key, outcome, outcome.size)
    return outcome


def _forget(key: str, task: asyncio.Task[Outcome]) -> None:
    in_flight.pop(key, None)
    # Хүлээгч бүгд тасарсан ч алдааг «уншаагүй» гэж анхааруулахгүй.
    if not task.cancelled():
        task.exception()


async def compile_once(key: str, language: str, source: str) -> tuple[Outcome, bool]:
    """Кэшээс эсвэл хөрвүүлж `(үр дүн, кэшээс_ирсэн_эсэх)` буцаана.

    Ижил кодыг зэрэг хөрвүүлэхгүй: анги бүхэлдээ нэг хичээлийг нэг мөчид
    ажиллуулсан ч хөрвүүлэлт нэг л удаа болж, бусад нь үр дүнг хүлээнэ.
    """
    cached = cache.get(key)
    if cached is not None:
        return cached, True

    task = in_flight.get(key)
    if task is None:
        task = asyncio.create_task(_compile_and_remember(key, language, source))
        in_flight[key] = task
        task.add_done_callback(lambda done: _forget(key, done))

    # Нэг хүсэлт тасарсан ч хөрвүүлэлт үргэлжилж, бусад хүлээгч үр дүнгээ авна.
    return await asyncio.shield(task), False


@app.post("/compile")
async def compile_endpoint(request: CompileRequest) -> Response:
    if len(request.source.encode("utf-8")) > settings.max_source_bytes:
        return _error(413, "SOURCE_TOO_LARGE")

    toolchain = TOOLCHAINS[request.language]
    key = cache_key(request.language, toolchain.flags, request.source)

    try:
        outcome, hit = await compile_once(key, request.language, request.source)
    except BusyError:
        return _error(503, "COMPILER_BUSY")
    except CompileTimeoutError:
        return _error(504, "COMPILE_TIMEOUT")

    headers = {"X-Compile-Cache": "hit" if hit else "miss"}
    if isinstance(outcome, Compiled):
        return Response(outcome.module, media_type="application/wasm", headers=headers)
    return JSONResponse(
        status_code=422,
        content={"code": "COMPILE_ERROR", "diagnostics": outcome.diagnostics},
        headers=headers,
    )


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
