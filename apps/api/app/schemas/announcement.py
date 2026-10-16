"""Админы зарлал (popup)."""

import uuid
from datetime import UTC, datetime
from typing import Annotated, Literal

from pydantic import BaseModel, Field, StringConstraints, field_validator, model_validator

from app.models.enums import AnnouncementAudience, AnnouncementKind

Title = Annotated[str, StringConstraints(min_length=2, max_length=120, strip_whitespace=True)]
Body = Annotated[str, StringConstraints(min_length=1, max_length=2000, strip_whitespace=True)]
CtaLabel = Annotated[str, StringConstraints(min_length=1, max_length=40, strip_whitespace=True)]

URL_ERROR = "Холбоос `/`-ээр (сайтын хуудас) эсвэл `https://`-ээр эхлэх ёстой."


def _clean_url(value: str | None) -> str | None:
    """Сайтын хуудас (`/pricing`) эсвэл `https://…`. `//evil.com`, `javascript:` болохгүй."""
    if value is None:
        return None
    value = value.strip()
    if not value:
        return None
    if any(ch.isspace() for ch in value):
        raise ValueError(URL_ERROR)
    internal = value.startswith("/") and not value.startswith("//")
    if not internal and not value.startswith("https://"):
        raise ValueError(URL_ERROR)
    return value


def _aware(value: datetime | None) -> datetime | None:
    if value is not None and value.tzinfo is None:
        return value.replace(tzinfo=UTC)
    return value


class _Validators(BaseModel):
    @field_validator("cta_label", mode="before", check_fields=False)
    @classmethod
    def blank_label_is_none(cls, value: object) -> object:
        if isinstance(value, str) and not value.strip():
            return None
        return value

    @field_validator("cta_url", check_fields=False)
    @classmethod
    def valid_url(cls, value: str | None) -> str | None:
        return _clean_url(value)

    @field_validator("starts_at", "ends_at", check_fields=False)
    @classmethod
    def aware(cls, value: datetime | None) -> datetime | None:
        return _aware(value)


class AnnouncementCreate(_Validators):
    kind: AnnouncementKind
    title: Title
    body: Body
    cta_label: CtaLabel | None = None
    cta_url: str | None = Field(default=None, max_length=500)
    audience: AnnouncementAudience
    starts_at: datetime | None = None
    ends_at: datetime | None = None
    # `false` — ноорог хэлбэрээр хадгална.
    active: bool = False

    @model_validator(mode="after")
    def consistent(self) -> "AnnouncementCreate":
        if (self.cta_label is None) != (self.cta_url is None):
            raise ValueError("Товчны бичвэр, холбоосыг хамт оруулна уу.")
        if self.starts_at and self.ends_at and self.ends_at <= self.starts_at:
            raise ValueError("Дуусах өдөр эхлэх өдрөөс хойш байх ёстой.")
        if self.ends_at is not None and self.ends_at <= datetime.now(UTC):
            raise ValueError("Дуусах өдөр ирээдүйд байх ёстой.")
        return self


class AnnouncementUpdate(_Validators):
    """Зөвхөн ирсэн талбарыг өөрчилнө. Товч, хугацааны уялдааг сервер
    өөрчилсний дараах утгаар шалгана."""

    kind: AnnouncementKind | None = None
    title: Title | None = None
    body: Body | None = None
    cta_label: CtaLabel | None = None
    cta_url: str | None = Field(default=None, max_length=500)
    audience: AnnouncementAudience | None = None
    starts_at: datetime | None = None
    ends_at: datetime | None = None
    active: bool | None = None

    @model_validator(mode="after")
    def required_not_null(self) -> "AnnouncementUpdate":
        for name in ("kind", "title", "body", "audience", "active"):
            if name in self.model_fields_set and getattr(self, name) is None:
                raise ValueError(f"`{name}` хоосон байж болохгүй.")
        return self


class AnnouncementPublic(BaseModel):
    """Хэрэглэгчид харагдах цонхны агуулга."""

    id: uuid.UUID
    kind: AnnouncementKind
    title: str
    body: str
    cta_label: str | None
    cta_url: str | None


AnnouncementStatus = Literal["draft", "scheduled", "live", "ended"]


class AnnouncementItem(AnnouncementPublic):
    """Админд: бүх тохиргоо ба төлөв."""

    audience: AnnouncementAudience
    starts_at: datetime | None
    ends_at: datetime | None
    active: bool
    # `draft` — нийтлээгүй; `scheduled` — эхлэх өдөр болоогүй; `live` — харагдаж
    # байна; `ended` — дуусах өдөр өнгөрсөн.
    status: AnnouncementStatus
    created_at: datetime
    updated_at: datetime
    # Бичсэн админы нэр. Бүртгэл нь устсан бол `None`.
    created_by: str | None
