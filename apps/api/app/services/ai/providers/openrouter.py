"""OpenRouter — OpenAI-тэй нийцтэй Chat Completions-ийн нимгэн REST client.

Google виртуал карт хүлээж авахгүй тул Gemini-г одоохондоо OpenRouter-оор (ижил
загвар, Google-ийн үнэ; шимтгэл нь кредит худалдан авахад). Загварын нэр нь
`google/gemini-3.8-flash` хэлбэртэй.

Хүсэлт бүр:
- `provider.data_collection: "deny"` — сургалтад ашигладаг endpoint руу явахгүй
  (оюутны материал); `OPENROUTER_ZDR=true` бол зөвхөн мэдээлэл хадгалдаггүй endpoint;
- PDF-ийг загварын өөрийн уншлагаар (`file-parser` → `native`) — OCR-ийн нэмэлт
  төлбөргүй, диаграм, хүснэгт ч уншигдана;
- `usage.cost` — OpenRouter-ийн бодит зардлыг `ai_requests`-д бичнэ.

https://openrouter.ai/docs/api-reference/overview
"""

import base64
import logging
from decimal import Decimal, InvalidOperation
from typing import Any

import httpx

from app.core.config import settings
from app.services.ai.errors import AIError, AIIncompleteError
from app.services.ai.types import Part, ProviderRequest, ProviderResult, Usage

logger = logging.getLogger(__name__)

COMPLETIONS_PATH = "/chat/completions"
# 529 — upstream provider хэт ачаалалтай.
RETRYABLE_STATUSES = {408, 429, 500, 502, 503, 504, 529}


def _part(part: Part) -> dict[str, Any]:
    if part.kind == "text":
        return {"type": "text", "text": part.text or ""}
    data = base64.b64encode(part.data or b"").decode("ascii")
    url = f"data:{part.mime_type};base64,{data}"
    if part.kind == "image":
        return {"type": "image_url", "image_url": {"url": url}}
    return {"type": "file", "file": {"filename": "material.pdf", "file_data": url}}


def strict_schema(node: Any) -> Any:
    """`strict` JSON Schema: объект бүр `additionalProperties: false` (LLM-ийн схемд
    бүх талбар аль хэдийн `required`)."""
    if isinstance(node, list):
        return [strict_schema(item) for item in node]
    if not isinstance(node, dict):
        return node
    out = {key: strict_schema(value) for key, value in node.items()}
    if out.get("type") == "object" and "properties" in out:
        out["properties"] = {name: strict_schema(prop) for name, prop in node["properties"].items()}
        out["additionalProperties"] = False
    return out


def build_body(request: ProviderRequest) -> dict[str, Any]:
    provider: dict[str, Any] = {
        # ЗААВАЛ: оюутны материалыг сургалтад ашигладаг endpoint руу илгээхгүй.
        "data_collection": "deny",
        # JSON схем, бодлын түвшинг дэмждэг endpoint л.
        "require_parameters": True,
    }
    if settings.openrouter_zdr:
        provider["zdr"] = True
    return {
        "model": request.model,
        "messages": [
            {"role": "system", "content": request.system},
            {"role": "user", "content": [_part(part) for part in request.parts]},
        ],
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "name": "output",
                "strict": True,
                "schema": strict_schema(request.schema),
            },
        },
        "max_tokens": request.max_output_tokens,
        # Gemini 3-т шууд `thinkingLevel` болж хувирна. Бодлын текстийг буцаахгүй.
        "reasoning": {"effort": request.thinking_level, "exclude": True},
        "plugins": [{"id": "file-parser", "pdf": {"engine": "native"}}],
        "provider": provider,
        "usage": {"include": True},
    }


