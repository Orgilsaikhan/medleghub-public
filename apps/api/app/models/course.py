from typing import TYPE_CHECKING

from sqlalchemy import Boolean, CheckConstraint, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import Category, Difficulty, values

if TYPE_CHECKING:
    from app.models.enrollment import Enrollment
    from app.models.module import Module


class Course(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "courses"
    __table_args__ = (
        CheckConstraint(
            "difficulty IN ('" + "','".join(values(Difficulty)) + "')",
            name="difficulty_valid",
        ),
        CheckConstraint(
            "category IN ('" + "','".join(values(Category)) + "')",
            name="category_valid",
        ),
        CheckConstraint("free_lessons >= 0", name="free_lessons_non_negative"),
        # Catalog-ийн үндсэн filter query-г хурдасгана.
        Index("ix_courses_catalog", "published", "category", "difficulty"),
    )

    title: Mapped[str] = mapped_column(String(200), nullable=False)
    slug: Mapped[str] = mapped_column(String(200), unique=True, index=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, default="", nullable=False)
    thumbnail_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    difficulty: Mapped[str] = mapped_column(String(20), nullable=False)
    category: Mapped[str] = mapped_column(String(30), nullable=False)
    is_free: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    # `is_free=False` үед эхний хэдэн хичээл нь бүгдэд нээлттэй вэ. Үлдсэнийг
    # нь зөвхөн идэвхтэй багцтай хэрэглэгч үзнэ (`app/services/access.py`).
    free_lessons: Mapped[int] = mapped_column(
        Integer, default=0, server_default="0", nullable=False
    )
    published: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    modules: Mapped[list["Module"]] = relationship(
        back_populates="course",
        cascade="all, delete-orphan",
        order_by="Module.position",
    )
    enrollments: Mapped[list["Enrollment"]] = relationship(
        back_populates="course", cascade="all, delete-orphan"
    )
