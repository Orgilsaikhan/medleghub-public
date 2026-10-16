"""Тэмдэг олгох логик.

Тэмдгийн тодорхойлолт нь `app/content/badges.py`-д, энд нөхцөл бүрийг
хэрэглэгчийн ахицаас тооцно. Олгосон тэмдэг `user_badges`-д хадгалагдаж
хэзээ ч хасагдахгүй.

`sync_badges` нь хичээл дуусгах бүрд болон профайл нээхэд дуудагдана —
профайлын дуудлага нь энэ системээс өмнө дуусгасан ахицыг ч гүйцээж олгоно.
Бүх тооцоо нь хэрэглэгч тутамд цөөн хэдэн query — хэрэглэгч бүрийн өгөгдөл жижиг.
Тэмдэг бүрийн ховор байдал (хэдэн хувь нь авсан) нь бүх хэрэглэгчийн дээр
тэмдгийн тооноос үл хамааран хоёр aggregate query.

Эзэн авсан тэмдгүүдээсээ 5 хүртэлхийг профайлын нэрийн хажууд онцолно
(`set_showcase`, `user_badges.showcase_position`).
"""

import uuid
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import date, datetime

from sqlalchemy import and_, case, func, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.content.badges import (
    ADVANCED_PROJECT_LESSONS,
    BADGES,
    BADGES_BY_KEY,
    EARLY_ADOPTER_DEADLINE,
    LOCAL_TZ,
    MORNING_HOURS,
    NIGHT_HOURS,
    PROGRAMMING_CATEGORIES,
    SECRET_DESCRIPTION,
    STREAK_DAYS,
    BadgeSpec,
)
from app.core.errors import BadRequestError
from app.models.badge import UserBadge
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.models.enums import UserRole
from app.models.lesson import Lesson
from app.models.module import Module
from app.models.progress import LessonProgress
from app.models.user import User
from app.schemas.auth import UserResponse
from app.schemas.badge import (
    BadgeProgress,
    BadgeStatus,
    BadgeUnlocked,
    ProfileResponse,
    ProfileStats,
)

# --- Хэрэглэгчийн ахицын баримт ------------------------------------------------

# SQL-ийн мөрдөгчийн хэрэг — хариултаар шалгагддаг дасгал (`case_service`).
IS_CASE = Lesson.exercise["kind"].astext == "answer"


@dataclass(frozen=True, slots=True)
class CompletedLesson:
    slug: str
    completed_at: datetime | None
    has_exercise: bool
    course_id: uuid.UUID
    is_case: bool = False


@dataclass(slots=True)
class Facts:
    created_at: datetime
    completed: list[CompletedLesson] = field(default_factory=list)
    # Сургалт бүрийн модулиуд байрлалын дарааллаар — бүрэн дууссан эсэх.
    modules_done: dict[uuid.UUID, list[bool]] = field(default_factory=dict)
    category: dict[uuid.UUID, str] = field(default_factory=dict)
    enrolled: set[uuid.UUID] = field(default_factory=set)
    # Нийтлэгдсэн хичээлтэй нийтлэгдсэн сургалтын тоо («Hidden Gem»).
    course_total: int = 0
    # Нийтлэгдсэн мөрдөгчийн хэргийн тоо («Where the Answers Hide»).
    case_total: int = 0

    @property
    def lesson_count(self) -> int:
        return len(self.completed)

    @property
    def exercise_count(self) -> int:
        return sum(1 for lesson in self.completed if lesson.has_exercise)

    @property
    def case_count(self) -> int:
        return sum(1 for lesson in self.completed if lesson.is_case)

    @property
    def completed_courses(self) -> list[uuid.UUID]:
        return [course for course, done in self.modules_done.items() if done and all(done)]

    def local_hours(self) -> list[int]:
        return [
            lesson.completed_at.astimezone(LOCAL_TZ).hour
            for lesson in self.completed
            if lesson.completed_at is not None
        ]

    def local_days(self) -> list[date]:
        return sorted(
            {
                lesson.completed_at.astimezone(LOCAL_TZ).date()
                for lesson in self.completed
                if lesson.completed_at is not None
            }
        )


