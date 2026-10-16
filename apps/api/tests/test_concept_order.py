"""Хичээл бүр зөвхөн өмнө нь (эсвэл өөрөө) заасан синтаксийг ашиглана.

Эхнээс нь сурч буй сурагч заагаагүй `if`, давталт, массивыг мэдэхгүй. Иймээс
дасгалын эхлэл код, жишиг шийдэл (тэгэхээр тестүүд ч) зөвхөн тухайн хичээл
хүртэл заасан зүйлд тулгуурлана. Жишээ нь C-ийн «Модул 3 — scanf» дасгалын
нууц тест буруу оролтод мессеж хүлээж байсан нь «Модул 5 — Нөхцөл»-ийн `if`-ийг
шаарддаг байв.

Ойлголт бүрийг түүнийг ЗААДАГ хичээлийн slug-аар тэмдэглэнэ. Түүнээс өмнөх
хичээлийн эхлэл код эсвэл шийдэлд гарвал тест унана. Хичээлийн жишээ кодыг энд
шалгахгүй — тайлбартай, «(Модул N-д үзнэ)» гэсэн урьдчилсан харагдац
зөвшөөрөгдөнө.

SQL-д дасгал нь мөрдөгчийн хэргүүд (`app/content/sql/cases.py`): модул бүрийн
төгсгөлийн хэрэг зөвхөн тэр модул хүртэл заасныг ашиглана. Энгийн хичээлийн
эхлэл код нь тайлбартай жишээ тул шалгахгүй.

Эзэмшигчийн шийдвэр: C-ийн эхний дасгалууд оролтоо бэлэн бичсэн `scanf("%d", …)`
мөрөөр уншина (Модул 3-т заана) — тиймээс `scanf`-ийг энд шалгахгүй.
JavaScript-д мөн адил: эхлэл кодод бэлэн бичсэн `prompt()`-той мөр (жишээ нь
`const n = Number(prompt());`) шалгагдахгүй — `prompt()`-ийг «too-ba-mur»-д заана.

Flowgorithm-ийн схем нь JSON: дүрсний төрөл, илэрхийллийн тэмдгийг шалгана.
Сурагчийн өөрөө нэмэх, засах дүрс (эхлэл схемд байхгүй) хатуу дүрэмтэй; эхлэл
схемд тухайн хичээлд тайлбарласан бэлэн дүрс (`FLOW_PREVIEWS`) байж болно.
C-ийн бэлэн `scanf`-тэй адил: Declare, Input-ийг Модул 2 заадаг ч даалгавар бүр
оролт уншдаг тул эхний хичээлүүдийн эхлэл схемд оролт авах Declare + Input бэлэн.

Хичээл нэмэх, дараалал өөрчлөхөд дүрэм зөрчигдвөл: синтаксийг заадаг хичээлийн
өмнө бүү хэрэглэ, эсвэл тухайн хичээлд тайлбарлаад энд заах цэгийг шилжүүл.
"""

import ast
import json
import re

import pytest

from app.content.c_cpp import C_CPP_COURSE
from app.content.flowgorithm import FLOWGORITHM_COURSE
from app.content.javascript import JS_COURSE
from app.content.python import PYTHON_COURSE
from app.content.react import REACT_COURSE
from app.content.sql import SQL_COURSE
from app.content.types import CourseSpec, LessonSpec


def lessons_in_order(course: CourseSpec) -> list[LessonSpec]:
    return [lesson for module in course.modules for lesson in module.lessons]


def exercise_code(lesson: LessonSpec) -> list[tuple[str, str]]:
    code = [("эхлэл код", lesson.initial_code)]
    if lesson.exercise:
        code.append(("жишиг шийдэл", lesson.exercise.solution))
    return code


# --- C/C++ -----------------------------------------------------------------------


def _strip_c(code: str) -> str:
    """Тайлбар, мөр, тэмдэгтийн утгыг хасна — `"if ("` гэх мэт текст тооцогдохгүй."""
    code = re.sub(r"/\*.*?\*/", " ", code, flags=re.S)
    code = re.sub(r"//[^\n]*", " ", code)
    code = re.sub(r'"(?:\\.|[^"\\])*"', '""', code)
    return re.sub(r"'(?:\\.|[^'\\])*'", "''", code)


def _without_preprocessor(code: str) -> str:
    return "\n".join(line for line in code.split("\n") if not line.lstrip().startswith("#"))


_C_FUNCTION = re.compile(
    r"^[ \t]*(?:static\s+)?(?:unsigned\s+|const\s+)?(?:int|void|double|float|char|long|bool)"
    r"\s*\*?\s*(\w+)\s*\([^;{]*\)\s*\{",
    re.M,
)

