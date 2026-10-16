import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    true,
)
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, CreatedAtMixin, UUIDPrimaryKeyMixin
from app.models.enums import PromoKind, values


class PromoCode(UUIDPrimaryKeyMixin, CreatedAtMixin, Base):
    """Админы үүсгэсэн промо код (`/admin/promo`).

    Хоёр төрөл:
    - `percent` — төлбөрөөс `percent_off` хувь хасна (олон сарын үнэгүй сарын
      дараах нийт дүнгээс). Checkout дээр оруулна.
    - `free_months` — төлбөргүйгээр багцыг `free_months` сараар сунгана
      (`POST /billing/promo/redeem`).

    Хэрэглэгч нэг кодыг нэг л удаа ашиглана (`promo_redemptions`). Төрөл,
    хэмжээг үүсгэсний дараа солихгүй — төлбөрүүд түүнд холбогддог. Хугацаа,
    ашиглах дээд тоо, идэвхтэй эсэхийг админ өөрчилнө.
    """

    __tablename__ = "promo_codes"
    __table_args__ = (
        CheckConstraint(
            "kind IN ('" + "','".join(values(PromoKind)) + "')",
            name="kind_valid",
        ),
        CheckConstraint(
            "(kind = 'percent' AND percent_off BETWEEN 1 AND 99 AND free_months IS NULL)"
            " OR (kind = 'free_months' AND free_months >= 1 AND percent_off IS NULL)",
            name="value_matches_kind",
        ),
        CheckConstraint("max_uses IS NULL OR max_uses >= 1", name="max_uses_positive"),
    )

    # Том латин үсэг, тоо (`HELLOWORLD2026`). Хэрэглэгчийн оруулсныг томруулж хайна.
    code: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    kind: Mapped[str] = mapped_column(String(20), nullable=False)
    percent_off: Mapped[int | None] = mapped_column(Integer, nullable=True)
    free_months: Mapped[int | None] = mapped_column(Integer, nullable=True)
    # Энэ мөчөөс хойш хүчингүй. NULL бол хугацаагүй.
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    # Нийт хэдэн хэрэглэгч ашиглаж болох вэ. NULL бол хязгааргүй.
    max_uses: Mapped[int | None] = mapped_column(Integer, nullable=True)
    # Админ хугацаанаас нь өмнө зогсоож болно (код задарсан гэх мэт).
    active: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default=true(), nullable=False
    )
    # Админд зориулсан тэмдэглэл — хэрэглэгчид харагдахгүй.
    note: Mapped[str | None] = mapped_column(String(500), nullable=True)
    # Үүсгэсэн админ. Бүртгэл нь устсан ч код үлдэнэ.
    created_by: Mapped[uuid.UUID | None] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )


class PromoRedemption(UUIDPrimaryKeyMixin, CreatedAtMixin, Base):
    """Хэрэглэгч промо кодыг ашигласан нэг удаа.

    Хувийн хөнгөлөлттэй код — төлбөр амжилттай болох үед (`payment_id`).
    Үнэгүй сарын код — идэвхжүүлэх үед (`months`). Хэрэглэгч × код давтагдахгүй.
    """

    __tablename__ = "promo_redemptions"
    __table_args__ = (
        UniqueConstraint("promo_code_id", "user_id", name="uq_promo_redemptions_code_user"),
    )

    promo_code_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("promo_codes.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    # Бүртгэл устахад NULL — хувийн мэдээлэл үлдэхгүй, ашигласан тоо хэвээр.
    user_id: Mapped[uuid.UUID | None] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    # Хувийн кодоор хийсэн төлбөр. Хадгалах хугацаа дуусч устахад NULL.
    payment_id: Mapped[uuid.UUID | None] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("payments.id", ondelete="SET NULL"),
        nullable=True,
    )
    # Үнэгүй сарын кодоор олгосон сар.
    months: Mapped[int | None] = mapped_column(Integer, nullable=True)
