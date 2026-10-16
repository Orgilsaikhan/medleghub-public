"""Промо код ба найзаа урих хөтөлбөр

- `promo_codes` — админы үүсгэсэн код: хувийн хөнгөлөлт эсвэл үнэгүй сар,
  дуусах хугацаа, ашиглах дээд тоо.
- `promo_redemptions` — хэрэглэгч кодыг ашигласан удаа (хэрэглэгч × код нэг).
- `referrals` — хэн хэнийг урьсан, найзын хөнгөлөлт, найз анх хэзээ төлсөн,
  урьсан хүнд олгосон сар.
- `users.referral_code` — хэрэглэгчийн урилгын код. Одоо байгаа хэрэглэгч
  бүрд санамсаргүй код үүсгэнэ.
- `payments` — хөнгөлөлтийн хувь, дүн, промо код, урилгын хөнгөлөлт.

Шинэ хүснэгт бүр RLS асаалттай (`20260927_2100_enable_rls.py`-г үз).

Revision ID: 8ef64d74047a
Revises: f2b8d4c6a913
Create Date: 2026-09-30 12:00:00.000000

"""

import secrets
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "8ef64d74047a"
down_revision: str | Sequence[str] | None = "f2b8d4c6a913"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

# `app/services/promo_service.py`-тэй ижил: 0/O, 1/I-гүй.
CODE_ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"


def _created_at() -> sa.Column:
    return sa.Column(
        "created_at",
        sa.DateTime(timezone=True),
        server_default=sa.text("now()"),
        nullable=False,
    )


