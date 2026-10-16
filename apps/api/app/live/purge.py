"""`maintenance` ажлын Live алхмууд: R2-ийн файл устгах, AI логийн хадгалах хугацаа."""

import logging
from datetime import UTC, datetime, timedelta

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.live.storage import BlobStorage, StorageError
from app.models.ai_request import AIRequest
from app.models.live import LiveBlobDeletion

logger = logging.getLogger(__name__)

BATCH = 50
# Олон удаа бүтэлгүйтсэн файлыг логт анхааруулна (устгахыг оролдсоор байна).
WARN_AFTER_ATTEMPTS = 10


async def drain_blob_deletions(db: AsyncSession, storage: BlobStorage) -> int:
    """Устгасан материалын R2 файлыг устгана. Устгасан файлын тоо."""
    rows = (
        (
            await db.execute(
                select(LiveBlobDeletion).order_by(LiveBlobDeletion.created_at).limit(BATCH)
            )
        )
        .scalars()
        .all()
    )
    removed = 0
    for row in rows:
        try:
            await storage.delete(row.storage_key)
        except StorageError:
            row.attempts += 1
            if row.attempts == WARN_AFTER_ATTEMPTS:
                logger.warning("live: %s-г устгаж чадахгүй байна", row.storage_key)
            continue
        await db.delete(row)
        removed += 1
    await db.commit()
    return removed


async def purge_ai_requests(db: AsyncSession) -> int:
    cutoff = datetime.now(UTC) - timedelta(days=settings.ai_request_retention_days)
    result = await db.execute(delete(AIRequest).where(AIRequest.created_at < cutoff))
    await db.commit()
    return result.rowcount or 0
