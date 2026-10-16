"""Задалсан баримтын нийтлэг хэсэг: алдаа, хуудас, текст цэвэрлэх, нийт хязгаар."""

import re
from dataclasses import dataclass
from typing import Any

# Гарчиг нь хуудасны текстэд аль хэдийн багтсан. Энд зөвхөн жагсаалтад
# харуулах хэмжээгээр таслана.
MAX_TITLE_CHARS = 300


@dataclass(frozen=True)
class Page:
    """PDF-ийн хуудас, PPTX-ийн слайд эсвэл DOCX-ийн хэсэг."""

    title: str | None
    text: str


class ExtractError(Exception):
    """Файлыг задлах боломжгүй. `code` нь API-д очих алдааны код.

    `detail` нь зөвхөн log-д (Python-ы алдааны төрөл гэх мэт) — файлын
    агуулгыг ХЭЗЭЭ Ч оруулахгүй.
    """

    def __init__(self, code: str, *, page_count: int | None = None, detail: str | None = None):
        super().__init__(code)
        self.code = code
        self.page_count = page_count
        self.detail = detail


_LINE_BREAKS = re.compile(r"\r\n|[\r\x0b\x0c\x85  ]")
# Удирдах тэмдэгт, ганц surrogate, «тэмдэгт биш» кодууд. Postgres текстэд NUL
# хадгалахгүй, ганц surrogate нь UTF-8 болж чадахгүй.
_INVISIBLE = re.compile(r"[\x00-\x08\x0e-\x1f\x7f-\x84\x86-\x9f\ud800-\udfff￾￿]")
# Мөр шилжүүлэхээс бусад бүх хоосон зай (таб, NBSP, U+3000 гэх мэт).
_SPACES = re.compile(r"[^\S\n]+")


def normalize(text: str) -> str:
    """Хоосон зайг нэг болгож, мөр бүрийг тайрч, дараалсан хоосон мөрийг нэг болгоно.

    Кирилл болон бусад Unicode тэмдэгт хэвээр үлдэнэ.
    """
    text = _INVISIBLE.sub("", _LINE_BREAKS.sub("\n", text))
    lines: list[str] = []
    for raw in text.split("\n"):
        line = _SPACES.sub(" ", raw).strip()
        if line or (lines and lines[-1]):
            lines.append(line)
    while lines and not lines[-1]:
        lines.pop()
    return "\n".join(lines)


def title_of(text: str) -> str | None:
    """Олон мөрт гарчгийг нэг мөр болгоно. Хоосон бол None."""
    title = " ".join(line for line in text.split("\n") if line)
    return title[:MAX_TITLE_CHARS] or None


def build_result(
    kind: str, pages: list[Page], max_text_chars: int, truncated: bool = False
) -> dict[str, Any]:
    """API-ийн хариу. Нийт текст хязгаарт хүрмэгц үлдсэн хуудсууд хоосон текстэй."""
    remaining = max_text_chars
    items = []
    for number, page in enumerate(pages, start=1):
        text = page.text
        if len(text) > remaining:
            text = text[:remaining]
            truncated = True
        remaining -= len(text)
        items.append({"number": number, "title": page.title, "text": text})
    return {"kind": kind, "page_count": len(pages), "pages": items, "truncated": truncated}
