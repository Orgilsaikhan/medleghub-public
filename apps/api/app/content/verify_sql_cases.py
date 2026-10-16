"""SQL-ийн мөрдөгчийн хэргүүдийг жинхэнэ MySQL sandbox дээр шалгана.

    cd apps/api
    python -m app.content.verify_sql_cases                  # sql-runner-ийн image-д medleg_hot бий
    python -m app.content.verify_sql_cases --with-dataset   # image хуучин: сангийн скриптийг урд нь нэмнэ
    python -m app.content.verify_sql_cases --only hereg-1,hereg-2

Ажиллуулагчийн хаяг `SQL_RUNNER_URL` (анхдагч http://127.0.0.1:8091) — хөгжүүлэлтийн
`docker compose`-ийн `sql-runner`. Хэрэг бүрт:

1. жишиг шийдэл алдаагүй ажиллаж, үр дүнгийн аль нэг нүд (эсвэл нэг мөрийн
   нүднүүд хамтдаа) зөв хариулттай таарна — хариултыг зөвхөн SQL-ээр олох боломжтой;
2. эхлэл код алдаагүй ажиллана, гэхдээ хариултыг шууд харуулахгүй;
3. хариулт (нэр, үг) даалгавар, хичээлийн текст, эхлэл код, зөвлөгөөнд бичигдээгүй.

Харьцуулалт нь API-тай ИЖИЛ (`app/services/case_service.normalize_answer`).
"""

import os
import sys
from pathlib import Path
from typing import Any

import httpx

from app.content.types import LessonSpec
from app.services.case_service import normalize_answer

RUNNER = os.environ.get("SQL_RUNNER_URL", "http://127.0.0.1:8091").rstrip("/")
DATASET = Path(__file__).resolve().parents[3] / "sql-runner" / "sandbox" / "medleg_hot.sql"


def case_lessons() -> list[LessonSpec]:
    from app.content.sql import SQL_COURSE

    found = {
        lesson.slug: lesson
        for module in SQL_COURSE.modules
        for lesson in module.lessons
        if lesson.exercise and lesson.exercise.answers
    }
    try:  # Сургалтад холбогдоогүй ч шалгаж болно.
        from app.content.sql import cases
    except ImportError:
        cases = None
    if cases is not None:
        extra = list(getattr(cases, "MODULE_CASES", {}).values())
        finale = getattr(cases, "FINALE", None)
        extra += list(finale.lessons) if finale else []
        for lesson in extra:
            found.setdefault(lesson.slug, lesson)
    return list(found.values())


def run(source: str, with_dataset: bool) -> dict[str, Any]:
    if with_dataset:
        source = DATASET.read_text(encoding="utf-8") + "\n" + source
    response = httpx.post(f"{RUNNER}/run", json={"source": source}, timeout=90)
    response.raise_for_status()
    return response.json()


def problems_of(outcome: dict[str, Any]) -> str | None:
    if outcome.get("error"):
        error = outcome["error"]
        return f"{error.get('line')}-р мөр: {error.get('message')}"
    if outcome.get("timed_out"):
        return "хугацаа хэтэрлээ"
    return None


def reveals(outcome: dict[str, Any], accepted: set[str]) -> bool:
    for result in outcome.get("results", []):
        for row in result.get("rows", []) if result.get("type") == "rows" else []:
            cells = [normalize_answer(cell) for cell in row if cell is not None]
            if accepted & set(cells) or normalize_answer(" ".join(cells)) in accepted:
                return True
    return False


def check(lesson: LessonSpec, with_dataset: bool) -> list[str]:
    exercise = lesson.exercise
    assert exercise is not None
    accepted = {normalize_answer(answer) for answer in exercise.answers}
    failures: list[str] = []

    solved = run(exercise.solution, with_dataset)
    if problem := problems_of(solved):
        failures.append(f"шийдэл алдаатай — {problem}")
    elif not reveals(solved, accepted):
        failures.append("шийдлийн үр дүнд зөв хариулт алга")

    started = run(lesson.initial_code, with_dataset)
    if problem := problems_of(started):
        failures.append(f"эхлэл код алдаатай — {problem}")
    elif reveals(started, accepted):
        failures.append("эхлэл код хариултыг шууд харуулж байна")

    # Тоо, богино үг текстэд санамсаргүй таарч болох тул нэр, үгийг л шалгана.
    text = normalize_answer(
        " ".join([exercise.statement, lesson.content, lesson.initial_code, exercise.tips])
    )
    for answer in accepted:
        if len(answer) >= 3 and not answer.replace(" ", "").isdigit() and answer in text:
            failures.append(f"хариулт «{answer}» текстэд бичигдсэн байна")
    return failures


def main() -> int:
    with_dataset = "--with-dataset" in sys.argv
    only = None
    if "--only" in sys.argv:
        only = set(sys.argv[sys.argv.index("--only") + 1].split(","))
    lessons = [lesson for lesson in case_lessons() if not only or lesson.slug in only]
    if not lessons:
        print("Шалгах хэрэг алга.")
        return 1
    total = 0
    for lesson in lessons:
        failures = check(lesson, with_dataset)
        total += len(failures)
        mark = "✓" if not failures else "✗"
        print(f"  {mark} {lesson.slug}")
        for failure in failures:
            print(f"      {failure}")
    print(f"\n{len(lessons)} хэрэг, {total} алдаа.")
    return 0 if total == 0 else 1


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[union-attr]
    raise SystemExit(main())
