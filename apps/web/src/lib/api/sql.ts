/**
 * MySQL кодыг серверийн тусгаарлагдсан sandbox дээр ажиллуулна.
 *
 * C/C++-ээс ялгаатай нь код хөтөч дотор биш, СЕРВЕР дээр ажиллана — MySQL
 * хөтөчид ажилладаггүй. Ажиллагаа бүрийн өмнө сервер `delguur`, `nomiin_san`,
 * `medleg_hot` (мөрдөгчийн хэргүүд) жишээ сангуудтайгаа анхны төлөвт буцна.
 *
 * Сурагчийн SQL алдаа нь HTTP алдаа биш — `error` талбарт ирнэ.
 */

import { apiFetch } from "@/lib/api/client";

export interface SqlWarning {
  level: string;
  code: number;
  message: string;
}

/** `SELECT`, `SHOW`, `CALL` зэрэг мөр буцаадаг statement. */
export interface SqlRowsResult {
  type: "rows";
  /** Скрипт дэх statement-ийн эхлэх мөр. */
  line: number;
  columns: string[];
  /** NULL нь `null`, бусад нь текст. */
  rows: (string | null)[][];
  /** Хэт олон мөртэй тул бүгдийг уншаагүй бол `null`. */
  row_count: number | null;
  truncated: boolean;
  warnings: SqlWarning[];
  duration_ms: number;
}

/** `INSERT`, `CREATE`, `USE` зэрэг мөр буцаадаггүй statement. */
export interface SqlOkResult {
  type: "ok";
  line: number;
  affected_rows: number;
  warnings: SqlWarning[];
  duration_ms: number;
}

export type SqlResult = SqlRowsResult | SqlOkResult;

export interface SqlError {
  line: number | null;
  code: number | null;
  sqlstate: string | null;
  message: string;
}

export interface SqlRunResponse {
  results: SqlResult[];
  error: SqlError | null;
  timed_out: boolean;
  /** Гаралт хэт их тул үлдсэн statement-ийг ажиллуулаагүй. */
  output_truncated: boolean;
  duration_ms: number;
}

export function runSqlRequest(source: string, signal?: AbortSignal): Promise<SqlRunResponse> {
  return apiFetch<SqlRunResponse>("/sql/run", { method: "POST", json: { source }, signal });
}
