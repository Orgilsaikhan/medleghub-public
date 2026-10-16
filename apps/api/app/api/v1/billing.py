"""Standard багц ба Wire төлбөр."""

import uuid
from typing import Annotated

import httpx
from fastapi import APIRouter, Depends, Request

from app.core import rate_limit
from app.core.config import settings
from app.core.deps import AdminUser, CurrentUser, DbSession, OptionalUser
from app.core.errors import RateLimitError
from app.models.enums import BillingPlan
from app.schemas.billing import (
    AdminUserPlanResponse,
    CheckoutRequest,
    CheckoutResponse,
    PaymentStatusResponse,
    PlanGrantRequest,
    PlanLookupRequest,
    PlanPriceResponse,
    PlanPriceUpdate,
    PlanResponse,
    PromoRedeemResponse,
    RedemptionReceiptResponse,
)
from app.schemas.common import MessageResponse
from app.schemas.promo import (
    PromoCheckRequest,
    PromoCodeCreate,
    PromoCodeItem,
    PromoCodeUpdate,
    PromoPreview,
)
from app.services import billing_service, promo_service
from app.services.wire import SIGNATURE_HEADER, get_wire_client

router = APIRouter(prefix="/billing", tags=["billing"])

WireClient = Annotated[httpx.AsyncClient, Depends(get_wire_client)]


async def limit_checkout(user: CurrentUser) -> None:
    """Нэхэмжлэх бүр Wire дээр intent үүсгэдэг — хэрэглэгч тус бүрд хязгаарлана."""
    if not settings.rate_limit_enabled:
        return
    allowed, retry_after = rate_limit.backend.hit(
        f"checkout:{user.id}",
        settings.checkout_rate_limit_max,
        settings.checkout_rate_limit_window_seconds,
    )
    if not allowed:
        raise RateLimitError(retry_after)


async def limit_promo(user: CurrentUser) -> None:
    """Промо кодыг таамаглаж олохоос сэргийлнэ — хэрэглэгч тус бүрд."""
    rate_limit.enforce(
        f"promo:{user.id}", settings.promo_rate_limit_max, settings.promo_rate_limit_window_seconds
    )


@router.get("/plan", response_model=PlanResponse)
async def get_plan(db: DbSession, user: OptionalUser, client: WireClient) -> PlanResponse:
    """Нэвтрээгүй зочинд зөвхөн үнэ. Үнийг админ тавина (`PUT /billing/price`)."""
    if user is None:
        return await billing_service.anonymous_plan(db)
    return await billing_service.get_plan(db, client, user)


@router.post(
    "/checkout",
    response_model=CheckoutResponse,
    dependencies=[Depends(limit_checkout)],
)
async def checkout(
    db: DbSession, user: CurrentUser, client: WireClient, payload: CheckoutRequest | None = None
) -> CheckoutResponse:
    """1–12 сарын төлбөрийн нэхэмжлэх үүсгэж, Wire-ийн төлбөрийн хуудсыг буцаана.

    Body-гүй бол нэг сар — хуучин client-үүд эвдрэхгүй. Промо код оруулаагүй
    бол ашиглаагүй урилгын хөнгөлөлт автоматаар орно.
    """
    months = payload.months if payload else 1
    promo_code = payload.promo_code if payload else None
    plan = BillingPlan(payload.plan) if payload else BillingPlan.STANDARD
    return await billing_service.start_checkout(db, client, user, months, promo_code, plan)


@router.post("/promo/check", response_model=PromoPreview, dependencies=[Depends(limit_promo)])
async def check_promo(payload: PromoCheckRequest, db: DbSession, user: CurrentUser) -> PromoPreview:
    """Промо кодыг шалгана — хувийн код бол хөнгөлөлттэй үнийг буцаана."""
    return await billing_service.promo_preview(db, user, payload.code)


@router.post(
    "/promo/redeem", response_model=PromoRedeemResponse, dependencies=[Depends(limit_promo)]
)
async def redeem_promo(
    payload: PromoCheckRequest, db: DbSession, user: CurrentUser
) -> PromoRedeemResponse:
    """Үнэгүй сарын кодыг идэвхжүүлж, багцыг төлбөргүй сунгана. `redemption_id`-аар
    баримтыг (`GET /billing/redemptions/{id}`) авна."""
    return await billing_service.redeem_promo(db, user, payload.code)


