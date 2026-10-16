/**
 * Backend API-тай харилцах нэгдсэн fetch wrapper.
 *
 * - Нэвтрэлт нь httpOnly cookie-гоор явдаг тул `credentials: "include"` заавал.
 * - Бүх алдааг `ApiError` болгон нэгтгэнэ — UI нь монгол мессежийг шууд харуулна.
 */

const PUBLIC_BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1";

/** Server Component-ээс дуудахад дотоод хаяг ашиглаж болно. */
const SERVER_BASE = process.env.API_INTERNAL_URL || PUBLIC_BASE;

export const apiBaseUrl = typeof window === "undefined" ? SERVER_BASE : PUBLIC_BASE;

export interface ApiFieldError {
  field: string;
  message: string;
}

export class ApiError extends Error {
  readonly status: number;
  readonly code: string;
  readonly fields: ApiFieldError[];

  constructor(status: number, code: string, message: string, fields: ApiFieldError[] = []) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.code = code;
    this.fields = fields;
  }

  get isUnauthorized(): boolean {
    return this.status === 401;
  }

  get isForbidden(): boolean {
    return this.status === 403;
  }

  get isNotFound(): boolean {
    return this.status === 404;
  }
}

export const NETWORK_ERROR_MESSAGE = "Сервертэй холбогдож чадсангүй. Дараа дахин оролдоно уу.";
const UNKNOWN_ERROR_MESSAGE = "Алдаа гарлаа. Дараа дахин оролдоно уу.";

interface ErrorBody {
  detail?: string | { code?: string; message?: string; fields?: ApiFieldError[] };
}

export async function toApiError(response: Response): Promise<ApiError> {
  let body: ErrorBody = {};
  try {
    body = (await response.json()) as ErrorBody;
  } catch {
    // Хариу JSON биш байж болно (жишээ нь gateway-ийн HTML алдаа).
  }

  const detail = body.detail;
  if (detail && typeof detail === "object") {
    return new ApiError(
      response.status,
      detail.code ?? "UNKNOWN",
      detail.message ?? UNKNOWN_ERROR_MESSAGE,
      detail.fields ?? [],
    );
  }
  return new ApiError(
    response.status,
    "UNKNOWN",
    typeof detail === "string" ? detail : UNKNOWN_ERROR_MESSAGE,
  );
}

export interface RequestOptions extends Omit<RequestInit, "body" | "method"> {
  method?: "GET" | "POST" | "PUT" | "PATCH" | "DELETE";
  /** JSON болгож хувиргах биет. */
  json?: unknown;
  /** Файл илгээх (`multipart/form-data`). Content-Type-ийг хөтөч boundary-тай нь тавина. */
  form?: FormData;
  /** Query string параметрүүд. `undefined`/`null`/хоосон утгууд орхигдоно. */
  query?: object;
}

function buildUrl(path: string, query?: RequestOptions["query"]): string {
  const url = `${apiBaseUrl}${path}`;
  if (!query) return url;

  const params = new URLSearchParams();
  for (const [key, value] of Object.entries(query)) {
    if (value === undefined || value === null || value === "") continue;
    if (typeof value === "string" || typeof value === "number" || typeof value === "boolean") {
      params.set(key, String(value));
    }
  }
  const search = params.toString();
  return search ? `${url}?${search}` : url;
}

export async function apiFetch<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const { method = "GET", json, form, query, headers, ...rest } = options;

  let response: Response;
  try {
    response = await fetch(buildUrl(path, query), {
      ...rest,
      method,
      credentials: "include",
      headers: {
        ...(json !== undefined ? { "Content-Type": "application/json" } : {}),
        ...headers,
      },
      body: form ?? (json !== undefined ? JSON.stringify(json) : undefined),
    });
  } catch {
    throw new ApiError(0, "NETWORK_ERROR", NETWORK_ERROR_MESSAGE);
  }

  if (!response.ok) {
    throw await toApiError(response);
  }
  if (response.status === 204) {
    return undefined as T;
  }
  return (await response.json()) as T;
}
