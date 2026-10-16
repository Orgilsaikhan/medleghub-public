import httpx

from app.content import COURSES
from app.models.enums import UserRole
from tests.conftest import login_as, make_user
from tests.factories import make_course, make_course_with_lessons, make_lesson, make_module


async def test_lesson_player_returns_everything_in_one_call(
    client: httpx.AsyncClient, api: str, db
) -> None:
    course, lessons = await make_course_with_lessons(db, slug="js-undes", lesson_count=3)
    await make_user(db, "suragch@test.mn")
    await login_as(client, api, "suragch@test.mn")
    await client.post(f"{api}/courses/{course.id}/enroll")
    await client.post(f"{api}/lessons/{lessons[0].id}/complete")

    response = await client.get(f"{api}/courses/{course.slug}/lessons/{lessons[1].slug}")
    assert response.status_code == 200
    body = response.json()

    assert body["course"]["slug"] == course.slug
    assert body["lesson"]["slug"] == lessons[1].slug
    assert body["lesson"]["initial_code"]
    assert body["lesson"]["completed"] is False
    assert body["enrolled"] is True
    assert body["progress"] == {"completed_lessons": 1, "total_lessons": 3, "percent": 33}
    assert body["previous_lesson"]["slug"] == lessons[0].slug
    assert body["next_lesson"]["slug"] == lessons[2].slug
    assert body["modules"][0]["lessons"][0]["completed"] is True


async def test_lesson_player_returns_the_challenging_tag(
    client: httpx.AsyncClient, api: str, db
) -> None:
    """Хэцүү хичээл «Заавар» хэсэгт шар «Хэцүү» шошготой — бусад нь үгүй."""
    course, lessons = await make_course_with_lessons(db, slug="c-undes", lesson_count=2)
    lessons[1].challenging = True
    await db.commit()
    await make_user(db, "suragch@test.mn")
    await login_as(client, api, "suragch@test.mn")

    for lesson, expected in ((lessons[0], False), (lessons[1], True)):
        body = (await client.get(f"{api}/courses/{course.slug}/lessons/{lesson.slug}")).json()
        assert body["lesson"]["challenging"] is expected
        assert (await client.get(f"{api}/lessons/{lesson.id}")).json()["challenging"] is expected


def test_seeded_challenging_lessons() -> None:
    """Эзэмшигчийн сонгосон хэцүү хичээлүүд агуулгад тэмдэглэгдсэн."""
    challenging = {
        lesson.slug
        for course in COURSES
        for module in course.modules
        for lesson in module.lessons
        if lesson.challenging
    }
    assert "c-arifmetik-ba-onooh" in challenging


async def test_lesson_player_returns_the_exercise(client: httpx.AsyncClient, api: str, db) -> None:
    course, lessons = await make_course_with_lessons(db, slug="c-undes", lesson_count=2)
    lessons[0].exercise = {
        "statement": "Хоёр тоог нэм.",
        "tests": [{"stdin": "1 2\n", "expected_output": "3\n", "sample": True}],
        "tips": "- Нэм.",
        "solution": "int main(void) { return 0; }",
    }
    await db.commit()
    await make_user(db, "suragch@test.mn")
    await login_as(client, api, "suragch@test.mn")

    body = (await client.get(f"{api}/courses/{course.slug}/lessons/{lessons[0].slug}")).json()
    # Зөвлөгөө, шийдэл хичээлийн хариунд ОРОХГҮЙ — зөвхөн «Тусламж»-аар.
    assert body["lesson"]["exercise"] == {
        "statement": "Хоёр тоог нэм.",
        "tests": [{"stdin": "1 2\n", "expected_output": "3\n", "sample": True}],
        "kind": "tests",
    }
    assert (await client.get(f"{api}/lessons/{lessons[0].id}")).json()["exercise"] == body[
        "lesson"
    ]["exercise"]

    # Дасгалгүй хичээл урьдын адил «Хичээл дууссан» товчтой.
    other = (await client.get(f"{api}/courses/{course.slug}/lessons/{lessons[1].slug}")).json()
    assert other["lesson"]["exercise"] is None


