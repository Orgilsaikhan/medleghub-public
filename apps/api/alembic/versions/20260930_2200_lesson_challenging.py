"""Хэцүү хичээлийн шошго

- `lessons.challenging` — бусдаасаа хэцүү хичээл. «Заавар» хэсэгт шар «Хэцүү»
  шошго харагдана. Утгыг сургалтын агуулгаас (`LessonSpec.challenging`) seed
  бичнэ; одоо байгаа хичээлүүд `false`.

Revision ID: 8b6cf027f25e
Revises: 3e173d944404
Create Date: 2026-09-30 22:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "8b6cf027f25e"
down_revision: str | Sequence[str] | None = "3e173d944404"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "lessons",
        sa.Column("challenging", sa.Boolean(), server_default=sa.false(), nullable=False),
    )


def downgrade() -> None:
    op.drop_column("lessons", "challenging")
