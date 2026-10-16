"""Хэн Live ашиглах вэ, ямар хязгаартай вэ.

- `LIVE_ACCESS`: `off` — бүх зам 404; `admins` — зөвхөн админ; `all` — нэвтэрсэн бүгд.
- Эрх: `standard` — идэвхтэй Standard багц (Live багтсан); `premium` —
  `live_subscriptions`-ийн идэвхтэй мөр (Standard дээр илүү AI); админ үргэлж
  `premium`. `free` (багцгүй) хэрэглэгчид Live огт нээлттэй биш (эзэн 2026-10-01):
  `/live/config`-оос бусад бүх зам 402 `LIVE_PLAN_REQUIRED`. Багц дуусахад
  материалууд устахгүй — дахин багц авбал буцаж харагдана.
- `pass` — багцгүй ч нэг удаагийн эрхтэй (`live_passes`, эзэн 2026-10-03):
  ашиглаагүй эрхээр нэг материал оруулна; зөвхөн эрхээр нээсэн материалаа
  `live_pass_access_days` хоног хардаг. AI-ийн хязгаар нь сарынх биш —
  материал тус бүрийн бүх ажлын нийлбэр (`live_pass_ai_usd`).
- Материалын тоог хэрэглэгчид харуулахгүй.
- AI зардлын сарын хязгаар бүх боломжийн нийлбэрт үйлчилнэ. Тоолол нь
  `ai_requests`-ээс (материал устгасан ч үлдэнэ) — дахин оролдлого ч тоологдоно.
- Сар нь Улаанбаатарын цагаар 1-ний 00:00-аас.
"""

import uuid
from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta, timezone
from decimal import Decimal
from typing import Annotated

from fastapi import Depends, status
from sqlalchemy import and_, func, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.core.config import settings
from app.core.deps import CurrentUser, DbSession
from app.live.errors import live_error, not_found
from app.models.ai_request import AIRequest
from app.models.enums import LiveMaterialStatus, LiveTier
from app.models.live import LiveMaterial, LivePass, LiveSubscription
from app.models.user import User
from app.services.ai.capabilities import Capability
from app.services.ai.errors import AIBudgetError

ULAANBAATAR = timezone(timedelta(hours=8))
# Платформын төсвийн энэ хувьд хүрвэл шинэ AI ажил эхлэхгүй.
PLATFORM_PAUSE_RATIO = Decimal("0.95")


def live_enabled_for(user: User | None) -> bool:
    if user is None:
        return False
    if settings.live_access == "all":
        return True
    return settings.live_access == "admins" and user.is_admin


async def get_live_user(user: CurrentUser, db: DbSession) -> User:
    """Live хаалттай бол замууд байхгүй мэт 404 — боломж байгааг задруулахгүй.
    Нээлттэй ч багцгүй бол 402 — Live нь зөвхөн Standard, Premium-д."""
    if not live_enabled_for(user):
        raise not_found()
    if (await entitlement_for(db, user)).tier == LiveTier.FREE:
        raise live_error(status.HTTP_402_PAYMENT_REQUIRED, "LIVE_PLAN_REQUIRED")
    return user


LiveUser = Annotated[User, Depends(get_live_user)]


def month_start(now: datetime | None = None) -> datetime:
    local = (now or datetime.now(UTC)).astimezone(ULAANBAATAR)
    return local.replace(day=1, hour=0, minute=0, second=0, microsecond=0)


def next_month_start(now: datetime | None = None) -> datetime:
    start = month_start(now)
    return (start + timedelta(days=32)).replace(day=1)


@dataclass(frozen=True)
class Entitlement:
    tier: LiveTier
    expires_at: datetime | None
    # `None` — тоогоор хязгааргүй.
    documents_limit: int | None
    # `pass`-д сарынх биш — материал тус бүрийн AI хязгаар.
    ai_monthly_usd: Decimal
    # `pass`: эрхээр нээсэн материал → эрх дуусах мөч; ашиглаагүй эрх (байвал).
    pass_materials: Mapping[uuid.UUID, datetime] = field(default_factory=dict)
    unused_pass_id: uuid.UUID | None = None

    def can_open(self, material_id: uuid.UUID) -> bool:
        """Багцтай бол өөрийн бүх материал; эрхээр бол зөвхөн эрхээр нээсэн нь."""
        return self.tier != LiveTier.PASS or material_id in self.pass_materials


