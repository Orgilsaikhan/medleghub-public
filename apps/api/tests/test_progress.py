import httpx

from app.models.enums import UserRole
from tests.conftest import login_as, make_user
from tests.factories import make_course, make_course_with_lessons, make_module
from tests.factories import make_lesson as build_lesson


async def test_enroll_is_idempotent(client: httpx.AsyncClient, api: str, db) -> None:
    course, _ = await make_course_with_lessons(db)
    await make_user(db, "suragch@test.mn")
    await login_as(client, api, "suragch@test.mn")

    first = await client.post(f"{api}/courses/{course.id}/enroll")
    assert first.status_code == 201
    assert first.json()["already_enrolled"] is False

    second = await client.post(f"{api}/courses/{course.id}/enroll")
    assert second.status_code == 201
    assert second.json()["already_enrolled"] is True


async def test_enroll_requires_login(client: httpx.AsyncClient, api: str, db) -> None:
    course = await make_course(db)
    assert (await client.post(f"{api}/courses/{course.id}/enroll")).status_code == 401


async def test_paid_course_can_be_enrolled_without_plan(
    client: httpx.AsyncClient, api: str, db
) -> None:
    """Төлбөрт сургалтын эхний хичээлүүд үнэгүй тул бүртгэл нээлттэй."""
    course = await make_course(db, slug="premium", is_free=False, free_lessons=2)
    await make_user(db, "suragch@test.mn")
    await login_as(client, api, "suragch@test.mn")

    response = await client.post(f"{api}/courses/{course.id}/enroll")
    assert response.status_code == 201


async def test_complete_requires_enrollment(client: httpx.AsyncClient, api: str, db) -> None:
    _, lessons = await make_course_with_lessons(db)
    await make_user(db, "suragch@test.mn")
    await login_as(client, api, "suragch@test.mn")

    response = await client.post(f"{api}/lessons/{lessons[0].id}/complete")
    assert response.status_code == 403
    assert response.json()["detail"]["code"] == "NOT_ENROLLED"


async def test_complete_updates_progress_and_is_idempotent(
    client: httpx.AsyncClient, api: str, db
) -> None:
    course, lessons = await make_course_with_lessons(db, lesson_count=4)
    await make_user(db, "suragch@test.mn")
    await login_as(client, api, "suragch@test.mn")
    await client.post(f"{api}/courses/{course.id}/enroll")

    first = await client.post(f"{api}/lessons/{lessons[0].id}/complete")
    assert first.status_code == 200
    assert first.json()["course_progress"] == {
        "completed_lessons": 1,
        "total_lessons": 4,
        "percent": 25,
    }

    repeat = await client.post(f"{api}/lessons/{lessons[0].id}/complete")
    assert repeat.json()["course_progress"]["completed_lessons"] == 1
    assert repeat.json()["completed_at"] == first.json()["completed_at"]

    await client.post(f"{api}/lessons/{lessons[1].id}/complete")
    progress = (await client.get(f"{api}/courses/{course.id}/progress")).json()
    assert progress == {"completed_lessons": 2, "total_lessons": 4, "percent": 50}


async def test_progress_survives_logout(client: httpx.AsyncClient, api: str, db) -> None:
    """Ахиц сервер дээр хадгалагдана — дахин нэвтрэхэд хэвээр байна."""
    course, lessons = await make_course_with_lessons(db, lesson_count=2)
    await make_user(db, "suragch@test.mn")
    await login_as(client, api, "suragch@test.mn")
    await client.post(f"{api}/courses/{course.id}/enroll")
    await client.post(f"{api}/lessons/{lessons[0].id}/complete")

    await client.post(f"{api}/auth/logout")
    await login_as(client, api, "suragch@test.mn")

    detail = (await client.get(f"{api}/courses/{course.slug}")).json()
    assert detail["enrolled"] is True
    assert detail["progress"]["percent"] == 50
    assert detail["modules"][0]["lessons"][0]["completed"] is True
    assert detail["modules"][0]["lessons"][1]["completed"] is False


async def test_my_courses_returns_continue_lesson(client: httpx.AsyncClient, api: str, db) -> None:
    course, lessons = await make_course_with_lessons(db, lesson_count=3)
    await make_user(db, "suragch@test.mn")
    await login_as(client, api, "suragch@test.mn")
    await client.post(f"{api}/courses/{course.id}/enroll")
    await client.post(f"{api}/lessons/{lessons[0].id}/complete")

    body = (await client.get(f"{api}/me/courses")).json()
    assert len(body) == 1
    assert body[0]["course"]["slug"] == course.slug
    assert body[0]["progress"]["percent"] == 33
    assert body[0]["continue_lesson"]["slug"] == lessons[1].slug
    assert body[0]["continue_lesson"]["course_slug"] == course.slug


async def test_my_courses_empty_for_new_user(client: httpx.AsyncClient, api: str, db) -> None:
    await make_user(db, "shine@test.mn")
    await login_as(client, api, "shine@test.mn")
    assert (await client.get(f"{api}/me/courses")).json() == []


async def test_unpublished_lesson_not_completable(client: httpx.AsyncClient, api: str, db) -> None:
    course = await make_course(db, slug="hagas-belen")
    module = await make_module(db, course.id)
    hidden = await build_lesson(db, module.id, slug="nuuts", published=False)
    await make_user(db, "suragch@test.mn")
    await login_as(client, api, "suragch@test.mn")
    await client.post(f"{api}/courses/{course.id}/enroll")

    response = await client.post(f"{api}/lessons/{hidden.id}/complete")
    assert response.status_code == 404
    assert response.json()["detail"]["code"] == "LESSON_NOT_FOUND"


async def test_admin_sees_unpublished_course(client: httpx.AsyncClient, api: str, db) -> None:
    await make_course(db, slug="nooluur", published=False)
    await make_user(db, "admin@test.mn", role=UserRole.ADMIN)
    await login_as(client, api, "admin@test.mn")

    assert (await client.get(f"{api}/courses")).json()["total"] == 1
