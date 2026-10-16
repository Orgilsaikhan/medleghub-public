"""C/C++ хөрвүүлэлтийн proxy.

Жинхэнэ хөрвүүлэгч шаардахгүй — `apps/compiler` үйлчилгээг
`httpx.MockTransport`-оор орлуулна. Хөрвүүлэгчийн өөрийн тестүүд нь
`apps/compiler/tests` дотор байна.
"""

import json
from collections.abc import AsyncGenerator, Callable

import httpx
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import rate_limit
from app.core.config import settings
from app.main import app
from app.services.compile_service import get_compiler_client
from tests.conftest import login_as, make_user

# WebAssembly-ийн хамгийн бага хүчинтэй толгой.
WASM = b"\x00asm\x01\x00\x00\x00"

Handler = Callable[[httpx.Request], httpx.Response]


def use_compiler(handler: Handler) -> list[httpx.Request]:
    """Хөрвүүлэгчийн хариуг загварчилж, түүн рүү очсон хүсэлтүүдийг цуглуулна."""
    seen: list[httpx.Request] = []

    def record(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return handler(request)

    async def override() -> AsyncGenerator[httpx.AsyncClient, None]:
        async with httpx.AsyncClient(
            transport=httpx.MockTransport(record), base_url="http://compiler"
        ) as client:
            yield client

    # `client` fixture нь teardown-д бүх override-ыг цэвэрлэнэ.
    app.dependency_overrides[get_compiler_client] = override
    return seen


async def _signed_in(client: httpx.AsyncClient, api: str, db: AsyncSession) -> None:
    await make_user(db, "hurvuulegch@suralts.mn")
    await login_as(client, api, "hurvuulegch@suralts.mn")


def _ok(_: httpx.Request) -> httpx.Response:
    return httpx.Response(200, content=WASM, headers={"x-compile-cache": "miss"})


async def test_compile_requires_login(client: httpx.AsyncClient, api: str) -> None:
    seen = use_compiler(_ok)

    response = await client.post(f"{api}/compile", json={"language": "c", "source": "int main(){}"})

    assert response.status_code == 401
    assert seen == [], "Нэвтрээгүй хэрэглэгчийн код хөрвүүлэгч рүү очих ёсгүй"


async def test_compile_returns_wasm(client: httpx.AsyncClient, api: str, db: AsyncSession) -> None:
    seen = use_compiler(_ok)
    await _signed_in(client, api, db)

    source = '#include <stdio.h>\nint main(void) { printf("Сайн уу"); return 0; }'
    response = await client.post(f"{api}/compile", json={"language": "c", "source": source})

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/wasm"
    assert response.headers["cache-control"] == "no-store"
    assert response.content == WASM

    # Хүсэлт хөрвүүлэгч рүү өөрчлөгдөөгүй хүрсэн эсэх.
    assert len(seen) == 1
    assert json.loads(seen[0].content) == {"language": "c", "source": source}


async def test_cache_hit_is_reported(client: httpx.AsyncClient, api: str, db: AsyncSession) -> None:
    use_compiler(lambda _: httpx.Response(200, content=WASM, headers={"x-compile-cache": "hit"}))
    await _signed_in(client, api, db)

    response = await client.post(
        f"{api}/compile", json={"language": "cpp", "source": "int main(){}"}
    )

    assert response.headers["x-compile-cache"] == "hit"


async def test_compile_error_returns_diagnostics(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    diagnostics = "main.c:3:5: error: expected ';' before 'return'"
    use_compiler(
        lambda _: httpx.Response(422, json={"code": "COMPILE_ERROR", "diagnostics": diagnostics})
    )
    await _signed_in(client, api, db)

    response = await client.post(f"{api}/compile", json={"language": "c", "source": "int main(){"})

    assert response.status_code == 422
    detail = response.json()["detail"]
    assert detail["code"] == "COMPILE_ERROR"
    assert detail["diagnostics"] == diagnostics


async def test_unknown_language_is_rejected(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    seen = use_compiler(_ok)
    await _signed_in(client, api, db)

    response = await client.post(
        f"{api}/compile", json={"language": "rust", "source": "fn main(){}"}
    )

    assert response.status_code == 422
    assert response.json()["detail"]["code"] == "VALIDATION_ERROR"
    assert seen == []


async def test_source_limit_counts_bytes_not_characters(
    client: httpx.AsyncClient, api: str, db: AsyncSession, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Кирилл үсэг 2 байт — тэмдэгтээр тоолбол хязгаарыг хоёр дахин давж болно."""
    seen = use_compiler(_ok)
    await _signed_in(client, api, db)
    monkeypatch.setattr(settings, "compile_max_source_bytes", 10)

    # 6 тэмдэгт боловч 12 байт.
    response = await client.post(f"{api}/compile", json={"language": "c", "source": "сайнуу"})

    assert response.status_code == 413
    assert response.json()["detail"]["code"] == "SOURCE_TOO_LARGE"
    assert seen == []


@pytest.mark.parametrize(
    ("handler", "status", "code"),
    [
        (lambda _: httpx.Response(504, json={"code": "COMPILE_TIMEOUT"}), 504, "COMPILE_TIMEOUT"),
        (lambda _: httpx.Response(503, json={"code": "COMPILER_BUSY"}), 503, "COMPILER_BUSY"),
        (lambda _: httpx.Response(500, text="boom"), 502, "COMPILER_ERROR"),
    ],
    ids=["timeout", "busy", "crash"],
)
async def test_compiler_failures_map_to_clear_errors(
    client: httpx.AsyncClient,
    api: str,
    db: AsyncSession,
    handler: Handler,
    status: int,
    code: str,
) -> None:
    use_compiler(handler)
    await _signed_in(client, api, db)

    response = await client.post(f"{api}/compile", json={"language": "c", "source": "int main(){}"})

    assert response.status_code == status
    assert response.json()["detail"]["code"] == code


@pytest.mark.parametrize(
    ("error", "status", "code"),
    [
        (httpx.ConnectError, 503, "COMPILER_UNAVAILABLE"),
        (httpx.ReadTimeout, 504, "COMPILE_TIMEOUT"),
    ],
    ids=["unreachable", "network-timeout"],
)
async def test_transport_errors_map_to_clear_errors(
    client: httpx.AsyncClient,
    api: str,
    db: AsyncSession,
    error: type[httpx.TransportError],
    status: int,
    code: str,
) -> None:
    def fail(request: httpx.Request) -> httpx.Response:
        raise error("хөрвүүлэгч хариу өгсөнгүй", request=request)

    use_compiler(fail)
    await _signed_in(client, api, db)

    response = await client.post(f"{api}/compile", json={"language": "c", "source": "int main(){}"})

    assert response.status_code == status
    assert response.json()["detail"]["code"] == code


async def test_compile_is_rate_limited_per_user(
    client: httpx.AsyncClient, api: str, db: AsyncSession, monkeypatch: pytest.MonkeyPatch
) -> None:
    use_compiler(_ok)
    await _signed_in(client, api, db)

    monkeypatch.setattr(settings, "rate_limit_enabled", True)
    monkeypatch.setattr(settings, "compile_rate_limit_max", 2)
    monkeypatch.setattr(rate_limit, "backend", rate_limit.InMemoryRateLimitBackend())

    body = {"language": "c", "source": "int main(){}"}
    assert (await client.post(f"{api}/compile", json=body)).status_code == 200
    assert (await client.post(f"{api}/compile", json=body)).status_code == 200

    blocked = await client.post(f"{api}/compile", json=body)
    assert blocked.status_code == 429
    assert "retry-after" in blocked.headers


async def test_large_module_is_gzipped(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    """C++ модуль ~200 KB — сүлжээгээр шахаж илгээнэ."""
    module = WASM + bytes(range(256)) * 64
    use_compiler(lambda _: httpx.Response(200, content=module))
    await _signed_in(client, api, db)

    response = await client.post(
        f"{api}/compile",
        json={"language": "cpp", "source": "int main(){}"},
        headers={"Accept-Encoding": "gzip"},
    )

    assert response.status_code == 200
    assert response.headers["content-encoding"] == "gzip"
    # Кэш нь шахсан ба шахаагүй хариуг ялгах ёстой. CORS middleware өөрийн
    # `Origin`-ийг нэмж болно (Starlette-ийн шинэ хувилбарууд үргэлж нэмдэг).
    vary = {value.strip().lower() for value in response.headers["vary"].split(",")}
    assert "accept-encoding" in vary
    assert int(response.headers["content-length"]) < len(module) // 4
    # httpx нь gzip-ийг автоматаар задална — хөтөч ч мөн адил.
    assert response.content == module


@pytest.mark.parametrize("accept", ["identity", "gzip;q=0"])
async def test_module_is_sent_plain_when_gzip_is_refused(
    client: httpx.AsyncClient, api: str, db: AsyncSession, accept: str
) -> None:
    module = WASM + bytes(range(256)) * 64
    use_compiler(lambda _: httpx.Response(200, content=module))
    await _signed_in(client, api, db)

    response = await client.post(
        f"{api}/compile",
        json={"language": "c", "source": "int main(){}"},
        headers={"Accept-Encoding": accept},
    )

    assert response.status_code == 200
    assert "content-encoding" not in response.headers
    assert response.content == module
