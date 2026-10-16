"""Профайлын тэмдгүүд (badges).

Тэмдэг бүрийн нэр, нөхцөл, хэлбэр энд. Олгох логик нь
`app/services/badge_service.py`-д — түлхүүрээр нь холбогдоно. Жагсаалтын
дараалал нь профайл дээрх дараалал.

ДҮРС
────
`apps/web/public/badges/<түлхүүр>.svg` (эсвэл `.png`, `.webp`) файл хийхэд
хангалттай — build хийх үед бүртгэгдэж, профайл дээр харагдана. Файлгүй бол
`shape`-ийн дагуу хоосон хэлбэр харагдана.

`tracked=False` тэмдгүүдийг олгоход шаардлагатай өгөгдлийг (илгээлтийн
оролдлого, тусламж ашигласан эсэх, зарцуулсан хугацаа, кодын чанар,
нийгэмлэг) одоогоор бүртгэдэггүй. Профайл дээр «Тун удахгүй» гэж харагдана.
"""

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from enum import StrEnum

from app.models.enums import Category


class BadgeShape(StrEnum):
    CIRCLE = "circle"
    SHIELD = "shield"
    HEXAGON = "hexagon"


@dataclass(frozen=True, slots=True)
class BadgeSpec:
    key: str
    """Тогтмол — өгөгдлийн санд болон дүрсний файлын нэрэнд хэрэглэгдэнэ.
    Өөрчилбөл хэрэглэгчдийн авсан тэмдэг алга болно."""
    name: str
    description: str
    """Сурагчид харагдах нөхцөл."""
    shape: BadgeShape = BadgeShape.CIRCLE
    tracked: bool = True
    secret: bool = False
    """Нууц амжилт — авах хүртэл нөхцөл нь харагдахгүй (`SECRET_DESCRIPTION`)."""
    rare: bool = False
    """Ховор амжилт — профайл дээр алтан гэрэлтэй харагдана."""
    prismatic: bool = False
    """Алтан биш солонгон гэрэлтэй — ховор амжилтаас ч онцгой."""
    invisible: bool = False
    """Авах хүртэл профайл дээр огт харагдахгүй, нийт тоонд ч орохгүй — «?» ч
    үлдээхгүй. `secret`-ээс ч нууц: байгаа эсэх нь хүртэл мэдэгдэхгүй."""


SECRET_DESCRIPTION = "?"

# Ахицаас биш, үйлдлээр олгогдох тэмдэг — `POST /me/badges/{key}`. Жишээ нь
# «Through Another's Path» нь сайтын хөлийн MedlegHub логоноос хөтөлдөг нууц
# `/footprints` хуудсыг нээхэд олгогдоно.
EVENT_BADGES = frozenset({"through-anothers-path"})


# Монгол улс 2017 оноос хойш зуны цаг хэрэглэдэггүй — тогтмол UTC+8.
# `zoneinfo` нь зарим Docker image-д tz өгөгдөлгүй байдаг тул ашиглахгүй.
LOCAL_TZ = timezone(timedelta(hours=8))

NIGHT_HOURS = frozenset({22, 23, 0, 1, 2, 3})
MORNING_HOURS = frozenset({5, 6, 7})

# «Програмчлалын хэл» — HTML/CSS, Git зэрэг нь тооцогдохгүй.
PROGRAMMING_CATEGORIES = frozenset(
    {Category.JAVASCRIPT, Category.PYTHON, Category.C, Category.CSHARP, Category.JAVA}
)

# «Ахисан шатны төсөл» — хичээлийн slug. Нэр солигдвол `test_badges.py` баригдана.
ADVANCED_PROJECT_LESSONS = frozenset(
    {
        "cpp-oyutan-udirdlaga",
        "cpp-bank-programm",
        "cpp-oop-tusul",
        "tusul-burtgeliin-system",
    }
)

EARLY_ADOPTER_DEADLINE = datetime(2027, 1, 1, tzinfo=LOCAL_TZ)

STREAK_DAYS = 7

