"""AI-ийн хариуны схем (Pydantic → JSON Schema → Gemini).

Схем нь энгийн, `Optional`-гүй (Gemini `anyOf` дэмждэггүй): «мэдэхгүй»
хуудас нь 0, холбоогүй сэдэв нь хоосон мөр. Урт, тоог энд хатуу шалгахгүй —
хэт урт мөрийг таслах, илүүдлийг хасахыг `pipeline.py` хийнэ; ингэснээр
жижиг зөрүүгээс болж засуулах дуудлага (зардал) гарахгүй.
"""

from typing import Literal

from pydantic import BaseModel, Field

# --- Материал задлах ---------------------------------------------------------


class AnalysisCard(BaseModel):
    front: str = Field(description="Нэр томьёо эсвэл богино асуулт.")
    back: str = Field(description="Тодорхойлолт эсвэл хариулт, 1–3 өгүүлбэр.")
    page: int = Field(description="Эх хуудас/слайдын дугаар, мэдэхгүй бол 0.")


class AnalysisTopic(BaseModel):
    key: str = Field(description="Англи, жижиг үсэг, зураастай тогтвортой нэр: binary-search.")
    title: str
    summary: str
    pages: list[int]
    cards: list[AnalysisCard]


class AnalysisSection(BaseModel):
    title: str
    topics: list[AnalysisTopic] = Field(min_length=1)


class DocumentAnalysis(BaseModel):
    title: str
    summary: str
    language: Literal["mn", "en", "mixed"]
    sections: list[AnalysisSection] = Field(min_length=1)


# --- Сэдвийн заавар ----------------------------------------------------------


class StudyGuideOutput(BaseModel):
    markdown: str = Field(min_length=50)


# --- Тест --------------------------------------------------------------------


class QuizQuestionOutput(BaseModel):
    prompt: str
    options: list[str] = Field(description="Яг 4 хариулт.")
    correct_index: int = Field(description="Зөв хариултын индекс, 0-ээс.")
    explanation: str
    topic_key: str
    page: int


class QuizOutput(BaseModel):
    questions: list[QuizQuestionOutput] = Field(min_length=1)


# --- Шалгалтад бэлтгэх -------------------------------------------------------

Likelihood = Literal["high", "medium", "low"]


class ExamPredictionOutput(BaseModel):
    topic_key: str
    title: str
    likelihood: Likelihood
    reason: str


class ExamQuestionOutput(BaseModel):
    question: str
    type: Literal["short", "long", "problem"]
    likelihood: Likelihood
    answer_outline: str
    topic_key: str


class ExamOutput(BaseModel):
    overview: str
    predictions: list[ExamPredictionOutput] = Field(min_length=1)
    questions: list[ExamQuestionOutput] = Field(min_length=1)
    study_plan: list[str]
