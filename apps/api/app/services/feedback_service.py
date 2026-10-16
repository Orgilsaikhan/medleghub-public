"""Санал хүсэлт — хэрэглэгч илгээж, админ уншиж шийднэ."""

import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.errors import NotFoundError
from app.models.feedback import Feedback
from app.models.user import User
from app.schemas.feedback import FeedbackCreate

DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100


async def create(db: AsyncSession, user: User, payload: FeedbackCreate) -> Feedback:
    feedback = Feedback(
        user_id=user.id, kind=payload.kind, message=payload.message, page=payload.page
    )
    db.add(feedback)
    await db.commit()
    return feedback


async def list_feedback(
    db: AsyncSession, *, resolved: bool | None, page: int, page_size: int
) -> tuple[list[Feedback], int]:
    """Шинэ нь эхэндээ. `resolved=None` бол бүгд."""
    stmt = select(Feedback)
    if resolved is not None:
        stmt = stmt.where(Feedback.resolved.is_(resolved))

    total = (await db.execute(select(func.count()).select_from(stmt.subquery()))).scalar_one()
    rows = await db.execute(
        stmt.options(selectinload(Feedback.user))
        .order_by(Feedback.created_at.desc(), Feedback.id)
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    return list(rows.scalars().all()), total


async def set_resolved(db: AsyncSession, feedback_id: uuid.UUID, resolved: bool) -> Feedback:
    feedback = (
        await db.execute(
            select(Feedback).where(Feedback.id == feedback_id).options(selectinload(Feedback.user))
        )
    ).scalar_one_or_none()
    if feedback is None:
        raise NotFoundError("FEEDBACK_NOT_FOUND", "Санал хүсэлт олдсонгүй.")
    feedback.resolved = resolved
    await db.commit()
    return feedback
