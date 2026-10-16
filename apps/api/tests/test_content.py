"""Сургалтын агуулгын бүрэн бүтэн байдлыг шалгана.

Агуулга нь код биш өгөгдөл боловч алдаа нь шууд хэрэглэгчид хүрдэг тул
автоматаар шалгах нь зүйтэй.
"""

import ast
import json
import re
from html.parser import HTMLParser

import pytest

from app.content import COURSES
from app.content.c_cpp import C_CPP_COURSE
from app.content.flowgorithm import FLOWGORITHM_COURSE
from app.content.git_github import GIT_COURSE
from app.content.html_css import HTML_COURSE
from app.content.html_css.common import parse_files
from app.content.javascript import JS_COURSE
from app.content.python import PYTHON_COURSE
from app.content.sql import SQL_COURSE
from app.content.types import CourseSpec, LessonSpec
from app.models.enums import LessonLanguage

SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

ALL_LESSONS = [
    (course, module, lesson)
    for course in COURSES
    for module in course.modules
    for lesson in module.lessons
]


def test_course_slugs_are_unique_and_valid() -> None:
    slugs = [course.slug for course in COURSES]
    assert len(slugs) == len(set(slugs)), "Сургалтын slug давхардсан"
    for slug in slugs:
        assert SLUG_PATTERN.match(slug), f"Буруу slug: {slug}"


@pytest.mark.parametrize("course", COURSES, ids=lambda course: course.slug)
def test_lesson_slugs_unique_within_course(course: CourseSpec) -> None:
    """Slug нь курс дотор давтагдвал `/learn/:course/:lesson` тодорхойгүй болно."""
    slugs = [lesson.slug for module in course.modules for lesson in module.lessons]
    davhardal = {slug for slug in slugs if slugs.count(slug) > 1}
    assert not davhardal, f"{course.slug} дотор давхардсан: {davhardal}"


PAID_COURSES = [course for course in COURSES if not course.is_free and course.lesson_count]


@pytest.mark.parametrize("course", PAID_COURSES, ids=lambda course: course.slug)
def test_free_lessons_end_on_a_module_boundary(course: CourseSpec) -> None:
    """Модулийн дундуур үнэгүй/төлбөрт гэж хуваагдахгүй.

    Хичээл нэмж, хасахад тасалбар шилжиж болох тул энд барина — тэгвэл
    `free_lessons`-ийг шинэ хил рүү нь зөөнө.
    """
    boundaries, total = [], 0
    for module in course.modules:
        total += len(module.lessons)
        boundaries.append(total)
    assert course.free_lessons in boundaries, (
        f"{course.slug}: free_lessons={course.free_lessons} модулийн хил биш {boundaries}"
    )
    assert 0 < course.free_lessons < course.lesson_count


@pytest.mark.parametrize(
    ("course", "module", "lesson"),
    ALL_LESSONS,
    ids=[f"{c.slug}/{lsn.slug}" for c, _, lsn in ALL_LESSONS],
)
def test_lesson_fields_are_sane(course: CourseSpec, module: object, lesson: object) -> None:
    assert SLUG_PATTERN.match(lesson.slug), f"Буруу slug: {lesson.slug}"
    assert lesson.title.strip(), "Гарчиг хоосон"
    assert lesson.content.strip(), "Агуулга хоосон"
    assert lesson.initial_code.strip(), "Анхны код хоосон"
    assert 0 < lesson.duration <= 86_400, f"Хугацаа боломжгүй: {lesson.duration}"
    # Гарчгийг агуулгын эхний мөрөнд давтахгүй — UI өөрөө харуулна.
    assert not lesson.content.lstrip().startswith(f"## {lesson.title}")


@pytest.mark.parametrize(
    ("course", "module", "lesson"),
    [item for item in ALL_LESSONS if item[2].language == LessonLanguage.PYTHON],
    ids=[f"{lsn.slug}" for c, _, lsn in ALL_LESSONS if lsn.language == LessonLanguage.PYTHON],
)
def test_python_starter_code_parses(course: CourseSpec, module: object, lesson: object) -> None:
    """Анхны код нь синтаксийн хувьд зөв Python байх ёстой.

    MVP-д хөтөч дотор ажиллуулж чадахгүй ч суралцагч өөрийн компьютер дээр
    хуулж ажиллуулна — тиймээс эвдэрсэн код нийтлэгдэж болохгүй.
    """
    try:
        ast.parse(lesson.initial_code)
    except SyntaxError as aldaa:
        pytest.fail(f"{lesson.slug}: Python синтакс алдаатай — {aldaa}")


