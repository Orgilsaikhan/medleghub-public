"""Бусад суралцагчийг харах — сургалтын суралцагчид, нийтийн профайл.

Имэйл, эрх, багцын мэдээлэл энд ХЭЗЭЭ Ч орохгүй — зөвхөн нэр, зураг, ахиц.
"""

import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.badge import BadgeStatus, ProfileStats
from app.schemas.common import ORMModel
from app.schemas.course import CourseProgress


class PublicUser(ORMModel):
    id: uuid.UUID
    name: str
    avatar_key: str | None
    created_at: datetime


class CourseStudent(BaseModel):
    id: uuid.UUID
    name: str
    avatar_key: str | None
    percent: int = Field(ge=0, le=100)
    """Энэ сургалтын ахиц."""


class CourseStudents(BaseModel):
    total: int
    items: list[CourseStudent]


class ProfileCourse(BaseModel):
    slug: str
    title: str
    category: str
    progress: CourseProgress


class PublicProfileResponse(BaseModel):
    user: PublicUser
    stats: ProfileStats
    badges: list[BadgeStatus]
    courses: list[ProfileCourse]
