"""Lesson унших болон админ CRUD."""

import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.errors import ConflictError, ForbiddenError, NotFoundError
from app.models.course import Course
from app.models.lesson import Lesson
from app.models.module import Module
from app.models.user import User
from app.schemas.learn import LearnCourse, LessonPlayerResponse
from app.schemas.lesson import LessonCreate, LessonDetail, LessonHelp, LessonLink, LessonUpdate
from app.services import stats
from app.services.access import assert_lesson_unlocked, locked_lesson_ids
from app.services.curriculum import build_curriculum, flatten_lessons
from app.services.module_service import get_module_or_404
from app.services.progress_service import is_enrolled


def _not_found() -> NotFoundError:
    return NotFoundError("LESSON_NOT_FOUND", "Хичээл олдсонгүй.")


async def get_lesson_or_404(db: AsyncSession, lesson_id: uuid.UUID) -> Lesson:
    lesson = await db.get(Lesson, lesson_id)
    if lesson is None:
        raise _not_found()
    return lesson


async def get_lesson_detail(db: AsyncSession, lesson_id: uuid.UUID, user: User) -> LessonDetail:
    lesson = await get_lesson_or_404(db, lesson_id)
    if not lesson.published and not user.is_admin:
        raise _not_found()
    await assert_lesson_unlocked(db, lesson, user)

    course_id = (
        await db.execute(select(Module.course_id).where(Module.id == lesson.module_id))
    ).scalar_one()
    done = await stats.completed_lesson_ids(db, user.id, course_id)

    detail = LessonDetail.model_validate(lesson)
    detail.completed = lesson.id in done
    return detail


async def get_lesson_help(db: AsyncSession, lesson_id: uuid.UUID, user: User) -> LessonHelp:
    """Дасгалын зөвлөгөө ба жишиг шийдэл.

    Хичээлийг үзэх эрхтэй адил шалгана (нийтлэгдсэн эсвэл админ, төлбөрт бол
    багцтай) — бүртгэл шаардахгүй, учир нь хичээл өөрөө бүртгэлгүй харагддаг.
    """
    lesson = await get_lesson_or_404(db, lesson_id)
    if not lesson.published and not user.is_admin:
        raise _not_found()
    await assert_lesson_unlocked(db, lesson, user)

    exercise = lesson.exercise or {}
    solution = exercise.get("solution")
    if not solution:
        raise NotFoundError("HELP_NOT_FOUND", "Энэ хичээлд тусламж байхгүй.")
    return LessonHelp(tips=exercise.get("tips") or "", solution=solution)


async def get_lesson_player(
    db: AsyncSession, course_slug: str, lesson_slug: str, user: User
) -> LessonPlayerResponse:
    """Lesson хуудсанд шаардлагатай бүх өгөгдлийг нэг дуудлагаар буцаана."""
    course = (
        await db.execute(
            select(Course)
            .where(Course.slug == course_slug)
            .options(selectinload(Course.modules).selectinload(Module.lessons))
        )
    ).scalar_one_or_none()
    if course is None or (not course.published and not user.is_admin):
        raise NotFoundError("COURSE_NOT_FOUND", "Сургалт олдсонгүй.")

    include_unpublished = user.is_admin
    ordered = flatten_lessons(course, include_unpublished=include_unpublished)
    lesson = next((item for item in ordered if item.slug == lesson_slug), None)
    if lesson is None:
        raise _not_found()

    done = await stats.completed_lesson_ids(db, user.id, course.id)
    index = ordered.index(lesson)
    locked = locked_lesson_ids(course, user)

    detail = LessonDetail.model_validate(lesson)
    detail.completed = lesson.id in done
    if lesson.id in locked:
        # 402 биш — хуудас curriculum, өмнөх/дараагийн холбоосоо харуулж,
        # агуулгын оронд багцын санал харуулна. Агуулга сервер дээрээ үлдэнэ.
        detail = _locked_detail(detail)

    return LessonPlayerResponse(
        course=LearnCourse(id=course.id, title=course.title, slug=course.slug),
        lesson=detail,
        modules=build_curriculum(
            course, done, include_unpublished=include_unpublished, locked_ids=locked
        ),
        progress=stats.build_progress(sum(1 for item in ordered if item.id in done), len(ordered)),
        enrolled=await is_enrolled(db, user.id, course.id),
        previous_lesson=_link(ordered[index - 1]) if index > 0 else None,
        next_lesson=_link(ordered[index + 1]) if index + 1 < len(ordered) else None,
    )