def test_python_course_follows_the_curriculum_document() -> None:
    """Python сургалт хөтөлбөрийнхөө бүтцийг дагасан эсэх.

    Ахисан шат (Async, FastAPI, Django, …) одоогоор ороогүй.
    """
    garchguud = [module.title for module in PYTHON_COURSE.modules]

    assert garchguud[0].startswith("Модул 0"), "Програмчлалын үндэс эхэнд байх ёстой"
    assert len(PYTHON_COURSE.modules) == 29, f"29 модул байх ёстой, одоо {len(garchguud)}"

    # Модулын дугаар 0-ээс 28 хүртэл дараалсан байх.
    dugaaruud = [int(re.match(r"Модул (\d+)", garchig).group(1)) for garchig in garchguud]
    assert dugaaruud == list(range(29)), f"Дараалал таарахгүй: {dugaaruud}"


def test_python_lessons_are_marked_as_python() -> None:
    for module in PYTHON_COURSE.modules:
        for lesson in module.lessons:
            assert lesson.language == LessonLanguage.PYTHON, (
                f"{lesson.slug} нь python гэж тэмдэглэгдээгүй"
            )


def test_javascript_course_still_runnable() -> None:
    """Туг сургалт нь хөтөч дотор ажилладаг хэвээр байх ёстой."""
    for module in JS_COURSE.modules:
        for lesson in module.lessons:
            assert lesson.language == LessonLanguage.JAVASCRIPT


def test_javascript_course_follows_the_curriculum_document() -> None:
    """JavaScript сургалт хөтөлбөрийнхөө бүтцийг дагасан эсэх.

    Модул 0-ээс 25 хүртэл: үндэс, анхан шат, хөтчийн JavaScript, дунд шат,
    төгсгөлийн төслүүд.
    """
    garchguud = [module.title for module in JS_COURSE.modules]

    assert garchguud[0].startswith("Модул 0"), "JavaScript-ийн үндэс эхэнд байх ёстой"
    assert len(JS_COURSE.modules) == 26, f"26 модул байх ёстой, одоо {len(garchguud)}"

    dugaaruud = [int(re.match(r"Модул (\d+)", garchig).group(1)) for garchig in garchguud]
    assert dugaaruud == list(range(26)), f"Дараалал таарахгүй: {dugaaruud}"


def test_every_javascript_module_has_lessons() -> None:
    for module in JS_COURSE.modules:
        assert module.lessons, f"{module.title} хичээлгүй"


def test_html_css_course_follows_the_curriculum_document() -> None:
    """HTML & CSS сургалт хөтөлбөрийнхөө бүтцийг дагасан эсэх.

    Модул 0-ээс 19 хүртэл: вэбийн үндэс, HTML, CSS, хариуцлагатай дизайн,
    төгсгөлийн төслүүд.
    """
    garchguud = [module.title for module in HTML_COURSE.modules]

    assert garchguud[0].startswith("Модул 0"), "Вэбийн үндэс эхэнд байх ёстой"
    assert len(HTML_COURSE.modules) == 20, f"20 модул байх ёстой, одоо {len(garchguud)}"

    dugaaruud = [int(re.match(r"Модул (\d+)", garchig).group(1)) for garchig in garchguud]
    assert dugaaruud == list(range(20)), f"Дараалал таарахгүй: {dugaaruud}"


def test_html_css_lessons_are_marked_html_or_css() -> None:
    for module in HTML_COURSE.modules:
        for lesson in module.lessons:
            assert lesson.language in {LessonLanguage.HTML, LessonLanguage.CSS}, (
                f"{lesson.slug} нь html эсвэл css гэж тэмдэглэгдээгүй"
            )


def test_every_html_css_module_has_lessons() -> None:
    for module in HTML_COURSE.modules:
        assert module.lessons, f"{module.title} хичээлгүй"


# Агуулгагүй шошго — хаах шошго шаарддаггүй.
VOID_TAGS = frozenset(
    [
        "area",
        "base",
        "br",
        "col",
        "embed",
        "hr",
        "img",
        "input",
        "link",
        "meta",
        "param",
        "source",
        "track",
        "wbr",
    ]
)

HTML_CSS_LESSONS = [lesson for module in HTML_COURSE.modules for lesson in module.lessons]


