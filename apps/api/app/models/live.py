"""MedlegHub Live (AI Study) — хэрэглэгчийн оруулсан материал ба түүнээс бүтсэн судлах хэрэгсэл.

Бүх хүснэгт `live_` угтвартай, бусад хүснэгтийг өөрчлөхгүй. Хэрэглэгч рүү
заасан FK бүр CASCADE эсвэл SET NULL — бүртгэл устгах ажил (нэг `DELETE FROM
users`) хэзээ ч гацахгүй. Материал хувийнх: зөвхөн эзэн нь хардаг.

Бүтэц:

    live_materials ─┬─ live_topics ─┬─ live_cards ── live_card_progress
                    │               └─ live_topic_progress
                    └─ live_generations ─┬─ live_questions
                                         └─ live_quiz_attempts ── live_quiz_answers

`*_progress` нь хэрэглэгч × карт/сэдэв; `live_generations` нь заавар, тест, таамаг.
"""

import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import (
    DDL,
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    SmallInteger,
    String,
    Text,
    event,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, CreatedAtMixin, TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import (
    LiveGenerationKind,
    LiveGenerationStatus,
    LiveMaterialKind,
    LiveMaterialStatus,
    LiveTier,
    values,
)


def _in(column: str, enum_values: list[str]) -> str:
    return f"{column} IN ('" + "','".join(enum_values) + "')"


def _user_fk(ondelete: str = "CASCADE") -> ForeignKey:
    return ForeignKey("users.id", ondelete=ondelete)


class LiveMaterial(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Хэрэглэгчийн оруулсан лекц, слайд, зураг — нэг судлах багц.

    Эх файл нь R2-ийн хувийн bucket-д (`storage_key`), задалсан текст нь
    `text_key`-д. Postgres-д зөвхөн AI-ийн бүтцийг (сэдэв, карт) хадгална.
    Мөр устахад trigger эх файлыг `live_blob_deletions`-д устгах дараалалд
    оруулна (бүртгэл устгасан ч мөн адил).
    """

    __tablename__ = "live_materials"
    __table_args__ = (
        CheckConstraint(_in("kind", values(LiveMaterialKind)), name="kind_valid"),
        CheckConstraint(_in("status", values(LiveMaterialStatus)), name="status_valid"),
        Index("ix_live_materials_owner_created", "owner_id", "created_at"),
        Index("ix_live_materials_status", "status"),
    )

    owner_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), _user_fk(), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    # Хэрэглэгчийн файлын нэр (цэвэрлэсэн) — зөвхөн харуулна, хадгалах замд орохгүй.
    filename: Mapped[str] = mapped_column(String(200), nullable=False)
    kind: Mapped[str] = mapped_column(String(10), nullable=False)
    size_bytes: Mapped[int] = mapped_column(Integer, nullable=False)
    # Файл ирсний дараа.
    sha256: Mapped[str | None] = mapped_column(String(64), nullable=True)
    # Санамсаргүй түлхүүр (`materials/<uuid>/original`) — файлын нэрээс гаргахгүй.
    storage_key: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    # Задалсан текст (JSON, хуудас тус бүр). PDF-ийн текстгүй, зурагт NULL.
    text_key: Mapped[str | None] = mapped_column(String(120), nullable=True)
    page_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    status: Mapped[str] = mapped_column(
        String(12), default=LiveMaterialStatus.UPLOADING, nullable=False
    )
    error_code: Mapped[str | None] = mapped_column(String(40), nullable=True)
    # Цаана боловсруулах оролдлого (`app/live/worker.py`).
    attempts: Mapped[int] = mapped_column(
        SmallInteger, default=0, server_default=text("0"), nullable=False
    )
    claimed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    # Материал бүртгэсэн мөч — Үйлчилгээний нөхцөлийн Live заалтыг (ашиглах эрх, AI
    # боловсруулалт) энэ үед хүлээн зөвшөөрсөн. Тусдаа чагт байхгүй.
    rights_confirmed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    processed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    # AI-ийн товч агуулга.
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    model: Mapped[str | None] = mapped_column(String(80), nullable=True)
    prompt_version: Mapped[str | None] = mapped_column(String(40), nullable=True)


# Материал ямар ч замаар устсан (эзэн, бүртгэл устгах CASCADE) R2-ийн файлыг
# устгах дараалалд оруулна — `maintenance` ажил цэвэрлэнэ. Тестийн `create_all`
# ч мөн үүсгэнэ; migration-д ижил SQL бий.
LIVE_BLOB_TRIGGER_SQL = (
    """
CREATE OR REPLACE FUNCTION live_queue_blob_deletion() RETURNS trigger
LANGUAGE plpgsql SET search_path = public AS $$
BEGIN
  INSERT INTO live_blob_deletions (id, storage_key, attempts, created_at)
  VALUES (gen_random_uuid(), OLD.storage_key, 0, now());
  IF OLD.text_key IS NOT NULL THEN
    INSERT INTO live_blob_deletions (id, storage_key, attempts, created_at)
    VALUES (gen_random_uuid(), OLD.text_key, 0, now());
  END IF;
  RETURN OLD;
END;
$$
""",
    """
CREATE TRIGGER live_materials_queue_blob_deletion
AFTER DELETE ON live_materials
FOR EACH ROW EXECUTE FUNCTION live_queue_blob_deletion()
""",
)


class LiveBlobDeletion(UUIDPrimaryKeyMixin, CreatedAtMixin, Base):
    """R2-оос устгах файлын дараалал. Амжилттай устгасны дараа мөр устана."""

    __tablename__ = "live_blob_deletions"

    storage_key: Mapped[str] = mapped_column(String(120), nullable=False)
    attempts: Mapped[int] = mapped_column(
        SmallInteger, default=0, server_default=text("0"), nullable=False
    )


for _statement in LIVE_BLOB_TRIGGER_SQL:
    # Хоёр хүснэгт хоёулаа үүссэний дараа — `create_all` бүх хүснэгтээ үүсгэж дуусахад.
    event.listen(Base.metadata, "after_create", DDL(_statement))


class LiveTopic(UUIDPrimaryKeyMixin, CreatedAtMixin, Base):
    """AI-ийн гаргасан сэдэв. Хэсэг (section) нь тусдаа хүснэгт биш — гарчиг, байрлал."""

    __tablename__ = "live_topics"
    __table_args__ = (Index("ix_live_topics_material_position", "material_id", "position"),)

    material_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("live_materials.id", ondelete="CASCADE"), nullable=False
    )
    section_position: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    section_title: Mapped[str] = mapped_column(String(200), nullable=False)
    # Материал доторх дараалал (хэсгүүдийг дамнасан).
    position: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    # Англи хэлний тогтвортой нэр (`binary-search`) — тест, таамаг сэдэвтэй холбогдоно.
    key: Mapped[str] = mapped_column(String(120), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    # Эх материалын хуудас/слайдын дугаар (1-ээс).
    pages: Mapped[list[int]] = mapped_column(
        JSONB, default=list, server_default=text("'[]'::jsonb"), nullable=False
    )


class LiveCard(UUIDPrimaryKeyMixin, CreatedAtMixin, Base):
    """Нэр томьёоны карт — материалыг задлахад сэдэв бүрд үүснэ (нэмэлт AI дуудлагагүй)."""

    __tablename__ = "live_cards"
    __table_args__ = (
        Index("ix_live_cards_material_position", "material_id", "position"),
        Index("ix_live_cards_topic_id", "topic_id"),
    )

    material_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("live_materials.id", ondelete="CASCADE"), nullable=False
    )
    topic_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("live_topics.id", ondelete="CASCADE"), nullable=False
    )
    position: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    front: Mapped[str] = mapped_column(String(300), nullable=False)
    back: Mapped[str] = mapped_column(Text, nullable=False)
    page: Mapped[int | None] = mapped_column(Integer, nullable=True)


class LiveCardProgress(Base):
    """Leitner хайрцаг (0–4). Мөр байхгүй бол карт шинэ — одоо давтана."""

    __tablename__ = "live_card_progress"
    __table_args__ = (CheckConstraint("box BETWEEN 0 AND 4", name="box_valid"),)

    user_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), _user_fk(), primary_key=True)
    card_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("live_cards.id", ondelete="CASCADE"),
        primary_key=True,
        index=True,
    )
    box: Mapped[int] = mapped_column(SmallInteger, default=0, nullable=False)
    due_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    reviews: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    reviewed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class LiveTopicProgress(Base):
    """Сэдвийн эзэмшлийн түүхий өгөгдөл. Эзэмшлийн хувийг `app/live/mastery.py` тооцно."""

    __tablename__ = "live_topic_progress"

    user_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), _user_fk(), primary_key=True)
    topic_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("live_topics.id", ondelete="CASCADE"),
        primary_key=True,
        index=True,
    )
    guide_read_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    # Энэ сэдвийн асуултуудын сүүлийн тестийн дүн.
    quiz_correct: Mapped[int | None] = mapped_column(SmallInteger, nullable=True)
    quiz_total: Mapped[int | None] = mapped_column(SmallInteger, nullable=True)
    last_studied_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class LiveGeneration(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """AI-аар үүсгэх судлах хэрэгсэл — нэг удаа үүсгэж, дахин дахин ашиглана.

    Материал × төрөл × сэдэв тутамд нэг л мөр (хоёр хэсэгчилсэн unique index).
    «Шинээр үүсгэх» нь хуучныг устгаж (асуулт, оролдлого нь дагаж устана)
    шинийг дараалалд оруулна. Сэдвийн эзэмшил `live_topic_progress`-д үлдэнэ.
    """

    __tablename__ = "live_generations"
    __table_args__ = (
        CheckConstraint(_in("kind", values(LiveGenerationKind)), name="kind_valid"),
        CheckConstraint(_in("status", values(LiveGenerationStatus)), name="status_valid"),
        CheckConstraint(
            "(kind = 'guide' AND topic_id IS NOT NULL)"
            " OR (kind = 'exam' AND topic_id IS NULL)"
            " OR kind = 'quiz'",
            name="topic_matches_kind",
        ),
        Index(
            "uq_live_generations_topic_kind",
            "material_id",
            "kind",
            "topic_id",
            unique=True,
            postgresql_where=text("topic_id IS NOT NULL"),
        ),
        Index(
            "uq_live_generations_material_kind",
            "material_id",
            "kind",
            unique=True,
            postgresql_where=text("topic_id IS NULL"),
        ),
        Index("ix_live_generations_status", "status"),
    )

    material_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("live_materials.id", ondelete="CASCADE"), nullable=False
    )
    topic_id: Mapped[uuid.UUID | None] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("live_topics.id", ondelete="CASCADE"), nullable=True
    )
    kind: Mapped[str] = mapped_column(String(10), nullable=False)
    status: Mapped[str] = mapped_column(
        String(12), default=LiveGenerationStatus.QUEUED, nullable=False
    )
    # `guide` — `{"markdown": …}`; `exam` — таамаг. Тестийн асуулт `live_questions`-д.
    content: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
    error_code: Mapped[str | None] = mapped_column(String(40), nullable=True)
    attempts: Mapped[int] = mapped_column(
        SmallInteger, default=0, server_default=text("0"), nullable=False
    )
    claimed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    model: Mapped[str | None] = mapped_column(String(80), nullable=True)
    prompt_version: Mapped[str | None] = mapped_column(String(40), nullable=True)


class LiveQuestion(UUIDPrimaryKeyMixin, Base):
    """Тестийн асуулт. `correct_index` зөвхөн серверт — хариулсны дараа л илгээнэ."""

    __tablename__ = "live_questions"
    __table_args__ = (
        Index("ix_live_questions_generation_position", "generation_id", "position"),
        CheckConstraint("correct_index BETWEEN 0 AND 5", name="correct_index_valid"),
    )

    generation_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("live_generations.id", ondelete="CASCADE"), nullable=False
    )
    topic_id: Mapped[uuid.UUID | None] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("live_topics.id", ondelete="SET NULL"), nullable=True
    )
    position: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    prompt: Mapped[str] = mapped_column(Text, nullable=False)
    options: Mapped[list[str]] = mapped_column(JSONB, nullable=False)
    correct_index: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    explanation: Mapped[str] = mapped_column(Text, nullable=False)
    page: Mapped[int | None] = mapped_column(Integer, nullable=True)


class LiveQuizAttempt(UUIDPrimaryKeyMixin, CreatedAtMixin, Base):
    __tablename__ = "live_quiz_attempts"
    __table_args__ = (Index("ix_live_quiz_attempts_user_created", "user_id", "created_at"),)

    generation_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("live_generations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), _user_fk(), nullable=False)
    total: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    correct_count: Mapped[int] = mapped_column(SmallInteger, default=0, nullable=False)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class LiveQuizAnswer(Base):
    """Асуулт бүрд нэг л хариулт — давхар хариултыг primary key хориглоно."""

    __tablename__ = "live_quiz_answers"

    attempt_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("live_quiz_attempts.id", ondelete="CASCADE"),
        primary_key=True,
    )
    question_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("live_questions.id", ondelete="CASCADE"),
        primary_key=True,
        index=True,
    )
    choice_index: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, nullable=False)
    answered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class LiveSubscription(TimestampMixin, Base):
    """Premium — Standard багц дээрх илүү AI хязгаар. Хэрэглэгч тутамд нэг мөр.

    Live нь Standard багцад багтсан (`users.plan_expires_at`); энэ хүснэгт зөвхөн
    Premium-ийг хадгална. Premium олгоход Standard багц ч мөн хугацаа хүртэл
    сунгагдана (`app/live/admin.py`). Одоохондоо админ гараар олгоно; үнийг кодонд
    бичихгүй.
    """

    __tablename__ = "live_subscriptions"
    __table_args__ = (CheckConstraint(_in("tier", [LiveTier.PREMIUM.value]), name="tier_valid"),)

    user_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), _user_fk(), primary_key=True)
    tier: Mapped[str] = mapped_column(String(10), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    # Олгосон админ. Бүртгэл нь устсан ч мөр үлдэнэ.
    granted_by: Mapped[uuid.UUID | None] = mapped_column(
        PGUUID(as_uuid=True), _user_fk("SET NULL"), nullable=True
    )
    note: Mapped[str | None] = mapped_column(String(200), nullable=True)


class LivePass(UUIDPrimaryKeyMixin, CreatedAtMixin, Base):
    """Нэг удаагийн Live эрх — багцгүй хэрэглэгч нэг материалыг Live-аар судална.

    Төлбөр амжилттай болоход үүснэ (`billing_service.apply_payment`); төлбөрийн мөр
    `payments.live_pass_id`-аар заана. Ашиглаагүй эрх хугацаагүй. Шинэ материал
    бүртгэхэд тэр материалд холбогдож (`material_id`, `used_at`),
    `live_pass_access_days` хоног нээлттэй (`expires_at`). Материал бэлэн болохоос
    өмнө устгавал эрх буцаж ашиглаагүй болно (`app/live/materials.py`).

    Авснаас хойш `live_pass_upgrade_days` хоногийн дотор Standard/Premium авбал
    `price_mnt` тэр төлбөрөөс хасагдаж, эрх `upgraded_at`-тэй болно — ашиглаагүй
    байсан бол дахин ашиглагдахгүй (үнэ нь багцад шилжсэн).
    """

    __tablename__ = "live_passes"
    __table_args__ = (
        CheckConstraint("price_mnt >= 0", name="price_nonnegative"),
        CheckConstraint("(used_at IS NULL) = (expires_at IS NULL)", name="used_has_expiry"),
        Index("ix_live_passes_user_created", "user_id", "created_at"),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), _user_fk(), nullable=False)
    # Бодитоор төлсөн дүн, бүхэл төгрөг — багц авахад хасагдах дүн.
    price_mnt: Mapped[int] = mapped_column(Integer, nullable=False)
    # Материал устахад NULL — эрх ашигласан хэвээр (бэлэн болохоос өмнө устгаснаас бусад).
    material_id: Mapped[uuid.UUID | None] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("live_materials.id", ondelete="SET NULL"),
        unique=True,
        nullable=True,
    )
    used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    upgraded_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