async def collect_facts(db: AsyncSession, user: User) -> Facts:
    """Нийтлэгдсэн хичээлийн ахицыг л тооцно — сурагчид харагдахгүй хичээл
    тэмдэг өгөх ёсгүй."""
    facts = Facts(created_at=user.created_at)

    enrolled = await db.execute(
        select(Enrollment.course_id)
        .join(Course, Course.id == Enrollment.course_id)
        .where(Enrollment.user_id == user.id, Course.published.is_(True))
    )
    facts.enrolled = set(enrolled.scalars().all())

    rows = await db.execute(
        select(
            Lesson.id,
            Lesson.slug,
            LessonProgress.completed_at,
            Lesson.exercise.is_not(None),
            IS_CASE,
            Module.course_id,
            Course.category,
        )
        .join(Lesson, Lesson.id == LessonProgress.lesson_id)
        .join(Module, Module.id == Lesson.module_id)
        .join(Course, Course.id == Module.course_id)
        .where(
            LessonProgress.user_id == user.id,
            LessonProgress.completed.is_(True),
            Lesson.published.is_(True),
            Course.published.is_(True),
        )
    )
    done_ids: set[uuid.UUID] = set()
    for lesson_id, slug, completed_at, has_exercise, is_case, course_id, category in rows.all():
        done_ids.add(lesson_id)
        facts.completed.append(
            CompletedLesson(slug, completed_at, bool(has_exercise), course_id, bool(is_case))
        )
        facts.category[course_id] = category

    # Ахицгүй хэрэглэгчид ч хэргийн явц «0 / N» харагдана.
    facts.course_total, facts.case_total = (
        await db.execute(
            select(
                func.count(func.distinct(Module.course_id)),
                func.count(Lesson.id).filter(IS_CASE),
            )
            .select_from(Module)
            .join(Lesson, Lesson.module_id == Module.id)
            .join(Course, Course.id == Module.course_id)
            .where(Lesson.published.is_(True), Course.published.is_(True))
        )
    ).one()

    if not facts.category:
        return facts

    # Модуль бүрэн дууссан эсэхийг мэдэхийн тулд хамаарах сургалтуудын бүтэц.
    structure = await db.execute(
        select(Module.course_id, Module.id, Lesson.id)
        .join(Lesson, Lesson.module_id == Module.id)
        .where(Module.course_id.in_(facts.category), Lesson.published.is_(True))
        .order_by(Module.course_id, Module.position, Module.id)
    )
    modules: dict[uuid.UUID, dict[uuid.UUID, list[uuid.UUID]]] = {}
    for course_id, module_id, lesson_id in structure.all():
        modules.setdefault(course_id, {}).setdefault(module_id, []).append(lesson_id)
    for course_id, by_module in modules.items():
        facts.modules_done[course_id] = [
            all(lesson_id in done_ids for lesson_id in lessons) for lessons in by_module.values()
        ]
    return facts


# --- Нөхцөлүүд ------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Evaluation:
    earned: bool
    progress: BadgeProgress | None = None


def _count(current: int, target: int) -> Evaluation:
    return Evaluation(current >= target, BadgeProgress(current=min(current, target), target=target))


def _longest_module_streak(facts: Facts) -> int:
    best = 0
    for done in facts.modules_done.values():
        run = 0
        for finished in done:
            run = run + 1 if finished else 0
            best = max(best, run)
    return best


def _longest_day_streak(facts: Facts) -> int:
    """Хичээл дуусгасан хамгийн урт дараалсан өдрүүд (Улаанбаатарын цагаар)."""
    best = run = 0
    previous: date | None = None
    for day in facts.local_days():
        run = run + 1 if previous is not None and (day - previous).days == 1 else 1
        best = max(best, run)
        previous = day
    return best


def _perfectionist(facts: Facts) -> Evaluation:
    """Бүртгүүлсэн бүх сургалт дууссан — дор хаяж 2. Зорилго нь бүртгэлийн тоо."""
    finished = len(facts.enrolled & set(facts.completed_courses))
    target = max(2, len(facts.enrolled))
    return Evaluation(
        len(facts.enrolled) >= 2 and finished == len(facts.enrolled),
        BadgeProgress(current=min(finished, target), target=target),
    )


def _all_cases(facts: Facts) -> Evaluation:
    """Нийтлэгдсэн бүх мөрдөгчийн хэрэг шийдэгдсэн. Хэрэг нэмэгдвэл зорилго ч өснө;
    нэг ч хэрэггүй үед олгохгүй."""
    if facts.case_total == 0:
        return Evaluation(False)
    return _count(facts.case_count, facts.case_total)


