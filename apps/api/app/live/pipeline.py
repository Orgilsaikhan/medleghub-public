"""Цаана хийгдэх ажил: материал задлах, заавар / тест / таамаг үүсгэх.

Өгөгдлийн сангийн холболтыг AI дуудлагын турш БАРИХГҮЙ (1–5 минут): уншаад
хаана, AI-г дуудна, үр дүнг шинэ богино транзакцаар бичнэ. Ажлын хооронд
материал устсан бол чимээгүй зогсоно.

Бүтэлгүйтвэл материал / үүсгэлт `failed` болж, `error_code`-оор монгол мессеж
харагдана. Эх файл R2-д үлдэх тул «Дахин оролдох» нь бүх алхмыг дахин хийнэ.
"""

import logging
import random
import re
import uuid
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.core.config import settings
from app.live import extract_client, prompts, source
from app.live.access import budget_check
from app.live.ai_outputs import DocumentAnalysis, ExamOutput, QuizOutput, StudyGuideOutput
from app.live.extract_client import Extraction, ExtractionError
from app.live.storage import BlobStorage, StorageError
from app.models.enums import (
    LiveGenerationKind,
    LiveGenerationStatus,
    LiveMaterialKind,
    LiveMaterialStatus,
)
from app.models.live import LiveCard, LiveGeneration, LiveMaterial, LiveQuestion, LiveTopic
from app.services.ai.capabilities import Capability
from app.services.ai.errors import (
    AIBudgetError,
    AIError,
    AIIncompleteError,
    AINotConfiguredError,
    AIOutputError,
)
from app.services.ai.service import AIService, CallContext
from app.services.ai.types import Part

logger = logging.getLogger(__name__)

MAX_TOPICS = 24
MAX_CARDS_PER_TOPIC = 8
MAX_PAGES_PER_TOPIC = 20

Extractor = Callable[[str, bytes], Awaitable[Extraction]]


@dataclass
class LiveContext:
    """Цаана ажиллах бүх хамаарал — тестэд хуурамчаар солино."""

    sessions: async_sessionmaker[AsyncSession]
    ai: AIService
    storage: BlobStorage
    extract: Extractor = extract_client.extract


class JobFailed(Exception):
    def __init__(self, code: str, *, retryable: bool = False) -> None:
        super().__init__(code)
        self.code = code
        self.retryable = retryable


def _ai_failure(exc: AIError) -> JobFailed:
    if isinstance(exc, AIBudgetError):
        codes = {"platform_budget": "LIVE_AI_PAUSED", "pass_budget": "LIVE_PASS_QUOTA_EXCEEDED"}
        return JobFailed(codes.get(exc.code, "LIVE_QUOTA_EXCEEDED"))
    if isinstance(exc, AINotConfiguredError):
        return JobFailed("LIVE_AI_NOT_CONFIGURED")
    if isinstance(exc, AIIncompleteError):
        return JobFailed("LIVE_AI_TOO_LONG")
    if isinstance(exc, AIOutputError):
        return JobFailed("LIVE_AI_OUTPUT_INVALID")
    if exc.detail in ("payment_required", "billing"):
        # Манай AI данс (OpenRouter кредит, Google billing) дууссан — бүх хэрэглэгчид адил.
        logger.error("live: AI-ийн данс дууссан (%s) — кредит нэмнэ үү", exc.code)
        return JobFailed("LIVE_AI_PAUSED")
    if exc.retryable:
        # Хүлээж дахин оролдсоор ч Gemini ачаалалтай — ажлыг дараалалд нэг удаа буцаана.
        return JobFailed("LIVE_AI_BUSY", retryable=True)
    return JobFailed("LIVE_AI_FAILED")


def _clip(value: str, limit: int) -> str:
    value = (value or "").strip()
    return value if len(value) <= limit else value[: limit - 1].rstrip() + "…"


