"""Хэл тус бүрийн хөрвүүлэгч ба тугууд.

Тугуудыг ЗӨВХӨН сервер тодорхойлно — сурагчийн кодоос хөрвүүлэгчийн
командын мөрөнд юу ч нэмэгдэхгүй.
"""

from dataclasses import dataclass

from compiler import pch
from compiler.settings import settings

COMPILE_FLAGS: tuple[str, ...] = (
    # -O2-оос хамаагүй хурдан хөрвүүлж, -O0-оос жижиг модуль гаргана.
    # Хичээлийн програмуудад гүйцэтгэлийн ялгаа мэдрэгдэхгүй.
    "-O1",
    # Хичээл «-Wall ашигла» гэж заадаг — анхааруулгыг сурагчид харуулна.
    "-Wall",
)

C_COMPILE_FLAGS: tuple[str, ...] = (*COMPILE_FLAGS, "-std=gnu17")

# try/catch. «Legacy» кодчилолыг Chrome 95+, Firefox 100+, Safari 15.2+
# дэмждэг — шинэ стандарт кодчилол нь хэт шинэ хөтөч шаардана. Хөрвүүлэх ба
# линк хийх аль алинд нь заавал өгнө.
EXCEPTION_FLAGS: tuple[str, ...] = ("-fwasm-exceptions", "-sWASM_LEGACY_EXCEPTIONS=1")

# Хичээл `g++ -std=c++17` гэж заадаг.
CPP_COMPILE_FLAGS: tuple[str, ...] = (*COMPILE_FLAGS, "-std=c++17", *EXCEPTION_FLAGS)

LINK_FLAGS: tuple[str, ...] = (
    # JavaScript «цавуу» кодгүй, зөвхөн WASI импорттой модуль.
    "-sSTANDALONE_WASM",
    # Анхдагч 64 KB стек нь рекурсын хичээлд бага.
    "-sSTACK_SIZE=1048576",
    "-sALLOW_MEMORY_GROWTH=1",
    "-sMAXIMUM_MEMORY=268435456",
)

OUTPUT_NAME = "main.wasm"

STDIO_SOURCE = """\
/* Сурагчийн програм бүрт холбогдоно: stdout-ийг буфергүй болгоно.
 *
 * Хөтөч дотор stdout нь мөрөөр буферлэгддэг бөгөөд musl нь stdin унших
 * үед түүнийг цэвэрлэдэггүй. Тэгвэл `printf("Нэр: ")` нь `scanf`-аас хойш
 * гарна. Терминалтай ижил дарааллын тулд буферийг унтраана.
 */
#include <stdio.h>

__attribute__((constructor))
static void medleghub_unbuffered_stdout(void) {
    setvbuf(stdout, NULL, _IONBF, 0);
}
"""

# Emscripten-д `_start` нь `__main_void`-ийг дууддаг. `int main()` бол clang
# түүнийг сурагчийн объект дотор үүсгэнэ; `int main(int, char **)` бол libc-ийн
# сул `__main_void` нь `__main_argc_argv`-ийг дуудна. Тиймээс `main` биш
# `__main_void`-ийг ороох нь хоёр хэлбэрийг хоёуланг нь хамарна.
MAIN_GUARD_WRAP = "-Wl,--wrap=__main_void"

