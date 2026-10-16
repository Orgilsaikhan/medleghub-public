"""Нэг удаагийн Live эрх

- `live_passes` — багцгүй хэрэглэгчийн нэг материалд зориулсан эрх. Ашиглаагүй бол
  хугацаагүй; материалд ашигласнаас хойш `live_pass_access_days` хоног.
- `payments.plan` / `plan_prices.plan` — `live_pass` нэмэгдэнэ (эрхийн төлбөр,
  админы тавьсан эрхийн үнэ).
- `payments.months` — эрхийн төлбөрт 0, багцад өмнөх шигээ ≥ 1.
- `payments.live_pass_id`, `payments.credit_mnt` — эрхийн төлбөрөөс үүссэн эрх, эсвэл
  багц авахад үнэ нь хасагдсан эрх ба хасагдсан дүн.

Одоо байгаа мөрүүд өөрчлөгдөхгүй (шинэ багана анхдагч утгатай). Шинэ хүснэгтэд RLS.

Revision ID: a2f3b018d9a5
Revises: 5e2b9c4d7a18
Create Date: 2026-10-03 12:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "a2f3b018d9a5"
down_revision: str | Sequence[str] | None = "5e2b9c4d7a18"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

PLANS_BEFORE = "plan IN ('standard','premium')"
PLANS_AFTER = "plan IN ('standard','premium','live_pass')"


def upgrade() -> None:
    op.create_table(
        "live_passes",
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("price_mnt", sa.Integer(), nullable=False),
        sa.Column("material_id", sa.UUID(), nullable=True),
        sa.Column("used_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("upgraded_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint("price_mnt >= 0", name=op.f("ck_live_passes_price_nonnegative")),
        sa.CheckConstraint(
            "(used_at IS NULL) = (expires_at IS NULL)",
            name=op.f("ck_live_passes_used_has_expiry"),
        ),
        sa.ForeignKeyConstraint(
            ["material_id"],
            ["live_materials.id"],
            name=op.f("fk_live_passes_material_id_live_materials"),
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_live_passes_user_id_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_live_passes")),
        sa.UniqueConstraint("material_id", name=op.f("uq_live_passes_material_id")),
    )
    op.create_index(
        "ix_live_passes_user_created", "live_passes", ["user_id", "created_at"], unique=False
    )
    op.execute("ALTER TABLE live_passes ENABLE ROW LEVEL SECURITY")

    for table in ("payments", "plan_prices"):
        op.drop_constraint(op.f(f"ck_{table}_plan_valid"), table, type_="check")
        op.create_check_constraint(op.f(f"ck_{table}_plan_valid"), table, PLANS_AFTER)

    op.drop_constraint(op.f("ck_payments_months_positive"), "payments", type_="check")
    op.create_check_constraint(
        op.f("ck_payments_months_valid"),
        "payments",
        "CASE WHEN plan = 'live_pass' THEN months = 0 ELSE months >= 1 END",
    )
    op.add_column("payments", sa.Column("live_pass_id", sa.UUID(), nullable=True))
    op.add_column(
        "payments",
        sa.Column("credit_mnt", sa.Integer(), server_default="0", nullable=False),
    )
    op.create_check_constraint(
        op.f("ck_payments_credit_mnt_nonnegative"), "payments", "credit_mnt >= 0"
    )
    op.create_foreign_key(
        op.f("fk_payments_live_pass_id_live_passes"),
        "payments",
        "live_passes",
        ["live_pass_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_index(op.f("ix_payments_live_pass_id"), "payments", ["live_pass_id"], unique=False)


def downgrade() -> None:
    # Эрхийн төлбөрүүд хуучин CHECK-д таарахгүй — буцаахаас өмнө устгана.
    op.execute("DELETE FROM payments WHERE plan = 'live_pass'")
    op.execute("DELETE FROM plan_prices WHERE plan = 'live_pass'")
    op.drop_index(op.f("ix_payments_live_pass_id"), table_name="payments")
    op.drop_constraint(op.f("fk_payments_live_pass_id_live_passes"), "payments", type_="foreignkey")
    op.drop_constraint(op.f("ck_payments_credit_mnt_nonnegative"), "payments", type_="check")
    op.drop_column("payments", "credit_mnt")
    op.drop_column("payments", "live_pass_id")
    op.drop_constraint(op.f("ck_payments_months_valid"), "payments", type_="check")
    op.create_check_constraint(op.f("ck_payments_months_positive"), "payments", "months >= 1")
    for table in ("payments", "plan_prices"):
        op.drop_constraint(op.f(f"ck_{table}_plan_valid"), table, type_="check")
        op.create_check_constraint(op.f(f"ck_{table}_plan_valid"), table, PLANS_BEFORE)
    op.drop_index("ix_live_passes_user_created", table_name="live_passes")
    op.drop_table("live_passes")