class _TagBalance(HTMLParser):
    """Хаагдаагүй болон буруу үүрлэсэн шошгыг олно."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[str] = []
        self.errors: list[str] = []

    def handle_starttag(self, tag: str, attrs: object) -> None:
        if tag not in VOID_TAGS:
            self.stack.append(tag)

    def handle_endtag(self, tag: str) -> None:
        if tag in VOID_TAGS:
            return
        if not self.stack:
            self.errors.append(f"нээгээгүй </{tag}>")
        elif self.stack[-1] != tag:
            self.errors.append(f"</{tag}> ирлээ, </{self.stack[-1]}> хүлээж байсан")
            if tag in self.stack:
                while self.stack and self.stack.pop() != tag:
                    pass
        else:
            self.stack.pop()


def html_css_files(lesson: LessonSpec) -> list[tuple[str, str]]:
    """`// @file`-аар хуваасан файлууд (`app/content/html_css/common.py`)."""
    default = "index.html" if lesson.language == LessonLanguage.HTML else "style.css"
    return parse_files(lesson.initial_code, default)


@pytest.mark.parametrize("lesson", HTML_CSS_LESSONS, ids=lambda lesson: lesson.slug)
def test_html_css_starter_code_is_well_formed(lesson: LessonSpec) -> None:
    """Анхны код нь суралцагч хуулж шууд ашиглах жишээ — эвдэрсэн байж болохгүй."""
    for name, code in html_css_files(lesson):
        if name.endswith(".html"):
            parser = _TagBalance()
            parser.feed(code)
            parser.close()
            assert not parser.errors, f"{lesson.slug}/{name}: {parser.errors[:3]}"
            assert not parser.stack, f"{lesson.slug}/{name}: хаагдаагүй шошго {parser.stack}"
        else:
            assert code.count("{") == code.count("}"), (
                f"{lesson.slug}/{name}: CSS хаалт тэнцэхгүй "
                f"({code.count('{')} нээсэн, {code.count('}')} хаасан)"
            )


@pytest.mark.parametrize("lesson", HTML_CSS_LESSONS, ids=lambda lesson: lesson.slug)
def test_html_css_lessons_have_a_page_for_the_browser(lesson: LessonSpec) -> None:
    """«Хөтөч» нь `.html` файлыг харуулна — CSS хичээлд ч хуудас байх ёстой."""
    parsed = html_css_files(lesson)
    names = [name for name, _ in parsed]
    assert len(names) == len(set(names)), f"{lesson.slug}: давхардсан файл {names}"
    assert all(re.fullmatch(r"[a-z0-9-]+\.(html|css)", name) for name in names), names
    assert any(name.endswith(".html") for name in names), f"{lesson.slug}: .html файл алга"


class _Selectors(HTMLParser):
    """HTML дахь бүх `class`, `id`, мөн холбосон CSS файлууд."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.classes: set[str] = set()
        self.ids: set[str] = set()
        self.stylesheets: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key: value or "" for key, value in attrs}
        self.classes.update(values.get("class", "").split())
        if values.get("id"):
            self.ids.add(values["id"])
        if tag == "link" and "stylesheet" in values.get("rel", "").split():
            self.stylesheets.add(values.get("href", ""))


def css_selectors(css: str) -> tuple[set[str], set[str]]:
    """Сонгогч доторх `.класс`, `#id` — утга (`#1f2933`), тайлбар, `[attr]` биш."""
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    classes: set[str] = set()
    ids: set[str] = set()
    for selector in re.findall(r"(?:^|(?<=[{};]))([^{};]+)\{", css):
        if selector.strip().startswith("@"):
            continue
        selector = re.sub(r"\[[^\]]*\]", "", selector)
        classes.update(re.findall(r"\.(-?[_a-zA-Z][\w-]*)", selector))
        ids.update(re.findall(r"#(-?[_a-zA-Z][\w-]*)", selector))
    return classes, ids


CSS_LESSONS = [lesson for lesson in HTML_CSS_LESSONS if lesson.language == LessonLanguage.CSS]


@pytest.mark.parametrize("lesson", CSS_LESSONS, ids=lambda lesson: lesson.slug)
def test_css_lessons_style_a_real_page(lesson: LessonSpec) -> None:
    """CSS хичээл: `index.html` нь `style.css`-ийг холбож, загварын бүх
    класс, id-г агуулна — сурагч бичсэн дүрэм бүрийнхээ үр дүнг «Хөтөч»-өөс
    харна."""
    parsed = dict(html_css_files(lesson))
    assert set(parsed) == {"index.html", "style.css"}, f"{lesson.slug}: {sorted(parsed)}"

    page = _Selectors()
    page.feed(parsed["index.html"])
    page.close()
    assert "style.css" in page.stylesheets, f"{lesson.slug}: index.html нь style.css-ийг холбоогүй"

    classes, ids = css_selectors(parsed["style.css"])
    assert not classes - page.classes, (
        f"{lesson.slug}: index.html-д алга класс {sorted(classes - page.classes)}"
    )
    assert not ids - page.ids, f"{lesson.slug}: index.html-д алга id {sorted(ids - page.ids)}"


