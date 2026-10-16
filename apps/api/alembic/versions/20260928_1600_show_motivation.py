"""Урам өгөх үг харуулах тохиргоо

- `users.show_motivation` — дасгалын тестэд 3 удаа дараалан унавал урам өгөх
  үг харуулах эсэх. Анхдагчаар асаалттай.

Revision ID: 5d2f8b6a1e94
Revises: 9a4c7e1f3b58
Create Date: 2026-09-28 16:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "5d2f8b6a1e94"
down_revision: str | Sequence[str] | None = "9a4c7e1f3b58"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("show_motivation", sa.Boolean(), server_default=sa.true(), nullable=False),
    )


def downgrade() -> None:
    op.drop_column("users", "show_motivation")
