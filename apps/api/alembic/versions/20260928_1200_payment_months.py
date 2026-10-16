"""Олон сарын төлбөр

- `payments.months` — төлбөр багцыг хэдэн сараар сунгах (үнэгүй сарыг
  оруулаад). Өмнөх бүх төлбөр нэг сарынх байсан тул анхдагч нь 1.

Revision ID: 3e8b5f2a9c71
Revises: 7c1e4a9d2b6f
Create Date: 2026-09-28 12:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "3e8b5f2a9c71"
down_revision: str | Sequence[str] | None = "7c1e4a9d2b6f"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("payments", sa.Column("months", sa.Integer(), server_default="1", nullable=False))
    op.create_check_constraint(op.f("ck_payments_months_positive"), "payments", "months >= 1")


def downgrade() -> None:
    op.drop_constraint(op.f("ck_payments_months_positive"), "payments", type_="check")
    op.drop_column("payments", "months")
