"""Хүсэлтийн хязгаарлалт (rate limiting).

MVP-д process-дотоод sliding window хангалттай. Backend нь protocol-оор
тодорхойлогдсон тул олон instance ажиллуулах үед Redis хувилбараар солиход
router-ийн код өөрчлөгдөхгүй.
"""

import hashlib
import hmac
import ipaddress
import time
from collections import defaultdict, deque
from typing import Protocol

from fastapi import Request

from app.core.config import settings
from app.core.errors import RateLimitError


class RateLimitBackend(Protocol):
    def hit(self, key: str, limit: int, window_seconds: int) -> tuple[bool, int]:
        """Тоолуурыг нэмэгдүүлнэ. `(зөвшөөрөх эсэх, дахин оролдох секунд)` буцаана."""
        ...


class InMemoryRateLimitBackend:
    """Нэг процессын хүрээнд ажиллах sliding-window тоолуур."""

    def __init__(self) -> None:
        self._hits: dict[str, deque[float]] = defaultdict(deque)

    def hit(self, key: str, limit: int, window_seconds: int) -> tuple[bool, int]:
        now = time.monotonic()
        window_start = now - window_seconds
        bucket = self._hits[key]

        while bucket and bucket[0] < window_start:
            bucket.popleft()

        if len(bucket) >= limit:
            retry_after = max(1, int(bucket[0] + window_seconds - now) + 1)
            return False, retry_after

        bucket.append(now)

        # Ашиглагдаагүй түлхүүрүүд хуримтлагдахаас сэргийлнэ.
        if len(self._hits) > 10_000:
            self._prune(window_start)
        return True, 0

    def _prune(self, window_start: float) -> None:
        stale = [
            key for key, bucket in self._hits.items() if not bucket or bucket[-1] < window_start
        ]
        for key in stale:
            del self._hits[key]


backend: RateLimitBackend = InMemoryRateLimitBackend()


# Cloudflare Worker-ийн нэмдэг толгой (`apps/web/worker/client-ip.mjs`).
CLIENT_IP_HEADER = "x-medleghub-client-ip"
CLIENT_IP_SIGNATURE_HEADER = "x-medleghub-client-ip-signature"
CLIENT_IP_SIGNATURE_TOLERANCE_SECONDS = 300


def _digest(secret: str, timestamp: str, ip: str) -> str:
    return hmac.new(secret.encode(), f"{timestamp}.{ip}".encode(), hashlib.sha256).hexdigest()


def sign_client_ip(secret: str, ip: str, timestamp: int) -> str:
    """Worker-ийн гарын үсэг: `t=<unix>,v1=<hex(HMAC_SHA256(secret, "<t>.<ip>"))>`."""
    return f"t={timestamp},v1={_digest(secret, str(timestamp), ip)}"


def _signed_ip(request: Request) -> str | None:
    """Worker-ийн гарын үсэгтэй зочны IP. Гарын үсэг буруу, хуучирсан бол `None`.

    Нууц нь сүлжээгээр дамждаггүй тул лог-д үлдсэн ч ашиглагдахгүй. Барьж авсан
    гарын үсгээр 5 минутын дотор зөвхөн тэр IP-г л нэрлэж чадна.
    """
    secret = settings.client_ip_secret
    ip = (request.headers.get(CLIENT_IP_HEADER) or "").strip()
    signature = request.headers.get(CLIENT_IP_SIGNATURE_HEADER)
    if not (secret and ip and signature):
        return None
    fields = dict(part.strip().partition("=")[::2] for part in signature.split(","))
    timestamp, supplied = fields.get("t", ""), fields.get("v1", "")
    if not timestamp.isdigit() or not supplied:
        return None
    if abs(time.time() - int(timestamp)) > CLIENT_IP_SIGNATURE_TOLERANCE_SECONDS:
        return None
    if not hmac.compare_digest(_digest(secret, timestamp, ip), supplied):
        return None
    try:
        ipaddress.ip_address(ip)
    except ValueError:
        return None
    return ip


def _peer_ip(request: Request) -> str:
    """Caddy-ийн харсан TCP хаяг — Worker-ээр ирсэн бол Cloudflare-ийнх.

    Caddy (`trusted_proxies`-гүй) нь ирсэн X-Forwarded-For-ыг хаяж, зөвхөн энэ
    хаягийг бичдэг тул хуурамчаар бичих боломжгүй. Итгэмжит proxy нэмэгдвэл
    Caddy-ийн нэмсэн хаяг хамгийн баруун талд байна.
    """
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[-1].strip()
    return request.client.host if request.client else "unknown"


def _bucket(ip: str) -> str:
    """IPv6-г /64-өөр нэгтгэнэ — /64 доторх хаягаа сольж хязгаараас мултрахгүй."""
    try:
        address = ipaddress.ip_address(ip)
    except ValueError:
        return ip
    if isinstance(address, ipaddress.IPv6Address):
        if address.ipv4_mapped:
            return str(address.ipv4_mapped)
        return str(ipaddress.IPv6Network(f"{address}/64", strict=False))
    return str(address)


def client_ip(request: Request) -> str:
    """Rate limit-ийн түлхүүрт ашиглах зочны IP (IPv6 бол /64).

    Зам: хөтөч → Cloudflare Worker → api.medleghub.com (Caddy) → api.
    api.medleghub.com-д шууд хандах боломжтой тул X-Forwarded-For,
    CF-Connecting-IP-г хэн ч бичиж чадна — зөвхөн Worker-ийн гарын үсэгтэй IP-д
    итгэнэ. Гарын үсэггүй бол Caddy-ийн харсан TCP хаяг.
    """
    return _bucket(_signed_ip(request) or _peer_ip(request))


def enforce(key: str, limit: int, window_seconds: int) -> None:
    """IP биш, дурын түлхүүрээр тоолно (жишээ нь имэйл тус бүр). Хэтэрвэл 429."""
    if not settings.rate_limit_enabled:
        return
    allowed, retry_after = backend.hit(key, limit, window_seconds)
    if not allowed:
        raise RateLimitError(retry_after)


class RateLimiter:
    """FastAPI dependency: `Depends(RateLimiter("auth:login"))`.

    Тохиргоог дуудагдах үедээ уншина — route бүртгэгдэх үед биш. Ингэснээр
    орчны утга өөрчлөгдөхөд (жишээ нь тестэд) шууд мөрдөгдөнө.
    """

    def __init__(self, scope: str, limit: int | None = None, window_seconds: int | None = None):
        self.scope = scope
        self._limit = limit
        self._window_seconds = window_seconds

    async def __call__(self, request: Request) -> None:
        if not settings.rate_limit_enabled:
            return
        limit = self._limit or settings.auth_rate_limit_max
        window = self._window_seconds or settings.auth_rate_limit_window_seconds
        allowed, retry_after = backend.hit(f"{self.scope}:{client_ip(request)}", limit, window)
        if not allowed:
            raise RateLimitError(retry_after)
