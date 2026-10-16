"""Судлах хэрэгсэл: заавар, тест, таамаг захиалах; тест өгөх; карт давтах.

AI-аар үүсгэх зүйл нэг удаа үүсч, дахин дахин ашиглагдана. Хэрэглэгч
«Шинээр үүсгэх» дарвал л AI дахин дуудагдана. Тестийн зөв хариулт зөвхөн
хариулсны дараа (`answer`) буцна — `case_service`-ийн зарчим.
"""

import uuid
from datetime import UTC, datetime
from typing import Any

from fastapi import status
from sqlalchemy import and_, func, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import rate_limit
from app.core.config import settings
from app.live import access
from app.live.errors import live_error, not_found
from app.live.mastery import Rating, review
from app.live.materials import (
    assert_ai_configured,
    generation_brief,
    owned_material,
    topic_views,
)
from app.models.enums import LiveGenerationKind, LiveGenerationStatus, LiveMaterialStatus
from app.models.live import (
    LiveCard,
    LiveCardProgress,
    LiveGeneration,
    LiveMaterial,
    LiveQuestion,
    LiveQuizAnswer,
    LiveQuizAttempt,
    LiveTopic,
    LiveTopicProgress,
)
from app.models.user import User
from app.schemas.live import (
    LiveAnswerCreate,
    LiveAnswerResult,
    LiveAttempt,
    LiveAttemptAnswer,
    LiveAttemptResult,
    LiveExamContent,
    LiveGenerationRequest,
    LiveGuideContent,
    LiveQuizContent,
    LiveQuizQuestion,
    LiveTopicResult,
)
from app.schemas.live import LiveCard as LiveCardView
from app.schemas.live import LiveGeneration as LiveGenerationView
from app.services.ai.capabilities import Capability


def _capability(kind: LiveGenerationKind, topic_id: uuid.UUID | None) -> Capability:
    if kind == LiveGenerationKind.GUIDE:
        return Capability.STUDY_GUIDE
    if kind == LiveGenerationKind.EXAM:
        return Capability.EXAM
    return Capability.TOPIC_QUIZ if topic_id is not None else Capability.FULL_QUIZ


IN_PROGRESS = (LiveGenerationStatus.QUEUED, LiveGenerationStatus.PROCESSING)


def _now() -> datetime:
    return datetime.now(UTC)


async def _owned(db: AsyncSession, user: User, material_id: uuid.UUID) -> LiveMaterial:
    return await owned_material(db, user, material_id)


async def owned_topic(db: AsyncSession, user: User, topic_id: uuid.UUID) -> LiveTopic:
    topic = await db.get(LiveTopic, topic_id)
    if topic is None:
        raise not_found()
    await _owned(db, user, topic.material_id)
    return topic


async def owned_generation(
    db: AsyncSession, user: User, generation_id: uuid.UUID
) -> LiveGeneration:
    generation = await db.get(LiveGeneration, generation_id)
    if generation is None:
        raise not_found()
    await _owned(db, user, generation.material_id)
    return generation


async def owned_attempt(db: AsyncSession, user: User, attempt_id: uuid.UUID) -> LiveQuizAttempt:
    attempt = await db.get(LiveQuizAttempt, attempt_id)
    if attempt is None or attempt.user_id != user.id:
        raise not_found()
    if not (user.is_admin or user.has_plan):
        # Нэг удаагийн эрхээр — зөвхөн эрхээр нээсэн материалын тест.
        await owned_generation(db, user, attempt.generation_id)
    return attempt


async def owned_card(db: AsyncSession, user: User, card_id: uuid.UUID) -> LiveCard:
    card = await db.get(LiveCard, card_id)
    if card is None:
        raise not_found()
    await _owned(db, user, card.material_id)
    return card


# --- Үүсгэлт ---------------------------------------------------------------


def _same_target(kind: str, topic_id: uuid.UUID | None) -> Any:
    target = (
        LiveGeneration.topic_id.is_(None)
        if topic_id is None
        else (LiveGeneration.topic_id == topic_id)
    )
    return and_(LiveGeneration.kind == kind, target)