BADGES: tuple[BadgeSpec, ...] = (
    BadgeSpec(
        key="first-commit",
        name="First Commit",
        description="Анхны хичээлээ дуусгах эсвэл анхны дасгалаа илгээх.",
    ),
    BadgeSpec(
        key="hello-world",
        name="Hello, World!",
        description="Аль нэг сургалтын эхний (танилцуулга) модулийг бүрэн дуусгах.",
    ),
    BadgeSpec(
        key="unstoppable",
        name="Unstoppable",
        description="Нэг сургалтын дараалсан 3 модулийг бүрэн дуусгах.",
    ),
    BadgeSpec(
        key="code-smith",
        name="Code Smith",
        description="10 кодын дасгалыг бүх тестийг давж илгээх.",
        shape=BadgeShape.SHIELD,
    ),
    BadgeSpec(
        key="bug-hunter",
        name="Bug Hunter",
        description="Кодын 25 алдаа засах.",
        tracked=False,
    ),
    BadgeSpec(
        key="debugger",
        name="Debugger",
        description="Алдаа хайж засах 10 даалгавар шийдэх.",
        tracked=False,
    ),
    BadgeSpec(
        key="compiler",
        name="Compiler",
        description="Програмчлалын хэлний аль нэг сургалтыг бүрэн дуусгах.",
        shape=BadgeShape.HEXAGON,
    ),
    BadgeSpec(
        key="mastery",
        name="Mastery",
        description="3 сургалтыг бүрэн дуусгах.",
        shape=BadgeShape.SHIELD,
    ),
    BadgeSpec(
        key="polyglot",
        name="Polyglot",
        description="3 өөр програмчлалын хэлний сургалтад тус бүр дор хаяж нэг модуль дуусгах.",
    ),
    BadgeSpec(
        key="speed-coder",
        name="Speed Coder",
        description="Хичээл эсвэл сургалтыг дунджаас мэдэгдэхүйц хурдан дуусгах.",
        tracked=False,
        rare=True,
    ),
    BadgeSpec(
        key="night-owl",
        name="Night Owl",
        description="Шөнө орой (22:00–04:00) 10 хичээл дуусгах.",
        rare=True,
    ),
    BadgeSpec(
        key="early-bird",
        name="Early Bird",
        description="Өглөө эрт (05:00–08:00) 10 хичээл дуусгах.",
        rare=True,
    ),
    BadgeSpec(
        key="persistent",
        name="Persistent",
        description="7 өдөр дараалан хичээл дуусгах.",
    ),
    BadgeSpec(
        key="stack-overflow",
        name="Stack Overflow",
        description="50 дасгалыг алгасалгүй зөв шийдэх.",
        shape=BadgeShape.SHIELD,
        tracked=False,
    ),
    BadgeSpec(
        key="recursion",
        name="Recursion",
        description="Рекурс ашигласан даалгавар шийдэх.",
        tracked=False,
    ),
    BadgeSpec(
        key="clean-code",
        name="Clean Code",
        description="20 илгээлтэд кодын чанарын өндөр оноо авах.",
        tracked=False,
    ),
    BadgeSpec(
        key="code-warrior",
        name="Code Warrior",
        description="100 кодын дасгал шийдэх.",
        shape=BadgeShape.SHIELD,
    ),
    BadgeSpec(
        key="perfect-run",
        name="Perfect Run",
        description="Нэг модулийн бүх дасгалыг нэг ч удаа алдалгүй шийдэх.",
        tracked=False,
    ),
    BadgeSpec(
        key="perfectionist",
        name="Perfectionist",
        description="Бүртгүүлсэн бүх сургалтаа бүрэн дуусгах (дор хаяж 2 сургалт).",
    ),
    BadgeSpec(
        key="knowledge-seeker",
        name="Knowledge Seeker",
        description="50 хичээл дуусгах.",
    ),
    BadgeSpec(
        key="century",
        name="Century",
        description="100 хичээл дуусгах.",
    ),
    BadgeSpec(
        key="mentor",
        name="Mentor",
        description="Бусад сурагчдад 25 удаа туслах.",
        shape=BadgeShape.SHIELD,
        tracked=False,
    ),
    BadgeSpec(
        key="architect",
        name="Architect",
        description="Ахисан шатны төсөл дуусгах.",
        shape=BadgeShape.HEXAGON,
        rare=True,
    ),
    BadgeSpec(
        key="hidden-gem",
        name="Hidden Gem",
        description="Бүх сургалтад дор хаяж нэг хичээл дуусгах.",
        secret=True,
        rare=True,
    ),
    BadgeSpec(
        key="ahead-of-time",
        name="Ahead of Time",
        description="MedlegHub платформын Hello World! мөчтэй хамт байсан",
        rare=True,
    ),
    BadgeSpec(
        # SQL сургалтын бүх мөрдөгчийн хэргийг (`kind == "answer"`) шийдэх.
        key="where-the-answers-hide",
        name="Where the Answers Hide",
        description=(
            "Хариулт үргэлж ил харагддаггүй. Кэйс бүрийн цаадахыг олж, учрыг нь тайлж чадсан нэгэн."
        ),
        rare=True,
        prismatic=True,
    ),
    BadgeSpec(
        key="through-anothers-path",
        name="Through Another's Path",
        # Зориуд хоосон — дүрс, нэр нь л үлдэнэ.
        description="",
        secret=True,
        rare=True,
        prismatic=True,
        invisible=True,
    ),
)

BADGES_BY_KEY: dict[str, BadgeSpec] = {badge.key: badge for badge in BADGES}