def _link(lesson: Lesson) -> LessonLink:
    return LessonLink(slug=lesson.slug, title=lesson.title)


def _locked_detail(detail: LessonDetail) -> LessonDetail:
    """Гарчиг, тайлбар үлдэнэ; үзэх, ажиллуулах бүх зүйл хасагдана."""
    return detail.model_copy(
        update={
            "content": "",
            "initial_code": "",
            "video_url": None,
            "exercise": None,
            "locked": True,
        }
    )


# --- Admin CRUD -----------------------------------------------------------


async def _assert_slug_unique_in_course(
    db: AsyncSession,
    module_id: uuid.UUID,
    slug: str,
    exclude_lesson_id: uuid.UUID | None = None,
) -> None:
    """Slug нь course-ийн хэмжээнд давхардахгүй байхыг баталгаажуулна.

    DB-ийн unique constraint зөвхөн module хүртэл хамаардаг тул course түвшний
    шалгалтыг энд хийнэ (`/learn/:courseSlug/:lessonSlug` route-ыг тодорхой байлгана).
    """
    course_id = (
        await db.execute(select(Module.course_id).where(Module.id == module_id))
    ).scalar_one()
    stmt = (
        select(func.count())
        .select_from(Lesson)
        .join(Module, Module.id == Lesson.module_id)
        .where(Module.course_id == course_id, Lesson.slug == slug)
    )
    if exclude_lesson_id:
        stmt = stmt.where(Lesson.id != exclude_lesson_id)
    if (await db.execute(stmt)).scalar_one() > 0:
        raise ConflictError(
            "LESSON_SLUG_TAKEN", "Энэ сургалт дотор ийм slug-тай хичээл аль хэдийн байна."
        )


async def _next_position(db: AsyncSession, module_id: uuid.UUID) -> int:
    current_max = (
        await db.execute(select(func.max(Lesson.position)).where(Lesson.module_id == module_id))
    ).scalar_one_or_none()
    return 0 if current_max is None else current_max + 1


async def create_lesson(db: AsyncSession, module_id: uuid.UUID, payload: LessonCreate) -> Lesson:
    await get_module_or_404(db, module_id)
    await _assert_slug_unique_in_course(db, module_id, payload.slug)

    data = payload.model_dump()
    if "position" not in payload.model_fields_set:
        data["position"] = await _next_position(db, module_id)

    lesson = Lesson(module_id=module_id, **data)
    db.add(lesson)
    await db.commit()
    await db.refresh(lesson)
    return lesson


async def update_lesson(db: AsyncSession, lesson_id: uuid.UUID, payload: LessonUpdate) -> Lesson:
    lesson = await get_lesson_or_404(db, lesson_id)
    data = payload.model_dump(exclude_unset=True)

    target_module_id = data.get("module_id", lesson.module_id)
    if "module_id" in data:
        await get_module_or_404(db, target_module_id)
    if "slug" in data or "module_id" in data:
        await _assert_slug_unique_in_course(
            db, target_module_id, data.get("slug", lesson.slug), exclude_lesson_id=lesson.id
        )

    for field, value in data.items():
        setattr(lesson, field, value)
    await db.commit()
    await db.refresh(lesson)
    return lesson


async def delete_lesson(db: AsyncSession, lesson_id: uuid.UUID) -> None:
    lesson = await get_lesson_or_404(db, lesson_id)
    await db.delete(lesson)
    await db.commit()


async def assert_lesson_accessible(db: AsyncSession, lesson: Lesson, user: User) -> uuid.UUID:
    """Хичээлийг дуусгахаас өмнөх шалгалт. Тухайн course-ийн ID-г буцаана."""
    if not lesson.published and not user.is_admin:
        raise _not_found()
    course_id = (
        await db.execute(select(Module.course_id).where(Module.id == lesson.module_id))
    ).scalar_one()
    if not await is_enrolled(db, user.id, course_id) and not user.is_admin:
        raise ForbiddenError("NOT_ENROLLED", "Энэ сургалтад эхлээд бүртгүүлнэ үү.")
    await assert_lesson_unlocked(db, lesson, user)
    return course_id
