"""MedlegHub Live (AI Study). Вэбийн `apps/web/src/lib/types/live.ts`-тэй таарна.

Хариултын түлхүүр (`correct_index`) зөвхөн `LiveAnswerResult`-д — хэрэглэгч
хариулсны дараа. Асуултын жагсаалтад хэзээ ч байхгүй.
"""

import uuid
from datetime import datetime
from typing import Annotated, Literal

from pydantic import BaseModel, EmailStr, Field, StringConstraints

from app.models.enums import (
    LiveGenerationKind,
    LiveGenerationStatus,
    LiveMaterialKind,
    LiveMaterialStatus,
    LiveTier,
)

Title = Annotated[str, StringConstraints(min_length=1, max_length=200, strip_whitespace=True)]
Likelihood = Literal["high", "medium", "low"]


class LiveUsage(BaseModel):
    """Энэ сарын AI хэрэглээ (хувиар). Материалын тоог хэрэглэгчид харуулахгүй."""

    ai_used_percent: int
    ai_period_resets_at: datetime


class LiveUploadLimits(BaseModel):
    max_bytes: int
    max_pages: int
    accepted: list[str]


class LivePassMaterial(BaseModel):
    """Нэг удаагийн эрхээр нээсэн материал: хэзээ хүртэл, AI-ийн хэдэн хувийг хэрэглэсэн."""

    material_id: uuid.UUID
    expires_at: datetime
    ai_used_percent: int


class LivePassInfo(BaseModel):
    """`tier == pass` үед. Ашиглаагүй эрхээр нэг материал оруулна."""

    unused: bool
    materials: list[LivePassMaterial]


class LiveConfig(BaseModel):
    enabled: bool
    ai_configured: bool
    tier: LiveTier | None
    tier_expires_at: datetime | None
    # Багцтай үед сарын хэрэглээ; нэг удаагийн эрхэд `None` (`passes`-ийг үз).
    usage: LiveUsage | None
    upload: LiveUploadLimits
    passes: LivePassInfo | None = None


class LiveMaterialCreate(BaseModel):
    filename: Annotated[str, StringConstraints(min_length=1, max_length=255)]
    size_bytes: int = Field(gt=0)
    title: Title | None = None


class LiveMaterialUpdate(BaseModel):
    title: Title


class LiveMaterialSummary(BaseModel):
    id: uuid.UUID
    title: str
    kind: LiveMaterialKind
    status: LiveMaterialStatus
    error_code: str | None
    error_message: str | None
    page_count: int | None
    size_bytes: int
    topic_count: int
    mastery: int
    created_at: datetime
    processed_at: datetime | None


class LiveTopic(BaseModel):
    id: uuid.UUID
    title: str
    summary: str
    pages: list[int]
    mastery: int
    card_count: int
    last_studied_at: datetime | None
    guide_read: bool
    quiz_percent: int | None


class LiveSection(BaseModel):
    title: str
    topics: list[LiveTopic]


class LiveGenerationBrief(BaseModel):
    id: uuid.UUID
    kind: LiveGenerationKind
    status: LiveGenerationStatus
    topic_id: uuid.UUID | None
    error_code: str | None
    error_message: str | None
    created_at: datetime
    updated_at: datetime


class LiveCardStats(BaseModel):
    total: int
    due: int
    new: int
    mastered: int


class LiveMaterialDetail(LiveMaterialSummary):
    summary: str | None
    sections: list[LiveSection]
    cards: LiveCardStats
    full_quiz: LiveGenerationBrief | None
    exam: LiveGenerationBrief | None
    last_studied_topic_id: uuid.UUID | None


class LiveGuideContent(BaseModel):
    markdown: str


class LiveQuizQuestion(BaseModel):
    id: uuid.UUID
    position: int
    prompt: str
    options: list[str]
    topic_id: uuid.UUID | None


class LiveQuizContent(BaseModel):
    questions: list[LiveQuizQuestion]


class LiveExamPrediction(BaseModel):
    topic_id: uuid.UUID | None
    title: str
    likelihood: Likelihood
    reason: str


class LiveExamQuestion(BaseModel):
    question: str
    type: Literal["short", "long", "problem"]
    likelihood: Likelihood
    answer_outline: str
    topic_id: uuid.UUID | None