def _limits(tier: LiveTier, expires_at: datetime | None) -> Entitlement:
    if tier == LiveTier.PREMIUM:
        return Entitlement(
            tier,
            expires_at,
            settings.live_premium_documents_per_month,
            Decimal(str(settings.live_premium_ai_monthly_usd)),
        )
    if tier == LiveTier.STANDARD:
        return Entitlement(
            tier,
            expires_at,
            settings.live_standard_documents_per_month,
            Decimal(str(settings.live_standard_ai_monthly_usd)),
        )
    # Багцгүй хэрэглэгч Live-ийг ашиглахгүй (`get_live_user`) — хязгаар нь тэг.
    return Entitlement(LiveTier.FREE, None, 0, Decimal(0))


async def entitlement_for(db: AsyncSession, user: User) -> Entitlement:
    if user.is_admin:
        return _limits(LiveTier.PREMIUM, None)
    subscription = await db.get(LiveSubscription, user.id)
    if subscription is not None and subscription.expires_at > datetime.now(UTC):
        return _limits(LiveTier.PREMIUM, subscription.expires_at)
    if user.has_plan:
        return _limits(LiveTier.STANDARD, user.plan_expires_at)
    return await _pass_entitlement(db, user)


def unused_pass_condition(user_id: uuid.UUID):
    """Ашиглаагүй, багц руу шилжээгүй эрх — хугацаагүй."""
    return and_(
        LivePass.user_id == user_id,
        LivePass.used_at.is_(None),
        LivePass.upgraded_at.is_(None),
    )


async def _pass_entitlement(db: AsyncSession, user: User) -> Entitlement:
    now = datetime.now(UTC)
    passes = (
        (
            await db.execute(
                select(LivePass)
                .where(
                    or_(
                        unused_pass_condition(user.id),
                        and_(LivePass.user_id == user.id, LivePass.expires_at > now),
                    )
                )
                .order_by(LivePass.created_at)
            )
        )
        .scalars()
        .all()
    )
    opened = {
        item.material_id: item.expires_at
        for item in passes
        if item.material_id is not None and item.expires_at is not None
    }
    unused = next((item.id for item in passes if item.used_at is None), None)
    if not opened and unused is None:
        return _limits(LiveTier.FREE, None)
    return Entitlement(
        LiveTier.PASS,
        max(opened.values(), default=None),
        1 if unused is not None else 0,
        Decimal(str(settings.live_pass_ai_usd)),
        pass_materials=opened,
        unused_pass_id=unused,
    )


async def use_pass(
    db: AsyncSession, entitlement: Entitlement, material_id: uuid.UUID
) -> datetime | None:
    """Ашиглаагүй эрхийг материалд холбоно — эрх дуусах мөч, эсвэл (зэрэг хүсэлт
    аль хэдийн ашигласан бол) `None`. Commit-ийг дуудагч хийнэ."""
    if entitlement.unused_pass_id is None:
        return None
    now = func.now()
    return (
        await db.execute(
            update(LivePass)
            .where(
                LivePass.id == entitlement.unused_pass_id,
                LivePass.used_at.is_(None),
                LivePass.upgraded_at.is_(None),
            )
            .values(
                material_id=material_id,
                used_at=now,
                expires_at=now + timedelta(days=settings.live_pass_access_days),
            )
            .returning(LivePass.expires_at)
        )
    ).scalar_one_or_none()


async def release_pass(db: AsyncSession, material: LiveMaterial) -> None:
    """Бэлэн болоогүй материалыг устгахад эрхийг буцаана — материалыг судлаагүй тул.
    Commit-ийг дуудагч хийнэ."""
    if material.status == LiveMaterialStatus.READY:
        return
    await db.execute(
        update(LivePass)
        .where(LivePass.material_id == material.id)
        .values(material_id=None, used_at=None, expires_at=None)
    )


async def documents_used(db: AsyncSession, user_id: uuid.UUID) -> int:
    """Энэ сард амжилттай задалсан материал + одоо дараалалд байгаа нь.

    Материал устгасан ч `ai_requests` үлддэг тул устгаж дахин оруулаад сарын
    хязгаараа сэргээх боломжгүй.
    """
    succeeded = select(func.count()).where(
        AIRequest.user_id == user_id,
        AIRequest.capability == Capability.DOCUMENT.value,
        AIRequest.success.is_(True),
    )
    succeeded = succeeded.where(AIRequest.created_at >= month_start())
    in_flight = select(func.count()).where(
        LiveMaterial.owner_id == user_id,
        LiveMaterial.status.in_([LiveMaterialStatus.QUEUED, LiveMaterialStatus.PROCESSING]),
    )
    return int((await db.execute(succeeded)).scalar_one()) + int(
        (await db.execute(in_flight)).scalar_one()
    )