def _page(value: int, page_count: int | None) -> int | None:
    if value < 1 or (page_count and value > page_count):
        return None
    return value


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")[:80]


# --- Материал задлах ---------------------------------------------------------


@dataclass
class _NormalizedTopic:
    section_position: int
    section_title: str
    key: str
    title: str
    summary: str
    pages: list[int]
    cards: list[tuple[str, str, int | None]]


def normalize_analysis(
    analysis: DocumentAnalysis, page_count: int | None
) -> list[_NormalizedTopic]:
    """Урт мөрийг таслах, илүүдлийг хасах, давхардсан key-г ялгах."""
    topics: list[_NormalizedTopic] = []
    keys: set[str] = set()
    for section_position, section in enumerate(analysis.sections):
        for topic in section.topics:
            title = _clip(topic.title, 200)
            if not title or len(topics) >= MAX_TOPICS:
                continue
            key = _slug(topic.key) or f"topic-{len(topics) + 1}"
            base, suffix = key, 2
            while key in keys:
                key, suffix = f"{base}-{suffix}", suffix + 1
            keys.add(key)
            pages = sorted({p for p in topic.pages if _page(p, page_count)})[:MAX_PAGES_PER_TOPIC]
            cards = [
                (_clip(card.front, 300), _clip(card.back, 1000), _page(card.page, page_count))
                for card in topic.cards
                if card.front.strip() and card.back.strip()
            ][:MAX_CARDS_PER_TOPIC]
            topics.append(
                _NormalizedTopic(
                    section_position=section_position,
                    section_title=_clip(section.title, 200) or title,
                    key=key,
                    title=title,
                    summary=_clip(topic.summary, 1000),
                    pages=pages,
                    cards=cards,
                )
            )
    return topics


def _validate_analysis(analysis: DocumentAnalysis) -> None:
    if not normalize_analysis(analysis, None):
        raise ValueError("Сэдэв олдсонгүй: sections[].topics[].title хоосон байж болохгүй.")


async def _fail_material(ctx: LiveContext, material_id: uuid.UUID, failure: JobFailed) -> None:
    async with ctx.sessions() as db:
        material = await db.get(LiveMaterial, material_id)
        if material is None:
            return
        if failure.retryable and material.attempts < settings.live_job_max_attempts:
            material.status = LiveMaterialStatus.QUEUED
        else:
            material.status = LiveMaterialStatus.FAILED
            material.error_code = failure.code
        await db.commit()


async def _extract(ctx: LiveContext, material: LiveMaterial, data: bytes):
    """`(хуудсууд, хуудасны тоо, таслагдсан эсэх)`."""
    kind = LiveMaterialKind(material.kind)
    if kind in source.EXTRACTED_KINDS:
        try:
            extraction = await ctx.extract(kind.value, data)
        except ExtractionError as exc:
            raise JobFailed(exc.code, retryable=exc.retryable) from exc
        return extraction.pages, extraction.page_count, extraction.truncated
    if kind in source.TEXT_KINDS:
        pages = source.paginate_text(source.decode_text(data))
        return pages, len(pages), False
    return [], 1, False


async def process_material(ctx: LiveContext, material_id: uuid.UUID) -> None:
    async with ctx.sessions() as db:
        material = await db.get(LiveMaterial, material_id)
        if material is None or material.status != LiveMaterialStatus.PROCESSING:
            return
        db.expunge(material)
    try:
        await _process_material(ctx, material)
    except JobFailed as failure:
        logger.info("live: материал %s → %s", material_id, failure.code)
        await _fail_material(ctx, material_id, failure)
    except AIError as exc:
        logger.warning("live: материал %s AI алдаа %s", material_id, exc.code)
        await _fail_material(ctx, material_id, _ai_failure(exc))


