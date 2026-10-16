"""Lesson унших, админ CRUD, lesson player."""

import uuid

from fastapi import APIRouter, status

from app.core.deps import AdminUser, CurrentUser, DbSession
from app.schemas.common import MessageResponse
from app.schemas.learn import LessonPlayerResponse
from app.schemas.lesson import LessonCreate, LessonDetail, LessonHelp, LessonUpdate
from app.services import lesson_service

router = APIRouter(tags=["lessons"])


@router.get("/lessons/{lesson_id}", response_model=LessonDetail)
async def get_lesson(lesson_id: uuid.UUID, db: DbSession, user: CurrentUser) -> LessonDetail:
    return await lesson_service.get_lesson_detail(db, lesson_id, user)


@router.get("/lessons/{lesson_id}/help", response_model=LessonHelp)
async def get_lesson_help(lesson_id: uuid.UUID, db: DbSession, user: CurrentUser) -> LessonHelp:
    """Дасгалын зөвлөгөө ба жишиг шийдэл — «Тусламж» товч."""
    return await lesson_service.get_lesson_help(db, lesson_id, user)


@router.get(
    "/courses/{course_slug}/lessons/{lesson_slug}",
    response_model=LessonPlayerResponse,
)
async def get_lesson_player(
    course_slug: str, lesson_slug: str, db: DbSession, user: CurrentUser
) -> LessonPlayerResponse:
    """Lesson хуудсанд шаардлагатай бүх өгөгдөл — нэг дуудлагаар."""
    return await lesson_service.get_lesson_player(db, course_slug, lesson_slug, user)


@router.post(
    "/modules/{module_id}/lessons",
    response_model=LessonDetail,
    status_code=status.HTTP_201_CREATED,
)
async def create_lesson(
    module_id: uuid.UUID, payload: LessonCreate, db: DbSession, _: AdminUser
) -> LessonDetail:
    lesson = await lesson_service.create_lesson(db, module_id, payload)
    return LessonDetail.model_validate(lesson)


@router.patch("/lessons/{lesson_id}", response_model=LessonDetail)
async def update_lesson(
    lesson_id: uuid.UUID, payload: LessonUpdate, db: DbSession, _: AdminUser
) -> LessonDetail:
    lesson = await lesson_service.update_lesson(db, lesson_id, payload)
    return LessonDetail.model_validate(lesson)


@router.delete("/lessons/{lesson_id}", response_model=MessageResponse)
async def delete_lesson(lesson_id: uuid.UUID, db: DbSession, _: AdminUser) -> MessageResponse:
    await lesson_service.delete_lesson(db, lesson_id)
    return MessageResponse(message="Хичээл устгагдлаа.")
