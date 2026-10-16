"""MedlegHub Live (AI Study): хандалт, хязгаар, файл оруулах, цаана боловсруулах,
заавар, тест, карт, эзэмшил, устгал.

AI нь хуурамч (`fake:` provider эсвэл скриптэй provider), задлагч нь хуурамч
функц, файлын сан нь түр хавтас. Цаана ажиллах дарааллыг `worker.drain()`-оор
тестийн дотор шууд ажиллуулна.
"""

import json
import uuid
from collections.abc import AsyncGenerator
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from pathlib import Path
from typing import Any

import httpx
import pytest
from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.core.config import settings
from app.live import purge, worker
from app.live.extract_client import ExtractedPage, Extraction, ExtractionError
from app.live.pipeline import LiveContext
from app.live.storage import LocalBlobStorage
from app.main import app
from app.models.ai_request import AIRequest
from app.models.enums import UserRole
from app.models.live import (
    LiveBlobDeletion,
    LiveCard,
    LiveGeneration,
    LiveMaterial,
    LivePass,
    LiveQuestion,
    LiveTopic,
    LiveTopicProgress,
)
from app.models.plan_adjustment import PlanAdjustment
from app.models.user import User
from app.services import account_service
from app.services.ai import router as ai_router
from app.services.ai.errors import AIError
from app.services.ai.providers.fake import FakeProvider
from app.services.ai.router import ModelHealth
from app.services.ai.service import MAX_TRANSIENT_ERRORS, AIService
from app.services.ai.types import ProviderRequest, ProviderResult, Usage
from tests.conftest import login_as, make_user
from tests.fake_wire import install_fake_wire, pay

LECTURE = """# Алгоритм

Алгоритм бол асуудлыг шийдэх алхмуудын дараалал. Алгоритм төгсгөлтэй байна.

# Хоёртын хайлт

Хоёртын хайлт эрэмбэлсэн массивт ажиллана. Хайх мужийг алхам бүрд хоёр хуваана.

# Хөөсөн эрэмбэлэлт

Хөөсөн эрэмбэлэлт хөрш элементүүдийг сольж эрэмбэлнэ. Энэ нь O(n^2) хугацаатай.

# Рекурс

Рекурс гэдэг нь функц өөрийгөө дуудах. Суурь тохиолдол заавал байна.
"""


@dataclass
class ScriptedProvider:
    """Дуудлага бүрд дараалсан хариу буцаана: `str` — JSON, `Exception` — алдаа."""

    name: str = "fake"
    script: list[Any] = field(default_factory=list)
    requests: list[ProviderRequest] = field(default_factory=list)

    async def aclose(self) -> None:
        return None

    async def generate(self, request: ProviderRequest) -> ProviderResult:
        self.requests.append(request)
        step = self.script.pop(0) if self.script else None
        if isinstance(step, Exception):
            raise step
        if step is None:
            return await FakeProvider().generate(request)
        return ProviderResult(text=step, usage=Usage(input_tokens=1000, output_tokens=200))


@dataclass
class FakeClock:
    """Загварын хөргөлтийн цаг — `sleep` нь цагийг урагшлуулна (тест хүлээхгүй)."""

    now: float = 1000.0
    slept: list[float] = field(default_factory=list)

    def __call__(self) -> float:
        return self.now

    async def sleep(self, seconds: float) -> None:
        self.slept.append(seconds)
        self.now += seconds


@dataclass
class LiveEnv:
    ctx: LiveContext
    provider: ScriptedProvider
    storage: LocalBlobStorage
    storage_dir: Path
    db: AsyncSession
    clock: FakeClock
    health: ModelHealth
    extractions: dict[str, Any] = field(default_factory=dict)

    async def drain(self) -> int:
        done = await worker.drain(self.ctx)
        # HTTP зам тестийн нэг session-ийг хуваалцдаг — цааны бичлэгийг харуулна.
        self.db.expire_all()
        return done


