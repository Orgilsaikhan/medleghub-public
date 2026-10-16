"use client";

import {
  AlertTriangleIcon,
  CircleCheckIcon,
  CircleXIcon,
  FlaskConicalIcon,
  LoaderCircleIcon,
} from "lucide-react";
import { useState } from "react";

import { Diagnostics } from "@/components/learn/console-output";
import { mn } from "@/lib/i18n/mn";
import { firstDifference, type TestCaseResult } from "@/lib/sandbox/grader";
import type { LessonTestCase } from "@/lib/types/api";
import { cn } from "@/lib/utils";

export interface TestRunState {
  /** Ажиллуулалт бүрд шинэ — сонгосон тестийг шинэчлэхэд `key` болно. */
  id: number;
  mode: "samples" | "all";
  /** `exercise.tests` доторх индексүүд — энэ удаа ажилласан тестүүд. */
  indices: number[];
  /** `indices`-тэй зэрэгцэнэ. `undefined` бол ажиллаж амжаагүй. */
  results: (TestCaseResult | undefined)[];
  status: "compiling" | "running" | "compile-error" | "failed" | "done";
  diagnostics?: string;
  message?: string;
  /** «Илгээх»-ийн эцсийн мэдэгдэл (хичээл дууссан эсэх гэх мэт). */
  note?: { tone: "success" | "info" | "error"; text: string };
}

interface TestResultsProps {
  tests: LessonTestCase[];
  run: TestRunState | null;
  /** Бэлтгэх үеийн текст — C/C++ хөрвүүлэх, Python ачаалах. */
  preparingText?: string;
  /** Тест ажиллуулаагүй үеийн заавар — анхдагч нь кодтой хичээлийнх. */
  emptyText?: string;
}

/**
 * «Тест ажиллуулах» / «Илгээх»-ийн үр дүн — HackerRank-ийн «Test case» хэсэг.
 *
 * Жишээ тестийн оролт, хүлээгдэж буй болон гарсан гаралтыг хажуу хажуугаар
 * харуулна. Нууц тестийн зөвхөн дүн харагдана.
 */
export function TestResults({ tests, run, preparingText, emptyText }: TestResultsProps) {
  if (!run) {
    return (
      <Shell muted>
        <span className="flex items-start gap-2">
          <FlaskConicalIcon className="mt-0.5 size-3.5 shrink-0" aria-hidden />
          {emptyText ?? mn.learn.exercise.empty}
        </span>
      </Shell>
    );
  }

  if (run.status === "compiling") {
    return <Shell muted>{preparingText ?? mn.learn.compiling}</Shell>;
  }

  if (run.status === "compile-error") {
    // Бусад төлөвтэй адил нэртэй log — дэлгэц уншигч алдааг дуудна.
    return (
      <div
        role="log"
        aria-live="polite"
        aria-label={mn.learn.exercise.tabTests}
        className="h-full overflow-auto p-3 font-mono text-[13px]"
      >
        <Diagnostics tone="error" title={mn.learn.compileErrorTitle} text={run.diagnostics ?? ""} />
      </div>
    );
  }

  if (run.status === "failed") {
    return (
      <Shell>
        <span className="text-destructive flex items-start gap-2">
          <AlertTriangleIcon className="mt-0.5 size-3.5 shrink-0" aria-hidden />
          {run.message}
        </span>
      </Shell>
    );
  }

  return <CaseList key={run.id} tests={tests} run={run} />;
}

function CaseList({ tests, run }: { tests: LessonTestCase[]; run: TestRunState }) {
  const finished = run.results.filter((result) => result !== undefined);
  const passed = finished.filter((result) => result.status === "passed").length;
  const total = run.indices.length;
  const done = run.status === "done";
  const allPassed = done && passed === total;

  // Анх эхний унасан тестийг нээнэ — сурагч хаана алдсанаа шууд харна.
  const [picked, setPicked] = useState<number | null>(null);
  const firstFailed = run.results.findIndex(
    (result) => result !== undefined && result.status !== "passed",
  );
  const selected = picked ?? (firstFailed === -1 ? 0 : firstFailed);

  // Жишээ ба нууц тестийг тус тусад нь дугаарлана.
  let sampleCount = 0;
  let hiddenCount = 0;
  const labels = run.indices.map((testIndex) =>
    tests[testIndex].sample
      ? mn.learn.exercise.sampleCase(++sampleCount)
      : mn.learn.exercise.hiddenCase(++hiddenCount),
  );

  const selectedTest = tests[run.indices[selected]];
  const selectedResult = run.results[selected];

  return (
    <div
      role="log"
      aria-live="polite"
      aria-label={mn.learn.exercise.tabTests}
      className="h-full overflow-auto p-3 text-sm"
    >
      <p
        className={cn(
          "flex items-center gap-2 font-medium",
          !done && "text-muted-foreground",
          done && (allPassed ? "text-success" : "text-destructive"),
        )}
      >
        {!done ? (
          <LoaderCircleIcon className="size-4 animate-spin" aria-hidden />
        ) : allPassed ? (
          <CircleCheckIcon className="size-4" aria-hidden />
        ) : (
          <CircleXIcon className="size-4" aria-hidden />
        )}
        {done
          ? mn.learn.exercise.summary(passed, total)
          : mn.learn.exercise.testingProgress(finished.length, total)}
      </p>

      {run.note && (
        <p
          className={cn(
            "mt-1 text-sm",
            run.note.tone === "success" && "text-success",
            run.note.tone === "error" && "text-destructive",
            run.note.tone === "info" && "text-muted-foreground",
          )}
        >
          {run.note.text}
        </p>
      )}

      <div
        className="mt-3 flex flex-wrap gap-1.5"
        role="group"
        aria-label={mn.learn.exercise.tabTests}
      >
        {labels.map((label, index) => {
          const result = run.results[index];
          return (
            <button
              key={index}
              type="button"
              onClick={() => setPicked(index)}
              aria-pressed={index === selected}
              className={cn(
                "flex items-center gap-1.5 rounded-md border px-2 py-1 text-xs font-medium transition-colors",
                "focus-visible:ring-ring focus-visible:ring-2 focus-visible:outline-none",
                index === selected ? "bg-muted border-foreground/20" : "hover:bg-muted/60",
              )}
            >
              <StatusIcon result={result} />
              {label}
            </button>
          );
        })}
      </div>

      {selectedTest && <CaseDetail test={selectedTest} result={selectedResult} />}
    </div>
  );
}

