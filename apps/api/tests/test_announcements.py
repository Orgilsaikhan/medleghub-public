"""Админы зарлал (popup): үүсгэх, засах, устгах, хэнд хэзээ харагдах."""

import uuid
from datetime import UTC, datetime, timedelta

import httpx
import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.announcement import Announcement
from app.models.enums import UserRole
from app.models.user import User
from tests.conftest import login_as, make_user

ADMIN = "admin@test.mn"
BODY = {
    "kind": "update",
    "title": "Шинэ React сургалт",
    "body": "**111 хичээл** нэмэгдлээ.",
    "cta_label": "Үзэх",
    "cta_url": "/courses/react-app-buteeh",
    "audience": "everyone",
    "active": True,
}


async def _admin(client: httpx.AsyncClient, api: str, db: AsyncSession) -> User:
    user = await make_user(db, ADMIN, UserRole.ADMIN)
    await login_as(client, api, ADMIN)
    return user


async def _create(client: httpx.AsyncClient, api: str, **fields: object) -> dict:
    response = await client.post(f"{api}/announcements", json={**BODY, **fields})
    assert response.status_code == 201, response.text
    return response.json()


def _add(db: AsyncSession, **fields: object) -> Announcement:
    values = {**BODY, **fields}
    item = Announcement(**values)
    db.add(item)
    return item


async def _current(client: httpx.AsyncClient, api: str) -> list[str]:
    response = await client.get(f"{api}/announcements/current")
    assert response.status_code == 200, response.text
    return [item["title"] for item in response.json()]


def _in(days: float) -> datetime:
    return datetime.now(UTC) + timedelta(days=days)


# --- Админ -------------------------------------------------------------------


