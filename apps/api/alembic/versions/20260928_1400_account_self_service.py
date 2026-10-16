"""Имэйл баталгаажуулалт, насны зөвшөөрөл, профайл нуух, бүртгэл устгах

- `users.email_verified_at` — өмнөх бүх бүртгэлийг `created_at`-аар
  баталгаажсанд тооцно (эс бөгөөс нэвтэрч чадахгүй болно).
- `users.pending_email`, `users.profile_hidden`, `users.terms_accepted_at`,
  `users.guardian_consent_at` (16 хүрээгүй бол), `users.deletion_scheduled_at`
  (устгах хүсэлтээс 2 цагийн дараа).
- `payments.user_id` — `ON DELETE SET NULL`: бүртгэл устахад төлбөрийн
  бүртгэл хуулийн хугацаанд үлдэнэ.

Revision ID: 9a4c7e1f3b58
Revises: 3e8b5f2a9c71
Create Date: 2026-09-28 14:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "9a4c7e1f3b58"
down_revision: str | Sequence[str] | None = "3e8b5f2a9c71"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "users", sa.Column("email_verified_at", sa.DateTime(timezone=True), nullable=True)
    )
    op.add_column("users", sa.Column("pending_email", sa.String(length=255), nullable=True))
    op.add_column(
        "users",
        sa.Column("profile_hidden", sa.Boolean(), server_default=sa.false(), nullable=False),
    )
    op.add_column(
        "users", sa.Column("terms_accepted_at", sa.DateTime(timezone=True), nullable=True)
    )
    op.add_column(
        "users", sa.Column("guardian_consent_at", sa.DateTime(timezone=True), nullable=True)
    )
    op.add_column(
        "users", sa.Column("deletion_scheduled_at", sa.DateTime(timezone=True), nullable=True)
    )
    op.execute("UPDATE users SET email_verified_at = created_at")

    op.drop_constraint(op.f("fk_payments_user_id_users"), "payments", type_="foreignkey")
    op.alter_column("payments", "user_id", existing_type=sa.UUID(), nullable=True)
    op.create_foreign_key(
        op.f("fk_payments_user_id_users"),
        "payments",
        "users",
        ["user_id"],
        ["id"],
        ondelete="SET NULL",
    )


def downgrade() -> None:
    op.drop_constraint(op.f("fk_payments_user_id_users"), "payments", type_="foreignkey")
    op.execute("DELETE FROM payments WHERE user_id IS NULL")
    op.alter_column("payments", "user_id", existing_type=sa.UUID(), nullable=False)
    op.create_foreign_key(
        op.f("fk_payments_user_id_users"),
        "payments",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.drop_column("users", "deletion_scheduled_at")
    op.drop_column("users", "guardian_consent_at")
    op.drop_column("users", "terms_accepted_at")
    op.drop_column("users", "profile_hidden")
    op.drop_column("users", "pending_email")
    op.drop_column("users", "email_verified_at")
