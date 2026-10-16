"""AI ажлууд (`Capability`) ба тус бүрийн тохиргоо (хугацаа, гаралтын дээд токен, бодлын түвшин).

Ажил бүр өөрийн загварын дараалалтай (`Settings.ai_*_models`): хөнгөн ажил
(сэдвийн заавар, сэдвийн тест) хямд загвараас, хүнд ажил (материал задлах, бүтэн
тест, таамаг) хүчтэй загвараас эхэлнэ. Аль загвар ажиллахыг `router.py` шийднэ.
"""

from dataclasses import dataclass
from enum import StrEnum


class Capability(StrEnum):
    # Материалыг задлах: хэсэг → сэдэв → нэр томьёоны карт. Хүнд.
    DOCUMENT = "document"
    # Сэдвийн заавар (Markdown). Хөнгөн.
    STUDY_GUIDE = "study_guide"
    # Нэг сэдвийн 5 асуулттай тест. Хөнгөн.
    TOPIC_QUIZ = "topic_quiz"
    # Бүтэн материалын тест. Хүнд.
    FULL_QUIZ = "full_quiz"
    # «Шалгалтад бэлтгэх» — шалгалтад гарч болох сэдэв, асуулт. Хүнд.
    EXAM = "exam"


@dataclass(frozen=True)
class CapabilitySpec:
    # `Settings`-ийн аль талбар загварын дарааллыг заах вэ.
    route_setting: str
    # Бодлын токенийг оруулсан гаралтын дээд хэмжээ — зардлын дээд хязгаарыг тогтооно.
    max_output_tokens: int
    # `low` / `medium` / `high` — 3.8 Flash, 3.5/3.1 Flash-Lite бүгд хүлээж авдаг
    # (2026-10-01 шалгасан). 3.8 Flash `minimal`-д алдаа өгдөг.
    thinking_level: str
    timeout_seconds: float


SPECS: dict[Capability, CapabilitySpec] = {
    # Том материалд хэсэг, сэдэв, карт нь 15–25 мянган токен хүрнэ.
    Capability.DOCUMENT: CapabilitySpec("ai_document_models", 32_768, "low", 300.0),
    Capability.STUDY_GUIDE: CapabilitySpec("ai_guide_models", 8_192, "low", 180.0),
    Capability.TOPIC_QUIZ: CapabilitySpec("ai_topic_quiz_models", 8_192, "medium", 180.0),
    Capability.FULL_QUIZ: CapabilitySpec("ai_full_quiz_models", 12_288, "medium", 180.0),
    Capability.EXAM: CapabilitySpec("ai_exam_models", 12_288, "medium", 180.0),
}
