/**
 * MedlegHub Live (AI Study) — backend-ийн response типүүд.
 *
 * `apps/api/app/schemas/live.py`-тай тохирч байх ёстой. Хариултын түлхүүр
 * (`correct_index`) зөвхөн хариулт илгээсний дараа `LiveAnswerResult`-д ирнэ —
 * асуултын жагсаалтад хэзээ ч байхгүй.
 */

/**
 * `free` — нийт 1 материал; `standard` — Standard багц (Live багтсан);
 * `premium` — Standard дээр илүү AI хязгаар.
 */
/** `pass` — багцгүй, нэг удаагийн эрхтэй: ашиглаагүй эрх эсвэл эрхээр нээсэн материал. */
export type LiveTier = "free" | "pass" | "standard" | "premium";

export type LiveMaterialKind = "pdf" | "pptx" | "docx" | "txt" | "md" | "image";

/**
 * `uploading` — мета бүртгэгдсэн, файл хараахан ирээгүй;
 * `queued`/`processing` — AI задалж байна; `ready` — судлахад бэлэн.
 */
export type LiveMaterialStatus = "uploading" | "queued" | "processing" | "ready" | "failed";

/** `guide` — сэдвийн заавар; `quiz` — сэдвийн эсвэл бүтэн тест; `exam` — шалгалтын таамаг. */
export type LiveGenerationKind = "guide" | "quiz" | "exam";

export type LiveGenerationStatus = "queued" | "processing" | "ready" | "failed";

/** Материалын тоог хэрэглэгчид харуулахгүй — зөвхөн AI хэрэглээний хувь. */
export interface LiveUsage {
  /** Энэ сарын AI хэрэглээ хэрэглэгчийн хязгаараас хэдэн хувь (0–100). */
  ai_used_percent: number;
  /** Дараагийн сарын эхлэл (Улаанбаатарын цагаар). */
  ai_period_resets_at: string;
}

export interface LiveConfig {
  /** `LIVE_ACCESS` энэ хэрэглэгчийг зөвшөөрч байгаа эсэх. Зочинд үргэлж `false`. */
  enabled: boolean;
  /** AI түлхүүр, загвар тохируулагдсан эсэх. `false` бол материал боловсруулахгүй. */
  ai_configured: boolean;
  tier: LiveTier | null;
  tier_expires_at: string | null;
  /**
   * Багцын сарын хэрэглээ. `null` — Live хаалттай, багцгүй (`free`) эсвэл нэг удаагийн
   * эрхтэй (`pass` — `passes`-ийг үз).
   */
  usage: LiveUsage | null;
  upload: {
    max_bytes: number;
    max_pages: number;
    /** Өргөтгөлүүд: `.pdf`, `.pptx`, … — `<input accept>`-д шууд. */
    accepted: string[];
  };
  /** Зөвхөн `tier === "pass"` үед. */
  passes?: LivePassInfo | null;
}

/** Нэг удаагийн эрхээр нээсэн материал. */
export interface LivePassMaterial {
  material_id: string;
  /** Эрх дуусах мөч — ашигласнаас хойш 30 хоног. */
  expires_at: string;
  /** Энэ материалын AI хязгаарын хэдэн хувийг хэрэглэсэн (0–100). */
  ai_used_percent: number;
}

export interface LivePassInfo {
  /** Ашиглаагүй эрх байгаа эсэх — байвал нэг материал оруулна. */
  unused: boolean;
  materials: LivePassMaterial[];
}

export interface LiveMaterialSummary {
  id: string;
  title: string;
  kind: LiveMaterialKind;
  status: LiveMaterialStatus;
  error_code: string | null;
  /** Монгол мессеж — `failed` үед. */
  error_message: string | null;
  page_count: number | null;
  size_bytes: number;
  topic_count: number;
  /** Сэдвүүдийн эзэмшлийн дундаж, 0–100. */
  mastery: number;
  created_at: string;
  processed_at: string | null;
}

export interface LiveTopic {
  id: string;
  title: string;
  summary: string;
  /** Эх материалын хуудас/слайдын дугаар (1-ээс). */
  pages: number[];
  /** 0–100: заавар уншсан 10 + картууд 40 + тест 50. */
  mastery: number;
  card_count: number;
  last_studied_at: string | null;
  guide_read: boolean;
  /** Энэ сэдвийн асуултуудын сүүлийн тестийн хувь. Тест өгөөгүй бол `null`. */
  quiz_percent: number | null;
}

export interface LiveSection {
  title: string;
  topics: LiveTopic[];
}

export interface LiveGenerationBrief {
  id: string;
  kind: LiveGenerationKind;
  status: LiveGenerationStatus;
  /** `null` — бүтэн материалын (бүтэн тест, шалгалтын таамаг). */
  topic_id: string | null;
  error_code: string | null;
  error_message: string | null;
  created_at: string;
  updated_at: string;
}

export interface LiveCardStats {
  total: number;
  /** Одоо давтах ёстой (шинэ картуудыг оруулаад). */
  due: number;
  /** Хэзээ ч давтаагүй. */
  new: number;
  /** Хамгийн дээд хайрцагт хүрсэн. */
  mastered: number;
}

