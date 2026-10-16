"""Community-ийн дүрэм ба түдгэлзүүлэлт — 7 → 14 → 30 хоног, дараа нь бүрмөсөн."""

import uuid
from datetime import UTC, datetime, timedelta

import httpx
import pytest
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.community_post import CommunitySuspension
from app.models.enums import UserRole
from app.models.user import User
from tests.conftest import login_as, make_user

STUDENT = "suragch@test.mn"
OTHER = "busad@test.mn"
ADMIN = "admin@test.mn"

POST = {
    "title": "Python-д list-ийг яаж эрэмбэлэх вэ?",
    "body": "Тоонуудын жагсаалтыг эрэмбэлмээр байна.",
    "language": "python",
    "type": "help",
}


async def _join(client: httpx.AsyncClient, api: str, email: str) -> None:
    await login_as(client, api, email)
    assert (await client.post(f"{api}/community/guidelines")).status_code == 200


async def _suspend(
    client: httpx.AsyncClient, api: str, user: User, reason: str = "Спам нийтлэл"
) -> dict:
    response = await client.post(
        f"{api}/admin/community/suspensions", json={"user_id": str(user.id), "reason": reason}
    )
    assert response.status_code == 201, response.text
    return response.json()


async def _expire(db: AsyncSession, suspension_id: str) -> None:
    """Хугацааг өнгөрсөн болгоно — дараагийн шатыг шалгахад."""
    await db.execute(
        update(CommunitySuspension)
        .where(CommunitySuspension.id == uuid.UUID(suspension_id))
        .values(ends_at=datetime.now(UTC) - timedelta(minutes=1))
    )
    await db.commit()


def _days_from_now(iso: str) -> float:
    return (datetime.fromisoformat(iso) - datetime.now(UTC)) / timedelta(days=1)


