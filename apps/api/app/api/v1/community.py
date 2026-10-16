"""Бусад суралцагчийг харах — сургалтын суралцагчид ба нийтийн профайл."""

import uuid
from typing import Annotated

from fastapi import APIRouter, Query

from app.core.deps import CurrentUser, DbSession
from app.schemas.community import CourseStudents, PublicProfileResponse
from app.services import community_service

router = APIRouter(tags=["community"])


@router.get("/courses/{slug}/students", response_model=CourseStudents)
async def course_students(
    slug: str,
    db: DbSession,
    user: CurrentUser,
    limit: Annotated[int, Query(ge=1, le=community_service.MAX_STUDENTS)] = 24,
) -> CourseStudents:
    return await community_service.course_students(db, slug, user, limit)


@router.get("/users/{user_id}/profile", response_model=PublicProfileResponse)
async def public_profile(
    user_id: uuid.UUID, db: DbSession, user: CurrentUser
) -> PublicProfileResponse:
    """Өөр хэрэглэгчийн профайл — нэр, зураг, статистик, тэмдэг, сургалтын ахиц.

    Профайлаа нуусан бол 403 (өөрөө л харна).
    """
    return await community_service.public_profile(db, user_id, user)
