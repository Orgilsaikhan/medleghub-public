"""Community — нийтлэл, сэтгэгдэл, лайк, дүрэм, түдгэлзүүлэлт; `report` төрөл

- `community_posts` — хэрэглэгчийн (эсвэл `author_id` NULL бол MedlegHub-ийн)
  нийтлэл, хэл ба төрлийн шошготой.
- `community_comments` — нийтлэлийн сэтгэгдэл.
- `community_post_likes` — хэрэглэгч нэг нийтлэлд нэг лайк.
- `community_suspensions` — дүрэм зөрчсөн хэрэглэгчийн түдгэлзүүлэлтийн түүх.
- `users.community_guidelines_accepted_at` — Community-ийн дүрмийг зөвшөөрсөн мөч.
- `feedback.kind` — Community-ийн гомдол `report` төрлөөр орно.

Хэрэглэгч устахад түүний нийтлэл, сэтгэгдэл, лайк, түдгэлзүүлэлт хамт устана. Шинэ хүснэгт
бүрт RLS асаалттай (`20260927_2100_enable_rls.py`-г үз).

Revision ID: e7a3c1f94b26
Revises: c4e9a7b2d813
Create Date: 2026-09-28 22:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "e7a3c1f94b26"
down_revision: str | Sequence[str] | None = "c4e9a7b2d813"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

LANGUAGES = (
    "python",
    "c",
    "cpp",
    "javascript",
    "html_css",
    "sql",
    "java",
    "csharp",
    "flowgorithm",
    "general",
)
TYPES = ("discussion", "help", "fun_fact")


def _in(column: str, values: Sequence[str]) -> str:
    return f"{column} IN ('" + "','".join(values) + "')"


def upgrade() -> None:
    op.create_table(
        "community_posts",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("author_id", sa.UUID(), nullable=True),
        sa.Column("title", sa.String(length=150), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("language", sa.String(length=20), nullable=False),
        sa.Column("type", sa.String(length=20), nullable=False),
        sa.Column("pinned", sa.Boolean(), server_default=sa.false(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            _in("language", LANGUAGES), name=op.f("ck_community_posts_language_valid")
        ),
        sa.CheckConstraint(_in("type", TYPES), name=op.f("ck_community_posts_type_valid")),
        sa.ForeignKeyConstraint(
            ["author_id"],
            ["users.id"],
            name=op.f("fk_community_posts_author_id_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_community_posts")),
    )
    op.create_index(
        op.f("ix_community_posts_author_id"), "community_posts", ["author_id"], unique=False
    )
    op.execute("ALTER TABLE community_posts ENABLE ROW LEVEL SECURITY")

    op.create_table(
        "community_comments",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("post_id", sa.UUID(), nullable=False),
        sa.Column("author_id", sa.UUID(), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["post_id"],
            ["community_posts.id"],
            name=op.f("fk_community_comments_post_id_community_posts"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["author_id"],
            ["users.id"],
            name=op.f("fk_community_comments_author_id_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_community_comments")),
    )
    op.create_index(
        op.f("ix_community_comments_post_id"), "community_comments", ["post_id"], unique=False
    )
    op.create_index(
        op.f("ix_community_comments_author_id"),
        "community_comments",
        ["author_id"],
        unique=False,
    )
    op.execute("ALTER TABLE community_comments ENABLE ROW LEVEL SECURITY")

    op.create_table(
        "community_post_likes",
        sa.Column("post_id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["post_id"],
            ["community_posts.id"],
            name=op.f("fk_community_post_likes_post_id_community_posts"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_community_post_likes_user_id_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("post_id", "user_id", name=op.f("pk_community_post_likes")),
    )
    op.create_index(
        op.f("ix_community_post_likes_user_id"),
        "community_post_likes",
        ["user_id"],
        unique=False,
    )
    op.execute("ALTER TABLE community_post_likes ENABLE ROW LEVEL SECURITY")

    op.create_table(
        "community_suspensions",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("admin_id", sa.UUID(), nullable=True),
        sa.Column("level", sa.Integer(), nullable=False),
        sa.Column("reason", sa.String(length=500), nullable=False),
        sa.Column("ends_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("lifted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint("level >= 1", name=op.f("ck_community_suspensions_level_positive")),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_community_suspensions_user_id_users"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["admin_id"],
            ["users.id"],
            name=op.f("fk_community_suspensions_admin_id_users"),
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_community_suspensions")),
    )
    op.create_index(
        op.f("ix_community_suspensions_user_id"),
        "community_suspensions",
        ["user_id"],
        unique=False,
    )
    op.execute("ALTER TABLE community_suspensions ENABLE ROW LEVEL SECURITY")

    op.add_column(
        "users",
        sa.Column("community_guidelines_accepted_at", sa.DateTime(timezone=True), nullable=True),
    )

    op.drop_constraint(op.f("ck_feedback_kind_valid"), "feedback", type_="check")
    op.create_check_constraint(
        op.f("ck_feedback_kind_valid"), "feedback", "kind IN ('idea','bug','other','report')"
    )


def downgrade() -> None:
    op.execute("DELETE FROM feedback WHERE kind = 'report'")
    op.drop_constraint(op.f("ck_feedback_kind_valid"), "feedback", type_="check")
    op.create_check_constraint(
        op.f("ck_feedback_kind_valid"), "feedback", "kind IN ('idea','bug','other')"
    )

    op.drop_column("users", "community_guidelines_accepted_at")
    op.drop_index(op.f("ix_community_suspensions_user_id"), table_name="community_suspensions")
    op.drop_table("community_suspensions")

    op.drop_index(op.f("ix_community_post_likes_user_id"), table_name="community_post_likes")
    op.drop_table("community_post_likes")
    op.drop_index(op.f("ix_community_comments_author_id"), table_name="community_comments")
    op.drop_index(op.f("ix_community_comments_post_id"), table_name="community_comments")
    op.drop_table("community_comments")
    op.drop_index(op.f("ix_community_posts_author_id"), table_name="community_posts")
    op.drop_table("community_posts")
