"""Аюулгүй байдлын шаардлагуудыг (§21) шалгах тестүүд."""

import httpx
import jwt

from app.api.v1.auth import SESSION_HINT_COOKIE
from app.core.config import settings
from app.core.security import hash_password, verify_password
from app.models.enums import UserRole
from tests.conftest import TEST_PASSWORD, login_as, make_user
from tests.factories import make_course, make_course_with_lessons


def test_passwords_are_hashed_not_stored() -> None:
    hashed = hash_password("Nuuts12345")
    assert hashed != "Nuuts12345"
    assert hashed.startswith("$2b$")
    assert verify_password("Nuuts12345", hashed)
    assert not verify_password("Nuuts12346", hashed)


def test_corrupt_hash_rejects_login() -> None:
    assert verify_password("anything", "not-a-bcrypt-hash") is False


async def test_auth_cookie_is_http_only(client: httpx.AsyncClient, api: str, db) -> None:
    await make_user(db, "cookie@test.mn")
    response = await client.post(
        f"{api}/auth/login", json={"email": "cookie@test.mn", "password": TEST_PASSWORD}
    )
    raw = response.headers.get_list("set-cookie")
    token_cookie = next(c for c in raw if c.startswith(settings.auth_cookie_name))
    hint_cookie = next(c for c in raw if c.startswith(SESSION_HINT_COOKIE))

    assert "HttpOnly" in token_cookie, "JWT нь JavaScript-д хүрэхгүй байх ёстой"
    assert "SameSite" in token_cookie
    # Сэжүүр cookie нь нууц утгагүй тул JS уншиж болно.
    assert "HttpOnly" not in hint_cookie


async def test_token_is_not_returned_in_body(client: httpx.AsyncClient, api: str, db) -> None:
    await make_user(db, "body@test.mn")
    response = await client.post(
        f"{api}/auth/login", json={"email": "body@test.mn", "password": TEST_PASSWORD}
    )
    body = response.json()
    assert "token" not in body
    assert "access_token" not in body
    assert "password_hash" not in body


async def test_forged_token_is_rejected(client: httpx.AsyncClient, api: str, db) -> None:
    user = await make_user(db, "forged@test.mn")
    forged = jwt.encode(
        {"sub": str(user.id), "role": "admin", "exp": 9_999_999_999, "typ": "access"},
        "wrong-secret",
        algorithm="HS256",
    )
    client.cookies.set(settings.auth_cookie_name, forged)
    assert (await client.get(f"{api}/auth/me")).status_code == 401


async def test_expired_token_is_rejected(client: httpx.AsyncClient, api: str, db) -> None:
    user = await make_user(db, "expired@test.mn")
    expired = jwt.encode(
        {"sub": str(user.id), "role": "student", "exp": 1_000_000, "typ": "access"},
        settings.jwt_secret,
        algorithm="HS256",
    )
    client.cookies.set(settings.auth_cookie_name, expired)
    assert (await client.get(f"{api}/auth/me")).status_code == 401


async def test_role_in_token_does_not_grant_admin(client: httpx.AsyncClient, api: str, db) -> None:
    """Эрхийг token доторх `role` биш, өгөгдлийн сан дахь бичлэг шийднэ."""
    user = await make_user(db, "escalate@test.mn", role=UserRole.STUDENT)
    elevated = jwt.encode(
        {"sub": str(user.id), "role": "admin", "exp": 9_999_999_999, "typ": "access"},
        settings.jwt_secret,
        algorithm="HS256",
    )
    client.cookies.set(settings.auth_cookie_name, elevated)

    response = await client.post(f"{api}/courses", json={"title": "Хакер", "slug": "haker"})
    assert response.status_code == 403


async def test_student_cannot_reach_admin_course_view(
    client: httpx.AsyncClient, api: str, db
) -> None:
    course = await make_course(db, slug="nuuts-surgalt", published=False)
    await make_user(db, "suragch@test.mn")
    await login_as(client, api, "suragch@test.mn")
    assert (await client.get(f"{api}/admin/courses/{course.id}")).status_code == 403


