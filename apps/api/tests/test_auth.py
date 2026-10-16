import httpx

from app.api.v1.auth import SESSION_HINT_COOKIE
from app.core.config import settings
from tests.conftest import login_as, make_user

CONSENT = {"is_16_or_older": True, "accept_terms": True}


async def test_register_sets_cookie_and_returns_user(client: httpx.AsyncClient, api: str) -> None:
    """Имэйл баталгаажуулалт унтраалттай (Supabase тохируулаагүй) — шууд нэвтэрнэ."""
    response = await client.post(
        f"{api}/auth/register",
        json={"email": "shine@suralts.mn", "password": "Nuuts12345", "name": "Шинэ", **CONSENT},
    )
    assert response.status_code == 201, response.text
    result = response.json()
    assert result["verification_required"] is False
    body = result["user"]
    assert body["email"] == "shine@suralts.mn"
    assert body["role"] == "student"
    assert body["profile_hidden"] is False
    assert "password" not in body and "password_hash" not in body
    assert settings.auth_cookie_name in response.cookies
    # UI-д зориулсан сэжүүр cookie — нууц утгагүй.
    assert response.cookies[SESSION_HINT_COOKIE] == "1"


async def test_register_rejects_duplicate_email(client: httpx.AsyncClient, api: str) -> None:
    payload = {"email": "davhar@suralts.mn", "password": "Nuuts12345", "name": "Давхар", **CONSENT}
    assert (await client.post(f"{api}/auth/register", json=payload)).status_code == 201

    response = await client.post(f"{api}/auth/register", json=payload)
    assert response.status_code == 409
    assert response.json()["detail"]["code"] == "EMAIL_TAKEN"


async def test_register_rejects_weak_password(client: httpx.AsyncClient, api: str) -> None:
    response = await client.post(
        f"{api}/auth/register",
        json={"email": "sul@suralts.mn", "password": "onlyletters", "name": "Сул", **CONSENT},
    )
    assert response.status_code == 422
    assert response.json()["detail"]["code"] == "VALIDATION_ERROR"


async def test_login_with_wrong_password_fails(client: httpx.AsyncClient, api: str, db) -> None:
    await make_user(db, "buruu@suralts.mn")
    response = await client.post(
        f"{api}/auth/login", json={"email": "buruu@suralts.mn", "password": "Buruu12345"}
    )
    assert response.status_code == 401
    assert response.json()["detail"]["code"] == "INVALID_CREDENTIALS"


async def test_me_requires_authentication(client: httpx.AsyncClient, api: str) -> None:
    response = await client.get(f"{api}/auth/me")
    assert response.status_code == 401
    assert response.json()["detail"]["code"] == "NOT_AUTHENTICATED"


async def test_login_then_me_then_logout(client: httpx.AsyncClient, api: str, db) -> None:
    await make_user(db, "uragshaa@suralts.mn")
    await login_as(client, api, "uragshaa@suralts.mn")

    me = await client.get(f"{api}/auth/me")
    assert me.status_code == 200
    assert me.json()["email"] == "uragshaa@suralts.mn"

    logout = await client.post(f"{api}/auth/logout")
    assert logout.status_code == 200
    assert SESSION_HINT_COOKIE not in client.cookies

    assert (await client.get(f"{api}/auth/me")).status_code == 401
