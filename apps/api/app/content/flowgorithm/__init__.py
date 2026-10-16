"""Өмнөх мэдлэггүй суралцагчийн Flowgorithm сургалт.

Хичээл бүр сайт дотор засварлаж, ажиллуулж болох блок схемтэй.
"""

from dataclasses import replace

from app.content.flowgorithm.data import DATA_MODULES
from app.content.flowgorithm.decisions import DECISION_MODULES
from app.content.flowgorithm.diagrams import lesson_diagram
from app.content.flowgorithm.fundamentals import FUNDAMENTAL_MODULES
from app.content.flowgorithm.loops_projects import LOOP_PROJECT_MODULES
from app.content.types import CourseSpec
from app.models.enums import Category, Difficulty

FLOWGORITHM_COURSE = CourseSpec(
    title="Flowgorithm — програмчлалын анхны алхам",
    slug="flowgorithm-undes",
    description=(
        "Огт програмчлал мэдэхгүй хүнд зориулсан 24 хичээл. Өдөр тутмын жишээгээр "
        "алгоритм ойлгож, блок схем зурж, хувьсагч, оролт/гаралт, нөхцөл, давталтыг "
        "алхам алхмаар сурна. Хичээл бүр автоматаар шалгагддаг даалгавартай, хоёр жижиг төсөлтэй. "
        "Монгол тайлбараа уншаад блок схемээ сайт дотроо байгуулж, ажиллуулна. "
        "Input, Output, If, давталт, алхмаар ажиллуулах боломжтой. Өмнөх мэдлэг шаардахгүй."
    ),
    difficulty=Difficulty.BEGINNER,
    category=Category.FLOWGORITHM,
    modules=[
        replace(
            module,
            lessons=[
                replace(lesson, initial_code=lesson_diagram(lesson.slug))
                for lesson in module.lessons
            ],
        )
        for module in [
            *FUNDAMENTAL_MODULES,
            *DATA_MODULES,
            *DECISION_MODULES,
            *LOOP_PROJECT_MODULES,
        ]
    ],
)
