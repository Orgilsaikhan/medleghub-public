"""Module-ийн засвар, устгал (админ)."""

import uuid

from fastapi import APIRouter

from app.core.deps import AdminUser, DbSession
from app.schemas.common import MessageResponse
from app.schemas.module import ModuleUpdate, ModuleWithLessons
from app.services import module_service

router = APIRouter(prefix="/modules", tags=["modules"])


@router.patch("/{module_id}", response_model=ModuleWithLessons)
async def update_module(
    module_id: uuid.UUID, payload: ModuleUpdate, db: DbSession, _: AdminUser
) -> ModuleWithLessons:
    module = await module_service.update_module(db, module_id, payload)
    return ModuleWithLessons(
        id=module.id,
        title=module.title,
        description=module.description,
        position=module.position,
        lessons=[],
    )


@router.delete("/{module_id}", response_model=MessageResponse)
async def delete_module(module_id: uuid.UUID, db: DbSession, _: AdminUser) -> MessageResponse:
    await module_service.delete_module(db, module_id)
    return MessageResponse(message="Модул устгагдлаа.")
