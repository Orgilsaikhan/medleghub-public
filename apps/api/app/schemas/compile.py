"""C/C++ хөрвүүлэлтийн хүсэлт."""

from typing import Literal

from pydantic import BaseModel, Field


class CompileRequest(BaseModel):
    language: Literal["c", "cpp"]
    # Тэмдэгтийн хязгаар нь зөвхөн хэт том биеийг эрт татгалзах зориулалттай.
    # Жинхэнэ хязгаар нь БАЙТААР — кирилл үсэг UTF-8-д 2 байт эзэлдэг тул
    # endpoint нь `compile_max_source_bytes`-ийг тусад нь шалгана.
    source: str = Field(min_length=1, max_length=200_000)
