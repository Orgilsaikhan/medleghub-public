/**
 * C/C++ кодыг серверт хөрвүүлж WebAssembly модуль авна.
 *
 * Бусад API дуудлагаас ялгаатай нь амжилттай хариу нь JSON биш,
 * `application/wasm` байт. Тиймээс `apiFetch`-ийн оронд `fetch`-ийг шууд
 * ашиглана.
 *
 * Сервер кодыг ЗӨВХӨН хөрвүүлнэ. Ажиллуулах нь сурагчийн browser доторх
 * Web Worker-т болно.
 */

import { ApiError, apiBaseUrl, NETWORK_ERROR_MESSAGE, toApiError } from "@/lib/api/client";

export type NativeLanguage = "c" | "cpp";

/**
 * Хөрвүүлэлтийн үр дүн.
 *
 * `compile-error` нь сурагчийн кодонд алдаа байгааг хэлнэ — хөрвүүлэгчийн
 * мессежийг бүтнээр нь харуулах ёстой.
 */
export type CompileOutcome =
  { kind: "compiled"; wasm: ArrayBuffer } | { kind: "compile-error"; diagnostics: string };

interface CompileErrorBody {
  detail?: { code?: string; diagnostics?: unknown };
}

/**
 * Хөрвүүлэлтийн алдааг бусад алдаанаас тусад нь буцаана.
 *
 * Хөрвүүлэлтийн алдаа нь сүлжээ эсвэл эрхийн алдаа шиг «амжилтгүй хүсэлт»
 * биш — сурагчийн кодын тухай хэвийн хариу. Тиймээс шидэхгүй, үр дүн болгож
 * буцаана. Бусад бүх алдаа `ApiError` болж шидэгдэнэ.
 */
export async function compileNative(
  language: NativeLanguage,
  source: string,
  signal?: AbortSignal,
): Promise<CompileOutcome> {
  let response: Response;
  try {
    response = await fetch(`${apiBaseUrl}/compile`, {
      method: "POST",
      credentials: "include",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ language, source }),
      signal,
    });
  } catch (error) {
    // Шинэ «Ажиллуулах» дарсан тул өмнөх хүсэлтийг цуцалсан — алдаа биш.
    if (signal?.aborted) throw error;
    throw new ApiError(0, "NETWORK_ERROR", NETWORK_ERROR_MESSAGE);
  }

  if (response.ok) {
    return { kind: "compiled", wasm: await response.arrayBuffer() };
  }

  if (response.status === 422) {
    // `toApiError` биеийг уншдаг тул хуулбараас нь шалгана.
    const body = (await response
      .clone()
      .json()
      .catch(() => null)) as CompileErrorBody | null;

    if (body?.detail?.code === "COMPILE_ERROR") {
      return { kind: "compile-error", diagnostics: String(body.detail.diagnostics ?? "") };
    }
  }

  throw await toApiError(response);
}
