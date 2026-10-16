"""Найзаа урих: урилгын кодоор бүртгүүлсэн шинэ хэрэглэгч 10% хөнгөлөлт авна
(промо кодтой нийлэхгүй), урьсан хүн хөнгөлөлт авахгүй — урьсан найзуудаас 3 нь
багц авах бүрд 1 сар үнэгүй. Wire-ийг `tests/fake_wire.py` орлуулна."""

import uuid
from datetime import UTC, datetime, timedelta

import httpx
import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.payment import Payment
from app.models.promo_code import PromoCode
from app.models.referral import Referral
from app.models.user import User
from app.services.promo_service import CODE_ALPHABET
from tests.conftest import TEST_PASSWORD, login_as, make_user
from tests.fake_wire import FakeWire, checkout, install_fake_wire, pay
from tests.test_email_codes import GOOD_CODE, FakeSupabase, supabase  # noqa: F401

PRICE = 24_900
FRIEND_PRICE = 22_410  # 10% хөнгөлөлттэй
REFERRER = "urigch@test.mn"
SIGNUP = {"name": "Найз", "password": TEST_PASSWORD, "is_16_or_older": True, "accept_terms": True}


@pytest.fixture
def wire(monkeypatch: pytest.MonkeyPatch) -> FakeWire:
    return install_fake_wire(monkeypatch)


async def _referrer(client: httpx.AsyncClient, api: str, db: AsyncSession) -> tuple[User, str]:
    """Урьсан хэрэглэгч ба түүний код. Дараа нь нэвтэрсэн хэвээр."""
    user = await make_user(db, REFERRER)
    await login_as(client, api, REFERRER)
    summary = (await client.get(f"{api}/me/referral")).json()
    return user, summary["code"]


async def _register_friend(
    client: httpx.AsyncClient, api: str, email: str, code: str | None
) -> httpx.Response:
    """Бүртгүүлнэ. Баталгаажуулалт унтраалттай бол найз шууд нэвтэрнэ."""
    body = {**SIGNUP, "email": email}
    if code is not None:
        body["referral_code"] = code
    return await client.post(f"{api}/auth/register", json=body)


async def _paying_friends(
    client: httpx.AsyncClient, api: str, code: str, count: int, *, start: int = 1
) -> None:
    """`count` найз урилгаар бүртгүүлж, тус бүр 1 сарын багц авна."""
    for index in range(start, start + count):
        response = await _register_friend(client, api, f"naiz{index}@test.mn", code)
        assert response.status_code == 201, response.text
        await pay(client, api, await checkout(client, api))


async def _summary(client: httpx.AsyncClient, api: str) -> dict:
    await login_as(client, api, REFERRER)
    return (await client.get(f"{api}/me/referral")).json()


def _months_left(value: datetime | None) -> float:
    assert value is not None
    return (value - datetime.now(UTC)) / timedelta(days=30.4)


# --- Урилгын код ------------------------------------------------------------------


