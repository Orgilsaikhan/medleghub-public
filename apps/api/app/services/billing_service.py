"""Standard ба Premium багц — Wire-ээр 1–12 сарын төлбөр авч, багцыг сунгана.

Premium = Standard (сургалт + MedlegHub Live) + Live-ийн илүү AI хязгаар. Premium
төлбөр Standard-ийг `months` сараар сунгаж, Premium-ийг (`live_subscriptions`) мөн
сараар сунгана. Premium-ийг Live бүх хэрэглэгчид нээлттэй үед л зарна.

Нэг удаагийн Live эрх (`live_pass`, эзэн 2026-10-03) — багцгүй хэрэглэгч нэг
материалыг судална. Төлбөр нь багцыг сунгахгүй, `live_passes`-д эрх үүсгэнэ.
Хөнгөлөлт (промо, урилга) эрхэд орохгүй, урилгын «багц авсан найз»-д ч тоологдохгүй.
Эрх авснаас хойш `live_pass_upgrade_days` хоногийн дотор Standard/Premium авбал
эрхийн үнэ тэр төлбөрөөс хасагдана (`credit_mnt`), эрх `upgraded_at`-тэй болно.

Урсгал:
    1. `start_checkout` — `payments` мөр (сарын тоотой) → Wire PaymentIntent →
       hosted checkout. Амжилттай бол Wire `/billing/success` руу буцаана.
    2. Хэрэглэгч `pay.wire.mn` дээр QR/банкны апп-аар төлнө.
    3. Буцах хуудас (`sync_payment`) эсвэл webhook (`handle_webhook`) нь
       PaymentIntent-ийн төлөвийг Wire-ээс татаж, `succeeded` бол `apply_payment`.

Wire-д автомат сунгалт (subscription) байхгүй. Төлбөр бүр багцыг одоогийн
дуусах хугацаанаас (эсвэл одооноос) `payments.months` сараар сунгана. Олон
сараар авбал хямд: `plan_free_month_every` сар тутамд нэг сар үнэгүй.

Сарын үнийг админ өөрчилнө (`plan_prices`-ийн сүүлийн мөр); өөрчлөөгүй бол
`PLAN_PRICE_MNT`. Үнэ өөрчлөгдсөн ч үүссэн төлбөрийн дүн хэвээр.

Хөнгөлөлт (нэг төлбөрт нэг, нийлэхгүй): оруулсан промо код (`promo_service`),
эс бөгөөс урилгын кодоор бүртгүүлсэн хэрэглэгчийн ашиглаагүй хөнгөлөлт
(`referral_service`). Олон сарын нийт дүнгээс хувиар хасна. Төлбөр амжилттай
болоход кодыг ашигласанд, урилгын хөнгөлөлтийг хэрэглэсэнд тооцож, хэрэглэгчийг
урьсан хүнд «багц авсан найз» тоолж шагнал олгоно — бүгд нэг транзакцид
(`apply_payment`).
"""

import logging
import uuid
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Literal

import httpx
from sqlalchemy import ColumnElement, func, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from app.core.config import settings
from app.core.errors import AppError, ConflictError, NotFoundError
from app.models.enums import BillingPlan, LiveTier, PaymentStatus, PromoKind
from app.models.live import LivePass, LiveSubscription
from app.models.payment import Payment
from app.models.plan_adjustment import PlanAdjustment
from app.models.plan_price import PlanPrice
from app.models.promo_code import PromoCode, PromoRedemption
from app.models.referral import Referral
from app.models.user import User
from app.schemas.billing import (
    AdminUserPlanResponse,
    CheckoutResponse,
    PaymentReceipt,
    PaymentStatusResponse,
    PlanAdjustmentItem,
    PlanDiscount,
    PlanOption,
    PlanPriceResponse,
    PlanResponse,
    PromoRedeemResponse,
    RedemptionReceiptResponse,
    UpgradeCredit,
)
from app.schemas.promo import PromoPreview
from app.services import promo_service, referral_service, wire

logger = logging.getLogger(__name__)

# Wire нь төлөгдөөгүй intent-ийг 10 минутад цуцалдаг. Үүнээс хуучин хүлээгдэж
# буй төлбөрийг `plan` дуудлага бүрт дахин шалгах шаардлагагүй.
PENDING_RECHECK_WINDOW = timedelta(minutes=30)
# Эрхийн үнийг хасахад төлбөр үүнээс бага болохгүй (админы үнийн доод хязгаартай ижил).
MIN_PAYMENT_MNT = 100


def free_months(months: int) -> int:
    """6 сар тутамд 1 сар үнэгүй: 6–11 сар → 1, 12 сар → 2."""
    return months // settings.plan_free_month_every


def _default_price(plan: BillingPlan) -> int:
    if plan == BillingPlan.PREMIUM:
        return settings.premium_price_mnt
    if plan == BillingPlan.LIVE_PASS:
        return settings.live_pass_price_mnt
    return settings.plan_price_mnt


