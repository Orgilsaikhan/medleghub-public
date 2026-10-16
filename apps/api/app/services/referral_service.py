"""Найзаа урих хөтөлбөр.

Хэрэглэгч бүр урилгын кодтой (`users.referral_code` — бүртгүүлэхэд үүснэ,
хэрэглэгчийн цэс ба профайлд харагдана). Шинэ хэрэглэгч бүртгүүлэхдээ кодыг
оруулбал (`/register?ref=…`) `referrals` мөр үүснэ.

- Шинэ хэрэглэгч (найз) нэг удаагийн хөнгөлөлт авна — промо код оруулаагүй
  төлбөрт checkout автоматаар хэрэглэнэ. Урьсан хүн хөнгөлөлт авахгүй.
- Найз анх амжилттай төлөхөд `billing_service` түүнийг «багц авсан найз»
  болгож, тогтсон тоо хүрэх бүрд урьсан хүний багцыг сунгана.
"""

import uuid
from datetime import UTC, datetime

from sqlalchemy import func, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.errors import AppError
from app.models.referral import Referral
from app.models.user import User
from app.schemas.promo import ReferralSummary, normalize_code
from app.services.promo_service import random_code


async def ensure_code(db: AsyncSession, user: User) -> str:
    """Урилгын кодыг буцаана — байхгүй бол үүсгэж хадгална."""
    if user.referral_code:
        return user.referral_code
    # Rollback нь `user`-ийг expire хийдэг — id-г урьдчилан авна.
    user_id = user.id
    for _ in range(5):
        try:
            # Зэрэг ирсэн хүсэлт аль хэдийн тавьсан бол юу ч өөрчлөхгүй.
            await db.execute(
                update(User)
                .where(User.id == user_id, User.referral_code.is_(None))
                .values(referral_code=random_code())
            )
            await db.commit()
        except IntegrityError:
            # Өөр хэрэглэгчийн кодтой давхцсан — дахин санамсаргүй.
            await db.rollback()
            continue
        await db.refresh(user)
        if user.referral_code:
            return user.referral_code
    raise AppError(500, "REFERRAL_CODE_FAILED", "Урилгын код үүсгэж чадсангүй. Дахин оролдоно уу.")


async def find_referrer(db: AsyncSession, raw_code: str) -> User | None:
    code = normalize_code(raw_code)
    if not code:
        return None
    return (await db.execute(select(User).where(User.referral_code == code))).scalar_one_or_none()


async def confirm_signup(db: AsyncSession, friend_id: uuid.UUID) -> None:
    """Найз имэйлээ баталгаажуулсан — урьсан хүний «Урьсан найз» тоонд орно.

    Нэг л удаа. Commit-ийг дуудагч хийнэ.
    """
    await db.execute(
        update(Referral)
        .where(Referral.friend_id == friend_id, Referral.signup_confirmed_at.is_(None))
        .values(signup_confirmed_at=datetime.now(UTC))
    )


async def available_discount(db: AsyncSession, friend_id: uuid.UUID) -> Referral | None:
    """Энэ хэрэглэгчийн урилгаар авсан, ашиглаагүй хөнгөлөлт (урилгатай бүртгүүлсэн бол)."""
    return (
        await db.execute(
            select(Referral).where(
                Referral.friend_id == friend_id, Referral.discount_used_at.is_(None)
            )
        )
    ).scalar_one_or_none()


async def summary(db: AsyncSession, user: User) -> ReferralSummary:
    code = await ensure_code(db, user)
    friends, paying, months_earned = (
        await db.execute(
            select(
                func.count(Referral.signup_confirmed_at),
                func.count(Referral.first_paid_at),
                func.coalesce(func.sum(Referral.months_rewarded), 0),
            ).where(Referral.referrer_id == user.id)
        )
    ).one()
    per_reward = settings.referral_friends_per_reward
    return ReferralSummary(
        code=code,
        friend_percent_off=settings.referral_friend_percent_off,
        friends_per_reward=per_reward,
        reward_months=settings.referral_reward_months,
        friends=friends,
        paying_friends=paying,
        friends_to_next_reward=per_reward - paying % per_reward,
        months_earned=months_earned,
    )
