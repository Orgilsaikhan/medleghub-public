"""Enrollment болон хичээлийн ахицын логик.

Ахицыг зөвхөн сервер шийднэ — client-ээс ирсэн "дууссан" төлөвт итгэхгүй.
"""

import uuid
from datetime import UTC, datetime

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.errors import NotFoundError
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.models.lesson import Lesson
from app.models.module import Module
from app.models.progress import LessonProgress
from app.models.user import User
from app.schemas.course import CourseProgress, CourseSummary
from app.schemas.progress import ContinueLink, EnrollmentResponse, MyCourse
from app.services import stats
from app.services.curriculum import flatten_lessons


async def is_enrolled(db: AsyncSession, user_id: uuid.UUID, course_id: uuid.UUID) -> bool:
    found = (
        await db.execute(
            select(Enrollment.id).where(
                Enrollment.user_id == user_id, Enrollment.course_id == course_id
            )
        )
    ).scalar_one_or_none()
    return found is not None


async def enroll(db: AsyncSession, user: User, course_id: uuid.UUID) -> EnrollmentResponse:
    course = await db.get(Course, course_id)
    if course is None or (not course.published and not user.is_admin):
        raise NotFoundError("COURSE_NOT_FOUND", "Сургалт олдсонгүй.")

    existing = (
        await db.execute(
            select(Enrollment).where(
                Enrollment.user_id == user.id, Enrollment.course_id == course_id
            )
        )
    ).scalar_one_or_none()
    if existing:
        return EnrollmentResponse(
            course_id=course_id, enrolled_at=existing.created_at, already_enrolled=True
        )

    enrollment = Enrollment(user_id=user.id, course_id=course_id)
    db.add(enrollment)
    try:
        await db.commit()
    except IntegrityError:
        # Зэрэг ирсэн хоёр хүсэлт — давхардлыг чимээгүй зөөлрүүлнэ.
        await db.rollback()
        existing = (
            await db.execute(
                select(Enrollment).where(
                    Enrollment.user_id == user.id, Enrollment.course_id == course_id
                )
            )
        ).scalar_one()
        return EnrollmentResponse(
            course_id=course_id, enrolled_at=existing.created_at, already_enrolled=True
        )

    await db.refresh(enrollment)
    return EnrollmentResponse(
        course_id=course_id, enrolled_at=enrollment.created_at, already_enrolled=False
    )


async def complete_lesson(
    db: AsyncSession, user: User, lesson: Lesson
) -> tuple[LessonProgress, uuid.UUID]:
    """Хичээлийг дууссан гэж тэмдэглэнэ. Дахин дуудахад төлөв өөрчлөгдөхгүй."""
    record = (
        await db.execute(
            select(LessonProgress).where(
                LessonProgress.user_id == user.id, LessonProgress.lesson_id == lesson.id
            )
        )
    ).scalar_one_or_none()

    if record is None:
        record = LessonProgress(
            user_id=user.id,
            lesson_id=lesson.id,
            completed=True,
            completed_at=datetime.now(UTC),
        )
        db.add(record)
        try:
            await db.commit()
        except IntegrityError:
            await db.rollback()
            record = (
                await db.execute(
                    select(LessonProgress).where(
                        LessonProgress.user_id == user.id,
                        LessonProgress.lesson_id == lesson.id,
                    )
                )
            ).scalar_one()
    elif not record.completed:
        record.completed = True
        record.completed_at = datetime.now(UTC)
        await db.commit()

    await db.refresh(record)
    course_id = (
        await db.execute(select(Module.course_id).where(Module.id == lesson.module_id))
    ).scalar_one()
    return record, course_id


async def course_progress(db: AsyncSession, user: User, course_id: uuid.UUID) -> CourseProgress:
    include_unpublished = user.is_admin
    course_stats = await stats.course_stats(
        db, [course_id], include_unpublished=include_unpublished
    )
    done = await stats.completed_counts(
        db, user.id, [course_id], include_unpublished=include_unpublished
    )
    return stats.build_progress(done.get(course_id, 0), course_stats[course_id].lesson_count)


async def my_courses(db: AsyncSession, user: User) -> list[MyCourse]:
    """Dashboard-ийн үндсэн query.

    Хичээлийн бүтцийг нэг selectinload-оор ачаалж, ахицыг нэг IN query-ээр авна —
    сургалтын тооноос үл хамааран query-ийн тоо тогтмол.
    """
    rows = await db.execute(
        select(Enrollment, Course)
        .join(Course, Course.id == Enrollment.course_id)
        .where(Enrollment.user_id == user.id)
        .options(
            selectinload(Enrollment.course)
            .selectinload(Course.modules)
            .selectinload(Module.lessons)
        )
        .order_by(Enrollment.created_at.desc())
    )
    pairs = rows.all()
    if not pairs:
        return []

    course_ids = [course.id for _, course in pairs]
    done_ids = await _completed_lesson_ids_for_courses(db, user.id, course_ids)
    last_completed = await _last_completed_at(db, user.id, course_ids)

    result: list[MyCourse] = []
    for enrollment, course in pairs:
        lessons = flatten_lessons(course, include_unpublished=False)
        completed_ids = done_ids.get(course.id, set())

        summary = CourseSummary.model_validate(course)
        summary.lesson_count = len(lessons)
        summary.duration = sum(lesson.duration for lesson in lessons)
        summary.enrolled = True
        progress = stats.build_progress(
            sum(1 for lesson in lessons if lesson.id in completed_ids), len(lessons)
        )
        summary.progress = progress

        next_lesson = next(
            (lesson for lesson in lessons if lesson.id not in completed_ids),
            lessons[-1] if lessons else None,
        )
        result.append(
            MyCourse(
                course=summary,
                enrolled_at=enrollment.created_at,
                progress=progress,
                continue_lesson=(
                    ContinueLink(
                        slug=next_lesson.slug,
                        title=next_lesson.title,
                        course_slug=course.slug,
                    )
                    if next_lesson
                    else None
                ),
                last_completed_at=last_completed.get(course.id),
            )
        )
    return result


async def _completed_lesson_ids_for_courses(
    db: AsyncSession, user_id: uuid.UUID, course_ids: list[uuid.UUID]
) -> dict[uuid.UUID, set[uuid.UUID]]:
    rows = await db.execute(
        select(Module.course_id, LessonProgress.lesson_id)
        .join(Lesson, Lesson.id == LessonProgress.lesson_id)
        .join(Module, Module.id == Lesson.module_id)
        .where(
            LessonProgress.user_id == user_id,
            LessonProgress.completed.is_(True),
            Module.course_id.in_(course_ids),
        )
    )
    grouped: dict[uuid.UUID, set[uuid.UUID]] = {}
    for course_id, lesson_id in rows.all():
        grouped.setdefault(course_id, set()).add(lesson_id)
    return grouped


async def _last_completed_at(
    db: AsyncSession, user_id: uuid.UUID, course_ids: list[uuid.UUID]
) -> dict[uuid.UUID, datetime]:
    rows = await db.execute(
        select(Module.course_id, func.max(LessonProgress.completed_at))
        .join(Lesson, Lesson.id == LessonProgress.lesson_id)
        .join(Module, Module.id == Lesson.module_id)
        .where(
            LessonProgress.user_id == user_id,
            LessonProgress.completed.is_(True),
            Module.course_id.in_(course_ids),
        )
        .group_by(Module.course_id)
    )
    return {course_id: value for course_id, value in rows.all() if value is not None}
