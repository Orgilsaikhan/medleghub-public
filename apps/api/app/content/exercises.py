"""Дасгалыг өгөгдлийн сан болон шалгагчид бэлдэх.

Жишиг шийдэл, тестүүд зөв эсэхийг шалгах:

    python -m app.content.exercises | node ../web/scripts/verify-exercises.mjs
    python -m app.content.exercises --react | node ../web/scripts/verify-react-exercises.mjs
    python -m app.content.exercises --react --module 3 | node ../web/scripts/verify-react-exercises.mjs

Энэ модуль нь дасгалтай бүх хичээлийг (жишиг шийдэлтэй нь) JSON болгон
хэвлэнэ. Шалгагч нь шийдэл болон эхлэл кодыг хөрвүүлэгч рүү илгээж, хөтөчийн
worker-тэй ЯГ ИЖИЛ WASI shim дээр ажиллуулна:

- жишиг шийдэл бүх тестийг давах ёстой;
- эхлэл код хөрвүүлэгдэх ёстой ч бүх тестийг давах ЁСГҮЙ.

Flowgorithm-ийн даалгаврыг (`plaintext`, схемийн JSON) эдгээр скрипт алгасна —
тэдгээрийг `apps/web/tests/flowgorithm.test.mjs` (`npm run test:unit`) хөтөчийн
схемийн runtime-аар мөн адил шалгана.

Өгөгдлийн санд жишиг шийдэл, зөвлөгөө ХАМТ хадгалагдана. Хичээлийн хариу
(`LessonExercise`) тэдгээрийг агуулахгүй — сурагч «Тусламж»-ийг зөвшөөрсний
дараа л `GET /lessons/{id}/help`-ээр авна.
"""

import json
import sys
from typing import Any

from app.content.types import ExerciseSpec, ReactTestSpec, TestCaseSpec
from app.models.enums import LessonLanguage


def _test_payload(test: TestCaseSpec | ReactTestSpec) -> dict[str, Any]:
    if isinstance(test, ReactTestSpec):
        return {"name": test.name, "code": test.code, "sample": True}
    return {"stdin": test.stdin, "expected_output": test.expected_output, "sample": test.sample}


def exercise_payload(exercise: ExerciseSpec | None) -> dict[str, Any] | None:
    """`lessons.exercise` баганад бичих хэлбэр."""
    if exercise is None:
        return None
    payload: dict[str, Any] = {
        "statement": exercise.statement,
        "tests": [_test_payload(test) for test in exercise.tests],
        "tips": exercise.tips,
        "solution": exercise.solution,
    }
    if exercise.answers:
        # Хариулт нь зөвхөн өгөгдлийн санд — `LessonExercise` схем үүнийг хаяна.
        payload["kind"] = "answer"
        payload["answers"] = list(exercise.answers)
    return payload


def export(*, react: bool = False, module_number: int | None = None) -> list[dict[str, Any]]:
    """Дасгалтай хичээлүүд. `react=True` бол React-ийн БҮХ хичээл (дасгалгүй ч) —
    эхлэл код нь «Хөтөч» дээр алдаагүй ажиллахыг шалгахад. `module_number` —
    зөвхөн «Модул N — …» гарчигтай модуль."""
    from app.content import COURSES

    result: list[dict[str, Any]] = []
    for course in COURSES:
        for module in course.modules:
            if module_number is not None and not module.title.startswith(f"Модул {module_number} "):
                continue
            for lesson in module.lessons:
                is_react = lesson.language == LessonLanguage.JSX
                if react != is_react or (lesson.exercise is None and not react):
                    continue
                result.append(
                    {
                        "course": course.slug,
                        "slug": lesson.slug,
                        "language": str(lesson.language),
                        "starter": lesson.initial_code,
                        **(exercise_payload(lesson.exercise) or {}),
                    }
                )
    return result


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[union-attr]
    number = sys.argv[sys.argv.index("--module") + 1] if "--module" in sys.argv else None
    json.dump(
        export(react="--react" in sys.argv, module_number=int(number) if number else None),
        sys.stdout,
        ensure_ascii=False,
    )
