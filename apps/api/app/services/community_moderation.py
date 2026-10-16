"""Community-ийн дүрэм ба түдгэлзүүлэлт.

Хэрэглэгч эхний удаа Community-д ороход дүрмийг зөвшөөрнө. Зөвшөөрөөгүй эсвэл
түдгэлзсэн бол зөвхөн уншина: нийтлэл, сэтгэгдэл бичих, лайк дарах, мэдэгдэх
боломжгүй. Өөрийн бичсэнийг устгах нь хэзээд боломжтой.

Түдгэлзүүлэх хугацаа удаа ахих тусам уртасна (`community_suspension_days`,
анхдагчаар 7 → 14 → 30 хоног), дараагийн зөрчил бүрмөсөн. Админ цуцалсан
түдгэлзүүлэлт (алдаатай шийдвэр) дараагийн удааг тоолоход орохгүй.
"""

import uuid
from datetime import UTC, datetime, timedelta

from sqlalchemy import ColumnElement, and_, func, not_, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.config import settings
from app.core.errors import BadRequestError, ConflictError, ForbiddenError, NotFoundError
from app.models.community_post import CommunitySuspension
from app.models.user import User
from app.schemas.community_post import (
    CommunityStatus,
    SuspensionAdmin,
    SuspensionCreate,
    SuspensionInfo,
    SuspensionItem,
    SuspensionUser,
)

DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100


def _is_active() -> ColumnElement[bool]:
    return and_(
        CommunitySuspension.lifted_at.is_(None),
        or_(CommunitySuspension.ends_at.is_(None), CommunitySuspension.ends_at > func.now()),
    )


def _still_active(suspension: CommunitySuspension, now: datetime) -> bool:
    return suspension.lifted_at is None and (suspension.ends_at is None or suspension.ends_at > now)


async def active_suspension(db: AsyncSession, user_id: uuid.UUID) -> CommunitySuspension | None:
    return (
        await db.execute(
            select(CommunitySuspension)
            .where(CommunitySuspension.user_id == user_id, _is_active())
            .order_by(CommunitySuspension.created_at.desc())
            .limit(1)
        )
    ).scalar_one_or_none()


async def ensure_can_participate(db: AsyncSession, user: User) -> None:
    """Бичих, лайк дарах, мэдэгдэхийн өмнө шалгана."""
    if user.community_guidelines_accepted_at is None:
        raise ForbiddenError(
            "COMMUNITY_GUIDELINES_REQUIRED", "Эхлээд Community-ийн дүрмийг уншиж, зөвшөөрнө үү."
        )
    if await active_suspension(db, user.id) is not None:
        raise ForbiddenError(
            "COMMUNITY_SUSPENDED",
            "Дүрэм зөрчсөн тул таны Community-д оролцох эрх түдгэлзсэн байна. "
            "Зөвхөн унших боломжтой.",
        )


async def status(db: AsyncSession, user: User) -> CommunityStatus:
    suspension = await active_suspension(db, user.id)
    return CommunityStatus(
        guidelines_accepted=user.community_guidelines_accepted_at is not None,
        suspension=(
            None
            if suspension is None
            else SuspensionInfo(
                level=suspension.level,
                reason=suspension.reason,
                created_at=suspension.created_at,
                ends_at=suspension.ends_at,
            )
        ),
        suspension_days=settings.community_suspension_days,
    )


async def accept_guidelines(db: AsyncSession, user: User) -> CommunityStatus:
    """Анх зөвшөөрсөн мөчийг хадгална — дахин дуудахад өөрчлөхгүй."""
    if user.community_guidelines_accepted_at is None:
        user.community_guidelines_accepted_at = datetime.now(UTC)
        await db.commit()
    return await status(db, user)


def _item(suspension: CommunitySuspension, now: datetime) -> SuspensionItem:
    admin = suspension.admin
    return SuspensionItem(
        id=suspension.id,
        user=SuspensionUser.model_validate(suspension.user),
        admin=None if admin is None else SuspensionAdmin.model_validate(admin),
        level=suspension.level,
        reason=suspension.reason,
        created_at=suspension.created_at,
        ends_at=suspension.ends_at,
        lifted_at=suspension.lifted_at,
        active=_still_active(suspension, now),
    )


async def _load(db: AsyncSession, suspension_id: uuid.UUID) -> CommunitySuspension:
    suspension = (
        await db.execute(
            select(CommunitySuspension)
            .where(CommunitySuspension.id == suspension_id)
            .options(
                selectinload(CommunitySuspension.user),
                selectinload(CommunitySuspension.admin),
            )
            .execution_options(populate_existing=True)
        )
    ).scalar_one_or_none()
    if suspension is None:
        raise NotFoundError("SUSPENSION_NOT_FOUND", "Түдгэлзүүлэлт олдсонгүй.")
    return suspension


async def suspend(db: AsyncSession, admin: User, payload: SuspensionCreate) -> SuspensionItem:
    """Дараагийн шатны хугацаагаар түдгэлзүүлнэ. Жагсаалт дууссан бол бүрмөсөн."""
    user = await db.get(User, payload.user_id)
    if user is None:
        raise NotFoundError("USER_NOT_FOUND", "Хэрэглэгч олдсонгүй.")
    if user.is_admin:
        raise BadRequestError("CANNOT_SUSPEND_ADMIN", "Админыг түдгэлзүүлэх боломжгүй.")
    if await active_suspension(db, user.id) is not None:
        raise ConflictError("ALREADY_SUSPENDED", "Энэ хэрэглэгч аль хэдийн түдгэлзсэн байна.")

    previous = (
        await db.execute(
            select(func.count())
            .select_from(CommunitySuspension)
            .where(
                CommunitySuspension.user_id == user.id,
                CommunitySuspension.lifted_at.is_(None),
            )
        )
    ).scalar_one()
    level = previous + 1
    days = settings.community_suspension_days
    ends_at = datetime.now(UTC) + timedelta(days=days[level - 1]) if level <= len(days) else None

    suspension = CommunitySuspension(
        user_id=user.id, admin_id=admin.id, level=level, reason=payload.reason, ends_at=ends_at
    )
    db.add(suspension)
    await db.commit()
    return _item(await _load(db, suspension.id), datetime.now(UTC))


async def lift(db: AsyncSession, suspension_id: uuid.UUID) -> SuspensionItem:
    """Идэвхтэй түдгэлзүүлэлтийг цуцална. Дараагийн удааг тоолоход орохгүй болно."""
    suspension = await _load(db, suspension_id)
    now = datetime.now(UTC)
    if not _still_active(suspension, now):
        raise ConflictError("SUSPENSION_NOT_ACTIVE", "Энэ түдгэлзүүлэлт аль хэдийн дууссан байна.")
    suspension.lifted_at = now
    await db.commit()
    return _item(suspension, now)


async def list_suspensions(
    db: AsyncSession, *, active: bool | None, page: int, page_size: int
) -> tuple[list[SuspensionItem], int]:
    """Шинэ нь эхэндээ. `active=None` бол бүгд."""
    stmt = select(CommunitySuspension)
    if active is not None:
        stmt = stmt.where(_is_active() if active else not_(_is_active()))

    total = (await db.execute(select(func.count()).select_from(stmt.subquery()))).scalar_one()
    rows = await db.execute(
        stmt.options(
            selectinload(CommunitySuspension.user), selectinload(CommunitySuspension.admin)
        )
        .order_by(CommunitySuspension.created_at.desc(), CommunitySuspension.id)
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    now = datetime.now(UTC)
    return [_item(suspension, now) for suspension in rows.scalars().all()], total
