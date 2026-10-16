"""emcc/em++-ийг хязгаартайгаар ажиллуулна.

Контейнерийн тусгаарлалтаас гадна:
  • Хүсэлт бүр өөрийн түр хавтастай, дууссаны дараа устгагдана.
  • Нийт хугацаа хязгаартай — хэтэрвэл процессын бүлгийг (clang, wasm-ld)
    бүхэлд нь устгана.
  • prlimit: CPU хугацаа, файлын хэмжээ, санах ойн хаягийн зай.
  • Мессежийг хязгаартай уншина — хэтэрвэл процессыг зогсооно.
  • stdin хаалттай — `#include "/dev/stdin"` гацаахгүй.

Хөрвүүлэгч сурагчийн кодыг ХЭЗЭЭ Ч ажиллуулахгүй — зөвхөн WebAssembly
модуль гаргана.
"""

import asyncio
import contextlib
import math
import os
import shutil
import signal
import tempfile
from dataclasses import dataclass
from pathlib import Path

from compiler import diagnostics
from compiler.settings import settings
from compiler.toolchain import OUTPUT_NAME, Toolchain
from compiler.wasm import WARNINGS_SECTION, append_custom_section

FALLBACK_FAILURE = "Хөрвүүлэлт амжилтгүй боллоо."
OUTPUT_TOO_LARGE = "Хөрвүүлсэн програм хэт том байна. Кодоо багасгаад дахин оролдоно уу."


@dataclass(frozen=True)
class Compiled:
    """WebAssembly модуль. Анхааруулга байвал custom section-д орсон."""

    module: bytes

    @property
    def size(self) -> int:
        return len(self.module)


@dataclass(frozen=True)
class Failed:
    """Сурагчийн кодонд алдаа байна. Ижил код үргэлж ижил алдаа өгнө."""

    diagnostics: str

    @property
    def size(self) -> int:
        return len(self.diagnostics.encode("utf-8"))


Outcome = Compiled | Failed


class CompileTimeoutError(Exception):
    """Хугацаандаа дуусаагүй. Кэшлэхгүй — серверийн ачааллаас хамаарна."""


_PRLIMIT = shutil.which("prlimit")


def _with_limits(args: list[str]) -> list[str]:
    if _PRLIMIT is None:
        return args
    limits = [
        f"--cpu={math.ceil(settings.timeout_seconds) + 1}",
        f"--fsize={settings.max_file_bytes}",
        "--core=0",
    ]
    if settings.max_address_space_bytes:
        limits.append(f"--as={settings.max_address_space_bytes}")
    return [_PRLIMIT, *limits, *args]


def _environment(work_dir: Path) -> dict[str, str]:
    """Контейнерийн орчин + хүсэлтийн түр хавтас.

    АНХААР: сурагч `#include "/proc/self/environ"` бичиж орчныг хэвлэж
    чадна. Энэ контейнерт нууц мэдээлэл хэзээ ч бүү өг.
    """
    env = dict(os.environ)
    env.update(HOME=str(work_dir), TMPDIR=str(work_dir), LC_ALL="C.UTF-8")
    return env


def _kill(process: asyncio.subprocess.Process) -> None:
    # `start_new_session` тул pid нь бүлгийн дугаар — clang, wasm-ld хамт үхнэ.
    with contextlib.suppress(ProcessLookupError):
        os.killpg(process.pid, signal.SIGKILL)


async def _read_bounded(stream: asyncio.StreamReader, limit: int) -> tuple[bytes, bool]:
    data = bytearray()
    while chunk := await stream.read(65536):
        data.extend(chunk)
        if len(data) > limit:
            return bytes(data[:limit]), True
    return bytes(data), False


async def compile_source(toolchain: Toolchain, source: str) -> Outcome:
    work_dir = Path(tempfile.mkdtemp(prefix="compile-", dir=settings.work_dir))
    try:
        (work_dir / toolchain.source_name).write_text(source, encoding="utf-8")

        process = await asyncio.create_subprocess_exec(
            *_with_limits(toolchain.command(source)),
            cwd=work_dir,
            env=_environment(work_dir),
            stdin=asyncio.subprocess.DEVNULL,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
            start_new_session=True,
        )
        assert process.stdout is not None

        try:
            async with asyncio.timeout(settings.timeout_seconds):
                output, flooded = await _read_bounded(process.stdout, settings.max_capture_bytes)
                if flooded:
                    _kill(process)
                returncode = await process.wait()
        except TimeoutError:
            raise CompileTimeoutError from None
        finally:
            if process.returncode is None:
                _kill(process)
                await process.wait()

        # Дохиогоор үхсэн ч мессеж хэтрээгүй бол — CPU хязгаарт хүрсэн.
        if returncode < 0 and not flooded:
            raise CompileTimeoutError

        text = diagnostics.clean(
            output.decode("utf-8", errors="replace"),
            strip_prefixes=(f"{work_dir}/", f"{settings.artifacts_dir}/"),
        )
        if flooded and not text.endswith(diagnostics.TRUNCATED_NOTE):
            text = f"{text}\n{diagnostics.TRUNCATED_NOTE}"

        module_path = work_dir / OUTPUT_NAME
        if returncode != 0 or not module_path.is_file():
            return Failed(text or FALLBACK_FAILURE)
        if module_path.stat().st_size > settings.max_output_bytes:
            return Failed(OUTPUT_TOO_LARGE)

        module = module_path.read_bytes()
        if text:
            module = append_custom_section(module, WARNINGS_SECTION, text.encode("utf-8"))
        return Compiled(module)
    finally:
        shutil.rmtree(work_dir, ignore_errors=True)
