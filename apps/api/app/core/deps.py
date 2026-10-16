"""Дундын FastAPI dependency-ууд."""

import uuid
from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.errors import ForbiddenError, UnauthorizedError
from app.core.security import decode_access_token
from app.db.session import get_db
from app.models.user import User

DbSession = Annotated[AsyncSession, Depends(get_db)]


def _read_token(request: Request) -> str | None:
    """Token-ыг httpOnly cookie-оос уншина.

    `Authorization: Bearer` нь зөвхөн API client/тестэд зориулсан нөөц зам.
    Browser нь cookie ашиглана — ингэснээр token JavaScript-д хүрэхгүй (XSS хамгаалалт).
    """
    token = request.cookies.get(settings.auth_cookie_name)
    if token:
        return token
    header = request.headers.get("authorization", "")
    if header.lower().startswith("bearer "):
        return header[7:].strip() or None
    return None


async def get_current_user_optional(request: Request, db: DbSession) -> User | None:
    """Нэвтрээгүй бол None. Нийтийн endpoint дээр хувийн мэдээлэл нэмэхэд ашиглана."""
    token = _read_token(request)
    if not token:
        return None
    payload = decode_access_token(token)
    if not payload:
        return None
    try:
        user_id = uuid.UUID(payload["sub"])
    except (KeyError, ValueError):
        return None
    user = await db.get(User, user_id)
    # Нууц үг сольсноос өмнө олгосон token — бусад төхөөрөмжийн сесс гарна.
    # `pwv`-гүй хуучин token нь 0 — нууц үгээ хэзээ ч солиогүй бол хүчинтэй.
    if user and payload.get("pwv", 0) != user.password_version:
        return None
    return user


async def get_current_user(
    user: Annotated[User | None, Depends(get_current_user_optional)],
) -> User:
    if user is None:
        raise UnauthorizedError()
    return user


async def require_admin(user: Annotated[User, Depends(get_current_user)]) -> User:
    if not user.is_admin:
        raise ForbiddenError(message="Зөвхөн админ энэ үйлдлийг хийх боломжтой.")
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
OptionalUser = Annotated[User | None, Depends(get_current_user_optional)]
AdminUser = Annotated[User, Depends(require_admin)]