function StatusIcon({ result }: { result: TestCaseResult | undefined }) {
  if (!result) {
    return <LoaderCircleIcon className="text-muted-foreground size-3.5 animate-spin" aria-hidden />;
  }
  return result.status === "passed" ? (
    <CircleCheckIcon
      className="text-success size-3.5"
      aria-label={mn.learn.exercise.status.passed}
    />
  ) : (
    <CircleXIcon
      className="text-destructive size-3.5"
      aria-label={mn.learn.exercise.status[result.status]}
    />
  );
}

function CaseDetail({
  test,
  result,
}: {
  test: LessonTestCase;
  result: TestCaseResult | undefined;
}) {
  if (!result) {
    return <p className="text-muted-foreground mt-3 text-xs">{mn.learn.exercise.testing}</p>;
  }

  const failed = result.status !== "passed";

  return (
    <div className="mt-3 space-y-3">
      <p className={cn("text-xs font-semibold", failed ? "text-destructive" : "text-success")}>
        {mn.learn.exercise.status[result.status]}
        {result.status === "wrong-answer" && test.sample && (
          <span className="text-muted-foreground ml-2 font-normal">
            {diffHint(result.actual, test.expected_output)}
          </span>
        )}
      </p>

      {result.status === "runtime-error" && result.message && (
        <p className="text-destructive font-mono text-[13px] break-words whitespace-pre-wrap">
          {result.message}
        </p>
      )}
      {result.status === "timeout" && (
        <p className="text-destructive text-xs">{mn.learn.timeout}</p>
      )}

      {test.sample ? (
        <div className="grid gap-3 lg:grid-cols-3">
          <Block
            title={mn.learn.exercise.input}
            text={test.stdin}
            empty={mn.learn.exercise.noInput}
          />
          <Block
            title={mn.learn.exercise.yourOutput}
            text={result.actual}
            empty={mn.learn.exercise.emptyOutput}
            tone={failed ? "error" : undefined}
          />
          <Block
            title={mn.learn.exercise.expectedOutput}
            text={test.expected_output}
            empty={mn.learn.exercise.emptyOutput}
          />
        </div>
      ) : (
        failed && <p className="text-muted-foreground text-xs">{mn.learn.exercise.hiddenDetails}</p>
      )}

      {!!result.exitCode && (
        <p className="text-muted-foreground text-xs italic">{mn.learn.exitCode(result.exitCode)}</p>
      )}
    </div>
  );
}

function diffHint(actual: string, expected: string): string {
  const diff = firstDifference(actual, expected);
  if (!diff) return "";
  if (diff.actual === null) return mn.learn.exercise.lineMissing(diff.line);
  if (diff.expected === null) return mn.learn.exercise.lineExtra(diff.line);
  return mn.learn.exercise.lineDiffers(diff.line);
}

function Block({
  title,
  text,
  empty,
  tone,
}: {
  title: string;
  text: string;
  empty: string;
  tone?: "error";
}) {
  const shown = text.replace(/\n+$/, "");
  return (
    <div className="min-w-0">
      <p className="text-muted-foreground mb-1 text-xs font-medium">{title}</p>
      {/* Урт мөр хэвтээгээр гүйлгэгдэнэ — гарын түлхүүрээр ч хүрнэ (WCAG 2.1.1). */}
      <pre
        tabIndex={0}
        className={cn(
          "bg-background overflow-x-auto rounded-md border px-2.5 py-2 font-mono text-[13px] leading-relaxed",
          "focus-visible:ring-ring focus-visible:ring-2 focus-visible:outline-none",
          tone === "error" && "border-destructive/40",
        )}
      >
        {shown || <span className="text-muted-foreground italic">{empty}</span>}
      </pre>
    </div>
  );
}

function Shell({ children, muted }: { children: React.ReactNode; muted?: boolean }) {
  return (
    <div className={cn("flex h-full items-start p-3 text-sm", muted && "text-muted-foreground")}>
      {children}
    </div>
  );
}