def test_css_selector_scan_skips_values_and_attributes() -> None:
    classes, ids = css_selectors(
        '/* .tailbar */ a[href$=".pdf"] { color: #1f2933; }\n'
        ".kart:hover > #gol, .tovch { width: .5rem; }\n"
        "@media (min-width: 40em) { .sav { gap: 1px; } }"
    )
    assert classes == {"kart", "tovch", "sav"}
    assert ids == {"gol"}


# Sandbox нь Web Worker дотор ажилладаг тул эдгээр нь БАЙХГҮЙ. Хичээлийн
# анхны код нь тэдгээрийг ашиглах бол өөрөө дотроо зарлах ёстой — эс бөгөөс
# суралцагч «Код ажиллуулах» дарах бүрд алдаа харна.
#
# Дурдсан төдийг биш ХЭРЭГЛЭСЭН тохиолдлыг л хайна: `fetch(` дуудалт,
# `document.` хандалт. Хичээлийн текст дотор нэрийг нь дурдах нь зүгээр.
SANDBOX_BLOCKED = {
    "document": ".",
    "window": ".",
    "localStorage": ".",
    "sessionStorage": ".",
    "fetch": "(",
}


@pytest.mark.parametrize(
    "lesson",
    [lesson for module in JS_COURSE.modules for lesson in module.lessons],
    ids=lambda lesson: lesson.slug,
)
def test_javascript_starter_code_avoids_sandbox_globals(lesson: object) -> None:
    code = lesson.initial_code

    for ner, hereglee in SANDBOX_BLOCKED.items():
        if f"{ner}{hereglee}" not in code:
            continue

        zarlasan = re.search(rf"\b(?:const|let|var|function|async\s+function)\s+{ner}\b", code)
        assert zarlasan, (
            f"{lesson.slug}: `{ner}` нь sandbox дотор байхгүй. "
            "Ашиглах бол анхны код дотроо загварыг нь зарлана уу."
        )


def test_c_cpp_course_follows_the_curriculum_document() -> None:
    """C/C++ сургалт хөтөлбөрийнхөө бүтцийг дагасан эсэх.

    Хөтөлбөр нь модул 0-гүй тул энэ сургалт 1-ээс эхэлж 21-ээр
    дуусна: 1-10 нь C, 11-19 нь C++, 20-21 нь төслүүд.
    """
    garchguud = [module.title for module in C_CPP_COURSE.modules]

    assert garchguud[0].startswith("Модул 1"), "C-ийн үндэс эхэнд байх ёстой"
    assert len(C_CPP_COURSE.modules) == 21, f"21 модул байх ёстой, одоо {len(garchguud)}"

    dugaaruud = [int(re.match(r"Модул (\d+)", garchig).group(1)) for garchig in garchguud]
    assert dugaaruud == list(range(1, 22)), f"Дараалал таарахгүй: {dugaaruud}"


def test_git_course_follows_the_curriculum_document() -> None:
    """Git сургалт хөтөлбөрийнхөө бүтцийг дагасан эсэх — Модул 0-ээс 17."""
    garchguud = [module.title for module in GIT_COURSE.modules]

    assert garchguud[0].startswith("Модул 0"), "Хувилбарын хяналтын үндэс эхэнд байх ёстой"
    assert len(GIT_COURSE.modules) == 18, f"18 модул байх ёстой, одоо {len(garchguud)}"

    dugaaruud = [int(re.match(r"Модул (\d+)", garchig).group(1)) for garchig in garchguud]
    assert dugaaruud == list(range(18)), f"Дараалал таарахгүй: {dugaaruud}"


def test_c_cpp_lessons_are_marked_c_or_cpp() -> None:
    for module in C_CPP_COURSE.modules:
        for lesson in module.lessons:
            assert lesson.language in {LessonLanguage.C, LessonLanguage.CPP}, (
                f"{lesson.slug} нь c эсвэл cpp гэж тэмдэглэгдээгүй"
            )


