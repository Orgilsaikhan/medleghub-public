"""Сургалтын агуулгыг тодорхойлох бүтэц.

Агуулгыг энгийн dict биш dataclass-аар бичдэг нь талбарын нэр бичихдээ
алдахаас сэргийлж, шинэ хичээл нэмэхэд шаардлагатай талбарыг санууллаа.
"""

from dataclasses import dataclass, field

from app.models.enums import Category, Difficulty, LessonLanguage


@dataclass(frozen=True, slots=True)
class TestCaseSpec:
    """Дасгалын нэг тест: програмд өгөх оролт ба хүлээгдэж буй гаралт.

    Гаралтыг мөр бүрийн төгсгөлийн зай, төгсгөлийн хоосон мөрийг үл тоон
    харьцуулна (`apps/web/src/lib/sandbox/grader.ts`). Бусад бүх тэмдэгт
    яг таарах ёстой.
    """

    __test__ = False  # pytest-ийн тестийн класс биш

    stdin: str
    expected_output: str
    sample: bool = False
    """`True` бол даалгаврын доор «Жишээ» болж харагдана, «Тест ажиллуулах»
    товч үүгээр шалгана. Бусад нь нууц — зөвхөн «Илгээх» үед ажиллана."""


@dataclass(frozen=True, slots=True)
class ReactTestSpec:
    """React хичээлийн DOM тест — react-tutorial.app-ийн адил нэр нь
    шаардлага болж жагсана («Товч дарахад тоо 1-ээр нэмэгдэнэ»).

    `code` нь async функцийн бие бөгөөд sandbox-ийн тест runtime дээр
    ажиллана (`apps/web/src/lib/sandbox/react-runtime/testing.ts`):
    `render`, `screen`, `user`, `expect`, `waitFor`, `within`, `fn`, `mod`,
    `App`, `runMain`, `logs`, `api`, `setPath`, `React`. JSX бичиж болно.
    """

    __test__ = False  # pytest-ийн тестийн класс биш

    name: str
    code: str


@dataclass(frozen=True, slots=True)
class ExerciseSpec:
    """HackerRank маягийн дасгал: даалгавар, тест, жишиг шийдэл.

    Хичээлийн `initial_code` нь дасгалын эхлэл код (сурагчийн бөглөх араг)
    болно. Бүх тестийг давбал хичээл дууссанд тооцогдоно.
    """

    statement: str
    """Markdown — даалгавар, оролт ба гаралтын формат. Жишээ оролт/гаралтыг
    UI нь `sample` тестүүдээс өөрөө харуулна — энд давтаж бичихгүй."""
    tests: tuple[TestCaseSpec, ...] | tuple[ReactTestSpec, ...]
    solution: str
    """Жишиг шийдэл — бүх тестийг давах ёстой (`python -m app.content.exercises`
    шалгана). Хичээлийн хариунд ОРОХГҮЙ: сурагч «Тусламж» дарж анхааруулгыг
    зөвшөөрсний дараа л тусдаа хүсэлтээр (`GET /lessons/{id}/help`) авна."""
    tips: str = ""
    """Markdown — хэрхэн бодох, хичээлийн гол ойлголт, түгээмэл алдаа. «Тусламж»
    дээр шийдлийн өмнө харагдана. Бүтэн код бичихгүй."""
    answers: tuple[str, ...] = ()
    """Мөрдөгчийн хэрэг (SQL): сурагч асуулгаа ажиллуулж олсон ХАРИУЛТАА бичнэ,
    API нь үүнтэй харьцуулна (`app/services/case_service.py` — том жижиг үсэг,
    зай, хашилтыг үл тооно). Эхнийх нь үндсэн хариулт, бусад нь зөвшөөрөгдөх
    хувилбар («Анужин», «Анужин Батын»). Хариулттай дасгал тестгүй байна.
    Хариулт хэзээ ч хөтөч рүү очихгүй — зөвхөн шалгах endpoint мэднэ."""

    @property
    def kind(self) -> str:
        return "answer" if self.answers else "tests"


@dataclass(frozen=True, slots=True)
class LessonSpec:
    title: str
    slug: str
    description: str
    """Markdown. Хичээлийн гарчгийг давтаж бичихгүй — UI өөрөө харуулна."""
    content: str
    initial_code: str
    """Секундээр."""
    duration: int
    language: LessonLanguage = LessonLanguage.JAVASCRIPT
    video_url: str | None = None
    published: bool = True
    exercise: ExerciseSpec | None = None
    challenging: bool = False
    """Бусдаасаа хэцүү хичээл — «Заавар» хэсэгт шар «Хэцүү» шошго харагдана."""


@dataclass(frozen=True, slots=True)
class ModuleSpec:
    title: str
    description: str
    lessons: list[LessonSpec] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class CourseSpec:
    title: str
    slug: str
    description: str
    difficulty: Difficulty
    category: Category
    modules: list[ModuleSpec] = field(default_factory=list)
    thumbnail_url: str | None = None
    # `is_free=False` үед эхний `free_lessons` хичээл үнэгүй, үлдсэн нь Standard
    # багцтай. Модулийн дундуур таслахгүй байхаар сонгоно.
    is_free: bool = True
    free_lessons: int = 0
    published: bool = True

    @property
    def lesson_count(self) -> int:
        return sum(len(module.lessons) for module in self.modules)