async def _latest_price(
    db: AsyncSession, plan: BillingPlan = BillingPlan.STANDARD
) -> PlanPrice | None:
    return (
        await db.execute(
            select(PlanPrice)
            .where(PlanPrice.plan == plan)
            .order_by(PlanPrice.created_at.desc())
            .limit(1)
        )
    ).scalar_one_or_none()


async def monthly_price(db: AsyncSession, plan: BillingPlan = BillingPlan.STANDARD) -> int:
    """Одоогийн сарын үнэ, бүхэл төгрөг — админы тавьсан, эсвэл анхдагч."""
    latest = await _latest_price(db, plan)
    return latest.price_mnt if latest else _default_price(plan)


def premium_available(user: User | None) -> bool:
    """Premium-ийн ялгаа нь Live-ийн AI — Live бүгдэд нээлттэй үед л зарна (админ турших)."""
    return settings.live_access == "all" or (user is not None and user.is_admin)


def live_pass_available(user: User | None) -> bool:
    """Нэг удаагийн эрх ч Live-ийнх — Premium шиг Live бүгдэд нээлттэй үед л."""
    return premium_available(user)


async def _has_unused_pass(db: AsyncSession, user_id: uuid.UUID) -> bool:
    """Ашиглаагүй, багц руу шилжээгүй эрх — хугацаагүй."""
    found = await db.execute(
        select(LivePass.id)
        .where(
            LivePass.user_id == user_id,
            LivePass.used_at.is_(None),
            LivePass.upgraded_at.is_(None),
        )
        .limit(1)
    )
    return found.scalar_one_or_none() is not None


@dataclass(frozen=True)
class Credit:
    """Багц авахад хасагдах нэг удаагийн эрхийн үнэ."""

    pass_id: uuid.UUID
    amount_mnt: int
    expires_at: datetime


async def _upgrade_credit(db: AsyncSession, user: User) -> Credit | None:
    """Сүүлийн `live_pass_upgrade_days` хоногт авсан, багц руу шилжээгүй хамгийн сүүлийн
    эрх. Ашигласан эсэх хамаагүй — эрхээр туршаад багц авахыг урамшуулна."""
    window = timedelta(days=settings.live_pass_upgrade_days)
    row = (
        await db.execute(
            select(LivePass)
            .where(
                LivePass.user_id == user.id,
                LivePass.upgraded_at.is_(None),
                LivePass.price_mnt > 0,
                LivePass.created_at > func.now() - window,
            )
            .order_by(LivePass.created_at.desc())
            .limit(1)
        )
    ).scalar_one_or_none()
    if row is None:
        return None
    return Credit(row.id, row.price_mnt, row.created_at + window)


def credit_amount(price_after_discount: int, credit: Credit | None) -> int:
    """Энэ төлбөрөөс хасах эрхийн үнэ — төлбөр `MIN_PAYMENT_MNT`-ээс бага болохгүй."""
    if credit is None:
        return 0
    return max(0, min(credit.amount_mnt, price_after_discount - MIN_PAYMENT_MNT))


async def _premium_until(db: AsyncSession, user: User) -> datetime | None:
    subscription = await db.get(LiveSubscription, user.id)
    return subscription.expires_at if subscription is not None else None


def plan_price(months: int, monthly: int) -> int:
    """`months` сарын нийт үнэ, бүхэл төгрөг. Үнэгүй сарыг тооцохгүй."""
    return monthly * (months - free_months(months))


def discount_amount(total: int, percent_off: int) -> int:
    """Хасах дүн, бүхэл төгрөг (доош бүхэлчилнэ)."""
    return total * percent_off // 100


@dataclass(frozen=True)
class Discount:
    """Checkout-д орох нэг хөнгөлөлт ба түүний эх үүсвэр."""

    source: Literal["promo", "referral"]
    percent_off: int
    promo: PromoCode | None = None
    referral_id: uuid.UUID | None = None


def plan_options(
    monthly: int, percent_off: int = 0, credit: Credit | None = None
) -> list[PlanOption]:
    options = []
    for months in range(1, settings.plan_max_months + 1):
        price = plan_price(months, monthly)
        discounted = price - discount_amount(price, percent_off)
        minus = credit_amount(discounted, credit)
        options.append(
            PlanOption(
                months=months,
                free_months=free_months(months),
                price_mnt=price,
                final_price_mnt=discounted - minus,
                credit_mnt=minus,
            )
        )
    return options