def test_git_lessons_are_marked_shell() -> None:
    for module in GIT_COURSE.modules:
        for lesson in module.lessons:
            assert lesson.language == LessonLanguage.SHELL, (
                f"{lesson.slug} нь shell гэж тэмдэглэгдээгүй"
            )


def test_every_lesson_language_is_a_monaco_id() -> None:
    """`code-editor.tsx` нь утгыг шууд Monaco руу дамжуулдаг.

    Танихгүй ID өгвөл засварлагч өнгө ялгахаа болино. Frontend-ийн
    `LessonLanguage` төрөлтэй гар аргаар синк байлгана. Цорын ганц үл
    хамаарах нь `jsx` — засварлагч үүнийг `javascript` болгодог.
    """
    monaco_ids = {
        "jsx",
        "javascript",
        "html",
        "css",
        "python",
        "c",
        "cpp",
        "shell",
        "mysql",
        "sql",
        "plaintext",
    }
    assert {member.value for member in LessonLanguage} == monaco_ids


C_CPP_LESSONS = [lesson for module in C_CPP_COURSE.modules for lesson in module.lessons]


@pytest.mark.parametrize("lesson", C_CPP_LESSONS, ids=lambda lesson: lesson.slug)
def test_c_cpp_starter_code_is_balanced(lesson: object) -> None:
    """Анхны код нь хуулж хөрвүүлэх жишээ тул хаалт нь тэнцүү байх ёстой.

    Бүрэн синтаксийн шалгалт биш — CI дээр хөрвүүлэгч байхгүй. Гэхдээ
    хаалт тэнцэхгүй бол гарцаагүй эвдэрсэн гэсэн үг.
    """
    code = lesson.initial_code

    for neeh, haah in (("{", "}"), ("(", ")"), ("[", "]")):
        assert code.count(neeh) == code.count(haah), (
            f"{lesson.slug}: `{neeh}{haah}` тэнцэхгүй "
            f"({code.count(neeh)} нээсэн, {code.count(haah)} хаасан)"
        )

    assert "int main" in code, f"{lesson.slug}: `main` функц байхгүй"


def _assert_well_formed_exercise(lesson: LessonSpec) -> None:
    """HackerRank маягийн дасгалын бүтэц — хэлнээс үл хамаарах шаардлагууд.

    Тестүүд ЗӨВ эсэхийг (жишиг шийдэл давдаг, эхлэл код давдаггүй) энд
    шалгах боломжгүй — хөрвүүлэгч, Pyodide хэрэгтэй. Үүнийг
    `python -m app.content.exercises | node ../web/scripts/verify-exercises.mjs`
    шалгана.
    """
    exercise = lesson.exercise
    assert exercise is not None, f"{lesson.slug}: дасгалгүй"
    assert exercise.statement.strip(), f"{lesson.slug}: даалгаврын текст хоосон"
    assert exercise.tips.strip(), f"{lesson.slug}: «Тусламж»-ийн зөвлөгөөгүй"
    assert exercise.solution.strip() != lesson.initial_code.strip(), (
        f"{lesson.slug}: эхлэл код нь шийдэлтэйгээ ижил"
    )

    tests = exercise.tests
    assert any(test.sample for test in tests), f"{lesson.slug}: жишээ тест алга"
    assert all(test.expected_output.strip() for test in tests), (
        f"{lesson.slug}: хоосон гаралттай тест байна"
    )
    stdins = [test.stdin for test in tests]
    assert len(set(stdins)) == len(stdins), f"{lesson.slug}: ижил оролттой тест давхардсан"

    # Хүлээгдэж буй гаралтыг гараар хэвлээд давахаас сэргийлнэ (эзэмшигч,
    # 2026-09-30): даалгавар бүр оролт уншиж, нууц тестүүд өөр оролттой, өөр
    # гаралттай байна. Оролтгүй ганц тест нь «хариуг хэвлэ» л гэсэн үг. Хоосон
    # мөр («нууц үг хоосон», «тоо алга») нь захын тохиолдлын зөв тест.
    assert any(test.stdin.strip() for test in tests), f"{lesson.slug}: оролтгүй даалгавар"
    assert len(tests) >= 4, f"{lesson.slug}: 4-өөс цөөн тест"
    assert any(not test.sample for test in tests), f"{lesson.slug}: нууц тест алга"
    outputs = {test.expected_output.strip() for test in tests}
    assert len(outputs) >= 2, (
        f"{lesson.slug}: бүх тест ижил гаралттай — оролтыг үл тоосон код давна"
    )

    # Жишээ оролт/гаралтыг UI нь тестүүдээс өөрөө харуулна.
    assert "Жишээ оролт" not in exercise.statement, (
        f"{lesson.slug}: жишээг даалгаварт давтаж бичсэн"
    )


