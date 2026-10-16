"""Онцлох амжилт (`PUT /me/showcase`) ба тэмдгийн ховор байдал (`earned_percent`)."""

import asyncio
import uuid
from datetime import UTC, datetime, timedelta

import httpx
import pytest
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.models.badge import SHOWCASE_MAX, UserBadge
from app.models.enums import UserRole
from app.models.user import User
from app.services import account_service, badge_service
from tests.conftest import TEST_DATABASE_URL, login_as, make_user

OWNER = "ezen@test.mn"
VIEWER = "uzegch@test.mn"
# Ахицгүй хэрэглэгчид профайл нээхэд олгогдохгүй тэмдгүүд — шууд бичнэ.
# Дээд тооноос нэгээр олон: хэтэрсэн хүсэлтийг шалгана.
EARNED = ["first-commit", "hello-world", "unstoppable", "code-smith", "compiler", "mastery"]
NOT_EARNED = {
    "code": "SHOWCASE_BADGE_NOT_EARNED",
    "message": "Зөвхөн авсан амжилтаа онцлох боломжтой.",
}


async def give(db: AsyncSession, user_id: uuid.UUID, *keys: str) -> None:
    db.add_all([UserBadge(user_id=user_id, badge_key=key) for key in keys])
    await db.commit()


async def owner_with_badges(client: httpx.AsyncClient, api: str, db: AsyncSession) -> uuid.UUID:
    """Анхааруулга: 400 хариу session-ийг rollback хийж ORM объектуудыг
    хуучирсан болгодог тул тестүүд `User` биш зөвхөн id-г хадгална."""
    owner = await make_user(db, OWNER)
    await give(db, owner.id, *EARNED)
    await login_as(client, api, OWNER)
    return owner.id


async def put(client: httpx.AsyncClient, api: str, keys: list[str]) -> httpx.Response:
    return await client.put(f"{api}/me/showcase", json={"badge_keys": keys})


def by_key(profile: dict) -> dict[str, dict]:
    return {badge["key"]: badge for badge in profile["badges"]}


def positions(profile: dict) -> dict[str, int]:
    """Онцолсон тэмдгүүд ба байр."""
    return {
        badge["key"]: badge["showcase_position"]
        for badge in profile["badges"]
        if badge["showcase_position"] is not None
    }


async def my_positions(client: httpx.AsyncClient, api: str) -> dict[str, int]:
    return positions((await client.get(f"{api}/me/profile")).json())


def test_limit_matches_the_db_constraint() -> None:
    """`SHOWCASE_MAX`-ийг өөрчилбөл CHECK-ийг migration-аар хамт өөрчилнө."""
    assert len(EARNED) == SHOWCASE_MAX + 1
    check = next(
        constraint
        for constraint in UserBadge.__table__.constraints
        if constraint.name == "ck_user_badges_showcase_position_valid"
    )
    assert str(check.sqltext) == f"showcase_position BETWEEN 1 AND {SHOWCASE_MAX}"


# --- Хадгалах ---------------------------------------------------------------------


