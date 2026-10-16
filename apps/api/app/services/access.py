"""Төлбөрт хичээлийн хандалтын дүрэм.

`is_free=False` сургалтын эхний `free_lessons` хичээл бүгдэд нээлттэй. Үлдсэн
хичээлийн агуулга, дасгал, тусламж, «дууслаа» тэмдэглэгээг зөвхөн Standard
багцтай хэрэглэгч (эсвэл админ) авна. Curriculum-ийн ЖАГСААЛТ (гарчиг, үргэлжлэх
хугацаа) хүн бүрт харагдана — юу нээгдэхийг харуулах нь өөрөө урамшуулал.

Дараалал нь сурагчийн харах дараалал: зөвхөн нийтлэгдсэн хичээл, модул ба
хичээлийн байрлалаар (`curriculum.flatten_lessons`). Нийтлэгдээгүй хичээл
тоололд орохгүй тул админ ноорог нэмэхэд үнэгүй хэсэг шилжихгүй.
"""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.errors import PaymentRequiredError
from app.models.course import Course
from app.models.lesson import Lesson
from app.models.module import Module
from app.models.user import User
from app.services.curriculum import flatten_lessons


def locked_lesson_ids(course: Course, user: User | None) -> set[uuid.UUID]:
    """Энэ хэрэглэгчид түгжигдсэн хичээлүүдийн ID. `course.modules` ачаалагдсан байна."""
    if course.is_free or (user is not None and user.has_plan):
        return set()
    ordered = flatten_lessons(course, include_unpublished=False)
    return {lesson.id for lesson in ordered[course.free_lessons :]}


async def assert_lesson_unlocked(db: AsyncSession, lesson: Lesson, user: User) -> None:
    """Түгжигдсэн хичээл бол 402 `PLAN_REQUIRED`."""
    if user.has_plan:
        return
    course = (
        await db.execute(
            select(Course)
            .join(Module, Module.course_id == Course.id)
            .where(Module.id == lesson.module_id)
            .options(selectinload(Course.modules).selectinload(Module.lessons))
        )
    ).scalar_one()
    if lesson.id in locked_lesson_ids(course, user):
        raise PaymentRequiredError()