# (ойлголт, илрүүлэх функц, заадаг хичээл). Зөвхөн C-ийн хэсэг (Модул 1–10):
# C++-ийн хэсэг эдгээрийг бүгдийг нь мэддэг сурагчид зориулагдсан.
C_RULES: list[tuple[str, object, str]] = [
    # Эзэмшигчийн шийдвэр: Модул 2 бутархай хариуг эхнээс нь `double`
    # хувьсагчаар гаргана, хувиргалтыг «printf ба формат»-д заана.
    (
        "төрөл хувиргалт (double)",
        lambda code: re.search(r"\(\s*(?:double|float|int|char|long)\s*\)\s*[\w(]", code),
        "printf-ba-format",
    ),
    ("sizeof", lambda code: re.search(r"\bsizeof\b", code), "c-massiv"),
    (
        "харьцуулах/логик оператор",
        lambda code: re.search(
            r"==|!=|<=|>=|&&|\|\||(?<![<\w])<(?![<=])|(?<![->])>(?![>=])",
            _without_preprocessor(code),
        ),
        "c-hartsuulah-ba-logik",
    ),
    (
        "%, ++, +=",
        lambda code: re.search(r"\+\+|--|[+\-*/%]=|(?<![\"%])%(?![\d.]*[dfsciulp])", code),
        "c-arifmetik-ba-onooh",
    ),
    ("if/else", lambda code: re.search(r"\bif\s*\(|\belse\b", code), "c-if-else"),
    ("?: (тернар)", lambda code: "?" in code, "c-if-else"),
    ("switch", lambda code: re.search(r"\bswitch\s*\(", code), "c-switch"),
    ("for", lambda code: re.search(r"\bfor\s*\(", code), "c-for-davtalt"),
    ("while/do", lambda code: re.search(r"\bwhile\s*\(|\bdo\s*\{", code), "c-while-davtalt"),
    ("continue", lambda code: re.search(r"\bcontinue\s*;", code), "c-break-continue"),
    (
        "main-аас бусад функц",
        lambda code: any(match.group(1) != "main" for match in _C_FUNCTION.finditer(code)),
        "c-funkts",
    ),
    ("массив []", lambda code: re.search(r"\w\s*\[[^\]]*\]", code), "c-massiv"),
    ("мөр (%s)", lambda code: re.search(r"%\d*s", code), "c-mur"),
    (
        "заагч",
        lambda code: re.search(
            r"\b(?:int|char|double|float|void|long|struct\s+\w+)\s*\*+\s*\w|->|\bmalloc\s*\(", code
        ),
        "zaagch-gej-yu-ve",
    ),
    ("struct", lambda code: re.search(r"\bstruct\b|\btypedef\b", code), "c-struct"),
]

C_LESSONS = lessons_in_order(C_CPP_COURSE)
C_PART = C_LESSONS[: [lesson.slug for lesson in C_LESSONS].index("c-ba-cpp")]


def _violations(
    lessons: list[LessonSpec],
    lesson: LessonSpec,
    rules: list[tuple[str, object, str]],
    prepare=lambda code: code,
) -> list[str]:
    order = [item.slug for item in lessons]
    here = order.index(lesson.slug)
    found = []
    for concept, detect, taught in rules:
        if order.index(taught) <= here:
            continue
        for where, raw in exercise_code(lesson):
            if detect(prepare(raw)):
                found.append(f"{concept} ({taught}-д заана) — {where}")
    return found


def _cpp(pattern: str):
    return lambda code: re.search(pattern, _without_preprocessor(code))


# C++-ийн ойлголт — бүх сургалтын дарааллаар (C-ийн хэсэгт ч гарах ёсгүй).
# `std::string`-ийн товч танилцуулга «cin-orolt»-д, `&` (range-for-ийн alias)
# «cpp-davtalt»-д тайлбарлагдсан — дэлгэрэнгүй нь Модул 16, 17-д.
CPP_RULES: list[tuple[str, object, str]] = [
    ("cout/cin", _cpp(r"\b(?:std::)?(?:cout|cin)\b"), "cpp-butets-ba-namespace"),
    ("std::string", _cpp(r"\bstd::string\b|\bstring\s+\w"), "cin-orolt"),
    ("auto", _cpp(r"\bauto\b"), "auto-ba-horvuulelt"),
    ("static_cast", _cpp(r"\bstatic_cast\b"), "auto-ba-horvuulelt"),
    ("range-for", _cpp(r"\bfor\s*\([^;)]*[^:]:[^:][^;)]*\)"), "cpp-davtalt"),
    (
        "лавлагаа (&)",
        _cpp(r"\b(?:int|double|char|bool|auto|string|std::string|[A-Z]\w*)\s*&\s*\w"),
        "cpp-davtalt",
    ),
    ("class", _cpp(r"\bclass\b"), "angi-ba-obyekt"),
    ("std::array", _cpp(r"\barray\s*<"), "std-array"),
    ("std::vector", _cpp(r"\bvector\s*<"), "std-vector"),
    ("try/throw", _cpp(r"\btry\s*\{|\bthrow\b"), "cpp-tootsooluur"),
    ("lambda", _cpp(r"\[[^\]\[]*\]\s*\([^)]*\)\s*\{"), "cpp-oyutan-udirdlaga"),
]


def test_c_rules_point_at_existing_lessons() -> None:
    slugs = {lesson.slug for lesson in C_LESSONS}
    assert {taught for _, _, taught in C_RULES + CPP_RULES} <= slugs


@pytest.mark.parametrize("lesson", C_PART, ids=lambda lesson: lesson.slug)
def test_c_exercises_use_only_taught_syntax(lesson: LessonSpec) -> None:
    found = _violations(C_PART, lesson, C_RULES, _strip_c)
    assert not found, f"{lesson.slug}: {found}"


@pytest.mark.parametrize("lesson", C_LESSONS, ids=lambda lesson: lesson.slug)
def test_cpp_exercises_use_only_taught_syntax(lesson: LessonSpec) -> None:
    found = _violations(C_LESSONS, lesson, CPP_RULES, _strip_c)
    # `std::move` сургалтад хэзээ ч заагдаагүй.
    found += [
        f"std::move (заагдаагүй) — {where}"
        for where, raw in exercise_code(lesson)
        if "std::move" in _strip_c(raw)
    ]
    assert not found, f"{lesson.slug}: {found}"


