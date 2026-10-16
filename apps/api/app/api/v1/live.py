"""MedlegHub Live (AI Study). `LIVE_ACCESS` хэрэглэгчийг зөвшөөрөхгүй бол бүх зам 404.

AI ажил (материал задлах, заавар, тест, таамаг) цаана явна: эдгээр зам 202-оор
шууд хариулж, вэб төлөвийг нь давтан асууна.
"""

import uuid
from decimal import Decimal
from typing import Annotated, Literal

from fastapi import APIRouter, Depends, Query, Request, Response, status

from app.core.config import settings
from app.core.deps import AdminUser, DbSession, OptionalUser
from app.live import access, admin, materials, source, study, worker
from app.live.access import LiveUser
from app.live.storage import BlobStorage, get_storage
from app.models.enums import LiveTier
from app.schemas.live import (
    LiveAdminOverview,
    LiveAnswerCreate,
    LiveAnswerResult,
    LiveAttempt,
    LiveAttemptResult,
    LiveCard,
    LiveCardReview,
    LiveConfig,
    LiveGeneration,
    LiveGenerationRequest,
    LiveMaterialCreate,
    LiveMaterialDetail,
    LiveMaterialSummary,
    LiveMaterialUpdate,
    LiveModelStatus,
    LivePassInfo,
    LivePassMaterial,
    LiveSubscriptionGrant,
    LiveSubscriptionInfo,
    LiveSubscriptionLookup,
    LiveUploadLimits,
    LiveUsage,
)
from app.services.ai import routing
from app.services.ai.capabilities import Capability

router = APIRouter(prefix="/live", tags=["live"])


def get_live_storage() -> BlobStorage:
    """Тестэд `app.dependency_overrides`-оор түр хавтсаар солино."""
    return get_storage()


Storage = Annotated[BlobStorage, Depends(get_live_storage)]


@router.get("/config", response_model=LiveConfig)
async def config(db: DbSession, user: OptionalUser) -> LiveConfig:
    """Энэ хэрэглэгчид Live нээлттэй эсэх, хязгаар, энэ сарын хэрэглээ. Зочинд ч хариулна."""
    upload = LiveUploadLimits(
        max_bytes=settings.live_max_upload_bytes,
        max_pages=settings.live_max_pages,
        accepted=source.ACCEPTED_EXTENSIONS,
    )
    if user is None or not access.live_enabled_for(user):
        return LiveConfig(
            enabled=False,
            ai_configured=False,
            tier=None,
            tier_expires_at=None,
            usage=None,
            upload=upload,
        )
    entitlement = await access.entitlement_for(db, user)
    usage = None
    passes = None
    # Багцгүй хэрэглэгчид Live хаалттай — вэб «Standard, Premium-д» гэж харуулна.
    if entitlement.tier == LiveTier.PASS:
        cap = entitlement.ai_monthly_usd
        opened = []
        for material_id, expires_at in entitlement.pass_materials.items():
            spent = await access.material_spent_usd(db, material_id)
            opened.append(
                LivePassMaterial(
                    material_id=material_id,
                    expires_at=expires_at,
                    ai_used_percent=min(100, round(100 * spent / cap)) if cap > 0 else 100,
                )
            )
        passes = LivePassInfo(unused=entitlement.unused_pass_id is not None, materials=opened)
    elif entitlement.tier != LiveTier.FREE:
        spent = await access.ai_spent_usd(db, user.id)
        cap = entitlement.ai_monthly_usd
        usage = LiveUsage(
            ai_used_percent=min(100, round(100 * spent / cap)) if cap > Decimal(0) else 100,
            ai_period_resets_at=access.next_month_start(),
        )
    return LiveConfig(
        enabled=True,
        ai_configured=routing.is_configured(Capability.DOCUMENT),
        tier=entitlement.tier,
        tier_expires_at=entitlement.expires_at,
        usage=usage,
        upload=upload,
        passes=passes,
    )


@router.get("/materials", response_model=list[LiveMaterialSummary])
async def list_materials(db: DbSession, user: LiveUser) -> list[LiveMaterialSummary]:
    return await materials.list_for(db, user)


@router.post("/materials", response_model=LiveMaterialSummary, status_code=status.HTTP_201_CREATED)
async def create_material(
    payload: LiveMaterialCreate, db: DbSession, user: LiveUser
) -> LiveMaterialSummary:
    """Мета, эрх, хязгаарыг шалгана. Файлыг дараа нь `PUT …/content`-оор."""
    material = await materials.create(db, user, payload)
    return await materials.summary(db, user, material)


@router.put(
    "/materials/{material_id}/content",
    response_model=LiveMaterialSummary,
    status_code=status.HTTP_202_ACCEPTED,
)
async def upload_content(
    material_id: uuid.UUID, request: Request, db: DbSession, user: LiveUser, storage: Storage
) -> LiveMaterialSummary:
    """Файлын түүхий бие (`application/octet-stream`). Биеийн параметр ЗОРИУД байхгүй —
    FastAPI биеийг урьдчилан уншихгүй, нэвтрэлт, хязгаарыг эхэлж шалгана."""
    material = await materials.owned_material(db, user, material_id)
    material = await materials.receive_content(db, user, material, request, storage)
    worker.notify()
    return await materials.summary(db, user, material)


@router.get("/materials/{material_id}", response_model=LiveMaterialDetail)
async def get_material(material_id: uuid.UUID, db: DbSession, user: LiveUser) -> LiveMaterialDetail:
    material = await materials.owned_material(db, user, material_id)
    return await materials.detail(db, user, material)


