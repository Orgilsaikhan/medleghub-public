"""Task router: ажил бүрийг аль загвар хийхийг сонгоно.

Ажлын загварын дараалал (`routing.chain_for`) дотроос эхний БЭЛЭН загварыг авна.
Загвар бэлэн биш байх хоёр шалтгаан бий:

1. **Хөргөлт** (энэ процессын санах ойд). Google 429 (минутын хязгаар, өдрийн
   квот), 503 («high demand» ачаалал) эсвэл timeout өгсөн загварыг тодорхой хугацаанд
   алгасна. Хугацаа нь Google-ийн `retryDelay`, үгүй бол алдааны төрлөөс; дараалсан
   алдаанд өснө. Амжилттай дуудлага тоолуурыг тэглэнэ.
2. **Хэрэглээний хязгаар** (`Settings.ai_model_limits`, AI Studio-гоос хуулна).
   Google үлдсэн квотыг API-аар хэлдэггүй — `ai_requests`-ээс сүүлийн минутын
   хүсэлт, оролтын токен, 24 цагийн хүсэлтийг тоолж, 90%-д хүрмэгц алгасна.

Бүх загвар бэлэн биш бол хамгийн түрүүнд бэлэн болох хүртэл хүлээнэ (`AIService`).
API нэг процесс тул хөргөлт санах ойд хангалттай; олон процесс болбол Redis руу.
"""

import time
from collections.abc import Callable
from dataclasses import dataclass, field, replace
from datetime import UTC, datetime, timedelta

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.core.config import settings
from app.models.ai_request import AIRequest
from app.services.ai import prices
from app.services.ai.capabilities import Capability
from app.services.ai.errors import AIError, AINotConfiguredError
from app.services.ai.routing import ModelRoute, configured_chain

# Хязгаарын энэ хувьд хүрмэгц дараагийн загвар руу (Google-ийн тоололтой зөрүүгээс хамгаалж).
LIMIT_HEADROOM = 0.9
# Дараалсан ачаалал / timeout-ын хөргөлт: 4, 8, 16, 32, 64 с (дээд тал нь 2 минут).
BACKOFF_BASE_SECONDS = 4.0
BACKOFF_MAX_SECONDS = 120.0
# Google хугацаа хэлээгүй үед: минутын хязгаар — 1 минут, өдрийн квот — 1 цаг
# (дараа нь дахин шалгана).
RATE_LIMIT_SECONDS = 60.0
QUOTA_SECONDS = 3600.0


@dataclass
class Health:
    failures: int = 0
    # `time.monotonic()`-ийн утга — хана цагийн өөрчлөлтөд хамаарахгүй.
    cooldown_until: float = 0.0
    # `overloaded` / `rate_limited` / `quota` / `timeout`.
    reason: str | None = None
    last_error: str | None = None
    last_error_at: datetime | None = None
    # Админд харуулах хана цаг.
    available_at: datetime | None = None


def cooldown(error: AIError, failures: int) -> tuple[str, float]:
    """`(шалтгаан, секунд)` — алдааны төрөл ба дараалсан алдааны тооноос."""
    detail = (error.detail or "").lower()
    if error.code == "http_429":
        if "quota" in detail:
            return "quota", error.retry_after or QUOTA_SECONDS
        return "rate_limited", error.retry_after or RATE_LIMIT_SECONDS
    backoff = min(BACKOFF_MAX_SECONDS, BACKOFF_BASE_SECONDS * 2 ** (failures - 1))
    reason = "timeout" if error.code in ("timeout", "connection") else "overloaded"
    return reason, max(error.retry_after or 0.0, backoff)


class ModelHealth:
    """Загвар тутмын хөргөлт. Процесст нэг (`health`); тестэд цагийг солино."""

    def __init__(self, clock: Callable[[], float] = time.monotonic) -> None:
        self.clock = clock
        self._models: dict[str, Health] = {}

    def remaining(self, key: str) -> float:
        health = self._models.get(key)
        return max(0.0, health.cooldown_until - self.clock()) if health else 0.0

    def get(self, key: str) -> Health:
        return replace(self._models.get(key) or Health())

    def failure(self, key: str, error: AIError) -> float:
        health = self._models.setdefault(key, Health())
        health.failures += 1
        health.reason, seconds = cooldown(error, health.failures)
        health.cooldown_until = self.clock() + seconds
        health.last_error = error.code
        health.last_error_at = datetime.now(UTC)
        health.available_at = health.last_error_at + timedelta(seconds=seconds)
        return seconds

    def success(self, key: str) -> None:
        health = self._models.get(key)
        if health is not None:
            health.failures = 0
            health.cooldown_until = 0.0
            health.reason = None
            health.available_at = None


