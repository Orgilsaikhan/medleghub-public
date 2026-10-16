"""AI давхаргын алдаа. HTTP-ийн алдаа биш — дуудагч нь өөрийн кодоор хөрвүүлнэ."""

from app.services.ai.types import Usage


class AIError(Exception):
    """`code` нь тогтвортой (`ai_requests.error_code`-д бичигдэнэ)."""

    def __init__(
        self,
        code: str,
        detail: str = "",
        *,
        retryable: bool = False,
        retry_after: float | None = None,
    ) -> None:
        super().__init__(f"{code}: {detail}" if detail else code)
        self.code = code
        # Provider-ийн шалтгаан (`service_unavailable`, `rate_limit_exceeded`, `quota_exceeded`…).
        self.detail = detail
        self.retryable = retryable
        # Provider «хэдэн секундын дараа» гэж хэлсэн бол (`Retry-After`, `retryDelay`).
        self.retry_after = retry_after


class AINotConfiguredError(AIError):
    """Загвар, түлхүүр тохируулаагүй — ажил эхлэхгүй."""

    def __init__(self, detail: str = "") -> None:
        super().__init__("not_configured", detail)


class AIBudgetError(AIError):
    """Төсөв хүрэлцэхгүй. `code`: `user_budget` (хэрэглэгчийн сар) / `pass_budget` (нэг
    удаагийн эрхийн материал) / `platform_budget` (платформ)."""


class AIOutputError(AIError):
    """Засах оролдлогын дараа ч хариу схемд таарсангүй."""

    def __init__(self, detail: str = "") -> None:
        super().__init__("invalid_output", detail)


class AIIncompleteError(AIError):
    """Хариу бүрэн биш (`incomplete`, `failed`) — ихэвчлэн гаралтын дээд токенд хүрсэн.

    Токен зарцуулагдсан тул зардлыг бичихэд `usage`-ийг агуулна.
    """

    def __init__(self, status: str, usage: Usage) -> None:
        super().__init__(f"status_{status}")
        self.usage = usage
