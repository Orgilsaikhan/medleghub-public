"""user_badges хүснэгт нэмэх

Профайл дээрх тэмдгүүд. Тэмдгийн тодорхойлолт кодод
(`app/content/badges.py`), энд зөвхөн хэрэглэгчийн авсан тэмдэг.

Revision ID: f3b8d2a6c914
Revises: e7a2c4b91d05
Create Date: 2026-09-27 06:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "f3b8d2a6c914"
down_revision: str | Sequence[str] | None = "e7a2c4b91d05"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "user_badges",
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("badge_key", sa.String(length=64), nullable=False),
        sa.Column(
            "awarded_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_user_badges_user_id_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_user_badges")),
        sa.UniqueConstraint("user_id", "badge_key", name="uq_user_badges_user_badge"),
    )
    op.create_index(op.f("ix_user_badges_user_id"), "user_badges", ["user_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_user_badges_user_id"), table_name="user_badges")
    op.drop_table("user_badges")
