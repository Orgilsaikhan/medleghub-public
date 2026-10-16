"""Материал: бүртгэх, файл хүлээж авах, жагсаалт, дэлгэрэнгүй (эзэмшилтэй), устгах.

Файл хоёр алхмаар ирнэ: `POST /live/materials` (мета, эрх, хязгаар) → `PUT
…/content` (түүхий бие). Хоёр дахь алхам нь биеийг унших ӨМНӨ нэвтрэлт,
эзэмшил, хязгаарыг шалгаж, байт тоолж уншина — хэмжээнээс хэтэрвэл тэр даруй
413 (Starlette multipart шиг бүтнээр нь дискэнд буулгахгүй).
"""

import hashlib
import uuid
from collections import defaultdict
from dataclasses import dataclass
from datetime import UTC, datetime

from fastapi import Request, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import ClientDisconnect

from app.core import rate_limit
from app.core.config import settings
from app.live import access, source
from app.live.errors import live_error, message_for, not_found
from app.live.mastery import mastery
from app.live.storage import BlobStorage, StorageError, storage_configured
from app.models.enums import LiveGenerationKind, LiveMaterialKind, LiveMaterialStatus, LiveTier
from app.models.live import (
    LiveCard,
    LiveCardProgress,
    LiveGeneration,
    LiveMaterial,
    LiveTopic,
    LiveTopicProgress,
)
from app.models.user import User
from app.schemas.live import (
    LiveCardStats,
    LiveGenerationBrief,
    LiveMaterialCreate,
    LiveMaterialDetail,
    LiveMaterialSummary,
    LiveSection,
)
from app.schemas.live import LiveTopic as LiveTopicView
from app.services.ai import routing
from app.services.ai.capabilities import Capability


async def owned_material(db: AsyncSession, user: User, material_id: uuid.UUID) -> LiveMaterial:
    """Бусдын материалыг «байхгүй» гэж хариулна — байгаа эсэхийг ч задруулахгүй.

    Нэг удаагийн эрхтэй (багцгүй) хэрэглэгч зөвхөн эрхээр нээсэн материалаа
    хардаг; багцтай байхдаа оруулсан бусад нь багц авахад буцаж харагдана."""
    material = await db.get(LiveMaterial, material_id)
    if material is None or material.owner_id != user.id:
        raise not_found()
    if not (user.is_admin or user.has_plan):
        entitlement = await access.entitlement_for(db, user)
        if not entitlement.can_open(material.id):
            raise live_error(status.HTTP_402_PAYMENT_REQUIRED, "LIVE_PLAN_REQUIRED")
    return material


def assert_ai_configured(capability: Capability) -> None:
    if not routing.is_configured(capability):
        raise live_error(status.HTTP_503_SERVICE_UNAVAILABLE, "LIVE_AI_NOT_CONFIGURED")


async def create(db: AsyncSession, user: User, payload: LiveMaterialCreate) -> LiveMaterial:
    entitlement = await access.entitlement_for(db, user)
    kind = source.kind_for(payload.filename)
    if payload.size_bytes > settings.live_max_upload_bytes:
        raise live_error(status.HTTP_413_CONTENT_TOO_LARGE, "LIVE_FILE_TOO_LARGE")
    if not storage_configured():
        raise live_error(status.HTTP_503_SERVICE_UNAVAILABLE, "LIVE_STORAGE_NOT_CONFIGURED")
    assert_ai_configured(Capability.DOCUMENT)
    await access.assert_can_add_document(db, user, entitlement)
    await access.assert_ai_available(db, user, entitlement)
    rate_limit.enforce(
        f"live:upload:{user.id}",
        settings.live_upload_rate_limit_max,
        settings.live_upload_rate_limit_window_seconds,
    )

    material_id = uuid.uuid4()
    filename = source.clean_filename(payload.filename)
    material = LiveMaterial(
        id=material_id,
        owner_id=user.id,
        title=payload.title or source.default_title(filename),
        filename=filename,
        kind=kind,
        size_bytes=payload.size_bytes,
        storage_key=f"materials/{material_id}/original",
        status=LiveMaterialStatus.UPLOADING,
        # Тусдаа чагт байхгүй (эзэн 2026-10-01): Live-ийг ашиглах нь Үйлчилгээний
        # нөхцөлийн Live заалтыг (эрх, AI боловсруулалт) зөвшөөрсөн гэсэн үг.
        rights_confirmed_at=datetime.now(UTC),
    )
    db.add(material)
    if entitlement.tier == LiveTier.PASS:
        # Эрхийг энэ материалд холбоно — зэрэг ирсэн хоёр хүсэлтийн нэг л нь амжина.
        await db.flush()
        if await access.use_pass(db, entitlement, material_id) is None:
            await db.rollback()
            raise live_error(status.HTTP_402_PAYMENT_REQUIRED, "LIVE_PASS_USED")
    await db.commit()
    await db.refresh(material)
    return material


