"""Имэйлээр нэг удаагийн код (OTP) илгээх, шалгах — Supabase Auth-аар.

Supabase Auth-ийг зөвхөн «шуудан зөөгч, код шалгагч» болгон ашиглана:

    1. `send_code` — `POST /auth/v1/otp`. Supabase нь өөрийн SMTP-ээр
       «Confirm signup» (анх удаа) эсвэл «Magic Link» загвараар `{{ .Token }}`
       кодыг илгээнэ. Загварт холбоос биш, зөвхөн код байх ёстой
       (`README.md` → «Supabase»).
    2. `verify_code` — `POST /auth/v1/verify` (`type=email`). Амжилттай бол
       Supabase өөрийн сесс буцаадаг ч бид түүнийг ҮЛ ТООНО — нэвтрэлт манай
       JWT cookie-гоор л явна.

Supabase Auth дахь «сүүдэр» хэрэглэгч нь зөвхөн имэйл хаягтай бөгөөд Data API
унтраалттай, бүх хүснэгтэд RLS асаалттай тул түүний сесс юунд ч хандахгүй.
Бүртгэл устгах, имэйл солиход `delete_identity`-гээр түүнийг устгана.

Supabase бүх хүсэлтийг манай серверийн IP-ээс хүлээн авдаг тул түүний IP-ийн
хязгаар бүх хэрэглэгчид хуваагдана — имэйл тус бүрийн хязгаарыг бид өөрсдөө
тавьдаг (`api/v1/auth.py`).
"""

import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import httpx

from app.core.config import settings
from app.core.errors import AppError, RateLimitError

logger = logging.getLogger(__name__)

# Supabase нэг хэрэглэгчид дахин код илгээхийг анхдагчаар 60 секунд хориглодог.
RESEND_AFTER_SECONDS = 60


@asynccontextmanager
async def auth_client() -> AsyncGenerator[httpx.AsyncClient, None]:
    base = settings.supabase_url.rstrip("/") or "http://supabase.invalid"
    async with httpx.AsyncClient(
        base_url=f"{base}/auth/v1", timeout=settings.supabase_timeout_seconds
    ) as client:
        yield client


async def get_auth_client() -> AsyncGenerator[httpx.AsyncClient, None]:
    """Supabase Auth руу хандах client. Тестэд `httpx.MockTransport`-оор солино."""
    async with auth_client() as client:
        yield client


def _headers(key: str) -> dict[str, str]:
    # Шинэ `sb_…` түлхүүр нь JWT биш — зөвхөн `apikey`. Хуучин JWT түлхүүрийг
    # (anon, service_role) Authorization-д ч давхар өгнө.
    headers = {"apikey": key}
    if not key.startswith("sb_"):
        headers["Authorization"] = f"Bearer {key}"
    return headers


def _unavailable() -> AppError:
    return AppError(
        502,
        "EMAIL_PROVIDER_ERROR",
        "Имэйл илгээх үйлчилгээтэй холбогдож чадсангүй. Түр хүлээгээд дахин оролдоно уу.",
    )


def _error_code(response: httpx.Response) -> str:
    try:
        body = response.json()
    except ValueError:
        return "-"
    if not isinstance(body, dict):
        return "-"
    return str(body.get("error_code") or body.get("code") or body.get("error") or "-")


async def _post(client: httpx.AsyncClient, path: str, payload: dict) -> httpx.Response:
    try:
        return await client.post(path, json=payload, headers=_headers(settings.supabase_anon_key))
    except httpx.HTTPError as exc:
        raise _unavailable() from exc


async def send_code(client: httpx.AsyncClient, email: str) -> None:
    """`email` руу шинэ код илгээнэ. Supabase-д хэрэглэгч байхгүй бол үүсгэнэ."""
    response = await _post(client, "/otp", {"email": email, "create_user": True})
    if response.status_code == 429:
        # Supabase-ийн өөрийн хязгаар (имэйлийн цагийн хязгаар эсвэл нэг хэрэглэгчид
        # 60 секунд). Манай хязгаарлагчаас ялгахын тулд лог-д үлдээнэ.
        logger.warning("Supabase /otp → 429 %s", _error_code(response))
        raise RateLimitError(RESEND_AFTER_SECONDS)
    if response.status_code != 200:
        logger.warning("Supabase /otp → %s %s", response.status_code, _error_code(response))
        raise _unavailable()


async def verify_code(client: httpx.AsyncClient, email: str, code: str) -> bool:
    """Код зөв, хугацаа нь дуусаагүй бол `True`."""
    response = await _post(client, "/verify", {"type": "email", "email": email, "token": code})
    if response.status_code == 200:
        return True
    if response.status_code == 429:
        logger.warning("Supabase /verify → 429 %s", _error_code(response))
        raise RateLimitError(RESEND_AFTER_SECONDS)
    if response.status_code in (400, 401, 403, 404, 422):
        return False
    logger.warning("Supabase /verify → %s %s", response.status_code, _error_code(response))
    raise _unavailable()


async def delete_identity(client: httpx.AsyncClient, email: str) -> None:
    """Supabase Auth дахь `email`-ийн бичлэгийг устгана. Алдааг зөвхөн лог-д бичнэ.

    Манай бүртгэл аль хэдийн устсан/солигдсон — энд амжилтгүй болсон нь
    хэрэглэгчийн үйлдлийг буцаах шалтгаан биш.
    """
    key = settings.supabase_service_role_key
    if not settings.email_verification_enabled or not key:
        if settings.email_verification_enabled:
            logger.warning("SUPABASE_SERVICE_ROLE_KEY хоосон — Supabase Auth-д бичлэг үлдлээ.")
        return
    try:
        found = await client.get(
            "/admin/users", params={"filter": email, "per_page": 50}, headers=_headers(key)
        )
        if found.status_code != 200:
            logger.warning("Supabase admin/users → %s %s", found.status_code, _error_code(found))
            return
        body = found.json()
        users = body.get("users", []) if isinstance(body, dict) else []
        for candidate in users:
            if str(candidate.get("email", "")).lower() != email.lower():
                continue
            removed = await client.delete(f"/admin/users/{candidate['id']}", headers=_headers(key))
            if removed.status_code not in (200, 204):
                logger.warning(
                    "Supabase admin delete → %s %s", removed.status_code, _error_code(removed)
                )
    except (httpx.HTTPError, ValueError, KeyError, TypeError):
        logger.warning("Supabase Auth-аас %s-ийг устгаж чадсангүй", email, exc_info=True)
