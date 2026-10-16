"""Wire (https://docs.wire.mn) төлбөрийн API-ийн нимгэн client.

Ашигладаг хэсэг нь гурав: PaymentIntent үүсгэх, түүнд hosted checkout нээх,
PaymentIntent-ийн төлөвийг татах. Төлбөрийн үнэний эх сурвалж нь ЗӨВХӨН
PaymentIntent-ийн `status` — webhook ирсэн ч, хэрэглэгч буцаж ирсэн ч
төлөвийг API-аас дахин шалгана (Wire-ийн зөвлөмж).

Албан ёсны `wirepayment` SDK нь синхрон тул async API-д шууд httpx ашиглана.
"""

import hashlib
import hmac
import json
import logging
import time
from collections.abc import AsyncGenerator
from typing import Any

import httpx

from app.core.config import settings
from app.core.errors import AppError, BadRequestError

logger = logging.getLogger(__name__)

SIGNATURE_HEADER = "WirePayment-Signature"
SIGNATURE_TOLERANCE_SECONDS = 300
SANDBOX_OPERATOR = "sandbox"


async def get_wire_client() -> AsyncGenerator[httpx.AsyncClient, None]:
    """Wire руу хандах client. Тестэд `httpx.MockTransport`-оор солино."""
    async with httpx.AsyncClient(
        base_url=settings.wire_api_url, timeout=settings.wire_timeout_seconds
    ) as client:
        yield client


def _unavailable() -> AppError:
    return AppError(
        502,
        "PAYMENT_PROVIDER_ERROR",
        "Төлбөрийн үйлчилгээтэй холбогдож чадсангүй. Түр хүлээгээд дахин оролдоно уу.",
    )


async def _request(
    client: httpx.AsyncClient,
    method: str,
    path: str,
    *,
    headers: dict[str, str] | None = None,
    **kwargs: Any,
) -> dict:
    # Түлхүүрийг хүсэлт бүрт уншина — client-ийг тестэд солиход ч шалгагдана.
    headers = {"Authorization": f"Bearer {settings.wire_secret_key}", **(headers or {})}
    try:
        response = await client.request(method, path, headers=headers, **kwargs)
    except httpx.HTTPError as exc:
        raise _unavailable() from exc
    if response.status_code != 200:
        # Хэрэглэгчид ерөнхий алдаа — харин `operator_not_allowed` мэт тохиргооны
        # алдааг логоос олохын тулд Wire-ийн кодыг бичнэ.
        logger.warning(
            "Wire %s %s → %s %s", method, path, response.status_code, _error_code(response)
        )
        raise _unavailable()
    try:
        body = response.json()
    except ValueError as exc:
        raise _unavailable() from exc
    if not isinstance(body, dict):
        raise _unavailable()
    return body


def _error_code(response: httpx.Response) -> str:
    """Wire-ийн алдааны объектоос `code` ба `request_id` (дэмжлэгт хандахад)."""
    try:
        error = response.json().get("error")
    except (ValueError, AttributeError):
        return "-"
    if not isinstance(error, dict):
        return "-"
    return f"{error.get('code', '-')} request_id={error.get('request_id', '-')}"


def allowed_operators() -> list[str]:
    """Live түлхүүр `sandbox`-ийг `operator_not_allowed`-аар татгалздаг.

    `.env`-д test mode-оос үлдсэн `sandbox`-ийг хасна. Жагсаалт хоосорвол
    талбарыг илгээхгүй — Wire идэвхтэй оператораас автоматаар сонгоно.
    """
    operators = settings.wire_allowed_operators
    if settings.wire_secret_key.startswith("sk_live_"):
        operators = [op for op in operators if op != SANDBOX_OPERATOR]
    return operators