# --- React ---------------------------------------------------------------------------
#
# Сурагч JavaScript-ийг мэддэг — энд зөвхөн React-ийн API-г шалгана. Түгжигдсэн
# (`// @file X locked`) файлыг тооцохгүй: тэдгээр нь «ойлгох шаардлагагүй» гэсэн
# шошготой бэлэн жишээ байж болно (жишээ нь «key» хичээлийн `App.jsx`).

_REACT_MARKER = re.compile(r"^// @file (\S+)( locked)?\s*$", re.M)


def _react_student_code(source: str) -> str:
    """Засварлагдах файлууд л — `// @file` тэмдэггүй бол бүхэлдээ."""
    parts = _REACT_MARKER.split(source)
    if len(parts) == 1:
        return source
    # split: [өмнөх, нэр, locked, код, нэр, locked, код, …]
    return "\n".join(
        parts[index + 2]
        for index in range(1, len(parts) - 2, 3)
        if not parts[index + 1] and not parts[index].endswith(".html")
    )


def _react(pattern: str):
    return lambda code: re.search(pattern, _strip_c(code))


REACT_RULES: list[tuple[str, object, str]] = [
    ("useState", _react(r"\buseState\b"), "usestate"),
    ("useEffect", _react(r"\buseEffect\b"), "useeffect"),
    ("useRef", _react(r"\buseRef\b"), "useref-dom"),
    ("useMemo", _react(r"\buseMemo\b"), "usememo"),
    ("useCallback", _react(r"\buseCallback\b"), "usecallback"),
    # `memo`-г «usecallback» хичээл товч тайлбарладаг, дэлгэрэнгүй нь Модул 12-т.
    ("memo", _react(r"\bmemo\s*\("), "usecallback"),
    ("context", _react(r"\b(?:createContext|useContext)\b"), "context"),
    ("useReducer", _react(r"\buseReducer\b"), "usereducer"),
    ("react-router", _react(r"""from ["']react-router"""), "client-routing"),
    ("TanStack Query", _react(r"""from ["']@tanstack/react-query"""), "usequery"),
    ("lazy/Suspense", _react(r"\blazy\s*\(|\bSuspense\b"), "lazy-suspense"),
    ("useTransition", _react(r"\buseTransition\b"), "usetransition"),
    ("useDeferredValue", _react(r"\buseDeferredValue\b"), "usedeferredvalue"),
    ("useActionState", _react(r"\buseActionState\b"), "form-action"),
    ("useFormStatus", _react(r"\buseFormStatus\b"), "useformstatus"),
    ("useOptimistic", _react(r"\buseOptimistic\b"), "useoptimistic"),
    ("use()", _react(r"(?<![\w.])use\s*\("), "use-hook"),
    ("Profiler", _react(r"\bProfiler\b"), "render-hemjih"),
    ("vitest", _react(r"""from ["']vitest"""), "yagaad-test"),
]

REACT_LESSONS = lessons_in_order(REACT_COURSE)

# Дасгалгүй, «урьдчилан харах жишээ» гэж кодондоо тэмдэглэсэн хичээл: React-ийн
# тоологчийг Модул 0-ийн DOM тоологчтой харьцуулж харуулна.
REACT_PREVIEWS = {"react-gej-yu-ve": {"useState"}}


# --- Python ------------------------------------------------------------------------

_STRING_METHODS = {
    "upper",
    "lower",
    "strip",
    "replace",
    "join",
    "find",
    "startswith",
    "endswith",
    "title",
    "capitalize",
    "count",
    "isdigit",
    "isalpha",
    "lstrip",
    "rstrip",
    "format",
    "center",
    "ljust",
    "rjust",
    "zfill",
}
_LIST_METHODS = {"append", "insert", "remove", "pop", "sort", "reverse", "extend", "index", "clear"}
_DICT_METHODS = {"keys", "values", "items", "get", "update", "setdefault"}


def _python_concepts(code: str) -> set[str]:
    found: set[str] = set()
    for node in ast.walk(ast.parse(code)):
        match node:
            case ast.If() | ast.IfExp() | ast.Compare():
                found.add("if/харьцуулалт")
            case ast.BoolOp() | ast.UnaryOp(op=ast.Not()):
                found.add("and/or/not")
            case ast.For():
                found.add("for")
            case ast.While() | ast.Break() | ast.Continue() | ast.AugAssign():
                found.add("while/break/continue/+=")
            case ast.ListComp() | ast.DictComp() | ast.SetComp() | ast.GeneratorExp():
                found.add("comprehension")
            case ast.List() | ast.Subscript():
                found.add("жагсаалт/индекс")
            case ast.Dict():
                found.add("толь бичиг")
            case ast.Set():
                found.add("set")
            case ast.FunctionDef() | ast.Return():
                found.add("def")
            case ast.Lambda():
                found.add("lambda")
            case ast.JoinedStr():
                found.add("f-string")
            case ast.Try():
                found.add("try/except")
            case ast.With():
                found.add("with/open")
            case ast.Import() | ast.ImportFrom():
                found.add("import")
            case ast.ClassDef():
                found.add("class")
            case ast.Call(func=ast.Name(id="enumerate")):
                found.add("enumerate")
            case ast.Call(func=ast.Attribute(attr=attr)) if attr in _STRING_METHODS:
                found.add("мөрийн метод")
            case ast.Call(func=ast.Attribute(attr=attr)) if attr in _LIST_METHODS:
                found.add("жагсаалтын метод")
            case ast.Call(func=ast.Attribute(attr=attr)) if attr in _DICT_METHODS:
                found.add("толь бичгийн метод")
    return found


