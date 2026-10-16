/**
 * Хэрэглэгчийн Python кодыг хөтөч дотор ажиллуулах.
 *
 * Pyodide нь CPython-ийг WebAssembly болгож хөрвүүлсэн хувилбар. Сурагчийн
 * код нь сервер рүү ОГТ явахгүй — бүх зүйл өөрийнх нь хөтөч дээр болно.
 *
 * ЯАГААД WORKER-ЫГ ХАДГАЛДАГ ВЭ
 * ─────────────────────────────
 * Pyodide-ийг ачаалахад хэдэн секунд шаардагдана. JavaScript-ийн worker шиг
 * ажиллуулах бүрд шинээр үүсгэвэл хичээл бүр тэвчишгүй удаан болно. Тиймээс
 * нэг worker-ыг үүсгээд хадгална. Зөвхөн хугацаа хэтэрсэн үед л `terminate()`
 * дуудаж, дараагийн ажиллуулалтад дахин үүсгэнэ.
 */

import { gradeRun, type TestCaseResult } from "@/lib/sandbox/grader";
import { PYTHON_WORKER_SOURCE } from "@/lib/sandbox/python-worker-source";
import { DEFAULT_TIMEOUT_MS, type ConsoleEntry, type RunResult } from "@/lib/sandbox/runner";
import type { LessonTestCase } from "@/lib/types/api";

/** Ачаалах хугацааны дээд хязгаар — сүлжээ удаан бол ч мөнхөд хүлээхгүй. */
const LOAD_TIMEOUT_MS = 120_000;

interface RunMessage {
  type: "result";
  id: number;
  entries: ConsoleEntry[];
  truncated: boolean;
  error: { name: string; message: string; traceback?: string } | null;
}

interface ReadyMessage {
  type: "ready" | "init-error";
  message?: string;
}

type WorkerMessage = RunMessage | ReadyMessage;

let worker: Worker | null = null;
let ready: Promise<void> | null = null;
let blobUrl: string | null = null;
let nextId = 1;

const pending = new Map<number, (message: RunMessage) => void>();

function workerUrl(): string {
  if (!blobUrl) {
    blobUrl = URL.createObjectURL(new Blob([PYTHON_WORKER_SOURCE], { type: "text/javascript" }));
  }
  return blobUrl;
}

/** Хүлээгдэж буй бүх хүсэлтийг тодорхой үр дүнгээр хаана. */
function rejectPending(result: Omit<RunMessage, "type" | "id">) {
  for (const [id, resolve] of pending) {
    resolve({ type: "result", id, ...result });
  }
  pending.clear();
}

function teardown() {
  worker?.terminate();
  worker = null;
  ready = null;
}

/**
 * Worker-ыг үүсгэж, Pyodide ачаалж дуусахыг хүлээнэ.
 *
 * Давхар дуудагдвал нэг л worker үүснэ — `ready` промисыг дахин ашиглана.
 */
function start(): Promise<void> {
  if (ready) return ready;

  ready = new Promise<void>((resolve, reject) => {
    let instance: Worker;
    try {
      // Pyodide нь ES module тул classic worker дэмжихгүй.
      instance = new Worker(workerUrl(), { type: "module" });
    } catch {
      reject(new Error("Хөтөч энэ боломжийг дэмжихгүй байна."));
      return;
    }

    worker = instance;

    const timer = setTimeout(() => {
      teardown();
      reject(new Error("Python ачаалахад хэт удлаа. Холболтоо шалгана уу."));
    }, LOAD_TIMEOUT_MS);

    instance.onmessage = (event: MessageEvent<WorkerMessage>) => {
      const data = event.data;

      if (data.type === "ready") {
        clearTimeout(timer);
        resolve();
        return;
      }

      if (data.type === "init-error") {
        clearTimeout(timer);
        teardown();
        reject(new Error(data.message || "Python ачаалж чадсангүй."));
        return;
      }

      if (data.type === "result") {
        const resolveRun = pending.get(data.id);
        pending.delete(data.id);
        resolveRun?.(data);
      }
    };

    instance.onerror = (event) => {
      event.preventDefault();
      clearTimeout(timer);
      teardown();
      reject(new Error(event.message || "Python ачаалж чадсангүй."));
    };

    instance.postMessage({
      type: "init",
      indexURL: new URL("/pyodide/", location.origin).href,
    });
  });

  // Амжилтгүй болсон промисыг хадгалахгүй — дараагийн оролдлого шинээр эхэлнэ.
  ready.catch(() => {
    ready = null;
  });

  return ready;
}

