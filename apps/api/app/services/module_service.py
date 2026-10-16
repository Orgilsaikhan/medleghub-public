"""Module-ийн админ CRUD."""

import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import NotFoundError
from app.models.module import Module
from app.schemas.module import ModuleCreate, ModuleUpdate
from app.services.course_service import get_course_or_404


async def get_module_or_404(db: AsyncSession, module_id: uuid.UUID) -> Module:
    module = await db.get(Module, module_id)
    if module is None:
        raise NotFoundError("MODULE_NOT_FOUND", "Модул олдсонгүй.")
    return module


async def _next_position(db: AsyncSession, course_id: uuid.UUID) -> int:
    current_max = (
        await db.execute(select(func.max(Module.position)).where(Module.course_id == course_id))
    ).scalar_one_or_none()
    return 0 if current_max is None else current_max + 1


async def create_module(db: AsyncSession, course_id: uuid.UUID, payload: ModuleCreate) -> Module:
    await get_course_or_404(db, course_id)
    data = payload.model_dump()
    # Position заагаагүй бол төгсгөлд нь нэмнэ.
    if "position" not in payload.model_fields_set:
        data["position"] = await _next_position(db, course_id)

    module = Module(course_id=course_id, **data)
    db.add(module)
    await db.commit()
    await db.refresh(module)
    return module


async def update_module(db: AsyncSession, module_id: uuid.UUID, payload: ModuleUpdate) -> Module:
    module = await get_module_or_404(db, module_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(module, field, value)
    await db.commit()
    await db.refresh(module)
    return module


async def delete_module(db: AsyncSession, module_id: uuid.UUID) -> None:
    module = await get_module_or_404(db, module_id)
    await db.delete(module)
    await db.commit()