def _python_rule(concept: str, taught: str) -> tuple[str, object, str]:
    return (concept, lambda code: concept in _python_concepts(code), taught)


PYTHON_RULES = [
    _python_rule("f-string", "print-ba-anhny-kod"),
    _python_rule("if/харьцуулалт", "if-elif-else"),
    _python_rule("and/or/not", "and-or-not"),
    _python_rule("for", "for-davtalt"),
    _python_rule("while/break/continue/+=", "while-break-continue"),
    _python_rule("жагсаалт/индекс", "jagsaalt-uusgeh"),
    _python_rule("жагсаалтын метод", "jagsaalt-uurchluh"),
    _python_rule("толь бичиг", "toli-bichgiin-undes"),
    _python_rule("толь бичгийн метод", "toli-bichgiin-undes"),
    _python_rule("enumerate", "tuple"),
    _python_rule("set", "set"),
    _python_rule("def", "funkts-zarlah"),
    _python_rule("мөрийн метод", "muriin-uildluud"),
    _python_rule("with/open", "fail-unshih"),
    _python_rule("import", "json-unshih-bichih"),
    _python_rule("try/except", "try-except"),
    _python_rule("comprehension", "comprehension"),
    _python_rule("class", "klass-ba-obekt"),
    _python_rule("lambda", "lambda-map-filter"),
]

PYTHON_LESSONS = lessons_in_order(PYTHON_COURSE)


def test_react_rules_point_at_existing_lessons() -> None:
    slugs = {lesson.slug for lesson in REACT_LESSONS}
    assert {taught for _, _, taught in REACT_RULES} <= slugs


@pytest.mark.parametrize("lesson", REACT_LESSONS, ids=lambda lesson: lesson.slug)
def test_react_exercises_use_only_taught_apis(lesson: LessonSpec) -> None:
    allowed = REACT_PREVIEWS.get(lesson.slug, set())
    rules = [rule for rule in REACT_RULES if rule[0] not in allowed]
    if allowed:
        assert lesson.exercise is None, (
            f"{lesson.slug}: урьдчилсан харагдац дасгалтай байж болохгүй"
        )
        assert "Урьдчилан харах" in lesson.initial_code
    found = _violations(REACT_LESSONS, lesson, rules, _react_student_code)
    assert not found, f"{lesson.slug}: {found}"


def test_python_rules_point_at_existing_lessons() -> None:
    slugs = {lesson.slug for lesson in PYTHON_LESSONS}
    assert {taught for _, _, taught in PYTHON_RULES} <= slugs


@pytest.mark.parametrize("lesson", PYTHON_LESSONS, ids=lambda lesson: lesson.slug)
def test_python_exercises_use_only_taught_syntax(lesson: LessonSpec) -> None:
    found = _violations(PYTHON_LESSONS, lesson, PYTHON_RULES)
    assert not found, f"{lesson.slug}: {found}"


# --- JavaScript ----------------------------------------------------------------------


def _scan_js(code: str) -> tuple[str, bool]:
    """Тайлбарыг хасаж, мөрийн утгыг хоосолно. `(код, ${}-тэй template байгаа эсэх)`.

    Regex-ээр биш тэмдэгт тэмдэгтээр — `"https://…"` доторх `//`-ийг тайлбар гэж
    андуурахгүй. Template literal-ийн `${…}` доторх кодыг хадгална.
    """
    out: list[str] = []
    has_template = False
    i, n = 0, len(code)
    while i < n:
        ch = code[i]
        nxt = code[i + 1] if i + 1 < n else ""
        if ch == "/" and nxt == "/":
            while i < n and code[i] != "\n":
                i += 1
            continue
        if ch == "/" and nxt == "*":
            end = code.find("*/", i + 2)
            i = n if end == -1 else end + 2
            out.append(" ")
            continue
        if ch in "'\"":
            i += 1
            while i < n and code[i] != ch and code[i] != "\n":
                i += 2 if code[i] == "\\" else 1
            out.append(ch * 2)
            i += 1
            continue
        if ch == "`":
            out.append("``")
            i += 1
            while i < n and code[i] != "`":
                if code[i] == "\\":
                    i += 2
                    continue
                if code[i] == "$" and i + 1 < n and code[i + 1] == "{":
                    has_template = True
                    depth, start = 1, i + 2
                    i += 2
                    while i < n and depth:
                        depth += {"{": 1, "}": -1}.get(code[i], 0)
                        i += 1
                    out.append(" " + code[start : i - 1] + " ")
                    continue
                i += 1
            i += 1
            continue
        out.append(ch)
        i += 1
    return "".join(out), has_template


def _js(pattern: str, flags: int = 0):
    compiled = re.compile(pattern, flags)
    return lambda scanned: bool(compiled.search(scanned[0]))


