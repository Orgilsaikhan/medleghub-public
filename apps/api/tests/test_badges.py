"""Тэмдгийн систем — каталог, олгох нөхцөл, профайл."""

import re
from datetime import UTC, datetime, timedelta
from pathlib import Path

import httpx
import pytest
from sqlalchemy import delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.content import COURSES
from app.content.badges import ADVANCED_PROJECT_LESSONS, BADGES, BADGES_BY_KEY, LOCAL_TZ
from app.models.enums import Category
from app.models.lesson import Lesson
from app.models.progress import LessonProgress
from app.models.user import User
from app.services.badge_service import RULES
from tests.conftest import login_as, make_user
from tests.factories import make_course, make_lesson, make_module

EMAIL = "suragch@test.mn"


def by_key(profile: dict) -> dict[str, dict]:
    return {badge["key"]: badge for badge in profile["badges"]}


async def course_with_modules(
    db: AsyncSession, *, slug: str, modules: int, lessons: int = 2, category: str = Category.PYTHON
) -> list[list[Lesson]]:
    """`modules` модуль, модуль бүрт `lessons` хичээл. Хичээлүүдийг модулиар нь буцаана."""
    course = await make_course(db, slug=slug, category=category)
    result = []
    for position in range(modules):
        module = await make_module(db, course.id, title=f"Модул {position}", position=position)
        result.append(
            [
                await make_lesson(db, module.id, slug=f"{slug}-{position}-{index}", position=index)
                for index in range(lessons)
            ]
        )
    return result


async def enroll_and_complete(
    client: httpx.AsyncClient, api: str, course_id, lessons: list[Lesson]
) -> list[dict]:
    await client.post(f"{api}/courses/{course_id}/enroll")
    responses = []
    for lesson in lessons:
        response = await client.post(f"{api}/lessons/{lesson.id}/complete")
        assert response.status_code == 200, response.text
        responses.append(response.json())
    return responses


async def course_id_of(db: AsyncSession, lesson: Lesson):
    await db.refresh(lesson, ["module"])
    return lesson.module.course_id


# --- Каталог ----------------------------------------------------------------------


def test_catalog_keys_are_unique_file_friendly_slugs() -> None:
    keys = [badge.key for badge in BADGES]
    assert len(keys) == len(set(keys)) == 27
    for key in keys:
        # Өгөгдлийн сан болон `public/badges/<key>.svg` файлын нэр.
        assert re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", key), key


def test_icon_manifest_script_knows_every_badge() -> None:
    """Дүрсний бүртгэлийн скрипт файлын нэрийг түлхүүрээр шалгадаг."""
    script = Path(__file__).resolve().parents[2] / "web/scripts/generate-badge-manifest.mjs"
    block = re.search(r"const BADGE_KEYS = \[(.*?)\];", script.read_text(encoding="utf-8"), re.S)
    assert block, "BADGE_KEYS олдсонгүй"
    assert re.findall(r'"([a-z0-9-]+)"', block.group(1)) == [badge.key for badge in BADGES]


def test_rare_badges() -> None:
    rare = {badge.key for badge in BADGES if badge.rare}
    assert rare == {
        "ahead-of-time",
        "hidden-gem",
        "architect",
        "night-owl",
        "early-bird",
        "speed-coder",
        "where-the-answers-hide",
        "through-anothers-path",
    }
    # Солонгон гэрэлтэй тэмдгүүд. Авах хүртэл огт харагдахгүй нь зөвхөн нэг.
    assert {badge.key for badge in BADGES if badge.prismatic} == {
        "where-the-answers-hide",
        "through-anothers-path",
    }
    assert {badge.key for badge in BADGES if badge.invisible} == {"through-anothers-path"}


def test_every_tracked_badge_has_a_rule() -> None:
    tracked = {badge.key for badge in BADGES if badge.tracked}
    assert tracked == set(RULES), "Тооцдог тэмдэг бүр нөхцөлтэй, нөхцөл бүр каталогт байх ёстой"