async def _plan_for(db: AsyncSession, user: User) -> PlanResponse:
    """Хэрэглэгчийн багц. Урилгын хөнгөлөлт байвал үнэд тусгана."""
    monthly = await monthly_price(db)
    premium = await monthly_price(db, BillingPlan.PREMIUM)
    referral = await referral_service.available_discount(db, user.id)
    discount = (
        PlanDiscount(source="referral", percent_off=settings.referral_friend_percent_off)
        if referral is not None
        else None
    )
    percent_off = discount.percent_off if discount else 0
    available = premium_available(user)
    premium_until = await _premium_until(db, user)
    credit = await _upgrade_credit(db, user)
    return PlanResponse(
        has_plan=user.has_plan,
        plan_expires_at=user.plan_expires_at,
        price_mnt=monthly,
        options=plan_options(monthly, percent_off, credit),
        discount=discount,
        premium_available=available,
        premium_price_mnt=premium,
        premium_options=plan_options(premium, percent_off, credit) if available else [],
        has_premium=premium_until is not None and premium_until > datetime.now(UTC),
        premium_expires_at=premium_until,
        live_pass_available=live_pass_available(user),
        live_pass_price_mnt=await monthly_price(db, BillingPlan.LIVE_PASS),
        has_unused_live_pass=await _has_unused_pass(db, user.id),
        upgrade_credit=(
            UpgradeCredit(amount_mnt=credit.amount_mnt, expires_at=credit.expires_at)
            if credit
            else None
        ),
    )


async def anonymous_plan(db: AsyncSession) -> PlanResponse:
    monthly = await monthly_price(db)
    premium = await monthly_price(db, BillingPlan.PREMIUM)
    available = premium_available(None)
    return PlanResponse(
        has_plan=False,
        plan_expires_at=None,
        price_mnt=monthly,
        options=plan_options(monthly),
        premium_available=available,
        premium_price_mnt=premium,
        premium_options=plan_options(premium) if available else [],
        live_pass_available=live_pass_available(None),
        live_pass_price_mnt=await monthly_price(db, BillingPlan.LIVE_PASS),
    )


async def _checkout_discount(
    db: AsyncSession, user: User, promo_code: str | None
) -> Discount | None:
    """Промо код оруулсан бол зөвхөн түүнийг — урилгын хөнгөлөлттэй нийлэхгүй,
    урилгын хөнгөлөлт дараагийн төлбөрт хадгалагдана. Эс бөгөөс урилгын хөнгөлөлтийг."""
    if promo_code:
        promo = await promo_service.find_usable(db, user, promo_code)
        if promo.kind != PromoKind.PERCENT or promo.percent_off is None:
            raise promo_service.free_months_code()
        return Discount(source="promo", percent_off=promo.percent_off, promo=promo)
    referral = await referral_service.available_discount(db, user.id)
    if referral is not None:
        return Discount(
            source="referral",
            percent_off=settings.referral_friend_percent_off,
            referral_id=referral.id,
        )
    return None


async def promo_preview(db: AsyncSession, user: User, code: str) -> PromoPreview:
    """Кодыг шалгаж, юу өгөхийг харуулна. Ашигласанд тооцохгүй."""
    promo = await promo_service.find_usable(db, user, code)
    options = premium_options = []
    if promo.kind == PromoKind.PERCENT and promo.percent_off is not None:
        credit = await _upgrade_credit(db, user)
        options = plan_options(await monthly_price(db), promo.percent_off, credit)
        if premium_available(user):
            premium_options = plan_options(
                await monthly_price(db, BillingPlan.PREMIUM), promo.percent_off, credit
            )
    return PromoPreview(
        code=promo.code,
        kind=PromoKind(promo.kind),
        percent_off=promo.percent_off,
        free_months=promo.free_months,
        expires_at=promo.expires_at,
        options=options,
        premium_options=premium_options,
    )


async def redeem_promo(db: AsyncSession, user: User, code: str) -> PromoRedeemResponse:
    """Үнэгүй сарын кодоор багцыг төлбөргүй сунгана — төлбөртэй адил одоогийн
    дуусах хугацаанаас (өнгөрсөн бол одооноос)."""
    # Кодын мөрийг түгжинэ — зэрэг идэвхжүүлэхэд `max_uses` хэтрэхгүй.
    promo = await promo_service.find_usable(db, user, code, lock=True)
    if promo.kind != PromoKind.FREE_MONTHS or promo.free_months is None:
        await db.rollback()
        raise promo_service.not_redeemable()
    redeemed = (
        await db.execute(
            insert(PromoRedemption)
            .values(promo_code_id=promo.id, user_id=user.id, months=promo.free_months)
            .on_conflict_do_nothing(constraint="uq_promo_redemptions_code_user")
            .returning(PromoRedemption.id)
        )
    ).scalar_one_or_none()
    if redeemed is None:
        await db.rollback()
        raise promo_service.already_used()
    await db.execute(
        update(User).where(User.id == user.id).values(plan_expires_at=_extended(promo.free_months))
    )
    await db.commit()
    logger.info(
        "Хэрэглэгч %s промо код %s-ээр %s сар авлаа", user.id, promo.code, promo.free_months
    )
    await db.refresh(user)
    plan = await _plan_for(db, user)
    return PromoRedeemResponse(**plan.model_dump(), redemption_id=redeemed)