async def test_admin_creates_and_lists(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    await _admin(client, api, db)

    created = await _create(client, api, title="  Шинэ React сургалт  ", cta_label=" Үзэх ")

    assert (created["title"], created["cta_label"]) == ("Шинэ React сургалт", "Үзэх")
    assert (created["status"], created["created_by"], created["audience"]) == (
        "live",
        "Тест",
        "everyone",
    )
    listed = (await client.get(f"{api}/announcements")).json()
    assert [item["id"] for item in listed] == [created["id"]]


async def test_new_announcement_is_a_draft_by_default(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    await _admin(client, api, db)
    body = {key: value for key, value in BODY.items() if key != "active"}
    response = await client.post(f"{api}/announcements", json=body)
    assert (response.json()["active"], response.json()["status"]) == (False, "draft")
    assert await _current(client, api) == []


async def test_only_admins_manage_announcements(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    assert (await client.get(f"{api}/announcements")).status_code == 401
    await make_user(db, "suragch@test.mn")
    await login_as(client, api, "suragch@test.mn")
    assert (await client.get(f"{api}/announcements")).status_code == 403
    assert (await client.post(f"{api}/announcements", json=BODY)).status_code == 403
    item = _add(db)
    await db.commit()
    url = f"{api}/announcements/{item.id}"
    assert (await client.patch(url, json={"active": False})).status_code == 403
    assert (await client.delete(url)).status_code == 403


@pytest.mark.parametrize(
    "fields",
    [
        {"cta_url": "javascript:alert(1)"},
        {"cta_url": "//evil.example"},
        {"cta_url": "http://example.com"},
        {"cta_url": "/pricing page"},
        {"cta_url": None},
        {"cta_label": None},
        {"cta_label": "x" * 41},
        {"title": "x"},
        {"body": ""},
        {"body": "x" * 2001},
        {"kind": "news"},
        {"audience": "admins"},
        {"ends_at": "2020-01-01T00:00:00Z"},
        {"starts_at": "2030-01-02T00:00:00Z", "ends_at": "2030-01-01T00:00:00Z"},
    ],
)
async def test_invalid_announcements_are_rejected(
    client: httpx.AsyncClient, api: str, db: AsyncSession, fields: dict
) -> None:
    await _admin(client, api, db)
    response = await client.post(f"{api}/announcements", json={**BODY, **fields})
    assert response.status_code == 422, response.text


async def test_button_is_optional_and_https_links_work(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    await _admin(client, api, db)
    plain = await _create(client, api, cta_label="  ", cta_url="")
    assert (plain["cta_label"], plain["cta_url"]) == (None, None)
    external = await _create(client, api, cta_url="https://www.facebook.com/medleghub")
    assert external["cta_url"] == "https://www.facebook.com/medleghub"


async def test_admin_updates_part_of_an_announcement(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    await _admin(client, api, db)
    created = await _create(client, api)
    url = f"{api}/announcements/{created['id']}"

    body = (await client.patch(url, json={"active": False})).json()
    assert (body["active"], body["status"], body["title"]) == (False, "draft", BODY["title"])

    body = (await client.patch(url, json={"cta_label": None, "cta_url": None})).json()
    assert (body["cta_label"], body["cta_url"]) == (None, None)

    later = _in(3)
    body = (await client.patch(url, json={"active": True, "starts_at": later.isoformat()})).json()
    assert body["status"] == "scheduled"


@pytest.mark.parametrize(
    ("fields", "code"),
    [
        ({"cta_url": None}, "ANNOUNCEMENT_CTA_INCOMPLETE"),
        ({"starts_at": "2031-01-01T00:00:00Z", "ends_at": "2030-01-01T00:00:00Z"}, None),
        ({"ends_at": "2020-01-01T00:00:00Z", "starts_at": "2021-01-01T00:00:00Z"}, None),
    ],
)
async def test_update_keeps_the_announcement_consistent(
    client: httpx.AsyncClient, api: str, db: AsyncSession, fields: dict, code: str | None
) -> None:
    await _admin(client, api, db)
    created = await _create(client, api)
    response = await client.patch(f"{api}/announcements/{created['id']}", json=fields)
    assert response.status_code == 400, response.text
    assert response.json()["detail"]["code"] == (code or "ANNOUNCEMENT_PERIOD_INVALID")
    # Юу ч өөрчлөгдөөгүй.
    listed = (await client.get(f"{api}/announcements")).json()[0]
    assert (listed["cta_url"], listed["starts_at"]) == (BODY["cta_url"], None)


@pytest.mark.parametrize("field", ["title", "body", "kind", "audience", "active"])
async def test_update_rejects_null_required_fields(
    client: httpx.AsyncClient, api: str, db: AsyncSession, field: str
) -> None:
    await _admin(client, api, db)
    created = await _create(client, api)
    response = await client.patch(f"{api}/announcements/{created['id']}", json={field: None})
    assert response.status_code == 422


async def test_admin_deletes_an_announcement(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    await _admin(client, api, db)
    created = await _create(client, api)
    url = f"{api}/announcements/{created['id']}"

    assert (await client.delete(url)).status_code == 204
    assert (await client.delete(url)).status_code == 404
    assert (await client.patch(url, json={"active": True})).status_code == 404
    missing = await client.patch(f"{api}/announcements/{uuid.uuid4()}", json={})
    assert missing.status_code == 404


async def test_deleted_admin_keeps_the_announcement(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    admin = await _admin(client, api, db)
    await _create(client, api)

    await db.delete(admin)
    await db.commit()

    item = (await db.execute(select(Announcement))).scalar_one()
    assert item.created_by is None


# --- Хэнд, хэзээ харагдах ----------------------------------------------------------


async def test_visitors_see_only_announcements_for_everyone(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    for audience in ("everyone", "signed_in", "free", "standard"):
        _add(db, title=audience, audience=audience)
    await db.commit()

    response = await client.get(f"{api}/announcements/current")

    assert [item["title"] for item in response.json()] == ["everyone"]
    # Админы талбар гадагш гарахгүй.
    assert set(response.json()[0]) == {"id", "kind", "title", "body", "cta_label", "cta_url"}


async def test_free_and_standard_users_see_their_own(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    for index, audience in enumerate(("everyone", "signed_in", "free", "standard")):
        _add(
            db,
            title=audience,
            audience=audience,
            starts_at=datetime.now(UTC) - timedelta(hours=10 - index),
        )
    await db.commit()
    await make_user(db, "unegui@test.mn")
    paid = await make_user(db, "standard@test.mn")
    paid.plan_expires_at = _in(30)
    await db.commit()

    await login_as(client, api, "unegui@test.mn")
    # Шинэ нь эхэнд.
    assert await _current(client, api) == ["free", "signed_in", "everyone"]
    await login_as(client, api, "standard@test.mn")
    assert await _current(client, api) == ["standard", "signed_in", "everyone"]


async def test_admins_count_as_standard(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    _add(db, title="free", audience="free")
    _add(db, title="standard", audience="standard")
    await db.commit()
    await _admin(client, api, db)
    assert await _current(client, api) == ["standard"]


async def test_only_live_announcements_are_shown(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    _add(db, title="draft", active=False)
    _add(db, title="scheduled", starts_at=_in(1))
    _add(db, title="ended", starts_at=_in(-10), ends_at=_in(-1))
    _add(db, title="live", starts_at=_in(-1), ends_at=_in(1))
    await db.commit()

    assert await _current(client, api) == ["live"]


async def test_at_most_five_are_sent(client: httpx.AsyncClient, api: str, db: AsyncSession) -> None:
    for index in range(7):
        _add(db, title=f"n{index}", starts_at=datetime.now(UTC) - timedelta(hours=index))
    await db.commit()
    assert await _current(client, api) == ["n0", "n1", "n2", "n3", "n4"]


async def test_admin_list_reports_status(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    _add(db, title="draft", active=False)
    _add(db, title="scheduled", starts_at=_in(1))
    _add(db, title="ended", starts_at=_in(-10), ends_at=_in(-1))
    _add(db, title="live")
    await db.commit()
    await _admin(client, api, db)

    listed = {
        item["title"]: item["status"] for item in (await client.get(f"{api}/announcements")).json()
    }

    assert listed == {"draft": "draft", "scheduled": "scheduled", "ended": "ended", "live": "live"}