/**
 * Pyodide-ийг урьдчилан ачаална.
 *
 * Хичээлийн хуудас нээгдэх үед дуудагдана: сурагч тайлбараа уншиж байх зуур
 * татаж дуусна. Ингэснээр "Ажиллуулах" дарахад хүлээх шаардлагагүй.
 */
export function preloadPython(): Promise<void> {
  return start();
}

export interface PythonRunOptions {
  /** `input()`-д өгөх мөрүүд. Хоосон бол `input()` нь EOFError өгнө. */
  stdin?: string;
  timeoutMs?: number;
}

type RunMode = "run" | "test";

function loadFailure(error: unknown, startedAt: number): RunResult {
  return {
    entries: [],
    truncated: false,
    error: {
      name: "SandboxError",
      message: error instanceof Error ? error.message : "Python ачаалж чадсангүй.",
    },
    timedOut: false,
    durationMs: Math.round(performance.now() - startedAt),
  };
}

export async function runPython(
  code: string,
  { stdin = "", timeoutMs = DEFAULT_TIMEOUT_MS }: PythonRunOptions = {},
): Promise<RunResult> {
  const startedAt = performance.now();
  try {
    await start();
  } catch (error) {
    return loadFailure(error, startedAt);
  }
  return execute(code, stdin, timeoutMs, "run");
}

// --- Дасгалын тест -------------------------------------------------------------

export type PythonTestOutcome =
  { kind: "failed"; message: string } | { kind: "ran"; results: TestCaseResult[] };

export interface PythonTestOptions {
  /** Pyodide ачаалж дуусч тест эхлэх мөч. */
  onReady?: () => void;
  onResult?: (index: number, result: TestCaseResult) => void;
  timeoutMs?: number;
}

/**
 * Дасгалын тестүүдийг ажиллуулж дүгнэнэ.
 *
 * Тест бүр цэвэр нэрийн талбарт ажиллаж (`mode: "test"`), `input()`-ийн
 * асуулт гаралтад орохгүй. Хугацаа хэтэрвэл worker шинээр ачаалагдана —
 * дараагийн тест түүнийг хүлээнэ.
 */
export async function runPythonTests(
  code: string,
  tests: readonly LessonTestCase[],
  { onReady, onResult, timeoutMs = DEFAULT_TIMEOUT_MS }: PythonTestOptions = {},
): Promise<PythonTestOutcome> {
  try {
    await start();
  } catch (error) {
    return {
      kind: "failed",
      message: error instanceof Error ? error.message : "Python ачаалж чадсангүй.",
    };
  }
  onReady?.();

  const results: TestCaseResult[] = [];
  for (const [index, test] of tests.entries()) {
    let run: RunResult;
    try {
      await start();
      run = await execute(code, test.stdin, timeoutMs, "test");
    } catch (error) {
      run = loadFailure(error, performance.now());
    }
    const result = gradeRun(run, test.expected_output);
    results.push(result);
    onResult?.(index, result);
  }
  return { kind: "ran", results };
}

function execute(
  code: string,
  stdin: string,
  timeoutMs: number,
  mode: RunMode,
): Promise<RunResult> {
  const instance = worker;
  if (!instance) {
    return Promise.resolve({
      entries: [],
      truncated: false,
      error: { name: "SandboxError", message: "Python ачаалж чадсангүй." },
      timedOut: false,
      durationMs: 0,
    });
  }

  const id = nextId++;
  // Хугацааг ачаалсны ДАРАА л хэмжинэ — татах хугацаа кодын гүйцэтгэлд ороогүй.
  const runStartedAt = performance.now();

  return new Promise<RunResult>((resolve) => {
    let settled = false;

    const finish = (message: Omit<RunMessage, "type" | "id">, timedOut: boolean) => {
      if (settled) return;
      settled = true;
      clearTimeout(timer);
      resolve({
        entries: message.entries,
        truncated: message.truncated,
        error: message.error,
        timedOut,
        durationMs: Math.round(performance.now() - runStartedAt),
      });
    };

    const timer = setTimeout(() => {
      // SharedArrayBuffer байхгүй тул зогсоох цорын ганц арга нь terminate.
      // Дараагийн ажиллуулалт worker-ыг шинээр үүсгэнэ.
      pending.delete(id);
      rejectPending({ entries: [], truncated: false, error: null });
      teardown();
      finish({ entries: [], truncated: false, error: null }, true);
    }, timeoutMs);

    pending.set(id, (message) => finish(message, false));
    instance.postMessage({ type: "run", id, code, stdin, mode });
  });
}
