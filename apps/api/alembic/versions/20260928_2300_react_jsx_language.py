"""React сургалтын `jsx` хэл.

React хичээлийн код нь олон файл (`// @file App.jsx`) бөгөөд sandbox
iframe дотор «Хөтөч» дээр ажиллана. Засварлагч үүнийг `javascript` болгож
JSX-ийг таниулна.

Revision ID: f2b8d4c6a913
Revises: e7a3c1f94b26
Create Date: 2026-09-28 23:00:00.000000
"""

from collections.abc import Sequence

from alembic import op

revision: str = "f2b8d4c6a913"
down_revision: str | Sequence[str] | None = "e7a3c1f94b26"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

OLD_LANGUAGES = "'javascript','html','css','python','c','cpp','shell','mysql','sql','plaintext'"


def upgrade() -> None:
    op.drop_constraint("language_valid", "lessons", type_="check")
    op.create_check_constraint(
        "language_valid", "lessons", f"language IN ({OLD_LANGUAGES},'jsx')"
    )


def downgrade() -> None:
    # `jsx` хичээл байвал хуучин CHECK нь downgrade-ийг бүхэлд нь буцаана —
    # React сургалтын агуулга, суралцагчийн ахицыг автоматаар устгахгүй.
    op.drop_constraint("language_valid", "lessons", type_="check")
    op.create_check_constraint("language_valid", "lessons", f"language IN ({OLD_LANGUAGES})")