MAIN_GUARD_SOURCE = """\
// Сурагчийн C++ програм бүрт холбогдоно (`-Wl,--wrap=__main_void`).
//
// main-аас гарсан exception нь WebAssembly-ээс JavaScript руу «нүцгэн» гарч,
// хөтөч зөвхөн `WebAssembly.Exception` гэж харуулдаг. g++-тэй ижил мессеж
// хэвлээд abort хийнэ:
//
//   terminate called after throwing an instance of 'std::out_of_range'
//     what():  vector
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cxxabi.h>
#include <exception>
#include <typeinfo>

extern "C" int __real___main_void(void);

namespace {

// abi::__cxa_demangle нь C++ модуль бүрт ~80 KB нэмдэг (жижиг програмыг 30
// гаруй дахин томруулна). Сурагчийн шидэх түгээмэл төрлүүдийг л энд задалж,
// бусдыг кодлогдсон нэрээр нь хэвлэнэ.
struct Builtin {
    const char *mangled;
    const char *name;
};

const Builtin BUILTINS[] = {
    {"i", "int"},
    {"j", "unsigned int"},
    {"l", "long"},
    {"x", "long long"},
    {"d", "double"},
    {"f", "float"},
    {"c", "char"},
    {"b", "bool"},
    {"PKc", "char const*"},
    {"Pc", "char*"},
    {"NSt3__212basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEE", "std::string"},
};

// St12out_of_range → std::out_of_range, N4bank5AldaaE → bank::Aldaa
void print_type(const char *mangled) {
    for (const Builtin &entry : BUILTINS) {
        if (std::strcmp(mangled, entry.mangled) == 0) {
            std::fputs(entry.name, stderr);
            return;
        }
    }

    char buffer[256];
    std::size_t used = 0;
    auto append = [&](const char *text, std::size_t length) {
        if (used + length >= sizeof buffer) return false;
        std::memcpy(buffer + used, text, length);
        used += length;
        return true;
    };

    const char *cursor = mangled;
    const bool nested = *cursor == 'N';
    if (nested) ++cursor;
    if (cursor[0] == 'S' && cursor[1] == 't') {
        append("std::", 5);
        cursor += 2;
        // libc++-ийн дотоод inline namespace (std::__2) — сурагчид харуулахгүй.
        if (std::strncmp(cursor, "3__2", 4) == 0) cursor += 4;
    }

    bool parsed = false;
    while (*cursor >= '1' && *cursor <= '9') {
        char *end = nullptr;
        const unsigned long length = std::strtoul(cursor, &end, 10);
        if (std::strlen(end) < length) break;
        if (parsed && !append("::", 2)) break;
        if (!append(end, length)) break;
        cursor = end + length;
        parsed = true;
        if (!nested) break;
    }
    if (nested && *cursor == 'E') ++cursor;

    if (parsed && *cursor == '\\0') {
        std::fwrite(buffer, 1, used, stderr);
    } else {
        std::fputs(mangled, stderr);
    }
}

void report_uncaught(const char *what) {
    const std::type_info *type = abi::__cxa_current_exception_type();
    std::fputs("terminate called after throwing an instance of '", stderr);
    print_type(type != nullptr ? type->name() : "?");
    std::fputs("'\\n", stderr);
    if (what != nullptr) {
        std::fputs("  what():  ", stderr);
        std::fputs(what, stderr);
        std::fputs("\\n", stderr);
    }
}

}  // namespace

extern "C" int __wrap___main_void(void) {
    try {
        return __real___main_void();
    } catch (const std::exception &error) {
        report_uncaught(error.what());
    } catch (...) {
        report_uncaught(nullptr);
    }
    std::abort();
}
"""


@dataclass(frozen=True)
class Toolchain:
    language: str
    driver: str
    source_name: str
    compile_flags: tuple[str, ...]
    link_flags: tuple[str, ...]
    uses_pch: bool = False
    guards_main: bool = False

    @property
    def flags(self) -> tuple[str, ...]:
        """Нэг дуудлагаар хөрвүүлж, линк хийх бүх туг. PCH ч яг эдгээрээр бүтнэ."""
        return (*self.compile_flags, *self.link_flags)

    def command(self, source: str) -> list[str]:
        """Сурагчийн кодонд зориулсан бүтэн командын мөр."""
        args = [self.driver, *self.flags]

        if self.uses_pch:
            chosen = pch.select(pch.leading_system_headers(source))
            if chosen is not None:
                path = pch.pch_path(settings.pch_dir, chosen)
                if path.is_file():
                    args += ["-include-pch", str(path)]

        args.append(self.source_name)

        if settings.stdio_object.is_file():
            args.append(str(settings.stdio_object))
        # Объект байхгүй үед ороовол `__wrap___main_void` олдохгүй линк унана.
        if self.guards_main and settings.main_guard_object.is_file():
            args += [str(settings.main_guard_object), MAIN_GUARD_WRAP]

        args += ["-o", OUTPUT_NAME]
        return args


TOOLCHAINS: dict[str, Toolchain] = {
    "c": Toolchain("c", "emcc", "main.c", C_COMPILE_FLAGS, LINK_FLAGS),
    "cpp": Toolchain(
        "cpp",
        "em++",
        "main.cpp",
        CPP_COMPILE_FLAGS,
        (*LINK_FLAGS, *EXCEPTION_FLAGS),
        uses_pch=True,
        guards_main=True,
    ),
}
