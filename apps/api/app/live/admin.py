"""Админ: AI зардал, материалын тоо, Live багцыг гараар олгох.

Админ хэрэглэгчдийн материалын агуулгыг харахгүй — зөвхөн нийт тоо, зардал.
"""

from datetime import UTC, datetime

from fastapi import status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.errors import NotFoundError
from app.live import access
from app.live.errors import live_error
from app.models.ai_request import AIRequest
from app.models.enums import LiveMaterialStatus, LiveTier
from app.models.live import LiveMaterial, LiveSubscription
from app.models.plan_adjustment import PlanAdjustment
from app.models.user import User
from app.schemas.live import (
    LiveAdminOverview,
    LiveCapabilitySpend,
    LiveModelLimits,
    LiveModelStatus,
    LiveModelTask,
    LiveSubscriptionGrant,
    LiveSubscriptionInfo,
)
from app.services.ai import prices, router, routing
from app.services.ai.capabilities import Capability
from app.services.ai.routing import ModelRoute


async def overview(db: AsyncSession) -> LiveAdminOverview:
    since = access.month_start()
    rows = (
        await db.execute(
            select(
                AIRequest.capability,
                func.count(),
                func.count().filter(AIRequest.success.is_(False)),
                func.coalesce(func.sum(AIRequest.estimated_cost_usd), 0),
            )
            .where(AIRequest.created_at >= since)
            .group_by(AIRequest.capability)
            .order_by(AIRequest.capability)
        )
    ).all()
    spend = sum(float(row[3]) for row in rows)
    budget = float(access.platform_budget_usd())
    materials_total, materials_failed, owners = (
        await db.execute(
            select(
                func.count(),
                func.count().filter(LiveMaterial.status == LiveMaterialStatus.FAILED),
                func.count(func.distinct(LiveMaterial.owner_id)),
            ).select_from(LiveMaterial)
        )
    ).one()
    return LiveAdminOverview(
        live_access=settings.live_access,
        ai_configured=routing.is_configured(Capability.DOCUMENT),
        month_spend_usd=round(spend, 4),
        budget_usd=budget,
        budget_percent=min(100, round(100 * spend / budget)) if budget else 0,
        by_capability=[
            LiveCapabilitySpend(
                capability=capability,
                requests=int(requests),
                failed=int(failed),
                cost_usd=round(float(cost), 4),
            )
            for capability, requests, failed, cost in rows
        ],
        materials_total=int(materials_total),
        materials_failed=int(materials_failed),
        users_with_materials=int(owners),
    )


async def models_status(db: AsyncSession) -> list[LiveModelStatus]:
    """Ажлын дараалалд байгаа загвар бүр: бэлэн, хөргөгдсөн эсвэл хязгаарт ойртсон.

    Google үлдсэн квотыг хэлдэггүй тул «хязгаарт хүрсэн» нь (1) Google-ийн сүүлийн
    429/503 хариу, (2) `AI_MODEL_LIMITS`-тэй харьцуулсан манай тоолол.
    """
    tasks: dict[str, list[LiveModelTask]] = {}
    for capability in Capability:
        for position, route in enumerate(routing.chain_for(capability), start=1):
            tasks.setdefault(route.key, []).append(
                LiveModelTask(task=capability.value, position=position)
            )
    keys = list(tasks)
    usage = await router.usage_by_model(db, keys)
    key = AIRequest.provider + ":" + AIRequest.model
    month = {
        row[0]: row[1:]
        for row in (
            await db.execute(
                select(
                    key,
                    func.count(),
                    func.count().filter(AIRequest.success.is_(False)),
                    func.coalesce(func.sum(AIRequest.estimated_cost_usd), 0),
                )
                .where(AIRequest.created_at >= access.month_start(), key.in_(keys))
                .group_by(key)
            )
        ).all()
    }
    today = datetime.now(UTC).date()
    result: list[LiveModelStatus] = []
    for model_key in keys:
        route = ModelRoute.parse(model_key)
        health = router.health.get(model_key)
        used = usage.get(model_key, router.ModelUsage())
        limits = settings.ai_model_limits.get(model_key)
        price = prices.price_for(route, today)
        requests, failures, cost = month.get(model_key, (0, 0, 0))
        reason: str | None = None
        if not routing.provider_configured(route.provider):
            status_ = "not_configured"
        elif router.price_missing(route):
            status_ = "no_price"
        elif router.health.remaining(model_key) > 0:
            status_, reason = "cooling", health.reason
        elif near := router.limit_reason(model_key, used, 0):
            status_, reason = "near_limit", near
        else:
            status_ = "ready"
        result.append(
            LiveModelStatus(
                model=model_key,
                tasks=tasks[model_key],
                status=status_,
                reason=reason,
                available_at=health.available_at if status_ == "cooling" else None,
                last_error=health.last_error,
                last_error_at=health.last_error_at,
                minute_requests=used.minute_requests,
                minute_input_tokens=used.minute_input_tokens,
                day_requests=used.day_requests,
                limits=LiveModelLimits(
                    rpm=limits.get("rpm"), tpm=limits.get("tpm"), rpd=limits.get("rpd")
                )
                if limits
                else None,
                month_requests=int(requests),
                month_failures=int(failures),
                month_cost_usd=round(float(cost), 4),
                price_input_usd=float(price.input) if price else None,
                price_output_usd=float(price.output) if price else None,
            )
        )
    return result


