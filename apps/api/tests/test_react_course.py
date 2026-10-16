"""«React-ээр апп бүтээх» сургалтын бүтэц.

Дасгалын тест зөв эсэхийг (жишиг шийдэл давдаг, эхлэл код давдаггүй,
эхлэл код алдаагүй render хийгддэг) энд шалгах боломжгүй — хөтөч хэрэгтэй.
Үүнийг `cd apps/web && npm run verify:react` шалгана.
"""

import re

import pytest

from app.content.exercises import exercise_payload
from app.content.react import REACT_COURSE
from app.content.types import LessonSpec, ReactTestSpec
from app.models.enums import LessonLanguage

# Хөтөлбөрийн хүснэгт. Хичээл нэмэх, солиход энд өөрчилнө.
CURRICULUM: list[list[str]] = [
    [
        "tavtai-moril",
        "js-funkts-obekt",
        "js-massivyn-arguud",
        "js-module-async",
        "dom-yagaad-hetsuu",
    ],
    [
        "react-gej-yu-ve",
        "react-tosliin-butets",
        "react-element",
        "createroot-render",
        "jsx",
        "jsx-ilerhiilel",
        "jsx-attribute-style",
        "fragment",
        "anhny-component",
        "component-niiluuleh",
        "tusul-huviin-profile",
    ],
    [
        "props-damjuulah",
        "props-zadlah",
        "children",
        "nohtsolt-render",
        "jagsaalt-map",
        "key",
        "dahin-ashiglagdah-component",
        "tusul-baraany-katalog",
    ],
    [
        "uil-yavdal",
        "usestate",
        "state-snapshot",
        "funktsional-shinechlelt",
        "boolean-state",
        "object-state",
        "massiv-state",
        "ulamjlagdsan-utga",
        "tusul-sags",
    ],
    [
        "controlled-input",
        "olon-talbartai-form",
        "select-checkbox-radio",
        "form-ilgeeh",
        "form-batalgaajuulalt",
        "form-hurteemj",
        "tusul-burtgeliin-form",
    ],
    [
        "useeffect",
        "effect-hamaaral",
        "effect-tseverlegee",
        "effect-timer",
        "effect-fetch",
        "effect-heregtei-yu",
        "tusul-hailtyn-app",
    ],
    [
        "hook-durem",
        "useref-dom",
        "useref-utga",
        "usememo",
        "usecallback",
        "custom-hook",
        "uselocalstorage",
        "tusul-hook-san",
    ],
    [
        "state-deesh-urgeh",
        "neg-unen-survalj",
        "prop-drilling",
        "context",
        "context-provider",
        "usereducer",
        "reducer-context",
        "tusul-tohirgoo",
    ],
    [
        "client-routing",
        "link-navlink",
        "useparams",
        "usenavigate",
        "nested-routes",
        "not-found-search-params",
        "tusul-surgaltyn-platform",
    ],
    [
        "http-rest",
        "post-patch-delete",
        "achaalal-aldaa-hooson",
        "server-state",
        "usequery",
        "usemutation",
        "tusul-surgaltyn-samber",
    ],
    [
        "render-model",
        "reconciliation",
        "error-boundary",
        "lazy-suspense",
        "usetransition",
        "usedeferredvalue",
    ],
    [
        "react-19-shineleg",
        "form-action",
        "useformstatus",
        "useoptimistic",
        "use-hook",
        "server-components",
        "server-actions-compiler",
    ],
    ["render-hemjih", "memo", "memo-hamt", "code-splitting", "urt-jagsaalt", "tusul-hurdasgah"],
    [
        "yagaad-test",
        "anhny-test",
        "uildel-test",
        "form-test",
        "async-mock-test",
        "tusul-test-nemeh",
    ],
    [
        "capstone-butets",
        "capstone-katalog",
        "capstone-delgerengui",
        "capstone-hailt",
        "capstone-sags",
        "capstone-tootsoo",
        "capstone-nevtreh",
        "capstone-admin",
        "capstone-bie-daasan",
    ],
]

LESSONS = [lesson for module in REACT_COURSE.modules for lesson in module.lessons]

# `apps/web/src/lib/sandbox/react/files.ts`-ийн дүрэм.
MARKER = re.compile(r"^// @file (\S+)( locked)?\s*$")
QUIZ = re.compile(r"```quiz\n(.*?)```", re.DOTALL)
OPTION = re.compile(r"^\s*[-*] \[( |x|X)\] (.+)$")


