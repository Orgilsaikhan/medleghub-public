"""Төлбөрт хичээлийн хандалт — `app/services/access.py`.

`is_free=False` сургалтын эхний `free_lessons` хичээл бүгдэд нээлттэй,
үлдсэнийг зөвхөн Standard багцтай хэрэглэгч эсвэл админ үзнэ.
"""

from datetime import UTC, datetime, timedelta

import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import UserRole
from tests.conftest import login_as, make_user
from tests.factories import make_course_with_lessons, make_lesson, make_module


async def _paid_course(db: AsyncSession, *, lesson_count: int = 4, free_lessons: int = 2):
    return await make_course_with_lessons(
        db, slug="tolbort", lesson_count=lesson_count, is_free=False, free_lessons=free_lessons
    )


async def _student(
    client: httpx.AsyncClient, api: str, db: AsyncSession, *, plan_days: int | None = None
) -> None:
    user = await make_user(db, "suragch@test.mn")
    if plan_days is not None:
        user.plan_expires_at = datetime.now(UTC) + timedelta(days=plan_days)
        await db.commit()
    await login_as(client, api, "suragch@test.mn")


def _locked_flags(course_json: dict) -> list[bool]:
    return [lesson["locked"] for module in course_json["modules"] for lesson in module["lessons"]]


async def test_course_outline_marks_lessons_after_the_free_ones(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    await _paid_course(db)
    await _student(client, api, db)

    body = (await client.get(f"{api}/courses/tolbort")).json()
    assert body["is_free"] is False
    assert body["free_lessons"] == 2
    assert _locked_flags(body) == [False, False, True, True]


async def test_anonymous_visitors_see_the_same_locks(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    await _paid_course(db)
    body = (await client.get(f"{api}/courses/tolbort")).json()
    assert _locked_flags(body) == [False, False, True, True]


async def test_free_course_has_no_locks(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    await make_course_with_lessons(db, slug="unegui", lesson_count=3)
    await _student(client, api, db)
    body = (await client.get(f"{api}/courses/unegui")).json()
    assert _locked_flags(body) == [False, False, False]


async def test_player_strips_locked_lesson_but_keeps_navigation(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    await _paid_course(db)
    await _student(client, api, db)

    body = (await client.get(f"{api}/courses/tolbort/lessons/hicheel-3")).json()
    lesson = body["lesson"]
    assert lesson["locked"] is True
    assert lesson["title"] == "Хичээл 3"
    assert lesson["content"] == ""
    assert lesson["initial_code"] == ""
    assert lesson["exercise"] is None
    assert lesson["video_url"] is None
    assert body["previous_lesson"]["slug"] == "hicheel-2"
    assert body["next_lesson"]["slug"] == "hicheel-4"
    assert _locked_flags(body) == [False, False, True, True]


async def test_player_serves_free_lessons_in_full(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    await _paid_course(db)
    await _student(client, api, db)

    lesson = (await client.get(f"{api}/courses/tolbort/lessons/hicheel-2")).json()["lesson"]
    assert lesson["locked"] is False
    assert lesson["content"] == "## Агуулга"


async def test_locked_lesson_endpoints_require_a_plan(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    course, lessons = await _paid_course(db)
    await _student(client, api, db)
    await client.post(f"{api}/courses/{course.id}/enroll")
    locked = lessons[2]

    for response in (
        await client.get(f"{api}/lessons/{locked.id}"),
        await client.get(f"{api}/lessons/{locked.id}/help"),
        await client.post(f"{api}/lessons/{locked.id}/complete"),
    ):
        assert response.status_code == 402
        assert response.json()["detail"]["code"] == "PLAN_REQUIRED"

    # Үнэгүй хичээлийг дуусгаж болно.
    assert (await client.post(f"{api}/lessons/{lessons[0].id}/complete")).status_code == 200


async def test_active_plan_unlocks_everything(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    course, lessons = await _paid_course(db)
    await _student(client, api, db, plan_days=10)
    await client.post(f"{api}/courses/{course.id}/enroll")

    body = (await client.get(f"{api}/courses/tolbort")).json()
    assert _locked_flags(body) == [False, False, False, False]
    lesson = (await client.get(f"{api}/courses/tolbort/lessons/hicheel-4")).json()["lesson"]
    assert lesson["locked"] is False
    assert lesson["content"] == "## Агуулга"
    assert (await client.post(f"{api}/lessons/{lessons[3].id}/complete")).status_code == 200


async def test_expired_plan_locks_again(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    await _paid_course(db)
    await _student(client, api, db, plan_days=-1)
    body = (await client.get(f"{api}/courses/tolbort")).json()
    assert _locked_flags(body) == [False, False, True, True]


async def test_admin_is_never_locked_out(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    _, lessons = await _paid_course(db)
    await make_user(db, "admin@test.mn", role=UserRole.ADMIN)
    await login_as(client, api, "admin@test.mn")
    assert (await client.get(f"{api}/lessons/{lessons[3].id}")).status_code == 200


async def test_unpublished_lessons_do_not_shift_the_free_range(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    """Админ ноорог нэмэхэд сурагчийн харах үнэгүй хэсэг өөрчлөгдөхгүй."""
    course, _ = await _paid_course(db, lesson_count=3, free_lessons=2)
    module = await make_module(db, course.id, title="Эхний модул", position=-1)
    await make_lesson(db, module.id, slug="noorog", published=False)
    await _student(client, api, db)

    body = (await client.get(f"{api}/courses/tolbort")).json()
    assert _locked_flags(body) == [False, False, True]
