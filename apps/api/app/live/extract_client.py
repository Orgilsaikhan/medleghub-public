"""Файл задлагч (`apps/extractor`)-ийн client. API өөрөө PDF, PPTX, DOCX задлахгүй.

Задлагч нь тусдаа, сүлжээгүй, нууцгүй контейнер — эвдэрсэн эсвэл хортой
файл API-ийн процесс (бүх нууцтай) руу хүрэхгүй.
"""

from dataclasses import dataclass

import httpx

from app.core.config import settings

# Задлагчийн `{"error": …}` → Live-ийн алдааны код.
ERROR_CODES = {
    "too_many_pages": "LIVE_TOO_MANY_PAGES",
    "encrypted": "LIVE_FILE_ENCRYPTED",
    "macro_enabled": "LIVE_FILE_MACRO",
    "legacy_format": "LIVE_FILE_LEGACY",
    "corrupt": "LIVE_FILE_CORRUPT",
    "unsupported": "LIVE_FILE_CORRUPT",
    "timeout": "LIVE_FILE_TOO_COMPLEX",
    "too_large": "LIVE_FILE_TOO_LARGE",
}


@dataclass(frozen=True)
class ExtractedPage:
    number: int
    title: str | None
    text: str


@dataclass(frozen=True)
class Extraction:
    page_count: int
    pages: list[ExtractedPage]
    truncated: bool = False


class ExtractionError(Exception):
    def __init__(self, code: str, *, retryable: bool = False) -> None:
        super().__init__(code)
        self.code = code
        self.retryable = retryable


async def extract(kind: str, data: bytes, client: httpx.AsyncClient | None = None) -> Extraction:
    """`kind`: `pdf` / `pptx` / `docx`. Файлын алдаа — `ExtractionError` (дахин оролдохгүй);
    үйлчилгээ ажиллахгүй — `retryable`."""
    owned = client is None
    client = client or httpx.AsyncClient(
        base_url=settings.extractor_url, timeout=settings.extractor_timeout_seconds
    )
    try:
        response = await client.post(
            "/extract",
            params={"kind": kind},
            content=data,
            headers={"Content-Type": "application/octet-stream"},
        )
    except httpx.HTTPError as exc:
        raise ExtractionError("LIVE_EXTRACTOR_UNAVAILABLE", retryable=True) from exc
    finally:
        if owned:
            await client.aclose()

    if response.status_code in (413, 422):
        try:
            error = str(response.json().get("error", "corrupt"))
        except (ValueError, AttributeError):
            error = "corrupt"
        raise ExtractionError(ERROR_CODES.get(error, "LIVE_FILE_CORRUPT"))
    if response.status_code != 200:
        raise ExtractionError("LIVE_EXTRACTOR_UNAVAILABLE", retryable=True)
    try:
        body = response.json()
        pages = [
            ExtractedPage(
                number=int(page["number"]),
                title=page.get("title") or None,
                text=str(page.get("text") or ""),
            )
            for page in body["pages"]
        ]
        return Extraction(
            page_count=int(body["page_count"]),
            pages=pages,
            truncated=bool(body.get("truncated")),
        )
    except (ValueError, KeyError, TypeError) as exc:
        raise ExtractionError("LIVE_EXTRACTOR_UNAVAILABLE", retryable=True) from exc