def _error(response: httpx.Response) -> tuple[str, str]:
    """`(ангилал, мессеж)`. OpenRouter: `{"error": {"code": 402, "message": "…"}}`."""
    try:
        error = response.json().get("error")
    except (ValueError, AttributeError):
        return "-", ""
    if not isinstance(error, dict):
        return "-", ""
    message = str(error.get("message") or "")[:300]
    lowered = message.lower()
    if response.status_code == 402 or "credit" in lowered:
        return "payment_required", message
    if response.status_code == 429:
        return "rate_limit_exceeded", message
    if "no endpoints" in lowered:
        # Өгөгдлийн бодлого (`data_collection`, `zdr`)-д таарах endpoint алга.
        return "no_endpoints", message
    return str(error.get("code") or "-").lower(), message


def _retry_after(response: httpx.Response) -> float | None:
    header = response.headers.get("retry-after", "")
    return float(header) if header.replace(".", "", 1).isdigit() else None


def _usage(body: dict[str, Any]) -> Usage:
    usage = body.get("usage") or {}

    def number(value: object) -> int:
        return int(value) if isinstance(value, int | float) else 0

    completion = number(usage.get("completion_tokens"))
    reasoning = number((usage.get("completion_tokens_details") or {}).get("reasoning_tokens"))
    cost: Decimal | None = None
    if isinstance(usage.get("cost"), int | float):
        try:
            cost = Decimal(str(usage["cost"]))
        except InvalidOperation:
            cost = None
    return Usage(
        input_tokens=number(usage.get("prompt_tokens")),
        cached_input_tokens=number((usage.get("prompt_tokens_details") or {}).get("cached_tokens")),
        # OpenAI-ийн `completion_tokens` бодлын токенийг агуулдаг — давхар тоолохгүй.
        output_tokens=max(0, completion - reasoning),
        reasoning_tokens=reasoning,
        cost_usd=cost,
    )


class OpenRouterProvider:
    name = "openrouter"

    def __init__(self, api_key: str, base_url: str, client: httpx.AsyncClient | None = None):
        self._api_key = api_key
        self._client = client or httpx.AsyncClient(base_url=base_url)

    async def aclose(self) -> None:
        await self._client.aclose()

    async def generate(self, request: ProviderRequest) -> ProviderResult:
        try:
            response = await self._client.post(
                COMPLETIONS_PATH,
                json=build_body(request),
                headers={"Authorization": f"Bearer {self._api_key}", "X-Title": "MedlegHub"},
                timeout=request.timeout_seconds,
            )
        except httpx.TimeoutException as exc:
            raise AIError("timeout", retryable=True) from exc
        except httpx.HTTPError as exc:
            raise AIError("connection", type(exc).__name__, retryable=True) from exc

        if response.status_code != 200:
            reason, message = _error(response)
            logger.warning(
                "OpenRouter %s → %s %s: %s", request.model, response.status_code, reason, message
            )
            raise AIError(
                f"http_{response.status_code}",
                reason,
                retryable=response.status_code in RETRYABLE_STATUSES,
                retry_after=_retry_after(response),
            )
        try:
            body = response.json()
        except ValueError as exc:
            raise AIError("bad_response", retryable=True) from exc
        if not isinstance(body, dict):
            raise AIError("bad_response", retryable=True)
        # Upstream алдаа заримдаа 200 дотор ирдэг.
        if isinstance(body.get("error"), dict):
            error = body["error"]
            code = error.get("code")
            logger.warning("OpenRouter %s → %s: %s", request.model, code, error.get("message"))
            retryable = not isinstance(code, int) or code in RETRYABLE_STATUSES
            raise AIError(f"upstream_{code}", str(error.get("message") or ""), retryable=retryable)

        choices = body.get("choices") or []
        choice = choices[0] if choices and isinstance(choices[0], dict) else {}
        usage = _usage(body)
        if choice.get("finish_reason") == "length":
            raise AIIncompleteError("length", usage)
        content = (choice.get("message") or {}).get("content")
        if not isinstance(content, str) or not content.strip():
            raise AIIncompleteError(str(choice.get("finish_reason") or "empty"), usage)
        return ProviderResult(text=content, usage=usage, request_id=body.get("id"))
