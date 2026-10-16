import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.badge import BadgeUnlocked
from app.schemas.course import CourseProgress, CourseSummary
from app.schemas.lesson import LessonLink


class EnrollmentResponse(BaseModel):
    course_id: uuid.UUID
    enrolled_at: datetime
    already_enrolled: bool


class LessonCompleteResponse(BaseModel):
    lesson_id: uuid.UUID
    completed: bool
    completed_at: datetime | None
    course_progress: CourseProgress
    # Энэ хичээлээр шинээр авсан тэмдгүүд — UI мэдэгдэл харуулна.
    new_badges: list[BadgeUnlocked] = []


class ContinueLink(LessonLink):
    """Dashboard дээрх «Үргэлжлүүлэх» товчны зорилго."""

    course_slug: str


class MyCourse(BaseModel):
    course: CourseSummary
    enrolled_at: datetime
    progress: CourseProgress
    continue_lesson: ContinueLink | None = None
    last_completed_at: datetime | None = None


class CaseAnswerRequest(BaseModel):
    answer: str = Field(min_length=1, max_length=200)


class CaseAnswerResponse(BaseModel):
    """`completed` — ахиц хадгалагдсан (бүртгүүлсэн сурагч, зөв хариулт)."""

    correct: bool
    completed: bool
    course_progress: CourseProgress | None = None
    new_badges: list[BadgeUnlocked] = []