async def _user_by_email(db: AsyncSession, email: str) -> User:
    user = (
        await db.execute(select(User).where(func.lower(User.email) == email.strip().lower()))
    ).scalar_one_or_none()
    if user is None:
        raise NotFoundError("USER_NOT_FOUND", "Ийм имэйлтэй хэрэглэгч олдсонгүй.")
    return user


async def _info(db: AsyncSession, user: User) -> LiveSubscriptionInfo:
    entitlement = await access.entitlement_for(db, user)
    return LiveSubscriptionInfo(
        email=user.email,
        name=user.name,
        tier=entitlement.tier,
        expires_at=entitlement.expires_at,
        plan_expires_at=user.plan_expires_at,
    )


async def lookup(db: AsyncSession, email: str) -> LiveSubscriptionInfo:
    return await _info(db, await _user_by_email(db, email))


async def grant(
    db: AsyncSession, admin: User, payload: LiveSubscriptionGrant
) -> LiveSubscriptionInfo:
    """Premium-ийг `months` хуанлийн сараар олгоно (идэвхтэй бол дуусах өдрөөс нь).

    Premium = Standard + илүү AI, тиймээс Standard багц Premium дуусахаас өмнө
    дуусах бол түүнийг Premium-ийн дуусах өдөр хүртэл сунгаж, `plan_adjustments`-д
    бичнэ. Урт Standard багцыг богиносгохгүй.
    """
    user = (
        await db.execute(
            select(User)
            .where(func.lower(User.email) == payload.email.strip().lower())
            .with_for_update()
        )
    ).scalar_one_or_none()
    if user is None:
        raise NotFoundError("USER_NOT_FOUND", "Ийм имэйлтэй хэрэглэгч олдсонгүй.")
    if user.is_admin:
        raise live_error(status.HTTP_409_CONFLICT, "LIVE_ADMIN_ALWAYS_PREMIUM")
    subscription = await db.get(LiveSubscription, user.id)
    current = subscription.expires_at if subscription is not None else None
    # Standard багцтай ижил хуанлийн сар (`billing_service._extended`).
    premium_end: datetime = (
        await db.execute(
            select(
                func.greatest(func.coalesce(current, func.now()), func.now())
                + func.make_interval(0, payload.months)
            )
        )
    ).scalar_one()
    if subscription is None:
        subscription = LiveSubscription(user_id=user.id)
        db.add(subscription)
    subscription.tier = LiveTier.PREMIUM
    subscription.expires_at = premium_end
    subscription.granted_by = admin.id
    subscription.note = payload.note or None

    before = user.plan_expires_at
    if before is None or before < premium_end:
        user.plan_expires_at = premium_end
        db.add(
            PlanAdjustment(
                user_id=user.id,
                admin_id=admin.id,
                months=payload.months,
                expires_before=before,
                expires_after=premium_end,
                note=f"Premium {payload.months} сар"
                + (f" — {payload.note}" if payload.note else ""),
            )
        )
    await db.commit()
    await db.refresh(user)
    return await _info(db, user)