async def redemption_receipt(
    db: AsyncSession, user: User, redemption_id: uuid.UUID
) -> RedemptionReceiptResponse:
    """Үнэгүй сарын промо кодын баримт. Бусдынх, эсвэл төлбөртэй холбоотой
    (хувийн хөнгөлөлтийн) бичлэгийг байхгүй мэт харуулна — тэдгээрийн баримт нь
    төлбөрийнх."""
    row = (
        await db.execute(
            select(PromoRedemption, PromoCode.code)
            .join(PromoCode, PromoCode.id == PromoRedemption.promo_code_id)
            .where(PromoRedemption.id == redemption_id)
        )
    ).one_or_none()
    if row is None or row[0].user_id != user.id or row[0].months is None:
        raise NotFoundError("REDEMPTION_NOT_FOUND", "Промо кодын баримт олдсонгүй.")
    redemption, code = row
    return RedemptionReceiptResponse(
        id=redemption.id,
        plan=await _plan_for(db, user),
        receipt=PaymentReceipt(
            kind="promo",
            months=redemption.months,
            free_months=redemption.months,
            list_price_mnt=0,
            discount_percent=0,
            discount_mnt=0,
            discount_source="promo",
            promo_code=code,
            amount_mnt=0,
            currency="MNT",
            reference=None,
            created_at=redemption.created_at,
            paid_at=redemption.created_at,
        ),
    )


async def _price_row(
    db: AsyncSession, plan: BillingPlan
) -> tuple[int, datetime | None, str | None]:
    """`(үнэ, хэзээ өөрчилсөн, хэн)` — өөрчлөөгүй бол анхдагч үнэ."""
    latest = await _latest_price(db, plan)
    if latest is None:
        return _default_price(plan), None, None
    changed_by = None
    if latest.changed_by is not None:
        changed_by = (
            await db.execute(select(User.name).where(User.id == latest.changed_by))
        ).scalar_one_or_none()
    return latest.price_mnt, latest.created_at, changed_by


async def price_info(db: AsyncSession) -> PlanPriceResponse:
    price, changed_at, changed_by = await _price_row(db, BillingPlan.STANDARD)
    premium, premium_at, premium_by = await _price_row(db, BillingPlan.PREMIUM)
    live_pass, live_pass_at, live_pass_by = await _price_row(db, BillingPlan.LIVE_PASS)
    return PlanPriceResponse(
        price_mnt=price,
        default_price_mnt=settings.plan_price_mnt,
        changed_at=changed_at,
        changed_by=changed_by,
        premium_price_mnt=premium,
        premium_default_price_mnt=settings.premium_price_mnt,
        premium_changed_at=premium_at,
        premium_changed_by=premium_by,
        live_pass_price_mnt=live_pass,
        live_pass_default_price_mnt=settings.live_pass_price_mnt,
        live_pass_changed_at=live_pass_at,
        live_pass_changed_by=live_pass_by,
    )


async def set_monthly_price(
    db: AsyncSession, admin: User, price_mnt: int, plan: BillingPlan = BillingPlan.STANDARD
) -> PlanPriceResponse:
    """Админ сарын үнийг (`live_pass`-д нэг эрхийн үнийг) өөрчилнө. Хүлээгдэж буй
    төлбөрийн дүн өөрчлөгдөхгүй."""
    db.add(PlanPrice(price_mnt=price_mnt, changed_by=admin.id, plan=plan))
    await db.commit()
    logger.info("%s-ийн үнэ %s₮ болов (админ %s)", plan, price_mnt, admin.id)
    return await price_info(db)


def _return_urls(payment_id: uuid.UUID) -> tuple[str | None, str | None]:
    """Wire зөвхөн HTTPS хаяг хүлээж авна. Хөгжүүлэлтэд (`http://localhost`)
    буцах хаяггүй — Wire өөрийн «амжилттай» хуудсаа харуулж, хэрэглэгч
    `/pricing` руу буцахад хүлээгдэж буй төлбөр шалгагдана."""
    base = settings.site_url.rstrip("/")
    if not base.startswith("https://"):
        return None, None
    return f"{base}/billing/success?payment={payment_id}", f"{base}/pricing"


