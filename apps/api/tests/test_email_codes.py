"""Имэйлийн код (Supabase Auth) — бүртгэл баталгаажуулах, нууц үг сэргээх,
насны зөвшөөрөл, өөрийн бүртгэлийг удирдах.

Supabase Auth-ийг `httpx.MockTransport`-оор орлуулна — жинхэнэ имэйл илгээхгүй.
"""

import json
from collections.abc import AsyncGenerator
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta

import httpx
import pytest
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.rate_limit import InMemoryRateLimitBackend
from app.main import app
from app.models.enrollment import Enrollment
from app.models.feedback import Feedback
from app.models.payment import Payment
from app.models.user import User
from app.services import account_service
from app.services.email_otp import get_auth_client
from tests.conftest import TEST_PASSWORD, login_as, make_user
from tests.factories import make_course_with_lessons

GOOD_CODE = "123456"
EMAIL = "shine@suralts.mn"
ADULT = {"name": "Шинэ", "password": "Nuuts12345", "is_16_or_older": True, "accept_terms": True}


@dataclass
class FakeSupabase:
    """`/otp` илгээсэн имэйлийг бүртгэж, `/verify` зөвхөн GOOD_CODE-ийг хүлээн авна."""

    sent: list[str] = field(default_factory=list)
    deleted: list[str] = field(default_factory=list)
    users: dict[str, str] = field(default_factory=dict)  # email -> id
    status: int = 200

    def handle(self, request: httpx.Request) -> httpx.Response:
        assert request.headers["apikey"]
        path = request.url.path.removeprefix("/auth/v1")
        if self.status != 200:
            return httpx.Response(self.status, json={"error_code": "boom"})
        if request.method == "POST" and path == "/otp":
            email = json.loads(request.content)["email"]
            self.sent.append(email)
            self.users.setdefault(email, f"id-{len(self.users)}")
            return httpx.Response(200, json={})
        if request.method == "POST" and path == "/verify":
            body = json.loads(request.content)
            assert body["type"] == "email"
            if body["token"] == GOOD_CODE and body["email"] in self.sent:
                return httpx.Response(200, json={"access_token": "ignored", "user": {}})
            return httpx.Response(403, json={"error_code": "otp_expired"})
        if request.method == "GET" and path == "/admin/users":
            assert request.headers["apikey"] == "service-key"
            wanted = request.url.params["filter"]
            found = [{"id": uid, "email": e} for e, uid in self.users.items() if wanted in e]
            return httpx.Response(200, json={"users": found})
        if request.method == "DELETE" and path.startswith("/admin/users/"):
            uid = path.rsplit("/", 1)[1]
            email = next(e for e, i in self.users.items() if i == uid)
            self.deleted.append(email)
            del self.users[email]
            return httpx.Response(200, json={})
        return httpx.Response(404)


@pytest.fixture
def supabase(monkeypatch: pytest.MonkeyPatch) -> FakeSupabase:
    monkeypatch.setattr(settings, "supabase_url", "https://project.supabase.test")
    monkeypatch.setattr(settings, "supabase_anon_key", "anon-key")
    monkeypatch.setattr(settings, "supabase_service_role_key", "service-key")
    fake = FakeSupabase()

    async def override() -> AsyncGenerator[httpx.AsyncClient, None]:
        async with httpx.AsyncClient(
            transport=httpx.MockTransport(fake.handle),
            base_url="https://project.supabase.test/auth/v1",
        ) as client:
            yield client

    app.dependency_overrides[get_auth_client] = override
    return fake


async def _register(client: httpx.AsyncClient, api: str, **overrides: object) -> httpx.Response:
    return await client.post(f"{api}/auth/register", json={"email": EMAIL, **ADULT, **overrides})


# --- Бүртгэл ба зөвшөөрөл -------------------------------------------------------


@pytest.mark.parametrize(
    ("overrides", "drop"),
    [
        ({"accept_terms": False}, ()),
        ({"is_16_or_older": False}, ()),
        # 14–15 насны хуучин урсгал хасагдсан — насаа батлаагүй хүсэлт 422.
        ({"age_group": "under_16", "guardian_consent": True}, ("is_16_or_older",)),
    ],
)
async def test_register_requires_terms_and_age_16(
    client: httpx.AsyncClient, api: str, overrides: dict, drop: tuple[str, ...]
) -> None:
    payload = {"email": EMAIL, **ADULT, **overrides}
    for key in drop:
        payload.pop(key)
    response = await client.post(f"{api}/auth/register", json=payload)
    assert response.status_code == 422, response.text


