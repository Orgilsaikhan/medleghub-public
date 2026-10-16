"""JavaScript сургалтын анхны агуулга алдагдаагүйг баталгаажуулна.

Сургалт нь 3 модулиас 26 болж өргөжсөн.
Гэхдээ анхны 6 хичээл нь E2E тестүүдийн тулгуур цэг хэвээр байгаа тул
тэдгээрийн slug болон агуулга өөрчлөгдөөгүй байх ёстой.
"""

from app.content import COURSES
from app.content.javascript import JS_COURSE

# Эдгээр нь E2E тест болон marketing хуудаснаас шууд заагддаг тул устгаж
# эсвэл нэрийг нь солиж БОЛОХГҮЙ.
ANHNY_LESSON_SLUGS = [
    "tanilzuulga",
    "huvisagch",
    "ugugdliin-turul",
    "funkts",
    "parametr",
    "byatshan-tusul",
]


def _lesson(slug: str):
    return next(
        lesson for module in JS_COURSE.modules for lesson in module.lessons if lesson.slug == slug
    )


def test_javascript_course_identity_is_unchanged() -> None:
    """Slug болон гарчгийг E2E harness-ийн `SEED.course` заадаг."""
    assert JS_COURSE.slug == "javascript-undes"
    assert JS_COURSE.title == "JavaScript үндэс"


def test_original_lessons_still_exist() -> None:
    slugs = [lesson.slug for module in JS_COURSE.modules for lesson in module.lessons]
    for slug in ANHNY_LESSON_SLUGS:
        assert slug in slugs, f"{slug} хичээл алга болсон"


def test_first_lesson_is_the_introduction() -> None:
    """`course-completion.spec.mjs` нь энэ хичээлээс эхэлж сургалтыг дуусгадаг."""
    assert JS_COURSE.modules[0].lessons[0].slug == "tanilzuulga"


def test_javascript_lesson_content_survived() -> None:
    """E2E тестүүд эдгээр яг утгуудыг шалгадаг."""
    huvisagch = _lesson("huvisagch")
    assert 'const ner = "Бат";' in huvisagch.initial_code
    assert "Сайн байна уу, " in huvisagch.initial_code
    assert "Хувьсагч нь утга хадгалах зориулалттай" in huvisagch.content


def test_course_order_puts_javascript_first_in_catalog() -> None:
    """Каталог нь шинэ сургалтыг эхэнд харуулдаг тул туг сургалт сүүлд үүснэ."""
    assert COURSES[-1].slug == "javascript-undes"


def test_every_course_has_a_description() -> None:
    for course in COURSES:
        assert course.description.strip(), f"{course.slug} тайлбаргүй"