async def start_checkout(
    db: AsyncSession,
    client: httpx.AsyncClient,
    user: User,
    months: int,
    promo_code: str | None = None,
    plan: BillingPlan = BillingPlan.STANDARD,
) -> CheckoutResponse:
    if not settings.wire_secret_key:
        raise AppError(
            503, "BILLING_NOT_CONFIGURED", "Төлбөр хүлээн авах тохиргоо хийгдээгүй байна."
        )
    if plan == BillingPlan.PREMIUM and not premium_available(user):
        raise AppError(409, "PREMIUM_NOT_AVAILABLE", "Premium багц одоохондоо худалдаалагдахгүй.")

    if plan == BillingPlan.LIVE_PASS:
        await _assert_can_buy_pass(db, user, promo_code)
        # Нэг эрх: багц сунгахгүй, хөнгөлөлтгүй, хасагдах эрхгүй.
        months, discount, credit = 0, None, None
        total = await monthly_price(db, plan)
    else:
        discount = await _checkout_discount(db, user, promo_code)
        credit = await _upgrade_credit(db, user)
        total = plan_price(months, await monthly_price(db, plan))
    percent_off = discount.percent_off if discount else 0
    minus = discount_amount(total, percent_off)
    credit_mnt = credit_amount(total - minus, credit)
    payment = Payment(
        user_id=user.id,
        provider="wire",
        # Бүхэл төгрөг — Wire-ийн баримт бичигт «minor unit» гэсэн ч live API
        # дүнг QPay руу шууд дамжуулдаг: 150000 = 150,000₮ (2026-09-28).
        amount=total - minus - credit_mnt,
        currency="MNT",
        status=PaymentStatus.PENDING,
        months=months,
        plan=plan,
        discount_percent=percent_off,
        discount_mnt=minus,
        promo_code_id=discount.promo.id if discount and discount.promo else None,
        referral_id=discount.referral_id if discount else None,
        # Зэрэг нээсэн хоёр нэхэмжлэх хоёулаа хасалттай төлөгдөж болно (промо код шиг) —
        # эрх нэг л удаа `upgraded_at` авна.
        live_pass_id=credit.pass_id if credit and credit_mnt else None,
        credit_mnt=credit_mnt,
    )
    db.add(payment)
    await db.commit()
    await db.refresh(payment)

    success_url, cancel_url = _return_urls(payment.id)
    try:
        intent = await wire.create_payment_intent(
            client,
            amount=payment.amount,
            description=_description(plan, months, percent_off, credit_mnt),
            metadata={"payment_id": str(payment.id), "user_id": str(user.id)},
            idempotency_key=f"medleghub-pi-{payment.id}",
        )
        payment.provider_payment_id = str(intent["id"])
        session = await wire.create_checkout_session(
            client,
            payment_intent=payment.provider_payment_id,
            success_url=success_url,
            cancel_url=cancel_url,
            idempotency_key=f"medleghub-cs-{payment.id}",
        )
    except (AppError, KeyError):
        payment.status = PaymentStatus.FAILED
        await db.commit()
        raise

    payment.checkout_url = session["url"]
    await db.commit()
    return CheckoutResponse(payment_id=payment.id, checkout_url=session["url"])


async def _assert_can_buy_pass(db: AsyncSession, user: User, promo_code: str | None) -> None:
    if not live_pass_available(user):
        raise AppError(
            409, "LIVE_PASS_NOT_AVAILABLE", "Нэг удаагийн эрх одоохондоо худалдаалагдахгүй."
        )
    if promo_code:
        raise ConflictError("PROMO_NOT_FOR_LIVE_PASS", "Промо код нэг удаагийн эрхэд хамаарахгүй.")
    if user.has_plan:
        raise ConflictError(
            "LIVE_PASS_HAS_PLAN", "Таны багцад Live багтсан тул нэг удаагийн эрх хэрэггүй."
        )
    if await _has_unused_pass(db, user.id):
        raise ConflictError(
            "LIVE_PASS_UNUSED",
            "Танд ашиглаагүй нэг удаагийн эрх байна. Эхлээд түүнийгээ ашиглана уу.",
        )


def _description(plan: BillingPlan, months: int, percent_off: int, credit_mnt: int) -> str:
    """Wire-ийн төлбөрийн хуудсанд харагдах тайлбар."""
    if plan == BillingPlan.LIVE_PASS:
        return "Medleghub Live — нэг удаагийн эрх"
    notes = []
    if percent_off:
        notes.append(f"{percent_off}% хөнгөлөлттэй")
    if credit_mnt:
        notes.append(f"нэг удаагийн эрхийн {credit_mnt:,}₮ хасагдсан")
    suffix = f" ({', '.join(notes)})" if notes else ""
    return f"Medleghub {plan.capitalize()} багц — {months} сар{suffix}"


def _extended(months: int) -> ColumnElement[datetime]:
    """Одоогийн дуусах хугацаанаас (өнгөрсөн бол одооноос) `months` сараар."""
    now = func.now()
    return func.greatest(func.coalesce(User.plan_expires_at, now), now) + func.make_interval(
        0, months
    )


