"""Standard багц ба Wire төлбөр.

Wire-ийг `httpx.MockTransport`-оор орлуулна — жинхэнэ сүлжээнд гарахгүй.
"""

import hashlib
import hmac
import json
import time
import uuid
from collections.abc import AsyncGenerator, Callable
from datetime import UTC, datetime, timedelta

import httpx
import pytest
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.main import app
from app.models.enums import UserRole
from app.models.live import LivePass, LiveSubscription
from app.models.payment import Payment
from app.models.plan_adjustment import PlanAdjustment
from app.models.plan_price import PlanPrice
from app.models.promo_code import PromoCode
from app.models.user import User
from app.services.wire import get_wire_client
from tests.conftest import login_as, make_user
from tests.fake_wire import install_fake_wire, pay

Handler = Callable[[httpx.Request], httpx.Response]

# Бүхэл төгрөг — Wire-ийн live API ×100 хийвэл 100 дахин их нэхдэг.
PRICE_MNT = 24_900
WEBHOOK_SECRET = "whsec_test"


@pytest.fixture(autouse=True)
def _wire_settings(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(settings, "wire_secret_key", "sk_test_123")
    monkeypatch.setattr(settings, "wire_webhook_secret", WEBHOOK_SECRET)
    monkeypatch.setattr(settings, "wire_allowed_operators", ["sandbox"])
    monkeypatch.setattr(settings, "site_url", "https://medleghub.com")


def use_wire(handler: Handler) -> list[httpx.Request]:
    seen: list[httpx.Request] = []

    def record(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return handler(request)

    async def override() -> AsyncGenerator[httpx.AsyncClient, None]:
        async with httpx.AsyncClient(
            transport=httpx.MockTransport(record), base_url="https://api.wire.test"
        ) as client:
            yield client

    app.dependency_overrides[get_wire_client] = override
    return seen


def wire_api(*, intent_status: str = "succeeded", amount: int = PRICE_MNT) -> Handler:
    """Wire-ийн энгийн загвар: intent `pi_1`, session, retrieve."""

    def handler(request: httpx.Request) -> httpx.Response:
        if request.method == "POST" and request.url.path == "/v1/payment_intents":
            return httpx.Response(
                200, json={"id": "pi_1", "status": "requires_payment_method", "amount": amount}
            )
        if request.method == "POST" and request.url.path == "/v1/checkout/sessions":
            return httpx.Response(
                200,
                json={"id": "cs_1", "url": "https://pay.wire.mn/c/tok", "payment_intent": "pi_1"},
            )
        if request.method == "GET" and request.url.path == "/v1/payment_intents/pi_1":
            return httpx.Response(
                200,
                json={"id": "pi_1", "status": intent_status, "amount": amount, "currency": "MNT"},
            )
        return httpx.Response(404, json={"error": {"code": "not_found"}})

    return handler


async def _student(client: httpx.AsyncClient, api: str, db: AsyncSession) -> User:
    user = await make_user(db, "tologch@test.mn")
    await login_as(client, api, "tologch@test.mn")
    return user


async def _checkout(client: httpx.AsyncClient, api: str, months: int | None = None) -> str:
    body = None if months is None else {"months": months}
    response = await client.post(f"{api}/billing/checkout", json=body)
    assert response.status_code == 200, response.text
    return response.json()["payment_id"]


def _sign(body: bytes, *, secret: str = WEBHOOK_SECRET, timestamp: int | None = None) -> str:
    stamp = str(timestamp if timestamp is not None else int(time.time()))
    digest = hmac.new(secret.encode(), stamp.encode() + b"." + body, hashlib.sha256).hexdigest()
    return f"t={stamp},v1={digest}"


# --- Багцын төлөв ----------------------------------------------------------


async def test_free_user_has_no_plan(client: httpx.AsyncClient, api: str, db: AsyncSession) -> None:
    use_wire(wire_api())
    await _student(client, api, db)

    plan = (await client.get(f"{api}/billing/plan")).json()
    assert (plan["has_plan"], plan["plan_expires_at"], plan["price_mnt"]) == (False, None, 24_900)
    me = (await client.get(f"{api}/auth/me")).json()
    assert me["has_plan"] is False
    assert me["plan_expires_at"] is None


async def test_visitors_see_the_price(client: httpx.AsyncClient, api: str) -> None:
    seen = use_wire(wire_api())
    response = await client.get(f"{api}/billing/plan")
    assert response.status_code == 200
    plan = response.json()
    assert (plan["has_plan"], plan["plan_expires_at"], plan["price_mnt"]) == (False, None, 24_900)
    assert len(plan["options"]) == 12
    assert seen == []


async def test_every_sixth_month_is_free(client: httpx.AsyncClient, api: str) -> None:
    use_wire(wire_api())
    options = (await client.get(f"{api}/billing/plan")).json()["options"]
    by_months = {option["months"]: option for option in options}

    assert [option["months"] for option in options] == list(range(1, 13))

    def option(months: int, free: int, price: int) -> dict[str, int]:
        # Хөнгөлөлтгүй үед төлөх дүн нь үнэтэйгээ ижил.
        return {
            "months": months,
            "free_months": free,
            "price_mnt": price,
            "final_price_mnt": price,
            "credit_mnt": 0,
        }

    assert by_months[1] == option(1, 0, 24_900)
    assert by_months[5] == option(5, 0, 5 * 24_900)
    # 6 сар = 5 сарын үнэ, 12 сар = 10 сарын үнэ.
    assert by_months[6] == option(6, 1, 5 * 24_900)
    assert by_months[11] == option(11, 1, 10 * 24_900)
    assert by_months[12] == option(12, 2, 10 * 24_900)


async def test_checkout_requires_login(client: httpx.AsyncClient, api: str) -> None:
    use_wire(wire_api())
    assert (await client.post(f"{api}/billing/checkout")).status_code == 401


# --- Checkout ---------------------------------------------------------------


async def test_checkout_creates_intent_and_session(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    seen = use_wire(wire_api())
    await _student(client, api, db)

    response = await client.post(f"{api}/billing/checkout")
    assert response.status_code == 200
    body = response.json()
    assert body["checkout_url"] == "https://pay.wire.mn/c/tok"

    intent_request, session_request = seen
    assert intent_request.headers["authorization"] == "Bearer sk_test_123"
    assert intent_request.headers["idempotency-key"] == f"medleghub-pi-{body['payment_id']}"
    intent_body = json.loads(intent_request.content)
    assert intent_body["amount"] == PRICE_MNT
    assert intent_body["currency"] == "MNT"
    assert intent_body["allowed_operators"] == ["sandbox"]
    assert intent_body["metadata"]["payment_id"] == body["payment_id"]

    # Wire-ийн live API form-ийг `400 invalid_json`-оор татгалздаг — JSON байх ёстой.
    assert session_request.headers["content-type"] == "application/json"
    session_body = json.loads(session_request.content)
    assert session_body == {
        "payment_intent": "pi_1",
        "success_url": f"https://medleghub.com/billing/success?payment={body['payment_id']}",
        "cancel_url": "https://medleghub.com/pricing",
    }

    payment = await db.get(Payment, uuid.UUID(body["payment_id"]))
    assert payment is not None
    assert (payment.status, payment.provider_payment_id, payment.amount) == (
        "pending",
        "pi_1",
        PRICE_MNT,
    )


@pytest.mark.parametrize(
    ("operators", "sent"),
    [(["qpay"], ["qpay"]), (["sandbox", "qpay"], ["qpay"]), (["sandbox"], None)],
)
async def test_live_key_never_sends_sandbox(
    client: httpx.AsyncClient,
    api: str,
    db: AsyncSession,
    monkeypatch: pytest.MonkeyPatch,
    operators: list[str],
    sent: list[str] | None,
) -> None:
    """Live түлхүүр `sandbox`-ийг `operator_not_allowed`-аар татгалздаг."""
    monkeypatch.setattr(settings, "wire_secret_key", "sk_live_123")
    monkeypatch.setattr(settings, "wire_allowed_operators", operators)
    seen = use_wire(wire_api())
    await _student(client, api, db)
    await _checkout(client, api)
    assert json.loads(seen[0].content).get("allowed_operators") == sent


async def test_checkout_omits_return_urls_without_https(
    client: httpx.AsyncClient, api: str, db: AsyncSession, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Wire нь зөвхөн HTTPS буцах хаяг хүлээж авна."""
    monkeypatch.setattr(settings, "site_url", "http://localhost:3000")
    seen = use_wire(wire_api())
    await _student(client, api, db)
    await _checkout(client, api)
    assert json.loads(seen[1].content) == {"payment_intent": "pi_1"}


async def test_checkout_is_unavailable_without_keys(
    client: httpx.AsyncClient, api: str, db: AsyncSession, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(settings, "wire_secret_key", "")
    seen = use_wire(wire_api())
    await _student(client, api, db)

    response = await client.post(f"{api}/billing/checkout")
    assert response.status_code == 503
    assert response.json()["detail"]["code"] == "BILLING_NOT_CONFIGURED"
    assert seen == []


async def test_provider_failure_marks_payment_failed(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    use_wire(lambda _: httpx.Response(500, json={"error": {"code": "api_error"}}))
    await _student(client, api, db)

    response = await client.post(f"{api}/billing/checkout")
    assert response.status_code == 502
    assert response.json()["detail"]["code"] == "PAYMENT_PROVIDER_ERROR"
    statuses = (await db.execute(select(Payment.status))).scalars().all()
    assert statuses == ["failed"]


async def test_non_https_checkout_url_is_rejected(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/v1/checkout/sessions":
            return httpx.Response(200, json={"id": "cs_1", "url": "javascript:alert(1)"})
        return wire_api()(request)

    use_wire(handler)
    await _student(client, api, db)
    assert (await client.post(f"{api}/billing/checkout")).status_code == 502


# --- Төлбөр баталгаажих -----------------------------------------------------


async def test_succeeded_payment_extends_plan_once(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    use_wire(wire_api(intent_status="succeeded"))
    user = await _student(client, api, db)
    payment_id = await _checkout(client, api)

    first = (await client.get(f"{api}/billing/payments/{payment_id}")).json()
    assert first["status"] == "succeeded"
    assert first["plan"]["has_plan"] is True
    receipt = first["receipt"]
    assert {key: receipt[key] for key in ("months", "free_months", "amount_mnt")} == {
        "months": 1,
        "free_months": 0,
        "amount_mnt": PRICE_MNT,
    }
    assert (receipt["list_price_mnt"], receipt["discount_mnt"], receipt["discount_percent"]) == (
        PRICE_MNT,
        0,
        0,
    )
    assert (receipt["discount_source"], receipt["promo_code"]) == (None, None)
    assert (receipt["reference"], receipt["currency"]) == ("pi_1", "MNT")
    assert receipt["paid_at"] is not None
    expires = datetime.fromisoformat(first["plan"]["plan_expires_at"])
    assert timedelta(days=27) < expires - datetime.now(UTC) < timedelta(days=32)

    # Дахин шалгахад (буцах хуудас + webhook) сар давхар нэмэгдэхгүй.
    second = (await client.get(f"{api}/billing/payments/{payment_id}")).json()
    assert second["plan"]["plan_expires_at"] == first["plan"]["plan_expires_at"]
    await db.refresh(user)
    assert user.has_plan


async def test_yearly_payment_charges_ten_months_and_grants_twelve(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    seen = use_wire(wire_api(amount=10 * PRICE_MNT))
    await _student(client, api, db)

    payment_id = await _checkout(client, api, months=12)

    intent_body = json.loads(seen[0].content)
    assert intent_body["amount"] == 10 * PRICE_MNT
    assert intent_body["description"] == "Medleghub Standard багц — 12 сар"
    payment = await db.get(Payment, uuid.UUID(payment_id))
    assert payment is not None
    assert payment.months == 12

    body = (await client.get(f"{api}/billing/payments/{payment_id}")).json()
    assert body["status"] == "succeeded"
    expires = datetime.fromisoformat(body["plan"]["plan_expires_at"])
    assert timedelta(days=360) < expires - datetime.now(UTC) < timedelta(days=370)
    assert (body["receipt"]["months"], body["receipt"]["free_months"]) == (12, 2)
    assert body["receipt"]["amount_mnt"] == 10 * PRICE_MNT


async def test_six_months_cost_five(client: httpx.AsyncClient, api: str, db: AsyncSession) -> None:
    seen = use_wire(wire_api(amount=5 * PRICE_MNT))
    await _student(client, api, db)

    payment_id = await _checkout(client, api, months=6)

    assert json.loads(seen[0].content)["amount"] == 5 * PRICE_MNT
    body = (await client.get(f"{api}/billing/payments/{payment_id}")).json()
    expires = datetime.fromisoformat(body["plan"]["plan_expires_at"])
    assert timedelta(days=178) < expires - datetime.now(UTC) < timedelta(days=186)


@pytest.mark.parametrize("months", [0, 13, -1])
async def test_checkout_rejects_invalid_months(
    client: httpx.AsyncClient, api: str, db: AsyncSession, months: int
) -> None:
    seen = use_wire(wire_api())
    await _student(client, api, db)

    response = await client.post(f"{api}/billing/checkout", json={"months": months})

    assert response.status_code == 422
    assert seen == []


async def test_payment_extends_from_current_expiry(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    use_wire(wire_api())
    user = await _student(client, api, db)
    current = datetime.now(UTC) + timedelta(days=10)
    user.plan_expires_at = current
    await db.commit()

    payment_id = await _checkout(client, api)
    body = (await client.get(f"{api}/billing/payments/{payment_id}")).json()
    extended = datetime.fromisoformat(body["plan"]["plan_expires_at"])
    assert timedelta(days=27) < extended - current < timedelta(days=32)


async def test_pending_and_canceled_intents_grant_nothing(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    use_wire(wire_api(intent_status="requires_payment_method"))
    await _student(client, api, db)
    payment_id = await _checkout(client, api)

    pending = (await client.get(f"{api}/billing/payments/{payment_id}")).json()
    assert (pending["status"], pending["plan"]["has_plan"]) == ("pending", False)
    # Баримт зөвхөн амжилттай төлбөрт.
    assert pending["receipt"] is None

    use_wire(wire_api(intent_status="canceled"))
    canceled = (await client.get(f"{api}/billing/payments/{payment_id}")).json()
    assert (canceled["status"], canceled["plan"]["has_plan"]) == ("canceled", False)
    assert canceled["receipt"] is None


async def test_amount_mismatch_is_not_honoured(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    use_wire(wire_api(amount=100))
    await _student(client, api, db)
    payment_id = await _checkout(client, api)

    body = (await client.get(f"{api}/billing/payments/{payment_id}")).json()
    assert (body["status"], body["plan"]["has_plan"]) == ("failed", False)


async def test_other_users_payment_is_not_found(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    use_wire(wire_api())
    await _student(client, api, db)
    payment_id = await _checkout(client, api)

    await make_user(db, "busad@test.mn")
    await login_as(client, api, "busad@test.mn")
    response = await client.get(f"{api}/billing/payments/{payment_id}")
    assert response.status_code == 404


async def test_plan_endpoint_picks_up_a_recent_payment(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    """Webhook, буцах хаяггүй үед ч `/pricing` руу буцахад төлбөр бүртгэгдэнэ."""
    use_wire(wire_api(intent_status="succeeded"))
    await _student(client, api, db)
    await _checkout(client, api)

    plan = (await client.get(f"{api}/billing/plan")).json()
    assert plan["has_plan"] is True


# --- Webhook ----------------------------------------------------------------


async def test_signed_webhook_applies_payment(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    use_wire(wire_api(intent_status="succeeded"))
    user = await _student(client, api, db)
    await _checkout(client, api)

    body = json.dumps(
        {"id": "evt_1", "type": "payment_intent.succeeded", "data": {"object": {"id": "pi_1"}}}
    ).encode()
    response = await client.post(
        f"{api}/billing/webhooks/wire",
        content=body,
        headers={"WirePayment-Signature": _sign(body), "content-type": "application/json"},
    )
    assert response.status_code == 200
    await db.refresh(user)
    assert user.has_plan


async def test_webhook_rejects_bad_signatures(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    use_wire(wire_api())
    body = b'{"type": "payment_intent.succeeded", "data": {"id": "pi_1"}}'

    for header in (
        None,
        _sign(body, secret="whsec_wrong"),
        _sign(body, timestamp=int(time.time()) - 3600),
        _sign(body + b" "),
    ):
        headers = {"WirePayment-Signature": header} if header else {}
        response = await client.post(f"{api}/billing/webhooks/wire", content=body, headers=headers)
        assert response.status_code == 400
        assert response.json()["detail"]["code"] == "INVALID_SIGNATURE"


async def test_webhook_acknowledges_verification_ping(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    seen = use_wire(wire_api())
    body = b'{"id": "evt_0", "type": "endpoint.verification", "data": {}}'
    response = await client.post(
        f"{api}/billing/webhooks/wire", content=body, headers={"WirePayment-Signature": _sign(body)}
    )
    assert response.status_code == 200
    assert seen == []


# --- Админ гараар олгох -----------------------------------------------------


async def test_admin_can_grant_a_plan(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    use_wire(wire_api())
    student = await make_user(db, "suragch@test.mn")
    await make_user(db, "admin@test.mn", role=UserRole.ADMIN)
    await login_as(client, api, "admin@test.mn")

    response = await client.post(
        f"{api}/billing/grants", json={"email": "Suragch@Test.mn", "months": 2}
    )
    assert response.status_code == 200
    assert response.json()["has_plan"] is True
    await db.refresh(student)
    assert student.plan_expires_at is not None
    assert student.plan_expires_at - datetime.now(UTC) > timedelta(days=55)

    missing = await client.post(f"{api}/billing/grants", json={"email": "baihgui@test.mn"})
    assert missing.status_code == 404


async def _admin_and_student(
    client: httpx.AsyncClient, api: str, db: AsyncSession, *, months_left: int | None = None
) -> User:
    """Админаар нэвтэрсэн, `months_left` сар (≈30 хоног) үлдсэн сурагч."""
    use_wire(wire_api())
    student = await make_user(db, "suragch@test.mn")
    if months_left is not None:
        student.plan_expires_at = datetime.now(UTC) + timedelta(days=30 * months_left)
        await db.commit()
    admin = await make_user(db, "admin@test.mn", role=UserRole.ADMIN)
    admin.name = "Админ Бат"
    await db.commit()
    await login_as(client, api, "admin@test.mn")
    return student


async def _adjust(
    client: httpx.AsyncClient, api: str, months: int, note: str | None = None
) -> httpx.Response:
    return await client.post(
        f"{api}/billing/grants",
        json={"email": "suragch@test.mn", "months": months, "note": note},
    )


async def test_admin_grant_is_recorded_with_who_and_why(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    await _admin_and_student(client, api, db)

    response = await _adjust(client, api, 3, note="  Урамшуулал  ")
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["email"] == "suragch@test.mn"
    assert body["has_plan"] is True
    [adjustment] = body["adjustments"]
    assert adjustment["months"] == 3
    assert adjustment["expires_before"] is None
    assert adjustment["expires_after"] == body["plan_expires_at"]
    assert adjustment["note"] == "Урамшуулал"
    assert adjustment["admin_name"] == "Админ Бат"


async def test_admin_removes_months_from_an_active_plan(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    student = await _admin_and_student(client, api, db, months_left=3)
    before = student.plan_expires_at
    assert before is not None

    response = await _adjust(client, api, -1)
    assert response.status_code == 200, response.text
    await db.refresh(student)
    assert student.plan_expires_at is not None
    # Сарын урт 28–31 хоног.
    assert timedelta(days=28) <= before - student.plan_expires_at <= timedelta(days=31)
    assert student.has_plan

    adjustment = response.json()["adjustments"][0]
    assert adjustment["months"] == -1
    assert datetime.fromisoformat(adjustment["expires_before"]) == before


async def test_removing_more_than_is_left_ends_the_plan_now(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    student = await _admin_and_student(client, api, db, months_left=1)

    response = await _adjust(client, api, -6)
    assert response.status_code == 200, response.text
    assert response.json()["has_plan"] is False
    await db.refresh(student)
    assert student.plan_expires_at is not None
    # Өнгөрсөн огноо биш — яг одоо дууссан.
    assert abs(student.plan_expires_at - datetime.now(UTC)) < timedelta(minutes=1)
    assert not student.has_plan

    # Дахин нэмбэл одооноос сунгана.
    again = await _adjust(client, api, 1)
    assert again.json()["has_plan"] is True


async def test_cannot_remove_months_without_an_active_plan(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    student = await _admin_and_student(client, api, db)
    student.plan_expires_at = datetime.now(UTC) - timedelta(days=3)
    await db.commit()

    response = await _adjust(client, api, -1)
    assert response.status_code == 409
    assert response.json()["detail"]["code"] == "NO_ACTIVE_PLAN"

    lookup = await client.post(f"{api}/billing/grants/lookup", json={"email": "suragch@test.mn"})
    assert lookup.json()["adjustments"] == []


@pytest.mark.parametrize("months", [0, 25, -25])
async def test_grant_months_must_be_in_range(
    client: httpx.AsyncClient, api: str, db: AsyncSession, months: int
) -> None:
    await _admin_and_student(client, api, db, months_left=2)
    response = await _adjust(client, api, months)
    assert response.status_code == 422


async def test_admin_looks_up_a_plan_with_newest_changes_first(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    await _admin_and_student(client, api, db)
    await _adjust(client, api, 2)
    await _adjust(client, api, -1, note="Буцаалт")

    response = await client.post(
        f"{api}/billing/grants/lookup", json={"email": " Suragch@Test.mn "}
    )
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["name"] == "Тест"
    assert body["has_plan"] is True
    assert [item["months"] for item in body["adjustments"]] == [-1, 2]
    assert body["adjustments"][0]["note"] == "Буцаалт"

    missing = await client.post(f"{api}/billing/grants/lookup", json={"email": "baihgui@test.mn"})
    assert missing.status_code == 404


async def test_history_survives_the_admin_but_not_the_user(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    student = await _admin_and_student(client, api, db)
    await _adjust(client, api, 1)

    admin = (await db.execute(select(User).where(User.email == "admin@test.mn"))).scalar_one()
    await db.delete(admin)
    await db.commit()
    other_admin = await make_user(db, "admin2@test.mn", role=UserRole.ADMIN)
    assert other_admin.is_admin
    await login_as(client, api, "admin2@test.mn")

    lookup = await client.post(f"{api}/billing/grants/lookup", json={"email": "suragch@test.mn"})
    [adjustment] = lookup.json()["adjustments"]
    assert adjustment["admin_name"] is None

    await db.delete(student)
    await db.commit()
    assert (await db.execute(select(PlanAdjustment))).scalars().all() == []


async def test_students_cannot_grant_plans(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    use_wire(wire_api())
    await _student(client, api, db)
    response = await client.post(f"{api}/billing/grants", json={"email": "tologch@test.mn"})
    assert response.status_code == 403
    removed = await client.post(
        f"{api}/billing/grants", json={"email": "tologch@test.mn", "months": -1}
    )
    assert removed.status_code == 403
    lookup = await client.post(f"{api}/billing/grants/lookup", json={"email": "tologch@test.mn"})
    assert lookup.status_code == 403


async def test_anonymous_cannot_look_up_plans(client: httpx.AsyncClient, api: str) -> None:
    use_wire(wire_api())
    response = await client.post(f"{api}/billing/grants/lookup", json={"email": "a@test.mn"})
    assert response.status_code == 401


# --- Сарын үнийг админ өөрчлөх ------------------------------------------------


async def test_admin_changes_the_monthly_price(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    seen = use_wire(wire_api(amount=19_900))
    await make_user(db, "admin@test.mn", role=UserRole.ADMIN)
    await login_as(client, api, "admin@test.mn")

    before = (await client.get(f"{api}/billing/price")).json()
    assert before == {
        "price_mnt": 24_900,
        "default_price_mnt": 24_900,
        "changed_at": None,
        "changed_by": None,
        "premium_price_mnt": 39_900,
        "premium_default_price_mnt": 39_900,
        "premium_changed_at": None,
        "premium_changed_by": None,
        "live_pass_price_mnt": 4_900,
        "live_pass_default_price_mnt": 4_900,
        "live_pass_changed_at": None,
        "live_pass_changed_by": None,
    }

    response = await client.put(f"{api}/billing/price", json={"price_mnt": 19_900})
    assert response.status_code == 200, response.text
    changed = response.json()
    assert (changed["price_mnt"], changed["default_price_mnt"]) == (19_900, 24_900)
    assert changed["changed_at"] is not None
    assert changed["changed_by"] == "Тест"

    # Олон сарын үнэ, үнэгүй сар шинэ үнээр дахин тооцогдоно.
    plan = (await client.get(f"{api}/billing/plan")).json()
    assert plan["price_mnt"] == 19_900
    totals = {option["months"]: option["price_mnt"] for option in plan["options"]}
    assert (totals[1], totals[6], totals[12]) == (19_900, 5 * 19_900, 10 * 19_900)

    # Нэхэмжлэх шинэ үнээр үүснэ.
    payment_id = await _checkout(client, api, 1)
    assert json.loads(seen[0].content)["amount"] == 19_900
    payment = await db.get(Payment, uuid.UUID(payment_id))
    assert payment is not None
    assert payment.amount == 19_900


async def test_latest_price_wins_and_visitors_see_it(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    use_wire(wire_api())
    db.add(PlanPrice(price_mnt=29_900, created_at=datetime.now(UTC) - timedelta(days=1)))
    db.add(PlanPrice(price_mnt=14_900))
    await db.commit()

    plan = (await client.get(f"{api}/billing/plan")).json()
    assert plan["price_mnt"] == 14_900
    assert plan["options"][11]["price_mnt"] == 10 * 14_900


@pytest.mark.parametrize("price", [0, 99, 1_000_001, -5])
async def test_price_must_be_sensible(
    client: httpx.AsyncClient, api: str, db: AsyncSession, price: int
) -> None:
    await make_user(db, "admin@test.mn", role=UserRole.ADMIN)
    await login_as(client, api, "admin@test.mn")
    response = await client.put(f"{api}/billing/price", json={"price_mnt": price})
    assert response.status_code == 422


async def test_only_admins_see_or_change_the_price(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    assert (await client.get(f"{api}/billing/price")).status_code == 401
    assert (await client.put(f"{api}/billing/price", json={"price_mnt": 100})).status_code == 401

    await _student(client, api, db)
    assert (await client.get(f"{api}/billing/price")).status_code == 403
    assert (await client.put(f"{api}/billing/price", json={"price_mnt": 100})).status_code == 403


# --- Premium ----------------------------------------------------------------------


async def test_premium_is_sold_only_when_live_is_open(
    client: httpx.AsyncClient, api: str, db: AsyncSession, monkeypatch: pytest.MonkeyPatch
) -> None:
    use_wire(wire_api(amount=39_900))
    monkeypatch.setattr(settings, "live_access", "admins")
    visitor = (await client.get(f"{api}/billing/plan")).json()
    assert visitor["premium_available"] is False
    assert visitor["premium_options"] == []
    await make_user(db, "student@test.mn")
    await login_as(client, api, "student@test.mn")
    blocked = await client.post(f"{api}/billing/checkout", json={"months": 1, "plan": "premium"})
    assert blocked.status_code == 409
    assert blocked.json()["detail"]["code"] == "PREMIUM_NOT_AVAILABLE"

    monkeypatch.setattr(settings, "live_access", "all")
    plan = (await client.get(f"{api}/billing/plan")).json()
    assert plan["premium_available"] is True
    assert plan["premium_price_mnt"] == 39_900
    totals = {option["months"]: option["price_mnt"] for option in plan["premium_options"]}
    assert (totals[1], totals[6], totals[12]) == (39_900, 5 * 39_900, 10 * 39_900)
    assert plan["has_premium"] is False


async def test_premium_payment_extends_standard_and_premium(
    client: httpx.AsyncClient, api: str, db: AsyncSession, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(settings, "live_access", "all")
    wire = install_fake_wire(monkeypatch)
    user = await make_user(db, "premium@test.mn")
    user_id = user.id
    await login_as(client, api, "premium@test.mn")
    response = await client.post(f"{api}/billing/checkout", json={"months": 1, "plan": "premium"})
    assert response.status_code == 200, response.text
    assert wire.last_amount == 39_900
    assert "Premium" in list(wire.descriptions.values())[-1]
    payment_id = response.json()["payment_id"]

    status = (await client.get(f"{api}/billing/payments/{payment_id}")).json()
    assert status["status"] == "succeeded"
    assert status["receipt"]["plan"] == "premium"
    assert status["plan"]["has_plan"] is True
    assert status["plan"]["has_premium"] is True
    db.expire_all()
    stored = await db.get(User, user_id)
    subscription = await db.get(LiveSubscription, user_id)
    assert stored is not None and subscription is not None
    assert subscription.tier == "premium"
    # Нэг сар: Standard ба Premium хоёулаа ~1 сарын дараа дуусна.
    assert abs((stored.plan_expires_at - subscription.expires_at).total_seconds()) < 60

    # Live-ийн эрх Premium болсон.
    config = (await client.get(f"{api}/live/config")).json()
    assert config["tier"] == "premium"

    # Дахин авахад хоёулаа дуусах өдрөөсөө сунгагдана; давхар хэрэглэхгүй.
    before = subscription.expires_at
    second = (
        await client.post(f"{api}/billing/checkout", json={"months": 1, "plan": "premium"})
    ).json()
    await client.get(f"{api}/billing/payments/{second['payment_id']}")
    await client.get(f"{api}/billing/payments/{second['payment_id']}")
    db.expire_all()
    subscription = await db.get(LiveSubscription, user_id)
    assert subscription is not None
    gained = subscription.expires_at - before
    assert timedelta(days=27) < gained < timedelta(days=32)


async def test_standard_payment_does_not_grant_premium(
    client: httpx.AsyncClient, api: str, db: AsyncSession, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(settings, "live_access", "all")
    use_wire(wire_api())
    user = await make_user(db, "standard@test.mn")
    await login_as(client, api, "standard@test.mn")
    payment_id = await _checkout(client, api, 1)
    status = (await client.get(f"{api}/billing/payments/{payment_id}")).json()
    assert status["receipt"]["plan"] == "standard"
    assert status["plan"]["has_premium"] is False
    assert await db.get(LiveSubscription, user.id) is None


async def test_premium_price_is_separate_and_promo_applies(
    client: httpx.AsyncClient, api: str, db: AsyncSession, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(settings, "live_access", "all")
    seen = use_wire(wire_api(amount=34_000 - 34_000 * 20 // 100))
    await make_user(db, "boss@test.mn", role=UserRole.ADMIN)
    await login_as(client, api, "boss@test.mn")
    changed = await client.put(
        f"{api}/billing/price", json={"price_mnt": 34_000, "plan": "premium"}
    )
    assert changed.status_code == 200, changed.text
    assert changed.json()["premium_price_mnt"] == 34_000
    assert changed.json()["price_mnt"] == 24_900
    db.add(PromoCode(code="SAVE20", kind="percent", percent_off=20))
    await db.commit()

    await make_user(db, "buyer@test.mn")
    await login_as(client, api, "buyer@test.mn")
    plan = (await client.get(f"{api}/billing/plan")).json()
    assert plan["price_mnt"] == 24_900
    assert plan["premium_price_mnt"] == 34_000
    preview = (await client.post(f"{api}/billing/promo/check", json={"code": "SAVE20"})).json()
    assert preview["premium_options"][0]["final_price_mnt"] == 27_200
    response = await client.post(
        f"{api}/billing/checkout", json={"months": 1, "plan": "premium", "promo_code": "SAVE20"}
    )
    assert response.status_code == 200, response.text
    assert json.loads(seen[0].content)["amount"] == 27_200


# --- Нэг удаагийн Live эрх ---------------------------------------------------------

PASS_MNT = 4_900


async def _buy_pass(client: httpx.AsyncClient, api: str) -> dict:
    response = await client.post(f"{api}/billing/checkout", json={"plan": "live_pass"})
    assert response.status_code == 200, response.text
    return await pay(client, api, response.json()["payment_id"])


async def test_live_pass_is_sold_only_when_live_is_open(
    client: httpx.AsyncClient, api: str, db: AsyncSession, monkeypatch: pytest.MonkeyPatch
) -> None:
    install_fake_wire(monkeypatch)
    monkeypatch.setattr(settings, "live_access", "admins")
    visitor = (await client.get(f"{api}/billing/plan")).json()
    assert visitor["live_pass_available"] is False
    await make_user(db, "student@test.mn")
    await login_as(client, api, "student@test.mn")
    blocked = await client.post(f"{api}/billing/checkout", json={"plan": "live_pass"})
    assert blocked.status_code == 409
    assert blocked.json()["detail"]["code"] == "LIVE_PASS_NOT_AVAILABLE"

    # Нэвтрээгүй зочин ч үнэ, нөхцөлийг харна (`/pricing`, `/live`).
    monkeypatch.setattr(settings, "live_access", "all")
    await client.post(f"{api}/auth/logout")
    visitor = (await client.get(f"{api}/billing/plan")).json()
    assert visitor["live_pass_available"] is True
    assert visitor["live_pass_price_mnt"] == PASS_MNT
    assert (visitor["live_pass_access_days"], visitor["live_pass_upgrade_days"]) == (30, 7)


async def test_live_pass_purchase_then_upgrade_within_seven_days(
    client: httpx.AsyncClient, api: str, db: AsyncSession, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Эрх нь багцыг сунгахгүй; 7 хоногийн дотор Standard авбал эрхийн үнэ хасагдана."""
    monkeypatch.setattr(settings, "live_access", "all")
    wire = install_fake_wire(monkeypatch)
    user = await make_user(db, "pass@test.mn")
    user_id = user.id
    await login_as(client, api, "pass@test.mn")

    status = await _buy_pass(client, api)
    assert wire.last_amount == PASS_MNT
    assert list(wire.descriptions.values())[-1] == "Medleghub Live — нэг удаагийн эрх"
    receipt = status["receipt"]
    assert (receipt["plan"], receipt["months"], receipt["free_months"]) == ("live_pass", 0, 0)
    assert (receipt["amount_mnt"], receipt["list_price_mnt"], receipt["credit_mnt"]) == (
        PASS_MNT,
        PASS_MNT,
        0,
    )
    plan = status["plan"]
    assert (plan["has_plan"], plan["has_unused_live_pass"]) == (False, True)
    credit = plan["upgrade_credit"]
    assert credit["amount_mnt"] == PASS_MNT
    left = datetime.fromisoformat(credit["expires_at"]) - datetime.now(UTC)
    assert timedelta(days=6, hours=23) < left <= timedelta(days=7)
    first = plan["options"][0]
    assert (first["price_mnt"], first["final_price_mnt"], first["credit_mnt"]) == (
        PRICE_MNT,
        PRICE_MNT - PASS_MNT,
        PASS_MNT,
    )
    db.expire_all()
    stored = await db.get(User, user_id)
    assert stored is not None and stored.plan_expires_at is None
    [live_pass] = (await db.execute(select(LivePass))).scalars().all()
    assert (live_pass.user_id, live_pass.price_mnt, live_pass.used_at) == (user_id, PASS_MNT, None)
    pass_id = live_pass.id
    payment = (await db.execute(select(Payment))).scalar_one()
    assert (payment.months, payment.live_pass_id) == (0, pass_id)

    # Ашиглаагүй эрх байхад дахин авахгүй; промо код эрхэд хамаарахгүй.
    again = await client.post(f"{api}/billing/checkout", json={"plan": "live_pass"})
    assert again.json()["detail"]["code"] == "LIVE_PASS_UNUSED"
    promo = await client.post(
        f"{api}/billing/checkout", json={"plan": "live_pass", "promo_code": "SAVE20"}
    )
    assert promo.json()["detail"]["code"] == "PROMO_NOT_FOR_LIVE_PASS"

    response = await client.post(f"{api}/billing/checkout", json={"months": 1})
    assert response.status_code == 200, response.text
    assert wire.last_amount == PRICE_MNT - PASS_MNT
    assert list(wire.descriptions.values())[-1] == (
        "Medleghub Standard багц — 1 сар (нэг удаагийн эрхийн 4,900₮ хасагдсан)"
    )
    status = await pay(client, api, response.json()["payment_id"])
    receipt = status["receipt"]
    assert (receipt["amount_mnt"], receipt["list_price_mnt"], receipt["credit_mnt"]) == (
        PRICE_MNT - PASS_MNT,
        PRICE_MNT,
        PASS_MNT,
    )
    plan = status["plan"]
    assert plan["has_plan"] is True
    # Ашиглаагүй эрхийн үнэ багцад шилжсэн — дахин ашиглагдахгүй, хасалт ч дахин орохгүй.
    assert (plan["has_unused_live_pass"], plan["upgrade_credit"]) == (False, None)
    assert plan["options"][0]["final_price_mnt"] == PRICE_MNT
    db.expire_all()
    upgraded = await db.get(LivePass, pass_id)
    assert upgraded is not None and upgraded.upgraded_at is not None

    # Багцтай хэрэглэгчид Live багтсан — эрх зарахгүй.
    has_plan = await client.post(f"{api}/billing/checkout", json={"plan": "live_pass"})
    assert has_plan.json()["detail"]["code"] == "LIVE_PASS_HAS_PLAN"


async def test_live_pass_credit_ends_but_the_pass_stays(
    client: httpx.AsyncClient, api: str, db: AsyncSession, monkeypatch: pytest.MonkeyPatch
) -> None:
    """7 хоногийн дараа хасалт дуусна. Ашиглаагүй эрх хугацаагүй хэвээр."""
    monkeypatch.setattr(settings, "live_access", "all")
    wire = install_fake_wire(monkeypatch)
    await make_user(db, "late@test.mn")
    await login_as(client, api, "late@test.mn")
    await _buy_pass(client, api)
    await db.execute(
        update(LivePass).values(created_at=datetime.now(UTC) - timedelta(days=7, minutes=1))
    )
    await db.commit()

    plan = (await client.get(f"{api}/billing/plan")).json()
    assert plan["upgrade_credit"] is None
    assert plan["options"][0]["final_price_mnt"] == PRICE_MNT
    assert plan["has_unused_live_pass"] is True
    await pay(client, api, await _checkout(client, api, 1))
    assert wire.last_amount == PRICE_MNT
    db.expire_all()
    [live_pass] = (await db.execute(select(LivePass))).scalars().all()
    assert live_pass.upgraded_at is None


async def test_live_pass_credit_applies_after_a_promo_code(
    client: httpx.AsyncClient, api: str, db: AsyncSession, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(settings, "live_access", "all")
    wire = install_fake_wire(monkeypatch)
    db.add(PromoCode(code="SAVE20", kind="percent", percent_off=20))
    await make_user(db, "promo@test.mn")
    await login_as(client, api, "promo@test.mn")
    await _buy_pass(client, api)

    discounted = PRICE_MNT - PRICE_MNT * 20 // 100
    preview = (await client.post(f"{api}/billing/promo/check", json={"code": "SAVE20"})).json()
    assert preview["options"][0]["final_price_mnt"] == discounted - PASS_MNT
    response = await client.post(
        f"{api}/billing/checkout", json={"months": 1, "promo_code": "SAVE20"}
    )
    assert response.status_code == 200, response.text
    assert wire.last_amount == discounted - PASS_MNT
    receipt = (await pay(client, api, response.json()["payment_id"]))["receipt"]
    assert (receipt["discount_mnt"], receipt["credit_mnt"], receipt["list_price_mnt"]) == (
        PRICE_MNT - discounted,
        PASS_MNT,
        PRICE_MNT,
    )


async def test_admin_sets_the_live_pass_price(
    client: httpx.AsyncClient, api: str, db: AsyncSession, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(settings, "live_access", "all")
    wire = install_fake_wire(monkeypatch)
    await make_user(db, "boss@test.mn", role=UserRole.ADMIN)
    await login_as(client, api, "boss@test.mn")
    changed = await client.put(
        f"{api}/billing/price", json={"price_mnt": 5_900, "plan": "live_pass"}
    )
    assert changed.status_code == 200, changed.text
    body = changed.json()
    assert (body["live_pass_price_mnt"], body["price_mnt"], body["premium_price_mnt"]) == (
        5_900,
        24_900,
        39_900,
    )

    await make_user(db, "buyer@test.mn")
    await login_as(client, api, "buyer@test.mn")
    assert (await client.get(f"{api}/billing/plan")).json()["live_pass_price_mnt"] == 5_900
    status = await _buy_pass(client, api)
    assert wire.last_amount == 5_900
    # Хасалт нь бодитоор төлсөн дүн.
    assert status["plan"]["upgrade_credit"]["amount_mnt"] == 5_900
