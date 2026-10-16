"""Course-ийн унших болон админ CRUD логик."""

import uuid

from sqlalchemy import Select, func, or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.errors import ConflictError, NotFoundError
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.models.lesson import Lesson
from app.models.module import Module
from app.models.user import User
from app.schemas.course import CourseCreate, CourseDetail, CourseSummary, CourseUpdate
from app.services import stats
from app.services.access import locked_lesson_ids
from app.services.curriculum import build_curriculum

DEFAULT_PAGE_SIZE = 12
MAX_PAGE_SIZE = 48


def _not_found() -> NotFoundError:
    return NotFoundError("COURSE_NOT_FOUND", "Сургалт олдсонгүй.")


def _visible(stmt: Select, user: User | None) -> Select:
    """Админ бүх сургалтыг, бусад нь зөвхөн нийтлэгдсэнийг харна."""
    if user and user.is_admin:
        return stmt
    return stmt.where(Course.published.is_(True))


async def _enrolled_course_ids(
    db: AsyncSession, user: User | None, course_ids: list[uuid.UUID]
) -> set[uuid.UUID]:
    if not user or not course_ids:
        return set()
    rows = await db.execute(
        select(Enrollment.course_id).where(
            Enrollment.user_id == user.id, Enrollment.course_id.in_(course_ids)
        )
    )
    return set(rows.scalars().all())


async def _decorate(
    db: AsyncSession,
    courses: list[Course],
    user: User | None,
    *,
    include_unpublished_lessons: bool = False,
) -> dict[uuid.UUID, CourseSummary]:
    """Course бүрт хичээлийн тоо, үргэлжлэх хугацаа, enrollment, ахицыг нэмнэ.

    Нийт 3 нэмэлт query — сургалтын тооноос үл хамааран тогтмол.
    """
    course_ids = [course.id for course in courses]
    course_stats = await stats.course_stats(
        db, course_ids, include_unpublished=include_unpublished_lessons
    )
    enrolled_ids = await _enrolled_course_ids(db, user, course_ids)
    completed = (
        await stats.completed_counts(
            db, user.id, course_ids, include_unpublished=include_unpublished_lessons
        )
        if user
        else {}
    )

    result: dict[uuid.UUID, CourseSummary] = {}
    for course in courses:
        summary = CourseSummary.model_validate(course)
        stat = course_stats[course.id]
        summary.lesson_count = stat.lesson_count
        summary.duration = stat.duration
        summary.enrolled = course.id in enrolled_ids
        if summary.enrolled:
            summary.progress = stats.build_progress(completed.get(course.id, 0), stat.lesson_count)
        result[course.id] = summary
    return result


async def list_courses(
    db: AsyncSession,
    *,
    user: User | None,
    q: str | None = None,
    category: str | None = None,
    difficulty: str | None = None,
    page: int = 1,
    page_size: int = DEFAULT_PAGE_SIZE,
) -> tuple[list[CourseSummary], int]:
    stmt = _visible(select(Course), user)

    if q:
        pattern = f"%{q.strip()}%"
        stmt = stmt.where(or_(Course.title.ilike(pattern), Course.description.ilike(pattern)))
    if category:
        stmt = stmt.where(Course.category == category)
    if difficulty:
        stmt = stmt.where(Course.difficulty == difficulty)

    total = (await db.execute(select(func.count()).select_from(stmt.subquery()))).scalar_one()

    page_size = min(max(page_size, 1), MAX_PAGE_SIZE)
    rows = await db.execute(
        stmt.order_by(Course.created_at.desc(), Course.id)
        .offset((max(page, 1) - 1) * page_size)
        .limit(page_size)
    )
    courses = list(rows.scalars().all())
    decorated = await _decorate(db, courses, user)
    return [decorated[course.id] for course in courses], total


async def visible_course(db: AsyncSession, slug: str, user: User | None) -> Course:
    """Хэрэглэгчид харагдах сургалт (бүтэцгүй) эсвэл 404."""
    course = (
        await db.execute(_visible(select(Course), user).where(Course.slug == slug))
    ).scalar_one_or_none()
    if course is None:
        raise _not_found()
    return course


async def get_course_by_slug(db: AsyncSession, slug: str, user: User | None) -> CourseDetail:
    course = (
        await db.execute(
            _visible(select(Course), user)
            .where(Course.slug == slug)
            .options(selectinload(Course.modules).selectinload(Module.lessons))
        )
    ).scalar_one_or_none()
    if course is None:
        raise _not_found()

    is_admin = bool(user and user.is_admin)
    summary = (await _decorate(db, [course], user, include_unpublished_lessons=is_admin))[course.id]
    done = await stats.completed_lesson_ids(db, user.id, course.id) if user else set()

    detail = CourseDetail(
        **summary.model_dump(),
        created_at=course.created_at,
        updated_at=course.updated_at,
        modules=build_curriculum(
            course, done, include_unpublished=is_admin, locked_ids=locked_lesson_ids(course, user)
        ),
    )
    return detail


# --- Admin CRUD -----------------------------------------------------------


async def get_course_or_404(db: AsyncSession, course_id: uuid.UUID) -> Course:
    course = await db.get(Course, course_id)
    if course is None:
        raise _not_found()
    return course


async def create_course(db: AsyncSession, payload: CourseCreate) -> Course:
    course = Course(**payload.model_dump())
    db.add(course)
    try:
        await db.commit()
    except IntegrityError as exc:
        await db.rollback()
        raise ConflictError("SLUG_TAKEN", "Энэ slug-тай сургалт аль хэдийн байна.") from exc
    await db.refresh(course)
    return course


async def update_course(db: AsyncSession, course_id: uuid.UUID, payload: CourseUpdate) -> Course:
    course = await get_course_or_404(db, course_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(course, field, value)
    try:
        await db.commit()
    except IntegrityError as exc:
        await db.rollback()
        raise ConflictError("SLUG_TAKEN", "Энэ slug-тай сургалт аль хэдийн байна.") from exc
    await db.refresh(course)
    return course


async def delete_course(db: AsyncSession, course_id: uuid.UUID) -> None:
    course = await get_course_or_404(db, course_id)
    await db.delete(course)
    await db.commit()


async def admin_course_detail(db: AsyncSession, course_id: uuid.UUID) -> CourseDetail:
    """Админ засварын дэлгэц — нийтлэгдээгүй module/lesson-ууд ч харагдана."""
    course = (
        await db.execute(
            select(Course)
            .where(Course.id == course_id)
            .options(selectinload(Course.modules).selectinload(Module.lessons))
        )
    ).scalar_one_or_none()
    if course is None:
        raise _not_found()

    course_stats = await stats.course_stats(db, [course.id], include_unpublished=True)
    summary = CourseSummary.model_validate(course)
    summary.lesson_count = course_stats[course.id].lesson_count
    summary.duration = course_stats[course.id].duration

    return CourseDetail(
        **summary.model_dump(),
        created_at=course.created_at,
        updated_at=course.updated_at,
        modules=build_curriculum(course, set(), include_unpublished=True),
    )


async def course_id_for_lesson(db: AsyncSession, lesson_id: uuid.UUID) -> uuid.UUID | None:
    return (
        await db.execute(
            select(Module.course_id)
            .join(Lesson, Lesson.module_id == Module.id)
            .where(Lesson.id == lesson_id)
        )
    ).scalar_one_or_none()
