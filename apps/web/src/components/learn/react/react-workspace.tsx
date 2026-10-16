"use client";

import { BookOpenIcon, Code2Icon, MonitorIcon, RotateCcwIcon } from "lucide-react";
import dynamic from "next/dynamic";
import { useCallback, useEffect, useId, useMemo, useRef, useState, type ReactNode } from "react";

import { MotivationDialog } from "@/components/learn/motivation-dialog";
import {
  BrowserPane,
  INITIAL_BROWSER,
  type BrowserState,
} from "@/components/learn/react/browser-pane";
import { ConsolePanel } from "@/components/learn/react/console-panel";
import { FileTabs } from "@/components/learn/react/file-tabs";
import { TestPanel, type TestNote, type TestSlot } from "@/components/learn/react/test-panel";
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
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { useCurrentUser } from "@/lib/hooks/use-auth";
import { mn } from "@/lib/i18n/mn";
import { MOTIVATION_AFTER_FAILS, MOTIVATIONS, pickIndex, type Motivation } from "@/lib/motivation";
import { monacoLanguage, parseLessonFiles, type LessonFile } from "@/lib/sandbox/react/files";
import type { SandboxJob, SandboxMessage } from "@/lib/sandbox/react/protocol";
import { createJob, runReactTests } from "@/lib/sandbox/react/runner";
import type { ConsoleEntry } from "@/lib/sandbox/runner";
import type { LessonExercise } from "@/lib/types/api";
import { cn } from "@/lib/utils";

const CodeEditor = dynamic(() => import("@/components/learn/code-editor"), {
  ssr: false,
  loading: () => <Skeleton className="h-full w-full rounded-none" />,
});

const MAX_CONSOLE = 500;

interface ReactWorkspaceProps {
  lessonId: string;
  initialCode: string;
  exercise: LessonExercise | null;
  /** «Заавар» tab — хичээлийн текст, видео, даалгавар. */
  instructions: ReactNode;
  isDesktop: boolean;
  /** Бүх тест давсны дараа — хичээлийг дуусгаж мэдэгдлийг буцаана. */
  onSubmitPassed?: () => Promise<TestNote | undefined>;
  helpAction?: ReactNode;
  nextHref?: string | null;
}

type RightTab = "instructions" | "browser";
type MobileTab = "instructions" | "code" | "browser";

function describe(message: Extract<SandboxMessage, { type: "error" }>["error"]): string {
  const where = message.file ? `${message.file}${message.line ? `:${message.line}` : ""} — ` : "";
  return `${where}${message.kind === "compile" ? "Синтакс алдаа: " : ""}${message.message}`;
}

/**
 * React хичээлийн засварлагч — react-tutorial.app-ийн байршил:
 *
 *     ┌ App.jsx │ 🔒 main.jsx │ 🔒 index.html ┐ ┌ Заавар │ Хөтөч ─────────┐
 *     │ засварлагч                           │ │ хичээл / апп            │
 *     ├ Тестүүд (1 / 3)  [Тусламж] [▶ Ажил.] ┤ ├ Console ────────────────┤
 *     └ ✓ …  ✗ … (шалтгаан)                  ┘ └ › …                   ┘
 *
 * Нарийн дэлгэц дээр «Заавар / Код / Хөтөч» гэсэн гурван tab.
 *
 * Хичээл солигдоход дуудагч `key`-г сольж component-ийг шинээр үүсгэнэ.
 */