async def _process_material(ctx: LiveContext, material: LiveMaterial) -> None:
    try:
        data = await ctx.storage.get(material.storage_key)
    except StorageError as exc:
        raise JobFailed("LIVE_UPLOAD_MISSING") from exc

    pages, page_count, truncated = await _extract(ctx, material, data)
    if page_count > settings.live_max_pages:
        raise JobFailed("LIVE_TOO_MANY_PAGES")
    # PDF-д текст давхаргагүй (скан) байж болно — Gemini хуудсыг зураг байдлаар уншина.
    textual = material.kind not in (LiveMaterialKind.PDF, LiveMaterialKind.IMAGE)
    if textual and not source.has_text(pages):
        raise JobFailed("LIVE_EMPTY_DOCUMENT")

    material.page_count = page_count
    if source.has_text(pages):
        material.text_key = source.text_key(material)
        await ctx.storage.put(
            material.text_key, source.encode_pages(pages, truncated), "application/json"
        )
    async with ctx.sessions() as db:
        stored = await db.get(LiveMaterial, material.id)
        if stored is None:
            return
        stored.page_count = page_count
        stored.text_key = material.text_key
        await db.commit()

    loaded = await source.load_source(ctx.storage, material)
    analysis, run = await ctx.ai.generate(
        Capability.DOCUMENT,
        DocumentAnalysis,
        system=prompts.SYSTEM,
        parts=[*loaded.parts, Part.of_text(prompts.DOCUMENT.format(max_topics=MAX_TOPICS))],
        call=CallContext(material.owner_id, material.id, prompts.DOCUMENT_VERSION),
        input_tokens_estimate=loaded.input_tokens_estimate,
        budget_check=budget_check(ctx.sessions, material.owner_id, material.id),
        validate=_validate_analysis,
        context={"source_text": loaded.text, "title": material.title, "page_count": page_count},
    )
    topics = normalize_analysis(analysis, page_count)

    async with ctx.sessions() as db:
        stored = await db.get(LiveMaterial, material.id)
        if stored is None:
            return
        await db.execute(delete(LiveTopic).where(LiveTopic.material_id == stored.id))
        card_position = 0
        for position, item in enumerate(topics):
            topic = LiveTopic(
                material_id=stored.id,
                section_position=item.section_position,
                section_title=item.section_title,
                position=position,
                key=item.key,
                title=item.title,
                summary=item.summary,
                pages=item.pages,
            )
            db.add(topic)
            await db.flush()
            for front, back, page in item.cards:
                db.add(
                    LiveCard(
                        material_id=stored.id,
                        topic_id=topic.id,
                        position=card_position,
                        front=front,
                        back=back,
                        page=page,
                    )
                )
                card_position += 1
        # Хэрэглэгч нэр өгөөгүй (файлын нэрээс) бол AI-ийн нэрийг авна.
        if stored.title == source.default_title(stored.filename) and analysis.title.strip():
            stored.title = _clip(analysis.title, 200)
        stored.summary = _clip(analysis.summary, 2000)
        stored.status = LiveMaterialStatus.READY
        stored.error_code = None
        stored.processed_at = datetime.now(UTC)
        stored.model = f"{run.provider}:{run.model}"
        stored.prompt_version = run.prompt_version
        await db.commit()


# --- Заавар, тест, таамаг ------------------------------------------------------


def _topic_payload(topic: LiveTopic) -> dict[str, Any]:
    return {"key": topic.key, "title": topic.title, "summary": topic.summary}


def normalize_quiz(
    output: QuizOutput, keys: dict[str, uuid.UUID], page_count: int | None, limit: int
) -> list[dict[str, Any]]:
    """4 өөр хариулттай, зөв индекс нь хүрээндээ байгаа асуултууд — хариултыг холино."""
    questions: list[dict[str, Any]] = []
    seen: set[str] = set()
    for item in output.questions:
        prompt = _clip(item.prompt, 1000)
        options = [_clip(option, 300) for option in item.options]
        normalized = {option.casefold() for option in options}
        if (
            not prompt
            or prompt.casefold() in seen
            or len(options) != 4
            or "" in options
            or len(normalized) != 4
            or not 0 <= item.correct_index < 4
        ):
            continue
        seen.add(prompt.casefold())
        correct = options[item.correct_index]
        random.shuffle(options)
        questions.append(
            {
                "prompt": prompt,
                "options": options,
                "correct_index": options.index(correct),
                "explanation": _clip(item.explanation, 1000),
                "topic_id": keys.get(_slug(item.topic_key)),
                "page": _page(item.page, page_count),
            }
        )
        if len(questions) >= limit:
            break
    return questions


