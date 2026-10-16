/**
 * Дасгалын гаралт шалгагч — HackerRank-ийн адил програмын stdout-ийг
 * хүлээгдэж буй гаралттай харьцуулна.
 *
 * ХАРЬЦУУЛАХ ДҮРЭМ
 * ────────────────
 * - Зөвхөн stdout. stderr (`fprintf(stderr, …)`, `cerr`) тооцогдохгүй.
 * - Мөр бүрийн ТӨГСГӨЛИЙН зай, таб болон төгсгөлийн хоосон мөрүүдийг үл
 *   тооно — `printf("%d ", x)` гэх мэт нүдэнд үл харагдах зөрүүгээр сурагч
 *   унах ёсгүй. Бусад бүх тэмдэгт (мөрийн эхний зай, том жижиг үсэг) яг
 *   таарах ёстой.
 * - `main`-ийн буцаах код дүгнэлтэд ОРОХГҮЙ. Хичээлүүд буруу оролтод
 *   `return 1` хийхийг заадаг — түүнийг дагасан сурагч зөв гаралттай байхад
 *   унах ёсгүй. Кодыг зөвхөн мэдээлэл болгон харуулна.
 *
 * Энэ файл зөвхөн ТӨРЛИЙГ импортлодог (`import type`) — жишиг шийдлийг
 * шалгах Node скрипт (`scripts/verify-exercises.mjs`) ч мөн үүнийг ашиглана.
 * Ингэснээр сурагчийн хөтөч болон шалгагч ИЖИЛ дүрмээр дүгнэнэ.
 */

import type { RunResult } from "@/lib/sandbox/runner";
import type { LessonLanguage } from "@/lib/types/api";

/**
 * Дасгал (тест, «Илгээх») дэмждэг хэлнүүд. C/C++ нь `native-runner.ts`-ийн,
 * Python нь `python-runner.ts`-ийн тестийн горимоор ажиллана. React (`jsx`)
 * нь өөрийн DOM тесттэй — `lib/sandbox/react/runner.ts`.
 */
export function supportsExercises(language: LessonLanguage): boolean {
  return (
    language === "c" ||
    language === "cpp" ||
    language === "python" ||
    language === "javascript" ||
    language === "jsx"
  );
}

export type TestStatus = "passed" | "wrong-answer" | "runtime-error" | "timeout" | "output-limit";

export interface TestCaseResult {
  status: TestStatus;
  /** Хэвийн болгосон stdout. */
  actual: string;
  /** Ажиллах үеийн алдааны тайлбар (`runtime-error` үед). Python-д traceback. */
  message?: string;
  exitCode?: number;
  durationMs: number;
}

export interface OutputDifference {
  /** 1-ээс эхэлсэн мөрийн дугаар. */
  line: number;
  /** `null` бол тэр мөр огт байхгүй. */
  actual: string | null;
  expected: string | null;
}

export function normalizeOutput(text: string): string {
  const lines = text
    .replace(/\r\n?/g, "\n")
    .split("\n")
    .map((line) => line.replace(/[ \t]+$/, ""));
  while (lines.length > 0 && lines[lines.length - 1] === "") lines.pop();
  return lines.join("\n");
}

/** Worker-ийн мөрүүдээс stdout-ийг сэргээнэ. stderr (`error`) орохгүй. */
export function stdoutOf(result: RunResult): string {
  return result.entries
    .filter((entry) => entry.level === "log")
    .map((entry) => entry.text)
    .join("\n");
}

export function gradeRun(result: RunResult, expectedOutput: string): TestCaseResult {
  const actual = normalizeOutput(stdoutOf(result));
  const base = { actual, exitCode: result.exitCode, durationMs: result.durationMs };

  if (result.timedOut) return { ...base, status: "timeout" };
  if (result.error) {
    // Python-ий traceback нь аль мөрөнд алдсаныг заадаг — хамгийн хэрэгтэй мэдээлэл.
    return {
      ...base,
      status: "runtime-error",
      message: result.error.traceback ?? result.error.message,
    };
  }
  if (result.truncated) return { ...base, status: "output-limit" };
  if (actual !== normalizeOutput(expectedOutput)) return { ...base, status: "wrong-answer" };
  return { ...base, status: "passed" };
}

/** Эхний зөрүүтэй мөр — сурагчид «хаана буруу байна» гэдгийг заана. */
export function firstDifference(actual: string, expected: string): OutputDifference | null {
  const a = normalizeOutput(actual).split("\n");
  const b = normalizeOutput(expected).split("\n");
  const length = Math.max(a.length, b.length);
  for (let i = 0; i < length; i++) {
    if (a[i] !== b[i]) {
      return { line: i + 1, actual: a[i] ?? null, expected: b[i] ?? null };
    }
  }
  return null;
}
