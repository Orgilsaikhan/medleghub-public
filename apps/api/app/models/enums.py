"""Домэйн enum-ууд.

DB дээр native PostgreSQL enum биш VARCHAR + CHECK байдлаар хадгална —
шинэ утга нэмэхэд `ALTER TYPE` биш энгийн CHECK шинэчлэлт болно.
"""

from enum import StrEnum


class UserRole(StrEnum):
    STUDENT = "student"
    ADMIN = "admin"


class EditorLayout(StrEnum):
    """Хичээлийн засварлагчийн байрлал — хэрэглэгч «Тохиргоо»-ноос сонгоно."""

    # Засварлагч зүүн, заавар баруун — React хичээлийн байрлал. Анхдагч.
    NEW = "new"
    # Заавар дээр, засварлагч доор.
    LEGACY = "legacy"


class BillingPlan(StrEnum):
    """Худалдаж авах зүйл. Premium = Standard (сургалт + Live) + илүү AI хязгаар.

    `live_pass` — багц биш: нэг материалд зориулсан нэг удаагийн Live эрх
    (`live_passes`). Багцыг сунгахгүй (`payments.months` = 0).
    """

    STANDARD = "standard"
    PREMIUM = "premium"
    LIVE_PASS = "live_pass"


class PaymentStatus(StrEnum):
    PENDING = "pending"
    SUCCEEDED = "succeeded"
    CANCELED = "canceled"
    FAILED = "failed"


class PromoKind(StrEnum):
    # Төлбөрөөс хувиар хасна.
    PERCENT = "percent"
    # Төлбөргүйгээр багцыг хэдэн сараар сунгана.
    FREE_MONTHS = "free_months"


class AnnouncementKind(StrEnum):
    # Шинэ хичээл, засвар, өөрчлөлтийн мэдээ.
    UPDATE = "update"
    # Боломжийг онцлох, урамшуулал (промо код гэх мэт).
    FEATURE = "feature"


class AnnouncementAudience(StrEnum):
    """Зарлал хэнд харагдах вэ."""

    # Нэвтрээгүй зочин ч харна.
    EVERYONE = "everyone"
    SIGNED_IN = "signed_in"
    # Нэвтэрсэн, идэвхтэй багцгүй.
    FREE = "free"
    # Нэвтэрсэн, идэвхтэй багцтай.
    STANDARD = "standard"


class FeedbackKind(StrEnum):
    IDEA = "idea"
    BUG = "bug"
    OTHER = "other"
    # Community-ийн нийтлэл, сэтгэгдлийн гомдол. Хэрэглэгч «Санал хүсэлт»
    # цонхноос сонгохгүй — зөвхөн «Мэдэгдэх» товчоор үүснэ.
    REPORT = "report"


class PostLanguage(StrEnum):
    """Community нийтлэлийн хэлний шошго. `general` — тодорхой хэлгүй сэдэв.

    Шинэ утга нэмэхэд `community_posts.language`-ийн CHECK-ийг migration-аар,
    вэбийн `PostLanguage` төрөл ба `postLanguageLabels`-ийг хамт шинэчилнэ.
    """

    PYTHON = "python"
    C = "c"
    CPP = "cpp"
    JAVASCRIPT = "javascript"
    HTML_CSS = "html_css"
    SQL = "sql"
    JAVA = "java"
    CSHARP = "csharp"
    FLOWGORITHM = "flowgorithm"
    GENERAL = "general"


class PostType(StrEnum):
    """Community нийтлэлийн төрөл."""

    DISCUSSION = "discussion"
    HELP = "help"
    FUN_FACT = "fun_fact"


class Difficulty(StrEnum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class Category(StrEnum):
    HTML_CSS = "html_css"
    JAVASCRIPT = "javascript"
    PYTHON = "python"
    C = "c"
    CSHARP = "csharp"
    JAVA = "java"
    REACT = "react"
    BACKEND = "backend"
    DATABASE = "database"
    GIT = "git"
    FLOWGORITHM = "flowgorithm"


class LessonLanguage(StrEnum):
    """Code editor-ийн хэл.

    Утга бүр нь Monaco-ийн хэлний ID-тай ЯГ таарах ёстой — `code-editor.tsx`
    нь утгыг шууд Monaco руу дамжуулдаг. Шинэ утга нэмэхэд:

        1. Энд нэмнэ
        2. `lessons.language`-ийн CHECK-ийг migration-аар шинэчилнэ
        3. `apps/web/src/lib/types/api.ts`-ийн `LessonLanguage` төрөлд нэмнэ
        4. `apps/web/src/lib/i18n/mn.ts`-ийн `languageLabels`-д шошго нэмнэ

    `javascript`, `python`, `c`, `cpp` нь browser дотор ажиллана. `mysql` нь
    `apps/sql-runner`-ийн MySQL sandbox дээр ажиллана. Бусад нь зөвхөн syntax
    highlight хийгдэнэ.

    `jsx` (React) нь Monaco-ийн ID БИШ цорын ганц утга: засварлагч үүнийг
    `javascript` болгож `.jsx` файлын нэрээр JSX-ийг таниулна. Хичээлийн код
    нь олон файл (`// @file App.jsx`) бөгөөд sandbox iframe дотор «Хөтөч»
    дээр ажиллана — `apps/web/src/lib/sandbox/react/`.

    `sql` нь Monaco-ийн T-SQL горим тул SQL Server-ийн хичээлд, `mysql` нь
    MySQL-ийн хичээлд хэрэглэгдэнэ.
    """

    JAVASCRIPT = "javascript"
    JSX = "jsx"
    HTML = "html"
    CSS = "css"
    PYTHON = "python"
    C = "c"
    CPP = "cpp"
    SHELL = "shell"
    MYSQL = "mysql"
    SQL = "sql"
    PLAINTEXT = "plaintext"


class LiveTier(StrEnum):
    """MedlegHub Live-ийн эрх (`app/live/access.py`).

    `standard` — идэвхтэй Standard багц (Live багтсан); `premium` — Standard дээр
    илүү AI хязгаар (`live_subscriptions`); `pass` — багцгүй, гэхдээ нэг удаагийн
    эрхтэй (`live_passes`): ашиглаагүй эрх эсвэл эрхээр нээсэн материал; `free` —
    аль нь ч биш.
    """

    FREE = "free"
    PASS = "pass"
    STANDARD = "standard"
    PREMIUM = "premium"


class LiveMaterialKind(StrEnum):
    PDF = "pdf"
    PPTX = "pptx"
    DOCX = "docx"
    TXT = "txt"
    MD = "md"
    IMAGE = "image"


class LiveMaterialStatus(StrEnum):
    # Мета бүртгэгдсэн, файл хараахан ирээгүй.
    UPLOADING = "uploading"
    QUEUED = "queued"
    PROCESSING = "processing"
    READY = "ready"
    FAILED = "failed"


class LiveGenerationKind(StrEnum):
    # Сэдвийн заавар (Markdown).
    GUIDE = "guide"
    # Сэдвийн эсвэл бүтэн материалын тест.
    QUIZ = "quiz"
    # «Шалгалтад бэлтгэх» — шалгалтад гарч болох сэдэв, асуулт.
    EXAM = "exam"


class LiveGenerationStatus(StrEnum):
    QUEUED = "queued"
    PROCESSING = "processing"
    READY = "ready"
    FAILED = "failed"


def values(enum_cls: type[StrEnum]) -> list[str]:
    return [member.value for member in enum_cls]