export interface LiveMaterialDetail extends LiveMaterialSummary {
  /** AI-ийн товч агуулга (энгийн текст). */
  summary: string | null;
  sections: LiveSection[];
  /** Бүтэн материалын картууд. */
  cards: LiveCardStats;
  /** Бүтэн тест — хараахан үүсгээгүй бол `null`. */
  full_quiz: LiveGenerationBrief | null;
  /** «Шалгалтад бэлтгэх» — хараахан үүсгээгүй бол `null`. */
  exam: LiveGenerationBrief | null;
  last_studied_topic_id: string | null;
}

export interface LiveGuideContent {
  /** Markdown — HTML, зураггүй харуулна (`CommunityMarkdown`). */
  markdown: string;
}

export interface LiveQuizQuestion {
  id: string;
  position: number;
  prompt: string;
  options: string[];
  topic_id: string | null;
}

export interface LiveQuizContent {
  questions: LiveQuizQuestion[];
}

export type LiveLikelihood = "high" | "medium" | "low";

export interface LiveExamPrediction {
  topic_id: string | null;
  title: string;
  likelihood: LiveLikelihood;
  reason: string;
}

export interface LiveExamQuestion {
  question: string;
  /** `short` — богино хариулт; `long` — дэлгэрэнгүй; `problem` — бодлого. */
  type: "short" | "long" | "problem";
  likelihood: LiveLikelihood;
  /** Хариултын гол санаанууд (Markdown). */
  answer_outline: string;
  topic_id: string | null;
}

export interface LiveExamContent {
  overview: string;
  predictions: LiveExamPrediction[];
  questions: LiveExamQuestion[];
  study_plan: string[];
}

export interface LiveGeneration extends LiveGenerationBrief {
  material_id: string;
  guide: LiveGuideContent | null;
  quiz: LiveQuizContent | null;
  exam: LiveExamContent | null;
}

export interface LiveAttemptAnswer {
  question_id: string;
  choice_index: number;
  correct: boolean;
}

export interface LiveAttempt {
  id: string;
  generation_id: string;
  total: number;
  correct_count: number;
  answers: LiveAttemptAnswer[];
  finished_at: string | null;
}

export interface LiveAnswerResult {
  question_id: string;
  correct: boolean;
  correct_index: number;
  explanation: string;
  page: number | null;
}

export interface LiveTopicResult {
  topic_id: string;
  title: string;
  correct: number;
  total: number;
  /** Тестийн дараах шинэ эзэмшил. */
  mastery: number;
}

export interface LiveAttemptResult {
  correct_count: number;
  total: number;
  percent: number;
  topics: LiveTopicResult[];
}

export interface LiveCard {
  id: string;
  topic_id: string;
  front: string;
  back: string;
  page: number | null;
  /** Leitner хайрцаг 0–4. 4 — эзэмшсэн. */
  box: number;
  /** `null` — хэзээ ч давтаагүй (шинэ). */
  due_at: string | null;
  reviews: number;
}

/** `again` — мэдэхгүй; `hard` — эргэлзсэн; `good` — мэднэ. */
export type LiveCardRating = "again" | "hard" | "good";

// --- Админ -------------------------------------------------------------------

export interface LiveCapabilitySpend {
  capability: string;
  requests: number;
  failed: number;
  cost_usd: number;
}

export interface LiveAdminOverview {
  live_access: "off" | "admins" | "all";
  ai_configured: boolean;
  month_spend_usd: number;
  budget_usd: number;
  budget_percent: number;
  by_capability: LiveCapabilitySpend[];
  materials_total: number;
  materials_failed: number;
  users_with_materials: number;
}

export interface LiveModelTask {
  /** `document` / `study_guide` / `topic_quiz` / `full_quiz` / `exam`. */
  task: string;
  /** 1 — үндсэн загвар; 2+ — нөөц. */
  position: number;
}

/**
 * `ready` — ажил авна; `cooling` — Google 429 (хязгаар) / 503 (ачаалал)-ын дараа
 * түр алгасна; `near_limit` — AI Studio-гийн хязгаарын 90%-д хүрсэн;
 * `not_configured` — түлхүүргүй; `no_price` — үнэгүй тул production-д дуудахгүй.
 */
export type LiveModelState = "ready" | "cooling" | "near_limit" | "not_configured" | "no_price";

export interface LiveModelStatus {
  /** `gemini:gemini-3.8-flash`. */
  model: string;
  tasks: LiveModelTask[];
  status: LiveModelState;
  /** `overloaded` / `rate_limited` / `quota` / `timeout` / `rpm` / `tpm` / `rpd`. */
  reason: string | null;
  available_at: string | null;
  last_error: string | null;
  last_error_at: string | null;
  minute_requests: number;
  minute_input_tokens: number;
  day_requests: number;
  limits: { rpm: number | null; tpm: number | null; rpd: number | null } | null;
  month_requests: number;
  month_failures: number;
  month_cost_usd: number;
  /** 1 сая токен тутамд USD. */
  price_input_usd: number | null;
  price_output_usd: number | null;
}

export interface LiveSubscriptionInfo {
  email: string;
  name: string;
  tier: LiveTier;
  /** Тухайн эрхийн дуусах хугацаа (Standard бол багцынх, Premium бол Premium-ийнх). */
  expires_at: string | null;
  /** Сургалт + Live-ийн Standard багц. */
  plan_expires_at: string | null;
}
