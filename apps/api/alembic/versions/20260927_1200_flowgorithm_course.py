"""Flowgorithm ангилал болон алгоритмын төлөвлөгөөний plaintext хэл.

Revision ID: e6f9b2c48d13
Revises: d5e8a1f37c02
Create Date: 2026-09-27 12:00:00.000000
"""

from collections.abc import Sequence

from alembic import op

revision: str = "e6f9b2c48d13"
down_revision: str | Sequence[str] | None = "d5e8a1f37c02"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

OLD_CATEGORIES = (
    "'html_css','javascript','python','c','csharp','java','react','backend','database','git'"
)
OLD_LANGUAGES = "'javascript','html','css','python','c','cpp','shell','mysql','sql'"


def upgrade() -> None:
    op.drop_constraint("category_valid", "courses", type_="check")
    op.create_check_constraint(
        "category_valid", "courses", f"category IN ({OLD_CATEGORIES},'flowgorithm')"
    )
    op.drop_constraint("language_valid", "lessons", type_="check")
    op.create_check_constraint(
        "language_valid", "lessons", f"language IN ({OLD_LANGUAGES},'plaintext')"
    )


def downgrade() -> None:
    # Шинэ утгатай бичлэг байвал хуучин CHECK нь downgrade-ийг бүхэлд нь
    # буцаана. Сургалт, суралцагчийн ахицыг автоматаар устгахгүй.
    op.drop_constraint("language_valid", "lessons", type_="check")
    op.create_check_constraint("language_valid", "lessons", f"language IN ({OLD_LANGUAGES})")
    op.drop_constraint("category_valid", "courses", type_="check")
    op.create_check_constraint("category_valid", "courses", f"category IN ({OLD_CATEGORIES})")
