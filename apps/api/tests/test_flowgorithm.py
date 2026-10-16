"""Шинэ ангилал, plaintext хэл, суралцах урсгал ба seed-ийн нийцэл."""

import json

import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from app.content.flowgorithm import FLOWGORITHM_COURSE
from app.seed import _sync_course
from tests.conftest import login_as, make_user


async def test_flowgorithm_catalog_learning_and_reseed(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    spec = FLOWGORITHM_COURSE
    await _sync_course(db, spec)
    await db.commit()

    catalog = await client.get(f"{api}/courses", params={"category": "flowgorithm"})
    assert catalog.status_code == 200, catalog.text
    items = catalog.json()["items"]
    assert len(items) == 1
    assert items[0]["slug"] == spec.slug
    assert items[0]["lesson_count"] == 24
    assert items[0]["is_free"] is True

    await make_user(db, "flowgorithm@test.mn")
    await login_as(client, api, "flowgorithm@test.mn")
    enrolled = await client.post(f"{api}/courses/{items[0]['id']}/enroll")
    assert enrolled.status_code == 201, enrolled.text

    # Модуль хооронд шилжих болон шинэ хэл API-аар дамжихыг шалгана.
    last_in_intro = spec.modules[0].lessons[-1]
    lesson_url = f"{api}/courses/{spec.slug}/lessons/{last_in_intro.slug}"
    response = await client.get(lesson_url)
    assert response.status_code == 200, response.text
    player = response.json()
    assert len(player["modules"]) == 8
    assert player["lesson"]["language"] == "plaintext"
    assert player["lesson"]["content"] == last_in_intro.content
    assert player["lesson"]["initial_code"] == last_in_intro.initial_code
    # Даалгавар ирнэ, жишиг шийдэл, зөвлөгөө ирэхгүй — «Тусламж»-аар тусад нь авна.
    exercise = player["lesson"]["exercise"]
    assert exercise["statement"] and exercise["tests"]
    assert "solution" not in exercise and "tips" not in exercise
    assert player["next_lesson"]["slug"] == spec.modules[1].lessons[0].slug
    assert player["previous_lesson"]["slug"] == spec.modules[0].lessons[1].slug
    lesson_id = player["lesson"]["id"]
    help_response = await client.get(f"{api}/lessons/{lesson_id}/help")
    assert help_response.status_code == 200, help_response.text
    solution = json.loads(help_response.json()["solution"])
    assert solution["format"] == "medleghub-flowgorithm" and solution["nodes"]
    completed = await client.post(f"{api}/lessons/{lesson_id}/complete")
    assert completed.status_code == 200, completed.text

    await _sync_course(db, spec)
    await db.commit()
    refreshed = (await client.get(lesson_url)).json()
    assert refreshed["lesson"]["id"] == lesson_id
    assert refreshed["lesson"]["completed"] is True
    assert refreshed["enrolled"] is True
    assert refreshed["progress"]["completed_lessons"] == 1
    assert refreshed["progress"]["total_lessons"] == 24

    final_slug = spec.modules[-1].lessons[-1].slug
    final = (await client.get(f"{api}/courses/{spec.slug}/lessons/{final_slug}")).json()
    assert final["next_lesson"] is None
