"""Админы зарлал (popup) — шинэчлэл мэдээлэх, боломж онцлох."""

import uuid

from fastapi import APIRouter, Response, status

from app.core.deps import AdminUser, DbSession, OptionalUser
from app.schemas.announcement import (
    AnnouncementCreate,
    AnnouncementItem,
    AnnouncementPublic,
    AnnouncementUpdate,
)
from app.services import announcement_service

router = APIRouter(prefix="/announcements", tags=["announcements"])


@router.get("/current", response_model=list[AnnouncementPublic])
async def current(db: DbSession, user: OptionalUser) -> list[AnnouncementPublic]:
    """Одоо танд харагдах зарлалууд, шинэ нь эхэнд. Нэвтрээгүй зочинд зөвхөн
    «бүгдэд» гэсэн нь. Аль нь гарахыг, хаасныг хөтөч санана."""
    return await announcement_service.current_for(db, user)


@router.get("", response_model=list[AnnouncementItem])
async def list_all(db: DbSession, _: AdminUser) -> list[AnnouncementItem]:
    """Админ: бүх зарлал (ноорог, товлосон, дууссаныг оруулаад)."""
    return await announcement_service.list_all(db)


@router.post("", response_model=AnnouncementItem, status_code=status.HTTP_201_CREATED)
async def create(payload: AnnouncementCreate, db: DbSession, admin: AdminUser) -> AnnouncementItem:
    return await announcement_service.create(db, admin, payload)


@router.patch("/{announcement_id}", response_model=AnnouncementItem)
async def update(
    announcement_id: uuid.UUID, payload: AnnouncementUpdate, db: DbSession, _: AdminUser
) -> AnnouncementItem:
    return await announcement_service.update(db, announcement_id, payload)


@router.delete("/{announcement_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(announcement_id: uuid.UUID, db: DbSession, _: AdminUser) -> Response:
    await announcement_service.delete(db, announcement_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