@pytest.fixture
async def live(
    db: AsyncSession, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> AsyncGenerator[LiveEnv, None]:
    monkeypatch.setattr(settings, "live_access", "all")
    monkeypatch.setattr(settings, "ai_models", ["fake:test"])
    monkeypatch.setattr(settings, "ai_model_limits", {})
    storage = LocalBlobStorage(tmp_path / "blobs")
    provider = ScriptedProvider()
    sessions = async_sessionmaker(db.bind, expire_on_commit=False, autoflush=False)
    clock = FakeClock()
    health = ModelHealth(clock=clock)
    # Админы «AI загварууд» хуудас процессын нийтлэг бүртгэлийг уншдаг.
    monkeypatch.setattr(ai_router, "health", health)

    env = LiveEnv(
        ctx=LiveContext(
            sessions=sessions,
            ai=AIService(
                sessions, providers={"fake": provider}, sleep=clock.sleep, model_health=health
            ),
            storage=storage,
        ),
        provider=provider,
        storage=storage,
        storage_dir=tmp_path / "blobs",
        db=db,
        clock=clock,
        health=health,
    )

    async def fake_extract(kind: str, data: bytes) -> Extraction:
        outcome = env.extractions.get(kind)
        if isinstance(outcome, Exception):
            raise outcome
        if outcome is not None:
            return outcome
        return Extraction(3, [ExtractedPage(n, None, f"Хуудас {n}: агуулга") for n in (1, 2, 3)])

    env.ctx.extract = fake_extract
    from app.api.v1.live import get_live_storage

    app.dependency_overrides[get_live_storage] = lambda: storage
    yield env
    app.dependency_overrides.pop(get_live_storage, None)


async def student(client: httpx.AsyncClient, api: str, db: AsyncSession, email: str) -> User:
    """Нэвтэрсэн оюутан. Live зөвхөн багцтай хэрэглэгчдэд тул Standard багцтай."""
    user = await make_user(db, email)
    user.plan_expires_at = datetime.now(UTC) + timedelta(days=30)
    await db.commit()
    await db.refresh(user)
    await login_as(client, api, email)
    return user


async def upload(
    client: httpx.AsyncClient,
    api: str,
    filename: str = "lecture.md",
    body: bytes = LECTURE.encode(),
    **extra: Any,
) -> dict:
    created = await client.post(
        f"{api}/live/materials",
        json={"filename": filename, "size_bytes": len(body), **extra},
    )
    assert created.status_code == 201, created.text
    material = created.json()
    assert material["status"] == "uploading"
    sent = await client.put(
        f"{api}/live/materials/{material['id']}/content",
        content=body,
        headers={"Content-Type": "application/octet-stream"},
    )
    assert sent.status_code == 202, sent.text
    assert sent.json()["status"] == "queued"
    return sent.json()


async def ready_material(client: httpx.AsyncClient, api: str, live: LiveEnv) -> dict:
    material = await upload(client, api)
    await live.drain()
    detail = await client.get(f"{api}/live/materials/{material['id']}")
    assert detail.status_code == 200, detail.text
    assert detail.json()["status"] == "ready", detail.json()
    return detail.json()


def first_topic(detail: dict) -> dict:
    return detail["sections"][0]["topics"][0]


# --- Хандалт ---------------------------------------------------------------


async def test_live_is_hidden_when_off(
    client: httpx.AsyncClient, api: str, db: AsyncSession, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(settings, "live_access", "off")
    visitor = await client.get(f"{api}/live/config")
    assert visitor.status_code == 200
    assert visitor.json()["enabled"] is False
    await student(client, api, db, "off@example.com")
    assert (await client.get(f"{api}/live/config")).json()["enabled"] is False
    response = await client.get(f"{api}/live/materials")
    assert response.status_code == 404
    assert response.json()["detail"]["code"] == "LIVE_NOT_FOUND"


async def test_admins_only_mode(
    client: httpx.AsyncClient, api: str, db: AsyncSession, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(settings, "live_access", "admins")
    await student(client, api, db, "student@example.com")
    assert (await client.get(f"{api}/live/materials")).status_code == 404
    await make_user(db, "admin@example.com", role=UserRole.ADMIN)
    await login_as(client, api, "admin@example.com")
    assert (await client.get(f"{api}/live/materials")).status_code == 200
    config = (await client.get(f"{api}/live/config")).json()
    assert config["enabled"] is True
    assert config["tier"] == "premium"


async def test_live_requires_login(client: httpx.AsyncClient, api: str, live: LiveEnv) -> None:
    assert (await client.get(f"{api}/live/materials")).status_code == 401


# --- Файл оруулах, боловсруулах ---------------------------------------------


async def test_text_material_becomes_a_study_set(
    client: httpx.AsyncClient, api: str, db: AsyncSession, live: LiveEnv
) -> None:
    await student(client, api, db, "s@example.com")
    config = (await client.get(f"{api}/live/config")).json()
    assert config["enabled"] and config["ai_configured"]
    assert config["tier"] == "standard"
    # Материалын тоог хэрэглэгчид харуулахгүй — зөвхөн AI хэрэглээний хувь.
    assert config["usage"]["ai_used_percent"] == 0
    assert "documents_limit" not in config["usage"]
    assert ".pdf" in config["upload"]["accepted"]

    material = await upload(client, api, title="Алгоритмын лекц")
    assert await live.drain() == 1
    detail = (await client.get(f"{api}/live/materials/{material['id']}")).json()
    assert detail["status"] == "ready"
    assert detail["title"] == "Алгоритмын лекц"
    assert detail["page_count"] == 1
    topics = [topic for section in detail["sections"] for topic in section["topics"]]
    assert [topic["title"] for topic in topics] == [
        "Алгоритм",
        "Хоёртын хайлт",
        "Хөөсөн эрэмбэлэлт",
        "Рекурс",
    ]
    assert all(topic["mastery"] == 0 for topic in topics)
    assert detail["cards"]["total"] == detail["cards"]["new"] == detail["cards"]["due"] > 0
    assert detail["full_quiz"] is None and detail["exam"] is None

    # Эх файл ба задалсан текст файлын санд.
    stored = await db.get(LiveMaterial, uuid.UUID(material["id"]))
    assert stored is not None and stored.sha256 and stored.text_key
    assert (live.storage_dir / stored.storage_key).read_bytes() == LECTURE.encode()
    # AI-д материал эхэнд, даалгавар төгсгөлд (кэш); зардал бичигдсэн.
    request = live.provider.requests[0]
    assert request.capability == "document"
    assert "=== МАТЕРИАЛ" in (request.parts[0].text or "")
    assert "задал" in (request.parts[-1].text or "")
    rows = (await db.execute(select(AIRequest))).scalars().all()
    assert [(row.capability, row.success, row.kind) for row in rows] == [("document", True, "call")]

    listed = (await client.get(f"{api}/live/materials")).json()
    assert [item["id"] for item in listed] == [material["id"]]
    assert listed[0]["topic_count"] == 4


async def test_live_is_closed_to_free_users(
    client: httpx.AsyncClient, api: str, db: AsyncSession, live: LiveEnv
) -> None:
    """Live нь зөвхөн Standard, Premium-д: багцгүй хэрэглэгчид `/live/config`-оос
    бусад бүх зам 402. Багц дуусахад материал устахгүй, дахин авбал буцаж харагдана."""
    user = await student(client, api, db, "free@example.com")
    user_id = user.id
    material = await upload(client, api)
    await live.drain()

    user = await db.get(User, user_id)
    assert user is not None
    user.plan_expires_at = datetime.now(UTC) - timedelta(days=1)
    await db.commit()
    config = (await client.get(f"{api}/live/config")).json()
    assert config["enabled"] is True
    assert config["tier"] == "free"
    assert config["usage"] is None
    url = f"{api}/live/materials/{material['id']}"
    for response in (
        await client.get(f"{api}/live/materials"),
        await client.post(f"{api}/live/materials", json={"filename": "b.md", "size_bytes": 10}),
        await client.get(url),
        await client.post(f"{url}/generations", json={"kind": "exam"}),
        await client.get(f"{url}/cards"),
    ):
        assert response.status_code == 402, response.text
        detail = response.json()["detail"]
        assert detail["code"] == "LIVE_PLAN_REQUIRED"
        assert "Standard болон Premium" in detail["message"]

    user = await db.get(User, user_id)
    assert user is not None
    user.plan_expires_at = datetime.now(UTC) + timedelta(days=30)
    await db.commit()
    assert (await client.get(url)).status_code == 200


async def test_failed_processing_can_be_retried(
    client: httpx.AsyncClient, api: str, db: AsyncSession, live: LiveEnv
) -> None:
    await student(client, api, db, "retry@example.com")
    live.provider.script = [AIError("http_400", "bad")]
    material = await upload(client, api)
    await live.drain()
    detail = (await client.get(f"{api}/live/materials/{material['id']}")).json()
    assert detail["status"] == "failed"
    assert detail["error_code"] == "LIVE_AI_FAILED"
    assert detail["error_message"]
    retried = await client.post(f"{api}/live/materials/{material['id']}/retry")
    assert retried.status_code == 202
    await live.drain()
    assert (await client.get(f"{api}/live/materials/{material['id']}")).json()["status"] == "ready"
    # Бэлэн болсныг дахин эхлүүлэхгүй.
    again = await client.post(f"{api}/live/materials/{material['id']}/retry")
    assert again.status_code == 409


async def test_standard_plan_includes_live(
    client: httpx.AsyncClient, api: str, db: AsyncSession, live: LiveEnv
) -> None:
    """Live нь Standard багцад багтсан: сард `live_standard_*` хязгаартай."""
    user = await student(client, api, db, "standard@example.com")
    user_id = user.id
    user.plan_expires_at = datetime.now(UTC) + timedelta(days=10)
    await db.commit()
    config = (await client.get(f"{api}/live/config")).json()
    assert config["tier"] == "standard"
    assert config["tier_expires_at"]
    await upload(client, api)
    await live.drain()
    await upload(client, api, filename="second.md")
    await live.drain()

    # Сарын хязгаарт хүрвэл Premium биш — ойлгомжтой мессеж.
    for _ in range(settings.live_standard_documents_per_month):
        db.add(
            AIRequest(
                user_id=user_id,
                capability="document",
                provider="fake",
                model="test",
                prompt_version="v",
                attempt=1,
                kind="call",
                price_version="p",
                success=True,
            )
        )
    await db.commit()
    blocked = await client.post(
        f"{api}/live/materials",
        json={"filename": "c.md", "size_bytes": 10},
    )
    assert blocked.status_code == 402
    assert blocked.json()["detail"]["code"] == "LIVE_DOCUMENT_LIMIT"

    # Багц дуусвал үнэгүй эрх.
    user = await db.get(User, user_id)
    assert user is not None
    user.plan_expires_at = datetime.now(UTC) - timedelta(days=1)
    await db.commit()
    assert (await client.get(f"{api}/live/config")).json()["tier"] == "free"


# --- Нэг удаагийн эрх -----------------------------------------------------------


async def buy_pass(client: httpx.AsyncClient, api: str, monkeypatch: pytest.MonkeyPatch) -> None:
    """Нэвтэрсэн, багцгүй хэрэглэгч нэг удаагийн эрх авна (Wire-ийн загвар)."""
    install_fake_wire(monkeypatch)
    response = await client.post(f"{api}/billing/checkout", json={"plan": "live_pass"})
    assert response.status_code == 200, response.text
    status = await pay(client, api, response.json()["payment_id"])
    assert status["receipt"]["plan"] == "live_pass"


async def test_live_pass_opens_one_material_for_thirty_days(
    client: httpx.AsyncClient,
    api: str,
    db: AsyncSession,
    live: LiveEnv,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    await make_user(db, "pass@example.com")
    await login_as(client, api, "pass@example.com")
    await buy_pass(client, api, monkeypatch)
    config = (await client.get(f"{api}/live/config")).json()
    assert config["tier"] == "pass"
    assert config["usage"] is None
    assert config["passes"] == {"unused": True, "materials": []}

    detail = await ready_material(client, api, live)
    config = (await client.get(f"{api}/live/config")).json()
    assert config["passes"]["unused"] is False
    [opened] = config["passes"]["materials"]
    assert opened["material_id"] == detail["id"]
    left = datetime.fromisoformat(opened["expires_at"]) - datetime.now(UTC)
    assert timedelta(days=29, hours=23) < left <= timedelta(days=30)
    url = f"{api}/live/materials/{detail['id']}"
    assert (await client.post(f"{url}/generations", json={"kind": "exam"})).status_code == 202

    # Нэг эрх — нэг материал.
    second = await client.post(f"{api}/live/materials", json={"filename": "b.md", "size_bytes": 9})
    assert second.status_code == 402
    assert second.json()["detail"]["code"] == "LIVE_PASS_USED"

    # 30 хоногийн дараа хаагдана; материал устахгүй.
    await db.execute(
        update(LivePass).values(
            used_at=datetime.now(UTC) - timedelta(days=31),
            expires_at=datetime.now(UTC) - timedelta(days=1),
        )
    )
    await db.commit()
    assert (await client.get(f"{api}/live/config")).json()["tier"] == "free"
    closed = await client.get(url)
    assert closed.status_code == 402
    assert closed.json()["detail"]["code"] == "LIVE_PLAN_REQUIRED"
    assert await db.get(LiveMaterial, uuid.UUID(detail["id"])) is not None


async def test_live_pass_sees_only_its_own_material(
    client: httpx.AsyncClient,
    api: str,
    db: AsyncSession,
    live: LiveEnv,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Багцтай байхдаа оруулсан материал эрхээр харагдахгүй — багц авахад буцна."""
    user = await student(client, api, db, "former@example.com")
    user_id = user.id
    old = await ready_material(client, api, live)
    topic = first_topic(old)
    user.plan_expires_at = datetime.now(UTC) - timedelta(days=1)
    await db.commit()
    await buy_pass(client, api, monkeypatch)

    new = await upload(client, api, filename="new.md")
    listed = (await client.get(f"{api}/live/materials")).json()
    assert [item["id"] for item in listed] == [new["id"]]
    old_url = f"{api}/live/materials/{old['id']}"
    for response in (
        await client.get(old_url),
        await client.get(f"{old_url}/cards"),
        await client.post(f"{old_url}/generations", json={"kind": "exam"}),
        await client.post(f"{api}/live/topics/{topic['id']}/guide-read"),
    ):
        assert response.status_code == 402, response.text
        assert response.json()["detail"]["code"] == "LIVE_PLAN_REQUIRED"

    user = await db.get(User, user_id)
    assert user is not None
    user.plan_expires_at = datetime.now(UTC) + timedelta(days=30)
    await db.commit()
    assert (await client.get(old_url)).status_code == 200
    assert len((await client.get(f"{api}/live/materials")).json()) == 2


async def test_unused_live_pass_never_expires_and_returns_on_early_delete(
    client: httpx.AsyncClient,
    api: str,
    db: AsyncSession,
    live: LiveEnv,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    await make_user(db, "keeper@example.com")
    await login_as(client, api, "keeper@example.com")
    await buy_pass(client, api, monkeypatch)
    await db.execute(update(LivePass).values(created_at=datetime.now(UTC) - timedelta(days=400)))
    await db.commit()
    assert (await client.get(f"{api}/live/config")).json()["passes"]["unused"] is True

    # Файл ирээгүй (бэлэн болоогүй) материалыг устгавал эрх буцна.
    created = await client.post(f"{api}/live/materials", json={"filename": "a.md", "size_bytes": 9})
    assert created.status_code == 201
    assert (await client.get(f"{api}/live/config")).json()["passes"]["unused"] is False
    deleted = await client.delete(f"{api}/live/materials/{created.json()['id']}")
    assert deleted.status_code == 204
    assert (await client.get(f"{api}/live/config")).json()["passes"]["unused"] is True

    # Бэлэн болсон материалыг устгавал эрх буцахгүй.
    detail = await ready_material(client, api, live)
    assert (await client.delete(f"{api}/live/materials/{detail['id']}")).status_code == 204
    assert (await client.get(f"{api}/live/config")).json()["tier"] == "free"


async def test_live_pass_ai_cap_is_per_material(
    client: httpx.AsyncClient,
    api: str,
    db: AsyncSession,
    live: LiveEnv,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    user = await make_user(db, "capped@example.com")
    await login_as(client, api, "capped@example.com")
    await buy_pass(client, api, monkeypatch)
    detail = await ready_material(client, api, live)
    url = f"{api}/live/materials/{detail['id']}/generations"
    generation = (await client.post(url, json={"kind": "exam"})).json()

    db.add(
        AIRequest(
            user_id=user.id,
            material_id=uuid.UUID(detail["id"]),
            capability="quiz",
            provider="gemini",
            model="m",
            prompt_version="v",
            attempt=1,
            kind="call",
            estimated_cost_usd=Decimal(str(settings.live_pass_ai_usd)),
            price_version="p",
            success=True,
        )
    )
    await db.commit()
    blocked = await client.post(url, json={"kind": "quiz"})
    assert blocked.status_code == 402
    assert blocked.json()["detail"]["code"] == "LIVE_PASS_QUOTA_EXCEEDED"
    config = (await client.get(f"{api}/live/config")).json()
    assert config["passes"]["materials"][0]["ai_used_percent"] == 100

    # Захиалсан ажил ч AI дуудахаас өмнө зогсоно.
    await live.drain()
    failed = (await client.get(f"{api}/live/generations/{generation['id']}")).json()
    assert failed["error_code"] == "LIVE_PASS_QUOTA_EXCEEDED"


async def test_admin_grants_premium_with_standard(
    client: httpx.AsyncClient, api: str, db: AsyncSession, live: LiveEnv
) -> None:
    await make_user(db, "boss@example.com", role=UserRole.ADMIN)
    paid = await make_user(db, "paid@example.com")
    await login_as(client, api, "boss@example.com")
    lookup = await client.post(
        f"{api}/live/admin/subscriptions/lookup", json={"email": "paid@example.com"}
    )
    assert lookup.json()["tier"] == "free"
    assert lookup.json()["plan_expires_at"] is None

    granted = await client.post(
        f"{api}/live/admin/subscriptions",
        json={"email": "paid@example.com", "months": 1, "note": "туршилт"},
    )
    assert granted.status_code == 200, granted.text
    body = granted.json()
    assert body["tier"] == "premium"
    expires = datetime.fromisoformat(body["expires_at"])
    assert timedelta(days=27) < expires - datetime.now(UTC) < timedelta(days=32)
    # Premium = Standard + илүү AI: Standard багц ч мөн хүртэл.
    assert datetime.fromisoformat(body["plan_expires_at"]) == expires
    adjustments = (
        (await db.execute(select(PlanAdjustment).where(PlanAdjustment.user_id == paid.id)))
        .scalars()
        .all()
    )
    assert [(row.months, row.note) for row in adjustments] == [(1, "Premium 1 сар — туршилт")]

    # Сунгахад Premium-ийн дуусах өдрөөс хуанлийн 2 сараар.
    extended = (
        await client.post(
            f"{api}/live/admin/subscriptions", json={"email": "paid@example.com", "months": 2}
        )
    ).json()
    new_expires = datetime.fromisoformat(extended["expires_at"])
    assert timedelta(days=58) <= new_expires - expires <= timedelta(days=62)
    assert datetime.fromisoformat(extended["plan_expires_at"]) == new_expires

    # Урт Standard багцыг богиносгохгүй, түүхэнд бичихгүй.
    long_plan = await make_user(db, "long@example.com")
    long_plan.plan_expires_at = datetime.now(UTC) + timedelta(days=200)
    await db.commit()
    long_until = long_plan.plan_expires_at
    result = (
        await client.post(
            f"{api}/live/admin/subscriptions", json={"email": "long@example.com", "months": 1}
        )
    ).json()
    assert result["tier"] == "premium"
    assert datetime.fromisoformat(result["plan_expires_at"]) == long_until
    history = await db.execute(
        select(func.count())
        .select_from(PlanAdjustment)
        .where(PlanAdjustment.user_id == long_plan.id)
    )
    assert history.scalar_one() == 0

    admin_grant = await client.post(
        f"{api}/live/admin/subscriptions", json={"email": "boss@example.com", "months": 1}
    )
    assert admin_grant.json()["detail"]["code"] == "LIVE_ADMIN_ALWAYS_PREMIUM"

    await login_as(client, api, "paid@example.com")
    config = (await client.get(f"{api}/live/config")).json()
    assert config["tier"] == "premium"
    # Standard багц идэвхтэй тул сургалтын төлбөртэй хичээл ч нээлттэй.
    me = (await client.get(f"{api}/auth/me")).json()
    assert me["has_plan"] is True
    await upload(client, api)
    await live.drain()
    await upload(client, api, filename="second.md")


async def test_admin_endpoints_require_admin(
    client: httpx.AsyncClient, api: str, db: AsyncSession, live: LiveEnv
) -> None:
    await student(client, api, db, "nosy@example.com")
    assert (await client.get(f"{api}/live/admin/overview")).status_code == 403
    response = await client.post(
        f"{api}/live/admin/subscriptions",
        json={"email": "nosy@example.com", "months": 1},
    )
    assert response.status_code == 403


async def test_upload_validation(
    client: httpx.AsyncClient,
    api: str,
    db: AsyncSession,
    live: LiveEnv,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    await student(client, api, db, "v@example.com")

    async def create(filename: str, size: int = 10) -> httpx.Response:
        return await client.post(
            f"{api}/live/materials", json={"filename": filename, "size_bytes": size}
        )

    assert (await create("a.exe")).json()["detail"]["code"] == "LIVE_FILE_UNSUPPORTED"
    legacy = await create("slides.ppt")
    assert legacy.status_code == 415
    assert legacy.json()["detail"]["code"] == "LIVE_FILE_LEGACY"
    assert (await create("macro.docm")).json()["detail"]["code"] == "LIVE_FILE_MACRO"
    big = await create("a.pdf", size=settings.live_max_upload_bytes + 1)
    assert big.status_code == 413

    # Өргөтгөл нь PDF, агуулга нь текст.
    fake_pdf = (await create("fake.pdf")).json()
    mismatch = await client.put(f"{api}/live/materials/{fake_pdf['id']}/content", content=b"hi")
    assert mismatch.status_code == 415
    assert mismatch.json()["detail"]["code"] == "LIVE_FILE_MISMATCH"

    # Урьдчилан хэлсэн хэмжээнээс үл хамааран уншиж байхдаа тоолно.
    monkeypatch.setattr(settings, "live_max_upload_bytes", 100)
    material = (await create("a.md")).json()
    too_big = await client.put(f"{api}/live/materials/{material['id']}/content", content=b"x" * 101)
    assert too_big.status_code == 413
    empty = await client.put(f"{api}/live/materials/{material['id']}/content", content=b"")
    assert empty.json()["detail"]["code"] == "LIVE_FILE_EMPTY"
    ok = await client.put(f"{api}/live/materials/{material['id']}/content", content=b"# A\n\ntext")
    assert ok.status_code == 202
    twice = await client.put(f"{api}/live/materials/{material['id']}/content", content=b"x")
    assert twice.json()["detail"]["code"] == "LIVE_ALREADY_UPLOADED"


async def test_other_users_see_nothing(
    client: httpx.AsyncClient, api: str, db: AsyncSession, live: LiveEnv
) -> None:
    await student(client, api, db, "owner@example.com")
    detail = await ready_material(client, api, live)
    topic = first_topic(detail)
    generation = (
        await client.post(
            f"{api}/live/materials/{detail['id']}/generations",
            json={"kind": "quiz", "topic_id": topic["id"]},
        )
    ).json()
    await live.drain()
    attempt = (await client.post(f"{api}/live/generations/{generation['id']}/attempts")).json()
    card_id = (await client.get(f"{api}/live/materials/{detail['id']}/cards")).json()[0]["id"]

    await student(client, api, db, "stranger@example.com")
    material_id = detail["id"]
    for method, path in [
        ("GET", f"/live/materials/{material_id}"),
        ("PUT", f"/live/materials/{material_id}/content"),
        ("DELETE", f"/live/materials/{material_id}"),
        ("GET", f"/live/materials/{material_id}/cards"),
        ("GET", f"/live/generations/{generation['id']}"),
        ("POST", f"/live/generations/{generation['id']}/attempts"),
        ("POST", f"/live/attempts/{attempt['id']}/finish"),
        ("POST", f"/live/topics/{topic['id']}/guide-read"),
    ]:
        response = await client.request(method, f"{api}{path}")
        assert response.status_code == 404, (method, path, response.text)
    review = await client.post(f"{api}/live/cards/{card_id}/review", json={"rating": "good"})
    assert review.status_code == 404
    assert (await client.get(f"{api}/live/materials")).json() == []


async def test_pdf_goes_to_the_extractor_and_to_ai_as_a_document(
    client: httpx.AsyncClient, api: str, db: AsyncSession, live: LiveEnv
) -> None:
    await student(client, api, db, "pdf@example.com")
    pdf = b"%PDF-1.7\n" + b"0" * 200
    material = await upload(client, api, filename="Лекц 3.pdf", body=pdf)
    await live.drain()
    detail = (await client.get(f"{api}/live/materials/{material['id']}")).json()
    assert detail["status"] == "ready"
    assert detail["page_count"] == 3
    parts = live.provider.requests[0].parts
    assert parts[0].kind == "document"
    assert parts[0].data == pdf
    assert parts[0].mime_type == "application/pdf"


@pytest.mark.parametrize(
    ("error", "code"),
    [
        (ExtractionError("LIVE_FILE_ENCRYPTED"), "LIVE_FILE_ENCRYPTED"),
        (ExtractionError("LIVE_FILE_CORRUPT"), "LIVE_FILE_CORRUPT"),
        (Extraction(500, []), "LIVE_TOO_MANY_PAGES"),
        (Extraction(1, [ExtractedPage(1, None, "  ")]), "LIVE_EMPTY_DOCUMENT"),
    ],
)
async def test_extraction_failures(
    client: httpx.AsyncClient,
    api: str,
    db: AsyncSession,
    live: LiveEnv,
    error: Any,
    code: str,
) -> None:
    await student(client, api, db, "bad@example.com")
    live.extractions["pptx"] = error
    material = await upload(client, api, filename="s.pptx", body=b"PK\x03\x04rest")
    await live.drain()
    detail = (await client.get(f"{api}/live/materials/{material['id']}")).json()
    assert detail["status"] == "failed"
    assert detail["error_code"] == code
    assert live.provider.requests == []


async def test_extractor_outage_is_retried_then_fails(
    client: httpx.AsyncClient, api: str, db: AsyncSession, live: LiveEnv
) -> None:
    await student(client, api, db, "down@example.com")
    live.extractions["docx"] = ExtractionError("LIVE_EXTRACTOR_UNAVAILABLE", retryable=True)
    material = await upload(client, api, filename="n.docx", body=b"PK\x03\x04rest")
    assert await live.drain() == settings.live_job_max_attempts
    detail = (await client.get(f"{api}/live/materials/{material['id']}")).json()
    assert detail["error_code"] == "LIVE_EXTRACTOR_UNAVAILABLE"


# --- Заавар, тест, таамаг ------------------------------------------------------


async def test_guide_is_generated_once_and_marks_mastery(
    client: httpx.AsyncClient, api: str, db: AsyncSession, live: LiveEnv
) -> None:
    await student(client, api, db, "guide@example.com")
    detail = await ready_material(client, api, live)
    topic = first_topic(detail)
    url = f"{api}/live/materials/{detail['id']}/generations"
    first = await client.post(url, json={"kind": "guide", "topic_id": topic["id"]})
    assert first.status_code == 202
    assert first.json()["status"] == "queued"
    assert first.json()["guide"] is None
    # Давтан хүсэлт ижил үүсгэлтийг буцаана — AI дахин дуудагдахгүй.
    second = await client.post(url, json={"kind": "guide", "topic_id": topic["id"]})
    assert second.json()["id"] == first.json()["id"]
    await live.drain()
    ready = (await client.get(f"{api}/live/generations/{first.json()['id']}")).json()
    assert ready["status"] == "ready"
    assert "## Гол санаа" in ready["guide"]["markdown"]
    again = await client.post(url, json={"kind": "guide", "topic_id": topic["id"]})
    assert again.json()["id"] == first.json()["id"]
    assert len([r for r in live.provider.requests if r.capability == "study_guide"]) == 1

    assert (await client.post(f"{api}/live/topics/{topic['id']}/guide-read")).status_code == 204
    after = (await client.get(f"{api}/live/materials/{detail['id']}")).json()
    studied = first_topic(after)
    assert studied["guide_read"] is True
    assert studied["mastery"] == 10
    assert after["last_studied_topic_id"] == topic["id"]


async def test_generation_rules(
    client: httpx.AsyncClient, api: str, db: AsyncSession, live: LiveEnv
) -> None:
    await student(client, api, db, "rules@example.com")
    detail = await ready_material(client, api, live)
    url = f"{api}/live/materials/{detail['id']}/generations"
    no_topic = await client.post(url, json={"kind": "guide"})
    assert no_topic.json()["detail"]["code"] == "LIVE_BAD_TOPIC"
    topic_id = first_topic(detail)["id"]
    exam_topic = await client.post(url, json={"kind": "exam", "topic_id": topic_id})
    assert exam_topic.json()["detail"]["code"] == "LIVE_BAD_TOPIC"
    foreign = await client.post(url, json={"kind": "guide", "topic_id": str(uuid.uuid4())})
    assert foreign.json()["detail"]["code"] == "LIVE_BAD_TOPIC"

    stored = await db.get(LiveMaterial, uuid.UUID(detail["id"]))
    assert stored is not None
    stored.status = "processing"
    await db.commit()
    not_ready = await client.post(url, json={"kind": "exam"})
    assert not_ready.status_code == 409


async def test_quiz_flow_never_leaks_answers(
    client: httpx.AsyncClient, api: str, db: AsyncSession, live: LiveEnv
) -> None:
    await student(client, api, db, "quiz@example.com")
    detail = await ready_material(client, api, live)
    topic = first_topic(detail)
    generation = (
        await client.post(
            f"{api}/live/materials/{detail['id']}/generations",
            json={"kind": "quiz", "topic_id": topic["id"]},
        )
    ).json()
    await live.drain()
    quiz = (await client.get(f"{api}/live/generations/{generation['id']}")).json()
    assert quiz["status"] == "ready"
    questions = quiz["quiz"]["questions"]
    assert len(questions) == settings.live_topic_quiz_questions
    assert all(len(question["options"]) == 4 for question in questions)
    assert all(question["topic_id"] == topic["id"] for question in questions)
    assert "correct" not in json.dumps(quiz)
    assert "explanation" not in json.dumps(quiz)

    attempt = await client.post(f"{api}/live/generations/{generation['id']}/attempts")
    assert attempt.status_code == 201
    attempt_id = attempt.json()["id"]
    assert attempt.json()["total"] == len(questions)
    keys = {
        question.id: question.correct_index
        for question in (await db.execute(select(LiveQuestion))).scalars().all()
    }
    for index, question in enumerate(questions):
        correct = keys[uuid.UUID(question["id"])]
        # Эхний асуултад буруу, бусдад зөв хариулна.
        choice = (correct + 1) % 4 if index == 0 else correct
        result = await client.post(
            f"{api}/live/attempts/{attempt_id}/answers",
            json={"question_id": question["id"], "choice_index": choice},
        )
        assert result.status_code == 200, result.text
        assert result.json()["correct"] is (index != 0)
        assert result.json()["correct_index"] == correct
        assert result.json()["explanation"]
    duplicate = await client.post(
        f"{api}/live/attempts/{attempt_id}/answers",
        json={"question_id": questions[0]["id"], "choice_index": 0},
    )
    assert duplicate.json()["detail"]["code"] == "LIVE_ALREADY_ANSWERED"

    finished = await client.post(f"{api}/live/attempts/{attempt_id}/finish")
    assert finished.status_code == 200
    result = finished.json()
    total = len(questions)
    assert result["correct_count"] == total - 1
    assert result["percent"] == round(100 * (total - 1) / total)
    assert result["topics"][0]["topic_id"] == topic["id"]
    assert result["topics"][0]["mastery"] == round(50 * (total - 1) / total)
    # Давтан дуусгахад ижил дүн, эзэмшил хоёр дахин нэмэгдэхгүй.
    assert (await client.post(f"{api}/live/attempts/{attempt_id}/finish")).json() == result
    late = await client.post(
        f"{api}/live/attempts/{attempt_id}/answers",
        json={"question_id": questions[1]["id"], "choice_index": 0},
    )
    assert late.json()["detail"]["code"] == "LIVE_ATTEMPT_FINISHED"
    topic_after = first_topic((await client.get(f"{api}/live/materials/{detail['id']}")).json())
    assert topic_after["quiz_percent"] == result["percent"]


async def test_full_quiz_exam_and_regenerate(
    client: httpx.AsyncClient, api: str, db: AsyncSession, live: LiveEnv
) -> None:
    await student(client, api, db, "full@example.com")
    detail = await ready_material(client, api, live)
    url = f"{api}/live/materials/{detail['id']}/generations"
    quiz = (await client.post(url, json={"kind": "quiz"})).json()
    exam = (await client.post(url, json={"kind": "exam"})).json()
    assert quiz["topic_id"] is None
    await live.drain()
    after = (await client.get(f"{api}/live/materials/{detail['id']}")).json()
    assert after["full_quiz"]["status"] == "ready"
    assert after["exam"]["status"] == "ready"
    full = (await client.get(f"{api}/live/generations/{quiz['id']}")).json()
    assert len(full["quiz"]["questions"]) == settings.live_full_quiz_questions
    assert len({question["topic_id"] for question in full["quiz"]["questions"]}) == 4
    predicted = (await client.get(f"{api}/live/generations/{exam['id']}")).json()["exam"]
    topic_ids = {topic["id"] for section in detail["sections"] for topic in section["topics"]}
    assert {item["topic_id"] for item in predicted["predictions"]} <= topic_ids
    assert predicted["study_plan"]

    await client.post(f"{api}/live/generations/{quiz['id']}/attempts")
    fresh = await client.post(url, json={"kind": "quiz", "regenerate": True})
    assert fresh.json()["id"] != quiz["id"]
    assert fresh.json()["status"] == "queued"
    assert await db.get(LiveGeneration, uuid.UUID(quiz["id"])) is None
    await live.drain()
    assert (await client.get(f"{api}/live/generations/{fresh.json()['id']}")).json()["quiz"]


async def test_invalid_quiz_output_is_repaired_once(
    client: httpx.AsyncClient, api: str, db: AsyncSession, live: LiveEnv
) -> None:
    await student(client, api, db, "repair@example.com")
    detail = await ready_material(client, api, live)
    bad = json.dumps(
        {
            "questions": [
                {
                    "prompt": "Ижил хариулттай",
                    "options": ["а", "а", "б", "в"],
                    "correct_index": 0,
                    "explanation": "",
                    "topic_key": "topic-1",
                    "page": 0,
                }
            ]
        }
    )
    live.provider.script = [bad]
    generation = (
        await client.post(
            f"{api}/live/materials/{detail['id']}/generations",
            json={"kind": "quiz", "topic_id": first_topic(detail)["id"]},
        )
    ).json()
    await live.drain()
    ready = (await client.get(f"{api}/live/generations/{generation['id']}")).json()
    assert ready["status"] == "ready"
    quiz_calls = [r for r in live.provider.requests if r.capability == "topic_quiz"]
    assert len(quiz_calls) == 2
    assert "шаардлагад нийцсэнгүй" in (quiz_calls[1].parts[-1].text or "")
    kinds = (
        (
            await db.execute(
                select(AIRequest.kind, AIRequest.success)
                .where(AIRequest.capability == "topic_quiz")
                .order_by(AIRequest.attempt)
            )
        )
        .tuples()
        .all()
    )
    assert kinds == [("call", False), ("repair", True)]


async def test_ai_failures_are_reported_on_the_generation(
    client: httpx.AsyncClient, api: str, db: AsyncSession, live: LiveEnv
) -> None:
    await student(client, api, db, "fail@example.com")
    detail = await ready_material(client, api, live)
    url = f"{api}/live/materials/{detail['id']}/generations"
    # Буруу хүсэлт (4xx) — дахин оролдохгүй, шууд бүтэлгүйтнэ.
    live.provider.script = [AIError("http_400", "bad request")]
    generation = (await client.post(url, json={"kind": "exam"})).json()
    await live.drain()
    failed = (await client.get(f"{api}/live/generations/{generation['id']}")).json()
    assert failed["status"] == "failed"
    assert failed["error_code"] == "LIVE_AI_FAILED"
    assert failed["error_message"]
    # Энгийн хүсэлт бүтэлгүйтснийг буцаана — AI-г зөвхөн «Дахин оролдох» дуудна.
    same = await client.post(url, json={"kind": "exam"})
    assert same.json()["id"] == generation["id"]
    assert same.json()["status"] == "failed"
    retry = await client.post(url, json={"kind": "exam", "regenerate": True})
    assert retry.json()["id"] != generation["id"]
    assert retry.json()["status"] == "queued"


async def test_gemini_overload_waits_for_the_model(
    client: httpx.AsyncClient, api: str, db: AsyncSession, live: LiveEnv
) -> None:
    """Ганц загвартай бол ачааллын дараа хөргөлт дуустал хүлээж, дахин оролдоно."""
    await student(client, api, db, "busy@example.com")
    detail = await ready_material(client, api, live)
    url = f"{api}/live/materials/{detail['id']}/generations"
    overloaded = AIError("http_503", "service_unavailable", retryable=True)

    live.provider.script = [overloaded] * 3
    guide = (
        await client.post(url, json={"kind": "guide", "topic_id": first_topic(detail)["id"]})
    ).json()
    await live.drain()
    assert (await client.get(f"{api}/live/generations/{guide['id']}")).json()["status"] == "ready"
    kinds = (
        (
            await db.execute(
                select(AIRequest.kind)
                .where(AIRequest.capability == "study_guide")
                .order_by(AIRequest.created_at)
            )
        )
        .scalars()
        .all()
    )
    assert kinds == ["call", "retry", "retry", "retry"]
    # Хөргөлт дараалсан алдаанд өсдөг: 4, 8, 16 с.
    assert live.clock.slept == [4.0, 8.0, 16.0]
    assert live.health.remaining("fake:test") == 0

    # Удаан үргэлжилсэн ачаалал — нэг удаа дараалалд буцаад, дараа нь ойлгомжтой алдаа.
    live.provider.script = [overloaded] * 50
    live.clock.slept.clear()
    exam = (await client.post(url, json={"kind": "exam"})).json()
    assert await live.drain() == settings.live_job_max_attempts
    busy = (await client.get(f"{api}/live/generations/{exam['id']}")).json()
    assert busy["status"] == "failed"
    assert busy["error_code"] == "LIVE_AI_BUSY"
    assert "ачаалалтай" in busy["error_message"]
    calls = 50 - len(live.provider.script)
    assert calls <= (1 + MAX_TRANSIENT_ERRORS) * settings.live_job_max_attempts
    # Нэг хүлээлт 1 минутаас, нэг ажил ~5 минутаас хэтрэхгүй.
    assert max(live.clock.slept) <= 60
    assert sum(live.clock.slept) <= 5 * 60 * settings.live_job_max_attempts
    # Эдгээр дуудлага токен зарцуулаагүй — зардал 0.
    cost = (
        await db.execute(
            select(func.sum(AIRequest.estimated_cost_usd)).where(AIRequest.capability == "exam")
        )
    ).scalar_one()
    assert cost == 0


async def test_router_hands_off_to_the_next_model(
    client: httpx.AsyncClient,
    api: str,
    db: AsyncSession,
    live: LiveEnv,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Хязгаарт хүрсэн (429) эсвэл ачаалалтай (503) загвараас дараагийнх руу хүлээлгүй."""
    await student(client, api, db, "router@example.com")
    detail = await ready_material(client, api, live)
    monkeypatch.setattr(settings, "ai_models", ["fake:strong", "fake:cheap"])
    url = f"{api}/live/materials/{detail['id']}/generations"

    live.provider.script = [
        AIError("http_429", "rate_limit_exceeded", retryable=True, retry_after=30.0)
    ]
    exam = (await client.post(url, json={"kind": "exam"})).json()
    await live.drain()
    ready = (await client.get(f"{api}/live/generations/{exam['id']}")).json()
    assert ready["status"] == "ready"
    calls = [r.model for r in live.provider.requests if r.capability == "exam"]
    assert calls == ["strong", "cheap"]
    assert live.clock.slept == []
    stored = await db.get(LiveGeneration, uuid.UUID(exam["id"]))
    assert stored is not None and stored.model == "fake:cheap"
    rows = (
        await db.execute(
            select(AIRequest.model, AIRequest.kind, AIRequest.error_code)
            .where(AIRequest.capability == "exam")
            .order_by(AIRequest.created_at)
        )
    ).all()
    assert [tuple(row) for row in rows] == [
        ("strong", "call", "http_429"),
        ("cheap", "fallback", None),
    ]
    # Google хэлсэн 30 с хүртэл хүчтэй загвар алгасагдана — дараагийн ажил шууд хямд руу.
    assert 29 < live.health.remaining("fake:strong") <= 30
    guide = (
        await client.post(url, json={"kind": "guide", "topic_id": first_topic(detail)["id"]})
    ).json()
    await live.drain()
    assert [r.model for r in live.provider.requests if r.capability == "study_guide"] == ["cheap"]
    assert (await client.get(f"{api}/live/generations/{guide['id']}")).json()["status"] == "ready"

    # Админ хаанаас хязгаарт хүрснийг харна.
    await make_user(db, "ops@example.com", role=UserRole.ADMIN)
    await login_as(client, api, "ops@example.com")
    models = {item["model"]: item for item in (await client.get(f"{api}/live/admin/models")).json()}
    assert models["fake:strong"]["status"] == "cooling"
    assert models["fake:strong"]["reason"] == "rate_limited"
    assert models["fake:strong"]["available_at"]
    assert models["fake:strong"]["last_error"] == "http_429"
    assert models["fake:cheap"]["status"] == "ready"
    assert {task["position"] for task in models["fake:cheap"]["tasks"]} == {2}
    assert models["fake:cheap"]["month_requests"] >= 2

    # Хөргөлт дуусмагц хүчтэй загвар дахин үндсэн.
    live.clock.now += 31
    assert live.health.remaining("fake:strong") == 0


async def test_router_skips_models_near_their_usage_limit(
    client: httpx.AsyncClient,
    api: str,
    db: AsyncSession,
    live: LiveEnv,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """AI Studio-гийн хязгаар (`AI_MODEL_LIMITS`) — 90%-д хүрмэгц дараагийн загвар."""
    await student(client, api, db, "limits@example.com")
    detail = await ready_material(client, api, live)
    monkeypatch.setattr(settings, "ai_models", ["fake:strong", "fake:cheap"])
    monkeypatch.setattr(settings, "ai_model_limits", {"fake:strong": {"rpm": 3}})
    for _ in range(2):
        db.add(
            AIRequest(
                capability="exam",
                provider="fake",
                model="strong",
                prompt_version="v",
                attempt=1,
                kind="call",
                price_version="p",
                success=True,
            )
        )
    await db.commit()
    url = f"{api}/live/materials/{detail['id']}/generations"
    exam = (await client.post(url, json={"kind": "exam"})).json()
    await live.drain()
    assert [r.model for r in live.provider.requests if r.capability == "exam"] == ["cheap"]
    assert (await client.get(f"{api}/live/generations/{exam['id']}")).json()["status"] == "ready"

    await make_user(db, "limits-admin@example.com", role=UserRole.ADMIN)
    await login_as(client, api, "limits-admin@example.com")
    models = {item["model"]: item for item in (await client.get(f"{api}/live/admin/models")).json()}
    assert models["fake:strong"]["status"] == "near_limit"
    assert models["fake:strong"]["reason"] == "rpm"
    assert models["fake:strong"]["limits"] == {"rpm": 3, "tpm": None, "rpd": None}
    assert models["fake:strong"]["minute_requests"] == 2


# --- Карт ------------------------------------------------------------------


async def test_card_reviews_follow_leitner_boxes(
    client: httpx.AsyncClient, api: str, db: AsyncSession, live: LiveEnv
) -> None:
    await student(client, api, db, "cards@example.com")
    detail = await ready_material(client, api, live)
    topic = first_topic(detail)
    cards = (
        await client.get(
            f"{api}/live/materials/{detail['id']}/cards", params={"topic_id": topic["id"]}
        )
    ).json()
    assert len(cards) == topic["card_count"] > 0
    assert all(card["box"] == 0 and card["due_at"] is None for card in cards)

    good = await client.post(f"{api}/live/cards/{cards[0]['id']}/review", json={"rating": "good"})
    assert good.json()["box"] == 1
    assert datetime.fromisoformat(good.json()["due_at"]) > datetime.now(UTC) + timedelta(hours=23)
    again = await client.post(
        f"{api}/live/cards/{cards[-1]['id']}/review", json={"rating": "again"}
    )
    assert again.json()["box"] == 0

    due = (
        await client.get(
            f"{api}/live/materials/{detail['id']}/cards", params={"topic_id": topic["id"]}
        )
    ).json()
    assert cards[0]["id"] not in {card["id"] for card in due}
    everything = (
        await client.get(f"{api}/live/materials/{detail['id']}/cards", params={"mode": "all"})
    ).json()
    assert len(everything) == detail["cards"]["total"]

    after = (await client.get(f"{api}/live/materials/{detail['id']}")).json()
    assert first_topic(after)["mastery"] == round(40 * 1 / (4 * topic["card_count"]))
    assert after["cards"]["new"] == detail["cards"]["total"] - 2
    assert after["last_studied_topic_id"] == topic["id"]


# --- Төсөв ------------------------------------------------------------------


async def test_budgets_block_new_ai_work(
    client: httpx.AsyncClient, api: str, db: AsyncSession, live: LiveEnv
) -> None:
    user = await student(client, api, db, "spender@example.com")
    detail = await ready_material(client, api, live)
    url = f"{api}/live/materials/{detail['id']}/generations"

    def row(user_id: uuid.UUID | None, cost: str) -> AIRequest:
        return AIRequest(
            user_id=user_id,
            capability="quiz",
            provider="gemini",
            model="m",
            prompt_version="v",
            attempt=1,
            kind="call",
            estimated_cost_usd=Decimal(cost),
            price_version="p",
            success=True,
        )

    db.add(row(user.id, str(settings.live_standard_ai_monthly_usd)))
    await db.commit()
    blocked = await client.post(url, json={"kind": "exam"})
    assert blocked.status_code == 402
    assert blocked.json()["detail"]["code"] == "LIVE_QUOTA_EXCEEDED"
    config = (await client.get(f"{api}/live/config")).json()
    assert config["usage"]["ai_used_percent"] == 100

    await db.execute(update(AIRequest).values(user_id=None))
    db.add(row(None, str(settings.ai_platform_monthly_budget_usd)))
    await db.commit()
    paused = await client.post(url, json={"kind": "exam"})
    assert paused.status_code == 503
    assert paused.json()["detail"]["code"] == "LIVE_AI_PAUSED"


async def test_budget_is_checked_again_before_each_ai_call(
    client: httpx.AsyncClient, api: str, db: AsyncSession, live: LiveEnv
) -> None:
    user = await student(client, api, db, "late@example.com")
    detail = await ready_material(client, api, live)
    generation = (
        await client.post(f"{api}/live/materials/{detail['id']}/generations", json={"kind": "exam"})
    ).json()
    # Захиалсны дараа, ажил эхлэхээс өмнө хязгаарт хүрсэн.
    db.add(
        AIRequest(
            user_id=user.id,
            capability="quiz",
            provider="gemini",
            model="m",
            prompt_version="v",
            attempt=1,
            kind="call",
            estimated_cost_usd=Decimal(str(settings.live_standard_ai_monthly_usd)),
            price_version="p",
            success=True,
        )
    )
    await db.commit()
    await live.drain()
    failed = (await client.get(f"{api}/live/generations/{generation['id']}")).json()
    assert failed["error_code"] == "LIVE_QUOTA_EXCEEDED"
    assert [r for r in live.provider.requests if r.capability == "exam"] == []


async def test_ai_not_configured(
    client: httpx.AsyncClient,
    api: str,
    db: AsyncSession,
    live: LiveEnv,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    await student(client, api, db, "nokey@example.com")
    monkeypatch.setattr(settings, "ai_models", [])
    monkeypatch.setattr(settings, "ai_document_models", ["gemini:gemini-test"])
    monkeypatch.setattr(settings, "gemini_api_key", "")
    assert (await client.get(f"{api}/live/config")).json()["ai_configured"] is False
    response = await client.post(
        f"{api}/live/materials",
        json={"filename": "a.md", "size_bytes": 10},
    )
    assert response.status_code == 503
    assert response.json()["detail"]["code"] == "LIVE_AI_NOT_CONFIGURED"


# --- Устгал -----------------------------------------------------------------


async def test_deleting_a_material_removes_its_files(
    client: httpx.AsyncClient, api: str, db: AsyncSession, live: LiveEnv
) -> None:
    await student(client, api, db, "del@example.com")
    detail = await ready_material(client, api, live)
    stored = await db.get(LiveMaterial, uuid.UUID(detail["id"]))
    assert stored is not None
    keys = {stored.storage_key, stored.text_key}
    assert all((live.storage_dir / key).exists() for key in keys if key)
    assert (await client.delete(f"{api}/live/materials/{detail['id']}")).status_code == 204
    queued = set((await db.execute(select(LiveBlobDeletion.storage_key))).scalars().all())
    assert queued == keys
    assert (await db.execute(select(func.count()).select_from(LiveTopic))).scalar_one() == 0
    assert await purge.drain_blob_deletions(db, live.storage) == 2
    assert not any((live.storage_dir / key).exists() for key in keys if key)
    assert (await db.execute(select(func.count()).select_from(LiveBlobDeletion))).scalar_one() == 0


async def test_account_deletion_cascades_live_data(
    client: httpx.AsyncClient, api: str, db: AsyncSession, live: LiveEnv
) -> None:
    user = await student(client, api, db, "gone@example.com")
    detail = await ready_material(client, api, live)
    topic = first_topic(detail)
    generation = (
        await client.post(
            f"{api}/live/materials/{detail['id']}/generations",
            json={"kind": "quiz", "topic_id": topic["id"]},
        )
    ).json()
    await live.drain()
    attempt = (await client.post(f"{api}/live/generations/{generation['id']}/attempts")).json()
    await client.post(f"{api}/live/attempts/{attempt['id']}/finish")
    card = (await client.get(f"{api}/live/materials/{detail['id']}/cards")).json()[0]
    await client.post(f"{api}/live/cards/{card['id']}/review", json={"rating": "good"})

    await db.execute(
        update(User).where(User.id == user.id).values(deletion_scheduled_at=func.now())
    )
    await db.commit()
    async with httpx.AsyncClient() as auth:
        assert await account_service.purge_due_accounts(db, auth) == 1
    for model in (LiveMaterial, LiveTopic, LiveCard, LiveTopicProgress):
        assert (await db.execute(select(func.count()).select_from(model))).scalar_one() == 0
    # Зардлын мөр үлдэж, хэрэглэгчээс салсан.
    costs = (await db.execute(select(AIRequest.user_id, AIRequest.material_id))).all()
    assert costs and all(row == (None, None) for row in costs)
    assert (await db.execute(select(func.count()).select_from(LiveBlobDeletion))).scalar_one() == 2


# --- Дараалал -----------------------------------------------------------------


async def test_worker_recovers_interrupted_jobs(
    client: httpx.AsyncClient, api: str, db: AsyncSession, live: LiveEnv
) -> None:
    await student(client, api, db, "crash@example.com")
    material = await upload(client, api)
    await db.execute(
        update(LiveMaterial).values(status="processing", attempts=1, claimed_at=func.now())
    )
    await db.commit()
    await worker.recover(live.ctx)
    db.expire_all()
    assert (await db.get(LiveMaterial, uuid.UUID(material["id"]))).status == "queued"

    await db.execute(update(LiveMaterial).values(status="processing", attempts=5))
    await db.commit()
    await worker.recover(live.ctx)
    db.expire_all()
    stored = await db.get(LiveMaterial, uuid.UUID(material["id"]))
    assert stored is not None
    assert (stored.status, stored.error_code) == ("failed", "LIVE_INTERRUPTED")


async def test_deleted_material_mid_job_is_ignored(
    client: httpx.AsyncClient, api: str, db: AsyncSession, live: LiveEnv
) -> None:
    await student(client, api, db, "vanish@example.com")
    material = await upload(client, api)
    job = await worker.claim(live.ctx)
    assert job == ("material", uuid.UUID(material["id"]))
    assert (await client.delete(f"{api}/live/materials/{material['id']}")).status_code == 204
    await worker.run_job(live.ctx, job)
    assert (await db.execute(select(func.count()).select_from(LiveTopic))).scalar_one() == 0