async def create_payment_intent(
    client: httpx.AsyncClient,
    *,
    amount: int,
    description: str,
    metadata: dict[str, str],
    idempotency_key: str,
) -> dict:
    """`amount` нь БҮХЭЛ төгрөг (24,900 ₮ = 24_900).

    Wire-ийн «Money and time» баримт бичигт minor unit (×100) гэдэг ч live API
    дүнг QPay-ийн нэхэмжлэхэд шууд тавьдаг — 150000 гэж илгээхэд QR код
    150,000₮ нэхсэн (2026-09-28). ×100 бүү хий.
    """
    payload: dict[str, Any] = {
        "amount": amount,
        "currency": "MNT",
        "description": description,
        "metadata": metadata,
    }
    if operators := allowed_operators():
        payload["allowed_operators"] = operators
    return await _request(
        client,
        "POST",
        "/v1/payment_intents",
        json=payload,
        headers={"Idempotency-Key": idempotency_key},
    )


async def create_checkout_session(
    client: httpx.AsyncClient,
    *,
    payment_intent: str,
    success_url: str | None,
    cancel_url: str | None,
    idempotency_key: str,
) -> dict:
    """Hosted checkout (`pay.wire.mn/c/…`).

    JSON-оор илгээнэ. Wire-ийн гарын авлагын жишээ form (`curl -d`) хэлбэртэй ч
    live API нь form-ийг `400 invalid_json`-оор татгалздаг (2026-09-28).
    """
    payload = {"payment_intent": payment_intent}
    if success_url:
        payload["success_url"] = success_url
    if cancel_url:
        payload["cancel_url"] = cancel_url
    session = await _request(
        client,
        "POST",
        "/v1/checkout/sessions",
        json=payload,
        headers={"Idempotency-Key": idempotency_key},
    )
    # Хөтчийг энэ хаяг руу шилжүүлнэ — `javascript:` мэтийг хэзээ ч дамжуулахгүй.
    if not str(session.get("url", "")).startswith("https://"):
        raise _unavailable()
    return session


async def retrieve_payment_intent(client: httpx.AsyncClient, intent_id: str) -> dict:
    return await _request(client, "GET", f"/v1/payment_intents/{intent_id}")


def verify_webhook(payload: bytes, header: str | None, secret: str) -> dict:
    """`WirePayment-Signature: t=…,v1=…`-г шалгаж event-ийг буцаана.

    `v1` = hex(HMAC_SHA256(secret, f"{t}.{raw_body}")). Задлаагүй байтын эсрэг
    шалгана — JSON-ийг эхлээд задалбал байт өөрчлөгдөж signature эвдэрнэ.
    """
    invalid = BadRequestError("INVALID_SIGNATURE", "Webhook-ийн гарын үсэг буруу.")
    if not header:
        raise invalid

    timestamp: str | None = None
    signatures: list[str] = []
    for part in header.split(","):
        key, _, value = part.strip().partition("=")
        if key == "t":
            timestamp = value
        elif key == "v1":
            signatures.append(value)
    if not timestamp or not timestamp.isdigit() or not signatures:
        raise invalid
    if abs(time.time() - int(timestamp)) > SIGNATURE_TOLERANCE_SECONDS:
        raise invalid

    expected = hmac.new(
        secret.encode(), timestamp.encode() + b"." + payload, hashlib.sha256
    ).hexdigest()
    if not any(hmac.compare_digest(expected, candidate) for candidate in signatures):
        raise invalid

    try:
        event = json.loads(payload)
    except ValueError as exc:
        raise invalid from exc
    if not isinstance(event, dict):
        raise invalid
    return event


def event_payment_intent_id(event: dict) -> str | None:
    """Event-ийн PaymentIntent ID.

    Wire-ийн схемд `data` нь «event payload» гэж л бичигдсэн — `data.object`
    эсвэл шууд `data` байж болох тул хоёуланг нь шалгана. Аль ч тохиолдолд
    төлөвийг энэ ID-гаар API-аас дахин татна.
    """
    data = event.get("data")
    if not isinstance(data, dict):
        return None
    candidate = data.get("object", data)
    if not isinstance(candidate, dict):
        return None
    intent_id = candidate.get("id")
    return intent_id if isinstance(intent_id, str) else None
