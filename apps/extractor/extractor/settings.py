"""Задлагч үйлчилгээний тохиргоо — орчны хувьсагчаас нэг удаа уншина.

Талбар бүрийн хувьсагч нь `EXTRACTOR_<НЭР>` (жишээ нь `max_bytes` →
`EXTRACTOR_MAX_BYTES`). Дэд процесс (`extractor.worker`) энэ модулийг дахин
уншдаг бөгөөд эцэг процесс өөрийн утгуудыг `child_environment()`-ээр
дамжуулна — тестэд `settings`-ийг өөрчлөхөд дэд процесст ч хүрнэ.
"""

import os
import tempfile
from dataclasses import dataclass, field, fields
from pathlib import Path
from typing import TypeVar

SERVICE_ROOT = Path(__file__).resolve().parent.parent

T = TypeVar("T", int, float, str)


def _env(name: str, default: T) -> T:
    value = os.environ.get(f"EXTRACTOR_{name.upper()}")
    return type(default)(value) if value else default


@dataclass
class Settings:
    # HTTP хүсэлтийн биеийн дээд хэмжээ. API нь ~20 MB хүртэлх файл хүлээн авна.
    max_bytes: int = field(default_factory=lambda: _env("max_bytes", 25_000_000))
    # PDF-ийн хуудас, PPTX-ийн слайд, DOCX-ийн хэсгийн дээд тоо.
    max_pages: int = field(default_factory=lambda: _env("max_pages", 300))
    # Бүх хуудасны нийт текст. Хэтэрвэл үлдсэнийг хасч `truncated: true`.
    max_text_chars: int = field(default_factory=lambda: _env("max_text_chars", 1_000_000))
    # DOCX-ийн хэсэг энэ урттай болбол гарчиггүй ч шинэ хэсэг эхэлнэ.
    section_chars: int = field(default_factory=lambda: _env("section_chars", 4_000))
    # Зэрэг ажиллах дэд процесс. Нэг нь ~50–300 MB санах ой.
    max_concurrency: int = field(default_factory=lambda: _env("max_concurrency", 1))
    # Дараалалд хүлээх хугацаа. Хэтэрвэл 503 `busy`.
    queue_timeout_seconds: float = field(
        default_factory=lambda: _env("queue_timeout_seconds", 20.0)
    )
    # Дэд процессын нийт (ханын цагийн) хугацаа. Хэтэрвэл процессын бүлгийг устгана.
    timeout_seconds: float = field(default_factory=lambda: _env("timeout_seconds", 45.0))
    # Дэд процессын CPU хугацаа (RLIMIT_CPU).
    cpu_seconds: int = field(default_factory=lambda: _env("cpu_seconds", 30))
    # Дэд процессын санах ойн хаягийн зай (RLIMIT_AS). 0 бол хязгаарлахгүй.
    max_address_space_bytes: int = field(
        default_factory=lambda: _env("max_address_space_bytes", 768 * 1024 * 1024)
    )
    # Дэд процессын бичих ганц файлын дээд хэмжээ (RLIMIT_FSIZE). Юу ч бичих ёсгүй.
    max_file_bytes: int = field(default_factory=lambda: _env("max_file_bytes", 1024 * 1024))
    # Дэд процессын нээлттэй файлын тоо (RLIMIT_NOFILE).
    max_open_files: int = field(default_factory=lambda: _env("max_open_files", 64))
    # Дэд процессын stdout (JSON). 1 сая тэмдэгт кирилл ~2 MB болдог.
    max_output_bytes: int = field(
        default_factory=lambda: _env("max_output_bytes", 32 * 1024 * 1024)
    )
    # ZIP (PPTX, DOCX) bomb-оос хамгаалах хязгаарууд.
    max_zip_entries: int = field(default_factory=lambda: _env("max_zip_entries", 5_000))
    max_zip_bytes: int = field(default_factory=lambda: _env("max_zip_bytes", 200_000_000))
    max_part_bytes: int = field(default_factory=lambda: _env("max_part_bytes", 50_000_000))
    # Хүсэлтийн түр файл. Контейнерт tmpfs.
    work_dir: str = field(default_factory=lambda: _env("work_dir", tempfile.gettempdir()))

    def child_environment(self) -> dict[str, str]:
        """Дэд процессын ЦӨӨН орчин — эцэг процессын орчноос юу ч өвлөхгүй."""
        env = {
            f"EXTRACTOR_{item.name.upper()}": str(getattr(self, item.name)) for item in fields(self)
        }
        env.update(
            PYTHONPATH=str(SERVICE_ROOT),
            PYTHONDONTWRITEBYTECODE="1",
            PYTHONIOENCODING="utf-8",
            LC_ALL="C.UTF-8",
            HOME=self.work_dir,
            TMPDIR=self.work_dir,
        )
        return env


settings = Settings()
