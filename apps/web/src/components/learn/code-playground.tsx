"use client";

import {
  ChevronDownIcon,
  ChevronUpIcon,
  FlaskConicalIcon,
  KeyboardIcon,
  PlayIcon,
  RotateCcwIcon,
  SendIcon,
  Trash2Icon,
} from "lucide-react";
import dynamic from "next/dynamic";
import { useCallback, useEffect, useRef, useState, useTransition } from "react";

import { ConsoleOutput } from "@/components/learn/console-output";
import { MotivationDialog } from "@/components/learn/motivation-dialog";
import { TestResults, type TestRunState } from "@/components/learn/test-results";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Skeleton } from "@/components/ui/skeleton";
import { useCurrentUser } from "@/lib/hooks/use-auth";
import { languageLabels, mn } from "@/lib/i18n/mn";
import { MOTIVATION_AFTER_FAILS, MOTIVATIONS, pickIndex, type Motivation } from "@/lib/motivation";
import {
  isNativeLanguage,
  preloadNative,
  runNative,
  runNativeTests,
  type NativePhase,
} from "@/lib/sandbox/native-runner";
import { supportsExercises, type TestCaseResult } from "@/lib/sandbox/grader";
import { preloadPython, runPython, runPythonTests } from "@/lib/sandbox/python-runner";
import { runJavaScript, runJavaScriptTests, type RunResult } from "@/lib/sandbox/runner";
import { runSql } from "@/lib/sandbox/sql-runner";
import type { LessonExercise, LessonLanguage } from "@/lib/types/api";
import { cn } from "@/lib/utils";

/** Monaco нь хүнд сан — зөвхөн хичээлийн хуудсанд, зөвхөн browser дээр ачаална. */
const CodeEditor = dynamic(() => import("@/components/learn/code-editor"), {
  ssr: false,
  loading: () => <Skeleton className="h-full w-full rounded-none" />,
});

/**
 * Ажиллуулах боломжтой хэлүүд.
 *
 * C/C++ нь серверт хөрвүүлэгдээд хөтөч дотор ажиллана. MySQL нь серверийн
 * тусгаарлагдсан sandbox дээр ажиллана. SQL Server (`sql`)-ийн контейнер ARM
 * дээр ажилладаггүй тул ажиллуулахгүй. HTML/CSS нь энд ирэхгүй —
 * `HtmlWorkspace`-ийн «Хөтөч» дээр шууд харагдана.
 */
const RUNNABLE: ReadonlySet<LessonLanguage> = new Set<LessonLanguage>([
  "javascript",
  "python",
  "c",
  "cpp",
  "mysql",
]);

export type SubmitNote = TestRunState["note"];

interface CodePlaygroundProps {
  initialCode: string;
  language: LessonLanguage;
  /**
   * HackerRank маягийн дасгал. Байвал засварлагчийн доор «Тест ажиллуулах»,
   * «Илгээх» товч гарна. Одоогоор зөвхөн C/C++ — шалгагч нь тэдгээрийн
   * worker-ийг ашигладаг.
   */
  exercise?: LessonExercise | null;
  /**
   * «Илгээх»-ийн бүх тест давсны дараа дуудагдана — хичээлийг дуусгаад
   * сурагчид харуулах мэдэгдлийг буцаана.
   */
  onSubmitPassed?: () => Promise<SubmitNote>;
  /** Дасгалын товчнуудын зүүн талд — «Тусламж». */
  helpAction?: React.ReactNode;
}

type ConsoleTab = "console" | "tests";

/**
 * Засварлагч, ажиллуулагч, console-ийг холбосон хэсэг.
 *
 * Хичээл солигдоход дуудагч тал `key`-г солиж, энэ component-ийг цоо шинээр
 * үүсгэнэ — өмнөх код болон гаралт үлдэхгүй.
 */
