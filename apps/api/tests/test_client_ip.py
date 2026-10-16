"""Rate limit-ийн түлхүүрт ашиглах зочны IP.

Зам: хөтөч → Cloudflare Worker → api.medleghub.com (Caddy) → api. Worker нь
зочны IP-г HMAC-аар гарын үсэг зурж дамжуулна (`apps/web/worker/client-ip.mjs`).
api.medleghub.com-д шууд хандах боломжтой тул гарын үсэггүй толгойд итгэхгүй.
"""

import time
from collections.abc import Callable

import httpx
import pytest
from starlette.requests import Request

from app.core import rate_limit
from app.core.config import settings
from app.core.rate_limit import (
    CLIENT_IP_HEADER,
    CLIENT_IP_SIGNATURE_HEADER,
    InMemoryRateLimitBackend,
    client_ip,
    sign_client_ip,
)

SECRET = "s" * 40
CADDY_PEER = "172.68.93.138"  # Cloudflare Worker-ийн гарах хаяг — Caddy үүнийг бичнэ.


@pytest.fixture(autouse=True)
def _secret(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(settings, "client_ip_secret", SECRET)


def _request(headers: dict[str, str], peer: str = "127.0.0.1") -> Request:
    return Request(
        {
            "type": "http",
            "method": "POST",
            "path": "/api/v1/auth/login",
            "headers": [(k.lower().encode(), v.encode()) for k, v in headers.items()],
            "client": (peer, 1234),
        }
    )


def _signed(ip: str, *, secret: str = SECRET, timestamp: int | None = None) -> dict[str, str]:
    stamp = int(time.time()) if timestamp is None else timestamp
    return {
        "x-forwarded-for": CADDY_PEER,
        CLIENT_IP_HEADER: ip,
        CLIENT_IP_SIGNATURE_HEADER: sign_client_ip(secret, ip, stamp),
    }


# --- Гарын үсэгтэй IP ------------------------------------------------------------


def test_signature_matches_the_worker() -> None:
    """`apps/web/worker/client-ip.test.mjs` ижил жишээг шалгана — хоёр тал зөрөхгүй."""
    secret = "medleghub-test-vector-secret"
    assert sign_client_ip(secret, "203.0.113.7", 1790000000) == (
        "t=1790000000,v1=e80954e099859c48d4f2333580fb37f57ff75bb0e08a3532a7447a554cf9ca92"
    )
    assert sign_client_ip(secret, "2001:db8::1", 1790000000) == (
        "t=1790000000,v1=4835ee01277d71b73aec401340292d5ce8e26b21fd183dd6681b66be98430a1e"
    )


def test_signed_visitor_ip_is_used() -> None:
    assert client_ip(_request(_signed("203.0.113.7"))) == "203.0.113.7"


def test_ipv6_visitors_share_their_64() -> None:
    first = client_ip(_request(_signed("2001:db8:1:2::1")))
    second = client_ip(_request(_signed("2001:db8:1:2:ffff::9")))
    other = client_ip(_request(_signed("2001:db8:1:3::1")))
    assert first == second == "2001:db8:1:2::/64"
    assert other != first


def test_ipv4_mapped_ipv6_counts_as_ipv4() -> None:
    assert client_ip(_request(_signed("::ffff:203.0.113.7"))) == "203.0.113.7"


# --- Хуурамч, хуучирсан гарын үсэг -------------------------------------------------


# Толгойг тест ажиллах мөчид үүсгэнэ — цуглуулах үед тооцвол удаан ажиллагаанд
# «5 минутын дараах» хугацаа цонхонд буцаж орно.
FORGED: dict[str, Callable[[], dict[str, str]]] = {
    # Толгойг гараар бичсэн — гарын үсэггүй.
    "unsigned": lambda: {"x-forwarded-for": CADDY_PEER, CLIENT_IP_HEADER: "203.0.113.7"},
    # Өөр нууцаар гарын үсэг зурсан.
    "wrong-secret": lambda: _signed("203.0.113.7", secret="x" * 40),
    # 5 минутаас хуучин, эсвэл ирээдүйн.
    "expired": lambda: _signed("203.0.113.7", timestamp=int(time.time()) - 301),
    "future": lambda: _signed("203.0.113.7", timestamp=int(time.time()) + 301),
    # Гарын үсгийг өөр IP-д шилжүүлсэн.
    "moved": lambda: {**_signed("203.0.113.7"), CLIENT_IP_HEADER: "198.51.100.1"},
    # Эвдэрсэн формат.
    "no-t": lambda: {**_signed("203.0.113.7"), CLIENT_IP_SIGNATURE_HEADER: "v1=abc"},
    "bad-t": lambda: {**_signed("203.0.113.7"), CLIENT_IP_SIGNATURE_HEADER: "t=abc,v1=abc"},
    # IP биш утгад зөв гарын үсэг — Worker ийм юм илгээхгүй.
    "not-an-ip": lambda: _signed("not-an-ip"),
    # Хэрэглэгчийн өөрийн X-Forwarded-For, CF-Connecting-IP-д итгэхгүй.
    "cf-header": lambda: {"x-forwarded-for": CADDY_PEER, "cf-connecting-ip": "203.0.113.7"},
}


@pytest.mark.parametrize("case", FORGED)
def test_unsigned_or_forged_ip_falls_back_to_caddy_peer(case: str) -> None:
    assert client_ip(_request(FORGED[case]())) == CADDY_PEER


def test_signatures_are_ignored_without_a_secret(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(settings, "client_ip_secret", "")
    assert client_ip(_request(_signed("203.0.113.7"))) == CADDY_PEER


def test_caddy_peer_is_the_last_forwarded_entry() -> None:
    """Итгэмжит proxy нэмэгдсэн ч Caddy-ийн нэмсэн (баруун талын) хаягийг авна."""
    request = _request({"x-forwarded-for": f"6.6.6.6, {CADDY_PEER}"})
    assert client_ip(request) == CADDY_PEER


def test_without_forwarded_header_the_tcp_peer_is_used() -> None:
    assert client_ip(_request({}, peer="198.51.100.9")) == "198.51.100.9"


# --- Бүтэн урсгал: /auth/password/forgot -----------------------------------------


async def test_visitors_behind_one_cloudflare_ip_get_their_own_limit(
    client: httpx.AsyncClient, api: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Өмнө нь бүх зочин нэг Cloudflare IP-ийн ард нэг сав хуваалцаж, шинэ
    төхөөрөмж шууд 429 авдаг байв."""
    monkeypatch.setattr(settings, "rate_limit_enabled", True)
    monkeypatch.setattr(settings, "auth_rate_limit_max", 2)
    monkeypatch.setattr(rate_limit, "backend", InMemoryRateLimitBackend())

    async def forgot(headers: dict[str, str], email: str) -> int:
        response = await client.post(
            f"{api}/auth/password/forgot", json={"email": email}, headers=headers
        )
        return response.status_code

    first = [await forgot(_signed("203.0.113.7"), f"a{n}@test.mn") for n in range(3)]
    assert first[-1] == 429
    # Нэг Cloudflare хаягаар ирсэн өөр зочин хязгаарт өртөхгүй.
    assert await forgot(_signed("198.51.100.23"), "b@test.mn") != 429
    # Хуурамч IP толгойгоор шинэ сав авч чадахгүй — Caddy-ийн хаягаар тоологдоно.
    spoofed = {"x-forwarded-for": CADDY_PEER, CLIENT_IP_HEADER: "192.0.2.1"}
    statuses = [await forgot(spoofed, f"c{n}@test.mn") for n in range(3)]
    assert statuses[-1] == 429