async def test_showcase_keeps_the_given_order(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    await owner_with_badges(client, api, db)

    for count in range(1, SHOWCASE_MAX + 1):
        # Каталогийн биш, өгсөн дараалал — урвуугаар өгнө.
        keys = EARNED[:count][::-1]
        response = await put(client, api, keys)
        assert response.status_code == 200, response.text
        assert response.json() == {"badge_keys": keys}
        assert await my_positions(client, api) == {
            key: position for position, key in enumerate(keys, start=1)
        }


async def test_replacing_frees_old_positions(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    await owner_with_badges(client, api, db)
    await put(client, api, ["first-commit", "hello-world", "unstoppable"])

    # Байр солих (1 ↔ 2) — unique-ийг зөрчихгүй, хасагдсан нь байраа чөлөөлнө.
    swapped = await put(client, api, ["hello-world", "first-commit"])
    assert swapped.status_code == 200, swapped.text
    assert await my_positions(client, api) == {"hello-world": 1, "first-commit": 2}

    await put(client, api, ["mastery", "hello-world"])
    assert await my_positions(client, api) == {"mastery": 1, "hello-world": 2}


async def test_empty_list_clears_the_showcase(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    await owner_with_badges(client, api, db)
    await put(client, api, ["first-commit", "hello-world"])

    response = await put(client, api, [])

    assert response.status_code == 200, response.text
    assert response.json() == {"badge_keys": []}
    assert await my_positions(client, api) == {}


# --- Татгалзах ----------------------------------------------------------------------


@pytest.mark.parametrize(
    "keys",
    [EARNED, ["first-commit", "hello-world", "first-commit"]],
    ids=["too-many", "duplicate"],
)
async def test_too_many_or_duplicate_keys_are_invalid(
    client: httpx.AsyncClient, api: str, db: AsyncSession, keys: list[str]
) -> None:
    await owner_with_badges(client, api, db)
    await put(client, api, ["compiler"])

    response = await put(client, api, keys)

    assert response.status_code == 422, response.text
    detail = response.json()["detail"]
    assert detail["code"] == "VALIDATION_ERROR"
    assert [field["field"] for field in detail["fields"]] == ["badge_keys"]
    assert await my_positions(client, api) == {"compiler": 1}


async def test_missing_body_field_is_invalid(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    """Хоосон body онцлохыг санамсаргүй цуцлахгүй — `[]`-ийг ил илгээнэ."""
    await owner_with_badges(client, api, db)
    response = await client.put(f"{api}/me/showcase", json={})
    assert response.status_code == 422, response.text


async def test_only_earned_badges_can_be_showcased(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    owner_id = await owner_with_badges(client, api, db)
    # Каталогаас хасагдсан хуучин түлхүүр өгөгдлийн санд үлдсэн ч онцлогдохгүй.
    await give(db, owner_id, "unbroken")
    await put(client, api, ["compiler"])

    for keys in (["hello-world", "century"], ["no-such-badge"], ["unbroken"], [""]):
        response = await put(client, api, keys)
        assert response.status_code == 400, (keys, response.text)
        assert response.json()["detail"] == NOT_EARNED

    # Амжилтгүй хүсэлт юу ч өөрчлөөгүй — хэсэгчлэн ч хадгалаагүй.
    assert await my_positions(client, api) == {"compiler": 1}


async def test_showcase_requires_login(client: httpx.AsyncClient, api: str) -> None:
    assert (await put(client, api, [])).status_code == 401


async def test_showcase_is_public_and_only_the_owner_sets_it(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    owner_id = await owner_with_badges(client, api, db)
    await put(client, api, ["mastery", "compiler"])
    await make_user(db, VIEWER)
    await login_as(client, api, VIEWER)

    async def public() -> dict[str, int]:
        return positions((await client.get(f"{api}/users/{owner_id}/profile")).json())

    assert await public() == {"mastery": 1, "compiler": 2}

    # Өөр хэрэглэгч зөвхөн өөрийн авсан тэмдгийг — эзнийх өөрчлөгдөхгүй.
    denied = await put(client, api, ["mastery"])
    assert denied.status_code == 400
    assert denied.json()["detail"] == NOT_EARNED
    assert await public() == {"mastery": 1, "compiler": 2}
    assert await my_positions(client, api) == {}


async def test_concurrent_updates_never_collide(db: AsyncSession) -> None:
    """Хоёр хүсэлт зэрэг ирвэл нэг нь нөгөөгөө хүлээнэ — unique-ийн алдаа (500)
    гарахгүй, эцсийн төлөв нь аль нэгнийх бүхэлдээ (холилдохгүй)."""
    owner = await make_user(db, OWNER)
    owner_id = owner.id
    await give(db, owner_id, *EARNED)
    first, second = ["first-commit", "hello-world"], ["mastery", "compiler"]

    engine = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool)
    factory = async_sessionmaker(bind=engine, expire_on_commit=False, autoflush=False)

    async def save(keys: list[str]) -> list[str]:
        async with factory() as session:
            user = await session.get(User, owner_id)
            assert user is not None
            return await badge_service.set_showcase(session, user, keys)

    try:
        assert await asyncio.gather(save(first), save(second)) == [first, second]
    finally:
        await engine.dispose()

    rows = await db.execute(
        select(UserBadge.badge_key)
        .where(UserBadge.user_id == owner_id, UserBadge.showcase_position.is_not(None))
        .order_by(UserBadge.showcase_position)
    )
    assert rows.scalars().all() in (first, second)


async def test_deleting_the_account_removes_the_showcase(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    owner_id = await owner_with_badges(client, api, db)
    await put(client, api, ["compiler", "mastery"])
    await db.execute(
        update(User)
        .where(User.id == owner_id)
        .values(deletion_scheduled_at=datetime.now(UTC) - timedelta(seconds=1))
    )
    await db.commit()

    async with httpx.AsyncClient(
        transport=httpx.MockTransport(lambda _: httpx.Response(404)), base_url="https://p.test"
    ) as auth:
        assert await account_service.purge_due_accounts(db, auth) == 1

    left = await db.execute(select(UserBadge.id).where(UserBadge.user_id == owner_id))
    assert left.all() == []


# --- Ховор байдал -------------------------------------------------------------------


async def test_earned_percent_counts_verified_students_only(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    holder = await make_user(db, "s0@test.mn")
    holder_id = holder.id
    for index in (1, 2):
        await make_user(db, f"s{index}@test.mn")
    await give(db, holder_id, "night-owl")
    # Админ, имэйлээ баталгаажуулаагүй, профайлаа нуусан бүртгэл авсан ч тоонд
    # орохгүй (Нууцлалын бодлого §4.1).
    admin = await make_user(db, "admin@test.mn", role=UserRole.ADMIN)
    unverified = await make_user(db, "shine@test.mn")
    unverified.email_verified_at = None
    hidden = await make_user(db, "nuusan@test.mn")
    hidden.profile_hidden = True
    await db.commit()
    for user_id in (admin.id, unverified.id, hidden.id):
        await give(db, user_id, "night-owl", "century")
    await login_as(client, api, "s1@test.mn")

    badges = by_key((await client.get(f"{api}/me/profile")).json())
    assert badges["night-owl"]["earned_percent"] == 33.33  # 3-аас 1, 2 оронтой
    assert badges["century"]["earned_percent"] == 0.0
    # «Тун удахгүй» тэмдгийг хэн ч авах боломжгүй — хувьгүй.
    assert badges["mentor"]["available"] is False
    assert badges["mentor"]["earned_percent"] is None

    await make_user(db, "s3@test.mn")
    badges = by_key((await client.get(f"{api}/me/profile")).json())
    assert badges["night-owl"]["earned_percent"] == 25.0
    assert badges["night-owl"]["earned"] is False

    # Бусдын профайлд ч мөн адил.
    public = by_key((await client.get(f"{api}/users/{holder_id}/profile")).json())
    assert (public["night-owl"]["earned"], public["night-owl"]["earned_percent"]) == (True, 25.0)


async def test_earned_percent_is_none_without_counted_users(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    await make_user(db, "admin@test.mn", role=UserRole.ADMIN)
    await login_as(client, api, "admin@test.mn")

    profile = (await client.get(f"{api}/me/profile")).json()

    assert {badge["earned_percent"] for badge in profile["badges"]} == {None}