# (ойлголт, илрүүлэх функц, заадаг хичээл) — сургалтын дарааллаар.
JS_RULES: list[tuple[str, object, str]] = [
    ("let/const/var", _js(r"\b(?:let|const|var)\s+[\w\[{]"), "huvisagch"),
    ("prompt()", _js(r"\bprompt\s*\("), "too-ba-mur"),
    ("Number/parseInt/String", _js(r"\b(?:Number|parseInt|parseFloat|String)\s*\("), "too-ba-mur"),
    ("template literal ${…}", lambda scanned: scanned[1], "too-ba-mur"),
    ("typeof", _js(r"\btypeof\b"), "ugugdliin-turul"),
    ("% ++ -- += -= *= /=", _js(r"%|\+\+|--|[+\-*/]="), "arifmetik-ba-onooh"),
    (
        "харьцуулах оператор",
        _js(r"===|!==|==|!=|<=|>=|(?<![<=])<(?![<=])|(?<![=>\-])>(?![>=])"),
        "hartsuulah-ba-logik",
    ),
    ("&& || !", _js(r"&&|\|\||!(?!=)"), "hartsuulah-ba-logik"),
    ("гурвалсан оператор", _js(r"\?(?![.?])[^;\n]*:"), "gurvalsan-operator"),
    ("if/else", _js(r"\bif\s*\(|\belse\b"), "if-else-nuhtsul"),
    ("switch/case/break", _js(r"\bswitch\s*\(|\bcase\b|\bbreak\b"), "switch-salaalalt"),
    ("for", _js(r"\bfor\s*\("), "for-davtalt"),
    ("while/do", _js(r"\bwhile\s*\(|\bdo\s*\{"), "while-davtalt"),
    ("continue", _js(r"\bcontinue\b"), "break-ba-continue"),
    ("function/return", _js(r"\bfunction\b|\breturn\b"), "funkts"),
    ("=> (сум функц)", _js(r"=>"), "funkts-ilerhiilel-ba-sum-funkts"),
    ("массив [ ]", _js(r"\["), "massiv-uusgeh"),
    (
        "push/pop/shift/unshift/splice/indexOf/includes",
        _js(r"\.(?:push|pop|shift|unshift|splice|indexOf|includes)\s*\("),
        "massiv-element-nemeh-hasah",
    ),
    (
        "forEach, for…of",
        _js(r"\.forEach\s*\(|\bfor\s*\(\s*(?:const|let|var)\s+[^;)]*?\sof\b"),
        "massiv-davtah",
    ),
    (
        "map/filter/find/some/every",
        _js(r"\.(?:map|filter|find|findIndex|some|every)\s*\("),
        "map-filter-find",
    ),
    ("reduce", _js(r"\.reduce\s*\("), "reduce"),
    (
        "объект, Object.keys, for…in",
        _js(
            r"\{\s*[\w\"']+\s*:|\bObject\.(?:keys|values|entries)\b"
            r"|\bfor\s*\(\s*(?:const|let|var)\s+\w+\s+in\b"
        ),
        "obyekt-ba-shinj-chanar",
    ),
    ("delete, this", _js(r"\bdelete\b|\bthis\b"), "obyekt-metod"),
    ("... задлах, тараах", _js(r"\.\.\.|\b(?:const|let|var)\s*[\[{]"), "zadlah-ba-taraah"),
    (
        "мөрийн метод",
        _js(
            r"\.(?:toUpperCase|toLowerCase|trim|trimStart|trimEnd|slice|substring|replace"
            r"|replaceAll|startsWith|endsWith|repeat|charAt|at|padStart|padEnd)\s*\("
        ),
        "muriin-metod",
    ),
    (
        "split/join/хайлт",
        _js(r"\.(?:split|join|lastIndexOf|search|match)\s*\("),
        "muriig-haih-ba-huvaah",
    ),
    (
        "toFixed/toLocaleString",
        _js(r"\.(?:toFixed|toLocaleString)\s*\("),
        "template-literal-ba-helberjuulelt",
    ),
    ("Math", _js(r"\bMath\."), "too-taah-togloom"),
    ("JSON", _js(r"\bJSON\."), "json-tei-hamt-ashiglah"),
    ("sort", _js(r"\.sort\s*\("), "engiin-sambar"),
    ("?. ??", _js(r"\?\.|\?\?"), "anhdagch-parametr-ba-optional-chaining"),
    ("try/catch/finally", _js(r"\btry\s*\{|(?<!\.)\bcatch\b|\bfinally\b"), "try-catch-finally"),
    (
        "throw, Error, class",
        _js(r"\bthrow\b|\bnew\s+\w*Error\b|\bclass\b"),
        "throw-ba-uuriin-aldaa",
    ),
    ("setTimeout/setInterval", _js(r"\bset(?:Timeout|Interval)\s*\("), "sinhron-ba-asinhron"),
    ("Promise, then", _js(r"\bPromise\b|\.then\s*\(|\.catch\s*\("), "promise"),
    ("async/await", _js(r"\basync\b|\bawait\b"), "async-await"),
]

# Сургалтад огт заагаагүй, эсвэл sandbox-д ажиллахгүй.
JS_NEVER: list[tuple[str, object]] = [
    ("import/export (sandbox-д ES module байхгүй)", _js(r"^\s*(?:import|export)\b", re.M)),
    ("Map/Set", _js(r"\bnew\s+(?:Map|Set)\b")),
]

JS_LESSONS = lessons_in_order(JS_COURSE)


def _js_checked_code(lesson: LessonSpec) -> list[tuple[str, tuple[str, bool]]]:
    """Эхлэл кодод бэлэн бичсэн `prompt()`-той мөрийг (оролт унших) хасна."""
    given = {line.strip() for line in lesson.initial_code.splitlines() if "prompt(" in line}
    checked = []
    for where, raw in exercise_code(lesson):
        kept = "\n".join(line for line in raw.splitlines() if line.strip() not in given)
        checked.append((where, _scan_js(kept)))
    return checked


