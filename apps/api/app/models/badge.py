import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    SmallInteger,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.user import User

# Профайлын нэрийн хажууд онцлох авсан тэмдгийн дээд тоо (`PUT /me/showcase`).
# Орчны хувьсагчаар биш кодоор тогтооно: доорх CHECK-тэй таарах ёстой тул
# өөрчилбөл шинэ migration-аар CHECK-ийг хамт өөрчилнө. Вэбийн
# `BADGE_SHOWCASE_MAX` ч мөн адил.
SHOWCASE_MAX = 5


class UserBadge(UUIDPrimaryKeyMixin, Base):
    """Хэрэглэгчийн авсан тэмдэг.

    Тэмдгийн тодорхойлолт (нэр, нөхцөл) нь кодод — `app/content/badges.py`.
    Энд зөвхөн «хэн, аль тэмдгийг, хэзээ» гэдэг бичигдэнэ. Нэг удаа авсан
    тэмдэг хэзээ ч хасагдахгүй — агуулга өөрчлөгдсөн ч хэрэглэгч алдахгүй.
    """

    __tablename__ = "user_badges"
    __table_args__ = (
        UniqueConstraint("user_id", "badge_key", name="uq_user_badges_user_badge"),
        # Нэг байранд нэг л тэмдэг. Postgres олон NULL-ийг давхардал гэж үзэхгүй
        # тул онцлоогүй тэмдэгт хязгааргүй.
        UniqueConstraint("user_id", "showcase_position", name="uq_user_badges_showcase_position"),
        CheckConstraint(
            f"showcase_position BETWEEN 1 AND {SHOWCASE_MAX}", name="showcase_position_valid"
        ),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    badge_key: Mapped[str] = mapped_column(String(64), nullable=False)
    awarded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    # Эзний профайлд нэрийн хажууд онцлох байр (1, 2, …). NULL бол онцлоогүй.
    # `PUT /me/showcase` (`badge_service.set_showcase`) бүхэлд нь сольж бичнэ.
    showcase_position: Mapped[int | None] = mapped_column(SmallInteger, nullable=True)

    user: Mapped["User"] = relationship(back_populates="badges")
