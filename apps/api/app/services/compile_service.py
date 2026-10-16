"""C/C++ кодыг тусдаа хөрвүүлэгч үйлчилгээ рүү дамжуулна.

Backend өөрөө хөрвүүлдэггүй, ажиллуулдаггүй. Хүсэлтийг `apps/compiler`
үйлчилгээ рүү дамжуулж, үр дүнгийн WebAssembly модулийг browser руу буцаана.
Модуль нь ЗӨВХӨН сурагчийн browser доторх Web Worker-т ажиллана.

Хөрвүүлэгч нь нууц мэдээлэлгүй, өгөгдлийн сангүй, гадагшаа сүлжээгүй тусдаа
контейнерт ажилладаг. Тиймээс хөрвүүлэгчид цоорхой гарсан ч API-ийн JWT
нууц, өгөгдлийн сангийн эрхэд хүрэхгүй.
"""

from collections.abc import AsyncGenerator
from typing import Literal

import httpx
from fastapi import HTTPException

from app.core.config import settings
from app.core.errors import AppError

Language = Literal["c", "cpp"]


class CompileFailedError(HTTPException):
    """Сурагчийн кодонд хөрвүүлэлтийн алдаа байна.

    Бусад алдаанаас ялгаатай нь хөрвүүлэгчийн мессежийг (`diagnostics`) хамт
    буцаана — сурагч аль мөрөнд, юу алдсанаа харах ёстой. Энэ бол сургалтын
    хамгийн чухал хэсгүүдийн нэг (C хичээлийн «Хөрвүүлэлт ба алдаа унших»).
    """

    def __init__(self, diagnostics: str) -> None:
        super().__init__(
            status_code=422,
            detail={
                "code": "COMPILE_ERROR",
                "message": "Кодыг хөрвүүлж чадсангүй.",
                "diagnostics": diagnostics,
            },
        )


async def get_compiler_client() -> AsyncGenerator[httpx.AsyncClient, None]:
    """Хөрвүүлэгч рүү хандах client. Тестэд `httpx.MockTransport`-оор солино."""
    async with httpx.AsyncClient(
        base_url=settings.compiler_url,
        timeout=settings.compile_timeout_seconds,
    ) as client:
        yield client


def _error_body(response: httpx.Response) -> dict[str, object]:
    try:
        body = response.json()
    except ValueError:
        return {}
    return body if isinstance(body, dict) else {}


async def compile_source(
    client: httpx.AsyncClient, language: Language, source: str
) -> tuple[bytes, bool]:
    """Кодыг хөрвүүлж `(wasm_байт, кэшээс_ирсэн_эсэх)` буцаана."""
    try:
        response = await client.post("/compile", json={"language": language, "source": source})
    except httpx.TimeoutException as exc:
        raise AppError(
            504,
            "COMPILE_TIMEOUT",
            "Хөрвүүлэлт хэт удаан үргэлжиллээ. Кодоо хялбарчлаад дахин оролдоно уу.",
        ) from exc
    except httpx.HTTPError as exc:
        raise AppError(
            503,
            "COMPILER_UNAVAILABLE",
            "Хөрвүүлэгчтэй холбогдож чадсангүй. Түр хүлээгээд дахин оролдоно уу.",
        ) from exc

    if response.status_code == 200:
        return response.content, response.headers.get("x-compile-cache") == "hit"

    body = _error_body(response)

    if response.status_code == 422 and body.get("code") == "COMPILE_ERROR":
        raise CompileFailedError(str(body.get("diagnostics", "")))
    if response.status_code == 413:
        raise AppError(413, "SOURCE_TOO_LARGE", "Код хэт урт байна.")
    if response.status_code == 504:
        raise AppError(
            504,
            "COMPILE_TIMEOUT",
            "Хөрвүүлэлт хэт удаан үргэлжиллээ. Кодоо хялбарчлаад дахин оролдоно уу.",
        )
    if response.status_code == 503:
        raise AppError(
            503,
            "COMPILER_BUSY",
            "Хөрвүүлэгч завгүй байна. Түр хүлээгээд дахин оролдоно уу.",
        )

    raise AppError(502, "COMPILER_ERROR", "Хөрвүүлэхэд алдаа гарлаа. Дараа дахин оролдоно уу.")
