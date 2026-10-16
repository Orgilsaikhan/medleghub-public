"""Хөрвүүлэгчийн мессежийг сурагчид харуулахад бэлдэнэ.

emcc нь clang болон wasm-ld-г ажиллуулдаг бөгөөд тэдгээрийн мессежид
серверийн дотоод зам, бүтэн командын мөр орно. Сурагчид хэрэгтэй нь
`main.c:12:5: error: ...` мөр ба кодын хэсэг — үлдсэнийг цэвэрлэнэ.
"""

import re
from collections.abc import Iterable

MAX_CHARS = 20_000
TRUNCATED_NOTE = "… (мессеж хэт урт тул таслав)"

# Дэд процесс амжилтгүй болоход emcc нь дотоод командаа бүтнээр хэвлэдэг:
#   emcc: error: '/emsdk/upstream/bin/clang ... main.c' failed (returned 1)
_DRIVER_FAILURE = re.compile(r"^em(?:cc|\+\+): error: '.*' failed \(returned -?\d+\)\s*$")

# emcc-ийн түр хавтас: /tmp/.../emscripten_temp_n1wjpugy/main.o → main.o. Ажлын
# хавтасны угтварыг өмнө нь хассан бол `emscripten_temp_...`-ээр эхэлж болно.
_EMSCRIPTEN_TEMP = re.compile(r"(?:\S*/)?emscripten_temp_[^/\s]+/")

# Системийн толгой файл ба сан:
#   /emsdk/upstream/emscripten/cache/sysroot/include/c++/v1/vector → c++/v1/vector
_SYSROOT = re.compile(r"\S*/cache/sysroot/(?:include|lib/wasm32-emscripten)/")

# wasm-ld: C++-ийн нэрийг задалсан хэлбэрээр бичдэг — `Angi::hevleh() const`.
_UNDEFINED_SYMBOL = re.compile(r"undefined symbol: ([^\s(]+)")


def _hint(line: str) -> str | None:
    """Линкийн алдааг шинэ суралцагчид ойлгомжтой болгоно."""
    match = _UNDEFINED_SYMBOL.search(line)
    if match is None:
        return None
    name = match.group(1)
    # Emscripten `main`-ийг `__main_void`/`__main_argc_argv`-аар дууддаг, C++-д
    # түүнийг `--wrap=__main_void`-аар ороодог.
    if name in {"main", "__main_argc_argv", "__main_void", "__real___main_void"}:
        return "`main` функц олдсонгүй — програм бүр `int main()` функцээс эхэлнэ."
    return f"`{name}`-г зарласан ч биеийг нь бичээгүй эсвэл нэрийг нь буруу бичсэн байна."


def clean(output: str, strip_prefixes: Iterable[str] = ()) -> str:
    """Дотоод зам, командын мөрийг хасаж, хэт урт мессежийг таслана."""
    prefixes = tuple(strip_prefixes)
    lines: list[str] = []
    hints: set[str] = set()

    for raw in output.splitlines():
        if _DRIVER_FAILURE.match(raw):
            continue

        line = raw
        for prefix in prefixes:
            line = line.replace(prefix, "")
        line = _EMSCRIPTEN_TEMP.sub("", line)
        line = _SYSROOT.sub("", line)
        lines.append(line.rstrip())

        hint = _hint(line)
        if hint and hint not in hints:
            hints.add(hint)
            lines.append(f"  ↳ {hint}")

    text = "\n".join(lines).strip("\n")
    if len(text) > MAX_CHARS:
        text = text[:MAX_CHARS].rstrip() + "\n" + TRUNCATED_NOTE
    return text
