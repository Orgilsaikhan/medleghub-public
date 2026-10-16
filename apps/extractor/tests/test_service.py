"""HTTP гэрээ — жинхэнэ дэд процесс (`extractor.worker`)-оор.

    docker build --target test -t medleghub-extractor-test apps/extractor
    docker run --rm --read-only --tmpfs /tmp:size=256m,mode=1777 medleghub-extractor-test

Docker-гүй ч ажиллана (Linux).
"""

import asyncio
import json
import shutil
import subprocess
import sys
import time
from collections.abc import AsyncGenerator, AsyncIterator, Iterator
from pathlib import Path

import httpx
import pytest

from extractor import main
from extractor.settings import SERVICE_ROOT, settings
from tests import builders

OCTET = {"Content-Type": "application/octet-stream"}


@pytest.fixture(autouse=True)
def work_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Iterator[Path]:
    """Тест бүр чөлөөтэй слот, өөрийн түр хавтастай. Дараа нь түр файл үлдээгүйг шалгана."""
    work = tmp_path / "work"
    work.mkdir()
    monkeypatch.setattr(main, "slots", asyncio.Semaphore(1))
    monkeypatch.setattr(settings, "work_dir", str(work))
    yield work
    assert list(work.iterdir()) == []


@pytest.fixture
async def client() -> AsyncGenerator[httpx.AsyncClient, None]:
    transport = httpx.ASGITransport(app=main.app)
    async with httpx.AsyncClient(
        transport=transport, base_url="http://extractor", timeout=60
    ) as http:
        yield http


async def extract(client: httpx.AsyncClient, kind: str, data: bytes) -> httpx.Response:
    return await client.post("/extract", params={"kind": kind}, content=data, headers=OCTET)


def python_command(code: str) -> list[str]:
    return [sys.executable, "-c", code]


# --- Ерөнхий ---------------------------------------------------------------------


async def test_health(client: httpx.AsyncClient) -> None:
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.parametrize("kind", ["", "doc", "ppt", "PDF", "txt", "../pdf"])
async def test_unknown_kind_is_unsupported(client: httpx.AsyncClient, kind: str) -> None:
    response = await extract(client, kind, builders.make_pdf([["А"]]))
    assert response.status_code == 422
    assert response.json() == {"error": "unsupported"}


async def test_missing_kind_is_unsupported(client: httpx.AsyncClient) -> None:
    response = await client.post("/extract", content=b"%PDF-", headers=OCTET)
    assert response.status_code == 422
    assert response.json() == {"error": "unsupported"}


