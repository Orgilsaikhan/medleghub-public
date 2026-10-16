"""Хөрвүүлэгчийн мессеж цэвэрлэх — жинхэнэ emcc 6.0.9-ийн гаралтаас авсан жишээ."""

from compiler.diagnostics import MAX_CHARS, TRUNCATED_NOTE, clean

COMPILE_ERROR = """\
main.c:12:14: error: expected ';' at end of declaration
   12 |     int b = 3
      |              ^
      |              ;
main.c:15:38: error: use of undeclared identifier 'c'
   15 |     printf("Үржвэр: %d\\n", a * c);
      |                                ^
2 errors generated.
emcc: error: '/emsdk/upstream/bin/clang -target wasm32-unknown-emscripten -O1 -c main.c \
-o /tmp/compile-x1/emscripten_temp_b18afhmu/main.o' failed (returned 1)
"""

UNDEFINED_FUNCTION = """\
wasm-ld: error: /tmp/compile-x1/emscripten_temp_n1wjpugy/main.o: undefined symbol: helper
emcc: error: '/emsdk/upstream/bin/wasm-ld -o main.wasm /tmp/compile-x1/emscripten_temp_n1wjpugy/\
main.o -L/emsdk/upstream/emscripten/cache/sysroot/lib/wasm32-emscripten -lc' failed (returned 1)
"""

MISSING_MAIN = """\
wasm-ld: error: /emsdk/upstream/emscripten/cache/sysroot/lib/wasm32-emscripten/\
libstandalonewasm-memgrow.a(__main_void.o): undefined symbol: main
em++: error: '/emsdk/upstream/bin/wasm-ld -o main.wasm' failed (returned 1)
"""


def test_keeps_student_facing_lines_and_drops_the_driver_command() -> None:
    cleaned = clean(COMPILE_ERROR)

    assert cleaned.startswith("main.c:12:14: error: expected ';' at end of declaration")
    assert "      |              ^" in cleaned, "Заагч `^`-ийн зай хадгалагдах ёстой"
    assert "2 errors generated." in cleaned
    assert "emcc: error:" not in cleaned
    assert "/emsdk" not in cleaned
    assert "/tmp" not in cleaned


def test_undefined_function_gets_a_hint_and_no_paths() -> None:
    cleaned = clean(UNDEFINED_FUNCTION)

    assert cleaned.splitlines()[0] == "wasm-ld: error: main.o: undefined symbol: helper"
    assert "`helper`" in cleaned
    assert "/tmp" not in cleaned
    assert "wasm-ld -o" not in cleaned


def test_missing_main_gets_its_own_hint() -> None:
    cleaned = clean(MISSING_MAIN)

    first = cleaned.splitlines()[0]
    assert first == (
        "wasm-ld: error: libstandalonewasm-memgrow.a(__main_void.o): undefined symbol: main"
    )
    assert "int main()" in cleaned
    assert "биеийг нь" not in cleaned, "main-д ерөнхий зөвлөмж давхардах ёсгүй"


def test_cpp_symbol_hint_uses_the_qualified_name() -> None:
    cleaned = clean("wasm-ld: error: main.o: undefined symbol: Angi::hevleh() const\n")

    assert "`Angi::hevleh`" in cleaned


def test_hint_is_not_repeated() -> None:
    line = "wasm-ld: error: main.o: undefined symbol: helper\n"

    assert clean(line * 3).count("↳") == 1


def test_system_header_paths_are_shortened() -> None:
    cleaned = clean(
        "/emsdk/upstream/emscripten/cache/sysroot/include/c++/v1/vector:512:5: note: candidate\n"
    )

    assert cleaned == "c++/v1/vector:512:5: note: candidate"


def test_strips_given_prefixes() -> None:
    cleaned = clean("/app/build/pch/iostream.h:1:10: note: here\n", strip_prefixes=["/app/build/"])

    assert cleaned == "pch/iostream.h:1:10: note: here"


def test_long_output_is_truncated_with_a_note() -> None:
    cleaned = clean("main.c:1:1: warning: x\n" * 5000)

    assert len(cleaned) <= MAX_CHARS + len(TRUNCATED_NOTE) + 1
    assert cleaned.endswith(TRUNCATED_NOTE)


def test_empty_output_stays_empty() -> None:
    assert clean("") == ""
    assert clean("emcc: error: 'clang main.c' failed (returned 1)\n") == ""


def test_temp_path_is_removed_after_the_work_dir_prefix() -> None:
    """Runner эхлээд ажлын хавтасны угтварыг хасна — дараа нь `emscripten_temp_` үлдэнэ."""
    output = "wasm-ld: error: /tmp/compile-a1/emscripten_temp_x9/main.o: undefined symbol: helper\n"

    cleaned = clean(output, strip_prefixes=["/tmp/compile-a1/"])

    assert cleaned.splitlines()[0] == "wasm-ld: error: main.o: undefined symbol: helper"


def test_wrapped_main_gets_the_main_hint() -> None:
    cleaned = clean("wasm-ld: error: main_guard.o: undefined symbol: __real___main_void\n")

    assert "int main()" in cleaned
