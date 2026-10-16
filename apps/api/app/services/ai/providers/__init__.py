"""AI provider-ууд. Provider нь өгөгдлийн сан, төсөв мэдэхгүй — зөвхөн HTTP дуудлага."""

from typing import Protocol

from app.services.ai.types import ProviderRequest, ProviderResult


class AIProvider(Protocol):
    name: str

    async def generate(self, request: ProviderRequest) -> ProviderResult:
        """JSON текст буцаана. Алдаанд `AIError` (`retryable` тэмдэгтэй)."""
        ...

    async def aclose(self) -> None: ...
