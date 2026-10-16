"""Standard багцын сарын үнийг админ өөрчилнө

- `plan_prices` — сарын үнийн түүх. Хамгийн сүүлийн мөр нь одоогийн үнэ;
  хоосон бол `PLAN_PRICE_MNT`. RLS асаалттай
  (`20260927_2100_enable_rls.py`-г үз).

Revision ID: 8b3d6f1a4c27
Revises: 5d2f8b6a1e94
Create Date: 2026-09-28 18:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "8b3d6f1a4c27"
down_revision: str | Sequence[str] | None = "5d2f8b6a1e94"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "plan_prices",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("price_mnt", sa.Integer(), nullable=False),
        sa.Column("changed_by", sa.UUID(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint("price_mnt > 0", name=op.f("ck_plan_prices_price_positive")),
        sa.ForeignKeyConstraint(
            ["changed_by"],
            ["users.id"],
            name=op.f("fk_plan_prices_changed_by_users"),
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_plan_prices")),
    )
    op.execute("ALTER TABLE plan_prices ENABLE ROW LEVEL SECURITY")


def downgrade() -> None:
    op.drop_table("plan_prices")