async def test_new_user_gets_a_referral_code_at_signup(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    response = await _register_friend(client, api, "shine@test.mn", None)

    code = response.json()["user"]["referral_code"]
    assert len(code) == 8
    assert set(code) <= set(CODE_ALPHABET)
    # Хэрэглэгчийн цэс `/auth/me`-ээс уншина.
    assert (await client.get(f"{api}/auth/me")).json()["referral_code"] == code
    assert (await client.get(f"{api}/me/referral")).json()["code"] == code


async def test_summary_starts_empty(client: httpx.AsyncClient, api: str, db: AsyncSession) -> None:
    user, code = await _referrer(client, api, db)

    assert (await client.get(f"{api}/me/referral")).json() == {
        "code": code,
        "friend_percent_off": 10,
        "friends_per_reward": 3,
        "reward_months": 1,
        "friends": 0,
        "paying_friends": 0,
        "friends_to_next_reward": 3,
        "months_earned": 0,
    }
    # Код анх `/me/referral`-д үүссэн ч хадгалагдаж, дахин өөрчлөгдөхгүй.
    await db.refresh(user)
    assert user.referral_code == code


async def test_referral_needs_login(client: httpx.AsyncClient, api: str) -> None:
    assert (await client.get(f"{api}/me/referral")).status_code == 401


# --- Бүртгүүлэх ----------------------------------------------------------------------


async def test_referred_new_user_gets_ten_percent(
    client: httpx.AsyncClient, api: str, db: AsyncSession, wire: FakeWire
) -> None:
    referrer, code = await _referrer(client, api, db)

    response = await _register_friend(client, api, "naiz@test.mn", f" {code.lower()} ")

    assert response.status_code == 201, response.text
    friend = (await db.execute(select(User).where(User.email == "naiz@test.mn"))).scalar_one()
    referral = (await db.execute(select(Referral))).scalar_one()
    assert (referral.referrer_id, referral.friend_id) == (referrer.id, friend.id)
    plan = (await client.get(f"{api}/billing/plan")).json()
    assert plan["discount"] == {"source": "referral", "percent_off": 10, "code": None}
    first = plan["options"][0]
    assert (first["price_mnt"], first["final_price_mnt"]) == (PRICE, FRIEND_PRICE)
    assert "referral_discounts" not in plan


async def test_referrer_gets_no_discount(
    client: httpx.AsyncClient, api: str, db: AsyncSession, wire: FakeWire
) -> None:
    _, code = await _referrer(client, api, db)
    await _register_friend(client, api, "naiz@test.mn", code)
    await login_as(client, api, REFERRER)

    plan = (await client.get(f"{api}/billing/plan")).json()

    assert plan["discount"] is None
    assert plan["options"][0]["final_price_mnt"] == PRICE
    await checkout(client, api)
    assert wire.last_amount == PRICE
    assert (await _summary(client, api))["friends"] == 1


async def test_unknown_referral_code_blocks_signup(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    response = await _register_friend(client, api, "naiz@test.mn", "NOSUCH12")

    assert response.status_code == 400
    assert response.json()["detail"]["code"] == "INVALID_REFERRAL_CODE"
    assert (await db.execute(select(User))).first() is None


async def test_blank_referral_code_is_ignored(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    response = await _register_friend(client, api, "naiz@test.mn", "   ")
    assert response.status_code == 201
    assert (await db.execute(select(Referral))).first() is None
    assert (await client.get(f"{api}/billing/plan")).json()["discount"] is None


async def test_duplicate_email_with_code_creates_no_referral(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    _, code = await _referrer(client, api, db)
    response = await _register_friend(client, api, REFERRER, code)
    assert response.status_code == 409
    assert (await db.execute(select(Referral))).first() is None


async def test_friend_counts_after_email_verification(
    client: httpx.AsyncClient,
    api: str,
    db: AsyncSession,
    supabase: FakeSupabase,  # noqa: F811
) -> None:
    _, code = await _referrer(client, api, db)

    response = await _register_friend(client, api, "naiz@test.mn", code)
    assert response.json()["verification_required"] is True
    assert (await _summary(client, api))["friends"] == 0

    verified = await client.post(
        f"{api}/auth/verify-email", json={"email": "naiz@test.mn", "code": GOOD_CODE}
    )
    assert verified.status_code == 200, verified.text
    assert verified.json()["referral_code"]
    assert (await _summary(client, api))["friends"] == 1


async def test_password_reset_also_confirms_the_friend(
    client: httpx.AsyncClient,
    api: str,
    db: AsyncSession,
    supabase: FakeSupabase,  # noqa: F811
) -> None:
    """Баталгаажаагүй найз нууц үгээ кодоор сэргээвэл имэйлээ баталгаажуулсанд тооцно."""
    _, code = await _referrer(client, api, db)
    await _register_friend(client, api, "naiz@test.mn", code)
    await client.post(f"{api}/auth/password/forgot", json={"email": "naiz@test.mn"})

    reset = await client.post(
        f"{api}/auth/password/reset",
        json={"email": "naiz@test.mn", "code": GOOD_CODE, "new_password": "Shine12345"},
    )

    assert reset.status_code == 200, reset.text
    assert (await _summary(client, api))["friends"] == 1


# --- Шинэ хэрэглэгчийн 10% ----------------------------------------------------------------


async def test_live_pass_keeps_the_friend_discount_for_a_plan(
    client: httpx.AsyncClient,
    api: str,
    db: AsyncSession,
    wire: FakeWire,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Нэг удаагийн эрх багц биш: 10% орохгүй, урьсан хүнд «багц авсан найз» болохгүй.
    Дараа нь багц авахад 10% ба эрхийн үнэ хоёулаа хасагдана."""
    monkeypatch.setattr(settings, "live_access", "all")
    _, code = await _referrer(client, api, db)
    await _register_friend(client, api, "naiz@test.mn", code)

    response = await client.post(f"{api}/billing/checkout", json={"plan": "live_pass"})
    assert response.status_code == 200, response.text
    status = await pay(client, api, response.json()["payment_id"])
    assert wire.last_amount == 4_900
    assert status["receipt"]["discount_mnt"] == 0
    assert status["plan"]["discount"]["source"] == "referral"
    db.expire_all()
    referral = (await db.execute(select(Referral))).scalar_one()
    assert (referral.first_paid_at, referral.discount_used_at) == (None, None)

    await pay(client, api, await checkout(client, api, months=1))
    assert wire.last_amount == FRIEND_PRICE - 4_900
    assert (await _summary(client, api))["paying_friends"] == 1


async def test_friend_discount_is_used_on_paid_checkout(
    client: httpx.AsyncClient, api: str, db: AsyncSession, wire: FakeWire
) -> None:
    _, code = await _referrer(client, api, db)
    await _register_friend(client, api, "naiz@test.mn", code)

    payment_id = await checkout(client, api, months=1)

    assert wire.last_amount == FRIEND_PRICE
    assert wire.descriptions["pi_1"] == "Medleghub Standard багц — 1 сар (10% хөнгөлөлттэй)"
    payment = await db.get(Payment, uuid.UUID(payment_id))
    assert payment is not None
    assert (payment.discount_percent, payment.discount_mnt) == (10, 2_490)
    assert payment.referral_id is not None
    # Төлөөгүй бол хөнгөлөлт хэвээр (`/billing/plan` хүлээгдэж буй төлбөрийг Wire-ээс шалгана).
    wire.status = "requires_payment_method"
    assert (await client.get(f"{api}/billing/plan")).json()["discount"] is not None

    wire.status = "succeeded"
    body = await pay(client, api, payment_id)

    assert body["status"] == "succeeded"
    assert body["plan"]["discount"] is None
    receipt = body["receipt"]
    assert (receipt["discount_source"], receipt["discount_percent"], receipt["promo_code"]) == (
        "referral",
        10,
        None,
    )
    assert (receipt["list_price_mnt"], receipt["amount_mnt"]) == (PRICE, FRIEND_PRICE)
    assert body["plan"]["options"][0]["final_price_mnt"] == PRICE
    referral = (await db.execute(select(Referral))).scalar_one()
    await db.refresh(referral)
    assert referral.discount_used_at is not None
    # Дараагийн төлбөр бүтэн үнээр.
    await checkout(client, api, months=1)
    assert wire.last_amount == PRICE


async def test_friend_discount_applies_to_a_long_plan(
    client: httpx.AsyncClient, api: str, db: AsyncSession, wire: FakeWire
) -> None:
    _, code = await _referrer(client, api, db)
    await _register_friend(client, api, "naiz@test.mn", code)

    await checkout(client, api, months=12)

    # 12 сар = 10 сарын үнэ, дээрээс нь 10%.
    assert wire.last_amount == 10 * PRICE - 10 * PRICE // 10


async def test_canceled_payment_keeps_the_friend_discount(
    client: httpx.AsyncClient, api: str, db: AsyncSession, wire: FakeWire
) -> None:
    _, code = await _referrer(client, api, db)
    await _register_friend(client, api, "naiz@test.mn", code)
    wire.status = "canceled"

    assert (await pay(client, api, await checkout(client, api)))["status"] == "canceled"

    assert (await client.get(f"{api}/billing/plan")).json()["discount"] is not None


async def test_promo_code_replaces_the_friend_discount(
    client: httpx.AsyncClient, api: str, db: AsyncSession, wire: FakeWire
) -> None:
    """20% промо код + 10% урилга = 30% биш, зөвхөн 20%. Урилгын 10% дараа нь орно."""
    db.add(PromoCode(code="HELLOWORLD2026", kind="percent", percent_off=20))
    await db.commit()
    _, code = await _referrer(client, api, db)
    await _register_friend(client, api, "naiz@test.mn", code)

    payment_id = await checkout(client, api, promo_code="HELLOWORLD2026")

    assert wire.last_amount == 19_920
    payment = await db.get(Payment, uuid.UUID(payment_id))
    assert payment is not None
    assert (payment.discount_percent, payment.referral_id) == (20, None)
    await pay(client, api, payment_id)
    assert (await client.get(f"{api}/billing/plan")).json()["discount"]["percent_off"] == 10
    await checkout(client, api)
    assert wire.last_amount == FRIEND_PRICE


# --- Урьсан найзуудаас 3 нь багц авах бүрд 1 сар ----------------------------------------------


async def test_three_paying_friends_give_one_month(
    client: httpx.AsyncClient, api: str, db: AsyncSession, wire: FakeWire
) -> None:
    referrer, code = await _referrer(client, api, db)

    await _paying_friends(client, api, code, 2)
    await db.refresh(referrer)
    assert referrer.plan_expires_at is None
    summary = await _summary(client, api)
    assert (summary["paying_friends"], summary["friends_to_next_reward"]) == (2, 1)

    await _paying_friends(client, api, code, 1, start=3)

    await db.refresh(referrer)
    assert 0.9 < _months_left(referrer.plan_expires_at) < 1.1
    summary = await _summary(client, api)
    assert (summary["friends"], summary["paying_friends"], summary["months_earned"]) == (3, 3, 1)
    assert summary["friends_to_next_reward"] == 3


async def test_six_paying_friends_give_two_months(
    client: httpx.AsyncClient, api: str, db: AsyncSession, wire: FakeWire
) -> None:
    referrer, code = await _referrer(client, api, db)

    await _paying_friends(client, api, code, 6)

    await db.refresh(referrer)
    assert 1.9 < _months_left(referrer.plan_expires_at) < 2.1
    assert (await _summary(client, api))["months_earned"] == 2


async def test_a_friend_counts_once_however_much_they_buy(
    client: httpx.AsyncClient, api: str, db: AsyncSession, wire: FakeWire
) -> None:
    referrer, code = await _referrer(client, api, db)
    await _register_friend(client, api, "naiz@test.mn", code)

    await pay(client, api, await checkout(client, api, months=12))
    await pay(client, api, await checkout(client, api, months=3))
    await pay(client, api, await checkout(client, api, months=1))

    await db.refresh(referrer)
    assert referrer.plan_expires_at is None
    summary = await _summary(client, api)
    assert (summary["paying_friends"], summary["months_earned"]) == (1, 0)


async def test_friends_who_do_not_pay_do_not_count(
    client: httpx.AsyncClient, api: str, db: AsyncSession, wire: FakeWire
) -> None:
    referrer, code = await _referrer(client, api, db)
    for index in range(1, 3):
        await _register_friend(client, api, f"unegui{index}@test.mn", code)
    wire.status = "canceled"
    await _register_friend(client, api, "tsutsalsan@test.mn", code)
    await pay(client, api, await checkout(client, api))
    wire.status = "succeeded"
    await _paying_friends(client, api, code, 1)

    await db.refresh(referrer)
    assert referrer.plan_expires_at is None
    summary = await _summary(client, api)
    assert (summary["friends"], summary["paying_friends"]) == (4, 1)


async def test_reward_is_given_once_per_payment(
    client: httpx.AsyncClient, api: str, db: AsyncSession, wire: FakeWire
) -> None:
    referrer, code = await _referrer(client, api, db)
    await _paying_friends(client, api, code, 2)
    await _register_friend(client, api, "naiz3@test.mn", code)
    payment_id = await checkout(client, api)

    # Буцах хуудас ба webhook хоёулаа шалгасан ч шагнал давхардахгүй.
    await pay(client, api, payment_id)
    await pay(client, api, payment_id)

    await db.refresh(referrer)
    assert 0.9 < _months_left(referrer.plan_expires_at) < 1.1


async def test_reward_extends_an_active_plan(
    client: httpx.AsyncClient, api: str, db: AsyncSession, wire: FakeWire
) -> None:
    referrer, code = await _referrer(client, api, db)
    referrer.plan_expires_at = datetime.now(UTC) + timedelta(days=20)
    await db.commit()

    await _paying_friends(client, api, code, 3)

    await db.refresh(referrer)
    assert referrer.plan_expires_at is not None
    left = referrer.plan_expires_at - datetime.now(UTC)
    assert timedelta(days=47) < left < timedelta(days=52)


async def test_free_month_codes_do_not_make_a_paying_friend(
    client: httpx.AsyncClient, api: str, db: AsyncSession, wire: FakeWire
) -> None:
    _, code = await _referrer(client, api, db)
    db.add(PromoCode(code="GIFT3", kind="free_months", free_months=3))
    await db.commit()
    await _register_friend(client, api, "naiz@test.mn", code)

    redeem = await client.post(f"{api}/billing/promo/redeem", json={"code": "GIFT3"})

    assert redeem.status_code == 200
    assert (await _summary(client, api))["paying_friends"] == 0


async def test_friend_with_promo_code_still_counts_as_paying(
    client: httpx.AsyncClient, api: str, db: AsyncSession, wire: FakeWire
) -> None:
    db.add(PromoCode(code="HELLOWORLD2026", kind="percent", percent_off=20))
    await db.commit()
    _, code = await _referrer(client, api, db)
    await _register_friend(client, api, "naiz@test.mn", code)

    await pay(client, api, await checkout(client, api, promo_code="HELLOWORLD2026"))

    assert (await _summary(client, api))["paying_friends"] == 1


# --- Бүртгэл устгах ---------------------------------------------------------------------------


async def test_friend_deletion_keeps_the_referrer_stats(
    client: httpx.AsyncClient, api: str, db: AsyncSession, wire: FakeWire
) -> None:
    _, code = await _referrer(client, api, db)
    await _paying_friends(client, api, code, 3)
    friend = (await db.execute(select(User).where(User.email == "naiz3@test.mn"))).scalar_one()

    await db.delete(friend)
    await db.commit()

    referral = (await db.execute(select(Referral).where(Referral.months_rewarded > 0))).scalar_one()
    await db.refresh(referral)
    assert referral.friend_id is None
    summary = await _summary(client, api)
    assert (summary["friends"], summary["paying_friends"], summary["months_earned"]) == (3, 3, 1)


async def test_referrer_deletion_removes_the_referral(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    referrer, code = await _referrer(client, api, db)
    await _register_friend(client, api, "naiz@test.mn", code)

    await db.delete(referrer)
    await db.commit()

    assert (await db.execute(select(Referral))).first() is None
    assert (await db.execute(select(User).where(User.email == "naiz@test.mn"))).first()