def test_js_rules_point_at_existing_lessons() -> None:
    slugs = {lesson.slug for lesson in JS_LESSONS}
    assert {taught for _, _, taught in JS_RULES} <= slugs


def test_js_scanner_ignores_comments_and_strings() -> None:
    code = 'const url = "https://x.mn/a"; // if (x) { }\nconst t = `${a % 2} if`;'
    scanned, template = _scan_js(code)
    assert "if" not in scanned and "https" not in scanned
    assert "%" in scanned and template


@pytest.mark.parametrize("lesson", JS_LESSONS, ids=lambda lesson: lesson.slug)
def test_javascript_exercises_use_only_taught_syntax(lesson: LessonSpec) -> None:
    order = [item.slug for item in JS_LESSONS]
    here = order.index(lesson.slug)
    found = []
    for where, scanned in _js_checked_code(lesson):
        for concept, detect, taught in JS_RULES:
            if order.index(taught) > here and detect(scanned):
                found.append(f"{concept} ({taught}-д заана) — {where}")
        for concept, detect in JS_NEVER:
            if detect(scanned):
                found.append(f"{concept} — {where}")
    assert not found, f"{lesson.slug}: {found}"


# --- SQL (мөрдөгчийн хэргүүд) -----------------------------------------------------------


def _strip_sql(code: str) -> str:
    """Тайлбар, текстэн утгыг хасна — `'ORDER BY'` гэх мэт текст тооцогдохгүй."""
    code = re.sub(r"/\*.*?\*/", " ", code, flags=re.S)
    code = re.sub(r"(?:--|#)[^\n]*", " ", code)
    code = re.sub(r"'(?:''|\\.|[^'\\])*'", "''", code)
    return re.sub(r'"(?:""|\\.|[^"\\])*"', '""', code)


def _sql(pattern: str):
    compiled = re.compile(pattern, re.I)
    return lambda code: compiled.search(code)


