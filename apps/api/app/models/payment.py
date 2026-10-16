import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, String, text
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, CreatedAtMixin, UUIDPrimaryKeyMixin
from app.models.enums import BillingPlan, PaymentStatus, values

if TYPE_CHECKING:
    from app.models.user import User


class Payment(UUIDPrimaryKeyMixin, CreatedAtMixin, Base):
    """Standard, Premium багц эсвэл нэг удаагийн Live эрхийн төлбөр (`plan`).

    Мөрийг Wire-ийн PaymentIntent үүсгэхээс ӨМНӨ бичнэ — мөрийн `id` нь
    Wire-д илгээх `Idempotency-Key` болно. Ингэснээр дахин оролдлого давхар
    нэхэмжлэх үүсгэхгүй.

    `status` нь `pending`-ээс `succeeded` руу ЗӨВХӨН НЭГ удаа шилжинэ — багцыг
    сунгах нь тэр шилжилттэй нэг транзакцид явагдана (`billing_service`).
    Webhook болон буцах хуудас зэрэг ирсэн ч сар давхар нэмэгдэхгүй.
    """

    __tablename__ = "payments"
    __table_args__ = (
        CheckConstraint(
            "status IN ('" + "','".join(values(PaymentStatus)) + "')",
            name="status_valid",
        ),
        # Нэг удаагийн эрх багцыг сунгахгүй (0 сар); багц дор хаяж 1 сар.
        CheckConstraint(
            f"CASE WHEN plan = '{BillingPlan.LIVE_PASS}' THEN months = 0 ELSE months >= 1 END",
            name="months_valid",
        ),
        CheckConstraint("plan IN ('" + "','".join(values(BillingPlan)) + "')", name="plan_valid"),
        CheckConstraint("discount_percent BETWEEN 0 AND 99", name="discount_percent_valid"),
        CheckConstraint("discount_mnt >= 0", name="discount_mnt_nonnegative"),
        CheckConstraint("credit_mnt >= 0", name="credit_mnt_nonnegative"),
    )

    # Бүртгэл устахад NULL болно — төлбөрийн бүртгэл хуулийн хугацаанд үлдэнэ.
    user_id: Mapped[uuid.UUID | None] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    provider: Mapped[str] = mapped_column(String(20), default="wire", nullable=False)
    # Wire-ийн PaymentIntent (`pi_…`). Wire руу хүсэлт амжилттай болтол NULL.
    provider_payment_id: Mapped[str | None] = mapped_column(String(100), unique=True, nullable=True)
    # Бүхэл төгрөг, Wire-д илгээсэнтэй ижил: 24_900 = 24,900₮. 2026-09-28-аас
    # өмнөх (туршилтын) мөрүүд ×100 байсан.
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="MNT", nullable=False)
    status: Mapped[str] = mapped_column(String(20), default=PaymentStatus.PENDING, nullable=False)
    # Энэ төлбөр багцыг хэдэн сараар сунгах вэ (үнэгүй сарыг оруулаад). Нэг удаагийн
    # эрхэд 0.
    months: Mapped[int] = mapped_column(Integer, default=1, server_default="1", nullable=False)
    # `premium` — Standard-ийг `months` сараар сунгахаас гадна Premium-ийг (`live_subscriptions`)
    # мөн сараар сунгана. `live_pass` — нэг удаагийн Live эрх үүсгэнэ (`live_pass_id`).
    plan: Mapped[str] = mapped_column(
        String(10), default=BillingPlan.STANDARD, server_default=text("'standard'"), nullable=False
    )
    # Хөнгөлөлт: `amount` = олон сарын үнэ − `discount_mnt` − `credit_mnt`. Нэг төлбөрт нэг л
    # хөнгөлөлт — оруулсан промо код, эс бөгөөс урилгаар бүртгүүлсний хөнгөлөлт.
    discount_percent: Mapped[int] = mapped_column(
        Integer, default=0, server_default="0", nullable=False
    )
    discount_mnt: Mapped[int] = mapped_column(
        Integer, default=0, server_default="0", nullable=False
    )
    # Амжилттай болоход `promo_redemptions`-д бичигдэнэ. Код устахгүй ч NULL
    # болж болохоор.
    promo_code_id: Mapped[uuid.UUID | None] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("promo_codes.id", ondelete="SET NULL"),
        nullable=True,
    )
    # Урилгаар бүртгүүлсэн хэрэглэгчийн хөнгөлөлт — амжилттай болоход тэр мөрийн
    # `discount_used_at` тавигдана.
    referral_id: Mapped[uuid.UUID | None] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("referrals.id", ondelete="SET NULL"),
        nullable=True,
    )
    # Нэг удаагийн эрх: `live_pass` төлбөрт — үүссэн эрх; багцын төлбөрт — үнэ нь
    # хасагдсан эрх (`credit_mnt`). Хэрэглэгч устахад эрх устаж NULL болно.
    live_pass_id: Mapped[uuid.UUID | None] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("live_passes.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    # Эрх авснаас хойш `live_pass_upgrade_days` хоногт багц авахад хасагдсан эрхийн
    # үнэ: `amount` = олон сарын үнэ − `discount_mnt` − `credit_mnt`.
    credit_mnt: Mapped[int] = mapped_column(Integer, default=0, server_default="0", nullable=False)
    checkout_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    paid_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    user: Mapped["User | None"] = relationship(back_populates="payments")
