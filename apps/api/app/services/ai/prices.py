"""Загварын үнэ — 1 сая токен тутамд USD, хүчин төгөлдөр болох огноотой.

Үнэ өөрчлөгдвөл ШИНЭ мөр нэмж, `PRICE_VERSION`-ийг шинэчилнэ — хуучин
`ai_requests` мөр өөрийн хувилбарыг хадгална. Үнэгүй загварыг production-д
дуудахгүй (`service.py`) — зардал тоологдохгүй бол төсөв хамгаалагдахгүй.

Эх сурвалж: https://ai.google.dev/gemini-api/docs/pricing (2026-09-30 шалгасан).
"""

from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from app.services.ai.routing import ModelRoute
from app.services.ai.types import Usage

PRICE_VERSION = "2026-10-01b"

_MILLION = Decimal(1_000_000)


@dataclass(frozen=True)
class Price:
    valid_from: date
    input: Decimal
    cached_input: Decimal
    # Бодлын токен ч энэ үнээр.
    output: Decimal


def _price(valid_from: date, input_: str, cached: str, output: str) -> Price:
    return Price(valid_from, Decimal(input_), Decimal(cached), Decimal(output))


ZERO = _price(date(2000, 1, 1), "0", "0", "0")

# 3.6–3.8 Flash-ийн үнэ 2027-01-01-нээс хоёр дахин өснө.
_FLASH_2026 = (
    _price(date(2026, 1, 1), "0.75", "0.075", "3.75"),
    _price(date(2027, 1, 1), "1.50", "0.15", "7.50"),
)

# Standard tier, текст/зураг/PDF оролт. Gemini 2.5 нь Interactions API дээр 404 тул энд алга.
PRICES: dict[str, tuple[Price, ...]] = {
    "gemini:gemini-3.8-flash": _FLASH_2026,
    "gemini:gemini-3.7-flash": _FLASH_2026,
    "gemini:gemini-3.6-flash": _FLASH_2026,
    "gemini:gemini-3.5-flash": (_price(date(2026, 1, 1), "1.50", "0.15", "9.00"),),
    "gemini:gemini-3.5-flash-lite": (_price(date(2026, 1, 1), "0.30", "0.03", "2.50"),),
    "gemini:gemini-3.1-flash-lite": (_price(date(2026, 1, 1), "0.25", "0.025", "1.50"),),
}


def _table_key(route: ModelRoute) -> str:
    """OpenRouter Google-ийн загварыг Google-ийн үнээр дамжуулдаг (шимтгэл нь кредит
    авахад) — `openrouter:google/gemini-3.8-flash` → `gemini:gemini-3.8-flash`."""
    if route.provider == "openrouter" and route.model.startswith("google/"):
        return f"gemini:{route.model.removeprefix('google/')}"
    return route.key


def price_for(route: ModelRoute, today: date) -> Price | None:
    """Тухайн өдөр хүчинтэй үнэ. Хуурамч AI, OpenRouter-ийн `:free` загвар үнэгүй;
    мэдэгдэхгүй загвар `None` (production-д дуудахгүй)."""
    if route.provider == "fake" or (
        route.provider == "openrouter" and route.model.endswith(":free")
    ):
        return ZERO
    rows = [row for row in PRICES.get(_table_key(route), ()) if row.valid_from <= today]
    return max(rows, key=lambda row: row.valid_from) if rows else None


def cost_usd(price: Price, usage: Usage) -> Decimal:
    if usage.cost_usd is not None:
        return usage.cost_usd.quantize(Decimal("0.000001"))
    return estimated_cost_usd(price, usage)


def estimated_cost_usd(price: Price, usage: Usage) -> Decimal:
    """Үнийн хүснэгтээр: кэшлэгдсэн оролт хямд; гаралт = хариу + бодлын токен.

    Gemini-ийн `total_output_tokens` бодлын токенийг агуулдаггүй (2026-10-01
    жинхэнэ дуудлагаар шалгасан: 12 ба 224), тиймээс нэмнэ.
    """
    cached = min(usage.cached_input_tokens, usage.input_tokens)
    fresh = usage.input_tokens - cached
    total = (
        fresh * price.input
        + cached * price.cached_input
        + (usage.output_tokens + usage.reasoning_tokens) * price.output
    )
    return (total / _MILLION).quantize(Decimal("0.000001"))


def worst_case_usd(price: Price, input_tokens: int, max_output_tokens: int) -> Decimal:
    """Дуудлагын дээд зардал — төсөв шалгахад (кэшгүй, гаралт дүүрэн)."""
    total = input_tokens * price.input + max_output_tokens * price.output
    return (total / _MILLION).quantize(Decimal("0.000001"))