@router.get("/redemptions/{redemption_id}", response_model=RedemptionReceiptResponse)
async def redemption_receipt(
    redemption_id: uuid.UUID, db: DbSession, user: CurrentUser
) -> RedemptionReceiptResponse:
    """Үнэгүй сарын промо кодын баримт — зөвхөн өөрийнх."""
    return await billing_service.redemption_receipt(db, user, redemption_id)


@router.get("/payments/{payment_id}", response_model=PaymentStatusResponse)
async def payment_status(
    payment_id: uuid.UUID, db: DbSession, user: CurrentUser, client: WireClient
) -> PaymentStatusResponse:
    """Төлбөрийн дараах буцах хуудас — төлөвийг Wire-ээс шалгана."""
    return await billing_service.get_payment_status(db, client, user, payment_id)


@router.post("/grants/lookup", response_model=AdminUserPlanResponse)
async def lookup_plan(
    payload: PlanLookupRequest, db: DbSession, _: AdminUser
) -> AdminUserPlanResponse:
    """Админ: хэрэглэгчийн багц ба гараар хийсэн сүүлийн өөрчлөлтүүд."""
    return await billing_service.user_plan(db, payload.email)


@router.post("/grants", response_model=AdminUserPlanResponse)
async def adjust_plan(
    payload: PlanGrantRequest, db: DbSession, admin: AdminUser
) -> AdminUserPlanResponse:
    """Админ: хэрэглэгчийн багцыг гараар нэмнэ (`months` > 0) эсвэл хасна (< 0).

    Өөрчлөлт бүр хэн, хэзээ хийснээр `plan_adjustments`-д үлдэнэ.
    """
    return await billing_service.adjust_plan(db, admin, payload.email, payload.months, payload.note)


@router.get("/price", response_model=PlanPriceResponse)
async def get_price(db: DbSession, _: AdminUser) -> PlanPriceResponse:
    """Админ: одоогийн сарын үнэ, хэн хэзээ өөрчилсөн."""
    return await billing_service.price_info(db)


@router.put("/price", response_model=PlanPriceResponse)
async def set_price(payload: PlanPriceUpdate, db: DbSession, admin: AdminUser) -> PlanPriceResponse:
    """Админ: Standard эсвэл Premium багцын сарын үнэ. Олон сарын үнэ дагаж шинэчлэгдэнэ."""
    return await billing_service.set_monthly_price(
        db, admin, payload.price_mnt, BillingPlan(payload.plan)
    )


@router.get("/promo-codes", response_model=list[PromoCodeItem])
async def list_promo_codes(db: DbSession, _: AdminUser) -> list[PromoCodeItem]:
    """Админ: бүх промо код, ашигласан тоотой. Шинэ нь эхэндээ."""
    return await promo_service.list_codes(db)


@router.post("/promo-codes", response_model=PromoCodeItem, status_code=201)
async def create_promo_code(
    payload: PromoCodeCreate, db: DbSession, admin: AdminUser
) -> PromoCodeItem:
    """Админ: хувийн хөнгөлөлттэй эсвэл үнэгүй сарын код үүсгэнэ."""
    return await promo_service.create_code(db, admin, payload)


@router.patch("/promo-codes/{code_id}", response_model=PromoCodeItem)
async def update_promo_code(
    code_id: uuid.UUID, payload: PromoCodeUpdate, db: DbSession, _: AdminUser
) -> PromoCodeItem:
    """Админ: идэвхтэй эсэх, дуусах хугацаа, ашиглах дээд тоог өөрчилнө."""
    return await promo_service.update_code(db, code_id, payload)


@router.post("/webhooks/wire", response_model=MessageResponse)
async def wire_webhook(request: Request, db: DbSession, client: WireClient) -> MessageResponse:
    """Wire-ийн event. Нэвтрэлтгүй — гарын үсгээр баталгаажна."""
    await billing_service.handle_webhook(
        db, client, await request.body(), request.headers.get(SIGNATURE_HEADER)
    )
    return MessageResponse(message="ok")
