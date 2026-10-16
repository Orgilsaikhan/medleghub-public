"""Хөгжүүлэлтийн жишээ өгөгдөл.

Ажиллуулах:
    python -m app.seed            # агуулгыг `app/content/`-той тэнцүү болгоно
    python -m app.seed --reset    # бүх сургалт, хэрэглэгчийг устгаад шинээр

`--reset` нь тест ажиллуулсны дараа санг цэвэрлэхэд тохиромжтой.
Production дээр ажиллуулахгүй.

Хичээлийн агуулга нь `app/content/` дотор байрлана — энэ файл зөвхөн
өгөгдлийн санд бичих ажлыг гүйцэтгэнэ.

ЯАГААД ЗӨВХӨН НЭМЭХГҮЙ, ШИНЭЧИЛДЭГ ВЭ
──────────────────────────────────────
Өмнө нь slug давхцвал сургалтыг бүхэлд нь алгасдаг байв. Тиймээс
`app/content/`-д хичээл нэмсэн ч хөгжүүлэгчийн санд хуучин хувилбар үлдэж,
«яагаад өөрчлөлт харагдахгүй байна вэ» гэсэн эргэлзээ төрүүлдэг байлаа.
Одоо байгаа сургалтын агуулгыг spec-тэй тэнцүү болгоно.

Хичээлийг `slug`-аар нь тааруулдаг тул ахиц (`lesson_progress`) болон
бүртгэл (`enrollments`) хэвээр үлдэнэ. Зөвхөн spec-ээс бүрмөсөн хасагдсан
хичээлийн ахиц устана.

АНХААР: админ хэсгээс ГАРААР засварласан сургалт нь spec дээр байвал
дарагдана. Spec-д байхгүй сургалтад (E2E тестийн үүсгэсэн гэх мэт) хүрэхгүй.
"""

import asyncio
import os
import sys
from datetime import UTC, datetime, timedelta

from sqlalchemy import delete, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.content import COURSES
from app.content.community import OFFICIAL_POSTS, OfficialPost
from app.content.exercises import exercise_payload
from app.content.promo_codes import SEED_PROMO_CODES, SeedPromoCode
from app.content.types import CourseSpec
from app.core.config import settings
from app.core.security import hash_password
from app.db.session import SessionFactory, engine
from app.models.community_post import CommunityPost
from app.models.course import Course
from app.models.enums import UserRole
from app.models.lesson import Lesson
from app.models.module import Module
from app.models.promo_code import PromoCode
from app.models.user import User
from app.services.promo_service import random_code

ADMIN_EMAIL = os.getenv("SEED_ADMIN_EMAIL", "admin@suralts.mn")
DEFAULT_ADMIN_PASSWORD = "Admin12345"
ADMIN_PASSWORD = os.getenv("SEED_ADMIN_PASSWORD", DEFAULT_ADMIN_PASSWORD)
STUDENT_EMAIL = os.getenv("SEED_STUDENT_EMAIL", "suragch@suralts.mn")
STUDENT_PASSWORD = os.getenv("SEED_STUDENT_PASSWORD", "Suragch12345")
# Standard багцтай сурагч — төлбөрт хичээлүүдийг хөгжүүлэлт, E2E тестэд үзэхэд.
# `suragch@` нь үнэгүй хэрэглэгч хэвээр — багцын саналыг тэрээр харна.
STANDARD_EMAIL = os.getenv("SEED_STANDARD_EMAIL", "standard@suralts.mn")
STANDARD_PASSWORD = os.getenv("SEED_STANDARD_PASSWORD", "Standard12345")

