"""Flowgorithm болон test салбарын migration-уудыг нэгтгэнэ. Схем өөрчлөхгүй.

Revision ID: bf087d4b5d1d
Revises: e6f9b2c48d13, d2a9b6e4f1c3
Create Date: 2026-09-27 21:52:42.690547
"""

from collections.abc import Sequence

revision: str = "bf087d4b5d1d"
down_revision: str | Sequence[str] | None = ("e6f9b2c48d13", "d2a9b6e4f1c3")
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
