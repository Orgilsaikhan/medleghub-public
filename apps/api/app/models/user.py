from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, CheckConstraint, DateTime, String, false, text, true
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, CreatedAtMixin, UUIDPrimaryKeyMixin
from app.models.enums import EditorLayout, UserRole, values

if TYPE_CHECKING:
    from app.models.badge import UserBadge
    from app.models.enrollment import Enrollment
    from app.models.payment import Payment
    from app.models.progress import LessonProgress


_EPOCH = datetime(1970, 1, 1, tzinfo=UTC)


class User(UUIDPrimaryKeyMixin, CreatedAtMixin, Base):
    __tablename__ = "users"
    __table_args__ = (
        CheckConstraint(
            "role IN ('" + "','".join(values(UserRole)) + "')",
            name="role_valid",
        ),
        CheckConstraint(
            "editor_layout IN ('" + "','".join(values(EditorLayout)) + "')",
            name="editor_layout_valid",
        ),
    )

    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    role: Mapped[str] = mapped_column(String(20), default=UserRole.STUDENT, nullable=False)
    # Standard багц хүчинтэй хугацаа. NULL эсвэл өнгөрсөн бол үнэгүй хэрэглэгч.
    # Төлбөр бүр үүнийг нэг сараар сунгана (`billing_service.apply_payment`).
    plan_expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    # Нууц үг сольсон мөч. Token бүр олгох үеийн хувилбарыг (`password_version`)
    # агуулна — таарахгүй бол хүчингүй, бусад төхөөрөмжийн сесс гарна.
    password_changed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    # Профайлын зургийн агуулгын hash. Зургийн URL-ийн хувилбар болж, хөтөч
    # түүнийг мөнхөд кэшлэнэ. Зураг өөрөө `user_avatars` хүснэгтэд.
    avatar_key: Mapped[str | None] = mapped_column(String(32), nullable=True)
    # Имэйлд илгээсэн кодыг оруулсан мөч. NULL бол нэвтэрч чадахгүй (имэйл
    # баталгаажуулалт асаалттай үед). Энэ боломжоос өмнөх бүртгэлд `created_at`.
    email_verified_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    # Имэйл солих хүсэлт — нууц үгээ шалгуулсны дараа шинэ хаяг руу код
    # илгээнэ. Кодыг зөвхөн энэ хаягт хүлээж авна.
    pending_email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    # Дасгалын тестэд 3 удаа дараалан унавал урам өгөх үг харуулах эсэх.
    show_motivation: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default=true(), nullable=False
    )
    # Хичээлийн засварлагчийн байрлал: `new` — засварлагч зүүн, заавар баруун
    # (React хичээлийнх шиг); `legacy` — заавар дээр, засварлагч доор.
    editor_layout: Mapped[str] = mapped_column(
        String(10), default=EditorLayout.NEW, server_default=text("'new'"), nullable=False
    )
    # Бусад суралцагчийн жагсаалт, нийтийн профайлаас нуух.
    profile_hidden: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default=false(), nullable=False
    )
    # Бүртгүүлэхдээ Үйлчилгээний нөхцөл, Нууцлалын бодлогыг зөвшөөрсөн мөч.
    terms_accepted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    # 2026-09-28-аас өмнө 14–15 насныхан эцэг эхийн зөвшөөрлөөр бүртгүүлж болдог
    # байсан үеийн тэмдэглэгээ. Одоо 16 хүрээгүй бол бүртгүүлэхгүй тул шинэ
    # хэрэглэгчид үргэлж NULL — хуучин мөрийн түүхэнд л үлдсэн.
    guardian_consent_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    # Community-ийн дүрмийг уншиж зөвшөөрсөн мөч. NULL бол Community-д бичих,
    # лайк дарах, мэдэгдэх боломжгүй — эхний удаа ороход дүрэм харуулна.
    community_guidelines_accepted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    # Найзаа урих код (`/register?ref=…`). Анх `/me/referral` нээхэд үүснэ.
    referral_code: Mapped[str | None] = mapped_column(String(16), unique=True, nullable=True)
    # Бүртгэл устгах хүсэлтийн хугацаа дуусах мөч — хүсэлтээс яг 2 цагийн дараа
    # `maintenance` ажил бүрмөсөн устгана. Тэр хүртэл хэрэглэгч цуцалж болно.
    deletion_scheduled_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    enrollments: Mapped[list["Enrollment"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    lesson_progress: Mapped[list["LessonProgress"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    badges: Mapped[list["UserBadge"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    # Бүртгэл устахад төлбөрийн бүртгэл үлдэнэ (санхүү, татварын шаардлага) —
    # `payments.user_id` нь `ON DELETE SET NULL`.
    payments: Mapped[list["Payment"]] = relationship(back_populates="user", passive_deletes=True)

    @property
    def is_admin(self) -> bool:
        return self.role == UserRole.ADMIN

    @property
    def password_version(self) -> int:
        """Нууц үгийн хувилбар — солисон мөч микросекундээр (float-гүй, яг)."""
        if self.password_changed_at is None:
            return 0
        return (self.password_changed_at - _EPOCH) // timedelta(microseconds=1)

    @property
    def has_plan(self) -> bool:
        """Төлбөрт хичээлүүдийг үзэх эрхтэй эсэх. Админ үргэлж эрхтэй."""
        if self.is_admin:
            return True
        return self.plan_expires_at is not None and self.plan_expires_at > datetime.now(UTC)