def _languages_with_module(facts: Facts) -> int:
    return len(
        {
            facts.category[course]
            for course, done in facts.modules_done.items()
            if facts.category[course] in PROGRAMMING_CATEGORIES and any(done)
        }
    )


RULES: dict[str, Callable[[Facts], Evaluation]] = {
    # Нэг алхамтай тэмдэгт «0 / 1» явц утгагүй — зөвхөн авсан эсэх.
    "first-commit": lambda facts: Evaluation(facts.lesson_count >= 1),
    "hello-world": lambda facts: Evaluation(
        any(done and done[0] for done in facts.modules_done.values())
    ),
    "unstoppable": lambda facts: _count(_longest_module_streak(facts), 3),
    "code-smith": lambda facts: _count(facts.exercise_count, 10),
    "mastery": lambda facts: _count(len(facts.completed_courses), 3),
    "persistent": lambda facts: _count(_longest_day_streak(facts), STREAK_DAYS),
    "perfectionist": _perfectionist,
    "century": lambda facts: _count(facts.lesson_count, 100),
    "hidden-gem": lambda facts: Evaluation(
        facts.course_total > 0
        and len({lesson.course_id for lesson in facts.completed}) >= facts.course_total
    ),
    "compiler": lambda facts: Evaluation(
        any(facts.category[course] in PROGRAMMING_CATEGORIES for course in facts.completed_courses)
    ),
    "polyglot": lambda facts: _count(_languages_with_module(facts), 3),
    "night-owl": lambda facts: _count(
        sum(1 for hour in facts.local_hours() if hour in NIGHT_HOURS), 10
    ),
    "early-bird": lambda facts: _count(
        sum(1 for hour in facts.local_hours() if hour in MORNING_HOURS), 10
    ),
    "code-warrior": lambda facts: _count(facts.exercise_count, 100),
    "knowledge-seeker": lambda facts: _count(facts.lesson_count, 50),
    "architect": lambda facts: Evaluation(
        any(lesson.slug in ADVANCED_PROJECT_LESSONS for lesson in facts.completed)
    ),
    "ahead-of-time": lambda facts: Evaluation(facts.created_at < EARLY_ADOPTER_DEADLINE),
    "where-the-answers-hide": _all_cases,
    # Ахицаар хэзээ ч олгогдохгүй — зөвхөн `claim_event_badge`.
    "through-anothers-path": lambda facts: Evaluation(False),
}


def evaluate(badge: BadgeSpec, facts: Facts) -> Evaluation | None:
    """`None` — энэ тэмдгийг одоогоор тооцох боломжгүй («Тун удахгүй»)."""
    rule = RULES.get(badge.key)
    if not badge.tracked or rule is None:
        return None
    return rule(facts)


# --- Олгох ба профайл -----------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Awarded:
    """Хэрэглэгчийн авсан нэг тэмдэг."""

    awarded_at: datetime
    # Профайлын нэрийн хажууд онцолсон байр (1, 2, …), онцлоогүй бол `None`.
    showcase_position: int | None


async def _awarded(db: AsyncSession, user_id: uuid.UUID) -> dict[str, Awarded]:
    rows = await db.execute(
        select(UserBadge.badge_key, UserBadge.awarded_at, UserBadge.showcase_position).where(
            UserBadge.user_id == user_id
        )
    )
    return {key: Awarded(awarded_at, position) for key, awarded_at, position in rows.tuples()}


# Ховор байдлыг зөвхөн имэйлээ баталгаажуулсан суралцагчдаас тооцно — админ,
# баталгаажаагүй бүртгэл авсан хүний тоонд ч, нийт хэрэглэгчийн тоонд ч орохгүй.
# Профайлаа нуусан хүн ч орохгүй: Нууцлалын бодлого (§4.1) нуусан хэрэглэгчийг
# зөвхөн сургалтын нийт суралцагчийн тоонд тооцно гэж амласан.
COUNTS_FOR_RARITY = and_(
    User.role == UserRole.STUDENT,
    User.email_verified_at.is_not(None),
    User.profile_hidden.is_(False),
)


