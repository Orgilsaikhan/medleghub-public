"""Санал хүсэлт — хэрэглэгч илгээж, админ уншина."""

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from app.core import rate_limit
from app.core.config import settings
from app.core.deps import AdminUser, CurrentUser, DbSession
from app.core.errors import RateLimitError
from app.schemas.common import MessageResponse, Page
from app.schemas.feedback import FeedbackCreate, FeedbackItem, FeedbackUpdate
from app.services import feedback_service

router = APIRouter(tags=["feedback"])


async def limit_feedback(user: CurrentUser) -> None:
    """Хэрэглэгч тус бүрд — админы жагсаалтыг спамаар дүүргэхгүй."""
    if not settings.rate_limit_enabled:
        return
    allowed, retry_after = rate_limit.backend.hit(
        f"feedback:{user.id}",
        settings.feedback_rate_limit_max,
        settings.feedback_rate_limit_window_seconds,
    )
    if not allowed:
        raise RateLimitError(retry_after)


@router.post(
    "/feedback",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(limit_feedback)],
)
async def send_feedback(
    payload: FeedbackCreate, db: DbSession, user: CurrentUser
) -> MessageResponse:
    await feedback_service.create(db, user, payload)
    return MessageResponse(message="Баярлалаа! Таны санал хүсэлтийг хүлээн авлаа.")


@router.get("/admin/feedback", response_model=Page[FeedbackItem], tags=["admin"])
async def list_feedback(
    db: DbSession,
    _: AdminUser,
    resolved: bool | None = None,
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=feedback_service.MAX_PAGE_SIZE)] = (
        feedback_service.DEFAULT_PAGE_SIZE
    ),
) -> Page[FeedbackItem]:
    items, total = await feedback_service.list_feedback(
        db, resolved=resolved, page=page, page_size=page_size
    )
    return Page[FeedbackItem](
        items=[FeedbackItem.model_validate(item) for item in items],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=max(1, -(-total // page_size)),
    )


@router.patch("/admin/feedback/{feedback_id}", response_model=FeedbackItem, tags=["admin"])
async def update_feedback(
    feedback_id: uuid.UUID, payload: FeedbackUpdate, db: DbSession, _: AdminUser
) -> FeedbackItem:
    feedback = await feedback_service.set_resolved(db, feedback_id, payload.resolved)
    return FeedbackItem.model_validate(feedback)
