"""Standard багц: үнэгүй хичээлийн тоо, багцын хугацаа, төлбөр

- `courses.free_lessons` — `is_free=False` сургалтын эхний хэдэн хичээл
  бүгдэд нээлттэй вэ.
- `users.plan_expires_at` — Standard багц хүчинтэй хугацаа.
- `payments` — Wire-ээр хийсэн төлбөр бүр.

Revision ID: b4d7e1c9a2f6
Revises: a1c5e9f2b7d3
Create Date: 2026-09-27 19:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "b4d7e1c9a2f6"
down_revision: str | Sequence[str] | None = "a1c5e9f2b7d3"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "courses",
        sa.Column("free_lessons", sa.Integer(), server_default="0", nullable=False),
    )
    op.create_check_constraint(
        op.f("ck_courses_free_lessons_non_negative"), "courses", "free_lessons >= 0"
    )
    op.add_column("users", sa.Column("plan_expires_at", sa.DateTime(timezone=True), nullable=True))

    op.create_table(
        "payments",
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("provider", sa.String(length=20), nullable=False),
        sa.Column("provider_payment_id", sa.String(length=100), nullable=True),
        sa.Column("amount", sa.Integer(), nullable=False),
        sa.Column("currency", sa.String(length=3), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("checkout_url", sa.String(length=500), nullable=True),
        sa.Column("paid_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "status IN ('pending','succeeded','canceled','failed')",
            name=op.f("ck_payments_status_valid"),
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_payments_user_id_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_payments")),
        sa.UniqueConstraint("provider_payment_id", name=op.f("uq_payments_provider_payment_id")),
    )
    op.create_index(op.f("ix_payments_user_id"), "payments", ["user_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_payments_user_id"), table_name="payments")
    op.drop_table("payments")
    op.drop_column("users", "plan_expires_at")
    op.drop_constraint(op.f("ck_courses_free_lessons_non_negative"), "courses", type_="check")
    op.drop_column("courses", "free_lessons")
