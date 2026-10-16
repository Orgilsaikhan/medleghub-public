"""Тестийн өгөгдөл үүсгэх туслах функцүүд."""

import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.course import Course
from app.models.enums import Category, Difficulty, LessonLanguage
from app.models.lesson import Lesson
from app.models.module import Module


async def make_course(
    db: AsyncSession,
    *,
    slug: str = "test-surgalt",
    title: str = "Тест сургалт",
    published: bool = True,
    is_free: bool = True,
    free_lessons: int = 0,
    category: str = Category.JAVASCRIPT,
    difficulty: str = Difficulty.BEGINNER,
    description: str = "Тайлбар",
) -> Course:
    course = Course(
        title=title,
        slug=slug,
        description=description,
        difficulty=difficulty,
        category=category,
        is_free=is_free,
        free_lessons=free_lessons,
        published=published,
    )
    db.add(course)
    await db.commit()
    await db.refresh(course)
    return course


async def make_module(
    db: AsyncSession, course_id: uuid.UUID, *, title: str = "Модул", position: int = 0
) -> Module:
    module = Module(course_id=course_id, title=title, description="", position=position)
    db.add(module)
    await db.commit()
    await db.refresh(module)
    return module


async def make_lesson(
    db: AsyncSession,
    module_id: uuid.UUID,
    *,
    slug: str = "hicheel-1",
    title: str = "Хичээл",
    position: int = 0,
    published: bool = True,
    duration: int = 120,
) -> Lesson:
    lesson = Lesson(
        module_id=module_id,
        title=title,
        slug=slug,
        description="",
        duration=duration,
        content="## Агуулга",
        initial_code="console.log('sain uu');",
        language=LessonLanguage.JAVASCRIPT,
        position=position,
        published=published,
    )
    db.add(lesson)
    await db.commit()
    await db.refresh(lesson)
    return lesson


async def make_course_with_lessons(
    db: AsyncSession,
    *,
    slug: str = "js-undes",
    lesson_count: int = 3,
    is_free: bool = True,
    free_lessons: int = 0,
) -> tuple[Course, list[Lesson]]:
    course = await make_course(db, slug=slug, is_free=is_free, free_lessons=free_lessons)
    module = await make_module(db, course.id)
    lessons = [
        await make_lesson(
            db, module.id, slug=f"hicheel-{index + 1}", title=f"Хичээл {index + 1}", position=index
        )
        for index in range(lesson_count)
    ]
    return course, lessons