@pytest.mark.parametrize("lesson", C_CPP_LESSONS, ids=lambda lesson: lesson.slug)
def test_c_cpp_lesson_has_a_well_formed_exercise(lesson: LessonSpec) -> None:
    """C/C++ хичээл бүр дасгалтай — тестийг давж дуусна."""
    _assert_well_formed_exercise(lesson)
    assert lesson.exercise is not None
    assert "int main" in lesson.exercise.solution, f"{lesson.slug}: жишиг шийдэлгүй"


PYTHON_LESSONS = [lesson for module in PYTHON_COURSE.modules for lesson in module.lessons]


@pytest.mark.parametrize("lesson", PYTHON_LESSONS, ids=lambda lesson: lesson.slug)
def test_python_lesson_has_a_well_formed_exercise(lesson: LessonSpec) -> None:
    """Python хичээл бүр дасгалтай — C/C++-тэй ижил шаардлага."""
    _assert_well_formed_exercise(lesson)
    assert lesson.exercise is not None
    ast.parse(lesson.exercise.solution)
    # Pyodide-д байхгүй сангууд — сурагчийн хөтөч дотор импортлогдохгүй.
    for missing in ("requests", "sqlalchemy", "venv", "pip"):
        assert f"import {missing}" not in lesson.exercise.solution, (
            f"{lesson.slug}: `{missing}` Pyodide-д байхгүй"
        )


JAVASCRIPT_LESSONS = [lesson for module in JS_COURSE.modules for lesson in module.lessons]


@pytest.mark.parametrize("lesson", JAVASCRIPT_LESSONS, ids=lambda lesson: lesson.slug)
def test_javascript_lesson_has_a_well_formed_exercise(lesson: LessonSpec) -> None:
    """JavaScript хичээл бүр дасгалтай — оролтоо `prompt()`-оор уншина.

    Тестийг хөтөчийн worker дээр `verify-exercises.mjs` ажиллуулна. Worker нь
    DOM, сүлжээгүй тул шийдэл тэдгээрийг өөрөө загварчилна.
    """
    _assert_well_formed_exercise(lesson)
    assert lesson.exercise is not None
    assert "prompt(" in lesson.exercise.solution, f"{lesson.slug}: оролтоо `prompt()`-оор уншаагүй"
    for ner, hereglee in SANDBOX_BLOCKED.items():
        if f"{ner}{hereglee}" not in lesson.exercise.solution:
            continue
        zarlasan = re.search(
            rf"\b(?:const|let|var|function|async\s+function)\s+{ner}\b", lesson.exercise.solution
        )
        assert zarlasan, f"{lesson.slug}: жишиг шийдэлд `{ner}` sandbox дотор байхгүй"
    # Worker-т ES module ачаалагдахгүй — import/export нь синтакс алдаа.
    assert not re.search(r"^\s*(?:import|export)\b", lesson.exercise.solution, re.M), (
        f"{lesson.slug}: import/export sandbox дотор ажиллахгүй"
    )


FLOWGORITHM_LESSONS = [lesson for module in FLOWGORITHM_COURSE.modules for lesson in module.lessons]


@pytest.mark.parametrize("lesson", FLOWGORITHM_LESSONS, ids=lambda lesson: lesson.slug)
def test_flowgorithm_lesson_has_a_well_formed_task(lesson: LessonSpec) -> None:
    """Flowgorithm хичээл бүр автоматаар шалгагддаг даалгавартай.

    Жишиг шийдэл бүх тестийг давж, эхлэл схем давдаггүйг хөтөчийн runtime-аар
    `apps/web/tests/flowgorithm.test.mjs` шалгана. Хуучин цаасан «Дасгал»,
    «Өөрийгөө шалгая» нь даалгаврыг давхардуулж, хариуг нь дэлгэхгүй.
    """
    _assert_well_formed_exercise(lesson)
    assert lesson.exercise is not None
    solution = json.loads(lesson.exercise.solution)
    assert solution["format"] == "medleghub-flowgorithm", lesson.slug
    assert solution["nodes"], f"{lesson.slug}: жишиг шийдэл хоосон"
    for heading in ("### Дасгал", "### Өөрийгөө шалгая"):
        assert heading not in lesson.content, f"{lesson.slug}: «{heading}» даалгавартай давхардана"


