"""Өгөгдлийн Сангийн Үндэс (MySQL) сургалт.

Модул 0-ээс 20 хүртэл — өгөгдлийн сангийн үндэс, асуулга, хүснэгт ба
хязгаарлалт, JOIN, дизайн, transaction, ахисан сэдэв, төслүүд.

Slug нь `mssql-mysql-undes` хэвээр — өмнө нь MySQL ба SQL Server хоёрыг
заадаг байсан. Slug солибол бүртгэл, ахиц холбоосоо алдана. Хичээлийн slug
(`tsql-…`, `limit-top-offset-fetch` г.м.) мөн адил шалтгаанаар хэвээр.

КОД АЖИЛЛУУЛАХ: хичээл бүр `mysql` — кодыг `apps/sql-runner` үйлчилгээ
тусгаарлагдсан MySQL 8.4 сервер дээр ажиллуулна. Ажиллагаа бүр `delguur`,
`nomiin_san` жишээ сангууд анхны төлөвтэй бэлэн серверээс эхэлнэ. Анхны код
бүр нь суралцагч MySQL Workbench / `mysql` дээр хуулж шууд ажиллуулах бүрэн
скрипт.

Жишээ сан үүсгэдэг хоёр хичээлийн (`delguur-san-mysql`,
`nomiin-san-zagvar-mysql`) анхны кодыг өөрчилбөл `apps/sql-runner/sandbox/`
доторх хуулбарыг мөн шинэчилнэ — ажиллуулагч сангуудыг тэндээс ачаална
(`apps/api/tests/test_sql_run.py` шалгана).

Ихэнх хичээл Модул 1-ийн `delguur` жишээ санг ашиглах бөгөөд түүний
өгөгдлийг байнгын өөрчлөхгүй — түр хүснэгт эсвэл ROLLBACK.

МӨРДӨГЧИЙН ХЭРЭГ: Модул 1–20 бүр нэг хэргээр төгсөж, Модул 21 нь гурван
хэсэгтэй төгсгөлийн хэрэг (`cases.py`, сан `medleg_hot`). Сурагч асуулгаар
хариултыг олж бичнэ — API шалгана.
"""

from dataclasses import replace

from app.content.sql.advanced import SQL_ADVANCED_MODULES
from app.content.sql.cases import FINALE, MODULE_CASES
from app.content.sql.data_definition import SQL_DEFINITION_MODULES
from app.content.sql.design import SQL_DESIGN_MODULES
from app.content.sql.fundamentals import SQL_FUNDAMENTAL_MODULES
from app.content.sql.joins import SQL_JOIN_MODULES
from app.content.sql.projects import SQL_PROJECT_MODULES
from app.content.sql.querying import SQL_QUERY_MODULES
from app.content.types import CourseSpec, ModuleSpec
from app.models.enums import Category, Difficulty

_MODULES: list[ModuleSpec] = [
    *SQL_FUNDAMENTAL_MODULES,
    *SQL_QUERY_MODULES,
    *SQL_DEFINITION_MODULES,
    *SQL_JOIN_MODULES,
    *SQL_DESIGN_MODULES,
    *SQL_ADVANCED_MODULES,
    *SQL_PROJECT_MODULES,
]


def _with_case(number: int, module: ModuleSpec) -> ModuleSpec:
    """Модулийн төгсгөлд тухайн модулийн хэргийг нэмнэ (Модул 0-д хэрэггүй)."""
    case = MODULE_CASES.get(number)
    return replace(module, lessons=[*module.lessons, case]) if case else module


SQL_COURSE = CourseSpec(
    title="Өгөгдлийн Сангийн Үндэс (MySQL)",
    slug="mssql-mysql-undes",
    description=(
        "Хамгийн өргөн хэрэглэгддэг өгөгдлийн сан MySQL дээр SQL-ийг эхнээс "
        "нь сурна. SELECT, JOIN, бүлэглэлээс эхлээд хүснэгтийн дизайн, index, "
        "transaction, window функц, stored procedure хүртэл. Код бүрийг энд "
        "шууд ажиллуулна. Модул бүр мөрдөгчийн хэргээр төгсөнө: асуулгаар "
        "нотлох баримт хайж, гэмт хэргийг илрүүлнэ. Өмнөх мэдлэг шаардахгүй."
    ),
    difficulty=Difficulty.BEGINNER,
    category=Category.DATABASE,
    modules=[*(_with_case(number, module) for number, module in enumerate(_MODULES)), FINALE],
    # Үнэгүй хэсэг: «Модул 3 — WHERE шүүлт» хэргээ оруулаад дуустал. Үлдсэн нь Standard багц.
    is_free=False,
    free_lessons=14,
)
