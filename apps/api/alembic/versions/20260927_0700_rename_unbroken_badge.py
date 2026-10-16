"""«Unbroken» тэмдгийг «Unstoppable» болгож нэрлэх

Тэмдгийн түлхүүр `unbroken` → `unstoppable`. Аль хэдийн авсан хэрэглэгчид
тэмдгээ алдахгүйн тулд бичлэгийг шинэ түлхүүр рүү зөөнө.

Revision ID: a1c5e9f2b7d3
Revises: f3b8d2a6c914
Create Date: 2026-09-27 07:00:00.000000

"""

from collections.abc import Sequence

from alembic import op

revision: str = "a1c5e9f2b7d3"
down_revision: str | Sequence[str] | None = "f3b8d2a6c914"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("UPDATE user_badges SET badge_key = 'unstoppable' WHERE badge_key = 'unbroken'")


def downgrade() -> None:
    op.execute("UPDATE user_badges SET badge_key = 'unbroken' WHERE badge_key = 'unstoppable'")