async def test_register_records_terms_and_keeps_profile_visible(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    response = await _register(client, api)
    assert response.status_code == 201, response.text
    assert response.json()["user"]["profile_hidden"] is False

    user = (await db.execute(select(User).where(User.email == EMAIL))).scalar_one()
    assert user.terms_accepted_at is not None
    assert user.guardian_consent_at is None


async def test_register_sends_code_and_login_waits_for_it(
    client: httpx.AsyncClient, api: str, supabase: FakeSupabase
) -> None:
    response = await _register(client, api)

    assert response.status_code == 201, response.text
    assert response.json() == {"verification_required": True, "email": EMAIL, "user": None}
    assert settings.auth_cookie_name not in response.cookies
    assert supabase.sent == [EMAIL]

    login = await client.post(f"{api}/auth/login", json={"email": EMAIL, "password": "Nuuts12345"})
    assert login.status_code == 403
    assert login.json()["detail"]["code"] == "EMAIL_NOT_VERIFIED"
    # Нууц үг буруу бол баталгаажаагүй гэдгийг ч хэлэхгүй.
    wrong = await client.post(f"{api}/auth/login", json={"email": EMAIL, "password": "Buruu12345"})
    assert wrong.status_code == 401

    bad = await client.post(f"{api}/auth/verify-email", json={"email": EMAIL, "code": "000000"})
    assert bad.json()["detail"]["code"] == "INVALID_CODE"

    good = await client.post(f"{api}/auth/verify-email", json={"email": EMAIL, "code": GOOD_CODE})
    assert good.status_code == 200, good.text
    assert settings.auth_cookie_name in good.cookies
    assert (await client.get(f"{api}/auth/me")).json()["email"] == EMAIL

    again = await client.post(f"{api}/auth/verify-email", json={"email": EMAIL, "code": GOOD_CODE})
    assert again.json()["detail"]["code"] == "ALREADY_VERIFIED"


async def test_existing_email_cannot_be_registered_again(
    client: httpx.AsyncClient, api: str, supabase: FakeSupabase
) -> None:
    """Баталгаажаагүй бүртгэлийг ч дарж бичихгүй — эс бөгөөс өөр хүн эзний
    имэйлээр нууц үгээ тавьж болно."""
    assert (await _register(client, api)).status_code == 201
    response = await _register(client, api, password="Busad12345")
    assert response.status_code == 409
    assert supabase.sent == [EMAIL]


async def test_resend_only_for_unverified_accounts(
    client: httpx.AsyncClient, api: str, db: AsyncSession, supabase: FakeSupabase
) -> None:
    await make_user(db, "batalgaajsan@test.mn")
    await _register(client, api)

    for email in ("baihgui@test.mn", "batalgaajsan@test.mn", EMAIL):
        response = await client.post(f"{api}/auth/verify-email/resend", json={"email": email})
        assert response.status_code == 200

    assert supabase.sent == [EMAIL, EMAIL]


async def test_code_attempts_are_limited_per_email(
    client: httpx.AsyncClient, api: str, supabase: FakeSupabase, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(settings, "rate_limit_enabled", True)
    monkeypatch.setattr(settings, "auth_rate_limit_max", 100)
    monkeypatch.setattr("app.core.rate_limit.backend", InMemoryRateLimitBackend())
    await _register(client, api)

    statuses = [
        (
            await client.post(f"{api}/auth/verify-email", json={"email": EMAIL, "code": "111111"})
        ).status_code
        for _ in range(settings.otp_verify_rate_limit_max + 1)
    ]

    assert statuses[-1] == 429
    assert set(statuses[:-1]) == {400}


async def test_supabase_email_limit_is_a_logged_429(
    client: httpx.AsyncClient,
    api: str,
    supabase: FakeSupabase,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Supabase-ийн өөрийн хязгаарыг манай хязгаарлагчаас лог-оор ялгана."""
    supabase.status = 429
    with caplog.at_level("WARNING", logger="app.services.email_otp"):
        response = await _register(client, api)
    assert response.status_code == 429
    assert response.json()["detail"]["code"] == "RATE_LIMITED"
    assert "Supabase /otp → 429 boom" in caplog.text


async def test_supabase_outage_is_a_502(
    client: httpx.AsyncClient, api: str, supabase: FakeSupabase
) -> None:
    supabase.status = 500
    response = await _register(client, api)
    assert response.status_code == 502
    assert response.json()["detail"]["code"] == "EMAIL_PROVIDER_ERROR"


# --- Нууц үг сэргээх -------------------------------------------------------------


async def test_forgot_and_reset_password(
    client: httpx.AsyncClient, api: str, db: AsyncSession, supabase: FakeSupabase
) -> None:
    await make_user(db, EMAIL)
    await login_as(client, api, EMAIL)
    old_cookie = client.cookies.get(settings.auth_cookie_name)

    for email in ("baihgui@test.mn", EMAIL):
        response = await client.post(f"{api}/auth/password/forgot", json={"email": email})
        assert response.status_code == 200
    assert supabase.sent == [EMAIL]

    reset = {"email": EMAIL, "code": "999999", "new_password": "Shine12345"}
    bad = await client.post(f"{api}/auth/password/reset", json=reset)
    assert bad.json()["detail"]["code"] == "INVALID_CODE"

    good = await client.post(f"{api}/auth/password/reset", json={**reset, "code": GOOD_CODE})
    assert good.status_code == 200, good.text

    # Өмнөх сесс хүчингүй, шинэ нууц үгээр нэвтэрнэ.
    client.cookies.clear()
    stale = await client.get(f"{api}/auth/me", headers={"Authorization": f"Bearer {old_cookie}"})
    assert stale.status_code == 401
    login = await client.post(f"{api}/auth/login", json={"email": EMAIL, "password": "Shine12345"})
    assert login.status_code == 200


async def test_reset_also_verifies_an_unverified_account(
    client: httpx.AsyncClient, api: str, supabase: FakeSupabase
) -> None:
    """Эзэн нь баталгаажуулаагүй бүртгэлээ «Нууц үгээ мартсан»-аар сэргээнэ."""
    await _register(client, api)
    reset = {"email": EMAIL, "code": GOOD_CODE, "new_password": "Minii12345"}
    assert (await client.post(f"{api}/auth/password/reset", json=reset)).status_code == 200
    login = await client.post(f"{api}/auth/login", json={"email": EMAIL, "password": "Minii12345"})
    assert login.status_code == 200


async def test_password_reset_needs_supabase(client: httpx.AsyncClient, api: str) -> None:
    response = await client.post(f"{api}/auth/password/forgot", json={"email": EMAIL})
    assert response.status_code == 503


# --- Өөрийн бүртгэл ----------------------------------------------------------------


async def test_update_name_and_hide_profile(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    course, _ = await make_course_with_lessons(db, slug="js", lesson_count=1)
    me = await make_user(db, EMAIL)
    other = await make_user(db, "busad@test.mn")
    db.add_all(Enrollment(user_id=user.id, course_id=course.id) for user in (me, other))
    await db.commit()
    await login_as(client, api, EMAIL)

    updated = await client.patch(f"{api}/me", json={"name": "Шинэ нэр", "profile_hidden": True})
    assert updated.status_code == 200, updated.text
    assert (updated.json()["name"], updated.json()["profile_hidden"]) == ("Шинэ нэр", True)

    # Нуусан ч өөрийн профайлаа харна.
    assert (await client.get(f"{api}/users/{me.id}/profile")).status_code == 200

    await login_as(client, api, "busad@test.mn")
    hidden = await client.get(f"{api}/users/{me.id}/profile")
    assert hidden.status_code == 403
    assert hidden.json()["detail"]["code"] == "PROFILE_HIDDEN"
    students = (await client.get(f"{api}/courses/js/students")).json()
    assert students["total"] == 2
    assert [item["id"] for item in students["items"]] == [str(other.id)]


async def test_motivation_can_be_turned_off(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    await make_user(db, EMAIL)
    await login_as(client, api, EMAIL)
    assert (await client.get(f"{api}/auth/me")).json()["show_motivation"] is True

    updated = await client.patch(f"{api}/me", json={"show_motivation": False})

    assert updated.json()["show_motivation"] is False
    assert (await client.get(f"{api}/auth/me")).json()["show_motivation"] is False


async def test_editor_layout_defaults_to_new_and_can_be_changed(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    await make_user(db, EMAIL)
    await login_as(client, api, EMAIL)
    assert (await client.get(f"{api}/auth/me")).json()["editor_layout"] == "new"

    updated = await client.patch(f"{api}/me", json={"editor_layout": "legacy"})

    assert updated.json()["editor_layout"] == "legacy"
    assert (await client.get(f"{api}/auth/me")).json()["editor_layout"] == "legacy"
    # Бусад тохиргоо өөрчлөгдөхгүй.
    assert updated.json()["show_motivation"] is True
    assert (await client.patch(f"{api}/me", json={"editor_layout": "side"})).status_code == 422


async def test_change_email_without_verification(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    await make_user(db, EMAIL)
    await make_user(db, "avsan@test.mn")
    await login_as(client, api, EMAIL)

    wrong = await client.post(
        f"{api}/me/email", json={"new_email": "Shine2@Test.mn", "password": "Buruu12345"}
    )
    assert wrong.json()["detail"]["code"] == "WRONG_PASSWORD"
    taken = await client.post(
        f"{api}/me/email", json={"new_email": "avsan@test.mn", "password": TEST_PASSWORD}
    )
    assert taken.status_code == 409

    changed = await client.post(
        f"{api}/me/email", json={"new_email": "Shine2@Test.mn", "password": TEST_PASSWORD}
    )
    assert changed.status_code == 200, changed.text
    assert changed.json()["verification_required"] is False
    assert changed.json()["user"]["email"] == "shine2@test.mn"


async def test_change_email_with_code(
    client: httpx.AsyncClient, api: str, db: AsyncSession, supabase: FakeSupabase
) -> None:
    await make_user(db, EMAIL)
    supabase.users[EMAIL] = "old-id"
    await login_as(client, api, EMAIL)

    requested = await client.post(
        f"{api}/me/email", json={"new_email": "shine2@test.mn", "password": TEST_PASSWORD}
    )
    assert requested.json()["verification_required"] is True
    assert requested.json()["user"]["email"] == EMAIL
    assert supabase.sent == ["shine2@test.mn"]

    bad = await client.post(f"{api}/me/email/confirm", json={"code": "000000"})
    assert bad.json()["detail"]["code"] == "INVALID_CODE"
    good = await client.post(f"{api}/me/email/confirm", json={"code": GOOD_CODE})
    assert good.status_code == 200, good.text
    assert good.json()["email"] == "shine2@test.mn"
    assert supabase.deleted == [EMAIL]

    # Сесс хэвээр, шинэ имэйлээр нэвтэрнэ.
    assert (await client.get(f"{api}/auth/me")).json()["email"] == "shine2@test.mn"
    none_left = await client.post(f"{api}/me/email/confirm", json={"code": GOOD_CODE})
    assert none_left.json()["detail"]["code"] == "NO_PENDING_EMAIL"


async def test_account_deletion_waits_two_hours_and_can_be_cancelled(
    client: httpx.AsyncClient, api: str, db: AsyncSession, supabase: FakeSupabase
) -> None:
    user = await make_user(db, EMAIL)
    supabase.users[EMAIL] = "auth-id"
    db.add(Payment(user_id=user.id, amount=2_490_000, currency="MNT", status="succeeded"))
    await db.commit()
    await login_as(client, api, EMAIL)

    wrong = await client.post(f"{api}/me/delete", json={"password": "Buruu12345"})
    assert wrong.json()["detail"]["code"] == "WRONG_PASSWORD"

    scheduled = await client.post(f"{api}/me/delete", json={"password": TEST_PASSWORD})
    assert scheduled.status_code == 200, scheduled.text
    when = datetime.fromisoformat(scheduled.json()["deletion_scheduled_at"])
    assert timedelta(minutes=119) < when - datetime.now(UTC) <= timedelta(hours=2)
    # Дахин хүсэхэд хугацаа сунгагдахгүй.
    again = await client.post(f"{api}/me/delete", json={"password": TEST_PASSWORD})
    assert again.json()["deletion_scheduled_at"] == scheduled.json()["deletion_scheduled_at"]

    cancelled = await client.post(f"{api}/me/delete/cancel")
    assert cancelled.json()["deletion_scheduled_at"] is None
    await client.post(f"{api}/me/delete", json={"password": TEST_PASSWORD})

    async with httpx.AsyncClient(
        transport=httpx.MockTransport(supabase.handle), base_url="https://p.test/auth/v1"
    ) as auth:
        # Хугацаа болоогүй бол юу ч устгахгүй.
        assert await account_service.purge_due_accounts(db, auth) == 0
        await db.execute(
            update(User)
            .where(User.id == user.id)
            .values(deletion_scheduled_at=datetime.now(UTC) - timedelta(seconds=1))
        )
        await db.commit()
        assert await account_service.purge_due_accounts(db, auth) == 1

    assert supabase.deleted == [EMAIL]
    assert (await client.get(f"{api}/auth/me")).status_code == 401
    db.expire_all()
    assert (await db.execute(select(User).where(User.email == EMAIL))).first() is None
    payment = (await db.execute(select(Payment))).scalar_one()
    assert payment.user_id is None


async def test_retention_purges_old_feedback_and_payments(db: AsyncSession) -> None:
    user = await make_user(db, EMAIL)
    now = datetime.now(UTC)
    db.add_all(
        [
            Feedback(
                user_id=user.id,
                kind="idea",
                message="Хуучин санал",
                created_at=now - timedelta(days=91),
            ),
            Feedback(user_id=user.id, kind="idea", message="Шинэ санал"),
            Payment(
                user_id=user.id, amount=1, status="succeeded", created_at=now - timedelta(days=366)
            ),
            Payment(user_id=user.id, amount=2, status="succeeded"),
        ]
    )
    await db.commit()

    assert await account_service.purge_expired_records(db) == (1, 1)
    assert [f.message for f in (await db.execute(select(Feedback))).scalars()] == ["Шинэ санал"]
    assert [p.amount for p in (await db.execute(select(Payment))).scalars()] == [2]