async def _reward_referrer(db: AsyncSession, friend_id: uuid.UUID) -> None:
    """Урилгаар бүртгүүлсэн хэрэглэгч анх төлсөн бол урьсан хүний «багц авсан
    найз» болно. `REFERRAL_FRIENDS_PER_REWARD` найз хүрэх бүрд урьсан хүний
    багцыг сунгана. Commit-ийг дуудагч хийнэ.

    `first_paid_at IS NULL` нөхцөл нь найзыг нэг л удаа тоолно. Урьсан хүний
    мөрийг түгжиж тоолдог тул өөр өөр найзын зэрэг ирсэн төлбөр шагналыг
    давхар олгохгүй — хоёр дахь нь эхнийхийг commit хийсний дараа тоолно.
    """
    row = (
        await db.execute(
            update(Referral)
            .where(Referral.friend_id == friend_id, Referral.first_paid_at.is_(None))
            .values(first_paid_at=func.now())
            .returning(Referral.id, Referral.referrer_id)
        )
    ).one_or_none()
    if row is None:
        return
    referral_id, referrer_id = row
    await db.execute(select(User.id).where(User.id == referrer_id).with_for_update())
    paying, rewarded = (
        await db.execute(
            select(
                func.count(Referral.first_paid_at),
                func.coalesce(func.sum(Referral.months_rewarded), 0),
            ).where(Referral.referrer_id == referrer_id)
        )
    ).one()
    earned = paying // settings.referral_friends_per_reward * settings.referral_reward_months
    due = earned - rewarded
    if due <= 0:
        return
    await db.execute(
        update(Referral)
        .where(Referral.id == referral_id)
        .values(months_rewarded=Referral.months_rewarded + due)
    )
    await db.execute(
        update(User).where(User.id == referrer_id).values(plan_expires_at=_extended(due))
    )
    logger.info("Урилга: хэрэглэгч %s %s найз багц авсанд %s сар авлаа", referrer_id, paying, due)


async def _extend_premium(db: AsyncSession, user_id: uuid.UUID, months: int) -> None:
    """Premium-ийг одоогийн дуусах хугацаанаас (өнгөрсөн бол одооноос) `months` сараар.
    Commit-ийг дуудагч хийнэ."""
    interval = func.make_interval(0, months)
    statement = insert(LiveSubscription).values(
        user_id=user_id, tier=LiveTier.PREMIUM, expires_at=func.now() + interval, note="Төлбөр"
    )
    await db.execute(
        statement.on_conflict_do_update(
            index_elements=[LiveSubscription.user_id],
            set_={
                "tier": LiveTier.PREMIUM,
                "expires_at": func.greatest(LiveSubscription.expires_at, func.now()) + interval,
                "note": "Төлбөр",
                "updated_at": func.now(),
            },
        )
    )


async def apply_payment(db: AsyncSession, payment_id: uuid.UUID) -> bool:
    """Төлбөрийг амжилттай гэж тэмдэглэж, багцыг `months` сараар сунгана. Нэг л удаа.

    Нөхцөлт UPDATE нь мөрийг түгжинэ: зэрэг ирсэн хоёр дуудлагын хоёр дахь нь
    эхнийхийг commit хийсний дараа `status != succeeded` нөхцөлийг дахин
    шалгаж, юу ч өөрчлөхгүй. Тиймээс сар хэзээ ч давхар нэмэгдэхгүй.

    Мөн тэр транзакцид: промо кодыг ашигласанд, урилгын хөнгөлөлтийг
    хэрэглэсэнд тооцож, энэ хэрэглэгчийг урьсан хүнд «багц авсан найз» тоолно.
    Нэг удаагийн эрхийн төлбөр зөвхөн эрх үүсгэнэ; үнэ нь хасагдсан эрхийг багц руу
    шилжсэнд тооцно.
    """
    row = (
        await db.execute(
            update(Payment)
            .where(Payment.id == payment_id, Payment.status != PaymentStatus.SUCCEEDED)
            .values(status=PaymentStatus.SUCCEEDED, paid_at=func.now())
            .returning(
                Payment.user_id,
                Payment.months,
                Payment.promo_code_id,
                Payment.referral_id,
                Payment.plan,
                Payment.amount,
                Payment.live_pass_id,
            )
        )
    ).one_or_none()
    if row is None:
        await db.rollback()
        return False

    user_id, months, promo_code_id, referral_id, plan, amount, live_pass_id = row
    if plan == BillingPlan.LIVE_PASS:
        if user_id is not None:
            created = (
                await db.execute(
                    insert(LivePass)
                    .values(user_id=user_id, price_mnt=amount)
                    .returning(LivePass.id)
                )
            ).scalar_one()
            await db.execute(
                update(Payment).where(Payment.id == payment_id).values(live_pass_id=created)
            )
        await db.commit()
        return True

    if live_pass_id is not None:
        upgraded = await db.execute(
            update(LivePass)
            .where(LivePass.id == live_pass_id, LivePass.upgraded_at.is_(None))
            .values(upgraded_at=func.now())
            .returning(LivePass.id)
        )
        if upgraded.scalar_one_or_none() is None:
            logger.warning("Нэг удаагийн эрх %s аль хэдийн багц руу шилжсэн", live_pass_id)
    if user_id is not None:
        await db.execute(
            update(User).where(User.id == user_id).values(plan_expires_at=_extended(months))
        )
        if plan == BillingPlan.PREMIUM:
            await _extend_premium(db, user_id, months)
        if promo_code_id is not None:
            # Зэрэг нээсэн өөр нэхэмжлэхээр аль хэдийн ашигласан бол давхар бичихгүй.
            await db.execute(
                insert(PromoRedemption)
                .values(promo_code_id=promo_code_id, user_id=user_id, payment_id=payment_id)
                .on_conflict_do_nothing(constraint="uq_promo_redemptions_code_user")
            )
        await _reward_referrer(db, user_id)
    if referral_id is not None:
        await db.execute(
            update(Referral)
            .where(Referral.id == referral_id, Referral.discount_used_at.is_(None))
            .values(discount_used_at=func.now())
        )
    await db.commit()
    return True


