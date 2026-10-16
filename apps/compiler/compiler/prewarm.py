"""Docker image бүтээх үед НЭГ удаа ажиллана.

1. Жишээ програмуудыг хязгааргүй хөрвүүлж Emscripten-ийн system library,
   symbol list, Python bytecode-ийг бөглөнө. Runtime-д кэш зөвхөн
   уншигдана (`EM_FROZEN_CACHE=1`).
2. Сурагчийн програм бүрт холбогдох туслах объектууд.
3. C++-ийн урьдчилан хөрвүүлсэн толгой файл (PCH).
4. Жишээ програмуудыг runtime-тай ЯГ ИЖИЛ замаар (PCH, туслах объект,
   хязгаар) дахин хөрвүүлж шалгана.

Аль нэг алхам амжилтгүй бол image бүтээлт зогсоно — эвдэрсэн хөрвүүлэгч
production руу гарахгүй.
"""

import asyncio
import subprocess
import sys
import time

from compiler import pch
from compiler.runner import Compiled, compile_source
from compiler.settings import settings
from compiler.toolchain import (
    C_COMPILE_FLAGS,
    CPP_COMPILE_FLAGS,
    MAIN_GUARD_SOURCE,
    OUTPUT_NAME,
    STDIO_SOURCE,
    TOOLCHAINS,
)

SAMPLES = {
    "c": """\
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

int main(void) {
    char name[32];
    srand((unsigned) time(NULL));
    strcpy(name, "MedlegHub");
    printf("%s %.2f %d\\n", name, sqrt(2.0), rand() % 10);
    return scanf("%31s", name) == 1 ? 0 : 1;
}
""",
    "cpp": """\
#include <iostream>
#include <algorithm>
#include <iomanip>
#include <numeric>
#include <stdexcept>
#include <string>
#include <vector>

int main() {
    std::vector<int> values{3, 1, 2};
    std::sort(values.begin(), values.end());
    try {
        throw std::runtime_error("prewarm");
    } catch (const std::exception &error) {
        std::cout << error.what() << std::setw(4) << values.at(0) << std::endl;
    }
    return std::accumulate(values.begin(), values.end(), 0) == 6 ? 0 : 1;
}
""",
}


def _run(args: list[str]) -> None:
    result = subprocess.run(args, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        sys.exit(f"prewarm: {' '.join(args)}\n{result.stdout}{result.stderr}")


def fill_emscripten_cache() -> None:
    """Дутуу library-г бүтээж болзошгүй тул хугацааны хязгааргүй хөрвүүлнэ."""
    work = settings.artifacts_dir / "samples"
    work.mkdir(parents=True, exist_ok=True)
    for language, source in SAMPLES.items():
        toolchain = TOOLCHAINS[language]
        path = work / toolchain.source_name
        path.write_text(source, encoding="utf-8")
        _run([toolchain.driver, *toolchain.flags, str(path), "-o", str(work / OUTPUT_NAME)])


def build_helper_objects() -> None:
    stdio = settings.artifacts_dir / "stdio.c"
    stdio.write_text(STDIO_SOURCE, encoding="utf-8")
    _run(["emcc", *C_COMPILE_FLAGS, "-c", str(stdio), "-o", str(settings.stdio_object)])

    # C++-ийн exception загвар нь сурагчийн кодтой ижил байх ёстой.
    guard = settings.artifacts_dir / "main_guard.cpp"
    guard.write_text(MAIN_GUARD_SOURCE, encoding="utf-8")
    _run(["em++", *CPP_COMPILE_FLAGS, "-c", str(guard), "-o", str(settings.main_guard_object)])


def build_pch() -> None:
    settings.pch_dir.mkdir(parents=True, exist_ok=True)
    toolchain = TOOLCHAINS["cpp"]
    for headers in pch.PCH_SETS:
        header = settings.pch_dir / pch.header_name(headers)
        header.write_text(pch.header_text(headers), encoding="utf-8")
        # Хөрвүүлэлттэй ЯГ ИЖИЛ тугуудаар — эс бөгөөс clang PCH-г татгалзана.
        target = pch.pch_path(settings.pch_dir, headers)
        _run(
            [toolchain.driver, *toolchain.flags, "-x", "c++-header", str(header), "-o", str(target)]
        )
        print(f"prewarm: {target.name} {target.stat().st_size // 1024} KB")


async def verify_samples() -> None:
    for language, source in SAMPLES.items():
        started = time.perf_counter()
        outcome = await compile_source(TOOLCHAINS[language], source)
        if not isinstance(outcome, Compiled):
            sys.exit(f"prewarm: {language} жишээ хөрвүүлэгдсэнгүй\n{outcome.diagnostics}")
        elapsed = (time.perf_counter() - started) * 1000
        print(f"prewarm: {language} {len(outcome.module) // 1024} KB, {elapsed:.0f} ms")


def main() -> None:
    settings.artifacts_dir.mkdir(parents=True, exist_ok=True)
    fill_emscripten_cache()
    build_helper_objects()
    build_pch()
    asyncio.run(verify_samples())


if __name__ == "__main__":
    main()
