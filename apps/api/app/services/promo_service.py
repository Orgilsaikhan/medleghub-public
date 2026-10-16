"""Промо код — админ үүсгэнэ, хэрэглэгч ашиглана.

- Хувийн код (`percent`): checkout дээр оруулна. Төлбөр амжилттай болох үед
  `promo_redemptions`-д бичигдэнэ (`billing_service.apply_payment`). Төлөөгүй
  нэхэмжлэх кодыг «ашигласан» болгохгүй. Иймээс зэрэг нээсэн хэд хэдэн
  нэхэмжлэхийг бүгдийг нь төлбөл `max_uses` бага зэрэг хэтэрч болно.
- Үнэгүй сарын код (`free_months`): `POST /billing/promo/redeem`-ээр шууд
  идэвхжинэ. Кодын мөрийг түгжиж тоолдог тул `max_uses` хэтрэхгүй.

Хэрэглэгч нэг кодыг нэг л удаа ашиглана.
"""

import logging
import secrets
import uuid
from datetime import UTC, datetime

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import AppError, BadRequestError, ConflictError, NotFoundError
from app.models.enums import PromoKind
from app.models.promo_code import PromoCode, PromoRedemption
from app.models.user import User
from app.schemas.promo import (
    PromoCodeCreate,
    PromoCodeItem,
    PromoCodeUpdate,
    PromoStatus,
    normalize_code,
)

logger = logging.getLogger(__name__)

# 0/O, 1/I-г андуурахгүйн тулд хассан. Урилгын код ч үүнийг ашиглана.
CODE_ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
GENERATED_CODE_LENGTH = 8


def random_code(length: int = GENERATED_CODE_LENGTH) -> str:
    return "".join(secrets.choice(CODE_ALPHABET) for _ in range(length))


# --- Алдаа --------------------------------------------------------------------


def invalid_code() -> BadRequestError:
    # Байхгүй, идэвхгүй кодыг ялгахгүй — идэвхгүй болгосон код байсныг ил гаргахгүй.
    return BadRequestError("PROMO_INVALID", "Промо код буруу байна.")


def free_months_code() -> BadRequestError:
    return BadRequestError(
        "PROMO_FREE_MONTHS", "Энэ код үнэгүй сар олгоно — «Идэвхжүүлэх» товчийг дарна уу."
    )


def not_redeemable() -> BadRequestError:
    return BadRequestError(
        "PROMO_NOT_REDEEMABLE", "Энэ код хөнгөлөлтийн код — төлбөр төлөхдөө ашиглана."
    )


def already_used() -> ConflictError:
    return ConflictError("PROMO_ALREADY_USED", "Та энэ промо кодыг аль хэдийн ашигласан.")


# --- Хэрэглэгч ----------------------------------------------------------------


def _expired(code: PromoCode, now: datetime) -> bool:
    return code.expires_at is not None and code.expires_at <= now


async def _uses(db: AsyncSession, code_id: uuid.UUID) -> int:
    return (
        await db.execute(
            select(func.count())
            .select_from(PromoRedemption)
            .where(PromoRedemption.promo_code_id == code_id)
        )
    ).scalar_one()


async def find_usable(
    db: AsyncSession, user: User, raw_code: str, *, lock: bool = False
) -> PromoCode:
    """Хэрэглэгч энэ кодыг одоо ашиглаж болох эсэх. Болохгүй бол шалтгаантай 400/409.

    `lock` — кодын мөрийг транзакцын турш түгжинэ: зэрэг идэвхжүүлэхэд
    `max_uses` хэтрэхгүй. Дуудагч commit эсвэл rollback хийнэ.
    """
    statement = select(PromoCode).where(PromoCode.code == normalize_code(raw_code))
    if lock:
        statement = statement.with_for_update()
    code = (await db.execute(statement)).scalar_one_or_none()
    if code is None or not code.active:
        raise invalid_code()
    if _expired(code, datetime.now(UTC)):
        raise BadRequestError("PROMO_EXPIRED", "Энэ промо кодын хугацаа дууссан.")

    used_by_me = (
        await db.execute(
            select(PromoRedemption.id).where(
                PromoRedemption.promo_code_id == code.id, PromoRedemption.user_id == user.id
            )
        )
    ).first()
    if used_by_me is not None:
        raise already_used()
    if code.max_uses is not None and await _uses(db, code.id) >= code.max_uses:
        raise BadRequestError("PROMO_USED_UP", "Энэ промо кодыг ашиглах боломж дууссан.")
    return code


