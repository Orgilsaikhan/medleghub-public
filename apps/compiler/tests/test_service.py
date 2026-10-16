"""Жинхэнэ emcc-ээр хөрвүүлэх — зөвхөн Docker image дотор ажиллана.

    docker build --target test -t medleghub-compiler-test apps/compiler
    docker run --rm --read-only --tmpfs /tmp medleghub-compiler-test

emcc байхгүй орчинд бүгд алгасагдана.
"""

import asyncio
import os
import shutil
from collections.abc import AsyncGenerator
from pathlib import Path

import httpx
import pytest

from compiler import main
from compiler.cache import SizedLRUCache
from compiler.diagnostics import TRUNCATED_NOTE
from compiler.runner import compile_source
from compiler.settings import settings
from compiler.toolchain import TOOLCHAINS
from compiler.wasm import WARNINGS_SECTION
from tests.wasm_helpers import custom_sections, exports, imports

pytestmark = pytest.mark.skipif(
    shutil.which("emcc") is None, reason="emcc байхгүй — Docker image дотор ажиллуулна"
)

# Хөтөчийн worker (`apps/web/src/lib/sandbox/native-worker-source.ts`) WASI-аас
# гадна зөвхөн эдгээрийг хангадаг. Туг өөрчлөгдөж шинэ импорт нэмэгдвэл энд
# баригдана — эс бөгөөс програм хөтөч дээр ачаалагдахгүй.
WORKER_ENV_IMPORTS = {("env", "emscripten_notify_memory_growth")}

HELLO_C = """\
#include <stdio.h>

int main(void) {
    printf("Сайн байна уу!\\n");
    return 0;
}
"""

EXCEPTIONS_CPP = """\
#include <iostream>
#include <stdexcept>
#include <vector>

int main() {
    std::vector<int> values{1, 2, 3};
    try {
        values.at(10);
    } catch (const std::out_of_range &error) {
        std::cout << "барьлаа: " << error.what() << std::endl;
    }
    return 0;
}
"""


