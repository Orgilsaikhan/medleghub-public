import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, CheckConstraint, ForeignKey, String, Text, false
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, CreatedAtMixin, UUIDPrimaryKeyMixin
from app.models.enums import FeedbackKind, values

if TYPE_CHECKING:
    from app.models.user import User


class Feedback(UUIDPrimaryKeyMixin, CreatedAtMixin, Base):
    """Хэрэглэгчийн санал хүсэлт — админ `/admin/feedback` дээр уншиж шийднэ."""

    __tablename__ = "feedback"
    __table_args__ = (
        CheckConstraint(
            "kind IN ('" + "','".join(values(FeedbackKind)) + "')",
            name="kind_valid",
        ),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    kind: Mapped[str] = mapped_column(String(20), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    # Илгээх үед хэрэглэгч аль хуудсанд байсан — алдааг давтахад хэрэгтэй.
    page: Mapped[str | None] = mapped_column(String(300), nullable=True)
    resolved: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default=false(), nullable=False
    )

    user: Mapped["User"] = relationship()
