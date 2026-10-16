"""Админы зарлал (popup)

- `announcements` — гарчиг, Markdown бичвэр, заавал биш товч (бичвэр +
  холбоос), хүрэх хүрээ, эхлэх/дуусах хугацаа, нийтэлсэн эсэх. Хэн харсныг
  хадгалахгүй (хөтөч санана). RLS асаалттай (`20260927_2100_enable_rls.py`-г үз).

Revision ID: 6fba503fc346
Revises: 8ef64d74047a
Create Date: 2026-09-30 18:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "6fba503fc346"
down_revision: str | Sequence[str] | None = "8ef64d74047a"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "announcements",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("kind", sa.String(length=20), nullable=False),
        sa.Column("title", sa.String(length=120), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("cta_label", sa.String(length=40), nullable=True),
        sa.Column("cta_url", sa.String(length=500), nullable=True),
        sa.Column("audience", sa.String(length=20), nullable=False),
        sa.Column("starts_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("ends_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("active", sa.Boolean(), server_default=sa.false(), nullable=False),
        sa.Column("created_by", sa.UUID(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "kind IN ('update','feature')", name=op.f("ck_announcements_kind_valid")
        ),
        sa.CheckConstraint(
            "audience IN ('everyone','signed_in','free','standard')",
            name=op.f("ck_announcements_audience_valid"),
        ),
        sa.CheckConstraint(
            "(cta_label IS NULL) = (cta_url IS NULL)", name=op.f("ck_announcements_cta_complete")
        ),
        sa.CheckConstraint(
            "starts_at IS NULL OR ends_at IS NULL OR ends_at > starts_at",
            name=op.f("ck_announcements_period_valid"),
        ),
        sa.ForeignKeyConstraint(
            ["created_by"],
            ["users.id"],
            name=op.f("fk_announcements_created_by_users"),
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_announcements")),
    )
    op.execute("ALTER TABLE announcements ENABLE ROW LEVEL SECURITY")


def downgrade() -> None:
    op.drop_table("announcements")
