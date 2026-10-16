/**
 * Хэрэглэгчийн JavaScript-ийг Web Worker дотор аюулгүй ажиллуулах.
 *
 * Гол thread нь Worker-ийг үүсгэж, хугацаа хэмжиж, хэтэрвэл `terminate()`
 * дуудна — төгсгөлгүй давталт хуудсыг зогсоохгүй.
 */

import { gradeRun, type TestCaseResult } from "@/lib/sandbox/grader";
import { WORKER_SOURCE } from "@/lib/sandbox/worker-source";
import type { LessonTestCase } from "@/lib/types/api";

export const DEFAULT_TIMEOUT_MS = 3000;

export type ConsoleLevel = "log" | "info" | "warn" | "error";

export interface ConsoleEntry {
  level: ConsoleLevel;
  text: string;
  /** SQL хүснэгт — мөрийг ороохгүй, хажуу тийш гүйлгэнэ. */
  preformatted?: boolean;
}

export interface RunError {
  name: string;
  message: string;
  /**
   * Python-ий бүтэн traceback (зөвхөн Python хичээлд).
   *
   * JavaScript нь `error.message` дотроо байрлалаа агуулдаг тул нэмэлт мөр
   * шаардлагагүй. Python нь харин аль мөрөнд алдсаныг зөвхөн traceback-д
   * бичдэг — сурагчид энэ нь хамгийн хэрэгтэй мэдээлэл.
   */
  traceback?: string;
}

export interface RunResult {
  entries: ConsoleEntry[];
  /** Гаралт хэт урт болж таслагдсан эсэх. */
  truncated: boolean;
  /** Кодын ажиллагааны алдаа (гарсан бол). */
  error: RunError | null;
  /** Хугацаа хэтэрснээс болж зогссон эсэх. */
  timedOut: boolean;
  durationMs: number;
  /** C/C++: хөрвүүлэлтийн алдааны мессеж. Байвал програм огт ажиллаагүй. */
  compileError?: string;
  /** C/C++: хөрвүүлэгчийн анхааруулга (`-Wall`). Програм ажилласан. */
  warnings?: string;
  /** C/C++: `main`-ийн буцаасан (эсвэл `exit`-д өгсөн) код. */
  exitCode?: number;
  /** C/C++: програм оролт хүлээсэн ч «Оролт» хоосон байсан эсвэл дууссан. */
  needsInput?: boolean;
}

interface WorkerMessage {
  type: "result";
  entries: ConsoleEntry[];
  truncated: boolean;
  error: RunError | null;
}

let blobUrl: string | null = null;

/** Worker-ийн эх кодыг нэг л удаа blob болгоно. */
function getWorkerUrl(): string {
  if (!blobUrl) {
    blobUrl = URL.createObjectURL(new Blob([WORKER_SOURCE], { type: "text/javascript" }));
  }
  return blobUrl;
}

export interface JavaScriptRunOptions {
  /** `prompt()` дуудагдах бүрд дараагийн мөрийг өгнө. */
  stdin?: string;
  timeoutMs?: number;
}

export function runJavaScript(
  code: string,
  { stdin = "", timeoutMs = DEFAULT_TIMEOUT_MS }: JavaScriptRunOptions = {},
): Promise<RunResult> {
  const startedAt = performance.now();

  return new Promise<RunResult>((resolve) => {
    let worker: Worker;
    try {
      worker = new Worker(getWorkerUrl());
    } catch {
      resolve({
        entries: [],
        truncated: false,
        error: { name: "SandboxError", message: "Хөтөч энэ боломжийг дэмжихгүй байна." },
        timedOut: false,
        durationMs: 0,
      });
      return;
    }

    let settled = false;

    const finish = (result: Omit<RunResult, "durationMs">) => {
      if (settled) return;
      settled = true;
      clearTimeout(timer);
      worker.terminate();
      resolve({ ...result, durationMs: Math.round(performance.now() - startedAt) });
    };

    const timer = setTimeout(
      () => finish({ entries: [], truncated: false, error: null, timedOut: true }),
      timeoutMs,
    );

    worker.onmessage = (event: MessageEvent<WorkerMessage>) => {
      const { entries, truncated, error } = event.data;
      finish({ entries, truncated, error, timedOut: false });
    };

    worker.onerror = (event) => {
      // Syntax алдааг worker ачаалагдахад л илрүүлж болно.
      event.preventDefault();
      finish({
        entries: [],
        truncated: false,
        error: { name: "Error", message: event.message || "Кодыг ажиллуулж чадсангүй." },
        timedOut: false,
      });
    };

    worker.postMessage({ code, stdin });
  });
}

export type JavaScriptTestOutcome = { kind: "ran"; results: TestCaseResult[] };

/**
 * Дасгалын тестүүд — тест бүр шинэ worker-т (өмнөх тестийн хувьсагч үлдэхгүй),
 * `prompt()` нь тестийн оролтын мөрүүдийг дарааллаар өгнө. Гаралт нь зөвхөн
 * `console.log` — `prompt()`-ийн асуулт, `console.info/warn/error` тооцогдохгүй.
 */
export async function runJavaScriptTests(
  code: string,
  tests: readonly LessonTestCase[],
  {
    onResult,
    timeoutMs = DEFAULT_TIMEOUT_MS,
  }: { onResult?: (index: number, result: TestCaseResult) => void; timeoutMs?: number } = {},
): Promise<JavaScriptTestOutcome> {
  const results: TestCaseResult[] = [];
  for (const [index, test] of tests.entries()) {
    const result = gradeRun(
      await runJavaScript(code, { stdin: test.stdin, timeoutMs }),
      test.expected_output,
    );
    results.push(result);
    onResult?.(index, result);
  }
  return { kind: "ran", results };
}