async def test_lesson_player_returns_react_dom_tests(
    client: httpx.AsyncClient, api: str, db
) -> None:
    """React хичээлийн тест нь stdin биш `name`/`code`-той — хоёулаа дамжина."""
    course, lessons = await make_course_with_lessons(db, slug="react-undes", lesson_count=1)
    lessons[0].language = "jsx"
    lessons[0].exercise = {
        "statement": "Тоологч бич.",
        "tests": [{"name": "0-ээс эхэлнэ", "code": "render(<App />);", "sample": True}],
        "tips": "- useState.",
        "solution": "// @file App.jsx\nexport default function App() {}",
    }
    await db.commit()
    await make_user(db, "suragch@test.mn")
    await login_as(client, api, "suragch@test.mn")

    body = (await client.get(f"{api}/courses/{course.slug}/lessons/{lessons[0].slug}")).json()
    assert body["lesson"]["language"] == "jsx"
    assert body["lesson"]["exercise"] == {
        "statement": "Тоологч бич.",
        "tests": [{"name": "0-ээс эхэлнэ", "code": "render(<App />);", "sample": True}],
        "kind": "tests",
    }


async def test_lesson_help_returns_tips_and_solution(
    client: httpx.AsyncClient, api: str, db
) -> None:
    course, lessons = await make_course_with_lessons(db, slug="c-undes", lesson_count=2)
    lessons[0].exercise = {
        "statement": "Хоёр тоог нэм.",
        "tests": [{"stdin": "1 2\n", "expected_output": "3\n", "sample": True}],
        "tips": "- Нэм.",
        "solution": "int main(void) { return 0; }",
    }
    await db.commit()

    # Нэвтрээгүй бол хариу харагдахгүй.
    assert (await client.get(f"{api}/lessons/{lessons[0].id}/help")).status_code == 401

    await make_user(db, "suragch@test.mn")
    await login_as(client, api, "suragch@test.mn")

    # Бүртгүүлээгүй ч хичээлийг үзэж болдог тул тусламж ч авна.
    response = await client.get(f"{api}/lessons/{lessons[0].id}/help")
    assert response.status_code == 200
    assert response.json() == {"tips": "- Нэм.", "solution": "int main(void) { return 0; }"}

    # Дасгалгүй хичээлд тусламж байхгүй.
    missing = await client.get(f"{api}/lessons/{lessons[1].id}/help")
    assert missing.status_code == 404
    assert missing.json()["detail"]["code"] == "HELP_NOT_FOUND"


async def test_lesson_help_hides_unpublished_lessons(
    client: httpx.AsyncClient, api: str, db
) -> None:
    course = await make_course(db, slug="c-undes")
    module = await make_module(db, course.id)
    lesson = await make_lesson(db, module.id, published=False)
    lesson.exercise = {"statement": "", "tests": [], "tips": "", "solution": "int main(){}"}
    await db.commit()
    await make_user(db, "suragch@test.mn")
    await login_as(client, api, "suragch@test.mn")

    assert (await client.get(f"{api}/lessons/{lesson.id}/help")).status_code == 404


async def test_lesson_player_edges_have_no_neighbours(
    client: httpx.AsyncClient, api: str, db
) -> None:
    course, lessons = await make_course_with_lessons(db, lesson_count=2)
    await make_user(db, "suragch@test.mn")
    await login_as(client, api, "suragch@test.mn")

    first = (await client.get(f"{api}/courses/{course.slug}/lessons/{lessons[0].slug}")).json()
    assert first["previous_lesson"] is None
    assert first["next_lesson"]["slug"] == lessons[1].slug

    last = (await client.get(f"{api}/courses/{course.slug}/lessons/{lessons[1].slug}")).json()
    assert last["previous_lesson"]["slug"] == lessons[0].slug
    assert last["next_lesson"] is None


async def test_lesson_player_requires_login(client: httpx.AsyncClient, api: str, db) -> None:
    course, lessons = await make_course_with_lessons(db)
    response = await client.get(f"{api}/courses/{course.slug}/lessons/{lessons[0].slug}")
    assert response.status_code == 401


async def test_lesson_player_skips_unpublished_lessons(
    client: httpx.AsyncClient, api: str, db
) -> None:
    course = await make_course(db, slug="hagas")
    module = await make_module(db, course.id)
    first = await make_lesson(db, module.id, slug="negdugeer", position=0)
    await make_lesson(db, module.id, slug="nuuts", published=False, position=1)
    third = await make_lesson(db, module.id, slug="guravdugaar", position=2)

    await make_user(db, "suragch@test.mn")
    await login_as(client, api, "suragch@test.mn")

    body = (await client.get(f"{api}/courses/{course.slug}/lessons/{first.slug}")).json()
    assert body["next_lesson"]["slug"] == third.slug
    assert body["progress"]["total_lessons"] == 2


