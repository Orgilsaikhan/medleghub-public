import uuid
from datetime import datetime
from typing import Annotated, Literal

from pydantic import BaseModel, StringConstraints

from app.models.enums import FeedbackKind
from app.schemas.common import ORMModel

# Зөвхөн сайтын доторх зам (`/courses/python`). Админ UI үүнийг холбоос болгодог
# тул `javascript:`, мөн гадаад сайт руу заах `//host`, `/\host` хэлбэрийг хүлээж
# авахгүй (хөтөч `\`-ийг `/` гэж уншдаг).
PagePath = Annotated[str, StringConstraints(max_length=300, pattern=r"^/([^/\\\s]\S*)?$")]


class FeedbackCreate(BaseModel):
    # `report` нь зөвхөн Community-ийн «Мэдэгдэх» товчоор үүснэ.
    kind: Literal[FeedbackKind.IDEA, FeedbackKind.BUG, FeedbackKind.OTHER]
    message: Annotated[str, StringConstraints(min_length=5, max_length=2000, strip_whitespace=True)]
    page: PagePath | None = None


class FeedbackUpdate(BaseModel):
    resolved: bool


class FeedbackAuthor(ORMModel):
    id: uuid.UUID
    name: str
    email: str


class FeedbackItem(ORMModel):
    id: uuid.UUID
    kind: FeedbackKind
    message: str
    page: str | None
    resolved: bool
    created_at: datetime
    user: FeedbackAuthor
