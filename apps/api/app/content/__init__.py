"""Сургалтын агуулга.

Агуулгыг seed-ийн логикоос тусгаарласан: энд зөвхөн хичээлийн текст,
код байх бөгөөд өгөгдлийн сангийн ажиллагаа `app/seed.py` дотор байна.

Каталог нь шинэ сургалтыг эхэнд харуулдаг тул жагсаалтын **төгсгөлд**
байгаа сургалт нүүр хуудсанд түрүүлж гарна.
"""

from app.content.c_cpp import C_CPP_COURSE
from app.content.flowgorithm import FLOWGORITHM_COURSE
from app.content.git_github import GIT_COURSE
from app.content.html_css import HTML_COURSE
from app.content.javascript import JS_COURSE
from app.content.python import PYTHON_COURSE
from app.content.react import REACT_COURSE
from app.content.sql import SQL_COURSE
from app.content.types import CourseSpec, LessonSpec, ModuleSpec

COURSES: list[CourseSpec] = [
    REACT_COURSE,
    SQL_COURSE,
    GIT_COURSE,
    C_CPP_COURSE,
    HTML_COURSE,
    PYTHON_COURSE,
    JS_COURSE,
    FLOWGORITHM_COURSE,
]

__all__ = [
    "COURSES",
    "C_CPP_COURSE",
    "FLOWGORITHM_COURSE",
    "GIT_COURSE",
    "HTML_COURSE",
    "JS_COURSE",
    "PYTHON_COURSE",
    "REACT_COURSE",
    "SQL_COURSE",
    "CourseSpec",
    "LessonSpec",
    "ModuleSpec",
]
