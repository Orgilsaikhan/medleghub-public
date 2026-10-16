"""MedlegHub Live — AI Study (эхний прототип)

- `live_materials` — хэрэглэгчийн оруулсан лекц, слайд (эх файл нь R2-д);
  `live_topics`, `live_cards` — AI-ийн гаргасан сэдэв, нэр томьёоны карт.
- `live_generations` — сэдвийн заавар, тест, «Шалгалтад бэлтгэх»;
  `live_questions`, `live_quiz_attempts`, `live_quiz_answers` — тест.
- `live_topic_progress`, `live_card_progress` — эзэмшил, Leitner хайрцаг.
- `live_subscriptions` — Premium (Standard дээрх илүү AI хязгаар); Live өөрөө
  Standard багцад багтсан.
- `live_blob_deletions` + trigger — материал ямар ч замаар устсан R2-ийн
  файлыг устгах дараалалд оруулна.
- `ai_requests` — AI дуудлага бүрийн токен, зардал (агуулгагүй).

Бусад хүснэгтийг өөрчлөхгүй. Хэрэглэгч рүү заасан FK бүр CASCADE эсвэл
SET NULL. Бүх шинэ хүснэгтэд RLS асаалттай.

Revision ID: 7d41c9a2e5b3
Revises: 3cee52648b58
Create Date: 2026-10-01 09:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "7d41c9a2e5b3"
down_revision: str | Sequence[str] | None = "3cee52648b58"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

TABLES = (
    "live_blob_deletions",
    "live_materials",
    "live_subscriptions",
    "ai_requests",
    "live_topics",
    "live_cards",
    "live_generations",
    "live_topic_progress",
    "live_card_progress",
    "live_questions",
    "live_quiz_attempts",
    "live_quiz_answers",
)

# `app/models/live.py`-ийн `LIVE_BLOB_TRIGGER_SQL`-тэй ижил (migration model-оос
# хамаарахгүйн тулд хуулсан).
BLOB_TRIGGER_SQL = (
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


def upgrade() -> None:
    op.create_table(
        "live_blob_deletions",
        sa.Column("storage_key", sa.String(length=120), nullable=False),
        sa.Column("attempts", sa.SmallInteger(), server_default=sa.text("0"), nullable=False),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_live_blob_deletions")),
    )
    op.create_table(
        "live_materials",
        sa.Column("owner_id", sa.UUID(), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("filename", sa.String(length=200), nullable=False),
        sa.Column("kind", sa.String(length=10), nullable=False),
        sa.Column("size_bytes", sa.Integer(), nullable=False),
        sa.Column("sha256", sa.String(length=64), nullable=True),
        sa.Column("storage_key", sa.String(length=120), nullable=False),
        sa.Column("text_key", sa.String(length=120), nullable=True),
        sa.Column("page_count", sa.Integer(), nullable=True),
        sa.Column("status", sa.String(length=12), nullable=False),
        sa.Column("error_code", sa.String(length=40), nullable=True),
        sa.Column("attempts", sa.SmallInteger(), server_default=sa.text("0"), nullable=False),
        sa.Column("claimed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("rights_confirmed_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("processed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("model", sa.String(length=80), nullable=True),
        sa.Column("prompt_version", sa.String(length=40), nullable=True),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "kind IN ('pdf','pptx','docx','txt','md','image')",
            name=op.f("ck_live_materials_kind_valid"),
        ),
        sa.CheckConstraint(
            "status IN ('uploading','queued','processing','ready','failed')",
            name=op.f("ck_live_materials_status_valid"),
        ),
        sa.ForeignKeyConstraint(
            ["owner_id"],
            ["users.id"],
            name=op.f("fk_live_materials_owner_id_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_live_materials")),
        sa.UniqueConstraint("storage_key", name=op.f("uq_live_materials_storage_key")),
    )
    op.create_index(
        "ix_live_materials_owner_created",
        "live_materials",
        ["owner_id", "created_at"],
        unique=False,
    )
    op.create_index("ix_live_materials_status", "live_materials", ["status"], unique=False)
    op.create_table(
        "live_subscriptions",
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("tier", sa.String(length=10), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("granted_by", sa.UUID(), nullable=True),
        sa.Column("note", sa.String(length=200), nullable=True),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "tier IN ('premium')", name=op.f("ck_live_subscriptions_tier_valid")
        ),
        sa.ForeignKeyConstraint(
            ["granted_by"],
            ["users.id"],
            name=op.f("fk_live_subscriptions_granted_by_users"),
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_live_subscriptions_user_id_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("user_id", name=op.f("pk_live_subscriptions")),
    )
    op.create_table(
        "ai_requests",
        sa.Column("user_id", sa.UUID(), nullable=True),
        sa.Column("material_id", sa.UUID(), nullable=True),
        sa.Column("capability", sa.String(length=40), nullable=False),
        sa.Column("provider", sa.String(length=20), nullable=False),
        sa.Column("model", sa.String(length=80), nullable=False),
        sa.Column("prompt_version", sa.String(length=40), nullable=False),
        sa.Column("attempt", sa.SmallInteger(), nullable=False),
        sa.Column("kind", sa.String(length=10), nullable=False),
        sa.Column("input_tokens", sa.Integer(), nullable=False),
        sa.Column("cached_input_tokens", sa.Integer(), nullable=False),
        sa.Column("output_tokens", sa.Integer(), nullable=False),
        sa.Column("reasoning_tokens", sa.Integer(), nullable=False),
        sa.Column("estimated_cost_usd", sa.Numeric(precision=12, scale=6), nullable=False),
        sa.Column("price_version", sa.String(length=20), nullable=False),
        sa.Column("duration_ms", sa.Integer(), nullable=False),
        sa.Column("success", sa.Boolean(), nullable=False),
        sa.Column("error_code", sa.String(length=60), nullable=True),
        sa.Column("provider_request_id", sa.String(length=120), nullable=True),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["material_id"],
            ["live_materials.id"],
            name=op.f("fk_ai_requests_material_id_live_materials"),
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_ai_requests_user_id_users"),
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_ai_requests")),
    )
    op.create_index("ix_ai_requests_created_at", "ai_requests", ["created_at"], unique=False)
    op.create_index(
        "ix_ai_requests_user_created", "ai_requests", ["user_id", "created_at"], unique=False
    )
    op.create_table(
        "live_topics",
        sa.Column("material_id", sa.UUID(), nullable=False),
        sa.Column("section_position", sa.SmallInteger(), nullable=False),
        sa.Column("section_title", sa.String(length=200), nullable=False),
        sa.Column("position", sa.SmallInteger(), nullable=False),
        sa.Column("key", sa.String(length=120), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column(
            "pages",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default=sa.text("'[]'::jsonb"),
            nullable=False,
        ),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["material_id"],
            ["live_materials.id"],
            name=op.f("fk_live_topics_material_id_live_materials"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_live_topics")),
    )
    op.create_index(
        "ix_live_topics_material_position", "live_topics", ["material_id", "position"], unique=False
    )
    op.create_table(
        "live_cards",
        sa.Column("material_id", sa.UUID(), nullable=False),
        sa.Column("topic_id", sa.UUID(), nullable=False),
        sa.Column("position", sa.SmallInteger(), nullable=False),
        sa.Column("front", sa.String(length=300), nullable=False),
        sa.Column("back", sa.Text(), nullable=False),
        sa.Column("page", sa.Integer(), nullable=True),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["material_id"],
            ["live_materials.id"],
            name=op.f("fk_live_cards_material_id_live_materials"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["topic_id"],
            ["live_topics.id"],
            name=op.f("fk_live_cards_topic_id_live_topics"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_live_cards")),
    )
    op.create_index(
        "ix_live_cards_material_position", "live_cards", ["material_id", "position"], unique=False
    )
    op.create_index("ix_live_cards_topic_id", "live_cards", ["topic_id"], unique=False)
    op.create_table(
        "live_generations",
        sa.Column("material_id", sa.UUID(), nullable=False),
        sa.Column("topic_id", sa.UUID(), nullable=True),
        sa.Column("kind", sa.String(length=10), nullable=False),
        sa.Column("status", sa.String(length=12), nullable=False),
        sa.Column("content", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("error_code", sa.String(length=40), nullable=True),
        sa.Column("attempts", sa.SmallInteger(), server_default=sa.text("0"), nullable=False),
        sa.Column("claimed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("model", sa.String(length=80), nullable=True),
        sa.Column("prompt_version", sa.String(length=40), nullable=True),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "(kind = 'guide' AND topic_id IS NOT NULL)"
            " OR (kind = 'exam' AND topic_id IS NULL)"
            " OR kind = 'quiz'",
            name=op.f("ck_live_generations_topic_matches_kind"),
        ),
        sa.CheckConstraint(
            "kind IN ('guide','quiz','exam')", name=op.f("ck_live_generations_kind_valid")
        ),
        sa.CheckConstraint(
            "status IN ('queued','processing','ready','failed')",
            name=op.f("ck_live_generations_status_valid"),
        ),
        sa.ForeignKeyConstraint(
            ["material_id"],
            ["live_materials.id"],
            name=op.f("fk_live_generations_material_id_live_materials"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["topic_id"],
            ["live_topics.id"],
            name=op.f("fk_live_generations_topic_id_live_topics"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_live_generations")),
    )
    op.create_index("ix_live_generations_status", "live_generations", ["status"], unique=False)
    op.create_index(
        "uq_live_generations_material_kind",
        "live_generations",
        ["material_id", "kind"],
        unique=True,
        postgresql_where=sa.text("topic_id IS NULL"),
    )
    op.create_index(
        "uq_live_generations_topic_kind",
        "live_generations",
        ["material_id", "kind", "topic_id"],
        unique=True,
        postgresql_where=sa.text("topic_id IS NOT NULL"),
    )
    op.create_table(
        "live_topic_progress",
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("topic_id", sa.UUID(), nullable=False),
        sa.Column("guide_read_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("quiz_correct", sa.SmallInteger(), nullable=True),
        sa.Column("quiz_total", sa.SmallInteger(), nullable=True),
        sa.Column("last_studied_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["topic_id"],
            ["live_topics.id"],
            name=op.f("fk_live_topic_progress_topic_id_live_topics"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_live_topic_progress_user_id_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("user_id", "topic_id", name=op.f("pk_live_topic_progress")),
    )
    op.create_index(
        op.f("ix_live_topic_progress_topic_id"), "live_topic_progress", ["topic_id"], unique=False
    )
    op.create_table(
        "live_card_progress",
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("card_id", sa.UUID(), nullable=False),
        sa.Column("box", sa.SmallInteger(), nullable=False),
        sa.Column("due_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("reviews", sa.Integer(), nullable=False),
        sa.Column("reviewed_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("box BETWEEN 0 AND 4", name=op.f("ck_live_card_progress_box_valid")),
        sa.ForeignKeyConstraint(
            ["card_id"],
            ["live_cards.id"],
            name=op.f("fk_live_card_progress_card_id_live_cards"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_live_card_progress_user_id_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("user_id", "card_id", name=op.f("pk_live_card_progress")),
    )
    op.create_index(
        op.f("ix_live_card_progress_card_id"), "live_card_progress", ["card_id"], unique=False
    )
    op.create_table(
        "live_questions",
        sa.Column("generation_id", sa.UUID(), nullable=False),
        sa.Column("topic_id", sa.UUID(), nullable=True),
        sa.Column("position", sa.SmallInteger(), nullable=False),
        sa.Column("prompt", sa.Text(), nullable=False),
        sa.Column("options", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("correct_index", sa.SmallInteger(), nullable=False),
        sa.Column("explanation", sa.Text(), nullable=False),
        sa.Column("page", sa.Integer(), nullable=True),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.CheckConstraint(
            "correct_index BETWEEN 0 AND 5", name=op.f("ck_live_questions_correct_index_valid")
        ),
        sa.ForeignKeyConstraint(
            ["generation_id"],
            ["live_generations.id"],
            name=op.f("fk_live_questions_generation_id_live_generations"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["topic_id"],
            ["live_topics.id"],
            name=op.f("fk_live_questions_topic_id_live_topics"),
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_live_questions")),
    )
    op.create_index(
        "ix_live_questions_generation_position",
        "live_questions",
        ["generation_id", "position"],
        unique=False,
    )
    op.create_table(
        "live_quiz_attempts",
        sa.Column("generation_id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("total", sa.SmallInteger(), nullable=False),
        sa.Column("correct_count", sa.SmallInteger(), nullable=False),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["generation_id"],
            ["live_generations.id"],
            name=op.f("fk_live_quiz_attempts_generation_id_live_generations"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_live_quiz_attempts_user_id_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_live_quiz_attempts")),
    )
    op.create_index(
        op.f("ix_live_quiz_attempts_generation_id"),
        "live_quiz_attempts",
        ["generation_id"],
        unique=False,
    )
    op.create_index(
        "ix_live_quiz_attempts_user_created",
        "live_quiz_attempts",
        ["user_id", "created_at"],
        unique=False,
    )
    op.create_table(
        "live_quiz_answers",
        sa.Column("attempt_id", sa.UUID(), nullable=False),
        sa.Column("question_id", sa.UUID(), nullable=False),
        sa.Column("choice_index", sa.SmallInteger(), nullable=False),
        sa.Column("is_correct", sa.Boolean(), nullable=False),
        sa.Column(
            "answered_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["attempt_id"],
            ["live_quiz_attempts.id"],
            name=op.f("fk_live_quiz_answers_attempt_id_live_quiz_attempts"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["question_id"],
            ["live_questions.id"],
            name=op.f("fk_live_quiz_answers_question_id_live_questions"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("attempt_id", "question_id", name=op.f("pk_live_quiz_answers")),
    )
    op.create_index(
        op.f("ix_live_quiz_answers_question_id"), "live_quiz_answers", ["question_id"], unique=False
    )
    for table in TABLES:
        op.execute(f"ALTER TABLE {table} ENABLE ROW LEVEL SECURITY")
    for statement in BLOB_TRIGGER_SQL:
        op.execute(statement)


def downgrade() -> None:
    op.execute("DROP TRIGGER IF EXISTS live_materials_queue_blob_deletion ON live_materials")
    op.execute("DROP FUNCTION IF EXISTS live_queue_blob_deletion()")
    op.drop_index(op.f("ix_live_quiz_answers_question_id"), table_name="live_quiz_answers")
    op.drop_table("live_quiz_answers")
    op.drop_index("ix_live_quiz_attempts_user_created", table_name="live_quiz_attempts")
    op.drop_index(op.f("ix_live_quiz_attempts_generation_id"), table_name="live_quiz_attempts")
    op.drop_table("live_quiz_attempts")
    op.drop_index("ix_live_questions_generation_position", table_name="live_questions")
    op.drop_table("live_questions")
    op.drop_index(op.f("ix_live_card_progress_card_id"), table_name="live_card_progress")
    op.drop_table("live_card_progress")
    op.drop_index(op.f("ix_live_topic_progress_topic_id"), table_name="live_topic_progress")
    op.drop_table("live_topic_progress")
    op.drop_index(
        "uq_live_generations_topic_kind",
        table_name="live_generations",
        postgresql_where=sa.text("topic_id IS NOT NULL"),
    )
    op.drop_index(
        "uq_live_generations_material_kind",
        table_name="live_generations",
        postgresql_where=sa.text("topic_id IS NULL"),
    )
    op.drop_index("ix_live_generations_status", table_name="live_generations")
    op.drop_table("live_generations")
    op.drop_index("ix_live_cards_topic_id", table_name="live_cards")
    op.drop_index("ix_live_cards_material_position", table_name="live_cards")
    op.drop_table("live_cards")
    op.drop_index("ix_live_topics_material_position", table_name="live_topics")
    op.drop_table("live_topics")
    op.drop_index("ix_ai_requests_user_created", table_name="ai_requests")
    op.drop_index("ix_ai_requests_created_at", table_name="ai_requests")
    op.drop_table("ai_requests")
    op.drop_table("live_subscriptions")
    op.drop_index("ix_live_materials_status", table_name="live_materials")
    op.drop_index("ix_live_materials_owner_created", table_name="live_materials")
    op.drop_table("live_materials")
    op.drop_table("live_blob_deletions")