TABLES_IN_DELETE_ORDER = (
    "announcements",
    "community_post_likes",
    "community_comments",
    "community_posts",
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


def _use_utf8_output() -> None:
    """Windows console-ийн анхдагч cp1252 нь кирилл үсгийг хэвлэж чадахгүй."""
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            reconfigure(encoding="utf-8", errors="replace")


async def _ensure_user(
    db: AsyncSession,
    email: str,
    name: str,
    password: str,
    role: str,
    *,
    plan: bool = False,
) -> None:
    user = (await db.execute(select(User).where(User.email == email))).scalar_one_or_none()
    if user:
        print(f"  = хэрэглэгч байна: {email}")
    else:
        user = User(
            email=email,
            name=name,
            password_hash=hash_password(password),
            role=role,
            # Seed-ийн данс имэйл кодгүйгээр нэвтэрнэ.
            email_verified_at=datetime.now(UTC),
        )
        db.add(user)
        print(f"  + хэрэглэгч: {email} ({role})")
    if not user.referral_code:
        user.referral_code = random_code()
    if plan:
        # Seed бүрт сунгана — хөгжүүлэгчийн багц хэзээ ч дуусахгүй.
        user.plan_expires_at = datetime.now(UTC) + timedelta(days=3650)


async def _sync_curriculum(db: AsyncSession, course: Course, spec: CourseSpec) -> tuple[int, int]:
    """Модул, хичээлийг spec-тэй тэнцүү болгоно. (шинэ, хасагдсан) тоог буцаана.

    Модулийг байрлалаар нь, хичээлийг `slug`-аар нь тааруулна. Хичээлийн `id`
    хэвээр үлдэх нь чухал — түүнд ахицын бичлэг холбогддог.
    """
    modules = list(
        (
            await db.execute(
                select(Module).where(Module.course_id == course.id).order_by(Module.position)
            )
        ).scalars()
    )
    lessons = list(
        (
            await db.execute(select(Lesson).join(Module).where(Module.course_id == course.id))
        ).scalars()
    )
    by_slug = {lesson.slug: lesson for lesson in lessons}
    shine = 0

    for module_position, module_spec in enumerate(spec.modules):
        if module_position < len(modules):
            module = modules[module_position]
        else:
            module = Module(course_id=course.id)
            db.add(module)

        module.title = module_spec.title
        module.description = module_spec.description
        module.position = module_position
        await db.flush()

        for lesson_position, lesson_spec in enumerate(module_spec.lessons):
            lesson = by_slug.get(lesson_spec.slug)
            if lesson is None:
                lesson = Lesson(slug=lesson_spec.slug)
                db.add(lesson)
                shine += 1

            lesson.module_id = module.id
            lesson.title = lesson_spec.title
            lesson.description = lesson_spec.description
            lesson.video_url = lesson_spec.video_url
            lesson.duration = lesson_spec.duration
            lesson.content = lesson_spec.content
            lesson.initial_code = lesson_spec.initial_code
            lesson.language = lesson_spec.language
            lesson.position = lesson_position
            lesson.published = lesson_spec.published
            lesson.challenging = lesson_spec.challenging
            lesson.exercise = exercise_payload(lesson_spec.exercise)

    # Шилжүүлэлт бүрэн бичигдсэний ДАРАА л илүүдлийг устгана. Эс бөгөөс өөр
    # модул руу зөөгдөх ёстой хичээл хуучин модултайгаа хамт устана.
    await db.flush()

    spec_slugs = {lesson.slug for module in spec.modules for lesson in module.lessons}
    hassan_lessons = [lesson.id for lesson in lessons if lesson.slug not in spec_slugs]
    hassan_modules = [module.id for module in modules[len(spec.modules) :]]

    # ORM-ийн cascade биш DB-ийн `ON DELETE CASCADE`-д найдна — session дэх
    # хуучирсан хамаарлын жагсаалт хадгалагдах хичээлийг татаж авахгүй.
    if hassan_lessons:
        await db.execute(delete(Lesson).where(Lesson.id.in_(hassan_lessons)))
    if hassan_modules:
        await db.execute(delete(Module).where(Module.id.in_(hassan_modules)))

    return shine, len(hassan_lessons)


async def _sync_course(db: AsyncSession, spec: CourseSpec) -> None:
    course = (await db.execute(select(Course).where(Course.slug == spec.slug))).scalar_one_or_none()
    shine_surgalt = course is None

    if course is None:
        course = Course(slug=spec.slug)
        db.add(course)

    course.title = spec.title
    course.description = spec.description
    course.thumbnail_url = spec.thumbnail_url
    course.difficulty = spec.difficulty
    course.category = spec.category
    course.is_free = spec.is_free
    course.free_lessons = spec.free_lessons
    course.published = spec.published
    await db.flush()

    shine, hassan = await _sync_curriculum(db, course, spec)
    hemjee = f"{len(spec.modules)} модул, {spec.lesson_count} хичээл"

    if shine_surgalt:
        print(f"  + сургалт: {spec.slug} ({hemjee})")
    elif shine or hassan:
        print(f"  ~ сургалт шинэчлэгдлээ: {spec.slug} ({hemjee}; +{shine} шинэ, -{hassan} хасав)")
    else:
        print(f"  = сургалт хэвээр: {spec.slug} ({hemjee})")


async def _sync_official_posts(db: AsyncSession, posts: tuple[OfficialPost, ...]) -> None:
    """MedlegHub-ийн Community нийтлэлийг `id`-аар нь нэмж эсвэл шинэчилнэ.

    Лайк, сэтгэгдэл нь `id`-д холбогддог тул хэвээр үлдэнэ. Шинээр нэмэхэд
    жагсаалтын дарааллаар секунд зөрүүтэй огноо тавина — сүүлийнх нь хамгийн шинэ.
    """
    now = datetime.now(UTC)
    for index, spec in enumerate(posts):
        post = await db.get(CommunityPost, spec.id)
        if post is None:
            post = CommunityPost(id=spec.id, created_at=now - timedelta(seconds=len(posts) - index))
            db.add(post)
            print(f"  + Community нийтлэл: {spec.title}")
        else:
            print(f"  = Community нийтлэл: {spec.title}")
        post.author_id = None
        post.title = spec.title
        post.body = spec.body
        post.language = spec.language
        post.type = spec.type
        post.pinned = spec.pinned


async def _ensure_promo_codes(db: AsyncSession, codes: tuple[SeedPromoCode, ...]) -> None:
    """Байхгүй кодыг л нэмнэ — админы өөрчилсөн хугацаа, төлөвийг дарахгүй."""
    for spec in codes:
        exists = (await db.execute(select(PromoCode.id).where(PromoCode.code == spec.code))).first()
        if exists:
            print(f"  = промо код байна: {spec.code}")
            continue
        db.add(
            PromoCode(
                code=spec.code,
                kind=spec.kind,
                percent_off=spec.percent_off,
                free_months=spec.free_months,
                expires_at=spec.expires_at,
                max_uses=spec.max_uses,
                note=spec.note,
            )
        )
        print(f"  + промо код: {spec.code}")


async def reset(db: AsyncSession) -> None:
    """Бүх агуулга болон хэрэглэгчийг устгана. Схемд хүрэхгүй."""
    await db.execute(text(f"TRUNCATE {', '.join(TABLES_IN_DELETE_ORDER)} RESTART IDENTITY CASCADE"))
    await db.commit()
    print("  ! өмнөх өгөгдөл устгагдлаа")


async def seed(*, reset_first: bool = False) -> None:
    _use_utf8_output()
    # Production дээр: нийтэд мэдэгдэх нууц үгтэй админ үүсгэхгүй, жишээ
    # сурагчдыг (ялангуяа Standard багцтайг) огт үүсгэхгүй.
    production = settings.is_production
    if production and ADMIN_PASSWORD == DEFAULT_ADMIN_PASSWORD:
        raise SystemExit("Production дээр SEED_ADMIN_PASSWORD-ийг заавал тохируулна.")

    print("Жишээ өгөгдөл үүсгэж байна…")
    async with SessionFactory() as db:
        if reset_first:
            await reset(db)
        await _ensure_user(db, ADMIN_EMAIL, "Админ", ADMIN_PASSWORD, UserRole.ADMIN)
        if production:
            print("  - жишээ сурагчид production дээр үүсгэгдэхгүй")
        else:
            await _ensure_user(db, STUDENT_EMAIL, "Сурагч", STUDENT_PASSWORD, UserRole.STUDENT)
            await _ensure_user(
                db,
                STANDARD_EMAIL,
                "Standard сурагч",
                STANDARD_PASSWORD,
                UserRole.STUDENT,
                plan=True,
            )
        for spec in COURSES:
            await _sync_course(db, spec)
        await _sync_official_posts(db, OFFICIAL_POSTS)
        await _ensure_promo_codes(db, SEED_PROMO_CODES)
        await db.commit()
    await engine.dispose()
    print("Дууслаа.")
    if production:
        print(f"  Админ: {ADMIN_EMAIL}")
        return
    print(f"  Админ:  {ADMIN_EMAIL} / {ADMIN_PASSWORD}")
    print(f"  Сурагч: {STUDENT_EMAIL} / {STUDENT_PASSWORD}")
    print(f"  Standard: {STANDARD_EMAIL} / {STANDARD_PASSWORD}")


if __name__ == "__main__":
    asyncio.run(seed(reset_first="--reset" in sys.argv))