async def test_student_cannot_see_another_users_progress(
    client: httpx.AsyncClient, api: str, db
) -> None:
    course, lessons = await make_course_with_lessons(db, lesson_count=2)
    await make_user(db, "negdugeer@test.mn")
    await make_user(db, "hoyrdugaar@test.mn")

    await login_as(client, api, "negdugeer@test.mn")
    await client.post(f"{api}/courses/{course.id}/enroll")
    await client.post(f"{api}/lessons/{lessons[0].id}/complete")
    await client.post(f"{api}/auth/logout")

    await login_as(client, api, "hoyrdugaar@test.mn")
    progress = (await client.get(f"{api}/courses/{course.id}/progress")).json()
    assert progress["completed_lessons"] == 0


async def test_sql_injection_in_search_is_harmless(client: httpx.AsyncClient, api: str, db) -> None:
    await make_course(db, slug="jinhene", title="Жинхэнэ сургалт")
    response = await client.get(f"{api}/courses", params={"q": "'; DROP TABLE courses; --"})
    assert response.status_code == 200
    assert response.json()["total"] == 0
    # Хүснэгт байрандаа байгаа эсэхийг шалгана.
    assert (await client.get(f"{api}/courses")).json()["total"] == 1


async def test_oversized_input_is_rejected(client: httpx.AsyncClient, api: str, db) -> None:
    await make_user(db, "admin@test.mn", role=UserRole.ADMIN)
    await login_as(client, api, "admin@test.mn")

    response = await client.post(
        f"{api}/courses", json={"title": "Урт" * 200, "slug": "urt-garchig"}
    )
    assert response.status_code == 422


async def test_cors_only_allows_configured_origin(client: httpx.AsyncClient, api: str) -> None:
    response = await client.options(
        f"{api}/auth/login",
        headers={
            "Origin": "https://evil.example.com",
            "Access-Control-Request-Method": "POST",
        },
    )
    assert "access-control-allow-origin" not in {k.lower() for k in response.headers}


async def test_cors_preflight_allows_put(client: httpx.AsyncClient, api: str) -> None:
    """Локал вэб (өөр origin) PUT-ээр дууддаг — `/me/showcase`, `/me/avatar`."""
    origin = settings.cors_origins[0]
    response = await client.options(
        f"{api}/me/showcase",
        headers={
            "Origin": origin,
            "Access-Control-Request-Method": "PUT",
            "Access-Control-Request-Headers": "content-type",
        },
    )
    assert response.status_code == 200, response.text
    assert response.headers["access-control-allow-origin"] == origin
    assert "PUT" in response.headers["access-control-allow-methods"].split(", ")


async def test_rate_limiter_blocks_credential_stuffing() -> None:
    """Хязгаарлагч нь тохируулсан тооноос хэтэрсэн хүсэлтийг хаана."""
    from app.core.rate_limit import InMemoryRateLimitBackend

    backend = InMemoryRateLimitBackend()
    allowed = [backend.hit("auth:login:1.2.3.4", 3, 60)[0] for _ in range(5)]
    assert allowed == [True, True, True, False, False]
    # Өөр IP нь хамаарахгүй.
    assert backend.hit("auth:login:5.6.7.8", 3, 60)[0] is True


async def test_api_sends_security_headers(client: httpx.AsyncClient) -> None:
    response = await client.get("/health")
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["x-frame-options"] == "DENY"
    assert response.headers["referrer-policy"] == "no-referrer"
    assert "frame-ancestors 'none'" in response.headers["content-security-policy"]


async def test_auth_endpoints_are_rate_limited(
    client: httpx.AsyncClient, api: str, monkeypatch
) -> None:
    """Тест орчинд хязгаарлагч унтраалттай тул түр асааж шалгана."""
    from app.core import rate_limit
    from app.core.rate_limit import InMemoryRateLimitBackend

    monkeypatch.setattr(rate_limit.settings, "rate_limit_enabled", True)
    monkeypatch.setattr(rate_limit.settings, "auth_rate_limit_max", 3)
    monkeypatch.setattr(rate_limit, "backend", InMemoryRateLimitBackend())

    payload = {"email": "hen-negen@test.mn", "password": "Buruu12345"}
    statuses = [
        (await client.post(f"{api}/auth/login", json=payload)).status_code for _ in range(5)
    ]
    assert statuses[:3] == [401, 401, 401]
    assert statuses[3:] == [429, 429]
