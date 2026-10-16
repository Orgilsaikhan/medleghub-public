"""Мөрдөгчийн хэрэг (SQL): сурагчийн бичсэн хариултыг шалгах.

Сурагч асуулгаа ажиллуулж олсон хариултаа («Анужин», «УБА-4512», «37»)
бичнэ. Зөв хариулт хөтөч рүү ХЭЗЭЭ Ч очихгүй — зөвхөн энд харьцуулна.

Харьцуулалт нь бичлэгийн жижиг ялгааг үл тооно: том жижиг үсэг, илүү зай,
хашилт, цэг таслал, «₮». Бусад ялгаа (өөр нэр, өөр тоо) буруу. Зөвшөөрөгдөх
өөр хэлбэрийг (овогтой нэр г.м.) хичээлийн `answers`-д жагсаана.
"""

import re
import unicodedata
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import rate_limit
from app.core.config import settings
from app.core.errors import NotFoundError, RateLimitError
from app.models.lesson import Lesson
from app.models.module import Module
from app.models.user import User
from app.services.access import assert_lesson_unlocked
from app.services.progress_service import is_enrolled

_PUNCTUATION = re.compile(r"[\"'«»“”„`´.,!?;:()\[\]{}₮]")
_SPACES = re.compile(r"\s+")


def normalize_answer(text: str) -> str:
    text = unicodedata.normalize("NFKC", text).casefold().replace("ё", "е")
    text = _PUNCTUATION.sub(" ", text)
    return _SPACES.sub(" ", text).strip()


def is_correct(answer: str, accepted: list[str]) -> bool:
    given = normalize_answer(answer)
    return bool(given) and any(given == normalize_answer(item) for item in accepted)


def _not_a_case() -> NotFoundError:
    return NotFoundError("CASE_NOT_FOUND", "Энэ хичээлд шийдэх хэрэг байхгүй.")


async def check_answer(
    db: AsyncSession, lesson: Lesson, user: User, answer: str
) -> tuple[bool, uuid.UUID | None]:
    """Хариулт зөв эсэх, зөв ба бүртгүүлсэн бол хичээлийг дуусгах course-ийн ID.

    Бүртгүүлээгүй сурагч ч хэргээ шийдэж болно — ахиц нь л хадгалагдахгүй.
    Нийтлэгдээгүй эсвэл төлбөрт (багцгүй) хичээлд `/complete`-тэй ижил хариу.
    """
    exercise = lesson.exercise or {}
    accepted = exercise.get("answers") or []
    if exercise.get("kind") != "answer" or not accepted:
        raise _not_a_case()
    if not lesson.published and not user.is_admin:
        raise _not_a_case()
    await assert_lesson_unlocked(db, lesson, user)

    # Хэдэн нэр таамаглаж үзэх боломжтойг хязгаарлана — хэрэг бүрт тусдаа.
    if settings.rate_limit_enabled:
        allowed, retry_after = rate_limit.backend.hit(
            f"case:{user.id}:{lesson.id}",
            settings.case_answer_rate_limit_max,
            settings.case_answer_rate_limit_window_seconds,
        )
        if not allowed:
            raise RateLimitError(retry_after)

    if not is_correct(answer, accepted):
        return False, None
    course_id = (
        await db.execute(select(Module.course_id).where(Module.id == lesson.module_id))
    ).scalar_one()
    enrolled = user.is_admin or await is_enrolled(db, user.id, course_id)
    return True, course_id if enrolled else None
