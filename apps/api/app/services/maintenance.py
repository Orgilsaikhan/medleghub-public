"""Цаана тогтмол ажиллах ажил — товлосон бүртгэл устгах, хадгалах хугацаа мөрдүүлэх.

API процесс бүр (`main.lifespan`) `maintenance_interval_seconds` тутамд нэг
удаа ажиллуулна. Ажил бүр давтагдсан ч аюулгүй (идемпотент) тул олон процесс
зэрэг ажилласан ч асуудалгүй.
"""

import asyncio
import logging

from app.core.config import settings
from app.db.session import SessionFactory
from app.live import purge as live_purge
from app.live.storage import get_storage
from app.services import account_service, email_otp

logger = logging.getLogger(__name__)


async def run_once() -> None:
    async with SessionFactory() as db, email_otp.auth_client() as client:
        accounts = await account_service.purge_due_accounts(db, client)
        feedback, payments = await account_service.purge_expired_records(db)
        # Live: устгасан материалын R2 файл (бүртгэл устгасных ч), AI логийн хугацаа.
        blobs = await live_purge.drain_blob_deletions(db, get_storage())
        ai_requests = await live_purge.purge_ai_requests(db)
    if accounts or feedback or payments or blobs or ai_requests:
        logger.info(
            "maintenance: бүртгэл %s, санал хүсэлт %s, төлбөр %s, Live файл %s, AI лог %s устгалаа",
            accounts,
            feedback,
            payments,
            blobs,
            ai_requests,
        )


async def run_forever() -> None:
    while True:
        try:
            await run_once()
        except Exception:
            # Нэг удаагийн алдаа (жишээ нь сан түр салсан) ажлыг зогсоох ёсгүй.
            logger.exception("maintenance амжилтгүй")
        await asyncio.sleep(settings.maintenance_interval_seconds)