def normalize_exam(output: ExamOutput, keys: dict[str, uuid.UUID]) -> dict[str, Any]:
    def topic_id(key: str) -> str | None:
        found = keys.get(_slug(key))
        return str(found) if found else None

    return {
        "overview": _clip(output.overview, 1500),
        "predictions": [
            {
                "topic_id": topic_id(item.topic_key),
                "title": _clip(item.title, 200),
                "likelihood": item.likelihood,
                "reason": _clip(item.reason, 800),
            }
            for item in output.predictions[:10]
        ],
        "questions": [
            {
                "question": _clip(item.question, 1000),
                "type": item.type,
                "likelihood": item.likelihood,
                "answer_outline": _clip(item.answer_outline, 2500),
                "topic_id": topic_id(item.topic_key),
            }
            for item in output.questions[:12]
        ],
        "study_plan": [_clip(step, 300) for step in output.study_plan[:10] if step.strip()],
    }


async def _fail_generation(
    ctx: LiveContext, generation_id: uuid.UUID, code: str, *, retryable: bool = False
) -> None:
    async with ctx.sessions() as db:
        generation = await db.get(LiveGeneration, generation_id)
        if generation is None:
            return
        if retryable and generation.attempts < settings.live_job_max_attempts:
            generation.status = LiveGenerationStatus.QUEUED
        else:
            generation.status = LiveGenerationStatus.FAILED
            generation.error_code = code
        await db.commit()


async def process_generation(ctx: LiveContext, generation_id: uuid.UUID) -> None:
    async with ctx.sessions() as db:
        generation = await db.get(LiveGeneration, generation_id)
        if generation is None or generation.status != LiveGenerationStatus.PROCESSING:
            return
        material = await db.get(LiveMaterial, generation.material_id)
        if material is None or material.status != LiveMaterialStatus.READY:
            await _fail_generation(ctx, generation_id, "LIVE_MATERIAL_NOT_READY")
            return
        topics = list(
            (
                await db.execute(
                    select(LiveTopic)
                    .where(LiveTopic.material_id == material.id)
                    .order_by(LiveTopic.position)
                )
            )
            .scalars()
            .all()
        )
        for row in (generation, material, *topics):
            db.expunge(row)
    try:
        await _process_generation(ctx, generation, material, topics)
    except JobFailed as failure:
        await _fail_generation(ctx, generation_id, failure.code, retryable=failure.retryable)
    except StorageError:
        await _fail_generation(ctx, generation_id, "LIVE_UPLOAD_MISSING")
    except AIError as exc:
        logger.warning("live: үүсгэлт %s AI алдаа %s", generation_id, exc.code)
        failure = _ai_failure(exc)
        await _fail_generation(ctx, generation_id, failure.code, retryable=failure.retryable)


