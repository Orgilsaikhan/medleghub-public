"""SQL ажиллуулагчийн тохиргоо — орчны хувьсагчаас нэг удаа уншина."""

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
    # Зэрэг ажиллах MySQL сервер. Нэг нь ~160 MB санах ой + ~120 MB tmpfs.
    slots: int = field(default_factory=lambda: _int("SQLRUNNER_SLOTS", 2))
    # Нэг скриптийн нийт хугацаа. Хэтэрвэл холболтыг KILL хийнэ.
    run_timeout_seconds: float = field(
        default_factory=lambda: _float("SQLRUNNER_RUN_TIMEOUT_SECONDS", 10.0)
    )
    # Дараалал + ажиллагаа нь API-ийн 30 секундээс богино — API цэвэр 503 авна.
    queue_timeout_seconds: float = field(
        default_factory=lambda: _float("SQLRUNNER_QUEUE_TIMEOUT_SECONDS", 10.0)
    )
    max_source_bytes: int = field(
        default_factory=lambda: _int("SQLRUNNER_MAX_SOURCE_BYTES", 64_000)
    )
    max_statements: int = field(default_factory=lambda: _int("SQLRUNNER_MAX_STATEMENTS", 500))
    # Нэг үр дүнгийн олонлогоос харуулах мөр. Үлдсэнийг зөвхөн тоолно.
    max_rows: int = field(default_factory=lambda: _int("SQLRUNNER_MAX_ROWS", 200))
    # Тоолох дээд хязгаар — үүнээс олон мөр уншихгүй, ажиллагааг зогсооно.
    max_counted_rows: int = field(
        default_factory=lambda: _int("SQLRUNNER_MAX_COUNTED_ROWS", 100_000)
    )
    max_result_sets: int = field(default_factory=lambda: _int("SQLRUNNER_MAX_RESULT_SETS", 100))
    # Бүх нүдний нийт тэмдэгт. Хэтэрвэл үлдсэн statement-ийг ажиллуулахгүй.
    max_output_chars: int = field(
        default_factory=lambda: _int("SQLRUNNER_MAX_OUTPUT_CHARS", 200_000)
    )
    max_cell_chars: int = field(default_factory=lambda: _int("SQLRUNNER_MAX_CELL_CHARS", 1_000))
    # Хэдэн ажиллагааны дараа серверийг цэвэр загвараас дахин эхлүүлэх.
    restart_every: int = field(default_factory=lambda: _int("SQLRUNNER_RESTART_EVERY", 200))
    # ARM дээр анхны эхлэлт удаан байж болно.
    startup_timeout_seconds: float = field(
        default_factory=lambda: _float("SQLRUNNER_STARTUP_TIMEOUT_SECONDS", 60.0)
    )
    work_dir: Path = field(
        default_factory=lambda: Path(os.environ.get("SQLRUNNER_WORK_DIR") or tempfile.gettempdir())
    )
    # `prewarm` бүтээсэн цэвэр datadir. Image дотор зөвхөн уншигдана.
    template_dir: Path = field(
        default_factory=lambda: Path(
            os.environ.get("SQLRUNNER_TEMPLATE_DIR") or _SERVICE_ROOT / "build" / "template"
        )
    )
    # Жишээ сангуудын скрипт (`mysqld.SAMPLE_SCRIPTS`). Хичээлийн хуулбар.
    sample_dir: Path = field(
        default_factory=lambda: Path(
            os.environ.get("SQLRUNNER_SAMPLE_DIR") or _SERVICE_ROOT / "sandbox"
        )
    )
    mysqld: str = field(default_factory=lambda: os.environ.get("SQLRUNNER_MYSQLD") or "mysqld")


settings = Settings()
