"""lessons.language дээр mysql, sql нэмэх

MSSQL/MySQL сургалт нэмэгдсэнтэй холбоотой. `sql` нь Monaco-ийн T-SQL
(SQL Server) горим, `mysql` нь MySQL горим — `app/models/enums.py` дахь
тайлбарыг үзнэ үү.

Revision ID: d5e8a1f37c02
Revises: b3c47d92e1a8
Create Date: 2026-09-14 12:00:00.000000

"""

from collections.abc import Sequence

from alembic import op

revision: str = "d5e8a1f37c02"
down_revision: str | Sequence[str] | None = "b3c47d92e1a8"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

# Нэршлийн конвенц нь `ck_%(table_name)s_` угтварыг ӨӨРӨӨ нэмнэ —
# энд зөвхөн суурь нэрийг бичнэ, эс бөгөөс `ck_lessons_ck_lessons_…` болно.
CONSTRAINT = "language_valid"

OLD = "language IN ('javascript','html','css','python','c','cpp','shell')"
NEW = "language IN ('javascript','html','css','python','c','cpp','shell','mysql','sql')"


def upgrade() -> None:
    op.drop_constraint(CONSTRAINT, "lessons", type_="check")
    op.create_check_constraint(CONSTRAINT, "lessons", NEW)


def downgrade() -> None:
    # Буцаахын өмнө шинэ хэлтэй хичээл үлдсэн бол CHECK нь амжилтгүй болно.
    # Тиймээс эхлээд тэдгээрийг устгана — агуулга нь `app/content/` дотор
    # хэвээр байгаа тул seed дахин үүсгэнэ.
    op.execute("DELETE FROM lessons WHERE language IN ('mysql','sql')")
    op.drop_constraint(CONSTRAINT, "lessons", type_="check")
    op.create_check_constraint(CONSTRAINT, "lessons", OLD)