GIT_LESSONS = [lesson for module in GIT_COURSE.modules for lesson in module.lessons]


@pytest.mark.parametrize("lesson", GIT_LESSONS, ids=lambda lesson: lesson.slug)
def test_git_starter_code_heredocs_are_closed(lesson: object) -> None:
    """Хаагдаагүй heredoc нь хуулж ажиллуулахад терминалыг гацаана."""
    muruud = lesson.initial_code.split("\n")
    neesen = [mur for mur in muruud if re.search(r"<<\s*'?EOF'?\s*$", mur)]
    haasan = [mur for mur in muruud if mur.strip() == "EOF"]

    assert len(neesen) == len(haasan), (
        f"{lesson.slug}: heredoc тэнцэхгүй ({len(neesen)} нээсэн, {len(haasan)} хаасан)"
    )


def test_sql_course_follows_the_curriculum_document() -> None:
    """SQL сургалт MySQL хөтөлбөрөө дагасан эсэх — Модул 0-ээс 20,
    дээр нь Модул 21 — төгсгөлийн хэрэг."""
    garchguud = [module.title for module in SQL_COURSE.modules]

    assert garchguud[0].startswith("Модул 0"), "Өгөгдлийн сангийн үндэс эхэнд байх ёстой"
    assert len(SQL_COURSE.modules) == 22, f"22 модул байх ёстой, одоо {len(garchguud)}"

    dugaaruud = [int(re.match(r"Модул (\d+)", garchig).group(1)) for garchig in garchguud]
    assert dugaaruud == list(range(22)), f"Дараалал таарахгүй: {dugaaruud}"

    for module in SQL_COURSE.modules:
        assert module.lessons, f"{module.title} хичээлгүй"


def test_every_sql_module_ends_with_a_detective_case() -> None:
    """Модул 1–20 бүр нэг хэргээр төгсөж, Модул 21 бүхэлдээ хэрэг (`sql/cases.py`)."""
    for number, module in enumerate(SQL_COURSE.modules):
        cases = [lesson for lesson in module.lessons if lesson.exercise and lesson.exercise.answers]
        if number == 0:
            assert not cases, "Модул 0-д асуулга заагаагүй — хэрэг байх ёсгүй"
        elif number == 21:
            assert cases == module.lessons, "Модул 21 зөвхөн төгсгөлийн хэрэгтэй"
        else:
            assert cases == [module.lessons[-1]], f"{module.title}: төгсгөлд яг нэг хэрэг"


_SQL_CASES = [
    lesson
    for module in SQL_COURSE.modules
    for lesson in module.lessons
    if lesson.exercise and lesson.exercise.answers
]


@pytest.mark.parametrize("lesson", _SQL_CASES, ids=lambda lesson: lesson.slug)
def test_sql_cases_hide_their_answers(lesson: LessonSpec) -> None:
    """Хэрэг тестгүй, шийдэлтэй; хариулт нь хөтөч рүү очих текстэд бичигдээгүй.

    Хариулт хөтөчид ирдэггүй (`POST /lessons/{id}/answer` шалгана) — харин
    хичээлийн текст, эхлэл код, зөвлөгөө ирдэг. Жинхэнэ MySQL дээрх шалгалт:
    `python -m app.content.verify_sql_cases`.
    """
    from app.services.case_service import normalize_answer

    exercise = lesson.exercise
    assert exercise is not None
    assert exercise.kind == "answer"
    assert not exercise.tests, "Хэрэг тестгүй — хариултаар шалгана"
    assert exercise.solution.strip() and exercise.tips.strip() and exercise.statement.strip()
    accepted = [normalize_answer(answer) for answer in exercise.answers]
    assert all(accepted), f"Хоосон хариулт: {exercise.answers}"

    shown = normalize_answer(
        " ".join([lesson.content, exercise.statement, lesson.initial_code, exercise.tips])
    )
    for answer in accepted:
        if len(answer) >= 3 and not answer.replace(" ", "").isdigit():
            assert answer not in shown, f"«{answer}» хөтөч рүү очих текстэд бичигдсэн"


def test_sql_lessons_are_all_mysql() -> None:
    """Сургалт зөвхөн MySQL — хичээл бүр сайт дээр ажиллана.

    `LessonLanguage.SQL` (T-SQL) нь ажиллуулагчгүй тул SQL Server-ийн
    хичээл дахин нэмэгдвэл энэ тест анхааруулна.
    """
    helnuud = {lesson.language for module in SQL_COURSE.modules for lesson in module.lessons}
    assert helnuud == {LessonLanguage.MYSQL}, helnuud


