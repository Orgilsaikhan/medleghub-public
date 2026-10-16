"""`AIService` — ажил (`Capability`) хүлээж аваад бүтэцтэй, шалгасан хариу буцаана.

Дуудлага бүрийн өмнө task router (`router.py`) ажлын загварын дарааллаас бэлэн
загварыг сонгоно. Нэг ажилд:
1. эхний дуудлага;
2. түр зуурын алдаа (Google 429 хязгаар, 503 «high demand», timeout) — тэр загвар
   хөргөгдөж, дараагийн бэлэн загвар руу ШУУД шилжинэ (`fallback`); бүгд хөргөгдсөн
   бол хамгийн түрүүнд бэлэн болохыг хүлээнэ. Эдгээр нь токен зарцуулаагүй тул үнэгүй;
3. хариу схемд таараагүй бол алдааг нь буцааж тэр загвараар НЭГ удаа засуулна.

Дуудлага бүрийн өмнө `budget_check`-ийг тэр загварын хамгийн их зардлаар нь дуудна;
дуудлага бүр (амжилтгүй нь ч) `ai_requests`-д өөрийн транзакцаар бичигдэнэ.
"""

import asyncio
import logging
import re
import time
import uuid
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field, replace
from datetime import UTC, date, datetime
from decimal import Decimal
from typing import Any, TypeVar

from pydantic import BaseModel, ValidationError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.core.config import settings
from app.models.ai_request import AIRequest
from app.services.ai import prices
from app.services.ai.capabilities import SPECS, Capability
from app.services.ai.errors import AIError, AIIncompleteError, AINotConfiguredError, AIOutputError
from app.services.ai.providers import AIProvider
from app.services.ai.router import ModelHealth, TaskRouter
from app.services.ai.routing import ModelRoute
from app.services.ai.schema import llm_schema
from app.services.ai.types import Part, ProviderRequest, Usage

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)

BudgetCheck = Callable[[Decimal], Awaitable[None]]
# Детерминист нэмэлт шалгалт — `ValueError` бол засуулах оролдлого хийнэ.
Validator = Callable[[Any], None]

# Нэг ажилд түр зуурын алдааны дээд тоо (бүх загварын нийлбэр) ба бүх загвар
# хөргөгдсөн үед хүлээх дээд тоо, нэг хүлээлтийн дээд хугацаа.
MAX_TRANSIENT_ERRORS = 5
MAX_WAITS = 5
MAX_WAIT_SECONDS = 60.0
_FENCE = re.compile(r"^\s*```(?:json)?\s*|\s*```\s*$")


@dataclass(frozen=True)
class CallContext:
    """Лог ба төсөвт: хэн, аль материал, prompt-ийн аль хувилбар."""

    user_id: uuid.UUID | None
    material_id: uuid.UUID | None
    prompt_version: str


@dataclass(frozen=True)
class RunInfo:
    provider: str
    model: str
    prompt_version: str
    cost_usd: Decimal
    calls: int


def _today() -> date:
    return datetime.now(UTC).date()