health = ModelHealth()


@dataclass(frozen=True)
class ModelUsage:
    minute_requests: int = 0
    minute_input_tokens: int = 0
    day_requests: int = 0


async def usage_by_model(db: AsyncSession, keys: list[str]) -> dict[str, ModelUsage]:
    """Сүүлийн минут, 24 цагийн дуудлага (амжилтгүй нь ч — Google ч тоолж магадгүй)."""
    if not keys:
        return {}
    now = datetime.now(UTC)
    minute = AIRequest.created_at >= now - timedelta(minutes=1)
    key = AIRequest.provider + ":" + AIRequest.model
    rows = (
        await db.execute(
            select(
                key,
                func.count().filter(minute),
                func.coalesce(func.sum(AIRequest.input_tokens).filter(minute), 0),
                func.count(),
            )
            .where(AIRequest.created_at >= now - timedelta(days=1), key.in_(keys))
            .group_by(key)
        )
    ).all()
    return {row[0]: ModelUsage(int(row[1]), int(row[2]), int(row[3])) for row in rows}


def limit_reason(key: str, usage: ModelUsage, input_tokens: int) -> str | None:
    """`rpm` / `tpm` / `rpd` — энэ дуудлагаар хязгаарын 90%-ийг давах бол."""
    limits = settings.ai_model_limits.get(key) or {}
    if (rpm := limits.get("rpm")) and usage.minute_requests + 1 > rpm * LIMIT_HEADROOM:
        return "rpm"
    tpm = limits.get("tpm")
    if tpm and usage.minute_input_tokens + input_tokens > tpm * LIMIT_HEADROOM:
        return "tpm"
    if (rpd := limits.get("rpd")) and usage.day_requests + 1 > rpd * LIMIT_HEADROOM:
        return "rpd"
    return None


def price_missing(route: ModelRoute) -> bool:
    """Production-д үнэгүй загварыг дуудахгүй — зардал тоологдохгүй бол төсөв хамгаалагдахгүй."""
    return settings.is_production and prices.price_for(route, datetime.now(UTC).date()) is None


@dataclass
class Pick:
    route: ModelRoute | None
    # `route` байхгүй үед: хамгийн түрүүнд бэлэн болох хүртэлх секунд.
    wait_seconds: float = 0.0
    # Алгассан загвар ба шалтгаан (лог, тест).
    skipped: list[tuple[str, str]] = field(default_factory=list)


class TaskRouter:
    def __init__(
        self, sessions: async_sessionmaker[AsyncSession], model_health: ModelHealth | None = None
    ) -> None:
        self._sessions = sessions
        self.health = model_health or health

    async def pick(self, capability: Capability, input_tokens: int) -> Pick:
        chain = [route for route in configured_chain(capability) if not price_missing(route)]
        if not chain:
            raise AINotConfiguredError(capability.value)
        limited = [route.key for route in chain if settings.ai_model_limits.get(route.key)]
        usage: dict[str, ModelUsage] = {}
        if limited:
            async with self._sessions() as db:
                usage = await usage_by_model(db, limited)

        pick = Pick(route=None, wait_seconds=float("inf"))
        for route in chain:
            remaining = self.health.remaining(route.key)
            if remaining > 0:
                pick.skipped.append((route.key, self.health.get(route.key).reason or "cooldown"))
                pick.wait_seconds = min(pick.wait_seconds, remaining)
                continue
            reason = limit_reason(route.key, usage.get(route.key, ModelUsage()), input_tokens)
            if reason is not None:
                pick.skipped.append((route.key, reason))
                window = 86_400.0 if reason == "rpd" else RATE_LIMIT_SECONDS
                pick.wait_seconds = min(pick.wait_seconds, window)
                continue
            pick.route = route
            pick.wait_seconds = 0.0
            return pick
        return pick
