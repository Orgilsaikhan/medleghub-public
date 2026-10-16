"""Course catalog болон админ CRUD."""

import uuid
from typing import Annotated

from fastapi import APIRouter, Query, status

from app.core.deps import AdminUser, DbSession, OptionalUser
from app.models.enums import Category, Difficulty
from app.schemas.common import MessageResponse, Page
from app.schemas.course import CourseCreate, CourseDetail, CourseSummary, CourseUpdate
from app.schemas.module import ModuleCreate, ModuleWithLessons
from app.services import course_service, module_service

router = APIRouter(tags=["courses"])


@router.get("/courses", response_model=Page[CourseSummary])
async def list_courses(
    db: DbSession,
    user: OptionalUser,
    q: Annotated[str | None, Query(max_length=100)] = None,
    category: Category | None = None,
    difficulty: Difficulty | None = None,
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=course_service.MAX_PAGE_SIZE)] = (
        course_service.DEFAULT_PAGE_SIZE
    ),
) -> Page[CourseSummary]:
    items, total = await course_service.list_courses(
        db,
        user=user,
        q=q,
        category=category.value if category else None,
        difficulty=difficulty.value if difficulty else None,
        page=page,
        page_size=page_size,
    )
    return Page[CourseSummary](
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=max(1, -(-total // page_size)),
    )


@router.get("/courses/{slug}", response_model=CourseDetail)
async def get_course(slug: str, db: DbSession, user: OptionalUser) -> CourseDetail:
    return await course_service.get_course_by_slug(db, slug, user)


@router.post("/courses", response_model=CourseSummary, status_code=status.HTTP_201_CREATED)
async def create_course(payload: CourseCreate, db: DbSession, _: AdminUser) -> CourseSummary:
    course = await course_service.create_course(db, payload)
    return CourseSummary.model_validate(course)


@router.patch("/courses/{course_id}", response_model=CourseSummary)
async def update_course(
    course_id: uuid.UUID, payload: CourseUpdate, db: DbSession, _: AdminUser
) -> CourseSummary:
    course = await course_service.update_course(db, course_id, payload)
    return CourseSummary.model_validate(course)


@router.delete("/courses/{course_id}", response_model=MessageResponse)
async def delete_course(course_id: uuid.UUID, db: DbSession, _: AdminUser) -> MessageResponse:
    await course_service.delete_course(db, course_id)
    return MessageResponse(message="Сургалт устгагдлаа.")


@router.get("/admin/courses/{course_id}", response_model=CourseDetail, tags=["admin"])
async def admin_course_detail(course_id: uuid.UUID, db: DbSession, _: AdminUser) -> CourseDetail:
    """Админ засварын дэлгэцэд нийтлэгдээгүй module/lesson-ууд ч хэрэгтэй."""
    return await course_service.admin_course_detail(db, course_id)


@router.post(
    "/courses/{course_id}/modules",
    response_model=ModuleWithLessons,
    status_code=status.HTTP_201_CREATED,
)
async def create_module(
    course_id: uuid.UUID, payload: ModuleCreate, db: DbSession, _: AdminUser
) -> ModuleWithLessons:
    module = await module_service.create_module(db, course_id, payload)
    return ModuleWithLessons(
        id=module.id,
        title=module.title,
        description=module.description,
        position=module.position,
        lessons=[],
    )
