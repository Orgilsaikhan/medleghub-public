"""Промо код (админ үүсгэнэ) ба найзаа урих хөтөлбөрийн schema."""

import re
import uuid
from datetime import UTC, datetime
from typing import Annotated, Literal

from pydantic import AfterValidator, BaseModel, Field, field_validator, model_validator

from app.core.config import settings
from app.models.enums import PromoKind
from app.schemas.billing import PlanOption

CODE_PATTERN = re.compile(r"^[A-Z0-9]{4,32}$")


def normalize_code(value: str) -> str:
    """Хэрэглэгч `helloworld 2026`, `HELLO-WORLD2026` гэж бичсэн ч олдоно."""
    return re.sub(r"[\s\-_]+", "", value).upper()


def _valid_code(value: str) -> str:
    value = normalize_code(value)
    if not CODE_PATTERN.fullmatch(value):
        raise ValueError("Код 4–32 латин үсэг, тооноос бүрдэнэ.")
    return value


# Хэрэглэгчийн оруулсан код. Урт нь хязгаартай — нормчлохоос өмнө ч.
EnteredCode = Annotated[str, Field(min_length=1, max_length=64), AfterValidator(normalize_code)]
PromoCodeText = Annotated[str, Field(min_length=1, max_length=64), AfterValidator(_valid_code)]


def _aware(value: datetime | None) -> datetime | None:
    """Цагийн бүсгүй огноог UTC гэж үзнэ."""
    if value is not None and value.tzinfo is None:
        return value.replace(tzinfo=UTC)
    return value


def _blank_is_none(value: str | None) -> str | None:
    if value is None:
        return None
    return value.strip() or None


# --- Хэрэглэгч ----------------------------------------------------------------


class PromoCheckRequest(BaseModel):
    code: EnteredCode


class PromoPreview(BaseModel):
    """Оруулсан код хүчинтэй — юу өгөхийг, хувийн код бол үнийг харуулна."""

    code: str
    kind: PromoKind
    percent_off: int | None
    free_months: int | None
    expires_at: datetime | None
    # Хувийн код: 1–12 сар, тус бүрийн хөнгөлөлттэй үнэ. Үнэгүй сарын кодод хоосон.
    options: list[PlanOption]
    # Мөн Premium-д (Premium зарагдаж байвал), эс бөгөөс хоосон.
    premium_options: list[PlanOption] = []


class ReferralSummary(BaseModel):
    """Найзаа урих: өөрийн код ба олсон шагнал. Найзуудын нэр, төлбөрийг
    харуулахгүй — зөвхөн нийт тоо."""

    code: str
    # Урилгын кодоор бүртгүүлсэн найзын нэг удаагийн хөнгөлөлт (хувь).
    friend_percent_off: int
    # Урьсан найзуудаас `friends_per_reward` нь багц авах бүрд `reward_months` сар.
    friends_per_reward: int
    reward_months: int
    # Имэйлээ баталгаажуулсан найзын тоо.
    friends: int
    # Дор хаяж нэг удаа амжилттай төлсөн найзын тоо.
    paying_friends: int
    # Дараагийн үнэгүй сар хүртэл дахиад хэдэн найз багц авах вэ (1…`friends_per_reward`).
    friends_to_next_reward: int
    # Найзуудын төлбөрөөр нийт олсон үнэгүй сар.
    months_earned: int


# --- Админ -------------------------------------------------------------------


class PromoCodeCreate(BaseModel):
    """Код хоосон бол сервер санамсаргүй 8 тэмдэгт үүсгэнэ."""

    code: PromoCodeText | None = None
    kind: PromoKind
    percent_off: int | None = Field(default=None, ge=1, le=99)
    free_months: int | None = Field(default=None, ge=1, le=settings.promo_max_free_months)
    expires_at: datetime | None = None
    max_uses: int | None = Field(default=None, ge=1, le=1_000_000)
    note: str | None = Field(default=None, max_length=500)

    @field_validator("code", mode="before")
    @classmethod
    def blank_code_is_none(cls, value: object) -> object:
        if isinstance(value, str) and not value.strip():
            return None
        return value

    @field_validator("expires_at")
    @classmethod
    def aware_expiry(cls, value: datetime | None) -> datetime | None:
        return _aware(value)

    @field_validator("note")
    @classmethod
    def blank_note_is_none(cls, value: str | None) -> str | None:
        return _blank_is_none(value)

    @model_validator(mode="after")
    def value_matches_kind(self) -> "PromoCodeCreate":
        if self.kind == PromoKind.PERCENT:
            if self.percent_off is None:
                raise ValueError("Хөнгөлөлтийн хувийг оруулна уу.")
            self.free_months = None
        else:
            if self.free_months is None:
                raise ValueError("Үнэгүй сарын тоог оруулна уу.")
            self.percent_off = None
        if self.expires_at is not None and self.expires_at <= datetime.now(UTC):
            raise ValueError("Дуусах хугацаа ирээдүйд байх ёстой.")
        return self


class PromoCodeUpdate(BaseModel):
    """Зөвхөн ирсэн талбарыг өөрчилнө. `expires_at`, `max_uses`-ийг `null`
    болговол хязгааргүй болно. Төрөл, хэмжээг солихгүй."""

    active: bool | None = None
    expires_at: datetime | None = None
    max_uses: int | None = Field(default=None, ge=1, le=1_000_000)
    note: str | None = Field(default=None, max_length=500)

    @field_validator("expires_at")
    @classmethod
    def aware_expiry(cls, value: datetime | None) -> datetime | None:
        return _aware(value)

    @field_validator("note")
    @classmethod
    def blank_note_is_none(cls, value: str | None) -> str | None:
        return _blank_is_none(value)

    @field_validator("active")
    @classmethod
    def active_not_null(cls, value: bool | None) -> bool:
        if value is None:
            raise ValueError("Идэвхтэй эсэхийг true эсвэл false гэж өгнө.")
        return value


PromoStatus = Literal["active", "disabled", "expired", "used_up"]


class PromoCodeItem(BaseModel):
    id: uuid.UUID
    code: str
    kind: PromoKind
    percent_off: int | None
    free_months: int | None
    expires_at: datetime | None
    max_uses: int | None
    active: bool
    note: str | None
    # Хэдэн хэрэглэгч ашигласан (хувийн код — амжилттай төлбөр).
    uses: int
    status: PromoStatus
    created_at: datetime
    # Үүсгэсэн админы нэр. Бүртгэл нь устсан бол `None`.
    created_by: str | None