export function ReactWorkspace({
  lessonId,
  initialCode,
  exercise,
  instructions,
  isDesktop,
  onSubmitPassed,
  helpAction,
  nextHref,
}: ReactWorkspaceProps) {
  const initialFiles = useMemo(() => parseLessonFiles(initialCode), [initialCode]);
  const [files, setFiles] = useState<LessonFile[]>(initialFiles);
  const [active, setActive] = useState(
    () => initialFiles.find((file) => !file.locked)?.name ?? initialFiles[0].name,
  );
  const activeFile = files.find((file) => file.name === active) ?? files[0];
  const idPrefix = useId().replace(/:/g, "");

  const tests = useMemo(
    () =>
      (exercise?.tests ?? [])
        .filter((test) => test.code)
        .map((test, index) => ({ name: test.name || `Тест ${index + 1}`, code: test.code ?? "" })),
    [exercise],
  );

  const [rightTab, setRightTab] = useState<RightTab>("instructions");
  const [mobileTab, setMobileTab] = useState<MobileTab>("instructions");
  const [testsOpen, setTestsOpen] = useState(true);
  const [consoleOpen, setConsoleOpen] = useState(true);
  const [confirmReset, setConfirmReset] = useState(false);

  // --- «Хөтөч» ---------------------------------------------------------------

  // react-tutorial шиг: хичээл нээгдэхэд код шууд ажиллана.
  const [job, setJob] = useState<SandboxJob>(() =>
    createJob(initialFiles, "preview", { storage: {}, path: "/" }),
  );
  const [browser, setBrowser] = useState<BrowserState>(INITIAL_BROWSER);
  const [entries, setEntries] = useState<ConsoleEntry[]>([]);
  // `localStorage` нь «дахин ачаалах»-ын дараа ч үлдэнэ — жинхэнэ хөтөч шиг.
  const storage = useRef<Record<string, string>>({});
  const pathRef = useRef("/");

  const startPreview = useCallback((current: LessonFile[]) => {
    setEntries([]);
    setBrowser((state) => ({ ...state, canGoBack: false, canGoForward: false }));
    setJob(createJob(current, "preview", { storage: storage.current, path: pathRef.current }));
  }, []);

  const onMessage = useCallback((message: SandboxMessage) => {
    switch (message.type) {
      case "console":
        setEntries((list) =>
          list.length >= MAX_CONSOLE
            ? list
            : [...list, { level: message.level, text: message.text }],
        );
        break;
      case "error":
        setEntries((list) => [...list, { level: "error", text: describe(message.error) }]);
        break;
      case "title":
        setBrowser((state) => ({ ...state, title: message.title || "React App" }));
        break;
      case "location":
        pathRef.current = message.path;
        setBrowser((state) => ({
          ...state,
          path: message.path,
          canGoBack: message.canGoBack,
          canGoForward: message.canGoForward,
        }));
        break;
      case "storage":
        storage.current = message.data;
        break;
    }
  }, []);

  // --- Тест ------------------------------------------------------------------

  const [results, setResults] = useState<TestSlot[]>(() => tests.map(() => undefined));
  const [testing, setTesting] = useState(false);
  const [note, setNote] = useState<TestNote | undefined>();
  const runId = useRef(0);

  // Тестэд дараалан унасан тоо — 3 хүрвэл урам өгөх үг (бусад сургалттай ижил).
  const { user } = useCurrentUser();
  const showMotivation = user?.show_motivation ?? true;
  const failStreak = useRef(0);
  const lastMotivation = useRef<number | null>(null);
  const [motivation, setMotivation] = useState<Motivation | null>(null);

  const recordOutcome = useCallback(
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

  const runTests = useCallback(
    async (current: LessonFile[]) => {
      if (tests.length === 0) return;
      const id = ++runId.current;
      setTesting(true);
      setNote(undefined);
      setTestsOpen(true);
      setResults(tests.map(() => "running"));
      try {
        const outcome = await runReactTests(current, tests, (index, result) => {
          if (runId.current !== id) return;
          setResults((slots) => slots.map((slot, i) => (i === index ? result : slot)));
        });
        if (runId.current !== id) return;
        setResults(outcome);
        const allPassed = outcome.every((result) => result.passed);
        recordOutcome(allPassed);
        if (!allPassed) {
          setNote({ tone: "error", text: mn.learn.react.someFailed });
          return;
        }
        setNote({ tone: "success", text: mn.learn.exercise.submitPassedAgain });
        const saved = await onSubmitPassed?.();
        if (runId.current === id && saved) setNote(saved);
      } finally {
        if (runId.current === id) setTesting(false);
      }
    },
    [tests, onSubmitPassed, recordOutcome],
  );

  // --- Үйлдлүүд ------------------------------------------------------------------

  const filesRef = useRef(files);
  useEffect(() => {
    filesRef.current = files;
  }, [files]);

  const run = useCallback(() => {
    const current = filesRef.current;
    startPreview(current);
    if (tests.length > 0) {
      void runTests(current);
      if (!isDesktop && mobileTab === "instructions") setMobileTab("code");
    } else {
      // Тестгүй хичээлд үр дүн нь зөвхөн «Хөтөч» дээр — шууд харуулна.
      setRightTab("browser");
      if (!isDesktop) setMobileTab("browser");
    }
  }, [startPreview, runTests, tests.length, isDesktop, mobileTab]);

  // Tab солих үед Monaco шинэ (түгжигдсэн) model дээр `onChange` дуудаж
  // болно — идэвхтэй tab-аар биш, өөрчлөгдсөн model-ийн замаар шинэчилнэ.
  const modelScope = `/lesson-${lessonId}/`;
  const updateFile = useCallback(
    (code: string, modelPath?: string) => {
      if (!modelPath?.startsWith(modelScope)) return;
      const name = modelPath.slice(modelScope.length);
      setFiles((list) =>
        list.map((file) =>
          file.name === name && !file.locked && file.code !== code ? { ...file, code } : file,
        ),
      );
    },
    [modelScope],
  );

  const changed = files.some((file, index) => file.code !== initialFiles[index]?.code);

  const reset = () => {
    setFiles(initialFiles);
    pathRef.current = "/";
    storage.current = {};
    setResults(tests.map(() => undefined));
    setNote(undefined);
    startPreview(initialFiles);
  };

  // --- Хэсгүүд ---------------------------------------------------------------------

  const resetButton = (
    <Dialog open={confirmReset} onOpenChange={setConfirmReset}>
      <DialogTrigger asChild>
        {/* Файлын tab-д зай үлдээхийн тулд зөвхөн дүрс. */}
        <Button
          variant="ghost"
          size="icon"
          className="size-7"
          disabled={!changed}
          title={mn.learn.reset}
          aria-label={mn.learn.reset}
        >
          <RotateCcwIcon className="size-3.5" />
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
  );

  const editor = (
    <div className="flex min-h-0 flex-1 flex-col">
      <FileTabs
        files={files}
        active={activeFile.name}
        onSelect={setActive}
        idPrefix={idPrefix}
        actions={resetButton}
      />
      <div
        id={`${idPrefix}-panel`}
        role="tabpanel"
        aria-labelledby={`${idPrefix}-tab-${files.indexOf(activeFile)}`}
        className="min-h-0 flex-1"
      >
        <CodeEditor
          value={activeFile.code}
          onChange={updateFile}
          language="jsx"
          monacoLanguage={monacoLanguage(activeFile.name)}
          path={`${modelScope}${activeFile.name}`}
          modelScope={modelScope}
          readOnly={activeFile.locked}
          readOnlyMessage={mn.learn.react.lockedMessage}
          onRun={run}
        />
      </div>
      <TestPanel
        names={tests.map((test) => test.name)}
        results={results}
        running={testing}
        note={note}
        open={testsOpen}
        onToggle={() => setTestsOpen((open) => !open)}
        onRun={run}
        helpAction={tests.length > 0 ? helpAction : undefined}
        nextHref={nextHref}
      />
    </div>
  );

  const browserPane = (
    <BrowserPane
      job={job}
      state={browser}
      onMessage={onMessage}
      onReload={() => startPreview(filesRef.current)}
    />
  );

  const consolePanel = (
    <ConsolePanel
      entries={entries}
      open={consoleOpen}
      onToggle={() => setConsoleOpen((open) => !open)}
      onClear={() => setEntries([])}
    />
  );

  const motivationDialog = (
    <MotivationDialog
      motivation={motivation}
      onClose={() => setMotivation(null)}
      canDisable={user !== null}
    />
  );

  // Идэвхгүй tab-ийг `display:none` биш `invisible`-ээр нууна: iframe-ийн
  // хэмжээ (useWindowSize гэх мэт) зөв үлдэж, timer нь удаашрахгүй.
  const stacked = "absolute inset-0 data-[state=inactive]:invisible";

  if (!isDesktop) {
    return (
      <Tabs
        value={mobileTab}
        onValueChange={(value) => setMobileTab(value as MobileTab)}
        className="flex min-h-0 flex-1 flex-col gap-0"
      >
        {motivationDialog}
        <TabsList className="mx-3 mt-2 shrink-0 self-start">
          <TabsTrigger value="instructions">{mn.learn.react.instructions}</TabsTrigger>
          <TabsTrigger value="code">{mn.learn.react.code}</TabsTrigger>
          <TabsTrigger value="browser">{mn.learn.react.browser}</TabsTrigger>
        </TabsList>
        <div className="relative min-h-0 flex-1">
          <TabsContent value="instructions" forceMount className={stacked}>
            {instructions}
          </TabsContent>
          <TabsContent value="code" forceMount className={cn(stacked, "flex flex-col")}>
            {editor}
          </TabsContent>
          <TabsContent value="browser" forceMount className={cn(stacked, "flex flex-col")}>
            <div className="min-h-0 flex-1">{browserPane}</div>
            {consolePanel}
          </TabsContent>
        </div>
      </Tabs>
    );
  }

  return (
    <div className="flex min-h-0 flex-1">
      {motivationDialog}
      <div className="flex min-h-0 w-1/2 min-w-0 flex-col border-r">{editor}</div>
      <Tabs
        value={rightTab}
        onValueChange={(value) => setRightTab(value as RightTab)}
        className="flex min-h-0 w-1/2 min-w-0 flex-col gap-0"
      >
        <TabsList variant="line" className="h-10 w-full shrink-0 justify-start border-b px-2">
          <TabsTrigger value="instructions" className="flex-none px-3">
            <BookOpenIcon aria-hidden />
            {mn.learn.react.instructions}
          </TabsTrigger>
          <TabsTrigger value="browser" className="flex-none px-3">
            <MonitorIcon aria-hidden />
            {mn.learn.react.browser}
          </TabsTrigger>
          {tests.length === 0 && (
            <span className="text-muted-foreground ml-auto hidden items-center gap-1.5 pr-1 text-xs xl:flex">
              <Code2Icon className="size-3.5" aria-hidden />
              Ctrl + Enter
            </span>
          )}
        </TabsList>
        <div className="relative min-h-0 flex-1">
          <TabsContent value="instructions" forceMount className={stacked}>
            {instructions}
          </TabsContent>
          <TabsContent value="browser" forceMount className={stacked}>
            {browserPane}
          </TabsContent>
        </div>
        {consolePanel}
      </Tabs>
    </div>
  );
}