async def sync_payment(db: AsyncSession, client: httpx.AsyncClient, payment: Payment) -> Payment:
    """PaymentIntent-ийн төлөвийг Wire-ээс татаж, манай мөрийг шинэчилнэ."""
    if payment.status == PaymentStatus.SUCCEEDED or not payment.provider_payment_id:
        return payment

    intent = await wire.retrieve_payment_intent(client, payment.provider_payment_id)
    status = intent.get("status")

    if status == "succeeded":
        if intent.get("amount") != payment.amount or intent.get("currency") != payment.currency:
            # Бидний үүсгэсэн intent-тэй таарахгүй — багц олгохгүй.
            logger.warning(
                "Wire intent %s дүн таарахгүй: %s %s",
                payment.provider_payment_id,
                intent.get("amount"),
                intent.get("currency"),
            )
            payment.status = PaymentStatus.FAILED
            await db.commit()
        else:
            await apply_payment(db, payment.id)
    elif status == "canceled" and payment.status == PaymentStatus.PENDING:
        payment.status = PaymentStatus.CANCELED
        await db.commit()

    await db.refresh(payment)
    return payment


async def get_payment_status(
    db: AsyncSession, client: httpx.AsyncClient, user: User, payment_id: uuid.UUID
) -> PaymentStatusResponse:
    payment = await db.get(Payment, payment_id)
    # Бусдын төлбөрийг байхгүй мэт харуулна — ID таамаглах утгагүй.
    if payment is None or payment.user_id != user.id:
        raise NotFoundError("PAYMENT_NOT_FOUND", "Төлбөр олдсонгүй.")
    payment = await sync_payment(db, client, payment)
    await db.refresh(user)
    return PaymentStatusResponse(
        id=payment.id,
        status=payment.status,
        plan=await _plan_for(db, user),
        receipt=await _receipt(db, payment) if payment.status == PaymentStatus.SUCCEEDED else None,
    )


async def _receipt(db: AsyncSession, payment: Payment) -> PaymentReceipt:
    """Төлбөрийн мөрөөс баримт. Промо кодыг нэрээр нь, хөнгөлөлтийн эх үүсвэрийг
    холбоосоос нь тодорхойлно (код/урилга устсан бол эх үүсвэргүй)."""
    promo_code = None
    if payment.promo_code_id is not None:
        promo_code = (
            await db.execute(select(PromoCode.code).where(PromoCode.id == payment.promo_code_id))
        ).scalar_one_or_none()
    source: Literal["promo", "referral"] | None = None
    if payment.promo_code_id is not None:
        source = "promo"
    elif payment.referral_id is not None:
        source = "referral"
    return PaymentReceipt(
        plan=payment.plan,
        months=payment.months,
        free_months=free_months(payment.months),
        list_price_mnt=payment.amount + payment.discount_mnt + payment.credit_mnt,
        discount_percent=payment.discount_percent,
        discount_mnt=payment.discount_mnt,
        credit_mnt=payment.credit_mnt,
        discount_source=source,
        promo_code=promo_code,
        amount_mnt=payment.amount,
        currency=payment.currency,
        reference=payment.provider_payment_id,
        created_at=payment.created_at,
        paid_at=payment.paid_at,
    )


async def get_plan(db: AsyncSession, client: httpx.AsyncClient, user: User) -> PlanResponse:
    """Багцын төлөв. Саяхны хүлээгдэж буй төлбөрийг давхар шалгана.

    Webhook тохируулаагүй, эсвэл хэрэглэгч Wire-ийн хуудсыг хаачихсан ч
    `/pricing`-т буцаж ирэхэд төлсөн төлбөр нь бүртгэгдэнэ.
    """
    if settings.wire_secret_key:
        cutoff = datetime.now(UTC) - PENDING_RECHECK_WINDOW
        pending = (
            (
                await db.execute(
                    select(Payment).where(
                        Payment.user_id == user.id,
                        Payment.status == PaymentStatus.PENDING,
                        Payment.provider_payment_id.is_not(None),
                        Payment.created_at > cutoff,
                    )
                )
            )
            .scalars()
            .all()
        )
        for payment in pending:
            try:
                await sync_payment(db, client, payment)
            except AppError:
                # Wire түр унавал багцын төлөвийг харуулахад саад болохгүй.
                logger.warning("Wire төлбөр %s шалгаж чадсангүй", payment.id)
        await db.refresh(user)
    return await _plan_for(db, user)