async def test_body_over_limit_is_rejected(
    client: httpx.AsyncClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(settings, "max_bytes", 1000)
    response = await extract(client, "pdf", b"%PDF-" + b"x" * 996)
    assert response.status_code == 413
    assert response.json() == {"error": "too_large"}

    exact = await extract(client, "pdf", b"%PDF-" + b"x" * 995)
    assert exact.status_code == 422  # хязгаарт багтсан — зүгээр л эвдэрсэн PDF
    assert exact.json() == {"error": "corrupt"}


async def test_body_is_counted_without_content_length(
    client: httpx.AsyncClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Chunked биед Content-Length байхгүй — уншихдаа тоолно."""
    monkeypatch.setattr(settings, "max_bytes", 1000)

    async def chunks() -> AsyncIterator[bytes]:
        for _ in range(20):
            yield b"x" * 100

    response = await client.post(
        "/extract", params={"kind": "docx"}, content=chunks(), headers=OCTET
    )
    assert "content-length" not in response.request.headers
    assert response.status_code == 413
    assert response.json() == {"error": "too_large"}


async def test_lying_content_length_is_not_trusted(monkeypatch: pytest.MonkeyPatch) -> None:
    """Content-Length бага гэж худлаа хэлсэн ч бодит байтыг тоолно."""
    monkeypatch.setattr(settings, "max_bytes", 1000)
    messages = [
        {"type": "http.request", "body": b"x" * 800, "more_body": True},
        {"type": "http.request", "body": b"x" * 800, "more_body": False},
    ]
    sent: list[dict[str, object]] = []

    async def receive() -> dict[str, object]:
        return messages.pop(0) if messages else {"type": "http.disconnect"}

    async def send(message: dict[str, object]) -> None:
        sent.append(message)

    scope = {
        "type": "http",
        "asgi": {"version": "3.0"},
        "http_version": "1.1",
        "method": "POST",
        "scheme": "http",
        "path": "/extract",
        "raw_path": b"/extract",
        "query_string": b"kind=pdf",
        "root_path": "",
        "headers": [(b"content-length", b"10"), (b"host", b"extractor")],
        "client": ("127.0.0.1", 1),
        "server": ("extractor", 80),
    }
    await main.app(scope, receive, send)
    assert sent[0]["status"] == 413
    assert json.loads(sent[1]["body"]) == {"error": "too_large"}


# --- PDF ---------------------------------------------------------------------------


async def test_pdf_text_per_page(client: httpx.AsyncClient) -> None:
    pdf = builders.make_pdf(
        [
            ["Сайн байна уу, MedlegHub!", "  Хоёр   дахь мөр — Өө Үү  "],
            [],
            ["Гурав дахь хуудас", "ёЁ test 123"],
        ]
    )
    response = await extract(client, "pdf", pdf)
    assert response.status_code == 200, response.text
    assert response.json() == {
        "kind": "pdf",
        "page_count": 3,
        "pages": [
            {
                "number": 1,
                "title": None,
                "text": "Сайн байна уу, MedlegHub!\nХоёр дахь мөр — Өө Үү",
            },
            {"number": 2, "title": None, "text": ""},
            {"number": 3, "title": None, "text": "Гурав дахь хуудас\nёЁ test 123"},
        ],
        "truncated": False,
    }


async def test_pdf_header_may_follow_junk_within_first_kilobyte(
    client: httpx.AsyncClient,
) -> None:
    response = await extract(client, "pdf", b"\0" * 500 + builders.make_pdf([["Хог"]]))
    assert response.status_code == 200, response.text
    assert response.json()["pages"][0]["text"] == "Хог"


async def test_pdf_header_after_first_kilobyte_is_corrupt(client: httpx.AsyncClient) -> None:
    response = await extract(client, "pdf", b"\0" * 1100 + builders.make_pdf([["Хог"]]))
    assert response.status_code == 422
    assert response.json() == {"error": "corrupt"}


async def test_pdf_with_too_many_pages(
    client: httpx.AsyncClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(settings, "max_pages", 3)
    response = await extract(client, "pdf", builders.make_pdf([["Х"]] * 4))
    assert response.status_code == 422
    assert response.json() == {"error": "too_many_pages", "page_count": 4}

    ok = await extract(client, "pdf", builders.make_pdf([["Х"]] * 3))
    assert ok.status_code == 200
    assert ok.json()["page_count"] == 3


async def test_password_protected_pdf_is_encrypted(client: httpx.AsyncClient) -> None:
    response = await extract(client, "pdf", builders.make_pdf([["Нууц"]], user_password="nuuts"))
    assert response.status_code == 422
    assert response.json() == {"error": "encrypted"}


async def test_text_is_capped_across_pages(
    client: httpx.AsyncClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(settings, "max_text_chars", 25)
    pdf = builders.make_pdf([["Нэгдүгээр хуудас"], ["Хоёрдугаар хуудас"], ["Гуравдугаар"]])
    response = await extract(client, "pdf", pdf)
    assert response.status_code == 200
    body = response.json()
    assert body["truncated"] is True
    assert body["page_count"] == 3
    assert [page["text"] for page in body["pages"]] == ["Нэгдүгээр хуудас", "Хоёрдугаа", ""]


# --- PPTX ----------------------------------------------------------------------------


async def test_pptx_slides_in_presentation_order(client: httpx.AsyncClient) -> None:
    pptx = builders.make_pptx(
        [
            [
                builders.shape("Алгоритмын үндэс", placeholder="title"),
                builders.shape("Алгоритм гэж юу вэ?", "Алхам алхмаар бодох", split=True),
            ],
            [
                builders.shape("Хүснэгт ба бүлэг", placeholder="ctrTitle"),
                builders.group(
                    builders.shape("Бүлэг А"), builders.group(builders.shape("Бүлэг Б"))
                ),
                builders.table([["Нэр", "Оноо"], ["Бат", "95"]]),
            ],
            [builders.shape("Гарчиггүй слайд")],
        ],
        notes={0: ["Илтгэгч энд тайлбарлана.", "Хоёр дахь мөр."]},
        # slide3.xml эхэнд — файлын нэрээр биш, `p:sldIdLst`-ийн дарааллаар.
        order=[2, 0, 1],
    )
    response = await extract(client, "pptx", pptx)
    assert response.status_code == 200, response.text
    assert response.json() == {
        "kind": "pptx",
        "page_count": 3,
        "pages": [
            {"number": 1, "title": None, "text": "Гарчиггүй слайд"},
            {
                "number": 2,
                "title": "Алгоритмын үндэс",
                "text": (
                    "Алгоритмын үндэс\nАлгоритм гэж юу вэ?\nАлхам алхмаар бодох\n"
                    "Тэмдэглэл: Илтгэгч энд тайлбарлана.\nХоёр дахь мөр."
                ),
            },
            {
                "number": 3,
                "title": "Хүснэгт ба бүлэг",
                "text": "Хүснэгт ба бүлэг\nБүлэг А\nБүлэг Б\nНэр\nОноо\nБат\n95",
            },
        ],
        "truncated": False,
    }


async def test_pptx_with_too_many_slides(
    client: httpx.AsyncClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(settings, "max_pages", 2)
    pptx = builders.make_pptx([[builders.shape(f"Слайд {i}")] for i in range(3)])
    response = await extract(client, "pptx", pptx)
    assert response.status_code == 422
    assert response.json() == {"error": "too_many_pages", "page_count": 3}


# --- DOCX -----------------------------------------------------------------------------


async def test_docx_sections_start_at_headings(client: httpx.AsyncClient) -> None:
    docx = builders.make_docx(
        [
            builders.para("Удиртгал — гарчгийн өмнөх текст."),
            builders.para("Өгөгдлийн бүтэц", "Title"),
            builders.para("Энэ лекцээр массив, жагсаалтыг үзнэ.", split=True),
            builders.para("1. Массив", "Heading1"),
            builders.word_table([["Үйлдэл", "Хугацаа"], ["Хандах", "O(1)"]]),
            builders.para("1.1. Индекс", "Heading2"),
            builders.para("Гуравдугаар түвшин шинэ хэсэг эхлүүлэхгүй", "Heading3"),
            # Орос/монгол Word: загварын id нь «1», нэр нь «heading 1».
            builders.para("2. Жагсаалт", "1"),
            builders.para("Холбоост жагсаалт."),
        ]
    )
    response = await extract(client, "docx", docx)
    assert response.status_code == 200, response.text
    assert response.json() == {
        "kind": "docx",
        "page_count": 5,
        "pages": [
            {"number": 1, "title": None, "text": "Удиртгал — гарчгийн өмнөх текст."},
            {
                "number": 2,
                "title": "Өгөгдлийн бүтэц",
                "text": "Өгөгдлийн бүтэц\nЭнэ лекцээр массив, жагсаалтыг үзнэ.",
            },
            {"number": 3, "title": "1. Массив", "text": "1. Массив\nҮйлдэл\nХугацаа\nХандах\nO(1)"},
            {
                "number": 4,
                "title": "1.1. Индекс",
                "text": "1.1. Индекс\nГуравдугаар түвшин шинэ хэсэг эхлүүлэхгүй",
            },
            {"number": 5, "title": "2. Жагсаалт", "text": "2. Жагсаалт\nХолбоост жагсаалт."},
        ],
        "truncated": False,
    }


async def test_docx_long_section_is_split(client: httpx.AsyncClient) -> None:
    paragraph = ("Урт лекцийн догол мөр. " * 40).strip()  # ~920 тэмдэгт
    docx = builders.make_docx(
        [builders.para("Урт бүлэг", "Heading1"), *[builders.para(paragraph)] * 10]
    )
    response = await extract(client, "docx", docx)
    assert response.status_code == 200, response.text
    pages = response.json()["pages"]
    assert len(pages) == 3
    assert pages[0]["title"] == "Урт бүлэг"
    assert [page["title"] for page in pages[1:]] == [None, None]
    assert all(len(page["text"]) <= 4000 for page in pages)
    assert sum(page["text"].count(paragraph) for page in pages) == 10


async def test_docx_with_too_many_sections(
    client: httpx.AsyncClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(settings, "max_pages", 3)
    docx = builders.make_docx([builders.para(f"Бүлэг {i}", "Heading1") for i in range(5)])
    response = await extract(client, "docx", docx)
    assert response.status_code == 422
    assert response.json() == {"error": "too_many_pages", "page_count": 5}


async def test_empty_docx_has_no_sections(client: httpx.AsyncClient) -> None:
    response = await extract(client, "docx", builders.make_docx([builders.para("   ")]))
    assert response.status_code == 200
    assert response.json() == {"kind": "docx", "page_count": 0, "pages": [], "truncated": False}


# --- Татгалзах файлууд ---------------------------------------------------------------


@pytest.mark.parametrize("kind", ["pptx", "docx"])
async def test_encrypted_office_file(client: httpx.AsyncClient, kind: str) -> None:
    """Нууц үгтэй Office файл нь OLE сав (EncryptionInfo + EncryptedPackage)."""
    ole = builders.make_ole(["EncryptionInfo", "EncryptedPackage"])
    response = await extract(client, kind, ole)
    assert response.status_code == 422
    assert response.json() == {"error": "encrypted"}


@pytest.mark.parametrize(
    ("kind", "streams"),
    [("docx", ["WordDocument", "1Table"]), ("pptx", ["PowerPoint Document", "Pictures"])],
)
async def test_legacy_office_file(client: httpx.AsyncClient, kind: str, streams: list[str]) -> None:
    response = await extract(client, kind, builders.make_ole(streams))
    assert response.status_code == 422
    assert response.json() == {"error": "legacy_format"}


async def test_unreadable_ole_file_is_legacy(client: httpx.AsyncClient) -> None:
    response = await extract(client, "docx", builders.OLE_MAGIC + b"\xff" * 2000)
    assert response.status_code == 422
    assert response.json() == {"error": "legacy_format"}


async def test_ole_body_sent_as_pdf_is_corrupt(client: httpx.AsyncClient) -> None:
    response = await extract(client, "pdf", builders.make_ole(["WordDocument"]))
    assert response.status_code == 422
    assert response.json() == {"error": "corrupt"}


@pytest.mark.parametrize(
    ("kind", "data"),
    [
        ("pptx", builders.make_pptx([[builders.shape("Макро")]], main_type=builders.PPTM_MAIN)),
        ("docx", builders.make_docx([builders.para("Макро")], main_type=builders.DOCM_MAIN)),
        (
            "docx",
            builders.make_docx(
                [builders.para("Макро")], extra_files={"word/vbaProject.bin": b"\0" * 64}
            ),
        ),
        (
            "pptx",
            builders.make_pptx(
                [[builders.shape("Макро")]], extra_files={"ppt/VBAPROJECT.BIN": b"\0" * 64}
            ),
        ),
    ],
)
async def test_macro_enabled_package(client: httpx.AsyncClient, kind: str, data: bytes) -> None:
    response = await extract(client, kind, data)
    assert response.status_code == 422
    assert response.json() == {"error": "macro_enabled"}


async def test_zip_with_too_many_entries(client: httpx.AsyncClient) -> None:
    docx = builders.make_docx([builders.para("Бөмбөг")], extra_entries=5_000)
    response = await extract(client, "docx", docx)
    assert response.status_code == 422
    assert response.json() == {"error": "corrupt"}


async def test_zip_with_huge_declared_size(client: httpx.AsyncClient) -> None:
    docx = builders.set_declared_size(
        builders.make_docx([builders.para("Бөмбөг")]), "word/document.xml", 250_000_000
    )
    response = await extract(client, "docx", docx)
    assert response.status_code == 422
    assert response.json() == {"error": "corrupt"}


async def test_zip_part_over_limit(
    client: httpx.AsyncClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(settings, "max_part_bytes", 2_000)
    docx = builders.make_docx([builders.para("Том " * 1_000)])
    response = await extract(client, "docx", docx)
    assert response.status_code == 422
    assert response.json() == {"error": "corrupt"}


async def test_zip_part_larger_than_declared(client: httpx.AsyncClient) -> None:
    """Толгойд бага хэмжээ бичсэн ч бодит өгөгдөл нь том — хэмжээндээ хүрээд зогсоно."""
    docx = builders.set_declared_size(
        builders.make_docx([builders.para("Худал " * 1_000)]), "word/document.xml", 100
    )
    response = await extract(client, "docx", docx)
    assert response.status_code == 422
    assert response.json() == {"error": "corrupt"}


async def test_real_compression_bomb(client: httpx.AsyncClient) -> None:
    """60 MB тэг ~60 KB болж шахагдана — задлахаас өмнө хэмжээгээр нь татгалзана."""
    bomb = b"<w:document " + b" " * 60_000_000 + b"/>"
    docx = builders.make_docx([builders.para("Бөмбөг")], extra_files={"word/document.xml": bomb})
    assert len(docx) < 1_000_000
    response = await extract(client, "docx", docx)
    assert response.status_code == 422
    assert response.json() == {"error": "corrupt"}


async def test_xml_entities_are_rejected(client: httpx.AsyncClient) -> None:
    laughs = (
        '<?xml version="1.0"?><!DOCTYPE w:document [<!ENTITY a "хаха">'
        '<!ENTITY b "&a;&a;&a;&a;&a;&a;&a;&a;">]>'
        f'<w:document xmlns:w="{builders.NS_W}"><w:body><w:p><w:r><w:t>&b;</w:t></w:r></w:p>'
        "</w:body></w:document>"
    )
    docx = builders.make_docx([], extra_files={"word/document.xml": laughs})
    response = await extract(client, "docx", docx)
    assert response.status_code == 422
    assert response.json() == {"error": "corrupt"}


@pytest.mark.parametrize(
    ("kind", "data"),
    [
        ("pdf", b""),
        ("pdf", b"not a pdf at all"),
        ("pdf", b"%PDF-1.7\n" + b"\x00garbage" * 100),
        ("pdf", builders.make_pdf([["Тасархай"]])[:300]),
        ("pptx", b""),
        ("pptx", b"random bytes"),
        ("docx", b"PK\x03\x04" + b"\0" * 100),
        ("docx", builders.make_docx([builders.para("Тасархай")])[:200]),
        # Word баримтыг PPTX гэж илгээсэн.
        ("pptx", builders.make_docx([builders.para("Буруу төрөл")])),
        ("docx", builders.make_pptx([[builders.shape("Буруу төрөл")]])),
        # `[Content_Types].xml` алга.
        ("docx", builders.zip_bytes({"word/document.xml": "<w:document/>"})),
        # XML эвдэрсэн.
        (
            "docx",
            builders.make_docx([], extra_files={"word/document.xml": "<w:document><w:body>"}),
        ),
    ],
)
async def test_corrupt_input(client: httpx.AsyncClient, kind: str, data: bytes) -> None:
    response = await extract(client, kind, data)
    assert response.status_code == 422
    assert response.json() == {"error": "corrupt"}


# --- Дэд процесс, хязгаар ----------------------------------------------------------------


async def test_worker_timeout_kills_the_process(
    client: httpx.AsyncClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    sleep = shutil.which("sleep")
    assert sleep is not None
    monkeypatch.setattr(main, "worker_command", lambda kind, path: [sleep, "30"])
    monkeypatch.setattr(settings, "timeout_seconds", 0.5)
    started = time.monotonic()
    response = await extract(client, "pdf", builders.make_pdf([["Удаан"]]))
    assert time.monotonic() - started < 10
    assert response.status_code == 422
    assert response.json() == {"error": "timeout"}


async def test_cpu_limit_is_a_timeout(
    client: httpx.AsyncClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(settings, "cpu_seconds", 1)
    spin = (
        "from extractor.settings import settings\n"
        "from extractor.worker import limit_resources\n"
        "limit_resources(settings)\n"
        "while True:\n    pass\n"
    )
    monkeypatch.setattr(main, "worker_command", lambda kind, path: python_command(spin))
    response = await extract(client, "pdf", builders.make_pdf([["Халуун"]]))
    assert response.status_code == 422
    assert response.json() == {"error": "timeout"}


@pytest.mark.parametrize(
    "code",
    [
        "raise SystemExit(3)",
        "print('not json')",
        "print('[1, 2]')",
        # Мэдэгдэхгүй алдааны код API руу хэзээ ч гарахгүй.
        'print(\'{"ok": false, "error": "weird code"}\')',
        'print(\'{"ok": true, "kind": "pdf"}\')',
    ],
)
async def test_broken_worker_is_corrupt(
    client: httpx.AsyncClient, monkeypatch: pytest.MonkeyPatch, code: str
) -> None:
    monkeypatch.setattr(main, "worker_command", lambda kind, path: python_command(code))
    response = await extract(client, "pdf", builders.make_pdf([["Эвдэрхий"]]))
    assert response.status_code == 422
    assert response.json() == {"error": "corrupt"}


async def test_busy_when_queue_is_full(
    client: httpx.AsyncClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(settings, "queue_timeout_seconds", 0.2)
    await main.slots.acquire()
    try:
        response = await extract(client, "pdf", builders.make_pdf([["Дараалал"]]))
    finally:
        main.slots.release()
    assert response.status_code == 503
    assert response.json() == {"error": "busy"}


async def test_requests_wait_for_a_free_slot(client: httpx.AsyncClient) -> None:
    pdfs = [builders.make_pdf([[f"Хүсэлт {i}"]]) for i in range(3)]
    responses = await asyncio.gather(*(extract(client, "pdf", pdf) for pdf in pdfs))
    assert [r.json()["pages"][0]["text"] for r in responses] == [f"Хүсэлт {i}" for i in range(3)]


def test_worker_limits_its_own_resources() -> None:
    code = (
        "import json, resource\n"
        "from extractor.settings import settings\n"
        "from extractor.worker import limit_resources\n"
        "limit_resources(settings)\n"
        "names = ['RLIMIT_AS', 'RLIMIT_CPU', 'RLIMIT_FSIZE', 'RLIMIT_NOFILE', 'RLIMIT_CORE']\n"
        "limits = {n: resource.getrlimit(getattr(resource, n))[0] for n in names}\n"
        "try:\n"
        "    bytearray(2 * 1024 ** 3)\n"
        "    limits['memory_error'] = False\n"
        "except MemoryError:\n"
        "    limits['memory_error'] = True\n"
        "print(json.dumps(limits))\n"
    )
    completed = subprocess.run(
        python_command(code),
        env=settings.child_environment(),
        cwd=SERVICE_ROOT,
        capture_output=True,
        check=True,
        timeout=30,
    )
    assert json.loads(completed.stdout) == {
        "RLIMIT_AS": 768 * 1024 * 1024,
        "RLIMIT_CPU": 30,
        "RLIMIT_FSIZE": 1024 * 1024,
        "RLIMIT_NOFILE": 64,
        "RLIMIT_CORE": 0,
        "memory_error": True,
    }


def test_child_environment_inherits_nothing(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DATABASE_URL", "postgresql://secret@db/prod")
    monkeypatch.setenv("JWT_SECRET", "secret")
    env = settings.child_environment()
    assert "DATABASE_URL" not in env
    assert "JWT_SECRET" not in env
    assert "PATH" not in env
    allowed = {"PYTHONPATH", "PYTHONDONTWRITEBYTECODE", "PYTHONIOENCODING", "LC_ALL"}
    assert {key for key in env if not key.startswith("EXTRACTOR_")} == allowed | {"HOME", "TMPDIR"}
