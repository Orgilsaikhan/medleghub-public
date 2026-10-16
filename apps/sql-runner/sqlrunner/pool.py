"""MySQL slot-уудын сан.

Зэрэг ажиллагааг slot-ийн тоогоор хязгаарлана. Ажиллагаа дууссаны дараа slot
арын дэвсгэрт цэвэрлэгдэж байж дараалалд буцна — дараагийн сурагч өмнөхийн
өөрчлөлтийг хэзээ ч харахгүй.
"""

import asyncio
import logging
from collections.abc import AsyncIterator, Coroutine
from contextlib import asynccontextmanager
from typing import Any

from sqlrunner.mysqld import MysqlInstance
from sqlrunner.settings import settings

logger = logging.getLogger("uvicorn.error")

RETRY_MIN_SECONDS = 5.0
RETRY_MAX_SECONDS = 60.0


class BusyError(Exception):
    """Бүх slot завгүй бөгөөд дараалалд хэт удаан хүлээлээ."""


class SlotPool:
    def __init__(self, size: int) -> None:
        self.instances = [MysqlInstance(index) for index in range(size)]
        self._ready: asyncio.Queue[MysqlInstance] = asyncio.Queue()
        self._tasks: set[asyncio.Task[None]] = set()

    @property
    def ready_count(self) -> int:
        return self._ready.qsize()

    async def start(self) -> None:
        results = await asyncio.gather(
            *(asyncio.to_thread(instance.start) for instance in self.instances),
            return_exceptions=True,
        )
        for instance, result in zip(self.instances, results, strict=True):
            if isinstance(result, BaseException):
                logger.error("slot %d эхэлсэнгүй: %s", instance.index, result)
                self._spawn(self._retry_start(instance))
            else:
                self._ready.put_nowait(instance)

        if self._ready.empty():
            raise RuntimeError("Нэг ч MySQL slot эхэлсэнгүй.")

    async def stop(self) -> None:
        for task in self._tasks:
            task.cancel()
        await asyncio.gather(*(asyncio.to_thread(instance.kill) for instance in self.instances))

    @asynccontextmanager
    async def acquire(self) -> AsyncIterator[MysqlInstance]:
        try:
            async with asyncio.timeout(settings.queue_timeout_seconds):
                while True:
                    instance = await self._ready.get()
                    if instance.alive():
                        break
                    # Дараалалд хүлээж байх зуур унасан (жишээ нь OOM).
                    self._spawn(self._recycle(instance))
        except TimeoutError:
            raise BusyError from None

        try:
            yield instance
        finally:
            instance.runs += 1
            self._spawn(self._recycle(instance))

    async def _recycle(self, instance: MysqlInstance) -> None:
        try:
            if instance.alive() and instance.runs < settings.restart_every:
                try:
                    await asyncio.to_thread(instance.reset)
                except Exception as error:
                    logger.warning(
                        "slot %d цэвэрлэгээ амжилтгүй — дахин эхлүүлнэ: %s", instance.index, error
                    )
                    await asyncio.to_thread(instance.start)
            else:
                await asyncio.to_thread(instance.start)
        except Exception as error:
            logger.error("slot %d дахин эхэлсэнгүй: %s", instance.index, error)
            await self._retry_start(instance)
            return

        self._ready.put_nowait(instance)

    async def _retry_start(self, instance: MysqlInstance) -> None:
        delay = RETRY_MIN_SECONDS
        while True:
            await asyncio.sleep(delay)
            try:
                await asyncio.to_thread(instance.start)
            except Exception as error:
                logger.error("slot %d дахин эхэлсэнгүй: %s", instance.index, error)
                delay = min(delay * 2, RETRY_MAX_SECONDS)
                continue
            self._ready.put_nowait(instance)
            return

    def _spawn(self, coroutine: Coroutine[Any, Any, None]) -> None:
        task = asyncio.create_task(coroutine)
        self._tasks.add(task)
        task.add_done_callback(self._tasks.discard)