async def request_generation(
    db: AsyncSession, user: User, material: LiveMaterial, payload: LiveGenerationRequest
) -> LiveGeneration:
    """Бэлэн эсвэл үүсгэж байгаа нь байвал түүнийг буцаана (AI дахин дуудахгүй)."""
    kind = LiveGenerationKind(payload.kind)
    topic_id = payload.topic_id
    if (kind == LiveGenerationKind.GUIDE and topic_id is None) or (
        kind == LiveGenerationKind.EXAM and topic_id is not None
    ):
        raise live_error(status.HTTP_400_BAD_REQUEST, "LIVE_BAD_TOPIC")
    if topic_id is not None:
        topic = await db.get(LiveTopic, topic_id)
        if topic is None or topic.material_id != material.id:
            raise live_error(status.HTTP_400_BAD_REQUEST, "LIVE_BAD_TOPIC")
    if material.status != LiveMaterialStatus.READY:
        raise live_error(status.HTTP_409_CONFLICT, "LIVE_MATERIAL_NOT_READY")

    existing = (
        await db.execute(
            select(LiveGeneration).where(
                LiveGeneration.material_id == material.id, _same_target(kind, topic_id)
            )
        )
    ).scalar_one_or_none()
    # Явж байгаа ажлыг дундаас нь солихгүй. Бэлэн эсвэл бүтэлгүйтснийг зөвхөн
    # хэрэглэгч «Шинээр үүсгэх» / «Дахин оролдох» дарвал (`regenerate`) — хуудас
    # дахин нээх, цонх руу буцах нь AI-г дахин дуудахгүй.
    if existing is not None and (existing.status in IN_PROGRESS or not payload.regenerate):
        return existing

    assert_ai_configured(_capability(kind, topic_id))
    entitlement = await access.entitlement_for(db, user)
    await access.assert_ai_available(db, user, entitlement, material.id)
    rate_limit.enforce(
        f"live:generate:{user.id}",
        settings.live_generation_rate_limit_max,
        settings.live_generation_rate_limit_window_seconds,
    )
    if existing is not None:
        # Асуулт, оролдлого нь дагаж устана. Сэдвийн эзэмшил үлдэнэ.
        await db.delete(existing)
        await db.flush()
    generation = LiveGeneration(
        material_id=material.id,
        topic_id=topic_id,
        kind=kind,
        status=LiveGenerationStatus.QUEUED,
    )
    db.add(generation)
    try:
        await db.commit()
    except IntegrityError:
        # Зэрэг ирсэн хоёр хүсэлт — нөгөөх нь түрүүлж үүсгэсэн.
        await db.rollback()
        return (
            await db.execute(
                select(LiveGeneration).where(
                    LiveGeneration.material_id == material.id, _same_target(kind, topic_id)
                )
            )
        ).scalar_one()
    await db.refresh(generation)
    return generation


async def _questions(db: AsyncSession, generation_id: uuid.UUID) -> list[LiveQuestion]:
    return list(
        (
            await db.execute(
                select(LiveQuestion)
                .where(LiveQuestion.generation_id == generation_id)
                .order_by(LiveQuestion.position)
            )
        )
        .scalars()
        .all()
    )


async def generation_view(db: AsyncSession, generation: LiveGeneration) -> LiveGenerationView:
    brief = generation_brief(generation)
    assert brief is not None
    ready = generation.status == LiveGenerationStatus.READY
    content = generation.content or {}
    guide = quiz = exam = None
    if ready and generation.kind == LiveGenerationKind.GUIDE:
        guide = LiveGuideContent(markdown=content.get("markdown", ""))
    elif ready and generation.kind == LiveGenerationKind.QUIZ:
        quiz = LiveQuizContent(
            questions=[
                LiveQuizQuestion(
                    id=question.id,
                    position=question.position,
                    prompt=question.prompt,
                    options=list(question.options),
                    topic_id=question.topic_id,
                )
                for question in await _questions(db, generation.id)
            ]
        )
    elif ready and generation.kind == LiveGenerationKind.EXAM:
        exam = LiveExamContent.model_validate(content)
    return LiveGenerationView(
        **brief.model_dump(),
        material_id=generation.material_id,
        guide=guide,
        quiz=quiz,
        exam=exam,
    )


