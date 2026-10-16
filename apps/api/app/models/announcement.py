import uuid
from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, DateTime, ForeignKey, String, Text, false
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import AnnouncementAudience, AnnouncementKind, values


class Announcement(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Админы бичсэн зарлал — сайт дээр цонх (popup) болж гарна (`/admin/announcements`).

    Шинэчлэл мэдээлэх, боломж онцлох зорилготой. `active` (нийтэлсэн), хугацаа
    (`starts_at` … `ends_at`), хүрэх хүрээ (`audience`) тохирсон хэрэглэгчид
    харагдана. Хэрэглэгч хаасныг зөвхөн хөтөч санана — сервер хэн харсныг
    хадгалахгүй.
    """

    __tablename__ = "announcements"
    __table_args__ = (
        CheckConstraint(
            "kind IN ('" + "','".join(values(AnnouncementKind)) + "')", name="kind_valid"
        ),
        CheckConstraint(
            "audience IN ('" + "','".join(values(AnnouncementAudience)) + "')",
            name="audience_valid",
        ),
        CheckConstraint("(cta_label IS NULL) = (cta_url IS NULL)", name="cta_complete"),
        CheckConstraint(
            "starts_at IS NULL OR ends_at IS NULL OR ends_at > starts_at", name="period_valid"
        ),
    )

    kind: Mapped[str] = mapped_column(String(20), nullable=False)
    title: Mapped[str] = mapped_column(String(120), nullable=False)
    # Markdown — Community-ийнх шиг HTML, зураггүй харуулна.
    body: Mapped[str] = mapped_column(Text, nullable=False)
    # Заавал биш товч: дотоод хаяг (`/pricing`) эсвэл `https://…`.
    cta_label: Mapped[str | None] = mapped_column(String(40), nullable=True)
    cta_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    audience: Mapped[str] = mapped_column(String(20), nullable=False)
    # NULL бол нийтэлмэгц эхэлнэ / хугацаагүй.
    starts_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    ends_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    # `false` бол ноорог — хэнд ч харагдахгүй.
    active: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default=false(), nullable=False
    )
    # Бичсэн админ. Бүртгэл нь устсан ч зарлал үлдэнэ.
    created_by: Mapped[uuid.UUID | None] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
