/** MedlegHub Live (AI Study). Бүх endpoint нэвтрэлт шаардана (`/live/config`-оос бусад). */

import {
  ApiError,
  apiBaseUrl,
  apiFetch,
  NETWORK_ERROR_MESSAGE,
  toApiError,
} from "@/lib/api/client";
import type {
  LiveAdminOverview,
  LiveAnswerResult,
  LiveAttempt,
  LiveAttemptResult,
  LiveCard,
  LiveCardRating,
  LiveConfig,
  LiveGeneration,
  LiveGenerationKind,
  LiveMaterialDetail,
  LiveMaterialSummary,
  LiveModelStatus,
  LiveSubscriptionInfo,
} from "@/lib/types/live";

const id = encodeURIComponent;

/** Энэ хэрэглэгчид Live нээлттэй эсэх, хязгаар, энэ сарын хэрэглээ. Зочинд ч хариулна. */
export function getLiveConfig(): Promise<LiveConfig> {
  return apiFetch<LiveConfig>("/live/config");
}

export function listMaterials(): Promise<LiveMaterialSummary[]> {
  return apiFetch<LiveMaterialSummary[]>("/live/materials");
}

export interface CreateMaterialInput {
  filename: string;
  size_bytes: number;
  /** Хоосон бол файлын нэрээс. */
  title?: string;
  /** Материалыг ашиглах эрхтэй, AI боловсруулалтыг зөвшөөрсөн. Заавал `true`. */
}

/** Мета + эрх, хязгаарыг шалгана. Дараа нь `uploadMaterialContent`. */
export function createMaterial(input: CreateMaterialInput): Promise<LiveMaterialSummary> {
  return apiFetch<LiveMaterialSummary>("/live/materials", { method: "POST", json: input });
}

/**
 * Файлын агуулгыг (raw body) илгээнэ — явцыг `onProgress`-оор (0–1).
 * `fetch` явц мэдээлдэггүй тул XHR. Амжилттай бол материал `queued` болно.
 */
export function uploadMaterialContent(
  materialId: string,
  file: File,
  onProgress?: (fraction: number) => void,
  signal?: AbortSignal,
): Promise<LiveMaterialSummary> {
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();
    xhr.open("PUT", `${apiBaseUrl}/live/materials/${id(materialId)}/content`);
    xhr.withCredentials = true;
    xhr.setRequestHeader("Content-Type", "application/octet-stream");
    xhr.upload.onprogress = (event) => {
      if (event.lengthComputable) onProgress?.(event.loaded / event.total);
    };
    xhr.onload = () => {
      const response = new Response(xhr.responseText || null, {
        status: xhr.status,
        headers: { "Content-Type": "application/json" },
      });
      if (xhr.status >= 200 && xhr.status < 300) {
        resolve(response.json() as Promise<LiveMaterialSummary>);
      } else {
        void toApiError(response).then(reject);
      }
    };
    xhr.onerror = () => reject(new ApiError(0, "NETWORK_ERROR", NETWORK_ERROR_MESSAGE));
    xhr.onabort = () => reject(new ApiError(0, "ABORTED", NETWORK_ERROR_MESSAGE));
    signal?.addEventListener("abort", () => xhr.abort(), { once: true });
    xhr.send(file);
  });
}

export function getMaterial(materialId: string): Promise<LiveMaterialDetail> {
  return apiFetch<LiveMaterialDetail>(`/live/materials/${id(materialId)}`);
}

export function renameMaterial(materialId: string, title: string): Promise<LiveMaterialSummary> {
  return apiFetch<LiveMaterialSummary>(`/live/materials/${id(materialId)}`, {
    method: "PATCH",
    json: { title },
  });
}

export function deleteMaterial(materialId: string): Promise<void> {
  return apiFetch<void>(`/live/materials/${id(materialId)}`, { method: "DELETE" });
}

/** Амжилтгүй болсон боловсруулалтыг дахин эхлүүлнэ. */
export function retryMaterial(materialId: string): Promise<LiveMaterialSummary> {
  return apiFetch<LiveMaterialSummary>(`/live/materials/${id(materialId)}/retry`, {
    method: "POST",
  });
}

