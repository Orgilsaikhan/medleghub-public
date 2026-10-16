import httpx

from app.models.enums import UserRole
from tests.conftest import login_as, make_user
from tests.factories import make_course, make_course_with_lessons, make_lesson, make_module


async def test_catalog_hides_unpublished_courses(client: httpx.AsyncClient, api: str, db) -> None:
    await make_course(db, slug="il-garsan", title="Нийтлэгдсэн", published=True)
    await make_course(db, slug="nuuts", title="Нуугдсан", published=False)

    body = (await client.get(f"{api}/courses")).json()
    slugs = [item["slug"] for item in body["items"]]
    assert slugs == ["il-garsan"]
    assert body["total"] == 1


async def test_catalog_search_and_filters(client: httpx.AsyncClient, api: str, db) -> None:
    await make_course(db, slug="js", title="JavaScript үндэс", category="javascript")
    await make_course(db, slug="py", title="Python үндэс", category="python")
    await make_course(
        db, slug="react", title="React гүнзгий", category="react", difficulty="advanced"
    )

    assert [
        item["slug"] for item in (await client.get(f"{api}/courses?q=Python")).json()["items"]
    ] == ["py"]
    assert [
        item["slug"] for item in (await client.get(f"{api}/courses?category=react")).json()["items"]
    ] == ["react"]
    assert [
        item["slug"]
        for item in (await client.get(f"{api}/courses?difficulty=advanced")).json()["items"]
    ] == ["react"]


async def test_catalog_paginates(client: httpx.AsyncClient, api: str, db) -> None:
    for index in range(5):
        await make_course(db, slug=f"surgalt-{index}", title=f"Сургалт {index}")

    body = (await client.get(f"{api}/courses?page=1&page_size=2")).json()
    assert len(body["items"]) == 2
    assert body["total"] == 5
    assert body["total_pages"] == 3


async def test_course_detail_returns_curriculum(client: httpx.AsyncClient, api: str, db) -> None:
    course, _ = await make_course_with_lessons(db, slug="js-undes", lesson_count=2)

    body = (await client.get(f"{api}/courses/{course.slug}")).json()
    assert body["lesson_count"] == 2
    assert body["duration"] == 240
    assert len(body["modules"]) == 1
    assert [lesson["slug"] for lesson in body["modules"][0]["lessons"]] == [
        "hicheel-1",
        "hicheel-2",
    ]
    assert body["enrolled"] is False
    assert body["progress"] is None


async def test_course_detail_hides_unpublished_lessons(
    client: httpx.AsyncClient, api: str, db
) -> None:
    course = await make_course(db, slug="hagas")
    module = await make_module(db, course.id)
    await make_lesson(db, module.id, slug="il", published=True)
    await make_lesson(db, module.id, slug="nuuts", published=False, position=1)

    body = (await client.get(f"{api}/courses/{course.slug}")).json()
    assert [lesson["slug"] for lesson in body["modules"][0]["lessons"]] == ["il"]
    assert body["lesson_count"] == 1


async def test_unknown_course_returns_mongolian_error(client: httpx.AsyncClient, api: str) -> None:
    response = await client.get(f"{api}/courses/baihgui-surgalt")
    assert response.status_code == 404
    detail = response.json()["detail"]
    assert detail["code"] == "COURSE_NOT_FOUND"
    assert detail["message"] == "Сургалт олдсонгүй."


async def test_course_create_requires_admin(client: httpx.AsyncClient, api: str, db) -> None:
    await make_user(db, "suragch@test.mn")
    await login_as(client, api, "suragch@test.mn")

    response = await client.post(f"{api}/courses", json={"title": "Шинэ", "slug": "shine-surgalt"})
    assert response.status_code == 403
    assert response.json()["detail"]["code"] == "FORBIDDEN"


async def test_anonymous_cannot_create_course(client: httpx.AsyncClient, api: str) -> None:
    response = await client.post(f"{api}/courses", json={"title": "Шинэ", "slug": "shine"})
    assert response.status_code == 401


async def test_admin_course_lifecycle(client: httpx.AsyncClient, api: str, db) -> None:
    await make_user(db, "admin@test.mn", role=UserRole.ADMIN)
    await login_as(client, api, "admin@test.mn")

    created = await client.post(
        f"{api}/courses",
        json={
            "title": "Шинэ сургалт",
            "slug": "shine-surgalt",
            "description": "Тайлбар",
            "category": "javascript",
            "difficulty": "beginner",
        },
    )
    assert created.status_code == 201, created.text
    course_id = created.json()["id"]
    assert created.json()["published"] is False

    # Нийтлэгдээгүй тул нийтэд харагдахгүй.
    await client.post(f"{api}/auth/logout")
    assert (await client.get(f"{api}/courses")).json()["total"] == 0

    await login_as(client, api, "admin@test.mn")
    published = await client.patch(f"{api}/courses/{course_id}", json={"published": True})
    assert published.status_code == 200
    assert published.json()["published"] is True

    await client.post(f"{api}/auth/logout")
    assert (await client.get(f"{api}/courses")).json()["total"] == 1

    await login_as(client, api, "admin@test.mn")
    deleted = await client.delete(f"{api}/courses/{course_id}")
    assert deleted.status_code == 200
    assert (await client.get(f"{api}/courses/shine-surgalt")).status_code == 404


async def test_duplicate_slug_rejected(client: httpx.AsyncClient, api: str, db) -> None:
    await make_user(db, "admin@test.mn", role=UserRole.ADMIN)
    await login_as(client, api, "admin@test.mn")
    payload = {"title": "Сургалт", "slug": "davhar-slug"}

    assert (await client.post(f"{api}/courses", json=payload)).status_code == 201
    response = await client.post(f"{api}/courses", json=payload)
    assert response.status_code == 409
    assert response.json()["detail"]["code"] == "SLUG_TAKEN"


async def test_invalid_slug_rejected(client: httpx.AsyncClient, api: str, db) -> None:
    await make_user(db, "admin@test.mn", role=UserRole.ADMIN)
    await login_as(client, api, "admin@test.mn")

    response = await client.post(f"{api}/courses", json={"title": "Сургалт", "slug": "Буруу Slug!"})
    assert response.status_code == 422
