"""Нэг файлыг тусдаа процесст задална: `python -m extractor.worker <kind> <зам>`.

Эцэг процесс (`extractor.main`) хүсэлт бүрт үүнийг шинээр эхлүүлнэ. Файлыг
нээхээс ӨМНӨ өөрийн нөөцийг хязгаарлана: санах ойн хаягийн зай, CPU хугацаа,
бичих файлын хэмжээ, нээлттэй файлын тоо. Хязгаарт хүрвэл зөвхөн энэ процесс
үхнэ — HTTP үйлчилгээ хэвээр.

Үр дүн нь stdout-д ганц JSON:
  {"ok": true, "kind": ..., "page_count": ..., "pages": [...], "truncated": ...}
  {"ok": false, "error": "<код>", "page_count": <тоо|null>, "detail": "<log-д>"}
"""

import json
import resource
import sys
from typing import Any

from extractor.document import ExtractError
from extractor.settings import Settings, settings

KINDS = ("pdf", "pptx", "docx")


def _cap(limit: int, soft: int, hard: int | None = None) -> None:
    hard = soft if hard is None else hard
    _, current_hard = resource.getrlimit(limit)
    if current_hard != resource.RLIM_INFINITY:
        hard = min(hard, current_hard)
    resource.setrlimit(limit, (min(soft, hard), hard))


def limit_resources(config: Settings) -> None:
    if config.max_address_space_bytes:
        _cap(resource.RLIMIT_AS, config.max_address_space_bytes)
    # Soft хязгаарт SIGXCPU, hard-д SIGKILL.
    _cap(resource.RLIMIT_CPU, config.cpu_seconds, config.cpu_seconds + 2)
    _cap(resource.RLIMIT_FSIZE, config.max_file_bytes)
    _cap(resource.RLIMIT_NOFILE, config.max_open_files)
    _cap(resource.RLIMIT_CORE, 0)


def extract(kind: str, path: str, config: Settings) -> dict[str, Any]:
    # Задлагч сангуудыг хязгаар тавьсны ДАРАА импортлоно.
    if kind == "pdf":
        from extractor.pdf import extract_pdf

        return extract_pdf(path, config)
    if kind == "pptx":
        from extractor.ooxml import extract_pptx

        return extract_pptx(path, config)
    if kind == "docx":
        from extractor.ooxml import extract_docx

        return extract_docx(path, config)
    raise ExtractError("unsupported")


def run(kind: str, path: str, config: Settings) -> dict[str, Any]:
    try:
        return {"ok": True, **extract(kind, path, config)}
    except ExtractError as error:
        return {
            "ok": False,
            "error": error.code,
            "page_count": error.page_count,
            "detail": error.detail,
        }
    except MemoryError:
        # RLIMIT_AS-д хүрсэн — асар том эсвэл зориуд хийсэн файл.
        return {"ok": False, "error": "corrupt", "page_count": None, "detail": "MemoryError"}
    except Exception as error:
        # Задлах боломжгүй бусад бүх файл. Мессежид файлын агуулга орж болзошгүй
        # тул зөвхөн алдааны төрлийг log-д дамжуулна.
        return {
            "ok": False,
            "error": "corrupt",
            "page_count": None,
            "detail": type(error).__name__,
        }


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 2:
        print("usage: python -m extractor.worker <pdf|pptx|docx> <path>", file=sys.stderr)
        return 2
    kind, path = args
    limit_resources(settings)
    result = run(kind, path, settings)
    # Ганц surrogate үлдсэн ч UTF-8 болгож чадна («?»).
    payload = json.dumps(result, ensure_ascii=False, separators=(",", ":"))
    sys.stdout.buffer.write(payload.encode("utf-8", errors="replace"))
    sys.stdout.buffer.flush()
    return 0


if __name__ == "__main__":
    sys.exit(main())
