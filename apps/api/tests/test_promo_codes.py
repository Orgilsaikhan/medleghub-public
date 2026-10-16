"""Промо код — админ үүсгэнэ; хэрэглэгч checkout дээр (хувь) эсвэл идэвхжүүлж
(үнэгүй сар) ашиглана. Wire-ийг `tests/fake_wire.py` орлуулна."""

import uuid
from datetime import UTC, datetime, timedelta

import httpx
import pytest
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.content.promo_codes import SEED_PROMO_CODES
from app.core import rate_limit
from app.core.config import settings
from app.core.rate_limit import InMemoryRateLimitBackend
from app.models.enums import UserRole
from app.models.payment import Payment
from app.models.promo_code import PromoCode, PromoRedemption
from app.models.user import User
from app.seed import _ensure_promo_codes
from app.services.promo_service import CODE_ALPHABET
from tests.conftest import login_as, make_user
from tests.fake_wire import FakeWire, checkout, install_fake_wire, pay

PRICE = 24_900
ADMIN = "admin@test.mn"
STUDENT = "suragch@test.mn"


@pytest.fixture
def wire(monkeypatch: pytest.MonkeyPatch) -> FakeWire:
    return install_fake_wire(monkeypatch)


async def _admin(client: httpx.AsyncClient, api: str, db: AsyncSession) -> None:
    await make_user(db, ADMIN, UserRole.ADMIN)
    await login_as(client, api, ADMIN)


async def _create(client: httpx.AsyncClient, api: str, **body: object) -> dict:
    response = await client.post(f"{api}/billing/promo-codes", json=body)
    assert response.status_code == 201, response.text
    return response.json()


async def _as_student(
    client: httpx.AsyncClient, api: str, db: AsyncSession, email: str = STUDENT
) -> User:
    user = await make_user(db, email)
    await login_as(client, api, email)
    return user


async def _code(
    db: AsyncSession, code: str = "HELLOWORLD2026", *, percent: int | None = 20, **fields: object
) -> PromoCode:
    """Кодыг шууд санд — хэрэглэгчийн талын тестэд админаар нэвтрэхгүйн тулд."""
    promo = PromoCode(
        code=code,
        kind="percent" if percent is not None else "free_months",
        percent_off=percent,
        **fields,
    )
    db.add(promo)
    await db.commit()
    return promo


def _plus_months(value: str, low: int, high: int) -> None:
    left = datetime.fromisoformat(value) - datetime.now(UTC)
    assert timedelta(days=low) < left < timedelta(days=high), left


# --- Админ -------------------------------------------------------------------


