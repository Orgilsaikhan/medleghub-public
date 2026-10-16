import uuid
from typing import TYPE_CHECKING, Any

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    false,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, UUIDPrimaryKeyMixin
from app.models.enums import LessonLanguage, values

if TYPE_CHECKING:
    from app.models.module import Module
    from app.models.progress import LessonProgress


class Lesson(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "lessons"
    __table_args__ = (
        # Slug нь course дотор давхардахгүй байх ёстой. DB нь module хүртэл
        # баталгаажуулж, course-ийн түвшний давхардлыг service давхарга шалгана.
        UniqueConstraint("module_id", "slug", name="uq_lessons_module_id_slug"),
        CheckConstraint(
            "language IN ('" + "','".join(values(LessonLanguage)) + "')",
            name="language_valid",
        ),
        CheckConstraint("duration >= 0", name="duration_non_negative"),
        Index("ix_lessons_module_position", "module_id", "position"),
    )

    module_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("modules.id", ondelete="CASCADE"),
        nullable=False,
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    slug: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, default="", nullable=False)
    video_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    duration: Mapped[int] = mapped_column(Integer, default=0, nullable=False)  # секунд
    content: Mapped[str] = mapped_column(Text, default="", nullable=False)  # Markdown
    initial_code: Mapped[str] = mapped_column(Text, default="", nullable=False)
    language: Mapped[str] = mapped_column(
        String(20), default=LessonLanguage.JAVASCRIPT, nullable=False
    )
    position: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    published: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    # Бусдаасаа хэцүү хичээл — «Заавар» хэсэгт шар «Хэцүү» шошготой.
    challenging: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default=false(), nullable=False
    )
    # Дасгал: `{"statement", "tests": [{"stdin", "expected_output", "sample"}],
    # "tips", "solution"}`. Тестүүд хичээлтэйгээ үргэлж хамт уншигдаж бичигддэг
    # тул тусдаа хүснэгт биш. `tips`, `solution` нь хичээлийн хариунд ОРОХГҮЙ —
    # зөвхөн `GET /lessons/{id}/help`.
    exercise: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)

    module: Mapped["Module"] = relationship(back_populates="lessons")
    progress: Mapped[list["LessonProgress"]] = relationship(
        back_populates="lesson", cascade="all, delete-orphan"
    )
