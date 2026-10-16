"""Тохиргоог загварын дараалал (`ModelRoute`) болгох ЦОРЫН ГАНЦ газар.

Загварын нэр (`gemini-…`) кодын өөр хаана ч бичигдэхгүй — зөвхөн тохиргоо
(`AI_*_MODELS`) ба үнийн хүснэгтэд (`prices.py`). Загвар солиход код өөрчлөгдөхгүй.
Дарааллаас аль нь ажиллахыг `router.py` (эрүүл мэнд, хязгаар) сонгоно.
"""

from dataclasses import dataclass

from app.core.config import settings
from app.services.ai.capabilities import SPECS, Capability


@dataclass(frozen=True)
class ModelRoute:
    provider: str
    model: str

    @property
    def key(self) -> str:
        """Үнийн хүснэгт, хязгаар, лог дахь нэр: `gemini:gemini-3.8-flash`."""
        return f"{self.provider}:{self.model}"

    @classmethod
    def parse(cls, value: str) -> "ModelRoute":
        provider, _, model = value.partition(":")
        return cls(provider=provider, model=model)


def provider_configured(provider: str) -> bool:
    if provider == "gemini":
        return bool(settings.gemini_api_key)
    if provider == "openrouter":
        return bool(settings.openrouter_api_key)
    # Хуурамч AI түлхүүргүй ажиллана (production-д тохиргоо хориглоно).
    return provider == "fake" and not settings.is_production


def chain_for(capability: Capability) -> list[ModelRoute]:
    """Тохиргооны дараалал (давхардалгүй). `AI_MODELS` өгсөн бол бүх ажилд тэр."""
    values: list[str] = settings.ai_models or getattr(settings, SPECS[capability].route_setting)
    chain: list[ModelRoute] = []
    for value in values:
        route = ModelRoute.parse(value)
        if route not in chain:
            chain.append(route)
    return chain


def configured_chain(capability: Capability) -> list[ModelRoute]:
    """Түлхүүр нь тохирсон provider-ийн загварууд л."""
    return [route for route in chain_for(capability) if provider_configured(route.provider)]


def is_configured(capability: Capability) -> bool:
    return bool(configured_chain(capability))
