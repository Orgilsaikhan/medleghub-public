"""Санал хүсэлт — илгээх, админ жагсаалт, шийдсэн гэж тэмдэглэх."""

import uuid

import httpx
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.rate_limit import InMemoryRateLimitBackend
from app.models.enums import UserRole
from tests.conftest import login_as, make_user

STUDENT = "suragch@test.mn"
ADMIN = "admin@test.mn"

VALID = {"kind": "bug", "message": "Видео ачаалахгүй байна.", "page": "/learn/js/hicheel-1"}


async def test_send_requires_login(client: httpx.AsyncClient, api: str) -> None:
    assert (await client.post(f"{api}/feedback", json=VALID)).status_code == 401


@pytest.mark.parametrize(
    "payload",
    [
        {**VALID, "kind": "complaint"},
        {**VALID, "message": "   ok  "},
        {**VALID, "message": "а" * 2001},
        {**VALID, "page": "javascript:alert(1)"},
        {**VALID, "page": "https://evil.example/"},
        {**VALID, "page": "//evil.example/"},
        {**VALID, "page": "/\\evil.example/"},
    ],
)
async def test_send_rejects_invalid_input(
    client: httpx.AsyncClient, api: str, db: AsyncSession, payload: dict
) -> None:
    await make_user(db, STUDENT)
    await login_as(client, api, STUDENT)
    assert (await client.post(f"{api}/feedback", json=payload)).status_code == 422


async def test_admin_lists_and_resolves_feedback(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    await make_user(db, STUDENT)
    await make_user(db, ADMIN, role=UserRole.ADMIN)
    await login_as(client, api, STUDENT)
    sent = await client.post(f"{api}/feedback", json=VALID)
    assert sent.status_code == 201, sent.text
    await client.post(f"{api}/feedback", json={"kind": "idea", "message": "Харанхуй горим!"})

    # Сурагч жагсаалтыг харж чадахгүй.
    assert (await client.get(f"{api}/admin/feedback")).status_code == 403

    await login_as(client, api, ADMIN)
    page = (await client.get(f"{api}/admin/feedback")).json()
    assert page["total"] == 2
    newest, oldest = page["items"]
    assert newest["kind"] == "idea"
    assert newest["page"] is None
    assert oldest["page"] == VALID["page"]
    assert oldest["user"]["email"] == STUDENT
    assert oldest["resolved"] is False

    resolved = await client.patch(f"{api}/admin/feedback/{oldest['id']}", json={"resolved": True})
    assert resolved.status_code == 200, resolved.text
    assert resolved.json()["resolved"] is True

    open_items = (await client.get(f"{api}/admin/feedback", params={"resolved": False})).json()
    assert [item["id"] for item in open_items["items"]] == [newest["id"]]

    missing = await client.patch(f"{api}/admin/feedback/{uuid.uuid4()}", json={"resolved": True})
    assert missing.status_code == 404


async def test_send_is_rate_limited_per_user(
    client: httpx.AsyncClient, api: str, db: AsyncSession, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(settings, "rate_limit_enabled", True)
    monkeypatch.setattr(settings, "feedback_rate_limit_max", 2)
    monkeypatch.setattr("app.core.rate_limit.backend", InMemoryRateLimitBackend())
    await make_user(db, STUDENT)
    await login_as(client, api, STUDENT)

    statuses = [(await client.post(f"{api}/feedback", json=VALID)).status_code for _ in range(3)]

    assert statuses == [201, 201, 429]