async def test_admin_lesson_crud(client: httpx.AsyncClient, api: str, db) -> None:
    course = await make_course(db, slug="admin-surgalt")
    module = await make_module(db, course.id)
    await make_user(db, "admin@test.mn", role=UserRole.ADMIN)
    await login_as(client, api, "admin@test.mn")

    created = await client.post(
        f"{api}/modules/{module.id}/lessons",
        json={
            "title": "Хувьсагч",
            "slug": "huvisagch",
            "content": "## Хувьсагч",
            "initial_code": "const a = 1;",
            "duration": 300,
        },
    )
    assert created.status_code == 201, created.text
    lesson_id = created.json()["id"]
    assert created.json()["published"] is False

    updated = await client.patch(
        f"{api}/lessons/{lesson_id}", json={"title": "Хувьсагч (Variable)", "published": True}
    )
    assert updated.status_code == 200
    assert updated.json()["title"] == "Хувьсагч (Variable)"
    assert updated.json()["published"] is True

    fetched = await client.get(f"{api}/lessons/{lesson_id}")
    assert fetched.json()["initial_code"] == "const a = 1;"

    assert (await client.delete(f"{api}/lessons/{lesson_id}")).status_code == 200
    assert (await client.get(f"{api}/lessons/{lesson_id}")).status_code == 404


async def test_lesson_slug_unique_within_course(client: httpx.AsyncClient, api: str, db) -> None:
    """Route `/learn/:courseSlug/:lessonSlug` тодорхой байхын тулд шаардлагатай."""
    course = await make_course(db, slug="davhardal")
    module_a = await make_module(db, course.id, title="А", position=0)
    module_b = await make_module(db, course.id, title="Б", position=1)
    await make_user(db, "admin@test.mn", role=UserRole.ADMIN)
    await login_as(client, api, "admin@test.mn")

    payload = {"title": "Хичээл", "slug": "ijil-slug"}
    assert (
        await client.post(f"{api}/modules/{module_a.id}/lessons", json=payload)
    ).status_code == 201

    response = await client.post(f"{api}/modules/{module_b.id}/lessons", json=payload)
    assert response.status_code == 409
    assert response.json()["detail"]["code"] == "LESSON_SLUG_TAKEN"


async def test_lesson_create_requires_admin(client: httpx.AsyncClient, api: str, db) -> None:
    course = await make_course(db, slug="hamgaalalt")
    module = await make_module(db, course.id)
    await make_user(db, "suragch@test.mn")
    await login_as(client, api, "suragch@test.mn")

    response = await client.post(
        f"{api}/modules/{module.id}/lessons", json={"title": "Хичээл", "slug": "hicheel"}
    )
    assert response.status_code == 403


async def test_module_crud_and_reorder(client: httpx.AsyncClient, api: str, db) -> None:
    course = await make_course(db, slug="modul-tuslah")
    await make_user(db, "admin@test.mn", role=UserRole.ADMIN)
    await login_as(client, api, "admin@test.mn")

    first = await client.post(f"{api}/courses/{course.id}/modules", json={"title": "Модул 1"})
    second = await client.post(f"{api}/courses/{course.id}/modules", json={"title": "Модул 2"})
    assert first.status_code == 201
    assert first.json()["position"] == 0
    assert second.json()["position"] == 1

    moved = await client.patch(f"{api}/modules/{second.json()['id']}", json={"position": 0})
    assert moved.json()["position"] == 0

    assert (await client.delete(f"{api}/modules/{first.json()['id']}")).status_code == 200
    detail = (await client.get(f"{api}/admin/courses/{course.id}")).json()
    assert [module["title"] for module in detail["modules"]] == ["Модул 2"]


async def test_deleting_course_removes_lessons(client: httpx.AsyncClient, api: str, db) -> None:
    course, lessons = await make_course_with_lessons(db, slug="ustgah")
    await make_user(db, "admin@test.mn", role=UserRole.ADMIN)
    await login_as(client, api, "admin@test.mn")

    assert (await client.delete(f"{api}/courses/{course.id}")).status_code == 200
    assert (await client.get(f"{api}/lessons/{lessons[0].id}")).status_code == 404