@router.patch("/materials/{material_id}", response_model=LiveMaterialSummary)
async def rename_material(
    material_id: uuid.UUID, payload: LiveMaterialUpdate, db: DbSession, user: LiveUser
) -> LiveMaterialSummary:
    material = await materials.owned_material(db, user, material_id)
    material = await materials.rename(db, material, payload.title)
    return await materials.summary(db, user, material)


@router.delete("/materials/{material_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_material(material_id: uuid.UUID, db: DbSession, user: LiveUser) -> Response:
    material = await materials.owned_material(db, user, material_id)
    await materials.delete(db, material)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    "/materials/{material_id}/retry",
    response_model=LiveMaterialSummary,
    status_code=status.HTTP_202_ACCEPTED,
)
async def retry_material(
    material_id: uuid.UUID, db: DbSession, user: LiveUser
) -> LiveMaterialSummary:
    material = await materials.owned_material(db, user, material_id)
    material = await materials.retry(db, user, material)
    worker.notify()
    return await materials.summary(db, user, material)


@router.post(
    "/materials/{material_id}/generations",
    response_model=LiveGeneration,
    status_code=status.HTTP_202_ACCEPTED,
)
async def request_generation(
    material_id: uuid.UUID, payload: LiveGenerationRequest, db: DbSession, user: LiveUser
) -> LiveGeneration:
    """Бэлэн эсвэл үүсгэж байгаа нь байвал түүнийг буцаана — AI дахин дуудагдахгүй."""
    material = await materials.owned_material(db, user, material_id)
    generation = await study.request_generation(db, user, material, payload)
    worker.notify()
    return await study.generation_view(db, generation)


@router.get("/materials/{material_id}/cards", response_model=list[LiveCard])
async def list_cards(
    material_id: uuid.UUID,
    db: DbSession,
    user: LiveUser,
    topic_id: uuid.UUID | None = None,
    mode: Annotated[Literal["due", "all"], Query()] = "due",
) -> list[LiveCard]:
    material = await materials.owned_material(db, user, material_id)
    return await study.list_cards(db, user, material, topic_id=topic_id, mode=mode)


@router.get("/generations/{generation_id}", response_model=LiveGeneration)
async def get_generation(generation_id: uuid.UUID, db: DbSession, user: LiveUser) -> LiveGeneration:
    generation = await study.owned_generation(db, user, generation_id)
    return await study.generation_view(db, generation)


@router.post(
    "/generations/{generation_id}/attempts",
    response_model=LiveAttempt,
    status_code=status.HTTP_201_CREATED,
)
async def start_attempt(generation_id: uuid.UUID, db: DbSession, user: LiveUser) -> LiveAttempt:
    generation = await study.owned_generation(db, user, generation_id)
    attempt = await study.start_attempt(db, user, generation)
    return await study.attempt_view(db, attempt)


@router.post("/attempts/{attempt_id}/answers", response_model=LiveAnswerResult)
async def answer(
    attempt_id: uuid.UUID, payload: LiveAnswerCreate, db: DbSession, user: LiveUser
) -> LiveAnswerResult:
    """Зөв хариулт, тайлбар зөвхөн энд — хариулсны дараа."""
    attempt = await study.owned_attempt(db, user, attempt_id)
    return await study.answer(db, attempt, payload)


@router.post("/attempts/{attempt_id}/finish", response_model=LiveAttemptResult)
async def finish_attempt(attempt_id: uuid.UUID, db: DbSession, user: LiveUser) -> LiveAttemptResult:
    attempt = await study.owned_attempt(db, user, attempt_id)
    return await study.finish(db, user, attempt)


@router.post("/topics/{topic_id}/guide-read", status_code=status.HTTP_204_NO_CONTENT)
async def guide_read(topic_id: uuid.UUID, db: DbSession, user: LiveUser) -> Response:
    topic = await study.owned_topic(db, user, topic_id)
    await study.mark_guide_read(db, user, topic)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/cards/{card_id}/review", response_model=LiveCard)
async def review_card(
    card_id: uuid.UUID, payload: LiveCardReview, db: DbSession, user: LiveUser
) -> LiveCard:
    card = await study.owned_card(db, user, card_id)
    return await study.review_card(db, user, card, payload.rating)


# --- Админ -------------------------------------------------------------------


@router.get("/admin/overview", response_model=LiveAdminOverview)
async def admin_overview(db: DbSession, _: AdminUser) -> LiveAdminOverview:
    return await admin.overview(db)


@router.get("/admin/models", response_model=list[LiveModelStatus])
async def admin_models(db: DbSession, _: AdminUser) -> list[LiveModelStatus]:
    """Загвар бүр хязгаарт хүрсэн (хөргөгдсөн) эсэх, хэрэглээ, энэ сарын зардал."""
    return await admin.models_status(db)


@router.post("/admin/subscriptions/lookup", response_model=LiveSubscriptionInfo)
async def admin_lookup(
    payload: LiveSubscriptionLookup, db: DbSession, _: AdminUser
) -> LiveSubscriptionInfo:
    """Имэйл биед — URL, access log-д үлдэхгүй."""
    return await admin.lookup(db, payload.email)


@router.post("/admin/subscriptions", response_model=LiveSubscriptionInfo)
async def admin_grant(
    payload: LiveSubscriptionGrant, db: DbSession, admin_user: AdminUser
) -> LiveSubscriptionInfo:
    return await admin.grant(db, admin_user, payload)
