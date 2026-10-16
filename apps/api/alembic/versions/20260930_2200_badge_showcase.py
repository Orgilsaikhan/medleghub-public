"""Онцлох амжилт (профайлын нэрийн хажууд)

- `user_badges.showcase_position` — авсан тэмдгийг эзний профайлд онцлох байр
  (1–5). NULL бол онцлоогүй. Дээд тоо нь `app.models.badge.SHOWCASE_MAX` —
  өөрчилбөл энэ CHECK-ийг шинэ migration-аар хамт өөрчилнө.
- `uq_user_badges_showcase_position` — нэг хэрэглэгчийн нэг байранд нэг л
  тэмдэг. Postgres олон NULL-ийг давхардал гэж үзэхгүй тул онцлоогүй тэмдэгт
  хязгааргүй. RLS аль хэдийн асаалттай (`20260927_2100_enable_rls.py`).

Revision ID: 3cee52648b58
Revises: 8b6cf027f25e
Create Date: 2026-09-30 22:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "3cee52648b58"
down_revision: str | Sequence[str] | None = "8b6cf027f25e"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("user_badges", sa.Column("showcase_position", sa.SmallInteger(), nullable=True))
    op.create_check_constraint(
        op.f("ck_user_badges_showcase_position_valid"),
        "user_badges",
        "showcase_position BETWEEN 1 AND 5",
    )
    op.create_unique_constraint(
        "uq_user_badges_showcase_position", "user_badges", ["user_id", "showcase_position"]
    )


def downgrade() -> None:
    op.drop_constraint("uq_user_badges_showcase_position", "user_badges", type_="unique")
    op.drop_constraint(op.f("ck_user_badges_showcase_position_valid"), "user_badges", type_="check")
    op.drop_column("user_badges", "showcase_position")
