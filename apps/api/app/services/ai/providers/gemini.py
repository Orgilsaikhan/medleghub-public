"""Google Gemini — Interactions API-ийн нимгэн REST client (`wire.py`-ийн хэв маяг).

Албан ёсны `google-genai` SDK нь `websockets<17`-г шаарддаг (Live-ийн
multiplayer WebSocket түүн дээр ажиллана) ба ~25 MB хамаарал нэмдэг тул
шууд httpx ашиглана.

Хүсэлт бүр `store: false` — Google харилцааг 55 хоног хадгалахгүй. Дахин
оролдлогыг энд хийхгүй: `AIService` нэг л удаа давтана.

https://ai.google.dev/api/interactions-api
"""

import base64
import logging
import re
from typing import Any

import httpx

from app.services.ai.errors import AIError, AIIncompleteError
from app.services.ai.types import Part, ProviderRequest, ProviderResult, Usage

logger = logging.getLogger(__name__)

INTERACTIONS_PATH = "/v1beta/interactions"
# Эдгээр нь түр зуурын — нэг удаа дахин оролдоно.
RETRYABLE_STATUSES = {408, 429, 500, 502, 503, 504}
# Төлбөр дууссан — бүх загварт адил, дахин оролдох нь тус болохгүй. Өдрийн квот
# (`quota_exceeded`) нь загвар тутамд тул router өөр загвар руу шилжинэ.
NON_RETRYABLE_REASONS = ("billing", "payment")
_RETRY_DELAY = re.compile(r'"retry_?delay"\s*:\s*"?(\d+(?:\.\d+)?)s?"?', re.IGNORECASE)


def _part(part: Part) -> dict[str, Any]:
    if part.kind == "text":
        return {"type": "text", "text": part.text or ""}
    data = base64.b64encode(part.data or b"").decode("ascii")
    return {"type": part.kind, "data": data, "mime_type": part.mime_type}


def build_body(request: ProviderRequest) -> dict[str, Any]:
    return {
        "model": request.model,
        "system_instruction": request.system,
        "input": [_part(part) for part in request.parts],
        "response_format": {
            "type": "text",
            "mime_type": "application/json",
            "schema": request.schema,
        },
        "generation_config": {
            "thinking_level": request.thinking_level,
            "max_output_tokens": request.max_output_tokens,
        },
        # ЗААВАЛ: оюутны материал Google-ийн талд хадгалагдахгүй.
        "store": False,
    }


def _retry_after(response: httpx.Response) -> float | None:
    """`Retry-After` толгой эсвэл алдааны `retryDelay` / `retry_delay` («32s»)."""
    header = response.headers.get("retry-after", "")
    if header.replace(".", "", 1).isdigit():
        return float(header)
    match = _RETRY_DELAY.search(response.text)
    return float(match.group(1)) if match else None


def _error(response: httpx.Response) -> tuple[str, str]:
    """Gemini-ийн алдааны объектоос `(status/code, message)` — ангилах, логт бичихэд.

    Мессеж нь Google-ийн тайлбар («… experiencing high demand …»), материалын агуулга биш.
    """
    try:
        error = response.json().get("error")
    except (ValueError, AttributeError):
        return "-", ""
    if not isinstance(error, dict):
        return "-", ""
    reason = str(error.get("status") or error.get("code") or "-").lower()
    return reason, str(error.get("message") or "")[:300]


def _output_text(body: dict[str, Any]) -> str:
    """Сүүлийн `model_output` алхмын текст (`jq '.steps[-1].content[0].text'`)."""
    for step in reversed(body.get("steps") or []):
        if isinstance(step, dict) and step.get("type") == "model_output":
            texts = [
                item.get("text", "")
                for item in step.get("content") or []
                if isinstance(item, dict) and item.get("type") == "text"
            ]
            return "".join(texts)
    # Хуучин хэлбэр: `outputs[].text`.
    outputs = body.get("outputs") or []
    return "".join(item.get("text", "") for item in outputs if isinstance(item, dict))


def _usage(body: dict[str, Any]) -> Usage:
    usage = body.get("usage") or {}

    def number(key: str) -> int:
        value = usage.get(key)
        return int(value) if isinstance(value, int | float) else 0

    return Usage(
        input_tokens=number("total_input_tokens"),
        cached_input_tokens=number("total_cached_tokens"),
        output_tokens=number("total_output_tokens"),
        reasoning_tokens=number("total_thought_tokens"),
    )


class GeminiProvider:
    name = "gemini"

    def __init__(self, api_key: str, base_url: str, client: httpx.AsyncClient | None = None):
        self._api_key = api_key
        self._client = client or httpx.AsyncClient(base_url=base_url)

    async def aclose(self) -> None:
        await self._client.aclose()

    async def generate(self, request: ProviderRequest) -> ProviderResult:
        try:
            response = await self._client.post(
                INTERACTIONS_PATH,
                json=build_body(request),
                headers={"x-goog-api-key": self._api_key},
                timeout=request.timeout_seconds,
            )
        except httpx.TimeoutException as exc:
            raise AIError("timeout", retryable=True) from exc
        except httpx.HTTPError as exc:
            raise AIError("connection", type(exc).__name__, retryable=True) from exc

        if response.status_code != 200:
            reason, message = _error(response)
            logger.warning(
                "Gemini %s → %s %s: %s", request.model, response.status_code, reason, message
            )
            retryable = response.status_code in RETRYABLE_STATUSES and not any(
                word in reason for word in NON_RETRYABLE_REASONS
            )
            raise AIError(
                f"http_{response.status_code}",
                reason,
                retryable=retryable,
                retry_after=_retry_after(response),
            )

        try:
            body = response.json()
        except ValueError as exc:
            raise AIError("bad_response", retryable=True) from exc
        if not isinstance(body, dict):
            raise AIError("bad_response", retryable=True)

        status = body.get("status")
        usage = _usage(body)
        if status != "completed":
            # `incomplete` нь ихэвчлэн гаралтын дээд токенд хүрсэн — дахин оролдох нь
            # мөн адил тасарна. Токен зарцуулсан тул дуудагч зардлыг бичнэ.
            raise AIIncompleteError(str(status), usage)
        return ProviderResult(text=_output_text(body), usage=usage, request_id=body.get("id"))
