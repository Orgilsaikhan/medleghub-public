import uuid
from decimal import Decimal

from sqlalchemy import Boolean, ForeignKey, Index, Integer, Numeric, SmallInteger, String
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, CreatedAtMixin, UUIDPrimaryKeyMixin


class AIRequest(UUIDPrimaryKeyMixin, CreatedAtMixin, Base):
    """AI үйлчилгээ рүү илгээсэн нэг дуудлага — зардал, хязгаарын үнэний эх сурвалж.

    Prompt, материалын текст, AI-ийн хариуг ХАДГАЛАХГҮЙ — зөвхөн тоо. Хэрэглэгч,
    материал устсан ч мөр үлдэнэ (SET NULL): сарын төсөв, материалын
    хязгаар түүгээр тоологдоно. `ai_request_retention_days`-ийн дараа устана.

    `app/services/ai/` бүх платформд зориулагдсан тул `live_` угтваргүй.
    """

    __tablename__ = "ai_requests"
    __table_args__ = (
        Index("ix_ai_requests_user_created", "user_id", "created_at"),
        Index("ix_ai_requests_created_at", "created_at"),
    )

    user_id: Mapped[uuid.UUID | None] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    material_id: Mapped[uuid.UUID | None] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("live_materials.id", ondelete="SET NULL"), nullable=True
    )
    # `app.services.ai.capabilities.Capability`.
    capability: Mapped[str] = mapped_column(String(40), nullable=False)
    provider: Mapped[str] = mapped_column(String(20), nullable=False)
    model: Mapped[str] = mapped_column(String(80), nullable=False)
    prompt_version: Mapped[str] = mapped_column(String(40), nullable=False)
    # Нэг ажлын хэд дэх дуудлага (1–3), `call` / `retry` / `repair`.
    attempt: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    kind: Mapped[str] = mapped_column(String(10), nullable=False)
    input_tokens: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    cached_input_tokens: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    output_tokens: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    reasoning_tokens: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    estimated_cost_usd: Mapped[Decimal] = mapped_column(
        Numeric(12, 6), default=Decimal(0), nullable=False
    )
    # Үнийн хүснэгтийн хувилбар (`app/services/ai/prices.py`).
    price_version: Mapped[str] = mapped_column(String(20), nullable=False)
    duration_ms: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    success: Mapped[bool] = mapped_column(Boolean, nullable=False)
    error_code: Mapped[str | None] = mapped_column(String(60), nullable=True)
    provider_request_id: Mapped[str | None] = mapped_column(String(120), nullable=True)
