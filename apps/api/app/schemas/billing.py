import uuid
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, EmailStr, Field, field_validator

from app.core.config import settings


class PlanOption(BaseModel):
    """Нэг удаад авах хугацаа ба түүний нийт үнэ."""

    months: int
    free_months: int
    # Нийт дүн, бүхэл төгрөг — үнэгүй сарыг тооцсон, хөнгөлөлтгүй.
    price_mnt: int
    # Бодитоор төлөх дүн — хөнгөлөлт (`PlanResponse.discount`) ба нэг удаагийн эрхийн
    # үнэ (`PlanResponse.upgrade_credit`) байвал хасагдсан.
    final_price_mnt: int
    # Үүний нэг удаагийн эрхийн үнээс хасагдах хэсэг.
    credit_mnt: int = 0


class PlanDiscount(BaseModel):
    """Checkout-д орох хөнгөлөлт. Нэг төлбөрт нэг л хөнгөлөлт."""

    # `promo` — оруулсан промо код; `referral` — найзын урилгаар бүртгүүлсний хөнгөлөлт.
    source: Literal["promo", "referral"]
    percent_off: int
    # Промо кодын үед код, урилгын үед `None`.
    code: str | None = None


class UpgradeCredit(BaseModel):
    """Нэг удаагийн эрх авснаас хойш `live_pass_upgrade_days` хоногийн дотор
    Standard/Premium авбал эрхийн үнэ хасагдана. Үнэ (`options`) аль хэдийн тусгасан."""

    amount_mnt: int
    expires_at: datetime


class PlanResponse(BaseModel):
    has_plan: bool
    plan_expires_at: datetime | None
    # Сарын үнэ, бүхэл төгрөг (minor unit биш) — UI-д шууд харуулна.
    price_mnt: int
    # 1–12 сар, тус бүрийн үнэ. Хямдралын дүрмийг UI давтахгүй — эндээс уншина.
    options: list[PlanOption]
    # Промо код оруулаагүй бол дараагийн төлбөрт автоматаар орох урилгын
    # хөнгөлөлт — урилгын кодоор бүртгүүлсэн, хараахан ашиглаагүй хэрэглэгчид.
    discount: PlanDiscount | None = None
    # Premium = Standard + Live-ийн илүү AI. Live бүх хэрэглэгчид нээлттэй (эсвэл
    # хэрэглэгч админ) үед л зарна — `false` бол вэб Premium-ийг харуулахгүй.
    premium_available: bool = False
    premium_price_mnt: int = 0
    premium_options: list[PlanOption] = []
    has_premium: bool = False
    premium_expires_at: datetime | None = None
    # Premium нь Standard-аас Live-д хэд дахин их хэрэглээтэй («3 дахин»). Материалын
    # тоог хэрэглэгчид харуулахгүй — зөвхөн харьцааг (`/pricing` тохиргоог давтахгүй).
    premium_usage_multiplier: int = Field(
        default_factory=lambda: max(
            1,
            round(
                settings.live_premium_documents_per_month
                / max(1, settings.live_standard_documents_per_month)
            ),
        )
    )
    # Нэг удаагийн Live эрх — нэг материал. Premium шиг Live бүгдэд нээлттэй (эсвэл
    # админ) үед л зарна. Багцтай эсвэл ашиглаагүй эрхтэй хэрэглэгч дахин авахгүй.
    live_pass_available: bool = False
    live_pass_price_mnt: int = 0
    has_unused_live_pass: bool = False
    upgrade_credit: UpgradeCredit | None = None
    # Нөхцөлийг вэб давтахгүй: ашигласнаас хойш хэдэн хоног, хэдэн хоногт хасагдах.
    live_pass_access_days: int = Field(default_factory=lambda: settings.live_pass_access_days)
    live_pass_upgrade_days: int = Field(default_factory=lambda: settings.live_pass_upgrade_days)


