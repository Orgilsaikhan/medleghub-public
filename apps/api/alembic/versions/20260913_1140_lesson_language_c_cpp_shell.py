"""lessons.language дээр c, cpp, shell нэмэх

C & C++ болон Git & GitHub сургалт нэмэгдсэнтэй холбоотой. Утгууд нь
Monaco-ийн хэлний ID-тай таарна — `app/models/enums.py` дахь тайлбарыг үзнэ үү.

Revision ID: b3c47d92e1a8
Revises: 9f1f75711fed
Create Date: 2026-09-13 11:40:00.000000

"""

from collections.abc import Sequence

from alembic import op

revision: str = "b3c47d92e1a8"
down_revision: str | Sequence[str] | None = "9f1f75711fed"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

# Нэршлийн конвенц нь `ck_%(table_name)s_` угтварыг ӨӨРӨӨ нэмнэ —
# энд зөвхөн суурь нэрийг бичнэ, эс бөгөөс `ck_lessons_ck_lessons_…` болно.
CONSTRAINT = "language_valid"

OLD = "language IN ('javascript','html','css','python')"
NEW = "language IN ('javascript','html','css','python','c','cpp','shell')"


def upgrade() -> None:
    op.drop_constraint(CONSTRAINT, "lessons", type_="check")
    op.create_check_constraint(CONSTRAINT, "lessons", NEW)


def downgrade() -> None:
    # Буцаахын өмнө шинэ хэлтэй хичээл үлдсэн бол CHECK нь амжилтгүй болно.
    # Тиймээс эхлээд тэдгээрийг устгана — агуулга нь `app/content/` дотор
    # хэвээр байгаа тул seed дахин үүсгэнэ.
    op.execute("DELETE FROM lessons WHERE language IN ('c','cpp','shell')")
    op.drop_constraint(CONSTRAINT, "lessons", type_="check")
    op.create_check_constraint(CONSTRAINT, "lessons", OLD)