async def material_spent_usd(db: AsyncSession, material_id: uuid.UUID) -> Decimal:
    """Нэг материалын бүх хугацааны AI зардал — нэг удаагийн эрхийн хязгаар."""
    query = select(func.coalesce(func.sum(AIRequest.estimated_cost_usd), 0)).where(
        AIRequest.material_id == material_id
    )
    return Decimal((await db.execute(query)).scalar_one())


async def ai_spent_usd(db: AsyncSession, user_id: uuid.UUID | None = None) -> Decimal:
    """Энэ сарын AI зардал: хэрэглэгчийнх эсвэл (`None`) платформынх."""
    query = select(func.coalesce(func.sum(AIRequest.estimated_cost_usd), 0)).where(
        AIRequest.created_at >= month_start()
    )
    if user_id is not None:
        query = query.where(AIRequest.user_id == user_id)
    return Decimal((await db.execute(query)).scalar_one())


def platform_budget_usd() -> Decimal:
    return Decimal(str(settings.ai_platform_monthly_budget_usd))


async def assert_can_add_document(
    db: AsyncSession, user: User, entitlement: Entitlement, material: LiveMaterial | None = None
) -> None:
    """Шинэ материал боловсруулах эрх. 402 — сарын хязгаар, эсвэл эрх ашиглагдсан.

    `material` — аль хэдийн бүртгэсэн материал (файл илгээх, дахин оролдох): эрхээр
    бол тэр материалд холбогдсон байхад хангалттай."""
    if entitlement.tier == LiveTier.PASS:
        if material is not None and entitlement.can_open(material.id):
            return
        if material is None and entitlement.unused_pass_id is not None:
            return
        raise live_error(status.HTTP_402_PAYMENT_REQUIRED, "LIVE_PASS_USED")
    if entitlement.documents_limit is None:
        return
    if await documents_used(db, user.id) < entitlement.documents_limit:
        return
    raise live_error(status.HTTP_402_PAYMENT_REQUIRED, "LIVE_DOCUMENT_LIMIT")


async def budget_error(
    db: AsyncSession,
    user: User,
    entitlement: Entitlement,
    estimate: Decimal = Decimal(0),
    material_id: uuid.UUID | None = None,
) -> str | None:
    """`platform_budget` / `user_budget` / `pass_budget` / `None` — AI ажил эхлүүлж
    болох эсэх. Эрхээр бол `material_id`-ийн зардлыг тоолно (`None` — материал
    хараахан үүсээгүй, зардалгүй)."""
    if await ai_spent_usd(db) >= platform_budget_usd() * PLATFORM_PAUSE_RATIO:
        return "platform_budget"
    cap = entitlement.ai_monthly_usd
    if entitlement.tier == LiveTier.PASS:
        if material_id is None:
            return None
        if not entitlement.can_open(material_id):
            return "pass_budget"
        spent = await material_spent_usd(db, material_id)
        return "pass_budget" if spent >= cap or spent + estimate > cap else None
    spent = await ai_spent_usd(db, user.id)
    if spent >= cap or spent + estimate > cap:
        return "user_budget"
    return None


async def assert_ai_available(
    db: AsyncSession, user: User, entitlement: Entitlement, material_id: uuid.UUID | None = None
) -> None:
    """HTTP замд: AI ажил захиалахын өмнө. 503 — платформ; 402 — хэрэглэгчийн хязгаар."""
    error = await budget_error(db, user, entitlement, material_id=material_id)
    if error == "platform_budget":
        raise live_error(status.HTTP_503_SERVICE_UNAVAILABLE, "LIVE_AI_PAUSED")
    if error == "user_budget":
        raise live_error(status.HTTP_402_PAYMENT_REQUIRED, "LIVE_QUOTA_EXCEEDED")
    if error == "pass_budget":
        raise live_error(status.HTTP_402_PAYMENT_REQUIRED, "LIVE_PASS_QUOTA_EXCEEDED")


def budget_check(
    sessions: async_sessionmaker[AsyncSession], user_id: uuid.UUID, material_id: uuid.UUID
):
    """`AIService`-д: AI дуудлага бүрийн өмнө хамгийн их зардлаар нь шалгана."""

    async def check(worst_case: Decimal) -> None:
        async with sessions() as db:
            user = await db.get(User, user_id)
            if user is None:
                raise AIBudgetError("user_budget", "user deleted")
            entitlement = await entitlement_for(db, user)
            error = await budget_error(db, user, entitlement, worst_case, material_id)
        if error is not None:
            raise AIBudgetError(error)

    return check