def parse_files(source: str) -> list[tuple[str, bool, str]]:
    files: list[tuple[str, bool, str]] = []
    current: tuple[str, bool] | None = None
    lines: list[str] = []
    for line in source.split("\n"):
        match = MARKER.match(line)
        if match:
            if current:
                files.append((*current, "\n".join(lines)))
            current, lines = (match[1], bool(match[2])), []
        else:
            lines.append(line)
    if current:
        files.append((*current, "\n".join(lines)))
    return files or [("App.jsx", False, source)]


def test_course_follows_the_curriculum_document() -> None:
    titles = [module.title for module in REACT_COURSE.modules]
    numbers = [int(re.match(r"Модул (\d+) — ", title).group(1)) for title in titles]
    assert numbers == list(range(15)), numbers
    actual = [[lesson.slug for lesson in module.lessons] for module in REACT_COURSE.modules]
    assert actual == CURRICULUM


def test_free_part_is_modules_zero_and_one() -> None:
    first_two = sum(len(module.lessons) for module in REACT_COURSE.modules[:2])
    assert not REACT_COURSE.is_free
    assert REACT_COURSE.free_lessons == first_two


@pytest.mark.parametrize("lesson", LESSONS, ids=lambda lesson: lesson.slug)
def test_lessons_use_the_react_editor(lesson: LessonSpec) -> None:
    assert lesson.language == LessonLanguage.JSX


@pytest.mark.parametrize("lesson", LESSONS, ids=lambda lesson: lesson.slug)
def test_starter_files_are_well_formed(lesson: LessonSpec) -> None:
    files = parse_files(lesson.initial_code)
    names = [name for name, _, _ in files]
    assert len(names) == len(set(names)), f"давхардсан файл: {names}"
    assert any(not locked for _, locked, _ in files), "засварлагдах файл алга"
    assert sum(name.endswith(".html") for name in names) <= 1
    scripts = [name for name in names if re.search(r"\.(jsx?|mjs)$", name)]
    assert scripts, "JavaScript файл алга"
    # Синтаксийг хөтөч (`npm run verify:react`) шалгана — энд зөвхөн бүтэц.
    for name, _, code in files:
        assert code.strip(), f"{name} хоосон"


@pytest.mark.parametrize("lesson", LESSONS, ids=lambda lesson: lesson.slug)
def test_content_follows_the_lesson_structure(lesson: LessonSpec) -> None:
    """roadmap §17: зорилго → тайлбар → жишээ → шалгах асуулт → дүгнэлт."""
    content = lesson.content
    assert "### Энэ хичээлээр" in content
    assert "### Дүгнэлт" in content
    quizzes = QUIZ.findall(content)
    assert quizzes, "```quiz асуулт алга"
    for quiz in quizzes:
        options = [OPTION.match(line) for line in quiz.split("\n")]
        options = [option for option in options if option]
        assert len(options) >= 2, f"сонголт хэт цөөн: {quiz[:60]}"
        assert any(option[1].lower() == "x" for option in options), f"зөв хариулт алга: {quiz[:60]}"


@pytest.mark.parametrize(
    "lesson",
    [lesson for lesson in LESSONS if lesson.exercise],
    ids=lambda lesson: lesson.slug,
)
def test_exercises_are_well_formed(lesson: LessonSpec) -> None:
    exercise = lesson.exercise
    assert exercise is not None
    assert exercise.statement.startswith("**Түвшин:** ⭐"), "Түвшин заагаагүй (roadmap §20)"
    assert exercise.tips.strip(), "«Тусламж»-ийн зөвлөгөө алга"
    assert all(isinstance(test, ReactTestSpec) for test in exercise.tests)
    assert 1 <= len(exercise.tests) <= 6
    names = [test.name for test in exercise.tests]
    assert all(name.strip() for name in names)
    assert len(set(names)) == len(names), "ижил нэртэй тест"
    assert all(test.code.strip() for test in exercise.tests)

    starter = {name: code for name, _, code in parse_files(lesson.initial_code)}
    solution = parse_files(exercise.solution)
    assert solution, "жишиг шийдэл алга"
    changed = [name for name, _, code in solution if starter.get(name, "").strip() != code.strip()]
    assert changed, "шийдэл нь эхлэл кодтой ижил"


def test_most_lessons_have_an_exercise() -> None:
    """Суралцагч уншихаас илүү код бичих ёстой (roadmap §26)."""
    with_exercise = sum(1 for lesson in LESSONS if lesson.exercise)
    assert with_exercise / len(LESSONS) >= 0.8


def test_dom_tests_are_stored_with_their_names() -> None:
    lesson = next(lesson for lesson in LESSONS if lesson.exercise)
    payload = exercise_payload(lesson.exercise)
    assert payload is not None
    first = payload["tests"][0]
    assert set(first) == {"name", "code", "sample"}
    assert first["sample"] is True
