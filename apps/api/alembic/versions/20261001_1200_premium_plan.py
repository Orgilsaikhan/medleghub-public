"""Premium багц худалдаж авах

- `payments.plan` — `standard` / `premium`. Premium төлбөр Standard-ийг сунгахаас
  гадна `live_subscriptions`-ийг мөн сараар сунгана. Хуучин мөрүүд `standard`.
- `plan_prices.plan` — багц тус бүрийн үнийн түүх; хуучин мөрүүд `standard`.

Зөвхөн нэмэлт багана (анхдагч утгатай) — одоо байгаа өгөгдөл өөрчлөгдөхгүй. RLS
хоёр хүснэгтэд аль хэдийн асаалттай.

Revision ID: 5e2b9c4d7a18
Revises: 7d41c9a2e5b3
Create Date: 2026-10-01 12:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "5e2b9c4d7a18"
down_revision: str | Sequence[str] | None = "7d41c9a2e5b3"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    for table in ("payments", "plan_prices"):
        op.add_column(
            table,
            sa.Column(
                "plan", sa.String(length=10), server_default=sa.text("'standard'"), nullable=False
            ),
        )
        op.create_check_constraint(
            op.f(f"ck_{table}_plan_valid"), table, "plan IN ('standard','premium')"
        )
    op.create_index("ix_plan_prices_plan_created", "plan_prices", ["plan", "created_at"])


def downgrade() -> None:
    op.drop_index("ix_plan_prices_plan_created", table_name="plan_prices")
    for table in ("payments", "plan_prices"):
        op.drop_constraint(op.f(f"ck_{table}_plan_valid"), table, type_="check")
        op.drop_column(table, "plan")