async def test_status_before_accepting_guidelines(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    assert (await client.get(f"{api}/community/me")).status_code == 401
    await make_user(db, STUDENT)
    await login_as(client, api, STUDENT)

    status = (await client.get(f"{api}/community/me")).json()
    assert status == {
        "guidelines_accepted": False,
        "suspension": None,
        "suspension_days": [7, 14, 30],
    }


async def test_writing_requires_accepted_guidelines(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    author = await make_user(db, STUDENT)
    await make_user(db, OTHER)
    await _join(client, api, STUDENT)
    post = (await client.post(f"{api}/community/posts", json=POST)).json()
    comment = (
        await client.post(f"{api}/community/posts/{post['id']}/comments", json={"body": "Би"})
    ).json()

    await login_as(client, api, OTHER)
    attempts = [
        await client.post(f"{api}/community/posts", json=POST),
        await client.post(f"{api}/community/posts/{post['id']}/comments", json={"body": "Сайн"}),
        await client.put(f"{api}/community/posts/{post['id']}/like"),
        await client.post(f"{api}/community/posts/{post['id']}/report", json={"reason": "spam"}),
        await client.post(
            f"{api}/community/comments/{comment['id']}/report", json={"reason": "spam"}
        ),
    ]
    for response in attempts:
        assert response.status_code == 403, response.text
        assert response.json()["detail"]["code"] == "COMMUNITY_GUIDELINES_REQUIRED"

    # Уншихад дүрэм шаардлагагүй.
    assert (await client.get(f"{api}/community/posts")).status_code == 200
    assert (await client.get(f"{api}/community/posts/{post['id']}")).status_code == 200

    accepted = await client.post(f"{api}/community/guidelines")
    assert accepted.json()["guidelines_accepted"] is True
    assert (await client.post(f"{api}/community/posts", json=POST)).status_code == 201

    # Дахин зөвшөөрөхөд анхны огноо өөрчлөгдөхгүй.
    await login_as(client, api, STUDENT)
    await db.refresh(author)
    first = author.community_guidelines_accepted_at
    await client.post(f"{api}/community/guidelines")
    await db.refresh(author)
    assert author.community_guidelines_accepted_at == first


async def test_suspensions_escalate_to_permanent(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    student = await make_user(db, STUDENT)
    await make_user(db, ADMIN, role=UserRole.ADMIN)
    await login_as(client, api, ADMIN)

    levels = []
    for expected_days in (7, 14, 30):
        suspension = await _suspend(client, api, student)
        assert suspension["active"] is True
        assert round(_days_from_now(suspension["ends_at"])) == expected_days
        levels.append(suspension["level"])
        await _expire(db, suspension["id"])

    permanent = await _suspend(client, api, student)
    assert levels == [1, 2, 3]
    assert (permanent["level"], permanent["ends_at"]) == (4, None)
    assert permanent["user"] == {"id": str(student.id), "name": student.name, "email": STUDENT}
    assert permanent["admin"]["name"] == "Тест"

    # Бүрмөсөн ч цаашид дахин түдгэлзүүлэх шаардлагагүй.
    again = await client.post(
        f"{api}/admin/community/suspensions",
        json={"user_id": str(student.id), "reason": "Дахиад"},
    )
    assert again.status_code == 409


async def test_suspended_user_can_only_read(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    student = await make_user(db, STUDENT)
    await make_user(db, ADMIN, role=UserRole.ADMIN)
    await _join(client, api, STUDENT)
    post = (await client.post(f"{api}/community/posts", json=POST)).json()
    extra = (await client.post(f"{api}/community/posts", json=POST)).json()

    await login_as(client, api, ADMIN)
    suspension = await _suspend(client, api, student, reason="Доромжилсон сэтгэгдэл")

    await login_as(client, api, STUDENT)
    status = (await client.get(f"{api}/community/me")).json()
    assert status["suspension"]["level"] == 1
    assert status["suspension"]["reason"] == "Доромжилсон сэтгэгдэл"
    assert round(_days_from_now(status["suspension"]["ends_at"])) == 7

    attempts = [
        await client.post(f"{api}/community/posts", json=POST),
        await client.post(f"{api}/community/posts/{post['id']}/comments", json={"body": "Сайн"}),
        await client.put(f"{api}/community/posts/{post['id']}/like"),
        await client.delete(f"{api}/community/posts/{post['id']}/like"),
        await client.post(f"{api}/community/posts/{post['id']}/report", json={"reason": "spam"}),
    ]
    for response in attempts:
        assert response.status_code == 403, response.text
        assert response.json()["detail"]["code"] == "COMMUNITY_SUSPENDED"

    assert (await client.get(f"{api}/community/posts")).status_code == 200
    assert (await client.get(f"{api}/community/posts/{post['id']}")).status_code == 200
    # Өөрийнхөө бичсэнийг устгаж болно.
    assert (await client.delete(f"{api}/community/posts/{extra['id']}")).status_code == 200

    # Хугацаа дуусахад дахин бичнэ.
    await _expire(db, suspension["id"])
    assert (await client.get(f"{api}/community/me")).json()["suspension"] is None
    assert (await client.post(f"{api}/community/posts", json=POST)).status_code == 201


async def test_lifted_suspension_does_not_count(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    student = await make_user(db, STUDENT)
    await make_user(db, ADMIN, role=UserRole.ADMIN)
    await login_as(client, api, ADMIN)

    first = await _suspend(client, api, student)
    lifted = await client.post(f"{api}/admin/community/suspensions/{first['id']}/lift")
    assert lifted.status_code == 200, lifted.text
    assert lifted.json()["active"] is False
    assert lifted.json()["lifted_at"] is not None

    again = await client.post(f"{api}/admin/community/suspensions/{first['id']}/lift")
    assert again.status_code == 409
    missing = await client.post(f"{api}/admin/community/suspensions/{uuid.uuid4()}/lift")
    assert missing.status_code == 404

    second = await _suspend(client, api, student)
    assert second["level"] == 1
    assert round(_days_from_now(second["ends_at"])) == 7


@pytest.mark.parametrize(
    ("target", "reason", "expected"),
    [
        ("admin", "Спам нийтлэл", 400),
        ("missing", "Спам нийтлэл", 404),
        ("student", "Муу", 422),
        ("student", "а" * 501, 422),
    ],
)
async def test_suspend_rejects_invalid_targets(
    client: httpx.AsyncClient,
    api: str,
    db: AsyncSession,
    target: str,
    reason: str,
    expected: int,
) -> None:
    student = await make_user(db, STUDENT)
    admin = await make_user(db, ADMIN, role=UserRole.ADMIN)
    await login_as(client, api, ADMIN)
    user_id = {"admin": admin.id, "student": student.id, "missing": uuid.uuid4()}[target]

    response = await client.post(
        f"{api}/admin/community/suspensions", json={"user_id": str(user_id), "reason": reason}
    )
    assert response.status_code == expected, response.text


async def test_only_admin_manages_suspensions(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    await make_user(db, STUDENT)
    other = await make_user(db, OTHER)
    await login_as(client, api, STUDENT)

    assert (await client.get(f"{api}/admin/community/suspensions")).status_code == 403
    response = await client.post(
        f"{api}/admin/community/suspensions",
        json={"user_id": str(other.id), "reason": "Спам нийтлэл"},
    )
    assert response.status_code == 403


async def test_admin_lists_active_and_past_suspensions(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    student = await make_user(db, STUDENT)
    other = await make_user(db, OTHER)
    await make_user(db, ADMIN, role=UserRole.ADMIN)
    await login_as(client, api, ADMIN)

    past = await _suspend(client, api, student)
    await _expire(db, past["id"])
    lifted = await _suspend(client, api, other)
    await client.post(f"{api}/admin/community/suspensions/{lifted['id']}/lift")
    current = await _suspend(client, api, student)

    async def ids(**params: str) -> list[str]:
        page = (await client.get(f"{api}/admin/community/suspensions", params=params)).json()
        return [item["id"] for item in page["items"]]

    assert await ids() == [current["id"], lifted["id"], past["id"]]
    assert await ids(active="true") == [current["id"]]
    assert await ids(active="false") == [lifted["id"], past["id"]]


async def test_suspensions_follow_account_deletion(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    student = await make_user(db, STUDENT)
    other = await make_user(db, OTHER)
    admin = await make_user(db, ADMIN, role=UserRole.ADMIN)
    await login_as(client, api, ADMIN)
    await _suspend(client, api, student)
    kept = await _suspend(client, api, other)

    await db.execute(delete(User).where(User.id.in_([student.id, admin.id])))
    await db.commit()

    rows = (await db.execute(select(CommunitySuspension.id, CommunitySuspension.admin_id))).all()
    # Түдгэлзсэн хэрэглэгчийнх нь устана; админ устахад түүх үлдэж, админгүй болно.
    assert rows == [(uuid.UUID(kept["id"]), None)]
