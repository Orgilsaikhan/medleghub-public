"""Seed нь агуулгыг `app/content`-той тэнцүү болгодог эсэх.

Хамгийн чухал шинж нь: хичээлийг `slug`-аар нь тааруулдаг учраас дахин
seed хийхэд суралцагчийн ахиц алдагдахгүй.
"""

import pytest
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app import seed as seed_module
from app.content.types import CourseSpec, ExerciseSpec, LessonSpec, ModuleSpec, TestCaseSpec
from app.core.config import settings
from app.models.course import Course
from app.models.enums import Category, Difficulty
from app.models.lesson import Lesson
from app.models.module import Module
from app.models.progress import LessonProgress
from app.seed import _sync_course
from tests.conftest import make_user

SLUG = "test-surgalt"


def _lesson(slug: str, *, title: str | None = None, content: str = "Агуулга") -> LessonSpec:
    return LessonSpec(
        title=title or slug,
        slug=slug,
        description="Тайлбар",
        content=content,
        initial_code="console.log(1);",
        duration=60,
    )


def _course(*modules: tuple[str, list[str]], title: str = "Тест сургалт") -> CourseSpec:
    return CourseSpec(
        title=title,
        slug=SLUG,
        description="Сургалтын тайлбар",
        difficulty=Difficulty.BEGINNER,
        category=Category.JAVASCRIPT,
        modules=[
            ModuleSpec(
                title=modul,
                description="Модулын тайлбар",
                lessons=[_lesson(s) for s in slugs],
            )
            for modul, slugs in modules
        ],
    )


async def _read(db: AsyncSession) -> dict[str, list[str]]:
    """Сургалтыг {модулын гарчиг: [хичээлийн slug]} хэлбэрээр буцаана."""
    modules = (
        (
            await db.execute(
                select(Module).join(Course).where(Course.slug == SLUG).order_by(Module.position)
            )
        )
        .scalars()
        .all()
    )

    ur: dict[str, list[str]] = {}
    for modul in modules:
        lessons = (
            (
                await db.execute(
                    select(Lesson).where(Lesson.module_id == modul.id).order_by(Lesson.position)
                )
            )
            .scalars()
            .all()
        )
        ur[modul.title] = [lesson.slug for lesson in lessons]
    return ur


async def _lesson_id(db: AsyncSession, slug: str):
    return (
        await db.execute(
            select(Lesson.id)
            .join(Module)
            .join(Course)
            .where(Course.slug == SLUG, Lesson.slug == slug)
        )
    ).scalar_one()


async def test_creates_course_when_missing(db: AsyncSession) -> None:
    await _sync_course(db, _course(("Модул 1", ["a", "b"])))
    await db.commit()

    assert await _read(db) == {"Модул 1": ["a", "b"]}


async def test_adds_new_lessons_on_rerun(db: AsyncSession) -> None:
    await _sync_course(db, _course(("Модул 1", ["a"])))
    await db.commit()

    await _sync_course(db, _course(("Модул 1", ["a", "b"]), ("Модул 2", ["c"])))
    await db.commit()

    assert await _read(db) == {"Модул 1": ["a", "b"], "Модул 2": ["c"]}


async def test_existing_lesson_keeps_its_id_and_progress(db: AsyncSession) -> None:
    """Хамгийн чухал шалгалт — дахин seed хийхэд ахиц устахгүй."""
    await _sync_course(db, _course(("Модул 1", ["a"])))
    await db.commit()

    hicheel_id = await _lesson_id(db, "a")
    user = await make_user(db, "suragch@test.mn")
    db.add(LessonProgress(user_id=user.id, lesson_id=hicheel_id, completed=True))
    await db.commit()

    await _sync_course(db, _course(("Модул 1", ["a", "b"])))
    await db.commit()

    assert await _lesson_id(db, "a") == hicheel_id
    uldsen = (await db.execute(select(func.count()).select_from(LessonProgress))).scalar_one()
    assert uldsen == 1, "Ахицын бичлэг устсан"


async def test_content_changes_are_written(db: AsyncSession) -> None:
    await _sync_course(db, _course(("Модул 1", ["a"])))
    await db.commit()

    shine = CourseSpec(
        title="Шинэ гарчиг",
        slug=SLUG,
        description="Шинэ тайлбар",
        difficulty=Difficulty.BEGINNER,
        category=Category.JAVASCRIPT,
        modules=[
            ModuleSpec(
                title="Модул 1",
                description="Модулын тайлбар",
                lessons=[_lesson("a", title="Шинэчилсэн", content="Шинэ агуулга")],
            )
        ],
    )
    await _sync_course(db, shine)
    await db.commit()

    course = (await db.execute(select(Course).where(Course.slug == SLUG))).scalar_one()
    assert course.title == "Шинэ гарчиг"
    assert course.description == "Шинэ тайлбар"

    lesson = (
        await db.execute(select(Lesson).join(Module).where(Module.course_id == course.id))
    ).scalar_one()
    assert lesson.title == "Шинэчилсэн"
    assert lesson.content == "Шинэ агуулга"