SQL_RULES: list[tuple[str, object, str]] = [
    ("SELECT", _sql(r"\bSELECT\b"), "select-ba-from"),
    ("AS нэр", _sql(r"\bAS\s+\w"), "alias-ba-tootsoolson-bagana"),
    ("ORDER BY / DISTINCT", _sql(r"\bORDER\s+BY\b|\bDISTINCT\b"), "order-by-ba-distinct"),
    ("LIMIT", _sql(r"\bLIMIT\b|\bOFFSET\b"), "limit-top-offset-fetch"),
    ("WHERE", _sql(r"\bWHERE\b"), "haritsuulah-ba-logik-operator"),
    ("IN / BETWEEN / LIKE", _sql(r"\bIN\s*\(|\bBETWEEN\b|\bLIKE\b"), "in-between-like"),
    ("IS NULL", _sql(r"\bIS\s+(?:NOT\s+)?NULL\b"), "null-ba-gurvan-utgat-logik"),
    (
        "текстийн функц",
        _sql(
            r"\b(?:CONCAT|CONCAT_WS|UPPER|LOWER|CHAR_LENGTH|LENGTH|SUBSTRING|SUBSTR|TRIM"
            r"|REPLACE|LEFT|RIGHT|LOCATE)\s*\("
        ),
        "tekstiin-funkts",
    ),
    (
        "тоон функц",
        _sql(r"\b(?:ROUND|FLOOR|CEIL|CEILING|ABS|MOD|TRUNCATE)\s*\(|\bDIV\b"),
        "toon-funkts-ba-huvaalt",
    ),
    (
        "огнооны функц",
        _sql(
            r"\b(?:NOW|CURDATE|CURRENT_DATE|DATE_FORMAT|DATEDIFF|DATE_ADD|DATE_SUB|TIMESTAMPDIFF"
            r"|YEAR|MONTH|DAY|DAYOFWEEK|HOUR|MINUTE|DATE|TIME)\s*\("
        ),
        "ognoo-tsagiin-funkts",
    ),
    ("CAST / CONVERT", _sql(r"\b(?:CAST|CONVERT)\s*\("), "cast-ba-convert"),
    ("COUNT/SUM/AVG/MIN/MAX", _sql(r"\b(?:COUNT|SUM|AVG|MIN|MAX)\s*\("), "count-sum-avg-min-max"),
    ("GROUP BY", _sql(r"\bGROUP\s+BY\b"), "group-by-buleglel"),
    ("HAVING", _sql(r"\bHAVING\b"), "having-ba-logik-daraalal"),
    (
        "CREATE TABLE",
        _sql(r"\bCREATE\s+(?:TABLE|DATABASE|SCHEMA)\b"),
        "mysql-create-database-table",
    ),
    (
        "ALTER / DROP TABLE",
        _sql(r"\bALTER\s+TABLE\b|\bDROP\s+TABLE\b"),
        "alter-table-ba-drop-table",
    ),
    ("INSERT", _sql(r"\bINSERT\b"), "insert-ba-last-insert-id"),
    ("UPDATE", _sql(r"(?<!ON )\bUPDATE\s+\w"), "update-ba-join-update"),
    (
        "DELETE / TRUNCATE",
        _sql(r"\bDELETE\s+FROM\b|\bTRUNCATE\s+(?:TABLE\s+)?\w"),
        "delete-truncate-drop",
    ),
    ("FOREIGN KEY", _sql(r"\bFOREIGN\s+KEY\b|\bREFERENCES\b"), "foreign-key-cascade-set-null"),
    ("JOIN", _sql(r"\bJOIN\b"), "inner-join"),
    ("LEFT / RIGHT JOIN", _sql(r"\b(?:LEFT|RIGHT)\s+(?:OUTER\s+)?JOIN\b"), "left-right-join"),
    ("CROSS JOIN", _sql(r"\bCROSS\s+JOIN\b"), "full-self-cross-join"),
    ("дэд асуулга", _sql(r"\(\s*SELECT\b"), "scalar-in-ded-asuulga"),
    ("EXISTS", _sql(r"\bEXISTS\s*\("), "exists-correlated-ded-asuulga"),
    (
        "UNION / INTERSECT / EXCEPT",
        _sql(r"\b(?:UNION|INTERSECT|EXCEPT)\b"),
        "union-intersect-except",
    ),
    ("CASE", _sql(r"\bCASE\b"), "case-ilerhiilel"),
    ("COALESCE / NULLIF", _sql(r"\b(?:COALESCE|NULLIF|IFNULL)\s*\("), "coalesce-nullif-isnull"),
    ("VIEW", _sql(r"\bCREATE\s+(?:OR\s+REPLACE\s+)?VIEW\b"), "view-uusgeh-mysql-tsql"),
    ("INDEX", _sql(r"\bCREATE\s+(?:UNIQUE\s+)?INDEX\b"), "index-btree-clustered"),
    ("EXPLAIN", _sql(r"\bEXPLAIN\b"), "explain-execution-plan"),
    (
        "transaction",
        _sql(r"\bSTART\s+TRANSACTION\b|\bCOMMIT\b|\bROLLBACK\b|\bSAVEPOINT\b"),
        "transaction-acid-savepoint",
    ),
    (
        "WITH (CTE)",
        _sql(r"\bWITH\s+(?!RECURSIVE)\w+\s*(?:\([^)]*\)\s*)?AS\s*\("),
        "cte-with-uguulber",
    ),
    ("WITH RECURSIVE", _sql(r"\bWITH\s+RECURSIVE\b"), "recursive-cte"),
    (
        "цонхон функц",
        _sql(r"\bOVER\s*\(|\b(?:ROW_NUMBER|DENSE_RANK|RANK)\s*\("),
        "row-number-rank-dense-rank",
    ),
    ("LAG / LEAD", _sql(r"\b(?:LAG|LEAD)\s*\("), "running-total-lag-lead"),
    ("хувьсагч", _sql(r"@\w+|\bDECLARE\b"), "tsql-huvisagch-udirdlagyn-urgal"),
    ("процедур", _sql(r"\bCREATE\s+PROCEDURE\b|\bCALL\b|\bDELIMITER\b"), "mysql-stored-procedure"),
    ("функц үүсгэх", _sql(r"\bCREATE\s+FUNCTION\b"), "user-defined-function"),
    ("TRIGGER", _sql(r"\bCREATE\s+TRIGGER\b"), "mysql-trigger"),
    ("SIGNAL / HANDLER", _sql(r"\bSIGNAL\b|\bHANDLER\b"), "mysql-aldaa-handler-signal"),
    (
        "GRANT / хэрэглэгч",
        _sql(r"\bGRANT\b|\bREVOKE\b|\bCREATE\s+(?:USER|ROLE)\b"),
        "hereglegch-erh-grant-revoke",
    ),
    ("PREPARE", _sql(r"\bPREPARE\b|\bEXECUTE\b"), "sql-injection-parameterized"),
]

SQL_LESSONS = lessons_in_order(SQL_COURSE)
SQL_CASES = [lesson for lesson in SQL_LESSONS if lesson.exercise and lesson.exercise.answers]


def test_sql_rules_point_at_existing_lessons() -> None:
    slugs = {lesson.slug for lesson in SQL_LESSONS}
    assert {taught for _, _, taught in SQL_RULES} <= slugs


@pytest.mark.parametrize("lesson", SQL_CASES, ids=lambda lesson: lesson.slug)
def test_sql_cases_use_only_taught_syntax(lesson: LessonSpec) -> None:
    found = _violations(SQL_LESSONS, lesson, SQL_RULES, _strip_sql)
    assert not found, f"{lesson.slug}: {found}"


# --- Flowgorithm -------------------------------------------------------------------


def _flow_nodes(source: str) -> list[dict]:
    """Схемийн бүх дүрс — салаа, давталтын доторхыг оролцуулан."""
    flat: list[dict] = []

    def visit(nodes: list[dict]) -> None:
        for node in nodes:
            flat.append(node)
            for branch in ("trueBranch", "falseBranch", "body"):
                visit(node.get(branch, []))

    visit(json.loads(source)["nodes"])
    return flat


_FLOW_FIELDS = ("kind", "name", "dataType", "expression", "start", "end", "step", "direction")


def _flow_key(node: dict) -> tuple:
    return tuple(node.get(field) for field in _FLOW_FIELDS)


def _student_nodes(lesson: LessonSpec) -> list[dict]:
    """Жишиг шийдлийн эхлэл схемд байхгүй дүрсүүд — сурагч өөрөө нэмж, засна."""
    assert lesson.exercise is not None
    starter = [_flow_key(node) for node in _flow_nodes(lesson.initial_code)]
    added = []
    for node in _flow_nodes(lesson.exercise.solution):
        key = _flow_key(node)
        if key in starter:
            starter.remove(key)
        else:
            added.append(node)
    return added


