"""Community — нийтлэл, сэтгэгдэл, лайк, гомдол.

Зохиогчийн имэйл, эрх, багцын мэдээлэл энд ХЭЗЭЭ Ч орохгүй — зөвхөн нэр, зураг.
"""

import uuid
from datetime import datetime
from enum import StrEnum
from typing import Annotated

from pydantic import BaseModel, StringConstraints

from app.models.enums import PostLanguage, PostType
from app.schemas.common import ORMModel

PostTitle = Annotated[str, StringConstraints(min_length=5, max_length=150, strip_whitespace=True)]
PostBody = Annotated[
    str, StringConstraints(min_length=10, max_length=10_000, strip_whitespace=True)
]
CommentBody = Annotated[
    str, StringConstraints(min_length=1, max_length=3000, strip_whitespace=True)
]


class ReportReason(StrEnum):
    SPAM = "spam"
    ABUSE = "abuse"
    OTHER = "other"


class PostCreate(BaseModel):
    title: PostTitle
    body: PostBody
    language: PostLanguage
    type: PostType


class CommentCreate(BaseModel):
    body: CommentBody


class ReportCreate(BaseModel):
    reason: ReportReason
    details: Annotated[str, StringConstraints(max_length=500, strip_whitespace=True)] | None = None


class PostAuthor(ORMModel):
    id: uuid.UUID
    name: str
    avatar_key: str | None
    # Нуусан бол вэб профайл руу холбоос хийхгүй (профайл нь 403 буцаана).
    profile_hidden: bool


class _PostBase(BaseModel):
    id: uuid.UUID
    title: str
    language: PostLanguage
    type: PostType
    pinned: bool
    # NULL бол MedlegHub-ийн албан ёсны нийтлэл.
    author: PostAuthor | None
    created_at: datetime
    like_count: int
    comment_count: int
    # Одоогийн хэрэглэгч лайк дарсан эсэх.
    liked: bool


class PostSummary(_PostBase):
    # Жагсаалтад харуулах богино хэсэг — Markdown тэмдэгтгүй, нэг мөр.
    excerpt: str


class CommentItem(ORMModel):
    id: uuid.UUID
    body: str
    created_at: datetime
    author: PostAuthor


class PostDetail(_PostBase):
    body: str
    # Хуучнаас нь шинэ рүү.
    comments: list[CommentItem]


class LikeResult(BaseModel):
    liked: bool
    like_count: int


# --- Дүрэм ба түдгэлзүүлэлт --------------------------------------------------


class SuspensionInfo(BaseModel):
    """Хэрэглэгчид өөрт нь харагдах идэвхтэй түдгэлзүүлэлт."""

    level: int
    reason: str
    created_at: datetime
    # NULL бол бүрмөсөн.
    ends_at: datetime | None


class CommunityStatus(BaseModel):
    guidelines_accepted: bool
    suspension: SuspensionInfo | None
    # Удаа тутмын түдгэлзүүлэх хоног — дүрмийн цонхонд харуулна. Жагсаалт
    # дууссаны дараагийн зөрчил бүрмөсөн.
    suspension_days: list[int]


class SuspensionCreate(BaseModel):
    user_id: uuid.UUID
    reason: Annotated[str, StringConstraints(min_length=5, max_length=500, strip_whitespace=True)]


class SuspensionUser(ORMModel):
    id: uuid.UUID
    name: str
    email: str


class SuspensionAdmin(ORMModel):
    id: uuid.UUID
    name: str


class SuspensionItem(BaseModel):
    """Админы жагсаалтын мөр."""

    id: uuid.UUID
    user: SuspensionUser
    admin: SuspensionAdmin | None
    level: int
    reason: str
    created_at: datetime
    ends_at: datetime | None
    lifted_at: datetime | None
    active: bool