class CheckoutRequest(BaseModel):
    # `live_pass`-д тоолохгүй — нэг эрх.
    months: int = Field(default=1, ge=1, le=settings.plan_max_months)
    plan: Literal["standard", "premium", "live_pass"] = "standard"
    # Хувийн хөнгөлөлттэй промо код. Оруулбал урилгын хөнгөлөлт энэ удаа орохгүй
    # (нийлж 30% болохгүй; урилгын хөнгөлөлт дараагийн төлбөрт хадгалагдана).
    promo_code: str | None = Field(default=None, max_length=64)

    @field_validator("promo_code")
    @classmethod
    def blank_code_is_none(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return value.strip() or None


class CheckoutResponse(BaseModel):
    payment_id: uuid.UUID
    # `pay.wire.mn/c/…` — хөтөч энэ хаяг руу шилжинэ.
    checkout_url: str


class PaymentReceipt(BaseModel):
    """Амжилттай төлбөр эсвэл үнэгүй сарын промо кодын баримт — `/billing/success`
    хуудас хэвлэж харуулна."""

    # `payment` — Wire-ээр төлсөн; `promo` — үнэгүй сарын промо код (0₮).
    kind: Literal["payment", "promo"] = "payment"
    plan: Literal["standard", "premium", "live_pass"] = "standard"
    # Нэг удаагийн эрхэд 0.
    months: int
    # `months`-ийн хэд нь үнэгүй (6 сар тутамд 1).
    free_months: int
    # Хөнгөлөлтийн өмнөх дүн = `amount_mnt` + `discount_mnt` + `credit_mnt`. Бүхэл төгрөг.
    list_price_mnt: int
    discount_percent: int
    discount_mnt: int
    # Нэг удаагийн эрхийн үнээс хасагдсан дүн (эрх авснаас хойш хэдэн хоногт багц авсан).
    credit_mnt: int = 0
    # `promo` — промо код, `referral` — урилгаар бүртгүүлсний хөнгөлөлт, эс бөгөөс `None`.
    discount_source: Literal["promo", "referral"] | None
    promo_code: str | None
    # Бодитоор төлсөн дүн.
    amount_mnt: int
    currency: str
    # Wire-ийн гүйлгээний дугаар (`pi_…`) — дэмжлэгт хандахад хэрэгтэй.
    reference: str | None
    created_at: datetime
    paid_at: datetime | None


class PaymentStatusResponse(BaseModel):
    id: uuid.UUID
    status: str
    plan: PlanResponse
    # Зөвхөн `succeeded` үед.
    receipt: PaymentReceipt | None = None


class PromoRedeemResponse(PlanResponse):
    """Үнэгүй сарын кодыг идэвхжүүлсний дараах багц — баримтын хуудас руу шилжихэд
    `redemption_id` хэрэгтэй."""

    redemption_id: uuid.UUID


class RedemptionReceiptResponse(BaseModel):
    """Үнэгүй сарын промо кодын баримт (`/billing/success?redemption=…`)."""

    id: uuid.UUID
    plan: PlanResponse
    receipt: PaymentReceipt


class PlanLookupRequest(BaseModel):
    """Админ хэрэглэгчийн багцыг имэйлээр хайна. Имэйл URL-д (логт) орохгүйн
    тулд body-гоор ирнэ."""

    email: EmailStr = Field(max_length=255)

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        return value.strip().lower()


class PlanGrantRequest(PlanLookupRequest):
    """Админ гараар багц нэмэх (эерэг) эсвэл хасах (сөрөг) — дэмжлэг, туршилтын
    данс, төлбөрийн засвар."""

    months: int = Field(
        default=1, ge=-settings.plan_max_grant_months, le=settings.plan_max_grant_months
    )
    note: str | None = Field(default=None, max_length=500)

    @field_validator("months")
    @classmethod
    def not_zero(cls, value: int) -> int:
        if value == 0:
            raise ValueError("Сарын тоо 0 байж болохгүй.")
        return value

    @field_validator("note")
    @classmethod
    def blank_note_is_none(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return value.strip() or None


class PlanAdjustmentItem(BaseModel):
    """Гараар хийсэн нэг өөрчлөлт."""

    id: uuid.UUID
    months: int
    expires_before: datetime | None
    expires_after: datetime
    note: str | None
    # Админы нэр. Бүртгэл нь устсан бол `None`.
    admin_name: str | None
    created_at: datetime


class AdminUserPlanResponse(BaseModel):
    """Админд: хэрэглэгчийн багц ба гараар хийсэн сүүлийн өөрчлөлтүүд."""

    user_id: uuid.UUID
    name: str
    email: str
    has_plan: bool
    plan_expires_at: datetime | None
    # Шинэ нь эхэндээ, хамгийн ихдээ `PLAN_ADJUSTMENT_HISTORY` мөр.
    adjustments: list[PlanAdjustmentItem]


class PlanPriceResponse(BaseModel):
    """Админд: одоогийн сарын үнэ ба түүнийг хэн, хэзээ тавьсан. `premium_*` — Premium-ийнх."""

    price_mnt: int
    # Админ хэзээ ч өөрчлөөгүй бол ашиглагдах `PLAN_PRICE_MNT`.
    default_price_mnt: int
    # Анхдагч үнэ хэрэглэгдэж байвал `None`.
    changed_at: datetime | None
    changed_by: str | None
    premium_price_mnt: int
    premium_default_price_mnt: int
    premium_changed_at: datetime | None
    premium_changed_by: str | None
    # Нэг удаагийн Live эрхийн үнэ (сарынх биш).
    live_pass_price_mnt: int
    live_pass_default_price_mnt: int
    live_pass_changed_at: datetime | None
    live_pass_changed_by: str | None


class PlanPriceUpdate(BaseModel):
    """Сарын үнэ (`live_pass`-д нэг эрхийн үнэ), бүхэл төгрөг. Олон сарын үнэ, үнэгүй
    сарыг сервер тооцно."""

    price_mnt: int = Field(ge=100, le=1_000_000)
    plan: Literal["standard", "premium", "live_pass"] = "standard"