# --- Тест ------------------------------------------------------------------


async def _answers(db: AsyncSession, attempt_id: uuid.UUID) -> list[LiveQuizAnswer]:
    return list(
        (await db.execute(select(LiveQuizAnswer).where(LiveQuizAnswer.attempt_id == attempt_id)))
        .scalars()
        .all()
    )


async def attempt_view(db: AsyncSession, attempt: LiveQuizAttempt) -> LiveAttempt:
    return LiveAttempt(
        id=attempt.id,
        generation_id=attempt.generation_id,
        total=attempt.total,
        correct_count=attempt.correct_count,
        answers=[
            LiveAttemptAnswer(
                question_id=answer.question_id,
                choice_index=answer.choice_index,
                correct=answer.is_correct,
            )
            for answer in await _answers(db, attempt.id)
        ],
        finished_at=attempt.finished_at,
    )


async def start_attempt(
    db: AsyncSession, user: User, generation: LiveGeneration
) -> LiveQuizAttempt:
    if (
        generation.kind != LiveGenerationKind.QUIZ
        or generation.status != LiveGenerationStatus.READY
    ):
        raise live_error(status.HTTP_409_CONFLICT, "LIVE_MATERIAL_NOT_READY")
    total = int(
        (
            await db.execute(
                select(func.count()).where(LiveQuestion.generation_id == generation.id)
            )
        ).scalar_one()
    )
    attempt = LiveQuizAttempt(generation_id=generation.id, user_id=user.id, total=total)
    db.add(attempt)
    await db.commit()
    await db.refresh(attempt)
    return attempt


async def answer(
    db: AsyncSession, attempt: LiveQuizAttempt, payload: LiveAnswerCreate
) -> LiveAnswerResult:
    if attempt.finished_at is not None:
        raise live_error(status.HTTP_409_CONFLICT, "LIVE_ATTEMPT_FINISHED")
    question = await db.get(LiveQuestion, payload.question_id)
    if question is None or question.generation_id != attempt.generation_id:
        raise not_found()
    if payload.choice_index >= len(question.options):
        raise live_error(status.HTTP_400_BAD_REQUEST, "LIVE_BAD_CHOICE")
    if await db.get(LiveQuizAnswer, (attempt.id, question.id)) is not None:
        raise live_error(status.HTTP_409_CONFLICT, "LIVE_ALREADY_ANSWERED")
    correct = payload.choice_index == question.correct_index
    db.add(
        LiveQuizAnswer(
            attempt_id=attempt.id,
            question_id=question.id,
            choice_index=payload.choice_index,
            is_correct=correct,
        )
    )
    if correct:
        attempt.correct_count += 1
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise live_error(status.HTTP_409_CONFLICT, "LIVE_ALREADY_ANSWERED") from None
    return LiveAnswerResult(
        question_id=question.id,
        correct=correct,
        correct_index=question.correct_index,
        explanation=question.explanation,
        page=question.page,
    )


async def _touch_topics(
    db: AsyncSession, user_id: uuid.UUID, values_by_topic: dict[uuid.UUID, dict[str, Any]]
) -> None:
    """`live_topic_progress`-ийг upsert хийнэ (`last_studied_at` үргэлж шинэчлэгдэнэ)."""
    now = _now()
    for topic_id, values in values_by_topic.items():
        row = {"user_id": user_id, "topic_id": topic_id, "last_studied_at": now, **values}
        statement = insert(LiveTopicProgress).values(**row)
        await db.execute(
            statement.on_conflict_do_update(
                index_elements=[LiveTopicProgress.user_id, LiveTopicProgress.topic_id],
                set_={key: statement.excluded[key] for key in ("last_studied_at", *values)},
            )
        )