async def _earned_percents(db: AsyncSession) -> dict[str, float] | None:
    """Тэмдэг бүрийг авсан хэрэглэгчдийн хувь (0–100, 2 орны нарийвчлалтай).

    Хэн ч аваагүй тэмдэг толь бичигт орохгүй — дуудагч `0.0` гэж үзнэ. Нэг хүн
    ч авсан бол хамгийн багадаа `0.01` — маш олон хэрэглэгчтэй үед авсан хүн
    өөрийн тэмдэг дээр «0%» харахгүй. Тооцох хэрэглэгч огт байхгүй бол `None`.
    Тэмдгийн тооноос үл хамааран хоёр query: нийт хэрэглэгчийн тоо ба түлхүүр
    тутмын GROUP BY.
    """
    total = (await db.execute(select(func.count(User.id)).where(COUNTS_FOR_RARITY))).scalar_one()
    if total == 0:
        return None
    rows = await db.execute(
        select(UserBadge.badge_key, func.count(UserBadge.id))
        .join(User, User.id == UserBadge.user_id)
        .where(COUNTS_FOR_RARITY)
        .group_by(UserBadge.badge_key)
    )
    return {key: max(round(holders * 100 / total, 2), 0.01) for key, holders in rows.tuples()}


async def _award(db: AsyncSession, user: User, facts: Facts) -> list[BadgeSpec]:
    """Шинээр хангасан тэмдгүүдийг бичиж, тэдгээрийг буцаана."""
    awarded = await _awarded(db, user.id)
    earned = []
    for badge in BADGES:
        if badge.key in awarded:
            continue
        evaluation = evaluate(badge, facts)
        if evaluation is not None and evaluation.earned:
            earned.append(badge)
    if not earned:
        return []

    # Зэрэг ирсэн хоёр хүсэлт нэг тэмдгийг давхар олгохгүй — зөвхөн
    # ҮНЭХЭЭР шинээр бичигдсэнийг буцаана.
    inserted = await db.execute(
        insert(UserBadge)
        .values([{"user_id": user.id, "badge_key": badge.key} for badge in earned])
        .on_conflict_do_nothing(constraint="uq_user_badges_user_badge")
        .returning(UserBadge.badge_key)
    )
    new_keys = set(inserted.scalars().all())
    await db.commit()
    return [badge for badge in earned if badge.key in new_keys]


async def sync_badges(db: AsyncSession, user: User) -> list[BadgeUnlocked]:
    """Хэрэглэгчийн ахицыг шалгаж, шинээр хангасан тэмдгүүдийг олгоно."""
    facts = await collect_facts(db, user)
    return [
        BadgeUnlocked(
            key=badge.key,
            name=badge.name,
            description=badge.description,
            shape=badge.shape,
            secret=badge.secret,
            rare=badge.rare,
            prismatic=badge.prismatic,
        )
        for badge in await _award(db, user, facts)
    ]


async def claim_event_badge(db: AsyncSession, user: User, key: str) -> BadgeStatus | None:
    """Үйлдлээр олгогдох тэмдэг (`EVENT_BADGES`). Аль хэдийн авсан бол `None`.

    Бүтэн төлөвийг (тайлбар, солонгон эсэх) буцаана — UI нээгдсэн тэмдгийг
    дүрс, тайлбартай нь томоор харуулна.
    """
    badge = next(badge for badge in BADGES if badge.key == key)
    inserted = await db.execute(
        insert(UserBadge)
        .values(user_id=user.id, badge_key=badge.key)
        .on_conflict_do_nothing(constraint="uq_user_badges_user_badge")
        .returning(UserBadge.awarded_at)
    )
    awarded_at = inserted.scalar_one_or_none()
    await db.commit()
    if awarded_at is None:
        return None
    return BadgeStatus(
        key=badge.key,
        name=badge.name,
        description=badge.description,
        shape=badge.shape,
        available=True,
        earned=True,
        secret=badge.secret,
        rare=badge.rare,
        prismatic=badge.prismatic,
        awarded_at=awarded_at,
    )