async def _process_generation(
    ctx: LiveContext,
    generation: LiveGeneration,
    material: LiveMaterial,
    topics: list[LiveTopic],
) -> None:
    loaded = await source.load_source(ctx.storage, material)
    lines = [prompts.TopicLine(topic.key, topic.title) for topic in topics]
    keys = {topic.key: topic.id for topic in topics}
    topic = next((item for item in topics if item.id == generation.topic_id), None)
    if generation.topic_id is not None and topic is None:
        raise JobFailed("LIVE_BAD_TOPIC")
    common: dict[str, Any] = {
        "system": prompts.SYSTEM,
        "call": CallContext(material.owner_id, material.id, ""),
        "input_tokens_estimate": loaded.input_tokens_estimate,
        "budget_check": budget_check(ctx.sessions, material.owner_id, material.id),
    }
    content: dict[str, Any] | None = None
    questions: list[dict[str, Any]] = []

    if generation.kind == LiveGenerationKind.GUIDE:
        assert topic is not None
        instruction = prompts.GUIDE.format(
            title=topic.title,
            key=topic.key,
            section=topic.section_title,
            summary=topic.summary,
            pages=prompts.pages_label(topic.pages),
            other_topics=prompts.topic_list([line for line in lines if line.key != topic.key]),
        )
        common["call"] = CallContext(material.owner_id, material.id, prompts.GUIDE_VERSION)
        guide, run = await ctx.ai.generate(
            Capability.STUDY_GUIDE,
            StudyGuideOutput,
            parts=[*loaded.parts, Part.of_text(instruction)],
            context={
                "topic_title": topic.title,
                "topic_summary": topic.summary,
                "pages": topic.pages,
            },
            **common,
        )
        content = {"markdown": _clip(guide.markdown, 20_000)}

    elif generation.kind == LiveGenerationKind.QUIZ:
        count = settings.live_topic_quiz_questions if topic else settings.live_full_quiz_questions
        scope = (
            prompts.QUIZ_SCOPE_TOPIC.format(title=topic.title, key=topic.key)
            if topic
            else prompts.QUIZ_SCOPE_FULL
        )
        instruction = prompts.QUIZ.format(
            count=count, scope=scope, topics=prompts.topic_list(lines)
        )
        common["call"] = CallContext(material.owner_id, material.id, prompts.QUIZ_VERSION)

        def validate(output: QuizOutput) -> None:
            if len(normalize_quiz(output, keys, material.page_count, count)) < max(1, count // 2):
                raise ValueError(
                    "Асуулт бүр яг 4 өөр хариулттай, correct_index 0–3 байх ёстой; "
                    f"{count} асуулт хэрэгтэй."
                )

        quiz, run = await ctx.ai.generate(
            # Нэг сэдвийн тест хөнгөн (хямд загвараас), бүтэн тест хүнд.
            Capability.TOPIC_QUIZ if topic else Capability.FULL_QUIZ,
            QuizOutput,
            parts=[*loaded.parts, Part.of_text(instruction)],
            validate=validate,
            context={
                "topics": [_topic_payload(item) for item in ([topic] if topic else topics)],
                "count": count,
            },
            **common,
        )
        questions = normalize_quiz(quiz, keys, material.page_count, count)
        if topic is not None:
            # Сэдвийн тестийн бүх асуулт тэр сэдвийнх — AI буруу key өгсөн ч.
            for question in questions:
                question["topic_id"] = topic.id

    else:
        instruction = prompts.EXAM.format(topics=prompts.topic_list(lines))
        common["call"] = CallContext(material.owner_id, material.id, prompts.EXAM_VERSION)
        exam, run = await ctx.ai.generate(
            Capability.EXAM,
            ExamOutput,
            parts=[*loaded.parts, Part.of_text(instruction)],
            context={"topics": [_topic_payload(item) for item in topics]},
            **common,
        )
        content = normalize_exam(exam, keys)

    async with ctx.sessions() as db:
        stored = await db.get(LiveGeneration, generation.id)
        if stored is None:
            return
        await db.execute(delete(LiveQuestion).where(LiveQuestion.generation_id == stored.id))
        for position, question in enumerate(questions):
            db.add(LiveQuestion(generation_id=stored.id, position=position, **question))
        stored.content = content
        stored.status = LiveGenerationStatus.READY
        stored.error_code = None
        stored.model = f"{run.provider}:{run.model}"
        stored.prompt_version = run.prompt_version
        await db.commit()