async def receive_content(
    db: AsyncSession,
    user: User,
    material: LiveMaterial,
    request: Request,
    storage: BlobStorage,
) -> LiveMaterial:
    if material.status != LiveMaterialStatus.UPLOADING:
        raise live_error(status.HTTP_409_CONFLICT, "LIVE_ALREADY_UPLOADED")
    limit = settings.live_max_upload_bytes
    declared = request.headers.get("content-length")
    if declared and declared.isdigit() and int(declared) > limit:
        raise live_error(status.HTTP_413_CONTENT_TOO_LARGE, "LIVE_FILE_TOO_LARGE")
    # Хэд хэдэн материал зэрэг бүртгээд дараа нь файлаа илгээх замаар хязгаар давахгүй.
    entitlement = await access.entitlement_for(db, user)
    await access.assert_can_add_document(db, user, entitlement, material)

    body = bytearray()
    try:
        async for chunk in request.stream():
            body.extend(chunk)
            if len(body) > limit:
                raise live_error(status.HTTP_413_CONTENT_TOO_LARGE, "LIVE_FILE_TOO_LARGE")
    except ClientDisconnect:
        raise live_error(status.HTTP_400_BAD_REQUEST, "LIVE_UPLOAD_MISSING") from None
    if not body:
        raise live_error(status.HTTP_400_BAD_REQUEST, "LIVE_FILE_EMPTY")
    data = bytes(body)
    mime = source.sniff(LiveMaterialKind(material.kind), data[:4096])

    try:
        await storage.put(material.storage_key, data, mime)
    except StorageError:
        raise live_error(status.HTTP_503_SERVICE_UNAVAILABLE, "LIVE_STORAGE_FAILED") from None
    material.size_bytes = len(data)
    material.sha256 = hashlib.sha256(data).hexdigest()
    material.status = LiveMaterialStatus.QUEUED
    material.error_code = None
    material.attempts = 0
    await db.commit()
    await db.refresh(material)
    return material


async def retry(db: AsyncSession, user: User, material: LiveMaterial) -> LiveMaterial:
    if material.status != LiveMaterialStatus.FAILED:
        raise live_error(status.HTTP_409_CONFLICT, "LIVE_NOT_RETRYABLE")
    assert_ai_configured(Capability.DOCUMENT)
    entitlement = await access.entitlement_for(db, user)
    await access.assert_can_add_document(db, user, entitlement, material)
    await access.assert_ai_available(db, user, entitlement, material.id)
    material.status = LiveMaterialStatus.QUEUED
    material.error_code = None
    material.attempts = 0
    await db.commit()
    await db.refresh(material)
    return material


async def rename(db: AsyncSession, material: LiveMaterial, title: str) -> LiveMaterial:
    material.title = title
    await db.commit()
    await db.refresh(material)
    return material


async def delete(db: AsyncSession, material: LiveMaterial) -> None:
    """Сэдэв, карт, тест, эзэмшил CASCADE; R2-ийн файлыг trigger дараалалд оруулна.
    Бэлэн болоогүй материалд ашигласан нэг удаагийн эрх буцна."""
    await access.release_pass(db, material)
    await db.delete(material)
    await db.commit()


# --- Эзэмшил ---------------------------------------------------------------


@dataclass
class TopicProgressView:
    topic: LiveTopic
    card_count: int
    progress: LiveTopicProgress | None
    mastery: int


async def topic_views(
    db: AsyncSession, user_id: uuid.UUID, material_ids: list[uuid.UUID]
) -> dict[uuid.UUID, list[TopicProgressView]]:
    """Материал тус бүрийн сэдвүүд эзэмшилтэйгээ, байрлалын дарааллаар."""
    if not material_ids:
        return {}
    topics = (
        (
            await db.execute(
                select(LiveTopic)
                .where(LiveTopic.material_id.in_(material_ids))
                .order_by(LiveTopic.material_id, LiveTopic.position)
            )
        )
        .scalars()
        .all()
    )
    topic_ids = [topic.id for topic in topics]
    card_counts = dict(
        (
            await db.execute(
                select(LiveCard.topic_id, func.count())
                .where(LiveCard.material_id.in_(material_ids))
                .group_by(LiveCard.topic_id)
            )
        ).all()
    )
    box_sums = dict(
        (
            await db.execute(
                select(LiveCard.topic_id, func.sum(LiveCardProgress.box))
                .join(LiveCardProgress, LiveCardProgress.card_id == LiveCard.id)
                .where(
                    LiveCard.material_id.in_(material_ids),
                    LiveCardProgress.user_id == user_id,
                )
                .group_by(LiveCard.topic_id)
            )
        ).all()
    )
    progress = {
        row.topic_id: row
        for row in (
            await db.execute(
                select(LiveTopicProgress).where(
                    LiveTopicProgress.user_id == user_id,
                    LiveTopicProgress.topic_id.in_(topic_ids),
                )
            )
        )
        .scalars()
        .all()
    }
    views: dict[uuid.UUID, list[TopicProgressView]] = defaultdict(list)
    for topic in topics:
        cards = int(card_counts.get(topic.id, 0))
        row = progress.get(topic.id)
        views[topic.material_id].append(
            TopicProgressView(
                topic=topic,
                card_count=cards,
                progress=row,
                mastery=mastery(
                    guide_read=bool(row and row.guide_read_at),
                    box_sum=int(box_sums.get(topic.id) or 0),
                    card_count=cards,
                    quiz_correct=row.quiz_correct if row else None,
                    quiz_total=row.quiz_total if row else None,
                ),
            )
        )
    return views


