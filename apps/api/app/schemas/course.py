import uuid
from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field, StringConstraints

from app.models.enums import Category, Difficulty
from app.schemas.common import ORMModel, Slug
from app.schemas.module import ModuleWithLessons

Title = Annotated[str, StringConstraints(min_length=2, max_length=200, strip_whitespace=True)]


class CourseProgress(BaseModel):
    completed_lessons: int
    total_lessons: int
    percent: int = Field(ge=0, le=100)


class CourseSummary(ORMModel):
    """Catalog карт болон жагсаалтад ашиглагдана."""

    id: uuid.UUID
    title: str
    slug: str
    description: str
    thumbnail_url: str | None
    difficulty: str
    category: str
    is_free: bool
    # `is_free=False` үед эхний хэдэн хичээл үнэгүй вэ.
    free_lessons: int
    published: bool
    lesson_count: int = 0
    duration: int = 0  # секунд, хичээлүүдийн нийлбэр
    enrolled: bool = False
    progress: CourseProgress | None = None


class CourseDetail(CourseSummary):
    created_at: datetime
    updated_at: datetime
    modules: list[ModuleWithLessons] = Field(default_factory=list)


class CourseCreate(BaseModel):
    title: Title
    slug: Slug
    description: str = Field(default="", max_length=5000)
    thumbnail_url: str | None = Field(default=None, max_length=500)
    difficulty: Difficulty = Difficulty.BEGINNER
    category: Category = Category.JAVASCRIPT
    is_free: bool = True
    free_lessons: int = Field(default=0, ge=0, le=10_000)
    published: bool = False


class CourseUpdate(BaseModel):
    title: Title | None = None
    slug: Slug | None = None
    description: str | None = Field(default=None, max_length=5000)
    thumbnail_url: str | None = Field(default=None, max_length=500)
    difficulty: Difficulty | None = None
    category: Category | None = None
    is_free: bool | None = None
    free_lessons: int | None = Field(default=None, ge=0, le=10_000)
    published: bool | None = None
