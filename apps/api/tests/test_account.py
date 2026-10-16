"""Нууц үг солих, профайлын зураг."""

import io

import httpx
import pytest
from PIL import Image
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from tests.conftest import TEST_PASSWORD, login_as, make_user

NEW_PASSWORD = "Shine12345"


async def _signed_in(client: httpx.AsyncClient, api: str, db: AsyncSession, email="bi@test.mn"):
    user = await make_user(db, email)
    await login_as(client, api, email)
    return user


def _png(width: int = 600, height: int = 400, color=(255, 120, 0)) -> bytes:
    out = io.BytesIO()
    Image.new("RGB", (width, height), color).save(out, "PNG")
    return out.getvalue()


def _upload(content: bytes, name: str = "zurag.png", mime: str = "image/png") -> dict:
    return {"file": (name, content, mime)}


# --- Нууц үг солих -----------------------------------------------------------


async def test_change_password_then_login_with_new_one(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    await _signed_in(client, api, db)
    response = await client.post(
        f"{api}/auth/password",
        json={"current_password": TEST_PASSWORD, "new_password": NEW_PASSWORD},
    )
    assert response.status_code == 200
    # Энэ сесс шинэ cookie авсан тул нэвтэрсэн хэвээр.
    assert (await client.get(f"{api}/auth/me")).status_code == 200

    old = await client.post(
        f"{api}/auth/login", json={"email": "bi@test.mn", "password": TEST_PASSWORD}
    )
    assert old.status_code == 401
    new = await client.post(
        f"{api}/auth/login", json={"email": "bi@test.mn", "password": NEW_PASSWORD}
    )
    assert new.status_code == 200


async def test_change_password_logs_out_other_sessions(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    await _signed_in(client, api, db)
    other_device = client.cookies.get(settings.auth_cookie_name)
    assert other_device

    await client.post(
        f"{api}/auth/password",
        json={"current_password": TEST_PASSWORD, "new_password": NEW_PASSWORD},
    )
    response = await client.get(
        f"{api}/auth/me",
        headers={"Authorization": f"Bearer {other_device}"},
        cookies={settings.auth_cookie_name: ""},
    )
    assert response.status_code == 401


@pytest.mark.parametrize(
    ("current", "new", "status", "code"),
    [
        ("Buruu12345", NEW_PASSWORD, 400, "WRONG_PASSWORD"),
        (TEST_PASSWORD, TEST_PASSWORD, 400, "SAME_PASSWORD"),
        (TEST_PASSWORD, "zovhonuseg", 422, None),
        (TEST_PASSWORD, "Bogin1", 422, None),
    ],
)
async def test_change_password_rejections(
    client: httpx.AsyncClient, api: str, db: AsyncSession, current, new, status, code
) -> None:
    await _signed_in(client, api, db)
    response = await client.post(
        f"{api}/auth/password", json={"current_password": current, "new_password": new}
    )
    assert response.status_code == status
    if code:
        assert response.json()["detail"]["code"] == code
    # Амжилтгүй оролдлого сессийг гаргахгүй.
    assert (await client.get(f"{api}/auth/me")).status_code == 200


async def test_change_password_requires_login(client: httpx.AsyncClient, api: str) -> None:
    response = await client.post(
        f"{api}/auth/password",
        json={"current_password": TEST_PASSWORD, "new_password": NEW_PASSWORD},
    )
    assert response.status_code == 401


# --- Профайлын зураг ---------------------------------------------------------


async def test_upload_is_normalized_to_small_webp(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    user = await _signed_in(client, api, db)
    response = await client.put(f"{api}/me/avatar", files=_upload(_png()))
    assert response.status_code == 200
    key = response.json()["avatar_key"]
    assert key and (await client.get(f"{api}/auth/me")).json()["avatar_key"] == key

    image = await client.get(f"{api}/users/{user.id}/avatar", params={"v": key})
    assert image.status_code == 200
    assert image.headers["content-type"] == "image/webp"
    assert "immutable" in image.headers["cache-control"]
    decoded = Image.open(io.BytesIO(image.content))
    assert (decoded.format, decoded.size) == ("WEBP", (256, 256))


async def test_metadata_is_stripped(client: httpx.AsyncClient, api: str, db: AsyncSession) -> None:
    user = await _signed_in(client, api, db)
    exif = Image.Exif()
    exif[0x010F] = "SecretCamera"  # Make
    exif[0x8825] = {1: "N", 2: (47.0, 55.0, 0.0)}  # GPS
    raw = io.BytesIO()
    Image.new("RGB", (300, 300), "blue").save(raw, "JPEG", exif=exif)

    response = await client.put(
        f"{api}/me/avatar", files=_upload(raw.getvalue(), "zurag.jpg", "image/jpeg")
    )
    assert response.status_code == 200
    stored = await client.get(f"{api}/users/{user.id}/avatar")
    assert b"SecretCamera" not in stored.content
    assert not Image.open(io.BytesIO(stored.content)).getexif()


@pytest.mark.parametrize(
    ("content", "name", "mime"),
    [
        (b"not an image at all", "zurag.png", "image/png"),
        (
            b'<svg xmlns="http://www.w3.org/2000/svg"><script>alert(1)</script></svg>',
            "zurag.svg",
            "image/svg+xml",
        ),
        (b"", "hooson.png", "image/png"),
    ],
)
async def test_non_images_are_rejected(
    client: httpx.AsyncClient, api: str, db: AsyncSession, content, name, mime
) -> None:
    await _signed_in(client, api, db)
    response = await client.put(f"{api}/me/avatar", files=_upload(content, name, mime))
    assert response.status_code == 400
    assert response.json()["detail"]["code"] == "INVALID_IMAGE"


async def test_decompression_bomb_is_rejected(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    """10 000 × 10 000 нэг өнгийн PNG нь хэдхэн KB — задлахад 100 мегапиксель."""
    await _signed_in(client, api, db)
    bomb = _png(10_000, 10_000)
    assert len(bomb) < settings.avatar_max_upload_bytes
    response = await client.put(f"{api}/me/avatar", files=_upload(bomb))
    assert response.status_code == 400


async def test_oversized_upload_is_rejected(
    client: httpx.AsyncClient, api: str, db: AsyncSession, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(settings, "avatar_max_upload_bytes", 1_000)
    await _signed_in(client, api, db)
    response = await client.put(f"{api}/me/avatar", files=_upload(_png()))
    assert response.status_code == 413
    assert response.json()["detail"]["code"] == "IMAGE_TOO_LARGE"


async def test_replace_and_remove_avatar(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    user = await _signed_in(client, api, db)
    first = (await client.put(f"{api}/me/avatar", files=_upload(_png()))).json()["avatar_key"]
    second = (await client.put(f"{api}/me/avatar", files=_upload(_png(color=(0, 90, 200))))).json()[
        "avatar_key"
    ]
    assert first != second

    removed = await client.delete(f"{api}/me/avatar")
    assert removed.status_code == 200
    assert removed.json()["avatar_key"] is None
    assert (await client.get(f"{api}/users/{user.id}/avatar")).status_code == 404


async def test_avatar_upload_requires_login(client: httpx.AsyncClient, api: str) -> None:
    response = await client.put(f"{api}/me/avatar", files=_upload(_png()))
    assert response.status_code == 401