def upgrade() -> None:
    op.create_table(
        "promo_codes",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("code", sa.String(length=32), nullable=False),
        sa.Column("kind", sa.String(length=20), nullable=False),
        sa.Column("percent_off", sa.Integer(), nullable=True),
        sa.Column("free_months", sa.Integer(), nullable=True),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("max_uses", sa.Integer(), nullable=True),
        sa.Column("active", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column("note", sa.String(length=500), nullable=True),
        sa.Column("created_by", sa.UUID(), nullable=True),
        _created_at(),
        sa.CheckConstraint(
            "kind IN ('percent','free_months')", name=op.f("ck_promo_codes_kind_valid")
        ),
        sa.CheckConstraint(
            "(kind = 'percent' AND percent_off BETWEEN 1 AND 99 AND free_months IS NULL)"
            " OR (kind = 'free_months' AND free_months >= 1 AND percent_off IS NULL)",
            name=op.f("ck_promo_codes_value_matches_kind"),
        ),
        sa.CheckConstraint(
            "max_uses IS NULL OR max_uses >= 1", name=op.f("ck_promo_codes_max_uses_positive")
        ),
        sa.ForeignKeyConstraint(
            ["created_by"],
            ["users.id"],
            name=op.f("fk_promo_codes_created_by_users"),
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_promo_codes")),
        sa.UniqueConstraint("code", name=op.f("uq_promo_codes_code")),
    )
    op.execute("ALTER TABLE promo_codes ENABLE ROW LEVEL SECURITY")

    op.create_table(
        "referrals",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("referrer_id", sa.UUID(), nullable=False),
        sa.Column("friend_id", sa.UUID(), nullable=True),
        sa.Column("signup_confirmed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("discount_used_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("first_paid_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("months_rewarded", sa.Integer(), server_default="0", nullable=False),
        _created_at(),
        sa.CheckConstraint(
            "months_rewarded >= 0", name=op.f("ck_referrals_months_rewarded_nonnegative")
        ),
        sa.ForeignKeyConstraint(
            ["referrer_id"],
            ["users.id"],
            name=op.f("fk_referrals_referrer_id_users"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["friend_id"],
            ["users.id"],
            name=op.f("fk_referrals_friend_id_users"),
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_referrals")),
        sa.UniqueConstraint("friend_id", name=op.f("uq_referrals_friend_id")),
    )
    op.create_index(op.f("ix_referrals_referrer_id"), "referrals", ["referrer_id"], unique=False)
    op.execute("ALTER TABLE referrals ENABLE ROW LEVEL SECURITY")

    op.add_column(
        "payments",
        sa.Column("discount_percent", sa.Integer(), server_default="0", nullable=False),
    )
    op.add_column(
        "payments", sa.Column("discount_mnt", sa.Integer(), server_default="0", nullable=False)
    )
    op.add_column("payments", sa.Column("promo_code_id", sa.UUID(), nullable=True))
    op.add_column("payments", sa.Column("referral_id", sa.UUID(), nullable=True))
    op.create_check_constraint(
        op.f("ck_payments_discount_percent_valid"), "payments", "discount_percent BETWEEN 0 AND 99"
    )
    op.create_check_constraint(
        op.f("ck_payments_discount_mnt_nonnegative"), "payments", "discount_mnt >= 0"
    )
    op.create_foreign_key(
        op.f("fk_payments_promo_code_id_promo_codes"),
        "payments",
        "promo_codes",
        ["promo_code_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_foreign_key(
        op.f("fk_payments_referral_id_referrals"),
        "payments",
        "referrals",
        ["referral_id"],
        ["id"],
        ondelete="SET NULL",
    )

    op.create_table(
        "promo_redemptions",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("promo_code_id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=True),
        sa.Column("payment_id", sa.UUID(), nullable=True),
        sa.Column("months", sa.Integer(), nullable=True),
        _created_at(),
        sa.ForeignKeyConstraint(
            ["promo_code_id"],
            ["promo_codes.id"],
            name=op.f("fk_promo_redemptions_promo_code_id_promo_codes"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_promo_redemptions_user_id_users"),
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["payment_id"],
            ["payments.id"],
            name=op.f("fk_promo_redemptions_payment_id_payments"),
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_promo_redemptions")),
        sa.UniqueConstraint("promo_code_id", "user_id", name="uq_promo_redemptions_code_user"),
    )
    op.create_index(
        op.f("ix_promo_redemptions_promo_code_id"),
        "promo_redemptions",
        ["promo_code_id"],
        unique=False,
    )
    op.execute("ALTER TABLE promo_redemptions ENABLE ROW LEVEL SECURITY")

    op.add_column("users", sa.Column("referral_code", sa.String(length=16), nullable=True))
    op.create_unique_constraint(op.f("uq_users_referral_code"), "users", ["referral_code"])

    # Одоо байгаа хэрэглэгчид хэрэглэгчийн цэснээс кодоо шууд харна.
    bind = op.get_bind()
    user_ids = bind.execute(sa.text("SELECT id FROM users")).scalars().all()
    used: set[str] = set()
    for user_id in user_ids:
        code = "".join(secrets.choice(CODE_ALPHABET) for _ in range(8))
        while code in used:
            code = "".join(secrets.choice(CODE_ALPHABET) for _ in range(8))
        used.add(code)
        bind.execute(
            sa.text("UPDATE users SET referral_code = :code WHERE id = :id"),
            {"code": code, "id": user_id},
        )


def downgrade() -> None:
    op.drop_constraint(op.f("uq_users_referral_code"), "users", type_="unique")
    op.drop_column("users", "referral_code")

    op.drop_index(op.f("ix_promo_redemptions_promo_code_id"), table_name="promo_redemptions")
    op.drop_table("promo_redemptions")

    op.drop_constraint(op.f("fk_payments_referral_id_referrals"), "payments", type_="foreignkey")
    op.drop_constraint(
        op.f("fk_payments_promo_code_id_promo_codes"), "payments", type_="foreignkey"
    )
    op.drop_constraint(op.f("ck_payments_discount_mnt_nonnegative"), "payments", type_="check")
    op.drop_constraint(op.f("ck_payments_discount_percent_valid"), "payments", type_="check")
    op.drop_column("payments", "referral_id")
    op.drop_column("payments", "promo_code_id")
    op.drop_column("payments", "discount_mnt")
    op.drop_column("payments", "discount_percent")

    op.drop_index(op.f("ix_referrals_referrer_id"), table_name="referrals")
    op.drop_table("referrals")
    op.drop_table("promo_codes")