class AIService:
    def __init__(
        self,
        sessions: async_sessionmaker[AsyncSession],
        providers: dict[str, AIProvider] | None = None,
        *,
        sleep: Callable[[float], Awaitable[None]] = asyncio.sleep,
        model_health: ModelHealth | None = None,
    ) -> None:
        self._sessions = sessions
        self.router = TaskRouter(sessions, model_health)
        # Тестэд provider-ийг шууд өгнө; үгүй бол анх хэрэгтэй үед үүсгэнэ.
        self._providers: dict[str, AIProvider] = dict(providers or {})
        self._owned: list[AIProvider] = []
        self._sleep = sleep

    def _provider(self, name: str) -> AIProvider:
        if name not in self._providers:
            provider: AIProvider
            if name == "gemini":
                from app.services.ai.providers.gemini import GeminiProvider

                provider = GeminiProvider(settings.gemini_api_key, settings.gemini_api_url)
            elif name == "openrouter":
                from app.services.ai.providers.openrouter import OpenRouterProvider

                provider = OpenRouterProvider(
                    settings.openrouter_api_key, settings.openrouter_api_url
                )
            elif name == "fake":
                from app.services.ai.providers.fake import FakeProvider

                provider = FakeProvider()
            else:  # pragma: no cover - тохиргооны validator хориглоно
                raise AINotConfiguredError(f"provider {name}")
            self._providers[name] = provider
            self._owned.append(provider)
        return self._providers[name]

    async def aclose(self) -> None:
        for provider in self._owned:
            await provider.aclose()

    async def generate(
        self,
        capability: Capability,
        output: type[T],
        *,
        system: str,
        parts: list[Part],
        call: CallContext,
        input_tokens_estimate: int,
        budget_check: BudgetCheck | None = None,
        validate: Validator | None = None,
        context: dict[str, Any] | None = None,
    ) -> tuple[T, RunInfo]:
        spec = SPECS[capability]
        base = ProviderRequest(
            capability=capability.value,
            model="",
            system=system,
            parts=parts,
            schema=llm_schema(output),
            max_output_tokens=spec.max_output_tokens,
            thinking_level=spec.thinking_level,
            timeout_seconds=spec.timeout_seconds,
            context=context or {},
        )

        total_cost = Decimal(0)
        repair: tuple[ModelRoute, str] | None = None
        repaired = False
        previous: ModelRoute | None = None
        transient = waits = attempt = 0
        while True:
            if repair is not None:
                # Засуулах дуудлага нь алдаатай хариу өгсөн загвар руу.
                route, note = repair
                request = replace(base, model=route.model, parts=[*parts, Part.of_text(note)])
                kind = "repair"
            else:
                pick = await self.router.pick(capability, input_tokens_estimate)
                if pick.route is None:
                    if waits >= MAX_WAITS:
                        raise AIError("all_models_unavailable", retryable=True)
                    waits += 1
                    logger.info("AI: %s — бүх загвар түр бэлэн биш %s", capability, pick.skipped)
                    await self._sleep(min(pick.wait_seconds, MAX_WAIT_SECONDS))
                    continue
                route = pick.route
                request = replace(base, model=route.model)
                kind = "call" if previous is None else "retry" if route == previous else "fallback"
            price = self._price(route)
            if budget_check is not None:
                await budget_check(
                    prices.worst_case_usd(price, input_tokens_estimate, spec.max_output_tokens)
                )
            attempt += 1
            previous = route
            record = _Record(capability, route, call, attempt, kind, price)

            try:
                result = await self._provider(route.provider).generate(request)
            except AIIncompleteError as exc:
                await self._log(record.row(exc.usage, error=exc.code))
                raise
            except AIError as exc:
                await self._log(record.row(Usage(), error=exc.code))
                if exc.retryable and transient < MAX_TRANSIENT_ERRORS:
                    transient += 1
                    seconds = self.router.health.failure(route.key, exc)
                    logger.info("AI: %s хөргөгдлөө %.0f с (%s)", route.key, seconds, exc)
                    repair = None
                    continue
                raise
            self.router.health.success(route.key)

            try:
                parsed = _parse(output, result.text)
                if validate is not None:
                    validate(parsed)
            except (ValidationError, ValueError) as exc:
                row = record.row(result.usage, error="invalid_output", request_id=result.request_id)
                await self._log(row)
                total_cost += row.estimated_cost_usd
                if not repaired:
                    repaired = True
                    repair = (route, _repair_note(exc))
                    continue
                raise AIOutputError(str(exc)[:300]) from exc

            row = record.row(result.usage, request_id=result.request_id)
            await self._log(row)
            total_cost += row.estimated_cost_usd
            return parsed, RunInfo(
                provider=route.provider,
                model=route.model,
                prompt_version=call.prompt_version,
                cost_usd=total_cost,
                calls=attempt,
            )

    def _price(self, route: ModelRoute) -> prices.Price:
        price = prices.price_for(route, _today())
        if price is None:
            # Production-д router үнэгүй загварыг сонгохгүй (`router.price_missing`).
            logger.warning("AI: %s-д үнэ алга — 0 гэж тооцно", route.key)
            return prices.ZERO
        return price

    async def _log(self, row: AIRequest) -> None:
        """Ажил өөрөө бүтэлгүйтсэн ч зардал бичигдэх ёстой — тусдаа транзакц."""
        try:
            async with self._sessions() as db:
                db.add(row)
                await db.commit()
        except Exception:
            logger.exception("AI: ai_requests-д бичиж чадсангүй")


@dataclass
class _Record:
    """Нэг дуудлагын `ai_requests` мөрийг бүрдүүлнэ — хугацааг үүсгэснээс хэмжинэ."""

    capability: Capability
    route: ModelRoute
    call: CallContext
    attempt: int
    kind: str
    price: prices.Price
    started: float = field(default_factory=time.monotonic)

    def row(self, usage: Usage, *, error: str | None = None, request_id: str | None = None):
        return AIRequest(
            user_id=self.call.user_id,
            material_id=self.call.material_id,
            capability=self.capability.value,
            provider=self.route.provider,
            model=self.route.model,
            prompt_version=self.call.prompt_version,
            attempt=self.attempt,
            kind=self.kind,
            input_tokens=usage.input_tokens,
            cached_input_tokens=usage.cached_input_tokens,
            output_tokens=usage.output_tokens,
            reasoning_tokens=usage.reasoning_tokens,
            estimated_cost_usd=prices.cost_usd(self.price, usage),
            price_version=prices.PRICE_VERSION,
            duration_ms=int((time.monotonic() - self.started) * 1000),
            success=error is None,
            error_code=error,
            provider_request_id=request_id,
        )


def _parse(output: type[T], text: str) -> T:
    """JSON-оо «Here is the JSON…» гэх мэт өгүүлбэр, ``` блок дотор өгвөл гаргаж авна —
    засуулах (төлбөртэй) дуудлагаас өмнө."""
    cleaned = _FENCE.sub("", text)
    try:
        return output.model_validate_json(cleaned)
    except ValidationError:
        start, end = cleaned.find("{"), cleaned.rfind("}")
        if start <= 0 or end <= start:
            raise
        return output.model_validate_json(cleaned[start : end + 1])


def _repair_note(exc: Exception) -> str:
    detail = str(exc)
    if len(detail) > 1500:
        detail = detail[:1500] + "…"
    return (
        "Өмнөх хариу шаардлагад нийцсэнгүй:\n"
        f"{detail}\n\n"
        "Даалгаврыг дахин гүйцэтгэж, схемд яг таарсан JSON-ийг ЗӨВХӨН буцаа."
    )
