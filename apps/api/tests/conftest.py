"""Тестийн орчин.

Схемийг session-д нэг удаа үүсгэж, тест бүрийн өмнө хүснэгтүүдийг цэвэрлэнэ.
Engine-ийг тест бүрт шинээр үүсгэдэг — pytest-asyncio нь тест тус бүрд өөр
event loop ажиллуулдаг тул холболтыг дамжуулж болохгүй.
"""

import os
from collections.abc import AsyncGenerator
from datetime import UTC, datetime

os.environ.setdefault("ENVIRONMENT", "test")
os.environ.setdefault("RATE_LIMIT_ENABLED", "false")
os.environ.setdefault("BCRYPT_ROUNDS", "4")  # тест хурдасгах

import httpx  # noqa: E402
import pytest  # noqa: E402
from sqlalchemy import create_engine, text  # noqa: E402
from sqlalchemy.ext.asyncio import (  # noqa: E402
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool  # noqa: E402

from app.core.config import settings  # noqa: E402
from app.core.security import hash_password  # noqa: E402
from app.db.base import Base  # noqa: E402
from app.db.session import get_db  # noqa: E402
from app.main import app  # noqa: E402
from app.models.enums import UserRole  # noqa: E402
from app.models.user import User  # noqa: E402

TABLES = (
    "ai_requests",
    "live_blob_deletions",
    "live_subscriptions",
    "live_passes",
    "live_quiz_answers",
    "live_quiz_attempts",
    "live_questions",
    "live_generations",
    "live_card_progress",
    "live_topic_progress",
    "live_cards",
    "live_topics",
    "live_materials",
    "announcements",
    "community_suspensions",
    "community_post_likes",
    "community_comments",
    "community_posts",
    "feedback",
    "plan_adjustments",
    "plan_prices",
    "promo_redemptions",
    "payments",
    "referrals",
    "promo_codes",
    "user_avatars",
    "user_badges",
    "lesson_progress",
    "enrollments",
    "lessons",
    "modules",
    "courses",
    "users",
)


def _test_database_url() -> str:
    """Үндсэн DSN-ийн зөвхөн сангийн нэрийг солино (хэрэглэгчийн нэрийг биш)."""
    base, _, database = settings.database_url.rpartition("/")
    return f"{base}/{database}_test"


TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL", _test_database_url())
SYNC_URL = TEST_DATABASE_URL.replace("+asyncpg", "+psycopg")


@pytest.fixture(scope="session", autouse=True)
def _schema() -> None:
    """Схемийг синхрон холболтоор үүсгэнэ — event loop-той холбоогүй."""
    admin_url = SYNC_URL.rpartition("/")[0] + "/postgres"
    admin_engine = create_engine(admin_url, isolation_level="AUTOCOMMIT")
    database = TEST_DATABASE_URL.rpartition("/")[2]
    with admin_engine.connect() as conn:
        exists = conn.execute(
            text("SELECT 1 FROM pg_database WHERE datname = :name"), {"name": database}
        ).scalar()
        if not exists:
            conn.execute(text(f'CREATE DATABASE "{database}"'))
    admin_engine.dispose()

    engine = create_engine(SYNC_URL)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    engine.dispose()


@pytest.fixture
async def db() -> AsyncGenerator[AsyncSession, None]:
    engine = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool)
    async with engine.begin() as conn:
        await conn.execute(text(f"TRUNCATE {', '.join(TABLES)} RESTART IDENTITY CASCADE"))

    factory = async_sessionmaker(bind=engine, expire_on_commit=False, autoflush=False)
    async with factory() as session:
        yield session
    await engine.dispose()


@pytest.fixture
async def client(db: AsyncSession) -> AsyncGenerator[httpx.AsyncClient, None]:
    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        yield db

    app.dependency_overrides[get_db] = override_get_db
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as http_client:
        yield http_client
    app.dependency_overrides.clear()


@pytest.fixture
def api() -> str:
    return settings.api_v1_prefix


TEST_PASSWORD = "Nuuts12345"


async def make_user(db: AsyncSession, email: str, role: str = UserRole.STUDENT) -> User:
    user = User(
        email=email,
        name="Тест",
        password_hash=hash_password(TEST_PASSWORD),
        role=role,
        email_verified_at=datetime.now(UTC),
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def login_as(client: httpx.AsyncClient, api: str, email: str) -> None:
    response = await client.post(
        f"{api}/auth/login", json={"email": email, "password": TEST_PASSWORD}
    )
    assert response.status_code == 200, response.text
