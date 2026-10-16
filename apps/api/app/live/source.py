"""Материалын файл: төрөл, нэр, агуулгын шалгалт ба AI-д илгээх хэлбэр.

- PDF — Gemini шууд уншина (хуудасны зураг + текст): диаграм, хүснэгт ч ойлгогдоно.
- Зураг — шууд.
- PPTX, DOCX — задлагчийн гаргасан текст (Gemini эдгээрийг уншдаггүй).
- TXT, MD — API өөрөө UTF-8 болгож, ~3000 тэмдэгтийн «хуудас» болгон хуваана.

Задалсан текст нь R2-д JSON (`materials/<id>/text.json`) — Postgres-д биш.
"""

import codecs
import json
import re
import unicodedata
from dataclasses import dataclass
from pathlib import PurePath

from fastapi import status

from app.core.config import settings
from app.live.errors import live_error
from app.live.extract_client import ExtractedPage
from app.live.storage import BlobStorage
from app.models.enums import LiveMaterialKind
from app.models.live import LiveMaterial
from app.services.ai.types import Part

EXTENSIONS: dict[str, LiveMaterialKind] = {
    ".pdf": LiveMaterialKind.PDF,
    ".pptx": LiveMaterialKind.PPTX,
    ".docx": LiveMaterialKind.DOCX,
    ".txt": LiveMaterialKind.TXT,
    ".md": LiveMaterialKind.MD,
    ".markdown": LiveMaterialKind.MD,
    ".png": LiveMaterialKind.IMAGE,
    ".jpg": LiveMaterialKind.IMAGE,
    ".jpeg": LiveMaterialKind.IMAGE,
    ".webp": LiveMaterialKind.IMAGE,
}
# Тодорхой шалтгаантай татгалзал — «дэмжихгүй» гэхээс илүү ойлгомжтой.
REJECTED: dict[str, str] = {
    ".ppt": "LIVE_FILE_LEGACY",
    ".pps": "LIVE_FILE_LEGACY",
    ".doc": "LIVE_FILE_LEGACY",
    ".pptm": "LIVE_FILE_MACRO",
    ".ppsm": "LIVE_FILE_MACRO",
    ".docm": "LIVE_FILE_MACRO",
}
ACCEPTED_EXTENSIONS = sorted(EXTENSIONS)

# Задлагч шаардлагатай төрлүүд.
EXTRACTED_KINDS = {LiveMaterialKind.PDF, LiveMaterialKind.PPTX, LiveMaterialKind.DOCX}
TEXT_KINDS = {LiveMaterialKind.TXT, LiveMaterialKind.MD}

OLE_MAGIC = b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"
PAGE_CHARS = 3000
# PDF-ийн нэг хуудас Gemini 3-т ~560 зургийн токен + текст.
TOKENS_PER_PDF_PAGE = 900
TOKENS_PER_IMAGE = 1500


def clean_filename(name: str) -> str:
    """Замгүй, удирдлагын тэмдэгтгүй, 200 тэмдэгт хүртэл — зөвхөн харуулахад."""
    base = PurePath(name.replace("\\", "/")).name
    base = "".join(ch for ch in base if unicodedata.category(ch)[0] != "C")
    base = re.sub(r"\s+", " ", base).strip()
    return base[:200] or "material"


def default_title(filename: str) -> str:
    stem = PurePath(filename).stem.replace("_", " ").strip()
    return (re.sub(r"\s+", " ", stem) or "Материал")[:200]


def kind_for(filename: str) -> LiveMaterialKind:
    suffix = PurePath(filename.lower()).suffix
    if suffix in EXTENSIONS:
        return EXTENSIONS[suffix]
    code = REJECTED.get(suffix, "LIVE_FILE_UNSUPPORTED")
    raise live_error(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, code)


def image_mime(head: bytes) -> str | None:
    if head.startswith(b"\x89PNG\r\n\x1a\n"):
        return "image/png"
    if head.startswith(b"\xff\xd8\xff"):
        return "image/jpeg"
    if head[:4] == b"RIFF" and head[8:12] == b"WEBP":
        return "image/webp"
    return None


def _looks_like_cp1251(head: bytes) -> bool:
    """Удирдлагын тэмдэгтгүй бол текст гэж үзнэ (cp1251 бүх байтыг тайлдаг)."""
    return not any(byte < 0x20 and byte not in (0x09, 0x0A, 0x0D) for byte in head)


