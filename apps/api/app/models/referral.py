import uuid
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, CreatedAtMixin, UUIDPrimaryKeyMixin


class Referral(UUIDPrimaryKeyMixin, CreatedAtMixin, Base):
    """Нэг хэрэглэгч (`referrer`) урилгын кодоороо нэг найзаа бүртгүүлсэн нь.

    - Найз (шинэ хэрэглэгч) нэг удаагийн `REFERRAL_FRIEND_PERCENT_OFF` хувийн
      хөнгөлөлт авна. Промо код оруулаагүй төлбөрт автоматаар орж, төлбөр
      амжилттай болоход `discount_used_at` тэмдэглэнэ. Промо код хэрэглэвэл
      хөнгөлөлт нийлэхгүй — урилгын хөнгөлөлт дараагийн төлбөрт хадгалагдана.
    - Урьсан хүн хөнгөлөлт авахгүй. Түүний урьсан найзуудаас
      `REFERRAL_FRIENDS_PER_REWARD` нь багц авах бүрд `REFERRAL_REWARD_MONTHS`
      сар үнэгүй. Найз анх амжилттай төлөхөд `first_paid_at` тавигдана;
      шагнал олгосон төлбөрийн найзын мөрөнд `months_rewarded` нэмэгдэнэ.

    Тоолуурыг `payments`-аас дахин тооцохгүй — төлбөрийн бүртгэл 1 жилийн
    дараа устдаг (`payment_retention_days`).
    """

    __tablename__ = "referrals"
    __table_args__ = (CheckConstraint("months_rewarded >= 0", name="months_rewarded_nonnegative"),)

    # Урьсан хүний бүртгэл устахад мөр хамт устана.
    referrer_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    # Найз нэг л удаа, бүртгүүлэхдээ урилгын код оруулна. Бүртгэл нь устахад
    # NULL — урьсан хүний тоо, олсон сар хэвээр, найзын мэдээлэл үлдэхгүй.
    friend_id: Mapped[uuid.UUID | None] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        unique=True,
        nullable=True,
    )
    # Найз имэйлээ баталгаажуулсан мөч — урьсан хүний «Урьсан найз» тоонд орно.
    signup_confirmed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    # Найзын хөнгөлөлт орсон төлбөр нь `payments.referral_id`-аар холбогдоно.
    discount_used_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    # Найзын анхны амжилттай төлбөр — «багц авсан найз» болж тоологдоно.
    first_paid_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    months_rewarded: Mapped[int] = mapped_column(
        Integer, default=0, server_default="0", nullable=False
    )