async def set_showcase(db: AsyncSession, user: User, keys: list[str]) -> list[str]:
    """Эзний онцлох амжилтуудыг `keys`-ийн дарааллаар (1, 2, …) бүхэлд нь сольж
    бичнэ. Хоосон жагсаалт онцлохыг цуцална. Хадгалсан дарааллыг буцаана.

    Түлхүүр бүр каталогт байгаа, хэрэглэгчийн авсан тэмдэг байх ёстой — эс
    бөгөөс юу ч өөрчлөхгүй 400. Тоо, давхардлыг `BadgeShowcaseUpdate` шалгасан.
    """
    # Хэрэглэгчийн мөрийг түгжинэ: зэрэг ирсэн хоёр хүсэлт ээлжилж ажиллана —
    # нэг байрыг хоёр тэмдэгт оноож unique-ийн алдаа (500) гаргахгүй. `FOR NO
    # KEY UPDATE` нь тэр хэрэглэгч рүү FK-тэй мөр нэмэхийг (хичээл дуусгах,
    # тэмдэг олгох) хүлээлгэхгүй.
    await db.execute(select(User.id).where(User.id == user.id).with_for_update(key_share=True))
    awarded = await _awarded(db, user.id)
    if any(key not in BADGES_BY_KEY or key not in awarded for key in keys):
        await db.rollback()
        raise BadRequestError(
            "SHOWCASE_BADGE_NOT_EARNED", "Зөвхөн авсан амжилтаа онцлох боломжтой."
        )

    # Эхлээд бүх байрыг чөлөөлнө. Postgres unique-ийг мөр бүрт шууд шалгадаг тул
    # нэг UPDATE-ээр байр солих (1 ↔ 2) нь түр зуур давхцаж унана.
    await db.execute(
        update(UserBadge)
        .where(UserBadge.user_id == user.id, UserBadge.showcase_position.is_not(None))
        .values(showcase_position=None)
    )
    if keys:
        positions = {key: position for position, key in enumerate(keys, start=1)}
        await db.execute(
            update(UserBadge)
            .where(UserBadge.user_id == user.id, UserBadge.badge_key.in_(keys))
            .values(showcase_position=case(positions, value=UserBadge.badge_key))
        )
    await db.commit()
    return keys


async def summary(
    db: AsyncSession, user: User, *, award: bool
) -> tuple[ProfileStats, list[BadgeStatus]]:
    """Профайлын статистик ба тэмдгүүд — тэмдэг бүр ховор байдал (хэдэн хувь нь
    авсан), эзний онцолсон байртайгаа.

    `award` — хангасан ч хараахан олгоогүй тэмдгийг олгох эсэх. Зөвхөн өөрийн
    профайлд: бусдын профайлыг үзэх нь тэр хэрэглэгчийн өгөгдлийг өөрчлөхгүй.
    """
    facts = await collect_facts(db, user)
    if award:
        await _award(db, user, facts)
    awarded = await _awarded(db, user.id)
    percents = await _earned_percents(db)

    badges: list[BadgeStatus] = []
    for badge in BADGES:
        owned = awarded.get(badge.key)
        earned = owned is not None
        # Бүрэн нууц тэмдэг авах хүртэл жагсаалтад ч, нийт тоонд ч орохгүй.
        if badge.invisible and not earned:
            continue
        evaluation = evaluate(badge, facts)
        # Нууц амжилтын нөхцөл, явц нь авах хүртэл харагдахгүй.
        hidden = badge.secret and not earned
        badges.append(
            BadgeStatus(
                key=badge.key,
                name=badge.name,
                description=SECRET_DESCRIPTION if hidden else badge.description,
                shape=badge.shape,
                available=evaluation is not None,
                earned=earned,
                secret=badge.secret,
                rare=badge.rare,
                prismatic=badge.prismatic,
                awarded_at=owned.awarded_at if owned else None,
                progress=None if earned or hidden or evaluation is None else evaluation.progress,
                # «Тун удахгүй» тэмдгийг хэн ч авах боломжгүй — хувь нь утгагүй.
                earned_percent=(
                    None if percents is None or evaluation is None else percents.get(badge.key, 0.0)
                ),
                showcase_position=owned.showcase_position if owned else None,
            )
        )

    enrolled = (
        await db.execute(select(func.count(Enrollment.id)).where(Enrollment.user_id == user.id))
    ).scalar_one()

    stats = ProfileStats(
        completed_lessons=facts.lesson_count,
        completed_exercises=facts.exercise_count,
        completed_courses=len(facts.completed_courses),
        enrolled_courses=enrolled,
        earned_badges=sum(1 for badge in badges if badge.earned),
        total_badges=len(badges),
    )
    return stats, badges


async def profile(db: AsyncSession, user: User) -> ProfileResponse:
    stats, badges = await summary(db, user, award=True)
    return ProfileResponse(user=UserResponse.model_validate(user), stats=stats, badges=badges)
