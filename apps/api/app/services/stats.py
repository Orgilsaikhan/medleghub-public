"""Ахиц болон curriculum-ийн нэгтгэсэн тоон үзүүлэлт.

Бүх функц нь олон course-ыг нэг query-ээр боловсруулдаг — жагсаалтын хуудсууд
N+1 query үүсгэхгүй.
"""

import uuid
from dataclasses import dataclass

from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.lesson import Lesson
from app.models.module import Module
from app.models.progress import LessonProgress
from app.schemas.course import CourseProgress


@dataclass(frozen=True, slots=True)
class CourseStats:
    lesson_count: int = 0
    duration: int = 0


def _published_filter(stmt: Select, include_unpublished: bool) -> Select:
    return stmt if include_unpublished else stmt.where(Lesson.published.is_(True))


async def course_stats(
    db: AsyncSession,
    course_ids: list[uuid.UUID],
    *,
    include_unpublished: bool = False,
) -> dict[uuid.UUID, CourseStats]:
    """Course бүрийн хичээлийн тоо болон нийт үргэлжлэх хугацаа (секунд)."""
    if not course_ids:
        return {}
    stmt = (
        select(
            Module.course_id,
            func.count(Lesson.id),
            func.coalesce(func.sum(Lesson.duration), 0),
        )
        .join(Lesson, Lesson.module_id == Module.id)
        .where(Module.course_id.in_(course_ids))
        .group_by(Module.course_id)
    )
    rows = (await db.execute(_published_filter(stmt, include_unpublished))).all()
    stats = {course_id: CourseStats(count, int(total)) for course_id, count, total in rows}
    return {course_id: stats.get(course_id, CourseStats()) for course_id in course_ids}


async def completed_counts(
    db: AsyncSession,
    user_id: uuid.UUID,
    course_ids: list[uuid.UUID],
    *,
    include_unpublished: bool = False,
) -> dict[uuid.UUID, int]:
    """Course бүрт хэрэглэгчийн дуусгасан хичээлийн тоо."""
    if not course_ids:
        return {}
    stmt = (
        select(Module.course_id, func.count(LessonProgress.id))
        .join(Lesson, Lesson.id == LessonProgress.lesson_id)
        .join(Module, Module.id == Lesson.module_id)
        .where(
            LessonProgress.user_id == user_id,
            LessonProgress.completed.is_(True),
            Module.course_id.in_(course_ids),
        )
        .group_by(Module.course_id)
    )
    rows = (await db.execute(_published_filter(stmt, include_unpublished))).all()
    counts = dict(rows)
    return {course_id: counts.get(course_id, 0) for course_id in course_ids}


async def completed_lesson_ids(
    db: AsyncSession,
    user_id: uuid.UUID,
    course_id: uuid.UUID,
) -> set[uuid.UUID]:
    """Тухайн course доторх дуусгасан хичээлүүдийн ID — curriculum тэмдэглэхэд."""
    stmt = (
        select(LessonProgress.lesson_id)
        .join(Lesson, Lesson.id == LessonProgress.lesson_id)
        .join(Module, Module.id == Lesson.module_id)
        .where(
            LessonProgress.user_id == user_id,
            LessonProgress.completed.is_(True),
            Module.course_id == course_id,
        )
    )
    return set((await db.execute(stmt)).scalars().all())


def build_progress(completed: int, total: int) -> CourseProgress:
    percent = round(completed / total * 100) if total else 0
    return CourseProgress(
        completed_lessons=min(completed, total),
        total_lessons=total,
        percent=min(percent, 100),
    )