SQL_LESSONS = [lesson for module in SQL_COURSE.modules for lesson in module.lessons]

# Тайлбар болон тэмдэгт мөрийг зүүнээс баруун тийш нэг дор таниулна — эс
# бөгөөс `'--'` мөр эсвэл тайлбар доторх `'` нь бие биеэ эвдэнэ.
_SQL_NOISE = re.compile(r"--[^\n]*|/\*.*?\*/|N?'(?:[^']|'')*'", re.DOTALL)

# SQL Server (T-SQL)-д л байдаг бичиглэл. MySQL хичээлийн анхны кодод
# орвол суралцагч ажиллуулахад шууд синтакс алдаа гарна. (`ISNULL` нь
# MySQL-д нэг аргументтай өөр функц тул мөн хориглоно — андуурагдана.)
_NOT_MYSQL = {
    "TOP": r"\bTOP\b",
    "IDENTITY": r"\bIDENTITY\b",
    "NVARCHAR": r"\bNVARCHAR\b",
    "GETDATE": r"\bGETDATE\b",
    "ISNULL": r"\bISNULL\b",
    "IIF": r"\bIIF\s*\(",
    "DATEADD": r"\bDATEADD\s*\(",
    "SCOPE_IDENTITY": r"\bSCOPE_IDENTITY\b",
    "BEGIN TRY": r"\bBEGIN\s+TRY\b",
    "BEGIN TRANSACTION": r"\bBEGIN\s+TRAN(SACTION)?\b",
    "THROW": r"\bTHROW\b",
    "PRINT": r"\bPRINT\b",
    "EXEC": r"\bEXEC\b",
    "DECLARE @": r"\bDECLARE\s+@",
    "OFFSET … ROWS": r"\bOFFSET\s+\S+\s+ROWS\b",
    "APPLY": r"\b(CROSS|OUTER)\s+APPLY\b",
    "dbo.": r"\bdbo\.",
    "GO": r"^\s*GO\s*$",
}


@pytest.mark.parametrize("lesson", SQL_LESSONS, ids=lambda lesson: lesson.slug)
def test_sql_starter_code_is_balanced(lesson: object) -> None:
    """Хаагдаагүй хаалт, ишлэл, тайлбар нь скриптийг бүхэлд нь эвдэнэ."""
    code = _SQL_NOISE.sub(" ", lesson.initial_code)

    assert "'" not in code, f"{lesson.slug}: хаагдаагүй `'` ишлэл"
    assert "/*" not in code, f"{lesson.slug}: хаагдаагүй `/*` тайлбар"
    assert code.count("(") == code.count(")"), (
        f"{lesson.slug}: `()` тэнцэхгүй ({code.count('(')} нээсэн, {code.count(')')} хаасан)"
    )


@pytest.mark.parametrize("lesson", SQL_LESSONS, ids=lambda lesson: lesson.slug)
def test_sql_starter_code_has_no_tsql(lesson: object) -> None:
    """Анхны код MySQL 8.4-ийн sandbox дээр ажиллах ёстой — T-SQL үлдээгүй."""
    code = _SQL_NOISE.sub(" ", lesson.initial_code)

    oldson = [
        ner
        for ner, pattern in _NOT_MYSQL.items()
        if re.search(pattern, code, re.IGNORECASE | re.MULTILINE)
    ]
    assert not oldson, f"{lesson.slug}: T-SQL бичиглэл {oldson}"

    # `N'...'` угтвар нь `_SQL_NOISE`-д залгигддаг тул тусад нь шалгана.
    tailbargui = re.sub(r"--[^\n]*|/\*.*?\*/", " ", lesson.initial_code, flags=re.DOTALL)
    assert not re.search(r"(?<![\w'])N'", tailbargui), f"{lesson.slug}: T-SQL-ийн N'...' текст"


@pytest.mark.parametrize("lesson", SQL_LESSONS, ids=lambda lesson: lesson.slug)
def test_mysql_delimiter_is_restored(lesson: object) -> None:
    """`DELIMITER $$`-ийг буцаагаагүй бол дараагийн бүх тушаал ажиллахгүй."""
    tohirgoo = re.findall(r"^\s*DELIMITER\s+(\S+)", lesson.initial_code, re.MULTILINE)
    if tohirgoo:
        assert tohirgoo[-1] == ";", f"{lesson.slug}: төгсгөлд `DELIMITER ;` байхгүй"