def test_advanced_projects_exist_in_the_content() -> None:
    slugs = {lesson.slug for course in COURSES for m in course.modules for lesson in m.lessons}
    assert not ADVANCED_PROJECT_LESSONS - slugs, ADVANCED_PROJECT_LESSONS - slugs


# --- Профайл ----------------------------------------------------------------------


async def test_profile_requires_login(client: httpx.AsyncClient, api: str) -> None:
    assert (await client.get(f"{api}/me/profile")).status_code == 401


async def test_new_user_profile(client: httpx.AsyncClient, api: str, db: AsyncSession) -> None:
    await make_user(db, EMAIL)
    await login_as(client, api, EMAIL)

    profile = (await client.get(f"{api}/me/profile")).json()
    badges = by_key(profile)

    assert profile["user"]["email"] == EMAIL
    assert profile["stats"]["completed_lessons"] == 0
    # «Through Another's Path» авах хүртэл огт харагдахгүй.
    assert profile["stats"]["total_badges"] == 26
    assert sum(1 for badge in profile["badges"] if badge["rare"]) == 7
    # Хэрэг огт байхгүй үед (энэ тестийн сан хоосон) SQL-ийн тэмдэг олгогдохгүй.
    assert badges["where-the-answers-hide"]["earned"] is False
    assert badges["where-the-answers-hide"]["progress"] is None
    # 2027 оноос өмнө бүртгүүлсэн бүх хэрэглэгч.
    assert badges["ahead-of-time"]["earned"] is True
    assert badges["ahead-of-time"]["awarded_at"]
    assert profile["stats"]["earned_badges"] == 1

    first = badges["first-commit"]
    assert first["earned"] is False
    assert first["progress"] is None
    assert by_key(profile)["knowledge-seeker"]["progress"] == {"current": 0, "target": 50}

    # Нууц амжилтын нөхцөл авах хүртэл харагдахгүй.
    gem = badges["hidden-gem"]
    assert gem["secret"] is True
    assert gem["description"] == "?"
    assert gem["progress"] is None

    # Өгөгдөл нь бүртгэгддэггүй тэмдэг «Тун удахгүй».
    assert badges["mentor"]["available"] is False
    assert badges["mentor"]["progress"] is None