def sniff(kind: LiveMaterialKind, head: bytes) -> str:
    """Агуулга өргөтгөлтэйгөө таарч байгаа эсэх; таарвал MIME төрөл."""
    if kind == LiveMaterialKind.PDF and b"%PDF-" in head[:1024]:
        return "application/pdf"
    # OLE бол хуучин эсвэл нууц үгтэй Office — задлагч ялгаж хэлнэ.
    office = kind in (LiveMaterialKind.PPTX, LiveMaterialKind.DOCX)
    if office and head.startswith((b"PK\x03\x04", OLE_MAGIC)):
        return "application/octet-stream"
    if kind == LiveMaterialKind.IMAGE and (mime := image_mime(head)):
        return mime
    if kind in TEXT_KINDS and b"\x00" not in head:
        try:
            # `final=False` — эхний хэсгийн төгсгөлд таслагдсан олон байт тэмдэгт алдаа биш.
            codecs.getincrementaldecoder("utf-8")().decode(head, final=False)
        except UnicodeDecodeError:
            # Хуучин Windows-ийн кирилл (cp1251) — `decode_text` хөрвүүлнэ.
            if not _looks_like_cp1251(head):
                raise live_error(
                    status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, "LIVE_FILE_MISMATCH"
                ) from None
        return "text/markdown" if kind == LiveMaterialKind.MD else "text/plain"
    raise live_error(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, "LIVE_FILE_MISMATCH")


def decode_text(data: bytes) -> str:
    try:
        return data.decode("utf-8-sig")
    except UnicodeDecodeError:
        # Хуучин Windows-ийн кирилл файл.
        return data.decode("cp1251", errors="replace")


def paginate_text(text: str) -> list[ExtractedPage]:
    """Догол мөрийн хилээр ~`PAGE_CHARS` тэмдэгтийн хэсэг болгоно."""
    pages: list[ExtractedPage] = []
    current: list[str] = []
    size = 0
    for paragraph in re.split(r"\n\s*\n", text.replace("\r\n", "\n")):
        paragraph = paragraph.strip()
        if not paragraph:
            continue
        if current and size + len(paragraph) > PAGE_CHARS:
            pages.append(ExtractedPage(len(pages) + 1, None, "\n\n".join(current)))
            current, size = [], 0
        current.append(paragraph)
        size += len(paragraph)
    if current:
        pages.append(ExtractedPage(len(pages) + 1, None, "\n\n".join(current)))
    return pages


def text_key(material: LiveMaterial) -> str:
    return f"materials/{material.id}/text.json"


def encode_pages(pages: list[ExtractedPage], truncated: bool) -> bytes:
    return json.dumps(
        {
            "version": 1,
            "truncated": truncated,
            "pages": [{"number": p.number, "title": p.title, "text": p.text} for p in pages],
        },
        ensure_ascii=False,
    ).encode()


def decode_pages(data: bytes) -> list[ExtractedPage]:
    body = json.loads(data)
    return [ExtractedPage(p["number"], p.get("title"), p["text"]) for p in body["pages"]]


def has_text(pages: list[ExtractedPage]) -> bool:
    return sum(len(page.text.strip()) for page in pages) >= 20


def format_source(material: LiveMaterial, pages: list[ExtractedPage]) -> str:
    """AI-д: `--- Слайд 3: Гарчиг ---` тэмдэгтэй текст, дээд хэмжээгээр таслана."""
    label = "Слайд" if material.kind == LiveMaterialKind.PPTX else "Хуудас"
    lines = [f"=== МАТЕРИАЛ: {material.title} ==="]
    size = 0
    for page in pages:
        header = f"--- {label} {page.number}" + (f": {page.title}" if page.title else "") + " ---"
        text = page.text.strip()
        if size + len(text) > settings.live_max_text_chars:
            text = text[: max(0, settings.live_max_text_chars - size)]
            lines.extend([header, text, "[… материалын үлдсэн хэсэг хэт урт тул таслагдав]"])
            break
        lines.extend([header, text])
        size += len(text)
    return "\n".join(lines)


@dataclass(frozen=True)
class Source:
    """AI-д илгээх материал: хэсгүүд, хуурамч AI-д зориулсан текст, токены тооцоо."""

    parts: list[Part]
    text: str
    input_tokens_estimate: int


async def load_source(storage: BlobStorage, material: LiveMaterial) -> Source:
    pages: list[ExtractedPage] = []
    if material.text_key:
        pages = decode_pages(await storage.get(material.text_key))
    text = format_source(material, pages) if pages else ""

    if material.kind == LiveMaterialKind.PDF:
        data = await storage.get(material.storage_key)
        estimate = (material.page_count or 1) * TOKENS_PER_PDF_PAGE
        return Source([Part.of_document(data, "application/pdf")], text, estimate)
    if material.kind == LiveMaterialKind.IMAGE:
        data = await storage.get(material.storage_key)
        mime = image_mime(data[:16]) or "image/png"
        return Source([Part.of_image(data, mime)], "", TOKENS_PER_IMAGE)
    return Source([Part.of_text(text)], text, len(text) // 3 + 500)
