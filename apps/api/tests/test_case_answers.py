"""SQL-ийн мөрдөгчийн хэрэг — `POST /lessons/{id}/answer` (`app/services/case_service.py`)."""

import httpx
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.rate_limit import InMemoryRateLimitBackend
from app.services.case_service import is_correct, normalize_answer
from tests.conftest import login_as, make_user
from tests.factories import make_course_with_lessons

CASE = {
    "kind": "answer",
    "statement": "Хэн хулгай хийсэн бэ?",
    "tests": [],
    "tips": "- WHERE-ээр шүүгээрэй.",
    "solution": "SELECT ner FROM irgen WHERE id = 7;",
    "answers": ["Анужин", "Анужин Бат"],
}


async def _case_lesson(db: AsyncSession, **course):
    course_row, lessons = await make_course_with_lessons(db, slug="sql-undes", **course)
    lessons[0].language = "mysql"
    lessons[0].exercise = dict(CASE)
    await db.commit()
    return course_row, lessons


async def _student(client: httpx.AsyncClient, api: str, db: AsyncSession) -> None:
    await make_user(db, "murdugch@test.mn")
    await login_as(client, api, "murdugch@test.mn")


@pytest.mark.parametrize(
    "answer", ["Анужин", " анужин ", "«Анужин»", "АНУЖИН!", "Анужин   Бат", '"анужин бат".']
)
def test_answers_ignore_case_spacing_and_punctuation(answer: str) -> None:
    assert is_correct(answer, CASE["answers"])


@pytest.mark.parametrize("answer", ["Ануж", "Анужин Баатар", "Бат", "", "   "])
def test_other_answers_are_wrong(answer: str) -> None:
    assert not is_correct(answer, CASE["answers"])


def test_normalization_keeps_hyphens_and_digits() -> None:
    assert normalize_answer(" УБА-4512 ") == "уба-4512"
    assert normalize_answer("12 500₮") == "12 500"
    assert normalize_answer("Ёндон") == normalize_answer("Ендон")


async def test_correct_answer_completes_the_lesson(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    course, lessons = await _case_lesson(db)
    await _student(client, api, db)
    await client.post(f"{api}/courses/{course.id}/enroll")

    wrong = await client.post(f"{api}/lessons/{lessons[0].id}/answer", json={"answer": "Бат"})
    assert wrong.status_code == 200
    assert wrong.json() == {
        "correct": False,
        "completed": False,
        "course_progress": None,
        "new_badges": [],
    }

    right = await client.post(f"{api}/lessons/{lessons[0].id}/answer", json={"answer": "анужин"})
    body = right.json()
    assert body["correct"] is True
    assert body["completed"] is True
    assert body["course_progress"]["completed_lessons"] == 1

    player = await client.get(f"{api}/courses/{course.slug}/lessons/{lessons[0].slug}")
    assert player.json()["lesson"]["completed"] is True


async def test_answers_never_reach_the_browser(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    course, lessons = await _case_lesson(db)
    await _student(client, api, db)

    player = await client.get(f"{api}/courses/{course.slug}/lessons/{lessons[0].slug}")
    exercise = player.json()["lesson"]["exercise"]
    assert exercise == {"statement": CASE["statement"], "tests": [], "kind": "answer"}
    assert "Анужин" not in player.text
    detail = await client.get(f"{api}/lessons/{lessons[0].id}")
    assert "Анужин" not in detail.text


async def test_not_enrolled_student_can_solve_but_progress_is_not_saved(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    _, lessons = await _case_lesson(db)
    await _student(client, api, db)

    response = await client.post(f"{api}/lessons/{lessons[0].id}/answer", json={"answer": "Анужин"})
    assert response.json()["correct"] is True
    assert response.json()["completed"] is False


async def test_lessons_without_a_case_are_rejected(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    _, lessons = await _case_lesson(db)
    await _student(client, api, db)

    response = await client.post(f"{api}/lessons/{lessons[1].id}/answer", json={"answer": "x"})
    assert response.status_code == 404
    assert response.json()["detail"]["code"] == "CASE_NOT_FOUND"


async def test_answer_requires_login(client: httpx.AsyncClient, api: str, db: AsyncSession) -> None:
    _, lessons = await _case_lesson(db)
    response = await client.post(f"{api}/lessons/{lessons[0].id}/answer", json={"answer": "x"})
    assert response.status_code == 401


async def test_locked_case_needs_a_plan(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    course, lessons = await make_course_with_lessons(
        db, slug="sql-tolbort", lesson_count=2, is_free=False, free_lessons=1
    )
    lessons[1].language = "mysql"
    lessons[1].exercise = dict(CASE)
    await db.commit()
    await _student(client, api, db)
    await client.post(f"{api}/courses/{course.id}/enroll")

    response = await client.post(f"{api}/lessons/{lessons[1].id}/answer", json={"answer": "Анужин"})
    assert response.status_code == 402


async def test_guessing_is_rate_limited_per_case(
    client: httpx.AsyncClient, api: str, db: AsyncSession, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(settings, "rate_limit_enabled", True)
    monkeypatch.setattr(settings, "case_answer_rate_limit_max", 3)
    monkeypatch.setattr("app.core.rate_limit.backend", InMemoryRateLimitBackend())
    _, lessons = await _case_lesson(db)
    await _student(client, api, db)

    url = f"{api}/lessons/{lessons[0].id}/answer"
    for guess in ("Бат", "Дорж", "Сараа"):
        assert (await client.post(url, json={"answer": guess})).status_code == 200
    blocked = await client.post(url, json={"answer": "Анужин"})
    assert blocked.status_code == 429
