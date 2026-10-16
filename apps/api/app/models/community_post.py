import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    false,
    func,
)
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, CreatedAtMixin, UUIDPrimaryKeyMixin
from app.models.enums import PostLanguage, PostType, values

if TYPE_CHECKING:
    from app.models.user import User


class CommunityPost(UUIDPrimaryKeyMixin, CreatedAtMixin, Base):
    """Community хэсгийн нийтлэл — асуулт, хэлэлцүүлэг, сонирхолтой баримт.

    `author_id` NULL бол MedlegHub-ийн нэрийн өмнөөс нийтэлсэн албан ёсны
    нийтлэл (`app/content/community.py`, seed-ээр орно). Хэрэглэгчийн бүртгэл
    устахад нийтлэл нь сэтгэгдэл, лайктайгаа хамт устана.
    """

    __tablename__ = "community_posts"
    __table_args__ = (
        CheckConstraint(
            "language IN ('" + "','".join(values(PostLanguage)) + "')",
            name="language_valid",
        ),
        CheckConstraint(
            "type IN ('" + "','".join(values(PostType)) + "')",
            name="type_valid",
        ),
    )

    author_id: Mapped[uuid.UUID | None] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=True,
    )
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    # Markdown. Вэб нь HTML, зураггүйгээр харуулна — хавсралт оруулах боломжгүй.
    body: Mapped[str] = mapped_column(Text, nullable=False)
    language: Mapped[str] = mapped_column(String(20), nullable=False)
    type: Mapped[str] = mapped_column(String(20), nullable=False)
    # Жагсаалтын эхэнд байна. Зөвхөн seed тавьдаг.
    pinned: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default=false(), nullable=False
    )

    author: Mapped["User | None"] = relationship()


class CommunityComment(UUIDPrimaryKeyMixin, CreatedAtMixin, Base):
    __tablename__ = "community_comments"

    post_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("community_posts.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    author_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    body: Mapped[str] = mapped_column(Text, nullable=False)

    author: Mapped["User"] = relationship()


class CommunityPostLike(Base):
    """Хэрэглэгч нэг нийтлэлд нэг л удаа лайк дарна (нийлмэл primary key)."""

    __tablename__ = "community_post_likes"

    post_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("community_posts.id", ondelete="CASCADE"),
        primary_key=True,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class CommunitySuspension(UUIDPrimaryKeyMixin, CreatedAtMixin, Base):
    """Дүрэм зөрчсөн хэрэглэгчийн Community-д оролцох эрхийг түдгэлзүүлсэн түүх.

    Түдгэлзсэн хугацаанд зөвхөн уншина — нийтлэл, сэтгэгдэл бичих, лайк дарах,
    мэдэгдэх боломжгүй. Удаа ахих тусам хугацаа уртасна
    (`settings.community_suspension_days`), дараа нь бүрмөсөн (`ends_at` NULL).
    Админ цуцалсан (`lifted_at`) мөр дараагийн удааг тоолоход орохгүй.
    """

    __tablename__ = "community_suspensions"
    __table_args__ = (CheckConstraint("level >= 1", name="level_positive"),)

    # Бүртгэл нь устахад түүх нь хамт устана.
    user_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    # Түдгэлзүүлсэн админ. Бүртгэл нь устсан ч түүх үлдэнэ.
    admin_id: Mapped[uuid.UUID | None] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    # Хэд дэх удаагийн түдгэлзүүлэлт (цуцлагдаагүйг тоолно).
    level: Mapped[int] = mapped_column(Integer, nullable=False)
    reason: Mapped[str] = mapped_column(String(500), nullable=False)
    # NULL бол бүрмөсөн.
    ends_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    lifted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    user: Mapped["User"] = relationship(foreign_keys=[user_id])
    admin: Mapped["User | None"] = relationship(foreign_keys=[admin_id])