async def test_ahead_of_time_is_only_for_early_users(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    user = await make_user(db, EMAIL)
    await db.execute(
        update(User)
        .where(User.id == user.id)
        .values(created_at=datetime(2027, 1, 1, tzinfo=LOCAL_TZ) + timedelta(minutes=1))
    )
    await db.commit()
    await login_as(client, api, EMAIL)

    assert (
        by_key((await client.get(f"{api}/me/profile")).json())["ahead-of-time"]["earned"] is False
    )


# --- Хичээл дуусгахад олгох --------------------------------------------------------


async def test_completing_a_lesson_awards_first_commit_once(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    modules = await course_with_modules(db, slug="py", modules=2)
    await make_user(db, EMAIL)
    await login_as(client, api, EMAIL)
    course_id = await course_id_of(db, modules[0][0])

    first, second = await enroll_and_complete(client, api, course_id, modules[0])

    new = {badge["key"] for badge in first["new_badges"]}
    assert "first-commit" in new
    first_commit = next(badge for badge in first["new_badges"] if badge["key"] == "first-commit")
    assert (first_commit["name"], first_commit["prismatic"]) == ("First Commit", False)
    # Дахин олгохгүй. Модуль 1 бүрэн дууссан тул «Hello, World!» шинээр ирнэ.
    assert {badge["key"] for badge in second["new_badges"]} == {"hello-world"}

    again = await client.post(f"{api}/lessons/{modules[0][0].id}/complete")
    assert again.json()["new_badges"] == []


async def test_unstoppable_needs_three_consecutive_modules(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    modules = await course_with_modules(db, slug="py", modules=4, lessons=1)
    await make_user(db, EMAIL)
    await login_as(client, api, EMAIL)
    course_id = await course_id_of(db, modules[0][0])

    # 1, 2, 4-р модуль — дараалаагүй.
    await enroll_and_complete(client, api, course_id, [modules[0][0], modules[1][0], modules[3][0]])
    unstoppable = by_key((await client.get(f"{api}/me/profile")).json())["unstoppable"]
    assert unstoppable["earned"] is False
    assert unstoppable["progress"] == {"current": 2, "target": 3}

    await enroll_and_complete(client, api, course_id, [modules[2][0]])
    assert by_key((await client.get(f"{api}/me/profile")).json())["unstoppable"]["earned"] is True


async def test_compiler_counts_only_programming_courses(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    html = await course_with_modules(db, slug="html", modules=1, category=Category.HTML_CSS)
    python = await course_with_modules(db, slug="py", modules=1, category=Category.PYTHON)
    await make_user(db, EMAIL)
    await login_as(client, api, EMAIL)

    await enroll_and_complete(client, api, await course_id_of(db, html[0][0]), html[0])
    profile = (await client.get(f"{api}/me/profile")).json()
    assert by_key(profile)["compiler"]["earned"] is False
    assert profile["stats"]["completed_courses"] == 1

    await enroll_and_complete(client, api, await course_id_of(db, python[0][0]), python[0])
    assert by_key((await client.get(f"{api}/me/profile")).json())["compiler"]["earned"] is True


async def test_code_smith_counts_exercises(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    modules = await course_with_modules(db, slug="py", modules=1, lessons=3)
    lessons = modules[0]
    for lesson in lessons[:2]:
        lesson.exercise = {"statement": "", "tests": []}
    await db.commit()
    await make_user(db, EMAIL)
    await login_as(client, api, EMAIL)

    await enroll_and_complete(client, api, await course_id_of(db, lessons[0]), lessons)
    profile = (await client.get(f"{api}/me/profile")).json()
    assert profile["stats"]["completed_exercises"] == 2
    assert by_key(profile)["code-smith"]["progress"] == {"current": 2, "target": 10}


@pytest.mark.parametrize(
    ("hour", "badge", "earned"),
    [
        (23, "night-owl", True),
        (2, "night-owl", True),
        (6, "early-bird", True),
        (12, "night-owl", False),
    ],
)
async def test_time_of_day_badges_use_mongolian_time(
    client: httpx.AsyncClient, api: str, db: AsyncSession, hour: int, badge: str, earned: bool
) -> None:
    modules = await course_with_modules(db, slug="py", modules=1, lessons=10)
    user = await make_user(db, EMAIL)
    await login_as(client, api, EMAIL)
    await enroll_and_complete(client, api, await course_id_of(db, modules[0][0]), modules[0])

    # Улаанбаатарын цагаар `hour` цагт дуусгасан гэж тохируулна (UTC-д 8 цаг хасна).
    local = datetime(2026, 9, 27, hour, 30, tzinfo=LOCAL_TZ)
    await db.execute(
        update(LessonProgress)
        .where(LessonProgress.user_id == user.id)
        .values(completed_at=local.astimezone(UTC))
    )
    await db.commit()

    assert by_key((await client.get(f"{api}/me/profile")).json())[badge]["earned"] is earned


async def test_badges_are_never_taken_away(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    modules = await course_with_modules(db, slug="py", modules=1, lessons=1)
    user = await make_user(db, EMAIL)
    await login_as(client, api, EMAIL)
    await enroll_and_complete(client, api, await course_id_of(db, modules[0][0]), modules[0])

    await db.execute(delete(LessonProgress).where(LessonProgress.user_id == user.id))
    await db.commit()

    badges = by_key((await client.get(f"{api}/me/profile")).json())
    assert badges["first-commit"]["earned"] is True
    assert badges["hello-world"]["earned"] is True


async def test_unpublished_lessons_do_not_count(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    course = await make_course(db, slug="py", category=Category.PYTHON)
    module = await make_module(db, course.id)
    hidden = await make_lesson(db, module.id, slug="nuuts", published=False)
    admin = await make_user(db, "admin@test.mn", role="admin")
    await login_as(client, api, admin.email)

    # Админ нийтлэгдээгүй хичээлийг дуусгаж чадна, гэхдээ тэмдэг өгөхгүй.
    response = await client.post(f"{api}/lessons/{hidden.id}/complete")
    assert response.status_code == 200
    # Анхны шалгалтад зөвхөн бүртгүүлсэн огнооны тэмдэг л ирнэ.
    assert {badge["key"] for badge in response.json()["new_badges"]} == {"ahead-of-time"}


async def test_persistent_needs_seven_consecutive_days(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    modules = await course_with_modules(db, slug="py", modules=1, lessons=8)
    user = await make_user(db, EMAIL)
    await login_as(client, api, EMAIL)
    await enroll_and_complete(client, api, await course_id_of(db, modules[0][0]), modules[0])

    async def spread(days: list[int]) -> dict:
        # Хичээл бүрийг Улаанбаатарын цагаар өөр өдөр дуусгасан гэж тохируулна.
        for lesson, day in zip(modules[0], days, strict=True):
            local = datetime(2026, 9, 1, 12, tzinfo=LOCAL_TZ) + timedelta(days=day)
            await db.execute(
                update(LessonProgress)
                .where(LessonProgress.user_id == user.id, LessonProgress.lesson_id == lesson.id)
                .values(completed_at=local.astimezone(UTC))
            )
        await db.commit()
        return by_key((await client.get(f"{api}/me/profile")).json())["persistent"]

    # 3 өдөр, завсарлаад 4 өдөр — хамгийн урт нь 4.
    broken = await spread([0, 1, 2, 4, 5, 6, 7, 7])
    assert broken["earned"] is False
    assert broken["progress"] == {"current": 4, "target": 7}

    assert (await spread([0, 1, 2, 3, 4, 5, 6, 6]))["earned"] is True


async def test_mastery_and_perfectionist(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    courses = [
        await course_with_modules(db, slug=f"c{index}", modules=1, lessons=1) for index in range(4)
    ]
    await make_user(db, EMAIL)
    await login_as(client, api, EMAIL)
    ids = [await course_id_of(db, course[0][0]) for course in courses]

    # 3 сургалтад бүртгүүлээд 2-ыг нь дуусгана — бүгдийг биш.
    await client.post(f"{api}/courses/{ids[2]}/enroll")
    for course_id, course in zip(ids[:2], courses[:2], strict=True):
        await enroll_and_complete(client, api, course_id, course[0])
    badges = by_key((await client.get(f"{api}/me/profile")).json())
    assert badges["perfectionist"]["earned"] is False
    assert badges["perfectionist"]["progress"] == {"current": 2, "target": 3}
    assert badges["mastery"]["progress"] == {"current": 2, "target": 3}

    await enroll_and_complete(client, api, ids[2], courses[2][0])
    badges = by_key((await client.get(f"{api}/me/profile")).json())
    assert badges["perfectionist"]["earned"] is True
    assert badges["mastery"]["earned"] is True


async def test_hidden_gem_needs_a_lesson_in_every_course(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    first = await course_with_modules(db, slug="a", modules=1, lessons=2)
    second = await course_with_modules(db, slug="b", modules=1, lessons=2)
    await make_course(db, slug="hooson")  # хичээлгүй сургалт тооцогдохгүй
    await make_user(db, EMAIL)
    await login_as(client, api, EMAIL)

    await enroll_and_complete(client, api, await course_id_of(db, first[0][0]), first[0][:1])
    assert by_key((await client.get(f"{api}/me/profile")).json())["hidden-gem"]["earned"] is False

    response = await enroll_and_complete(
        client, api, await course_id_of(db, second[0][0]), second[0][:1]
    )
    assert "hidden-gem" in {badge["key"] for badge in response[0]["new_badges"]}

    gem = by_key((await client.get(f"{api}/me/profile")).json())["hidden-gem"]
    # Авсны дараа жинхэнэ нөхцөл харагдана.
    assert gem["earned"] is True
    assert gem["description"] == "Бүх сургалтад дор хаяж нэг хичээл дуусгах."


CASE = {
    "kind": "answer",
    "statement": "Хэн хулгай хийсэн бэ?",
    "tests": [],
    "tips": "",
    "solution": "SELECT ner FROM irgen WHERE id = 7;",
    "answers": ["Анужин"],
}


async def test_answers_badge_needs_every_published_case(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    modules = await course_with_modules(db, slug="sql", modules=2, lessons=2)
    # Модуль бүрийн сүүлийн хичээл нь хэрэг. Нийтлэгдээгүй хэрэг тооцогдохгүй.
    cases = [modules[0][1], modules[1][1]]
    hidden = await make_lesson(
        db, cases[0].module_id, slug="nuuts-hereg", position=5, published=False
    )
    for lesson in (*cases, hidden):
        lesson.exercise = dict(CASE)
    await db.commit()
    await make_user(db, EMAIL)
    await login_as(client, api, EMAIL)
    course_id = await course_id_of(db, cases[0])

    async def solve(lesson: Lesson) -> list[dict]:
        response = await client.post(f"{api}/lessons/{lesson.id}/answer", json={"answer": "Анужин"})
        assert response.json()["completed"] is True, response.text
        return response.json()["new_badges"]

    async def badge() -> dict:
        return by_key((await client.get(f"{api}/me/profile")).json())["where-the-answers-hide"]

    before = await badge()
    assert (before["earned"], before["rare"], before["prismatic"]) == (False, True, True)
    assert before["progress"] == {"current": 0, "target": 2}
    # Энгийн хичээл хэрэгт тооцогдохгүй.
    await enroll_and_complete(client, api, course_id, modules[0][:1])
    assert (await badge())["progress"] == {"current": 0, "target": 2}

    assert "where-the-answers-hide" not in {b["key"] for b in await solve(cases[0])}
    assert (await badge())["progress"] == {"current": 1, "target": 2}

    unlocked = next(b for b in await solve(cases[1]) if b["key"] == "where-the-answers-hide")
    # Солонгон тэмдгийг UI том цонхонд харуулна — дүрс, тайлбар нь хамт ирнэ.
    assert unlocked == {
        "key": "where-the-answers-hide",
        "name": "Where the Answers Hide",
        "description": BADGES_BY_KEY["where-the-answers-hide"].description,
        "shape": "circle",
        "secret": False,
        "rare": True,
        "prismatic": True,
    }
    after = await badge()
    assert (after["earned"], after["progress"]) == (True, None)


# --- Үйлдлээр олгогдох тэмдэг -------------------------------------------------------


async def test_secret_path_badge_is_claimed_once(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    await make_user(db, EMAIL)
    await login_as(client, api, EMAIL)

    # Авах хүртэл «?» ч үлдээхгүй — жагсаалтад огт байхгүй, тоонд ч орохгүй.
    before = (await client.get(f"{api}/me/profile")).json()
    assert "through-anothers-path" not in by_key(before)
    assert before["stats"]["total_badges"] == 26

    first = await client.post(f"{api}/me/badges/through-anothers-path")
    assert first.status_code == 200, first.text
    unlocked = first.json()["new_badge"]
    assert (unlocked["key"], unlocked["name"]) == (
        "through-anothers-path",
        "Through Another's Path",
    )
    assert unlocked["description"] == ""
    assert (unlocked["earned"], unlocked["prismatic"]) == (True, True)
    assert unlocked["awarded_at"] is not None
    again = await client.post(f"{api}/me/badges/through-anothers-path")
    assert again.json() == {"new_badge": None}

    after_profile = (await client.get(f"{api}/me/profile")).json()
    after = by_key(after_profile)["through-anothers-path"]
    assert after["earned"] is True
    assert after["description"] == ""
    assert after_profile["stats"]["total_badges"] == 27
    assert after_profile["stats"]["earned_badges"] >= 1


async def test_progress_badges_cannot_be_claimed(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    assert (await client.post(f"{api}/me/badges/through-anothers-path")).status_code == 401
    await make_user(db, EMAIL)
    await login_as(client, api, EMAIL)
    for key in ("century", "hidden-gem", "no-such-badge"):
        assert (await client.post(f"{api}/me/badges/{key}")).status_code == 404