async def handle_webhook(
    db: AsyncSession, client: httpx.AsyncClient, payload: bytes, signature: str | None
) -> None:
    if not settings.wire_webhook_secret:
        raise AppError(503, "WEBHOOK_NOT_CONFIGURED", "Webhook тохируулагдаагүй байна.")
    event = wire.verify_webhook(payload, signature, settings.wire_webhook_secret)

    # `endpoint.verification` зэрэг бусад event-д 2xx хариулахад л хангалттай.
    if event.get("type") != "payment_intent.succeeded":
        return
    intent_id = wire.event_payment_intent_id(event)
    if intent_id is None:
        return
    payment = (
        await db.execute(select(Payment).where(Payment.provider_payment_id == intent_id))
    ).scalar_one_or_none()
    if payment is None:
        logger.warning("Wire webhook: үл мэдэгдэх intent %s", intent_id)
        return
    await sync_payment(db, client, payment)


def _user_not_found() -> NotFoundError:
    return NotFoundError("USER_NOT_FOUND", "Ийм имэйлтэй хэрэглэгч олдсонгүй.")


async def user_plan(db: AsyncSession, email: str) -> AdminUserPlanResponse:
    """Админд: хэрэглэгчийн багц ба гараар хийсэн сүүлийн өөрчлөлтүүд."""
    user = (await db.execute(select(User).where(User.email == email))).scalar_one_or_none()
    if user is None:
        raise _user_not_found()

    admin = aliased(User)
    rows = (
        await db.execute(
            select(PlanAdjustment, admin.name)
            .outerjoin(admin, admin.id == PlanAdjustment.admin_id)
            .where(PlanAdjustment.user_id == user.id)
            .order_by(PlanAdjustment.created_at.desc())
            .limit(settings.plan_adjustment_history)
        )
    ).all()
    return AdminUserPlanResponse(
        user_id=user.id,
        name=user.name,
        email=user.email,
        has_plan=user.has_plan,
        plan_expires_at=user.plan_expires_at,
        adjustments=[
            PlanAdjustmentItem(
                id=adjustment.id,
                months=adjustment.months,
                expires_before=adjustment.expires_before,
                expires_after=adjustment.expires_after,
                note=adjustment.note,
                admin_name=admin_name,
                created_at=adjustment.created_at,
            )
            for adjustment, admin_name in rows
        ],
    )


async def adjust_plan(
    db: AsyncSession, admin: User, email: str, months: int, note: str | None
) -> AdminUserPlanResponse:
    """Админ гараар багцыг `months` сараар нэмнэ (эерэг) эсвэл хасна (сөрөг).

    Төлбөрийн мөр үүсгэхгүй — өөрчлөлт бүр `plan_adjustments`-д үлдэнэ.

    - Нэмэхэд төлбөртэй адил: одоогийн дуусах хугацаанаас (өнгөрсөн бол
      одооноос) сунгана.
    - Хасахад зөвхөн идэвхтэй багцаас хасна. Үлдсэнээс их хасвал багц яг
      одоо дуусна — өнгөрсөн огноо болохгүй.
    """
    # Мөрийг түгжинэ: зэрэг ирсэн төлбөр, өөр админы өөрчлөлт хоорондоо
    # дарагдахгүй, `expires_before` нь яг өөрчлөхийн өмнөх утга болно.
    user = (
        await db.execute(select(User).where(User.email == email).with_for_update())
    ).scalar_one_or_none()
    if user is None:
        raise _user_not_found()
    before = user.plan_expires_at

    if months > 0:
        statement = update(User).where(User.id == user.id).values(plan_expires_at=_extended(months))
    else:
        statement = (
            update(User)
            .where(User.id == user.id, User.plan_expires_at > func.now())
            .values(
                plan_expires_at=func.greatest(
                    User.plan_expires_at - func.make_interval(0, -months), func.now()
                )
            )
        )
    after = (await db.execute(statement.returning(User.plan_expires_at))).scalar_one_or_none()
    if after is None:
        await db.rollback()
        raise ConflictError("NO_ACTIVE_PLAN", "Хэрэглэгчид хасах идэвхтэй багц алга.")

    db.add(
        PlanAdjustment(
            user_id=user.id,
            admin_id=admin.id,
            months=months,
            expires_before=before,
            expires_after=after,
            note=note,
        )
    )
    await db.commit()
    logger.info(
        "Админ %s хэрэглэгч %s-ийн багцыг %+d сараар өөрчиллөө: %s → %s",
        admin.id,
        user.id,
        months,
        before,
        after,
    )
    # UPDATE-ийг ORM-оор биш хийсэн тул session дахь `user` хуучирсан.
    db.expire(user)
    return await user_plan(db, email)
