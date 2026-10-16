"""MySQL хичээлийн кодыг ажиллуулах хүсэлт ба хариу.

Хариу нь `apps/sql-runner`-ийн `/run`-ийн бүтэцтэй ижил. API нь хүлээн авсан
хариуг энэ загвараар шалгаж байж дамжуулна — ажиллуулагч эвдэрсэн хариу
өгвөл хөтөч рүү очихгүй.
"""

from typing import Annotated, Literal

from pydantic import BaseModel, Field


class SqlRunRequest(BaseModel):
    # Тэмдэгтийн хязгаар нь зөвхөн хэт том биеийг эрт татгалзах зориулалттай.
    # Жинхэнэ хязгаар нь БАЙТААР — кирилл үсэг UTF-8-д 2 байт эзэлдэг тул
    # endpoint нь `sql_run_max_source_bytes`-ийг тусад нь шалгана.
    source: str = Field(min_length=1, max_length=200_000)


class SqlWarning(BaseModel):
    level: str
    code: int
    message: str


class SqlRowsResult(BaseModel):
    """`SELECT`, `SHOW`, `CALL` зэрэг мөр буцаадаг statement."""

    type: Literal["rows"]
    # Скрипт дэх statement-ийн эхлэх мөр (1-ээс).
    line: int
    columns: list[str]
    # NULL нь `None`. Бусад утга бүгд `mysql` CLI шиг текст.
    rows: list[list[str | None]]
    # Хязгаараас хэтэрч бүгдийг уншаагүй бол `None`.
    row_count: int | None
    truncated: bool
    warnings: list[SqlWarning]
    duration_ms: int


class SqlOkResult(BaseModel):
    """`INSERT`, `CREATE`, `USE` зэрэг мөр буцаадаггүй statement."""

    type: Literal["ok"]
    line: int
    affected_rows: int
    warnings: list[SqlWarning]
    duration_ms: int


SqlResult = Annotated[SqlRowsResult | SqlOkResult, Field(discriminator="type")]


class SqlError(BaseModel):
    """Сурагчийн кодын алдаа — хэвийн хариуны нэг хэсэг, HTTP алдаа биш."""

    line: int | None
    code: int | None
    sqlstate: str | None
    message: str


class SqlRunResponse(BaseModel):
    results: list[SqlResult]
    error: SqlError | None
    timed_out: bool
    # Гаралт хэт их болж үлдсэн statement-ийг ажиллуулаагүй.
    output_truncated: bool
    duration_ms: int
