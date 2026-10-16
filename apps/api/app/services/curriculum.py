"""Curriculum (module → lesson) мод байгуулах дундын логик.

Course detail, lesson player, админ дэлгэц гурав ижил дүрмээр эрэмбэлж,
нийтлэгдээгүй хичээлийг ижил байдлаар шүүхийн тулд нэг газар байрлана.
"""

import uuid

from app.models.course import Course
from app.models.lesson import Lesson
from app.models.module import Module
from app.schemas.lesson import LessonSummary
from app.schemas.module import ModuleWithLessons


def sorted_modules(course: Course) -> list[Module]:
    return sorted(course.modules, key=lambda module: (module.position, module.title))


def visible_lessons(module: Module, *, include_unpublished: bool) -> list[Lesson]:
    lessons = sorted(module.lessons, key=lambda lesson: (lesson.position, lesson.title))
    if include_unpublished:
        return lessons
    return [lesson for lesson in lessons if lesson.published]


def flatten_lessons(course: Course, *, include_unpublished: bool) -> list[Lesson]:
    """Курсын бүх хичээлийг дараалалд нь жагсаана (өмнөх/дараагийн холбоосод)."""
    return [
        lesson
        for module in sorted_modules(course)
        for lesson in visible_lessons(module, include_unpublished=include_unpublished)
    ]


def build_curriculum(
    course: Course,
    completed_ids: set[uuid.UUID],
    *,
    include_unpublished: bool,
    locked_ids: set[uuid.UUID] | None = None,
) -> list[ModuleWithLessons]:
    locked_ids = locked_ids or set()
    modules: list[ModuleWithLessons] = []
    for module in sorted_modules(course):
        lessons = visible_lessons(module, include_unpublished=include_unpublished)
        # Оюутанд хоосон модул харуулахгүй; админд бүтэц бүрэн харагдана.
        if not lessons and not include_unpublished:
            continue
        modules.append(
            ModuleWithLessons(
                id=module.id,
                title=module.title,
                description=module.description,
                position=module.position,
                lessons=[
                    LessonSummary(
                        id=lesson.id,
                        title=lesson.title,
                        slug=lesson.slug,
                        duration=lesson.duration,
                        position=lesson.position,
                        published=lesson.published,
                        completed=lesson.id in completed_ids,
                        locked=lesson.id in locked_ids,
                    )
                    for lesson in lessons
                ],
            )
        )
    return modules