@pytest.fixture(autouse=True)
def isolated(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Тест бүр хоосон кэш, чөлөөтэй слот, өөрийн түр хавтастай."""
    monkeypatch.setattr(main, "cache", SizedLRUCache(settings.cache_bytes))
    monkeypatch.setattr(main, "slots", asyncio.Semaphore(2))
    monkeypatch.setattr(settings, "work_dir", str(tmp_path))


@pytest.fixture
async def client() -> AsyncGenerator[httpx.AsyncClient, None]:
    transport = httpx.ASGITransport(app=main.app)
    async with httpx.AsyncClient(
        transport=transport, base_url="http://compiler", timeout=60
    ) as http:
        yield http


async def post(client: httpx.AsyncClient, language: str, source: str) -> httpx.Response:
    return await client.post("/compile", json={"language": language, "source": source})


def assert_loads_in_browser_worker(module: bytes) -> None:
    names = exports(module)
    assert "_start" in names
    assert "memory" in names
    for module_name, name in imports(module):
        assert module_name == "wasi_snapshot_preview1" or (
            (module_name, name) in WORKER_ENV_IMPORTS
        ), f"worker хангадаггүй импорт: {module_name}.{name}"


def is_empty(directory: Path) -> bool:
    """Ажлын хавтас бүрэн цэвэрлэгдсэн эсэх (sync — async тестээс дуудна)."""
    return not any(directory.iterdir())


# --- Бэлтгэл ---------------------------------------------------------------------


def test_prewarm_built_every_artifact() -> None:
    """Эдгээр байхгүй бол доорх тестүүд юуг ч батлахгүй."""
    assert settings.stdio_object.is_file()
    assert settings.main_guard_object.is_file()
    assert sorted(settings.pch_dir.glob("*.pch"))


def test_toolchain_is_read_only() -> None:
    """Upstream emsdk image хөрвүүлэгчийг хэн ч бичих эрхтэй ирүүлдэг.

    Image-ийг production шиг `docker run --read-only`-оор ажиллуулж шалгана —
    эс бөгөөс эвдэрсэн хөрвүүлэлт дараагийн сурагчдын хөрвүүлэгчийг өөрчилж чадна.
    """
    root = main.toolchain_root()

    assert root is not None
    assert not os.access(root, os.W_OK)


def test_commands_use_pch_and_guard_only_where_they_apply() -> None:
    cpp = TOOLCHAINS["cpp"]

    with_iostream = cpp.command("#include <iostream>\n#include <string>\nint main() {}\n")
    assert "-include-pch" in with_iostream
    assert with_iostream[with_iostream.index("-include-pch") + 1].endswith("iostream.h.pch")
    assert "-Wl,--wrap=__main_void" in with_iostream

    assert "-include-pch" not in cpp.command("#include <vector>\nint main() {}\n")

    c = TOOLCHAINS["c"].command("#include <stdio.h>\nint main(void) {}\n")
    assert "-include-pch" not in c
    assert "-Wl,--wrap=__main_void" not in c
    assert str(settings.stdio_object) in c


# --- Амжилттай хөрвүүлэлт ---------------------------------------------------------


async def test_c_program_compiles_to_a_browser_module(client: httpx.AsyncClient) -> None:
    response = await post(client, "c", HELLO_C)

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/wasm"
    assert response.headers["x-compile-cache"] == "miss"
    assert_loads_in_browser_worker(response.content)
    assert custom_sections(response.content, WARNINGS_SECTION) == []


async def test_cpp_exceptions_compile_to_a_browser_module(client: httpx.AsyncClient) -> None:
    response = await post(client, "cpp", EXCEPTIONS_CPP)

    assert response.status_code == 200
    assert_loads_in_browser_worker(response.content)


async def test_identical_source_is_served_from_cache(client: httpx.AsyncClient) -> None:
    first = await post(client, "c", HELLO_C)
    second = await post(client, "c", HELLO_C)

    assert second.headers["x-compile-cache"] == "hit"
    assert second.content == first.content


async def test_warnings_travel_inside_the_module(client: httpx.AsyncClient) -> None:
    source = (
        "#include <stdio.h>\n\nint main(void) {\n"
        '    int nas;\n    printf("%d\\n", nas);\n    return 0;\n}\n'
    )

    response = await post(client, "c", source)

    assert response.status_code == 200
    [warnings] = custom_sections(response.content, WARNINGS_SECTION)
    text = warnings.decode("utf-8")
    assert text.startswith("main.c:5:")
    assert "-Wuninitialized" in text
    assert_loads_in_browser_worker(response.content)


# --- Сурагчийн алдаа ----------------------------------------------------------------


async def test_compile_error_points_at_the_line(client: httpx.AsyncClient) -> None:
    source = (
        "#include <stdio.h>\n\nint main(void) {\n"
        '    int b = 3\n    printf("%d\\n", b);\n    return 0;\n}\n'
    )

    response = await post(client, "c", source)

    assert response.status_code == 422
    body = response.json()
    assert body["code"] == "COMPILE_ERROR"
    assert body["diagnostics"].startswith("main.c:4:")
    for leak in ("/tmp", "/emsdk", "/app", "emcc: error:"):
        assert leak not in body["diagnostics"]


async def test_compile_errors_are_cached_too(client: httpx.AsyncClient) -> None:
    source = "int main(void) {\n    return 0\n}\n"

    await post(client, "c", source)
    second = await post(client, "c", source)

    assert second.status_code == 422
    assert second.headers["x-compile-cache"] == "hit"


async def test_undefined_function_explains_itself(client: httpx.AsyncClient) -> None:
    source = "int helper(int x);\n\nint main(void) {\n    return helper(2);\n}\n"

    response = await post(client, "c", source)

    assert response.status_code == 422
    diagnostics = response.json()["diagnostics"]
    assert "main.o: undefined symbol: helper" in diagnostics
    assert "↳" in diagnostics
    assert "/tmp" not in diagnostics


@pytest.mark.parametrize(
    ("language", "source"),
    [
        ("c", "int helper(int x) {\n    return x;\n}\n"),
        ("cpp", "#include <iostream>\n\nint helper() {\n    return 1;\n}\n"),
    ],
    ids=["c", "cpp"],
)
async def test_missing_main_explains_itself(
    client: httpx.AsyncClient, language: str, source: str
) -> None:
    response = await post(client, language, source)

    assert response.status_code == 422
    assert "int main()" in response.json()["diagnostics"]


PCH_PARITY_SOURCES = [
    "#include <iostream>\n\nint main() {\n    std::cout << std::setw(4) << 7 << std::endl;\n}\n",
    "#include <iostream>\n\nint main() {\n    std::vector<int> v{1, 2};\n"
    "    std::cout << v.size() << std::endl;\n}\n",
    "#include <iostream>\n#include <numeric>\n#include <vector>\n\nint main() {\n"
    "    std::vector<int> v{1, 2};\n"
    "    std::cout << std::accumulate(v.begin(), v.end(), 0) << std::endl;\n}\n",
]


@pytest.mark.parametrize("source", PCH_PARITY_SOURCES, ids=["setw", "vector", "accumulate"])
async def test_pch_never_changes_what_compiles(
    source: str, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """PCH зөвхөн хурдасгана: PCH-гүйгээр алдаатай код PCH-тэй ч алдаатай хэвээр."""
    with_pch = await compile_source(TOOLCHAINS["cpp"], source)

    monkeypatch.setattr(settings, "artifacts_dir", tmp_path / "artifacts-disabled")
    without_pch = await compile_source(TOOLCHAINS["cpp"], source)

    assert type(with_pch) is type(without_pch)


# --- Хамгаалалт ------------------------------------------------------------------------


async def test_source_over_the_limit_is_rejected(client: httpx.AsyncClient) -> None:
    response = await post(client, "c", "x" * (settings.max_source_bytes + 1))

    assert response.status_code == 413
    assert response.json() == {"code": "SOURCE_TOO_LARGE"}


async def test_timeout_kills_the_compiler_and_cleans_up(
    client: httpx.AsyncClient, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(settings, "timeout_seconds", 0.05)

    response = await post(client, "cpp", EXCEPTIONS_CPP)

    assert response.status_code == 504
    assert response.json() == {"code": "COMPILE_TIMEOUT"}
    assert is_empty(tmp_path)


async def test_busy_when_no_slot_frees_up(
    client: httpx.AsyncClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(main, "slots", asyncio.Semaphore(0))
    monkeypatch.setattr(settings, "queue_timeout_seconds", 0.05)

    response = await post(client, "c", HELLO_C)

    assert response.status_code == 503
    assert response.json() == {"code": "COMPILER_BUSY"}


async def test_identical_concurrent_requests_compile_once(
    client: httpx.AsyncClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Анги бүхэлдээ нэг мөчид «Ажиллуулах» дарсан ч хөрвүүлэлт нэг л удаа."""
    calls = 0

    async def counting(toolchain, source):  # noqa: ANN001, ANN202
        nonlocal calls
        calls += 1
        return await compile_source(toolchain, source)

    monkeypatch.setattr(main, "compile_source", counting)

    first, second = await asyncio.gather(post(client, "c", HELLO_C), post(client, "c", HELLO_C))

    assert first.status_code == second.status_code == 200
    assert first.content == second.content
    assert calls == 1


async def test_diagnostic_flood_is_cut_off(
    client: httpx.AsyncClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(settings, "max_capture_bytes", 4096)
    source = '#warning "анхааруулга"\n' * 400 + "int main(void) {\n    return 0;\n}\n"

    response = await post(client, "c", source)

    assert response.status_code == 422
    assert response.json()["diagnostics"].endswith(TRUNCATED_NOTE)


async def test_including_stdin_does_not_hang(client: httpx.AsyncClient) -> None:
    source = '#include "/dev/stdin"\n\nint main(void) {\n    return 0;\n}\n'

    response = await post(client, "c", source)

    assert response.status_code in (200, 422)


async def test_work_directory_is_removed(client: httpx.AsyncClient, tmp_path: Path) -> None:
    await post(client, "c", HELLO_C)

    assert is_empty(tmp_path)


async def test_health(client: httpx.AsyncClient) -> None:
    response = await client.get("/health")

    assert response.json() == {"status": "ok"}


async def test_small_cpp_programs_stay_small(client: httpx.AsyncClient) -> None:
    """main-ийн хамгаалалт `__cxa_demangle`-ийг (~80 KB) татаж оруулах ёсгүй."""
    source = '#include <cstdio>\n\nint main() {\n    std::puts("сайн уу");\n    return 0;\n}\n'

    response = await post(client, "cpp", source)

    assert response.status_code == 200
    assert len(response.content) < 32_000
