"""C/C++ хөрвүүлэлт.

Модулийн нэр нь `compile` биш — Python-ы суурь `compile()` функцийг
далдлахгүйн тулд.
"""

import gzip
from typing import Annotated

import httpx
from fastapi import APIRouter, Depends, Request, Response
from starlette.concurrency import run_in_threadpool

from app.core import rate_limit
from app.core.config import settings
from app.core.deps import CurrentUser
from app.core.errors import AppError, RateLimitError
from app.schemas.compile import CompileRequest
from app.services.compile_service import compile_source, get_compiler_client

router = APIRouter(tags=["compile"])

CompilerClient = Annotated[httpx.AsyncClient, Depends(get_compiler_client)]

# WebAssembly модуль gzip-ээр ~3 дахин багасна (C++ ~200 KB → ~67 KB). Жижиг
# хариуг шахах нь толгойн зардлаасаа ашиггүй.
GZIP_MIN_BYTES = 1024


async def limit_per_user(user: CurrentUser) -> None:
    """IP-гаар биш ХЭРЭГЛЭГЧЭЭР хязгаарлана.

    Нэг сургуулийн анги бүхэлдээ нэг IP хаягийн ард байдаг. IP-гаар
    хязгаарлавал нэг сурагч бүх ангийнхаа хөрвүүлэлтийг зогсооно.

    `rate_limit.backend`-ийг дуудах мөчид нь уншина — тестэд солих боломжтой.
    """
    if not settings.rate_limit_enabled:
        return
    allowed, retry_after = rate_limit.backend.hit(
        f"compile:{user.id}",
        settings.compile_rate_limit_max,
        settings.compile_rate_limit_window_seconds,
    )
    if not allowed:
        raise RateLimitError(retry_after)


def accepts_gzip(request: Request) -> bool:
    """`Accept-Encoding` gzip-ийг зөвшөөрсөн эсэх (`gzip;q=0` бол татгалзсан)."""
    for part in request.headers.get("accept-encoding", "").split(","):
        name, _, params = part.partition(";")
        if name.strip().lower() != "gzip":
            continue
        quality = params.strip().lower().removeprefix("q=")
        if not quality:
            return True
        try:
            return float(quality) > 0
        except ValueError:
            return True
    return False


@router.post(
    "/compile",
    dependencies=[Depends(limit_per_user)],
    response_class=Response,
    responses={200: {"content": {"application/wasm": {}}}},
)
async def compile_code(
    payload: CompileRequest, request: Request, _user: CurrentUser, client: CompilerClient
) -> Response:
    """C/C++ кодыг WebAssembly болгож буцаана.

    Backend кодыг ХӨРВҮҮЛЭГЧ рүү дамжуулна, өөрөө ажиллуулахгүй. Буцсан модуль
    нь зөвхөн сурагчийн browser дотор ажиллана.
    """
    if len(payload.source.encode("utf-8")) > settings.compile_max_source_bytes:
        raise AppError(413, "SOURCE_TOO_LARGE", "Код хэт урт байна.")

    wasm, cached = await compile_source(client, payload.language, payload.source)

    headers = {
        # Сурагч бүрийн код өөр — хөтөч эсвэл proxy кэшлэх ёсгүй.
        "Cache-Control": "no-store",
        "Vary": "Accept-Encoding",
        "X-Compile-Cache": "hit" if cached else "miss",
    }
    if len(wasm) >= GZIP_MIN_BYTES and accepts_gzip(request):
        wasm = await run_in_threadpool(gzip.compress, wasm, 6)
        headers["Content-Encoding"] = "gzip"

    return Response(content=wasm, media_type="application/wasm", headers=headers)
