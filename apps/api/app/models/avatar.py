import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, LargeBinary, func
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class UserAvatar(Base):
    """Профайлын зураг — 256×256 WebP (~10–20 KB).

    `users` хүснэгтээс тусад нь: хэрэглэгчийг ачаалах бүрт зургийн байт
    уншигдахгүй. Серверт ИРСЭН файлыг хэзээ ч шууд хадгалахгүй — дахин
    кодлосон WebP л энд орно (`avatar_service.normalize`).
    """

    __tablename__ = "user_avatars"

    user_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    data: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
