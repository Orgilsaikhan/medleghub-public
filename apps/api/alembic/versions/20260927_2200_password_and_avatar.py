"""Нууц үг солих, профайлын зураг

- `users.password_changed_at` — үүнээс өмнөх token хүчингүй.
- `users.avatar_key` — зургийн хувилбар (URL-д).
- `user_avatars` — зураг өөрөө (WebP байт). RLS асаалттай
  (`20260927_2100_enable_rls.py`-г үз).

Revision ID: d2a9b6e4f1c3
Revises: c8e3f5a1d7b2
Create Date: 2026-09-27 22:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "d2a9b6e4f1c3"
down_revision: str | Sequence[str] | None = "c8e3f5a1d7b2"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "users", sa.Column("password_changed_at", sa.DateTime(timezone=True), nullable=True)
    )
    op.add_column("users", sa.Column("avatar_key", sa.String(length=32), nullable=True))
    op.create_table(
        "user_avatars",
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("data", sa.LargeBinary(), nullable=False),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_user_avatars_user_id_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("user_id", name=op.f("pk_user_avatars")),
    )
    op.execute("ALTER TABLE user_avatars ENABLE ROW LEVEL SECURITY")


def downgrade() -> None:
    op.drop_table("user_avatars")
    op.drop_column("users", "avatar_key")
    op.drop_column("users", "password_changed_at")
