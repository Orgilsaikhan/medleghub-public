"""Тэмдэг ба профайлын хариу."""

from datetime import datetime

from pydantic import BaseModel, Field, field_validator

from app.models.badge import SHOWCASE_MAX
from app.schemas.auth import UserResponse


class BadgeProgress(BaseModel):
    current: int
    target: int


class BadgeStatus(BaseModel):
    key: str
    name: str
    description: str
    shape: str
    available: bool
    """`False` — олгох өгөгдлийг одоогоор бүртгэдэггүй («Тун удахгүй»)."""
    earned: bool
    secret: bool = False
    """Нууц амжилт — авах хүртэл `description` нь нөхцөлийг илчлэхгүй."""
    rare: bool = False
    """Ховор амжилт — UI алтан гэрэлтэй харуулна."""
    prismatic: bool = False
    """Алтан биш солонгон гэрэлтэй."""
    awarded_at: datetime | None = None
    progress: BadgeProgress | None = None
    """Тоологддог нөхцөлтэй, аваагүй тэмдэгт — жишээ нь 7/10 хичээл."""
    earned_percent: float | None = None
    """Энэ тэмдгийг авсан хэрэглэгчдийн хувь (0–100, 2 орны нарийвчлалтай) —
    «Нийт хэрэглэгчдийн XX% нь авсан». Имэйлээ баталгаажуулсан, профайлаа
    нуугаагүй суралцагчдаас тооцно. Хэн ч аваагүй бол `0.0`, нэг хүн ч авсан
    бол хамгийн багадаа `0.01`. «Тун удахгүй» тэмдэг эсвэл тооцох хэрэглэгч
    огт байхгүй бол `None`."""
    showcase_position: int | None = None
    """Эзний профайлд нэрийн хажууд онцолсон байр (1–5), онцлоогүй бол `None`."""


class BadgeUnlocked(BaseModel):
    """Хичээл дуусгахад шинээр авсан тэмдэг — UI мэдэгдэл харуулна.

    Солонгон тэмдгийг UI жижиг мэдэгдлийн оронд том цонхонд дүрс, тайлбартай
    нь харуулна — тиймээс хэлбэр, тайлбар нь хамт ирнэ.
    """

    key: str
    name: str
    description: str = ""
    shape: str = "circle"
    secret: bool = False
    rare: bool = False
    prismatic: bool = False


class BadgeClaimResponse(BaseModel):
    """`None` бол аль хэдийн авсан."""

    new_badge: BadgeStatus | None


class BadgeShowcaseUpdate(BaseModel):
    """Профайлын нэрийн хажууд онцлох амжилтууд, харуулах дарааллаар — өмнөхийг
    бүхэлд нь солино. Хоосон жагсаалт онцлохыг цуцална. Бүгд өөрийн авсан
    тэмдэг байх ёстойг `badge_service.set_showcase` шалгана."""

    badge_keys: list[str] = Field(max_length=SHOWCASE_MAX)

    @field_validator("badge_keys")
    @classmethod
    def no_duplicates(cls, value: list[str]) -> list[str]:
        if len(set(value)) != len(value):
            raise ValueError("Нэг амжилтыг хоёр удаа онцлох боломжгүй.")
        return value


class BadgeShowcaseResponse(BaseModel):
    """Хадгалсан онцлох амжилтууд, дарааллаар нь."""

    badge_keys: list[str]


class ProfileStats(BaseModel):
    completed_lessons: int
    completed_exercises: int
    completed_courses: int
    enrolled_courses: int
    earned_badges: int
    total_badges: int


class ProfileResponse(BaseModel):
    user: UserResponse
    stats: ProfileStats
    badges: list[BadgeStatus]
