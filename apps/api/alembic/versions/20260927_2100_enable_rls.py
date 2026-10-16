"""Бүх хүснэгтэд row level security асаах

Supabase нь `public` schema-гийн хүснэгт бүрийг Data API (PostgREST)-ээр
нээдэг бөгөөд `anon` түлхүүр нь нийтэд зориулагдсан. RLS-гүй бол `users`
(имэйл, нууц үгийн hash), `payments` зэрэг нь интернэтээс уншигдана.

RLS-ийг ДҮРЭМГҮЙГЭЭР асаана — `anon`/`authenticated` юу ч харахгүй. Манай API
нь хүснэгтийн ЭЗЭН (миграц ажиллуулсан) role-оор холбогддог тул RLS түүнд
үйлчлэхгүй (`FORCE ROW LEVEL SECURITY` ашиглаагүй). Энгийн Postgres дээр ч
(хөгжүүлэлт, CI) ажиллагаа өөрчлөгдөхгүй.

ШИНЭ ХҮСНЭГТ нэмэх миграц бүр түүнд `ENABLE ROW LEVEL SECURITY` хийнэ.

Revision ID: c8e3f5a1d7b2
Revises: b4d7e1c9a2f6
Create Date: 2026-09-27 21:00:00.000000

"""

from collections.abc import Sequence

from alembic import op

revision: str = "c8e3f5a1d7b2"
down_revision: str | Sequence[str] | None = "b4d7e1c9a2f6"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _all_tables(action: str) -> None:
    # `alembic_version` ч орно — одоогийн schema-гийн бүх энгийн хүснэгт.
    op.execute(
        f"""
        DO $$
        DECLARE t record;
        BEGIN
            FOR t IN SELECT tablename FROM pg_tables WHERE schemaname = current_schema() LOOP
                EXECUTE format('ALTER TABLE %I {action} ROW LEVEL SECURITY', t.tablename);
            END LOOP;
        END $$;
        """
    )


def upgrade() -> None:
    _all_tables("ENABLE")


def downgrade() -> None:
    _all_tables("DISABLE")
