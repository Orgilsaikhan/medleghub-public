"""Сургалтын суралцагчид ба нийтийн профайл."""

import uuid
from datetime import UTC, datetime

import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.course import Course
from app.models.enrollment import Enrollment
from app.models.enums import UserRole
from app.models.lesson import Lesson
from app.models.progress import LessonProgress
from app.models.user import User
from tests.conftest import login_as, make_user
from tests.factories import make_course, make_course_with_lessons

VIEWER = "uzegch@test.mn"


async def student(db: AsyncSession, email: str, name: str, role: str = UserRole.STUDENT) -> User:
    user = await make_user(db, email, role=role)
    user.name = name
    await db.commit()
    return user


async def enroll(db: AsyncSession, user: User, course: Course, *done: Lesson) -> None:
    db.add(Enrollment(user_id=user.id, course_id=course.id))
    for lesson in done:
        db.add(
            LessonProgress(
                user_id=user.id, lesson_id=lesson.id, completed=True, completed_at=datetime.now(UTC)
            )
        )
    await db.commit()


# --- Сургалтын суралцагчид -------------------------------------------------------


async def test_students_require_login(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    await make_course(db, slug="js")
    assert (await client.get(f"{api}/courses/js/students")).status_code == 401


async def test_students_sorted_by_progress_without_admins(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    course, lessons = await make_course_with_lessons(db, slug="js", lesson_count=4)
    slow = await student(db, "a@test.mn", "Бат")
    fast = await student(db, "b@test.mn", "Сараа")
    admin = await student(db, "admin@test.mn", "Админ", role=UserRole.ADMIN)
    await enroll(db, slow, course, lessons[0])
    await enroll(db, fast, course, *lessons[:3])
    await enroll(db, admin, course, *lessons)
    await make_user(db, VIEWER)
    await login_as(client, api, VIEWER)

    response = await client.get(f"{api}/courses/js/students")

    assert response.status_code == 200, response.text
    body = response.json()
    assert body["total"] == 2
    assert [(item["name"], item["percent"]) for item in body["items"]] == [
        ("Сараа", 75),
        ("Бат", 25),
    ]
    # Хувийн мэдээлэл ил гарахгүй.
    assert set(body["items"][0]) == {"id", "name", "avatar_key", "percent"}


async def test_students_limit_keeps_total(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    course, _ = await make_course_with_lessons(db, slug="js", lesson_count=1)
    for index in range(3):
        await enroll(db, await student(db, f"s{index}@test.mn", f"Сурагч {index}"), course)
    await make_user(db, VIEWER)
    await login_as(client, api, VIEWER)

    body = (await client.get(f"{api}/courses/js/students", params={"limit": 2})).json()

    assert body["total"] == 3
    assert len(body["items"]) == 2


async def test_students_of_unpublished_course_are_hidden(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    await make_course(db, slug="draft", published=False)
    await make_user(db, VIEWER)
    await login_as(client, api, VIEWER)

    assert (await client.get(f"{api}/courses/draft/students")).status_code == 404


# --- Нийтийн профайл ----------------------------------------------------------------


async def test_public_profile_hides_private_fields(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    course, lessons = await make_course_with_lessons(db, slug="js", lesson_count=2)
    draft = await make_course(db, slug="draft", published=False)
    classmate = await student(db, "naiz@test.mn", "Номин")
    await enroll(db, classmate, course, lessons[0])
    await enroll(db, classmate, draft)
    await make_user(db, VIEWER)
    await login_as(client, api, VIEWER)

    response = await client.get(f"{api}/users/{classmate.id}/profile")

    assert response.status_code == 200, response.text
    profile = response.json()
    assert set(profile["user"]) == {"id", "name", "avatar_key", "created_at"}
    assert profile["user"]["name"] == "Номин"
    assert profile["stats"]["completed_lessons"] == 1
    # Нийтлэгдээгүй сургалт харагдахгүй.
    assert [(item["slug"], item["progress"]["percent"]) for item in profile["courses"]] == [
        ("js", 50)
    ]


async def test_viewing_a_profile_does_not_award_badges(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    course, lessons = await make_course_with_lessons(db, slug="js", lesson_count=1)
    classmate = await student(db, "naiz@test.mn", "Номин")
    await enroll(db, classmate, course, *lessons)
    await make_user(db, VIEWER)
    await login_as(client, api, VIEWER)

    profile = (await client.get(f"{api}/users/{classmate.id}/profile")).json()

    first_commit = next(badge for badge in profile["badges"] if badge["key"] == "first-commit")
    assert first_commit["earned"] is False


async def test_public_profile_requires_login_and_existing_user(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    classmate = await student(db, "naiz@test.mn", "Номин")
    assert (await client.get(f"{api}/users/{classmate.id}/profile")).status_code == 401

    await make_user(db, VIEWER)
    await login_as(client, api, VIEWER)
    assert (await client.get(f"{api}/users/{uuid.uuid4()}/profile")).status_code == 404
