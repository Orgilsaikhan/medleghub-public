"""Provider-оос хамааралгүй хүсэлт, хариуны төрөл."""

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any, Literal


@dataclass(frozen=True)
class Part:
    """Хүсэлтийн нэг хэсэг: текст, PDF баримт эсвэл зураг."""

    kind: Literal["text", "document", "image"]
    text: str | None = None
    data: bytes | None = None
    mime_type: str | None = None

    @classmethod
    def of_text(cls, text: str) -> "Part":
        return cls(kind="text", text=text)

    @classmethod
    def of_document(cls, data: bytes, mime_type: str = "application/pdf") -> "Part":
        return cls(kind="document", data=data, mime_type=mime_type)

    @classmethod
    def of_image(cls, data: bytes, mime_type: str) -> "Part":
        return cls(kind="image", data=data, mime_type=mime_type)


@dataclass(frozen=True)
class Usage:
    input_tokens: int = 0
    cached_input_tokens: int = 0
    output_tokens: int = 0
    # Бодлын (thinking) токен — гаралтын үнээр тооцогдоно.
    reasoning_tokens: int = 0
    # Provider өөрөө хэлсэн бодит зардал (OpenRouter `usage.cost`). Байвал манай
    # үнийн хүснэгтээр тооцсоноос давуу.
    cost_usd: Decimal | None = None


@dataclass(frozen=True)
class ProviderRequest:
    capability: str
    model: str
    system: str
    parts: list[Part]
    # JSON Schema — `schema.llm_schema()`-ийн гаргасан энгийн хэлбэр.
    schema: dict[str, Any]
    max_output_tokens: int
    thinking_level: str
    timeout_seconds: float
    # Бүтэцтэй нэмэлт мэдээлэл (сэдвийн нэр гэх мэт). Жинхэнэ provider үл
    # тоомсорлоно — хуурамч provider хариугаа үүгээр бүтээнэ.
    context: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ProviderResult:
    text: str
    usage: Usage
    request_id: str | None = None