export function CodePlayground({
  initialCode,
  language,
  exercise,
  onSubmitPassed,
  helpAction,
}: CodePlaygroundProps) {
  const [code, setCode] = useState(initialCode);
  // Дасгалтай бол «Оролт»-ыг эхний жишээгээр бөглөнө — HackerRank-ийн
  // «custom input» шиг. Сурагч өөрчилж «Код ажиллуулах»-аар туршина.
  const [stdin, setStdin] = useState(
    () => exercise?.tests.find((test) => test.sample)?.stdin ?? "",
  );
  const [showStdin, setShowStdin] = useState(false);
  const [result, setResult] = useState<RunResult | null>(null);
  const [phase, setPhase] = useState<NativePhase | null>(null);
  const [isRunning, startRun] = useTransition();
  // Дасгалтай хичээлд засварлагчид зай гаргаж, эхлээд эвхэнэ — ажиллуулах,
  // шалгах үед автоматаар нээгдэнэ.
  const [consoleOpen, setConsoleOpen] = useState(!exercise);
  const [confirmReset, setConfirmReset] = useState(false);
  const [consoleTab, setConsoleTab] = useState<ConsoleTab>("console");
  const [testRun, setTestRun] = useState<TestRunState | null>(null);
  const [isTesting, setIsTesting] = useState(false);
  const testRunId = useRef(0);

  // Тестэд дараалан унасан тоо — 3 хүрвэл урам өгөх үг харуулж, дахин тоолно.
  // Бүх тест давбал тэглэнэ. Хичээл солигдоход component шинээр үүснэ.
  const { user } = useCurrentUser();
  const showMotivation = user?.show_motivation ?? true;
  const failStreak = useRef(0);
  const lastMotivation = useRef<number | null>(null);
  const [motivation, setMotivation] = useState<Motivation | null>(null);

  const recordTestOutcome = useCallback(
    (passed: boolean) => {
      if (passed) {
        failStreak.current = 0;
        return;
      }
      failStreak.current += 1;
      if (failStreak.current < MOTIVATION_AFTER_FAILS) return;
      failStreak.current = 0;
      if (!showMotivation) return;
      const index = pickIndex(MOTIVATIONS.length, lastMotivation.current);
      lastMotivation.current = index;
      setMotivation(MOTIVATIONS[index]);
    },
    [showMotivation],
  );

  const runnable = RUNNABLE.has(language);
  const isPython = language === "python";
  const isNative = isNativeLanguage(language);
  const isSql = language === "mysql";
  const isJavaScript = language === "javascript";
  // `input()`, `scanf`, `cin`, `prompt()` — гараас уншдаг хэлүүд.
  const acceptsStdin = isPython || isNative || isJavaScript;
  const hasExercise = !!exercise && supportsExercises(language) && exercise.tests.length > 0;
  const busy = isRunning || isTesting;

  // Python нь ачаалахад хэдэн секунд шаардана. Сурагч тайлбараа уншиж байх
  // зуур урьдчилан татвал "Ажиллуулах" дарахад шууд ажиллана.
  const [pythonReady, setPythonReady] = useState(false);
  useEffect(() => {
    if (!isPython) return;

    let cancelled = false;
    preloadPython().then(
      () => {
        if (!cancelled) setPythonReady(true);
      },
      () => {
        // Алдааг ажиллуулах үед console дээр харуулна.
      },
    );
    return () => {
      cancelled = true;
    };
  }, [isPython]);

  // C/C++-ийн анхны кодыг мөн адил урьдчилан хөрвүүлнэ.
  useEffect(() => {
    if (isNativeLanguage(language)) preloadNative(language, initialCode);
  }, [language, initialCode]);

  const run = useCallback(() => {
    if (!runnable || isTesting) return;
    // Үр дүн, алдаа шууд харагдах ёстой — console эвхэгдсэн байсан ч нээнэ.
    setConsoleOpen(true);
    setConsoleTab("console");
    startRun(async () => {
      if (isNativeLanguage(language)) {
        setResult(await runNative(language, code, { stdin, onPhase: setPhase }));
      } else if (isPython) {
        setResult(await runPython(code, { stdin }));
      } else if (isSql) {
        setResult(await runSql(code));
      } else {
        setResult(await runJavaScript(code, { stdin }));
      }
    });
  }, [code, stdin, runnable, isTesting, isPython, isSql, language]);

  /**
   * «Тест ажиллуулах» (`samples`) — зөвхөн жишээ тестүүд, дэлгэрэнгүйтэйгээ.
   * «Илгээх» (`all`) — нууцыг оролцуулан бүгд; бүгд давбал хичээл дуусна.
   */
  const runTests = useCallback(
    async (mode: TestRunState["mode"]) => {
      if (!exercise || !supportsExercises(language) || isRunning || isTesting) return;

      const indices = exercise.tests.flatMap((test, index) =>
        mode === "all" || test.sample ? [index] : [],
      );
      const id = ++testRunId.current;
      const base = { id, mode, indices, results: indices.map(() => undefined) };
      // Хуучирсан ажиллуулалтын callback шинэ үр дүнг дарахгүй.
      const update = (change: (run: TestRunState) => TestRunState) =>
        setTestRun((current) => (current && current.id === id ? change(current) : current));

      setConsoleOpen(true);
      setConsoleTab("tests");
      setIsTesting(true);
      setTestRun({ ...base, status: "compiling" });

      const tests = indices.map((index) => exercise.tests[index]);
      const onRunning = () => update((run) => ({ ...run, status: "running" }));
      const onResult = (index: number, result: TestCaseResult) =>
        update((run) => {
          const results = [...run.results];
          results[index] = result;
          return { ...run, results };
        });

      try {
        // C/C++ — нэг удаа хөрвүүлээд тест бүрийг шинэ worker-т. Python —
        // Pyodide-ийн worker-т тест бүрийг цэвэр нэрийн талбарт.
        const runAll = async () => {
          if (isNativeLanguage(language)) {
            return runNativeTests(language, code, tests, {
              onPhase: (phase) => phase === "running" && onRunning(),
              onResult,
            });
          }
          // JavaScript — тест бүр шинэ worker-т, ачаалах зүйлгүй.
          if (isJavaScript) {
            onRunning();
            return runJavaScriptTests(code, tests, { onResult });
          }
          return runPythonTests(code, tests, { onReady: onRunning, onResult });
        };
        const outcome = await runAll();

        if (outcome.kind === "compile-error") {
          const { diagnostics } = outcome;
          update((run) => ({ ...run, status: "compile-error", diagnostics }));
          recordTestOutcome(false);
          return;
        }
        // Хөрвүүлэгч, Python ачаалж чадаагүй — сурагчийн алдаа биш, тоолохгүй.
        if (outcome.kind === "failed") {
          const { message } = outcome;
          update((run) => ({ ...run, status: "failed", message }));
          return;
        }

        const allPassed = outcome.results.every((result) => result.status === "passed");
        recordTestOutcome(allPassed);
        let note: SubmitNote;
        if (mode === "samples" && allPassed) {
          note = { tone: "success", text: mn.learn.exercise.samplesPassed };
        } else if (mode === "all" && !allPassed) {
          note = { tone: "error", text: mn.learn.exercise.submitFailed };
        }
        update((run) => ({
          ...run,
          status: "done",
          results: outcome.results,
          note,
        }));

        if (mode === "all" && allPassed && onSubmitPassed) {
          const saved = await onSubmitPassed();
          update((run) => ({ ...run, note: saved }));
        }
      } finally {
        setIsTesting(false);
      }
    },
    [
      exercise,
      language,
      code,
      isRunning,
      isTesting,
      isJavaScript,
      onSubmitPassed,
      recordTestOutcome,
    ],
  );

  const reset = useCallback(() => {
    setCode(initialCode);
    setResult(null);
  }, [initialCode]);

  // Анх удаа ачаалж эсвэл хөрвүүлж байгаа бол console дээр юу болж байгааг хэлнэ.
  let statusText: string = mn.learn.running;
  if (isPython && !pythonReady) statusText = mn.learn.pythonLoading;
  if (isNative && phase === "compiling") statusText = mn.learn.compiling;
  if (isSql) statusText = mn.learn.sql.running;

  const showTests = hasExercise && consoleTab === "tests";

  return (
    <div className="flex min-h-0 flex-1 flex-col">
      <MotivationDialog
        motivation={motivation}
        onClose={() => setMotivation(null)}
        canDisable={user !== null}
      />
      <div className="flex flex-wrap items-center justify-between gap-2 border-b px-3 py-2">
        {/* Маш нарийн дэлгэц дээр шошго зай эзлэхгүй — товчнууд чухал. */}
        <span className="text-muted-foreground hidden font-mono text-xs min-[360px]:inline">
          {languageLabels[language]}
        </span>

        <div className="ml-auto flex items-center gap-2">
          {acceptsStdin && (
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setShowStdin((open) => !open)}
              aria-expanded={showStdin}
              title={showStdin ? mn.learn.stdinHide : mn.learn.stdinShow}
            >
              <KeyboardIcon className="size-3.5" />
              <span className="hidden sm:inline">{mn.learn.stdin}</span>
            </Button>
          )}
          <Dialog open={confirmReset} onOpenChange={setConfirmReset}>
            <DialogTrigger asChild>
              <Button
                variant="ghost"
                size="sm"
                disabled={code === initialCode}
                title={mn.learn.reset}
              >
                <RotateCcwIcon className="size-3.5" />
                <span className="hidden sm:inline">{mn.learn.reset}</span>
              </Button>
            </DialogTrigger>
            <DialogContent>
              <DialogHeader>
                <DialogTitle>{mn.learn.reset}</DialogTitle>
                <DialogDescription>{mn.learn.resetConfirm}</DialogDescription>
              </DialogHeader>
              <DialogFooter>
                <Button variant="outline" onClick={() => setConfirmReset(false)}>
                  {mn.admin.cancel}
                </Button>
                <Button
                  variant="destructive"
                  onClick={() => {
                    setConfirmReset(false);
                    reset();
                  }}
                >
                  {mn.learn.resetConfirmYes}
                </Button>
              </DialogFooter>
            </DialogContent>
          </Dialog>

          {/* Ажиллуулах нь давтагдах, бага эрсдэлтэй үйлдэл тул дэд өнгөтэй —
              өнгөт «Хичээл дууссан» товчтой мөргөлдөхгүй. */}
          <Button variant="secondary" size="sm" onClick={run} disabled={busy || !runnable}>
            <PlayIcon className="size-3.5" />
            {isRunning ? mn.learn.running : mn.learn.run}
          </Button>
        </div>
      </div>

      <div className="min-h-0 flex-1">
        <CodeEditor value={code} onChange={setCode} language={language} onRun={run} />
      </div>

      {/* Стандарт оролт — `input()`, `scanf`, `cin` ашигладаг хичээлүүдэд.
          Хөтөч дотор програмыг зогсоож гараас хүлээх боломжгүй тул мөрүүдийг
          урьдчилан бэлдэж өгнө. */}
      {acceptsStdin && showStdin && (
        <div className="shrink-0 border-t">
          <label
            htmlFor="sandbox-stdin"
            className="text-muted-foreground block px-3 pt-2 font-mono text-xs"
          >
            {mn.learn.stdin}
          </label>
          <textarea
            id="sandbox-stdin"
            value={stdin}
            onChange={(event) => setStdin(event.target.value)}
            rows={3}
            spellCheck={false}
            placeholder={
              isNative
                ? mn.learn.stdinPlaceholderNative
                : isJavaScript
                  ? mn.learn.stdinPlaceholderJs
                  : mn.learn.stdinPlaceholder
            }
            className={cn(
              "bg-code-bg placeholder:text-muted-foreground/70 w-full resize-none px-3 py-2",
              "focus-visible:ring-ring font-mono text-[13px] focus-visible:ring-2",
              "focus-visible:-outline-offset-2 focus-visible:outline-none",
            )}
          />
        </div>
      )}

      {/* HackerRank-ийн «Run / Submit»: «Код ажиллуулах» нь дээрх «Оролт»-оор
          чөлөөтэй туршина, эдгээр нь урьдчилан бэлдсэн тестүүдээр дүгнэнэ. */}
      {hasExercise && (
        <div className="flex shrink-0 flex-wrap items-center justify-end gap-2 border-t px-3 py-2">
          {helpAction && <div className="mr-auto">{helpAction}</div>}
          <Button
            variant="outline"
            size="sm"
            onClick={() => void runTests("samples")}
            disabled={busy}
            title={mn.learn.exercise.runTestsHint}
          >
            <FlaskConicalIcon className="size-3.5" />
            {isTesting && testRun?.mode === "samples"
              ? mn.learn.exercise.testing
              : mn.learn.exercise.runTests}
          </Button>
          <Button
            size="sm"
            onClick={() => void runTests("all")}
            disabled={busy}
            title={mn.learn.exercise.submitHint}
          >
            <SendIcon className="size-3.5" />
            {isTesting && testRun?.mode === "all"
              ? mn.learn.exercise.testing
              : mn.learn.exercise.submit}
          </Button>
        </div>
      )}

      <div
        className={cn(
          "flex shrink-0 flex-col border-t transition-[height] duration-150",
          consoleOpen ? "h-44 sm:h-56" : "h-9",
        )}
      >
        <div className="flex shrink-0 items-center justify-between gap-2 border-b px-3 py-1.5">
          <div className="flex min-w-0 items-center gap-1">
            <button
              type="button"
              onClick={() => setConsoleOpen((open) => !open)}
              aria-expanded={consoleOpen}
              aria-label={
                hasExercise
                  ? consoleOpen
                    ? mn.learn.consoleHide
                    : mn.learn.consoleShow
                  : undefined
              }
              className="text-muted-foreground hover:text-foreground -mx-1.5 flex items-center gap-1.5 rounded px-1.5 py-0.5 font-mono text-xs"
              title={consoleOpen ? mn.learn.consoleHide : mn.learn.consoleShow}
            >
              {consoleOpen ? (
                <ChevronDownIcon className="size-3.5" aria-hidden />
              ) : (
                <ChevronUpIcon className="size-3.5" aria-hidden />
              )}
              {!hasExercise && mn.learn.console}
            </button>

            {hasExercise && (
              <div
                role="tablist"
                aria-label={mn.learn.console}
                className="ml-1.5 flex items-center gap-1"
              >
                {(["console", "tests"] as const).map((tab) => (
                  <button
                    key={tab}
                    type="button"
                    role="tab"
                    aria-selected={consoleTab === tab}
                    onClick={() => {
                      setConsoleTab(tab);
                      setConsoleOpen(true);
                    }}
                    className={cn(
                      "rounded px-2 py-0.5 font-mono text-xs transition-colors",
                      consoleTab === tab
                        ? "bg-muted text-foreground"
                        : "text-muted-foreground hover:text-foreground",
                    )}
                  >
                    {tab === "console" ? mn.learn.exercise.tabConsole : mn.learn.exercise.tabTests}
                  </button>
                ))}
              </div>
            )}
          </div>
          <Button
            variant="ghost"
            size="sm"
            className="h-7 px-2"
            onClick={() => (showTests ? setTestRun(null) : setResult(null))}
            disabled={showTests ? !testRun || isTesting : !result}
            aria-label={mn.learn.clearConsole}
            title={mn.learn.clearConsole}
          >
            <Trash2Icon className="size-3.5" />
          </Button>
        </div>

        {consoleOpen && (
          <div className="bg-code-bg min-h-0 flex-1">
            {showTests && exercise ? (
              <TestResults
                tests={exercise.tests}
                run={testRun}
                preparingText={
                  isPython && !pythonReady ? mn.learn.pythonLoading : mn.learn.compiling
                }
              />
            ) : runnable ? (
              <ConsoleOutput
                result={result}
                isRunning={isRunning}
                statusText={statusText}
                emptyText={isSql ? mn.learn.sql.consoleEmpty : undefined}
              />
            ) : (
              <p className="text-muted-foreground p-3 text-sm">
                {language === "plaintext"
                  ? mn.learn.algorithmNotice
                  : language === "sql"
                    ? mn.learn.sql.sqlServerNotRunnable
                    : mn.learn.languageNotRunnable(languageLabels[language])}
              </p>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