export interface RequestGenerationInput {
  kind: LiveGenerationKind;
  /** `guide` үед заавал; `quiz` үед сэдвийн тест, `null` бол бүтэн тест; `exam` үед `null`. */
  topic_id?: string | null;
  /** `true` бол бэлэн байгааг орлуулж шинээр үүсгэнэ (AI хэрэглээнд тооцогдоно). */
  regenerate?: boolean;
}

/**
 * Заавар, тест, шалгалтын таамгийг захиална. Бэлэн (эсвэл үүсгэж байгаа) нь
 * байвал түүнийг буцаана — AI-г дахин дуудахгүй. 202.
 */
export function requestGeneration(
  materialId: string,
  input: RequestGenerationInput,
): Promise<LiveGeneration> {
  return apiFetch<LiveGeneration>(`/live/materials/${id(materialId)}/generations`, {
    method: "POST",
    json: input,
  });
}

export function getGeneration(generationId: string): Promise<LiveGeneration> {
  return apiFetch<LiveGeneration>(`/live/generations/${id(generationId)}`);
}

/** Тестийн шинэ оролдлого. */
export function startAttempt(generationId: string): Promise<LiveAttempt> {
  return apiFetch<LiveAttempt>(`/live/generations/${id(generationId)}/attempts`, {
    method: "POST",
  });
}

export function answerQuestion(
  attemptId: string,
  questionId: string,
  choiceIndex: number,
): Promise<LiveAnswerResult> {
  return apiFetch<LiveAnswerResult>(`/live/attempts/${id(attemptId)}/answers`, {
    method: "POST",
    json: { question_id: questionId, choice_index: choiceIndex },
  });
}

/** Оролдлогыг дуусгаж, сэдэв тус бүрийн эзэмшлийг шинэчилнэ. */
export function finishAttempt(attemptId: string): Promise<LiveAttemptResult> {
  return apiFetch<LiveAttemptResult>(`/live/attempts/${id(attemptId)}/finish`, {
    method: "POST",
  });
}

/** Сэдвийн заавар уншсаныг тэмдэглэнэ (эзэмшилд +10). */
export function markGuideRead(topicId: string): Promise<void> {
  return apiFetch<void>(`/live/topics/${id(topicId)}/guide-read`, { method: "POST" });
}

export interface CardListParams {
  /** Өгвөл зөвхөн тэр сэдвийн картууд. */
  topic_id?: string;
  /** `due` — одоо давтах ёстой нь эхэнд, зөвхөн тэд; `all` — бүгд. */
  mode?: "due" | "all";
}

export function listCards(materialId: string, params: CardListParams = {}): Promise<LiveCard[]> {
  return apiFetch<LiveCard[]>(`/live/materials/${id(materialId)}/cards`, { query: params });
}

export function reviewCard(cardId: string, rating: LiveCardRating): Promise<LiveCard> {
  return apiFetch<LiveCard>(`/live/cards/${id(cardId)}/review`, {
    method: "POST",
    json: { rating },
  });
}

// --- Админ -------------------------------------------------------------------

export function getLiveAdminOverview(): Promise<LiveAdminOverview> {
  return apiFetch<LiveAdminOverview>("/live/admin/overview");
}

/** Загвар бүр хязгаарт хүрсэн (хөргөгдсөн) эсэх, хэрэглээ, энэ сарын зардал. */
export function getLiveModels(): Promise<LiveModelStatus[]> {
  return apiFetch<LiveModelStatus[]>("/live/admin/models");
}

export function lookupLiveSubscription(email: string): Promise<LiveSubscriptionInfo> {
  return apiFetch<LiveSubscriptionInfo>("/live/admin/subscriptions/lookup", {
    method: "POST",
    json: { email },
  });
}

export interface GrantLiveInput {
  email: string;
  /** 1–24 сар. Идэвхтэй Premium байвал түүний дуусах өдрөөс сунгана. */
  months: number;
  note?: string;
}

/**
 * Админ: Premium-ийг гараар олгоно. Standard багц Premium дуусахаас өмнө дуусах бол
 * түүнийг ч мөн өдөр хүртэл сунгана (Premium = Standard + илүү AI).
 */
export function grantLiveSubscription(input: GrantLiveInput): Promise<LiveSubscriptionInfo> {
  return apiFetch<LiveSubscriptionInfo>("/live/admin/subscriptions", {
    method: "POST",
    json: input,
  });
}
