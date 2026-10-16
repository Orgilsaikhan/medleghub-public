"""Админ хэрэглэгчийн багцыг гараар нэмж, хасна

- `plan_adjustments` — гараар хийсэн өөрчлөлт бүр (хэн, хэзээ, хэдэн сар,
  өмнөх ба дараах дуусах хугацаа, тэмдэглэл). RLS асаалттай
  (`20260927_2100_enable_rls.py`-г үз).

Revision ID: c4e9a7b2d813
Revises: 8b3d6f1a4c27
Create Date: 2026-09-28 20:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "c4e9a7b2d813"
down_revision: str | Sequence[str] | None = "8b3d6f1a4c27"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "plan_adjustments",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("admin_id", sa.UUID(), nullable=True),
        sa.Column("months", sa.Integer(), nullable=False),
        sa.Column("expires_before", sa.DateTime(timezone=True), nullable=True),
        sa.Column("expires_after", sa.DateTime(timezone=True), nullable=False),
        sa.Column("note", sa.String(length=500), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint("months <> 0", name=op.f("ck_plan_adjustments_months_nonzero")),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_plan_adjustments_user_id_users"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["admin_id"],
            ["users.id"],
            name=op.f("fk_plan_adjustments_admin_id_users"),
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_plan_adjustments")),
    )
    op.create_index(
        op.f("ix_plan_adjustments_user_id"), "plan_adjustments", ["user_id"], unique=False
    )
    op.execute("ALTER TABLE plan_adjustments ENABLE ROW LEVEL SECURITY")


def downgrade() -> None:
    op.drop_index(op.f("ix_plan_adjustments_user_id"), table_name="plan_adjustments")
    op.drop_table("plan_adjustments")