async def test_exercise_is_written_with_its_help(db: AsyncSession) -> None:
    exercise = ExerciseSpec(
        statement="Хоёр тоог нэм.",
        tests=(
            TestCaseSpec(stdin="1 2\n", expected_output="3\n", sample=True),
            TestCaseSpec(stdin="-5 5\n", expected_output="0\n"),
        ),
        solution="int main(void) { return 0; } /* ШИЙДЭЛ */",
        tips="- Хоёр тоог уншаад нэм.",
    )
    spec = CourseSpec(
        title="Тест сургалт",
        slug=SLUG,
        description="Сургалтын тайлбар",
        difficulty=Difficulty.BEGINNER,
        category=Category.JAVASCRIPT,
        modules=[
            ModuleSpec(
                title="Модул 1",
                description="Модулын тайлбар",
                lessons=[
                    LessonSpec(
                        title="a",
                        slug="a",
                        description="",
                        content="",
                        initial_code="int main(void) { return 0; }",
                        duration=60,
                        exercise=exercise,
                    )
                ],
            )
        ],
    )
    await _sync_course(db, spec)
    await db.commit()

    lesson = (await db.execute(select(Lesson).where(Lesson.slug == "a"))).scalar_one()
    assert lesson.exercise == {
        "statement": "Хоёр тоог нэм.",
        "tests": [
            {"stdin": "1 2\n", "expected_output": "3\n", "sample": True},
            {"stdin": "-5 5\n", "expected_output": "0\n", "sample": False},
        ],
        "tips": "- Хоёр тоог уншаад нэм.",
        "solution": "int main(void) { return 0; } /* ШИЙДЭЛ */",
    }

    # Spec-ээс дасгалыг хасвал өгөгдлийн сангаас ч арилна.
    await _sync_course(db, _course(("Модул 1", ["a"])))
    await db.commit()
    await db.refresh(lesson)
    assert lesson.exercise is None


async def test_lesson_moved_between_modules_keeps_its_id(db: AsyncSession) -> None:
    await _sync_course(db, _course(("Модул 1", ["a", "b"])))
    await db.commit()
    hicheel_id = await _lesson_id(db, "b")

    await _sync_course(db, _course(("Модул 1", ["a"]), ("Модул 2", ["b"])))
    await db.commit()

    assert await _read(db) == {"Модул 1": ["a"], "Модул 2": ["b"]}
    assert await _lesson_id(db, "b") == hicheel_id


async def test_removed_lessons_and_modules_are_deleted(db: AsyncSession) -> None:
    await _sync_course(db, _course(("Модул 1", ["a", "b"]), ("Модул 2", ["c"])))
    await db.commit()

    await _sync_course(db, _course(("Модул 1", ["a"])))
    await db.commit()

    assert await _read(db) == {"Модул 1": ["a"]}
    niit = (await db.execute(select(func.count()).select_from(Lesson))).scalar_one()
    assert niit == 1


async def test_courses_outside_the_spec_are_untouched(db: AsyncSession) -> None:
    """Админ эсвэл E2E тестийн үүсгэсэн сургалтыг seed устгахгүй."""
    db.add(
        Course(
            title="Гараар үүсгэсэн",
            slug="garaar-uusgesen",
            description="Тайлбар",
            difficulty=Difficulty.BEGINNER,
            category=Category.JAVASCRIPT,
        )
    )
    await db.commit()

    await _sync_course(db, _course(("Модул 1", ["a"])))
    await db.commit()

    uldsen = (
        await db.execute(select(Course.slug).where(Course.slug == "garaar-uusgesen"))
    ).scalar_one_or_none()
    assert uldsen == "garaar-uusgesen"


async def test_production_refuses_the_default_admin_password(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Нийтэд мэдэгдэх `Admin12345`-тай админ production-д хэзээ ч үүсэхгүй."""
    monkeypatch.setattr(settings, "environment", "production")
    monkeypatch.setattr(seed_module, "ADMIN_PASSWORD", seed_module.DEFAULT_ADMIN_PASSWORD)
    with pytest.raises(SystemExit):
        await seed_module.seed()
