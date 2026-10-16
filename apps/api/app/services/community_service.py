"""Бусад суралцагчийг харах — сургалтын суралцагчид ба нийтийн профайл.

Зөвхөн нэвтэрсэн хэрэглэгчид. Хариунд имэйл, эрх, багцын мэдээлэл орохгүй
(`app/schemas/community.py`).
"""

import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import ForbiddenError, NotFoundError
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.models.enums import UserRole
from app.models.lesson import Lesson
from app.models.module import Module
from app.models.progress import LessonProgress
from app.models.user import User
from app.schemas.community import (
    CourseStudent,
    CourseStudents,
    ProfileCourse,
    PublicProfileResponse,
    PublicUser,
)
from app.services import badge_service, course_service, stats

MAX_STUDENTS = 50


async def course_students(db: AsyncSession, slug: str, viewer: User, limit: int) -> CourseStudents:
    """Сургалтад бүртгүүлсэн суралцагчид, ахиц ихээс нь бага руу.

    Админууд жагсаалтад орохгүй. Профайлаа нуусан суралцагч нэрээр харагдахгүй
    ч нийт тоонд орно. Ахицыг нэг GROUP BY query-ээр тоолно — суралцагчийн
    тооноос үл хамааран query-ийн тоо тогтмол.
    """
    course = await course_service.visible_course(db, slug, viewer)
    total_lessons = (await stats.course_stats(db, [course.id]))[course.id].lesson_count

    done = (
        select(LessonProgress.user_id, func.count(LessonProgress.id).label("done"))
        .join(Lesson, Lesson.id == LessonProgress.lesson_id)
        .join(Module, Module.id == Lesson.module_id)
        .where(
            Module.course_id == course.id,
            LessonProgress.completed.is_(True),
            Lesson.published.is_(True),
        )
        .group_by(LessonProgress.user_id)
        .subquery()
    )
    enrolled = (
        select(User.id)
        .join(Enrollment, Enrollment.user_id == User.id)
        .where(Enrollment.course_id == course.id, User.role == UserRole.STUDENT)
    )

    total = (await db.execute(select(func.count()).select_from(enrolled.subquery()))).scalar_one()
    done_count = func.coalesce(done.c.done, 0)
    rows = await db.execute(
        enrolled.add_columns(User.name, User.avatar_key, done_count)
        .where(User.profile_hidden.is_(False))
        .outerjoin(done, done.c.user_id == User.id)
        .order_by(done_count.desc(), Enrollment.created_at, User.id)
        .limit(limit)
    )
    return CourseStudents(
        total=total,
        items=[
            CourseStudent(
                id=user_id,
                name=name,
                avatar_key=avatar_key,
                percent=stats.build_progress(completed, total_lessons).percent,
            )
            for user_id, name, avatar_key, completed in rows.all()
        ],
    )


async def public_profile(
    db: AsyncSession, user_id: uuid.UUID, viewer: User
) -> PublicProfileResponse:
    user = await db.get(User, user_id)
    if user is None:
        raise NotFoundError("USER_NOT_FOUND", "Хэрэглэгч олдсонгүй.")
    if user.profile_hidden and user.id != viewer.id:
        raise ForbiddenError("PROFILE_HIDDEN", "Энэ суралцагч профайлаа нуусан байна.")

    profile_stats, badges = await badge_service.summary(db, user, award=False)

    courses = (
        (
            await db.execute(
                select(Course)
                .join(Enrollment, Enrollment.course_id == Course.id)
                .where(Enrollment.user_id == user.id, Course.published.is_(True))
                .order_by(Enrollment.created_at.desc())
            )
        )
        .scalars()
        .all()
    )
    course_ids = [course.id for course in courses]
    course_stats = await stats.course_stats(db, course_ids)
    done = await stats.completed_counts(db, user.id, course_ids)

    return PublicProfileResponse(
        user=PublicUser.model_validate(user),
        stats=profile_stats,
        badges=badges,
        courses=[
            ProfileCourse(
                slug=course.slug,
                title=course.title,
                category=course.category,
                progress=stats.build_progress(
                    done[course.id], course_stats[course.id].lesson_count
                ),
            )
            for course in courses
        ],
    )
