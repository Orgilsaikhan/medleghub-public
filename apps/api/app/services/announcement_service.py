"""Админы зарлал — сайт дээр цонх болж гарна.

Хэрэглэгч бүрд тохирох зарлалыг (нийтэлсэн, хугацаандаа, хүрээнд нь багтсан)
шинэ нь эхэнд буцаана. Аль нь харагдахыг, хаасныг хөтөч шийдэж санана —
сервер хэн юу харсныг хадгалахгүй.
"""

import logging
import uuid
from datetime import UTC, datetime

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import BadRequestError, NotFoundError
from app.models.announcement import Announcement
from app.models.enums import AnnouncementAudience, AnnouncementKind
from app.models.user import User
from app.schemas.announcement import (
    AnnouncementCreate,
    AnnouncementItem,
    AnnouncementPublic,
    AnnouncementStatus,
    AnnouncementUpdate,
)

logger = logging.getLogger(__name__)

# Нэг удаад илгээх дээд тоо — хөтөч сесс бүрд нэгийг л харуулна.
CURRENT_LIMIT = 5


def _audiences(user: User | None) -> list[str]:
    if user is None:
        return [AnnouncementAudience.EVERYONE]
    plan = AnnouncementAudience.STANDARD if user.has_plan else AnnouncementAudience.FREE
    return [AnnouncementAudience.EVERYONE, AnnouncementAudience.SIGNED_IN, plan]


def _public(item: Announcement) -> AnnouncementPublic:
    return AnnouncementPublic(
        id=item.id,
        kind=AnnouncementKind(item.kind),
        title=item.title,
        body=item.body,
        cta_label=item.cta_label,
        cta_url=item.cta_url,
    )


async def current_for(db: AsyncSession, user: User | None) -> list[AnnouncementPublic]:
    """Одоо энэ хэрэглэгчид харагдах зарлалууд, шинэ нь эхэнд."""
    now = func.now()
    rows = (
        (
            await db.execute(
                select(Announcement)
                .where(
                    Announcement.active.is_(True),
                    or_(Announcement.starts_at.is_(None), Announcement.starts_at <= now),
                    or_(Announcement.ends_at.is_(None), Announcement.ends_at > now),
                    Announcement.audience.in_(_audiences(user)),
                )
                .order_by(
                    func.coalesce(Announcement.starts_at, Announcement.created_at).desc(),
                    Announcement.created_at.desc(),
                )
                .limit(CURRENT_LIMIT)
            )
        )
        .scalars()
        .all()
    )
    return [_public(item) for item in rows]


def _status(item: Announcement, now: datetime) -> AnnouncementStatus:
    if not item.active:
        return "draft"
    if item.ends_at is not None and item.ends_at <= now:
        return "ended"
    if item.starts_at is not None and item.starts_at > now:
        return "scheduled"
    return "live"


def _item(item: Announcement, created_by: str | None, now: datetime) -> AnnouncementItem:
    return AnnouncementItem(
        **_public(item).model_dump(),
        audience=AnnouncementAudience(item.audience),
        starts_at=item.starts_at,
        ends_at=item.ends_at,
        active=item.active,
        status=_status(item, now),
        created_at=item.created_at,
        updated_at=item.updated_at,
        created_by=created_by,
    )


def _listing():
    return select(Announcement, User.name).outerjoin(User, User.id == Announcement.created_by)


async def list_all(db: AsyncSession) -> list[AnnouncementItem]:
    """Админд: бүгд, шинэ нь эхэнд."""
    now = datetime.now(UTC)
    rows = (await db.execute(_listing().order_by(Announcement.created_at.desc()))).all()
    return [_item(item, name, now) for item, name in rows]


async def _get_item(db: AsyncSession, announcement_id: uuid.UUID) -> AnnouncementItem:
    row = (await db.execute(_listing().where(Announcement.id == announcement_id))).one_or_none()
    if row is None:
        raise _not_found()
    item, name = row
    return _item(item, name, datetime.now(UTC))


def _not_found() -> NotFoundError:
    return NotFoundError("ANNOUNCEMENT_NOT_FOUND", "Зарлал олдсонгүй.")


async def create(db: AsyncSession, admin: User, payload: AnnouncementCreate) -> AnnouncementItem:
    item = Announcement(**payload.model_dump(), created_by=admin.id)
    db.add(item)
    await db.commit()
    logger.info("Админ %s зарлал %s үүсгэлээ", admin.id, item.id)
    return await _get_item(db, item.id)


async def update(
    db: AsyncSession, announcement_id: uuid.UUID, payload: AnnouncementUpdate
) -> AnnouncementItem:
    item = await db.get(Announcement, announcement_id)
    if item is None:
        raise _not_found()
    for field in payload.model_fields_set:
        setattr(item, field, getattr(payload, field))
    # Өөрчилсний дараах бүтэн утгаар шалгана — нэг талбарыг л ирүүлсэн ч.
    if (item.cta_label is None) != (item.cta_url is None):
        await db.rollback()
        raise BadRequestError(
            "ANNOUNCEMENT_CTA_INCOMPLETE", "Товчны бичвэр, холбоосыг хамт оруулна уу."
        )
    if item.starts_at and item.ends_at and item.ends_at <= item.starts_at:
        await db.rollback()
        raise BadRequestError(
            "ANNOUNCEMENT_PERIOD_INVALID", "Дуусах өдөр эхлэх өдрөөс хойш байх ёстой."
        )
    await db.commit()
    return await _get_item(db, announcement_id)


async def delete(db: AsyncSession, announcement_id: uuid.UUID) -> None:
    item = await db.get(Announcement, announcement_id)
    if item is None:
        raise _not_found()
    await db.delete(item)
    await db.commit()
