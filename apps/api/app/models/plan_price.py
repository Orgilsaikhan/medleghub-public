import uuid

from sqlalchemy import CheckConstraint, ForeignKey, Index, Integer, String, text
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, CreatedAtMixin, UUIDPrimaryKeyMixin
from app.models.enums import BillingPlan, values


class PlanPrice(UUIDPrimaryKeyMixin, CreatedAtMixin, Base):
    """Багцын сарын үнийн түүх — админ `/admin/billing` дээр өөрчилнө.

    Багц (`plan`) тус бүрийн хамгийн сүүлийн мөр нь одоогийн үнэ. Мөр байхгүй бол
    `PLAN_PRICE_MNT` / `PREMIUM_PRICE_MNT` / `LIVE_PASS_PRICE_MNT` (анхдагч). `live_pass`-ийн
    үнэ нь сарынх биш — нэг эрхийнх. Мөрийг засахгүй, шинээр нэмнэ — хэн, хэзээ
    өөрчилснийг хадгална.
    """

    __tablename__ = "plan_prices"
    __table_args__ = (
        CheckConstraint("price_mnt > 0", name="price_positive"),
        CheckConstraint("plan IN ('" + "','".join(values(BillingPlan)) + "')", name="plan_valid"),
        Index("ix_plan_prices_plan_created", "plan", "created_at"),
    )

    plan: Mapped[str] = mapped_column(
        String(10), default=BillingPlan.STANDARD, server_default=text("'standard'"), nullable=False
    )

    # Сарын үнэ, бүхэл төгрөг.
    price_mnt: Mapped[int] = mapped_column(Integer, nullable=False)
    # Өөрчилсөн админ. Бүртгэл нь устсан ч түүх үлдэнэ.
    changed_by: Mapped[uuid.UUID | None] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
