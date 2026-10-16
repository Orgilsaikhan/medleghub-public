"""lessons.exercise нэмэх

HackerRank маягийн дасгал — даалгавар болон оролт/гаралтын тестүүд. Эхлээд
C/C++ сургалтад хэрэглэнэ. Хоосон (`NULL`) бол хичээл дасгалгүй бөгөөд
урьдын адил «Хичээл дууссан» товчоор дуусна.

Revision ID: e7a2c4b91d05
Revises: d5e8a1f37c02
Create Date: 2026-09-27 01:30:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "e7a2c4b91d05"
down_revision: str | Sequence[str] | None = "d5e8a1f37c02"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "lessons",
        sa.Column("exercise", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("lessons", "exercise")