async def finish(db: AsyncSession, user: User, attempt: LiveQuizAttempt) -> LiveAttemptResult:
    """Сэдэв тутмын дүнг `live_topic_progress`-д бичнэ — хариулаагүй асуулт буруу."""
    generation = await db.get(LiveGeneration, attempt.generation_id)
    assert generation is not None
    questions = await _questions(db, attempt.generation_id)
    answers = {answer.question_id: answer for answer in await _answers(db, attempt.id)}
    per_topic: dict[uuid.UUID, list[int]] = {}
    for question in questions:
        if question.topic_id is None:
            continue
        tally = per_topic.setdefault(question.topic_id, [0, 0])
        answered = answers.get(question.id)
        tally[0] += int(bool(answered and answered.is_correct))
        tally[1] += 1

    if attempt.finished_at is None:
        attempt.finished_at = _now()
        await _touch_topics(
            db,
            user.id,
            {
                topic_id: {"quiz_correct": correct, "quiz_total": total}
                for topic_id, (correct, total) in per_topic.items()
            },
        )
        await db.commit()

    views = (await topic_views(db, user.id, [generation.material_id])).get(
        generation.material_id, []
    )
    by_id = {view.topic.id: view for view in views}
    correct_count = sum(1 for answer in answers.values() if answer.is_correct)
    total = len(questions)
    return LiveAttemptResult(
        correct_count=correct_count,
        total=total,
        percent=round(100 * correct_count / total) if total else 0,
        topics=[
            LiveTopicResult(
                topic_id=topic_id,
                title=by_id[topic_id].topic.title,
                correct=correct,
                total=count,
                mastery=by_id[topic_id].mastery,
            )
            for topic_id, (correct, count) in per_topic.items()
            if topic_id in by_id
        ],
    )


# --- Заавар уншсан -----------------------------------------------------------


async def mark_guide_read(db: AsyncSession, user: User, topic: LiveTopic) -> None:
    existing = await db.get(LiveTopicProgress, (user.id, topic.id))
    values: dict[str, Any] = {}
    if existing is None or existing.guide_read_at is None:
        values["guide_read_at"] = _now()
    await _touch_topics(db, user.id, {topic.id: values})
    await db.commit()


# --- Карт ------------------------------------------------------------------


def card_view(card: LiveCard, progress: LiveCardProgress | None) -> LiveCardView:
    return LiveCardView(
        id=card.id,
        topic_id=card.topic_id,
        front=card.front,
        back=card.back,
        page=card.page,
        box=progress.box if progress else 0,
        due_at=progress.due_at if progress else None,
        reviews=progress.reviews if progress else 0,
    )


async def list_cards(
    db: AsyncSession,
    user: User,
    material: LiveMaterial,
    *,
    topic_id: uuid.UUID | None,
    mode: str,
) -> list[LiveCardView]:
    """`due` — хугацаа нь болсон давталт (эртнийх нь эхэнд), дараа нь шинэ картууд."""
    query = (
        select(LiveCard, LiveCardProgress)
        .outerjoin(
            LiveCardProgress,
            and_(LiveCardProgress.card_id == LiveCard.id, LiveCardProgress.user_id == user.id),
        )
        .where(LiveCard.material_id == material.id)
        .order_by(LiveCard.position)
    )
    if topic_id is not None:
        query = query.where(LiveCard.topic_id == topic_id)
    rows = (await db.execute(query)).all()
    if mode != "due":
        return [card_view(card, progress) for card, progress in rows]
    now = _now()
    reviews = sorted(
        ((card, progress) for card, progress in rows if progress and progress.due_at <= now),
        key=lambda row: row[1].due_at,
    )
    new = [(card, progress) for card, progress in rows if progress is None]
    return [card_view(card, progress) for card, progress in [*reviews, *new]]


async def review_card(db: AsyncSession, user: User, card: LiveCard, rating: Rating) -> LiveCardView:
    now = _now()
    progress = await db.get(LiveCardProgress, (user.id, card.id))
    if progress is None:
        progress = LiveCardProgress(
            user_id=user.id, card_id=card.id, box=0, reviews=0, due_at=now, reviewed_at=now
        )
        db.add(progress)
    progress.box, progress.due_at = review(progress.box, rating, now)
    progress.reviews += 1
    progress.reviewed_at = now
    await _touch_topics(db, user.id, {card.topic_id: {}})
    await db.commit()
    await db.refresh(progress)
    return card_view(card, progress)
