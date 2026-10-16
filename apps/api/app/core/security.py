"""Нууц үгийн hash болон JWT.

bcrypt-ийг шууд ашиглана (passlib-гүй) — хамаарал цөөрч, хувилбарын зөрчил үүсэхгүй.
"""

from datetime import UTC, datetime, timedelta
from typing import Any

import bcrypt
import jwt

from app.core.config import settings

# bcrypt нь 72 байтаас дээш оролтыг чимээгүйгээр тасалдаг тул өөрсдөө хязгаарлана.
MAX_PASSWORD_BYTES = 72


def hash_password(password: str) -> str:
    payload = password.encode("utf-8")[:MAX_PASSWORD_BYTES]
    return bcrypt.hashpw(payload, bcrypt.gensalt(rounds=settings.bcrypt_rounds)).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    try:
        return bcrypt.checkpw(
            password.encode("utf-8")[:MAX_PASSWORD_BYTES],
            password_hash.encode("utf-8"),
        )
    except ValueError:
        # Гэмтсэн эсвэл буруу форматтай hash — нэвтрэхийг зөвшөөрөхгүй.
        return False


def create_access_token(subject: str, role: str, password_version: int = 0) -> str:
    """`pwv` — олгох үеийн нууц үгийн хувилбар (`User.password_version`).

    Нууц үг солигдоход хувилбар өөрчлөгдөж, хуучин token бүр хүчингүй болно.
    """
    now = datetime.now(UTC)
    payload: dict[str, Any] = {
        "sub": subject,
        "role": role,
        "pwv": password_version,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=settings.jwt_expire_minutes)).timestamp()),
        "typ": "access",
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> dict[str, Any] | None:
    """Token хүчинтэй бол payload, эс бөгөөс None буцаана."""
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
            options={"require": ["exp", "sub"]},
        )
    except jwt.PyJWTError:
        return None
    if payload.get("typ") != "access":
        return None
    return payload
