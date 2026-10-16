import uuid
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, CreatedAtMixin, UUIDPrimaryKeyMixin


class PlanAdjustment(UUIDPrimaryKeyMixin, CreatedAtMixin, Base):
    """Админ хэрэглэгчийн багцыг гараар нэмсэн, хассан түүх (`/admin/billing`).

    Мөрийг засахгүй, шинээр нэмнэ — хэн, хэзээ, хэдэн сар, өмнө нь болон
    дараа нь хэзээ дуусах байсныг хадгална. Төлбөрөөр сунгасныг `payments`
    хадгалдаг тул энд орохгүй.
    """

    __tablename__ = "plan_adjustments"
    __table_args__ = (CheckConstraint("months <> 0", name="months_nonzero"),)

    # Бүртгэл нь устахад түүх нь хамт устана — хувийн мэдээлэл үлдээхгүй.
    user_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    # Өөрчилсөн админ. Бүртгэл нь устсан ч түүх үлдэнэ.
    admin_id: Mapped[uuid.UUID | None] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    # Эерэг бол нэмсэн, сөрөг бол хассан сар.
    months: Mapped[int] = mapped_column(Integer, nullable=False)
    expires_before: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    expires_after: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    # Яагаад өөрчилснийг админ тэмдэглэнэ (заавал биш).
    note: Mapped[str | None] = mapped_column(String(500), nullable=True)
