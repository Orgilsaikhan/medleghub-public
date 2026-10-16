/**
 * MySQL хичээлийн кодыг ажиллуулж, үр дүнг console-ийн хэлбэрт оруулна.
 *
 * Хүснэгтийг `mysql` CLI шиг хүрээтэй текстээр харуулна — хичээлүүд болон
 * сурагчийн дараа ашиглах терминал ийм харагддаг:
 *
 *   +----------+--------------+
 *   | baraa_id | ner          |
 *   +----------+--------------+
 *   |        1 | Ухаалаг утас |
 *   +----------+--------------+
 *   1 мөр (0.00 сек)
 */

import { ApiError } from "@/lib/api/client";
import { runSqlRequest, type SqlResult, type SqlRunResponse } from "@/lib/api/sql";
import { mn } from "@/lib/i18n/mn";
import type { ConsoleEntry, RunError, RunResult } from "@/lib/sandbox/runner";

const NUMBER = /^-?\d+(\.\d+)?(e[+-]?\d+)?$/i;

/** Тэмдэгтийн тоо — кирилл үсэг нэг байрлал эзэлнэ. */
function width(text: string): number {
  return [...text].length;
}

function pad(text: string, size: number, alignRight: boolean): string {
  const fill = " ".repeat(Math.max(0, size - width(text)));
  return alignRight ? fill + text : text + fill;
}

/** Нүдийг нэг мөрөнд багтаана — мөр таслах тэмдэгт хүснэгтийг эвддэг. */
function displayCell(value: string | null): string {
  if (value === null) return "NULL";
  return value.replace(/\r?\n/g, "\\n").replace(/\t/g, "\\t");
}

export function formatTable(columns: string[], rows: (string | null)[][]): string {
  const cells = rows.map((row) => row.map(displayCell));
  const widths = columns.map((name, index) =>
    Math.max(width(name), ...cells.map((row) => width(row[index] ?? ""))),
  );
  // `mysql` CLI тоон баганыг баруун тийш зэрэгцүүлдэг.
  const numeric = columns.map(
    (_, index) =>
      rows.length > 0 && rows.every((row) => row[index] === null || NUMBER.test(row[index] ?? "")),
  );

  const border = `+${widths.map((size) => "-".repeat(size + 2)).join("+")}+`;
  const line = (values: string[], isHeader: boolean) =>
    `|${values
      .map((value, index) => ` ${pad(value, widths[index], !isHeader && numeric[index])} `)
      .join("|")}|`;

  return [
    border,
    line(columns, true),
    border,
    ...cells.map((row) => line(row, false)),
    border,
  ].join("\n");
}

function seconds(durationMs: number): string {
  return (durationMs / 1000).toFixed(2);
}

function resultEntries(result: SqlResult): ConsoleEntry[] {
  const entries: ConsoleEntry[] = [];
  const time = seconds(result.duration_ms);

  if (result.type === "ok") {
    entries.push({ level: "log", text: mn.learn.sql.ok(result.affected_rows, time) });
  } else if (result.rows.length === 0 && result.row_count === 0) {
    entries.push({ level: "log", text: mn.learn.sql.emptySet(time) });
  } else {
    entries.push({
      level: "log",
      text: formatTable(result.columns, result.rows),
      preformatted: true,
    });
    let summary: string;
    if (result.row_count === null) summary = mn.learn.sql.rowsTooMany(result.rows.length);
    else if (result.truncated)
      summary = mn.learn.sql.rowsTruncated(result.rows.length, result.row_count, time);
    else summary = mn.learn.sql.rows(result.row_count, time);
    entries.push({ level: result.truncated ? "warn" : "info", text: summary });
  }

  for (const warning of result.warnings) {
    entries.push({ level: "warn", text: mn.learn.sql.warning(warning.code, warning.message) });
  }
  return entries;
}

function toEntries(response: SqlRunResponse): ConsoleEntry[] {
  const entries = response.results.flatMap(resultEntries);
  if (response.timed_out) entries.push({ level: "error", text: mn.learn.sql.timeout });
  if (response.output_truncated)
    entries.push({ level: "warn", text: mn.learn.sql.outputTruncated });
  return entries;
}

function toError(response: SqlRunResponse): RunError | null {
  const error = response.error;
  if (!error) return null;

  const code = error.code === null ? null : `ERROR ${error.code}`;
  const name = code && error.sqlstate ? `${code} (${error.sqlstate})` : (code ?? "Алдаа");
  const where = error.line === null ? "" : `${mn.learn.sql.atLine(error.line)}: `;
  return { name, message: `${where}${error.message}` };
}

export async function runSql(source: string): Promise<RunResult> {
  const startedAt = performance.now();

  let response: SqlRunResponse;
  try {
    response = await runSqlRequest(source);
  } catch (error) {
    return {
      entries: [],
      truncated: false,
      error: {
        name: "Алдаа",
        message: error instanceof ApiError ? error.message : mn.learn.sql.failed,
      },
      timedOut: false,
      durationMs: Math.round(performance.now() - startedAt),
    };
  }

  return {
    entries: toEntries(response),
    truncated: false,
    error: toError(response),
    // SQL-ийн хугацааны мессеж нь давталтын тухай биш — `entries`-д тусад нь.
    timedOut: false,
    durationMs: response.duration_ms,
  };
}
