"""Хичээлийн засварлагчийн байрлал

- `users.editor_layout` — `new` (засварлагч зүүн, заавар баруун; анхдагч) эсвэл
  `legacy` (заавар дээр, засварлагч доор). Одоо байгаа хэрэглэгчид `new`.

Revision ID: 3e173d944404
Revises: 6fba503fc346
Create Date: 2026-09-30 20:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "3e173d944404"
down_revision: str | Sequence[str] | None = "6fba503fc346"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column(
            "editor_layout", sa.String(length=10), server_default=sa.text("'new'"), nullable=False
        ),
    )
    op.create_check_constraint(
        op.f("ck_users_editor_layout_valid"), "users", "editor_layout IN ('new','legacy')"
    )


def downgrade() -> None:
    op.drop_constraint(op.f("ck_users_editor_layout_valid"), "users", type_="check")
    op.drop_column("users", "editor_layout")
