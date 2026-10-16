"""Цаана ажиллах дараалал — Postgres дээр, тусдаа үйлчилгээгүй.

Дараалал нь домэйн хүснэгтүүд өөрсдөө: `status = 'queued'` материал, үүсгэлт.
`FOR UPDATE SKIP LOCKED`-оор нэгийг авч `processing` болгоно. API нэг процесс
тул `notify()` шууд сэрээнэ; сэрээлт алдагдсан ч 10 секунд тутам шалгана.

Процесс дахин эхлэхэд (deploy, OOM) `processing` үлдсэнийг дахин дараалалд
оруулна — оролдлогын дээд тооноос хэтэрвэл `failed` (`LIVE_INTERRUPTED`).
"""

import asyncio
import contextlib
import logging
import uuid
from typing import Literal

from sqlalchemy import func, select, update

from app.core.config import settings
from app.live import pipeline
from app.live.pipeline import LiveContext
from app.models.enums import LiveGenerationStatus, LiveMaterialStatus
from app.models.live import LiveGeneration, LiveMaterial

logger = logging.getLogger(__name__)

JobKind = Literal["material", "generation"]
Job = tuple[JobKind, uuid.UUID]

POLL_SECONDS = 10.0
_wakeup: asyncio.Event | None = None


def notify() -> None:
    """Шинэ ажил дараалалд орсныг мэдэгдэнэ (HTTP замаас)."""
    if _wakeup is not None:
        _wakeup.set()


# Хэрэглэгч хүлээж байдаг богино үүсгэлт эхэнд, дараа нь материал.
_QUEUES: tuple[tuple[JobKind, type[LiveGeneration] | type[LiveMaterial]], ...] = (
    ("generation", LiveGeneration),
    ("material", LiveMaterial),
)


async def claim(ctx: LiveContext) -> Job | None:
    async with ctx.sessions() as db:
        for kind, model in _QUEUES:
            oldest = (
                select(model.id)
                .where(model.status == "queued")
                .order_by(model.updated_at)
                .limit(1)
                .with_for_update(skip_locked=True)
                .scalar_subquery()
            )
            claimed = (
                await db.execute(
                    update(model)
                    .where(model.id == oldest)
                    .values(status="processing", claimed_at=func.now(), attempts=model.attempts + 1)
                    .returning(model.id)
                )
            ).scalar_one_or_none()
            if claimed is not None:
                await db.commit()
                return kind, claimed
        await db.commit()
    return None


async def run_job(ctx: LiveContext, job: Job) -> None:
    kind, job_id = job
    try:
        if kind == "material":
            await pipeline.process_material(ctx, job_id)
        else:
            await pipeline.process_generation(ctx, job_id)
    except Exception:
        # Урьдчилан тооцоогүй алдаа — ажлыг гацаахгүй, хэрэглэгч дахин оролдоно.
        logger.exception("live: %s %s амжилтгүй", kind, job_id)
        async with ctx.sessions() as db:
            model = LiveMaterial if kind == "material" else LiveGeneration
            row = await db.get(model, job_id)
            if row is not None and row.status == "processing":
                row.status = "failed"
                row.error_code = "LIVE_AI_FAILED"
                await db.commit()


async def recover(ctx: LiveContext) -> None:
    """Эхлэхэд: өмнөх процессын дундаас нь тасарсан ажил."""
    async with ctx.sessions() as db:
        for model, failed in (
            (LiveMaterial, LiveMaterialStatus.FAILED),
            (LiveGeneration, LiveGenerationStatus.FAILED),
        ):
            stuck = model.status == "processing"
            await db.execute(
                update(model)
                .where(stuck, model.attempts >= settings.live_job_max_attempts)
                .values(status=failed, error_code="LIVE_INTERRUPTED")
            )
            await db.execute(update(model).where(stuck).values(status="queued"))
        await db.commit()


async def drain(ctx: LiveContext) -> int:
    """Дараалал хоосортол нэг нэгээр нь (тестэд). Хийсэн ажлын тоо."""
    done = 0
    while (job := await claim(ctx)) is not None:
        await run_job(ctx, job)
        done += 1
    return done


async def run_forever(ctx: LiveContext) -> None:
    global _wakeup
    _wakeup = asyncio.Event()
    await recover(ctx)
    slots = asyncio.Semaphore(settings.live_worker_concurrency)
    running: set[asyncio.Task[None]] = set()

    async def run(job: Job) -> None:
        try:
            await run_job(ctx, job)
        finally:
            slots.release()

    while True:
        await slots.acquire()
        # Шалгахаас ӨМНӨ цэвэрлэнэ — шалгах зуур ирсэн `notify()` алдагдахгүй.
        _wakeup.clear()
        try:
            job = await claim(ctx)
        except Exception:
            logger.exception("live: дарааллаас ажил авч чадсангүй")
            job = None
        if job is None:
            slots.release()
            with contextlib.suppress(TimeoutError):
                await asyncio.wait_for(_wakeup.wait(), timeout=POLL_SECONDS)
            continue
        task = asyncio.create_task(run(job))
        running.add(task)
        task.add_done_callback(running.discard)
