import uuid
from typing import Annotated, Literal

from pydantic import BaseModel, Field, StringConstraints

from app.models.enums import LessonLanguage
from app.schemas.common import ORMModel, Position, Slug

Title = Annotated[str, StringConstraints(min_length=2, max_length=200, strip_whitespace=True)]

MAX_CONTENT_CHARS = 100_000
MAX_CODE_CHARS = 20_000


class LessonSummary(ORMModel):
    """Curriculum жагсаалтад харагдах хэлбэр — контентгүй, хөнгөн."""

    id: uuid.UUID
    title: str
    slug: str
    duration: int
    position: int
    published: bool
    completed: bool = False
    # Standard багц шаардлагатай — `app/services/access.py`.
    locked: bool = False


class LessonTestCase(BaseModel):
    """C/C++, Python-ийн тест — програмын оролт ба хүлээгдэж буй гаралт."""

    stdin: str
    expected_output: str
    sample: bool


class LessonDomTest(BaseModel):
    """React хичээлийн DOM тест. `name` нь шаардлага болж харагдана, `code` нь
    sandbox-ийн тест runtime дээр ажиллана (`apps/web/src/lib/sandbox/react-runtime`).
    """

    name: str
    code: str
    sample: bool = True


class LessonExercise(BaseModel):
    """Дасгалын даалгавар ба тестүүд.

    Сурагчийн код хөтөч дотор ажилладаг тул (`docs/ARCHITECTURE.md` §8) нууц
    тестүүдийн хүлээгдэж буй гаралт ч хөтөч рүү очно. UI нь тэдгээрийг
    харуулахгүй ч сүлжээний хүсэлтээс харж болно — энэ нь хуурах гэсэн
    сурагчийг зогсоохгүй, харин санамсаргүй «таарсан» кодыг баригдуулна.
    """

    statement: str
    # Хоёр төрлийн аль нь болохыг талбараар нь Pydantic өөрөө таньна.
    tests: list[LessonTestCase | LessonDomTest]
    # `answer` — SQL-ийн мөрдөгчийн хэрэг: тестгүй, сурагч хариултаа бичиж
    # `POST /lessons/{id}/answer`-ээр шалгуулна. Хариулт энд ОРОХГҮЙ.
    kind: Literal["tests", "answer"] = "tests"
    # `tips`, `solution` ЗОРИУД байхгүй — JSONB дахь илүү түлхүүрүүдийг
    # Pydantic хаяна. Тэдгээрийг `LessonHelp` л буцаана.


class LessonHelp(BaseModel):
    """«Тусламж» — сурагч анхааруулгыг зөвшөөрсний дараа л хүсэлт илгээнэ."""

    tips: str
    solution: str


class LessonDetail(ORMModel):
    id: uuid.UUID
    module_id: uuid.UUID
    title: str
    slug: str
    description: str
    video_url: str | None
    duration: int
    content: str
    initial_code: str
    language: str
    position: int
    published: bool
    # Бусдаасаа хэцүү хичээл — «Заавар» хэсэгт шар «Хэцүү» шошго.
    challenging: bool = False
    exercise: LessonExercise | None = None
    completed: bool = False
    # Түгжигдсэн үед агуулга, код, дасгал, видео хоосон ирнэ.
    locked: bool = False


class LessonCreate(BaseModel):
    title: Title
    slug: Slug
    description: str = Field(default="", max_length=2000)
    video_url: str | None = Field(default=None, max_length=1000)
    duration: int = Field(default=0, ge=0, le=86_400)
    content: str = Field(default="", max_length=MAX_CONTENT_CHARS)
    initial_code: str = Field(default="", max_length=MAX_CODE_CHARS)
    language: LessonLanguage = LessonLanguage.JAVASCRIPT
    position: Position = 0
    published: bool = False


class LessonUpdate(BaseModel):
    title: Title | None = None
    slug: Slug | None = None
    description: str | None = Field(default=None, max_length=2000)
    video_url: str | None = Field(default=None, max_length=1000)
    duration: int | None = Field(default=None, ge=0, le=86_400)
    content: str | None = Field(default=None, max_length=MAX_CONTENT_CHARS)
    initial_code: str | None = Field(default=None, max_length=MAX_CODE_CHARS)
    language: LessonLanguage | None = None
    position: Position | None = None
    published: bool | None = None
    module_id: uuid.UUID | None = None  # хичээлийг өөр module руу шилжүүлэх


class LessonLink(BaseModel):
    """Өмнөх/дараагийн хичээл рүү шилжих холбоос."""

    slug: str
    title: str
