"""Хэрэглэгчийн профайл, тэмдгүүд, профайлын зураг."""

import uuid

from fastapi import APIRouter, Depends, File, Request, Response, UploadFile

from app.content.badges import EVENT_BADGES
from app.core import rate_limit
from app.core.config import settings
from app.core.deps import CurrentUser, DbSession
from app.core.errors import NotFoundError, RateLimitError
from app.models.user import User
from app.schemas.auth import UserResponse
from app.schemas.badge import (
    BadgeClaimResponse,
    BadgeShowcaseResponse,
    BadgeShowcaseUpdate,
    ProfileResponse,
)
from app.services import avatar_service, badge_service

router = APIRouter(tags=["profile"])


@router.get("/me/profile", response_model=ProfileResponse)
async def my_profile(db: DbSession, user: CurrentUser) -> ProfileResponse:
    """Профайлын хуудсанд хэрэгтэй бүгд — хэрэглэгч, статистик, тэмдгүүд.

    Нээх бүрд тэмдгийн нөхцөлийг шалгаж, хангасан ч хараахан олгоогүйг
    олгоно — жишээ нь энэ систем нэмэгдэхээс өмнө дуусгасан ахиц.
    """
    return await badge_service.profile(db, user)


@router.post("/me/badges/{badge_key}", response_model=BadgeClaimResponse)
async def claim_badge(badge_key: str, db: DbSession, user: CurrentUser) -> BadgeClaimResponse:
    """Үйлдлээр олгогдох тэмдэг (`EVENT_BADGES`) — дахин дуудахад юу ч өөрчлөхгүй.

    Ахицаар олгогддог тэмдгийг ийм замаар авах боломжгүй — 404.
    """
    if badge_key not in EVENT_BADGES:
        raise NotFoundError("BADGE_NOT_FOUND", "Тэмдэг олдсонгүй.")
    return BadgeClaimResponse(new_badge=await badge_service.claim_event_badge(db, user, badge_key))


@router.put("/me/showcase", response_model=BadgeShowcaseResponse)
async def update_showcase(
    payload: BadgeShowcaseUpdate, db: DbSession, user: CurrentUser
) -> BadgeShowcaseResponse:
    """Профайлын нэрийн хажууд онцлох амжилтууд (0–5), харуулах дарааллаар.

    Өмнөхийг бүхэлд нь солино; `[]` онцлохыг цуцална. Зөвхөн өөрийн авсан
    тэмдэг — аваагүй, байхгүй түлхүүр 400 `SHOWCASE_BADGE_NOT_EARNED`.
    Байр нь `/me/profile`, `/users/{id}/profile`-ийн `showcase_position`-д.
    """
    keys = await badge_service.set_showcase(db, user, payload.badge_keys)
    return BadgeShowcaseResponse(badge_keys=keys)


async def limit_avatar_uploads(user: CurrentUser) -> None:
    """Зураг бүр Pillow-оор боловсрогдоно — хэрэглэгч тус бүрд хязгаарлана."""
    if not settings.rate_limit_enabled:
        return
    allowed, retry_after = rate_limit.backend.hit(
        f"avatar:{user.id}",
        settings.avatar_rate_limit_max,
        settings.avatar_rate_limit_window_seconds,
    )
    if not allowed:
        raise RateLimitError(retry_after)


@router.put(
    "/me/avatar",
    response_model=UserResponse,
    dependencies=[Depends(limit_avatar_uploads)],
)
async def upload_avatar(db: DbSession, user: CurrentUser, file: UploadFile = File(...)) -> User:
    return await avatar_service.set_avatar(db, user, file)


@router.delete("/me/avatar", response_model=UserResponse)
async def delete_avatar(db: DbSession, user: CurrentUser) -> User:
    return await avatar_service.remove_avatar(db, user)


@router.get("/users/{user_id}/avatar", response_class=Response)
async def get_avatar(user_id: uuid.UUID, request: Request, db: DbSession) -> Response:
    """Профайлын зураг — нэвтрэлтгүй (UUID нь таах боломжгүй).

    URL нь `?v={avatar_key}`-тэй тул тохирвол мөнхөд кэшлэнэ; зураг солигдоход
    `avatar_key` өөрчлөгдөж URL шинэ болно.
    """
    data = await avatar_service.get_avatar(db, user_id)
    if data is None:
        raise NotFoundError("AVATAR_NOT_FOUND", "Зураг олдсонгүй.")
    versioned = bool(request.query_params.get("v"))
    return Response(
        content=data,
        media_type="image/webp",
        headers={
            "Cache-Control": "public, max-age=31536000, immutable" if versioned else "no-cache"
        },
    )