# --- Админ -------------------------------------------------------------------


def _status(code: PromoCode, uses: int, now: datetime) -> PromoStatus:
    if not code.active:
        return "disabled"
    if _expired(code, now):
        return "expired"
    if code.max_uses is not None and uses >= code.max_uses:
        return "used_up"
    return "active"


def _item(code: PromoCode, uses: int, created_by: str | None, now: datetime) -> PromoCodeItem:
    return PromoCodeItem(
        id=code.id,
        code=code.code,
        kind=PromoKind(code.kind),
        percent_off=code.percent_off,
        free_months=code.free_months,
        expires_at=code.expires_at,
        max_uses=code.max_uses,
        active=code.active,
        note=code.note,
        uses=uses,
        status=_status(code, uses, now),
        created_at=code.created_at,
        created_by=created_by,
    )


def _listing():
    uses = (
        select(func.count())
        .select_from(PromoRedemption)
        .where(PromoRedemption.promo_code_id == PromoCode.id)
        .scalar_subquery()
    )
    return select(PromoCode, uses, User.name).outerjoin(User, User.id == PromoCode.created_by)


async def list_codes(db: AsyncSession) -> list[PromoCodeItem]:
    """Шинэ нь эхэндээ."""
    now = datetime.now(UTC)
    rows = (await db.execute(_listing().order_by(PromoCode.created_at.desc()))).all()
    return [_item(code, uses, name, now) for code, uses, name in rows]


async def _get_item(db: AsyncSession, code_id: uuid.UUID) -> PromoCodeItem:
    row = (await db.execute(_listing().where(PromoCode.id == code_id))).one_or_none()
    if row is None:
        raise NotFoundError("PROMO_NOT_FOUND", "Промо код олдсонгүй.")
    code, uses, name = row
    return _item(code, uses, name, datetime.now(UTC))


async def create_code(db: AsyncSession, admin: User, payload: PromoCodeCreate) -> PromoCodeItem:
    """Код өгөөгүй бол санамсаргүй үүсгэнэ (давхцвал дахин оролдоно)."""
    for _ in range(5):
        code = PromoCode(
            code=payload.code or random_code(),
            kind=payload.kind,
            percent_off=payload.percent_off,
            free_months=payload.free_months,
            expires_at=payload.expires_at,
            max_uses=payload.max_uses,
            note=payload.note,
            created_by=admin.id,
        )
        db.add(code)
        try:
            await db.commit()
        except IntegrityError as exc:
            await db.rollback()
            if payload.code:
                raise ConflictError("PROMO_CODE_TAKEN", "Ийм промо код аль хэдийн бий.") from exc
            continue
        logger.info("Админ %s промо код %s үүсгэлээ", admin.id, code.code)
        return await _get_item(db, code.id)
    raise AppError(500, "PROMO_CODE_GENERATION_FAILED", "Код үүсгэж чадсангүй. Дахин оролдоно уу.")


async def update_code(
    db: AsyncSession, code_id: uuid.UUID, payload: PromoCodeUpdate
) -> PromoCodeItem:
    code = await db.get(PromoCode, code_id)
    if code is None:
        raise NotFoundError("PROMO_NOT_FOUND", "Промо код олдсонгүй.")
    for field in payload.model_fields_set:
        setattr(code, field, getattr(payload, field))
    await db.commit()
    return await _get_item(db, code_id)