async def test_admin_creates_and_lists_codes(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    await _admin(client, api, db)
    expires = (datetime.now(UTC) + timedelta(days=30)).isoformat()

    created = await _create(
        client, api, code="hello-world 2026", kind="percent", percent_off=20, expires_at=expires
    )

    assert created["code"] == "HELLOWORLD2026"
    assert (created["kind"], created["percent_off"], created["free_months"]) == (
        "percent",
        20,
        None,
    )
    assert (created["uses"], created["status"], created["active"]) == (0, "active", True)
    assert created["created_by"] == "Тест"
    listed = (await client.get(f"{api}/billing/promo-codes")).json()
    assert [item["code"] for item in listed] == ["HELLOWORLD2026"]


async def test_blank_code_is_generated(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    await _admin(client, api, db)
    created = await _create(client, api, code="  ", kind="free_months", free_months=2)
    assert len(created["code"]) == 8
    assert set(created["code"]) <= set(CODE_ALPHABET)
    assert (created["percent_off"], created["free_months"]) == (None, 2)


async def test_duplicate_code_is_rejected(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    await _admin(client, api, db)
    await _create(client, api, code="SALE20", kind="percent", percent_off=20)
    response = await client.post(
        f"{api}/billing/promo-codes", json={"code": "sale20", "kind": "percent", "percent_off": 5}
    )
    assert response.status_code == 409
    assert response.json()["detail"]["code"] == "PROMO_CODE_TAKEN"


@pytest.mark.parametrize(
    "body",
    [
        {"kind": "percent"},
        {"kind": "free_months"},
        {"kind": "percent", "percent_off": 100},
        {"kind": "percent", "percent_off": 0},
        {"kind": "free_months", "free_months": 13},
        {"kind": "percent", "percent_off": 10, "code": "ab"},
        {"kind": "percent", "percent_off": 10, "code": "ХАЙ2026"},
        {"kind": "percent", "percent_off": 10, "max_uses": 0},
        {"kind": "percent", "percent_off": 10, "expires_at": "2020-01-01T00:00:00Z"},
    ],
)
async def test_invalid_codes_are_rejected(
    client: httpx.AsyncClient, api: str, db: AsyncSession, body: dict
) -> None:
    await _admin(client, api, db)
    response = await client.post(f"{api}/billing/promo-codes", json=body)
    assert response.status_code == 422, response.text


async def test_only_admins_manage_codes(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    assert (await client.get(f"{api}/billing/promo-codes")).status_code == 401
    await _as_student(client, api, db)
    assert (await client.get(f"{api}/billing/promo-codes")).status_code == 403
    body = {"kind": "percent", "percent_off": 90}
    assert (await client.post(f"{api}/billing/promo-codes", json=body)).status_code == 403
    promo = await _code(db)
    patch = await client.patch(f"{api}/billing/promo-codes/{promo.id}", json={"active": False})
    assert patch.status_code == 403


async def test_admin_updates_expiry_limit_and_status(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    await _admin(client, api, db)
    created = await _create(client, api, code="SALE20", kind="percent", percent_off=20, max_uses=5)
    url = f"{api}/billing/promo-codes/{created['id']}"
    later = datetime(2027, 3, 1, 15, 59, 59, tzinfo=UTC)

    body = (
        await client.patch(url, json={"expires_at": later.isoformat(), "max_uses": None})
    ).json()
    assert datetime.fromisoformat(body["expires_at"]) == later
    assert body["max_uses"] is None
    # Ирээгүй талбар өөрчлөгдөхгүй.
    assert (body["active"], body["percent_off"]) == (True, 20)

    body = (await client.patch(url, json={"active": False})).json()
    assert (body["active"], body["status"]) == (False, "disabled")
    assert datetime.fromisoformat(body["expires_at"]) == later

    assert (await client.patch(url, json={"active": None})).status_code == 422
    missing = await client.patch(f"{api}/billing/promo-codes/{uuid.uuid4()}", json={})
    assert missing.status_code == 404


async def test_status_reports_expired_and_used_up(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    await _admin(client, api, db)
    expired = await _code(db, "OLDCODE", expires_at=datetime.now(UTC) - timedelta(days=1))
    used_up = await _code(db, "ONCEONLY", max_uses=1)
    friend = await make_user(db, "friend@test.mn")
    db.add(PromoRedemption(promo_code_id=used_up.id, user_id=friend.id))
    await db.commit()

    listed = {
        item["code"]: item for item in (await client.get(f"{api}/billing/promo-codes")).json()
    }
    assert listed[expired.code]["status"] == "expired"
    assert (listed[used_up.code]["status"], listed[used_up.code]["uses"]) == ("used_up", 1)


# --- Шалгах ------------------------------------------------------------------


async def test_check_shows_discounted_prices(
    client: httpx.AsyncClient, api: str, db: AsyncSession, wire: FakeWire
) -> None:
    await _code(db)
    await _as_student(client, api, db)

    response = await client.post(f"{api}/billing/promo/check", json={"code": " helloworld2026 "})

    assert response.status_code == 200, response.text
    body = response.json()
    assert (body["code"], body["kind"], body["percent_off"]) == ("HELLOWORLD2026", "percent", 20)
    by_months = {option["months"]: option for option in body["options"]}
    assert (by_months[1]["price_mnt"], by_months[1]["final_price_mnt"]) == (PRICE, 19_920)
    # 12 сар = 10 сарын үнэ, дээрээс нь 20%.
    assert by_months[12]["final_price_mnt"] == 10 * PRICE * 80 // 100
    # Шалгах нь ашигласанд тооцохгүй.
    assert (await db.execute(select(PromoRedemption))).first() is None


async def test_check_requires_login(client: httpx.AsyncClient, api: str) -> None:
    response = await client.post(f"{api}/billing/promo/check", json={"code": "X"})
    assert response.status_code == 401


@pytest.mark.parametrize(
    ("fields", "error"),
    [
        ({"active": False}, "PROMO_INVALID"),
        ({"expires_at": datetime(2020, 1, 1, tzinfo=UTC)}, "PROMO_EXPIRED"),
    ],
)
async def test_check_rejects_unusable_codes(
    client: httpx.AsyncClient, api: str, db: AsyncSession, fields: dict, error: str
) -> None:
    await _code(db, **fields)
    await _as_student(client, api, db)
    response = await client.post(f"{api}/billing/promo/check", json={"code": "HELLOWORLD2026"})
    assert response.status_code == 400
    assert response.json()["detail"]["code"] == error


async def test_unknown_code_is_invalid(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    await _as_student(client, api, db)
    response = await client.post(f"{api}/billing/promo/check", json={"code": "NOPE"})
    assert response.status_code == 400
    assert response.json()["detail"]["code"] == "PROMO_INVALID"


async def test_promo_attempts_are_rate_limited(
    client: httpx.AsyncClient, api: str, db: AsyncSession, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(settings, "rate_limit_enabled", True)
    monkeypatch.setattr(settings, "auth_rate_limit_max", 100)
    monkeypatch.setattr(settings, "promo_rate_limit_max", 2)
    monkeypatch.setattr(rate_limit, "backend", InMemoryRateLimitBackend())
    await _as_student(client, api, db)

    for _ in range(2):
        response = await client.post(f"{api}/billing/promo/check", json={"code": "GUESS1"})
        assert response.status_code == 400
    response = await client.post(f"{api}/billing/promo/check", json={"code": "GUESS2"})
    assert response.status_code == 429


# --- Хувийн код checkout дээр --------------------------------------------------


async def test_checkout_with_code_charges_less_and_counts_on_success(
    client: httpx.AsyncClient, api: str, db: AsyncSession, wire: FakeWire
) -> None:
    promo = await _code(db)
    user = await _as_student(client, api, db)

    payment_id = await checkout(client, api, months=1, promo_code="helloworld2026")

    assert wire.last_amount == 19_920
    assert wire.descriptions["pi_1"] == "Medleghub Standard багц — 1 сар (20% хөнгөлөлттэй)"
    payment = await db.get(Payment, uuid.UUID(payment_id))
    assert payment is not None
    assert (payment.amount, payment.discount_percent, payment.discount_mnt) == (19_920, 20, 4_980)
    assert payment.promo_code_id == promo.id
    # Төлөөгүй нэхэмжлэх кодыг ашигласанд тооцохгүй.
    assert (await db.execute(select(PromoRedemption))).first() is None

    body = await pay(client, api, payment_id)
    assert body["status"] == "succeeded"
    _plus_months(body["plan"]["plan_expires_at"], 27, 32)
    receipt = body["receipt"]
    assert (receipt["list_price_mnt"], receipt["discount_mnt"], receipt["amount_mnt"]) == (
        PRICE,
        4_980,
        19_920,
    )
    assert (receipt["discount_percent"], receipt["discount_source"], receipt["promo_code"]) == (
        20,
        "promo",
        "HELLOWORLD2026",
    )
    assert receipt["kind"] == "payment"
    redemption = (await db.execute(select(PromoRedemption))).scalar_one()
    assert (redemption.user_id, redemption.payment_id) == (user.id, payment.id)

    again = await client.post(
        f"{api}/billing/checkout", json={"months": 1, "promo_code": "HELLOWORLD2026"}
    )
    assert again.status_code == 409
    assert again.json()["detail"]["code"] == "PROMO_ALREADY_USED"


async def test_percent_applies_after_free_months(
    client: httpx.AsyncClient, api: str, db: AsyncSession, wire: FakeWire
) -> None:
    await _code(db)
    await _as_student(client, api, db)
    payment_id = await checkout(client, api, months=12, promo_code="HELLOWORLD2026")
    assert wire.last_amount == 199_200
    _plus_months((await pay(client, api, payment_id))["plan"]["plan_expires_at"], 360, 370)


async def test_canceled_payment_does_not_use_the_code(
    client: httpx.AsyncClient, api: str, db: AsyncSession, wire: FakeWire
) -> None:
    await _code(db)
    await _as_student(client, api, db)
    wire.status = "canceled"
    payment_id = await checkout(client, api, promo_code="HELLOWORLD2026")
    assert (await pay(client, api, payment_id))["status"] == "canceled"

    assert (await db.execute(select(PromoRedemption))).first() is None
    wire.status = "succeeded"
    payment_id = await checkout(client, api, promo_code="HELLOWORLD2026")
    assert (await pay(client, api, payment_id))["status"] == "succeeded"


async def test_max_uses_stops_other_users(
    client: httpx.AsyncClient, api: str, db: AsyncSession, wire: FakeWire
) -> None:
    await _code(db, max_uses=1)
    await _as_student(client, api, db)
    await pay(client, api, await checkout(client, api, promo_code="HELLOWORLD2026"))

    await _as_student(client, api, db, "second@test.mn")
    response = await client.post(f"{api}/billing/promo/check", json={"code": "HELLOWORLD2026"})
    assert response.status_code == 400
    assert response.json()["detail"]["code"] == "PROMO_USED_UP"


async def test_two_open_checkouts_count_the_code_once(
    client: httpx.AsyncClient, api: str, db: AsyncSession, wire: FakeWire
) -> None:
    """Хоёр нэхэмжлэхийг хоёуланг нь төлбөл төлсөн хэвээр — код нэг л удаа бичигдэнэ."""
    await _code(db)
    await _as_student(client, api, db)
    first = await checkout(client, api, promo_code="HELLOWORLD2026")
    second = await checkout(client, api, promo_code="HELLOWORLD2026")

    await pay(client, api, first)
    body = await pay(client, api, second)

    assert body["status"] == "succeeded"
    _plus_months(body["plan"]["plan_expires_at"], 58, 63)
    assert len((await db.execute(select(PromoRedemption))).all()) == 1


# --- Үнэгүй сарын код ------------------------------------------------------------


async def test_free_months_code_extends_plan_without_payment(
    client: httpx.AsyncClient, api: str, db: AsyncSession, wire: FakeWire
) -> None:
    await _code(db, "GIFT3", percent=None, free_months=3)
    user = await _as_student(client, api, db)

    preview = (await client.post(f"{api}/billing/promo/check", json={"code": "gift3"})).json()
    assert (preview["kind"], preview["free_months"], preview["options"]) == ("free_months", 3, [])

    response = await client.post(f"{api}/billing/promo/redeem", json={"code": "gift3"})

    assert response.status_code == 200, response.text
    assert response.json()["has_plan"] is True
    _plus_months(response.json()["plan_expires_at"], 88, 94)
    redemption = (await db.execute(select(PromoRedemption))).scalar_one()
    assert (redemption.user_id, redemption.months, redemption.payment_id) == (user.id, 3, None)
    assert wire.amounts == {}

    again = await client.post(f"{api}/billing/promo/redeem", json={"code": "GIFT3"})
    assert again.status_code == 409
    assert again.json()["detail"]["code"] == "PROMO_ALREADY_USED"


async def test_free_months_code_has_a_receipt(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    await _code(db, "GIFT3", percent=None, free_months=3)
    await _as_student(client, api, db)

    redeemed = (await client.post(f"{api}/billing/promo/redeem", json={"code": "gift3"})).json()
    response = await client.get(f"{api}/billing/redemptions/{redeemed['redemption_id']}")

    assert response.status_code == 200, response.text
    body = response.json()
    assert body["id"] == redeemed["redemption_id"]
    assert body["plan"]["has_plan"] is True
    receipt = body["receipt"]
    assert (receipt["kind"], receipt["months"], receipt["promo_code"]) == ("promo", 3, "GIFT3")
    assert (receipt["amount_mnt"], receipt["reference"]) == (0, None)
    assert receipt["paid_at"] is not None


async def test_redemption_receipts_are_private(
    client: httpx.AsyncClient, api: str, db: AsyncSession, wire: FakeWire
) -> None:
    await _code(db, "GIFT3", percent=None, free_months=3)
    await _code(db)
    await _as_student(client, api, db)
    gift = (await client.post(f"{api}/billing/promo/redeem", json={"code": "GIFT3"})).json()
    await pay(client, api, await checkout(client, api, promo_code="HELLOWORLD2026"))
    percent = (
        await db.execute(select(PromoRedemption).where(PromoRedemption.payment_id.is_not(None)))
    ).scalar_one()

    # Хувийн хөнгөлөлтийн бичлэгийн баримт нь төлбөрийнх — энд байхгүй.
    missing = await client.get(f"{api}/billing/redemptions/{percent.id}")
    assert missing.status_code == 404
    assert (await client.get(f"{api}/billing/redemptions/{uuid.uuid4()}")).status_code == 404

    await _as_student(client, api, db, "second@test.mn")
    other = await client.get(f"{api}/billing/redemptions/{gift['redemption_id']}")
    assert other.status_code == 404
    assert other.json()["detail"]["code"] == "REDEMPTION_NOT_FOUND"


async def test_free_months_add_to_active_plan(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    await _code(db, "GIFT1", percent=None, free_months=1)
    user = await _as_student(client, api, db)
    await db.execute(
        update(User)
        .where(User.id == user.id)
        .values(plan_expires_at=datetime.now(UTC) + timedelta(days=10))
    )
    await db.commit()

    body = (await client.post(f"{api}/billing/promo/redeem", json={"code": "GIFT1"})).json()
    _plus_months(body["plan_expires_at"], 37, 43)


async def test_codes_are_used_in_the_right_place(
    client: httpx.AsyncClient, api: str, db: AsyncSession, wire: FakeWire
) -> None:
    await _code(db)
    await _code(db, "GIFT3", percent=None, free_months=3)
    await _as_student(client, api, db)

    redeem = await client.post(f"{api}/billing/promo/redeem", json={"code": "HELLOWORLD2026"})
    assert redeem.status_code == 400
    assert redeem.json()["detail"]["code"] == "PROMO_NOT_REDEEMABLE"

    pay_with_gift = await client.post(
        f"{api}/billing/checkout", json={"months": 1, "promo_code": "GIFT3"}
    )
    assert pay_with_gift.status_code == 400
    assert pay_with_gift.json()["detail"]["code"] == "PROMO_FREE_MONTHS"
    assert wire.amounts == {}


async def test_free_months_code_respects_max_uses(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    await _code(db, "GIFT1", percent=None, free_months=1, max_uses=1)
    await _as_student(client, api, db)
    assert (
        await client.post(f"{api}/billing/promo/redeem", json={"code": "GIFT1"})
    ).status_code == 200

    await _as_student(client, api, db, "second@test.mn")
    response = await client.post(f"{api}/billing/promo/redeem", json={"code": "GIFT1"})
    assert response.status_code == 400
    assert response.json()["detail"]["code"] == "PROMO_USED_UP"


# --- Бүртгэл устгах, seed ---------------------------------------------------------


async def test_deleted_account_keeps_the_use_count(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    promo = await _code(db, "GIFT1", percent=None, free_months=1, max_uses=1)
    user = await _as_student(client, api, db)
    await client.post(f"{api}/billing/promo/redeem", json={"code": "GIFT1"})

    await db.delete(user)
    await db.commit()

    redemption = (await db.execute(select(PromoRedemption))).scalar_one()
    assert (redemption.user_id, redemption.promo_code_id) == (None, promo.id)
    await _as_student(client, api, db, "second@test.mn")
    response = await client.post(f"{api}/billing/promo/redeem", json={"code": "GIFT1"})
    assert response.json()["detail"]["code"] == "PROMO_USED_UP"


async def test_seed_adds_helloworld_once_and_keeps_admin_edits(db: AsyncSession) -> None:
    await _ensure_promo_codes(db, SEED_PROMO_CODES)
    await db.commit()
    promo = (await db.execute(select(PromoCode))).scalar_one()
    assert (promo.code, promo.kind, promo.percent_off, promo.active) == (
        "HELLOWORLD2026",
        "percent",
        20,
        True,
    )
    # 2026-12-31 23:59:59 Улаанбаатарын цагаар.
    assert promo.expires_at == datetime(2026, 12, 31, 15, 59, 59, tzinfo=UTC)

    promo.active = False
    await db.commit()
    await _ensure_promo_codes(db, SEED_PROMO_CODES)
    await db.commit()
    await db.refresh(promo)
    assert promo.active is False
    assert len((await db.execute(select(PromoCode))).all()) == 1