class LiveExamContent(BaseModel):
    overview: str
    predictions: list[LiveExamPrediction]
    questions: list[LiveExamQuestion]
    study_plan: list[str]


class LiveGeneration(LiveGenerationBrief):
    material_id: uuid.UUID
    guide: LiveGuideContent | None
    quiz: LiveQuizContent | None
    exam: LiveExamContent | None


class LiveGenerationRequest(BaseModel):
    kind: LiveGenerationKind
    topic_id: uuid.UUID | None = None
    regenerate: bool = False


class LiveAttemptAnswer(BaseModel):
    question_id: uuid.UUID
    choice_index: int
    correct: bool


class LiveAttempt(BaseModel):
    id: uuid.UUID
    generation_id: uuid.UUID
    total: int
    correct_count: int
    answers: list[LiveAttemptAnswer]
    finished_at: datetime | None


class LiveAnswerCreate(BaseModel):
    question_id: uuid.UUID
    choice_index: int = Field(ge=0, le=5)


class LiveAnswerResult(BaseModel):
    question_id: uuid.UUID
    correct: bool
    correct_index: int
    explanation: str
    page: int | None


class LiveTopicResult(BaseModel):
    topic_id: uuid.UUID
    title: str
    correct: int
    total: int
    mastery: int


class LiveAttemptResult(BaseModel):
    correct_count: int
    total: int
    percent: int
    topics: list[LiveTopicResult]


class LiveCard(BaseModel):
    id: uuid.UUID
    topic_id: uuid.UUID
    front: str
    back: str
    page: int | None
    box: int
    due_at: datetime | None
    reviews: int


class LiveCardReview(BaseModel):
    rating: Literal["again", "hard", "good"]


# --- Админ -------------------------------------------------------------------


class LiveCapabilitySpend(BaseModel):
    capability: str
    requests: int
    failed: int
    cost_usd: float


class LiveAdminOverview(BaseModel):
    live_access: Literal["off", "admins", "all"]
    ai_configured: bool
    month_spend_usd: float
    budget_usd: float
    budget_percent: int
    by_capability: list[LiveCapabilitySpend]
    materials_total: int
    materials_failed: int
    users_with_materials: int


class LiveModelTask(BaseModel):
    task: str
    # 1 — үндсэн загвар; 2+ — нөөц (дарааллын байр).
    position: int


class LiveModelLimits(BaseModel):
    rpm: int | None
    tpm: int | None
    rpd: int | None


class LiveModelStatus(BaseModel):
    """Нэг загварын төлөв: хязгаарт хүрсэн эсэх, хэрэглээ, энэ сарын зардал."""

    model: str
    tasks: list[LiveModelTask]
    # `ready` — ажил авна; `cooling` — Google 429/503-ын дараа түр алгасна;
    # `near_limit` — `AI_MODEL_LIMITS`-ийн 90%-д хүрсэн; `not_configured` — түлхүүргүй;
    # `no_price` — үнэгүй тул production-д дуудахгүй.
    status: Literal["ready", "cooling", "near_limit", "not_configured", "no_price"]
    # `overloaded` / `rate_limited` / `quota` / `timeout` / `rpm` / `tpm` / `rpd`.
    reason: str | None
    available_at: datetime | None
    last_error: str | None
    last_error_at: datetime | None
    minute_requests: int
    minute_input_tokens: int
    day_requests: int
    limits: LiveModelLimits | None
    month_requests: int
    month_failures: int
    month_cost_usd: float
    # 1 сая токен тутамд USD (оролт / гаралт).
    price_input_usd: float | None
    price_output_usd: float | None


class LiveSubscriptionLookup(BaseModel):
    email: EmailStr


class LiveSubscriptionGrant(BaseModel):
    """Premium олгох. Standard багц ч Premium дуусах хүртэл сунгагдана."""

    email: EmailStr
    months: int = Field(ge=1, le=24)
    note: Annotated[str, StringConstraints(max_length=200, strip_whitespace=True)] | None = None


class LiveSubscriptionInfo(BaseModel):
    email: str
    name: str
    tier: LiveTier
    # Тухайн эрхийн дуусах хугацаа (Standard бол багцынх, Premium бол Premium-ийнх).
    expires_at: datetime | None
    # Сургалт + Live-ийн Standard багц (Premium-ээс урт байж болно).
    plan_expires_at: datetime | None
