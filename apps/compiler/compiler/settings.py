"""Хөрвүүлэгч үйлчилгээний тохиргоо — орчны хувьсагчаас нэг удаа уншина."""

import os
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

_SERVICE_ROOT = Path(__file__).resolve().parent.parent


def _int(name: str, default: int) -> int:
    value = os.environ.get(name)
    return int(value) if value else default


def _float(name: str, default: float) -> float:
    value = os.environ.get(name)
    return float(value) if value else default


@dataclass
class Settings:
    max_source_bytes: int = field(default_factory=lambda: _int("COMPILER_MAX_SOURCE_BYTES", 64_000))
    # Ердийн C++ хөрвүүлэлт 1 секундээс бага. Олон дахин урт бол template «бөмбөг».
    timeout_seconds: float = field(default_factory=lambda: _float("COMPILER_TIMEOUT_SECONDS", 15.0))
    max_concurrency: int = field(
        default_factory=lambda: _int("COMPILER_MAX_CONCURRENCY", os.cpu_count() or 2)
    )
    # Дараалал + хөрвүүлэлт нь API-ийн 30 секундээс богино — API цэвэр 503/504 авна.
    queue_timeout_seconds: float = field(
        default_factory=lambda: _float("COMPILER_QUEUE_TIMEOUT_SECONDS", 10.0)
    )
    cache_bytes: int = field(
        default_factory=lambda: _int("COMPILER_CACHE_BYTES", 128 * 1024 * 1024)
    )
    max_output_bytes: int = field(
        default_factory=lambda: _int("COMPILER_MAX_OUTPUT_BYTES", 8 * 1024 * 1024)
    )
    # Хөрвүүлэгчийн мессеж үүнээс их бол (жишээ нь анхааруулгын үер) процессыг зогсооно.
    max_capture_bytes: int = field(
        default_factory=lambda: _int("COMPILER_MAX_CAPTURE_BYTES", 1024 * 1024)
    )
    # Хөрвүүлэгчийн бичих ганц файлын дээд хэмжээ. Түр .o файлуудад ч хамаарна.
    max_file_bytes: int = field(
        default_factory=lambda: _int("COMPILER_MAX_FILE_BYTES", 64 * 1024 * 1024)
    )
    # clang/wasm-ld-ийн санах ойн хаягийн зай. 0 бол хязгаарлахгүй.
    max_address_space_bytes: int = field(
        default_factory=lambda: _int("COMPILER_MAX_ADDRESS_SPACE_BYTES", 2 * 1024 * 1024 * 1024)
    )
    work_dir: str = field(
        default_factory=lambda: os.environ.get("COMPILER_WORK_DIR") or tempfile.gettempdir()
    )
    # `prewarm` бүтээсэн PCH болон туслах объект. Image дотор зөвхөн уншигдана.
    artifacts_dir: Path = field(
        default_factory=lambda: Path(
            os.environ.get("COMPILER_ARTIFACTS_DIR") or _SERVICE_ROOT / "build"
        )
    )

    @property
    def pch_dir(self) -> Path:
        return self.artifacts_dir / "pch"

    @property
    def stdio_object(self) -> Path:
        return self.artifacts_dir / "stdio.o"

    @property
    def main_guard_object(self) -> Path:
        return self.artifacts_dir / "main_guard.o"


settings = Settings()