def _flow_text(node: dict) -> str:
    """Илэрхийллүүд — хашилт доторх текст `""` болно (доторх тэмдэг тооцогдохгүй)."""
    text = " ".join(str(node.get(field, "")) for field in ("expression", "start", "end", "step"))
    return re.sub(r'"[^"]*"', '""', text)


def _flow_kind(*kinds: str):
    return lambda node: node["kind"] in kinds


def _flow_expression(pattern: str):
    return lambda node: re.search(pattern, _flow_text(node), re.I)


def _flow_calls(node: dict) -> bool:
    words = re.findall(r"([a-z]\w*)\s*\(", _flow_text(node), re.I)
    return any(word.lower() not in {"and", "or", "not", "mod"} for word in words)


FLOW_RULES: list[tuple[str, object, str]] = [
    ("Output", _flow_kind("output"), "program-gej-yu-ve"),
    ('текст ("…")', _flow_expression(r'""'), "suulgah-ehleh"),
    ("Declare", _flow_kind("declare"), "huvisagch-turul"),
    ("Assignment", _flow_kind("assign"), "utga-onooh"),
    ("Input", _flow_kind("input"), "input-mendchilgee"),
    ("& (залгах)", _flow_expression(r"&"), "input-mendchilgee"),
    ("mod", _flow_expression(r"\bmod\b"), "operator-uldegdel"),
    ("харьцуулалт", _flow_expression(r"==|!=|<|>"), "hartsuulalt-boolean"),
    (
        "Boolean",
        lambda node: (
            node.get("dataType") == "Boolean" or _flow_expression(r"\b(?:true|false)\b")(node)
        ),
        "hartsuulalt-boolean",
    ),
    ("If", _flow_kind("if"), "if-hoyor-zam"),
    ("and/or/not", _flow_expression(r"\b(?:and|or|not)\b"), "logik-zuv-orolt"),
    ("While", _flow_kind("while"), "while-davtalt"),
    ("For", _flow_kind("for"), "for-tooluur"),
]

# Сургалтад огт заагаагүй — даалгаварт хэрэглэхгүй.
FLOW_NEVER: list[tuple[str, object]] = [
    ("Do", _flow_kind("do")),
    ("Comment, Breakpoint", _flow_kind("comment", "breakpoint")),
    ("функц (Len, ToFixed, …)", _flow_calls),
    ("^", _flow_expression(r"\^")),
    ("%, &&, ||, !, =, <>", _flow_expression(r"%|&&|\|\||!(?!=)|(?<![=!<>])=(?!=)|<>")),
]

# Эхлэл схемийн бэлэн дүрс — хичээл өөрөө тайлбарладаг. Даалгавар бүр оролт уншиж,
# өөр оролттой нууц тестээр шалгагддаг (эзэмшигч, 2026-09-30) тул Declare, Input-ийг
# заахаас өмнөх хичээлд оролт авах Declare + Input бэлэн — C-ийн бэлэн `scanf("%d", …)`
# мөртэй адил. Сурагч тэдгээрийг нэмэх, засах биш, зөвхөн Output-ийг (Модул 2-т
# Declare, Assignment-ийг) өөрөө нэмж засна; тэр нь дээрх дүрмээр хатуу шалгагдана.
# «huvisagch-turul»-д сурагч зөвхөн Declare нэмнэ; «utga-onooh»-д Assignment нэмнэ.
_READY_INPUT = {"Declare", "Input"}
FLOW_PREVIEWS = {
    "program-gej-yu-ve": _READY_INPUT,
    "algoritm-alham": _READY_INPUT,
    "orolt-garalt": _READY_INPUT,
    "suulgah-ehleh": _READY_INPUT,
    "durs-sum": _READY_INPUT,
    "anhnii-output": _READY_INPUT,
    "huvisagch-turul": {"Input"},
    "utga-onooh": {"Input"},
}

FLOW_LESSONS = lessons_in_order(FLOWGORITHM_COURSE)


def test_flow_rules_point_at_existing_lessons() -> None:
    slugs = {lesson.slug for lesson in FLOW_LESSONS}
    assert {taught for _, _, taught in FLOW_RULES} <= slugs
    assert set(FLOW_PREVIEWS) <= slugs


@pytest.mark.parametrize("lesson", FLOW_LESSONS, ids=lambda lesson: lesson.slug)
def test_flowgorithm_tasks_use_only_taught_shapes(lesson: LessonSpec) -> None:
    order = [item.slug for item in FLOW_LESSONS]
    here = order.index(lesson.slug)
    checked = [("эхлэл схем", node) for node in _flow_nodes(lesson.initial_code)]
    checked += [("сурагчийн дүрс", node) for node in _student_nodes(lesson)]
    found = set()
    for where, node in checked:
        for concept, detect, taught in FLOW_RULES:
            if order.index(taught) <= here or not detect(node):
                continue
            if where == "эхлэл схем" and concept in FLOW_PREVIEWS.get(lesson.slug, set()):
                continue
            found.add(f"{concept} ({taught}-д заана) — {where}")
        for concept, detect in FLOW_NEVER:
            if detect(node):
                found.add(f"{concept} (заагаагүй) — {where}")
    assert not found, f"{lesson.slug}: {sorted(found)}"