def _average(views: list[TopicProgressView]) -> int:
    return round(sum(view.mastery for view in views) / len(views)) if views else 0


def summary_view(material: LiveMaterial, topics: list[TopicProgressView]) -> LiveMaterialSummary:
    return LiveMaterialSummary(
        id=material.id,
        title=material.title,
        kind=material.kind,
        status=material.status,
        error_code=material.error_code,
        error_message=message_for(material.error_code),
        page_count=material.page_count,
        size_bytes=material.size_bytes,
        topic_count=len(topics),
        mastery=_average(topics),
        created_at=material.created_at,
        processed_at=material.processed_at,
    )


async def summary(db: AsyncSession, user: User, material: LiveMaterial) -> LiveMaterialSummary:
    views = await topic_views(db, user.id, [material.id])
    return summary_view(material, views.get(material.id, []))


async def list_for(db: AsyncSession, user: User) -> list[LiveMaterialSummary]:
    query = select(LiveMaterial).where(LiveMaterial.owner_id == user.id)
    entitlement = await access.entitlement_for(db, user)
    if entitlement.tier == LiveTier.PASS:
        query = query.where(LiveMaterial.id.in_(list(entitlement.pass_materials)))
    materials = (await db.execute(query.order_by(LiveMaterial.created_at.desc()))).scalars().all()
    views = await topic_views(db, user.id, [material.id for material in materials])
    return [summary_view(material, views.get(material.id, [])) for material in materials]


def generation_brief(generation: LiveGeneration | None) -> LiveGenerationBrief | None:
    if generation is None:
        return None
    return LiveGenerationBrief(
        id=generation.id,
        kind=generation.kind,
        status=generation.status,
        topic_id=generation.topic_id,
        error_code=generation.error_code,
        error_message=message_for(generation.error_code),
        created_at=generation.created_at,
        updated_at=generation.updated_at,
    )


async def card_stats(
    db: AsyncSession, user_id: uuid.UUID, material_id: uuid.UUID, now: datetime
) -> LiveCardStats:
    total = int(
        (
            await db.execute(select(func.count()).where(LiveCard.material_id == material_id))
        ).scalar_one()
    )
    reviewed, due, mastered = (
        await db.execute(
            select(
                func.count(),
                func.count().filter(LiveCardProgress.due_at <= now),
                func.count().filter(LiveCardProgress.box >= 4),
            )
            .select_from(LiveCardProgress)
            .join(LiveCard, LiveCard.id == LiveCardProgress.card_id)
            .where(LiveCard.material_id == material_id, LiveCardProgress.user_id == user_id)
        )
    ).one()
    new = total - int(reviewed)
    return LiveCardStats(total=total, due=new + int(due), new=new, mastered=int(mastered))


async def detail(db: AsyncSession, user: User, material: LiveMaterial) -> LiveMaterialDetail:
    views = (await topic_views(db, user.id, [material.id])).get(material.id, [])
    sections: list[LiveSection] = []
    current: tuple[int, str] | None = None
    for view in views:
        topic = view.topic
        key = (topic.section_position, topic.section_title)
        if key != current:
            sections.append(LiveSection(title=topic.section_title, topics=[]))
            current = key
        progress = view.progress
        sections[-1].topics.append(
            LiveTopicView(
                id=topic.id,
                title=topic.title,
                summary=topic.summary,
                pages=list(topic.pages or []),
                mastery=view.mastery,
                card_count=view.card_count,
                last_studied_at=progress.last_studied_at if progress else None,
                guide_read=bool(progress and progress.guide_read_at),
                quiz_percent=(
                    round(100 * (progress.quiz_correct or 0) / progress.quiz_total)
                    if progress and progress.quiz_total
                    else None
                ),
            )
        )
    whole = {
        generation.kind: generation
        for generation in (
            await db.execute(
                select(LiveGeneration).where(
                    LiveGeneration.material_id == material.id,
                    LiveGeneration.topic_id.is_(None),
                )
            )
        )
        .scalars()
        .all()
    }
    studied = [
        (view.progress.last_studied_at, view.topic.id)
        for view in views
        if view.progress and view.progress.last_studied_at
    ]
    base = summary_view(material, views)
    return LiveMaterialDetail(
        **base.model_dump(),
        summary=material.summary,
        sections=sections,
        cards=await card_stats(db, user.id, material.id, datetime.now(UTC)),
        full_quiz=generation_brief(whole.get(LiveGenerationKind.QUIZ)),
        exam=generation_brief(whole.get(LiveGenerationKind.EXAM)),
        last_studied_topic_id=max(studied)[1] if studied else None,
    )
