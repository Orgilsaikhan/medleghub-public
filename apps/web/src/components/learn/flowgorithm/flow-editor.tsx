"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import {
  DownloadIcon,
  FlaskConicalIcon,
  PauseIcon,
  PlayIcon,
  Redo2Icon,
  RotateCcwIcon,
  SendIcon,
  SkipForwardIcon,
  SquareIcon,
  Undo2Icon,
  ZoomInIcon,
  ZoomOutIcon,
} from "lucide-react";
import type { SubmitNote } from "@/components/learn/code-playground";
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
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useCurrentUser } from "@/lib/hooks/use-auth";
import { mn } from "@/lib/i18n/mn";
import { MOTIVATION_AFTER_FAILS, MOTIVATIONS, pickIndex, type Motivation } from "@/lib/motivation";
import { normalizeOutput, type TestCaseResult } from "@/lib/sandbox/grader";
import type { LessonExercise, LessonTestCase } from "@/lib/types/api";
import { cn } from "@/lib/utils";
import {
  editProgram,
  emptyProgram,
  exportFprg,
  LABELS,
  newNode,
  parseProgram,
  type FlowNode,
  type FlowProgram,
  type InsertPoint,
  type NodeKind,
} from "@/lib/flowgorithm/model";
import { FlowRuntime, type RuntimeEvent, type RuntimeSnapshot } from "@/lib/flowgorithm/runtime";
import { executeFlow } from "@/lib/flowgorithm/testing";
import { Chart } from "./chart";
import { NodeDialog } from "./node-dialog";
import { Palette } from "./palette";

type Status = "idle" | "running" | "paused" | "input" | "done" | "error";
const STATUS: Record<Status, string> = {
  idle: "Бэлэн",
  running: "Ажиллаж байна",
  paused: "Түр зогссон",
  input: "Оролт хүлээж байна",
  done: "Дууслаа",
  error: "Алдаа",
};
const EMPTY: RuntimeSnapshot = { variables: [], output: "", steps: 0 };

interface ExerciseProps {
  /** Даалгавар — «Тест ажиллуулах», «Илгээх» товч ба «Тест» хэсэг гарна. */
  exercise?: LessonExercise | null;
  /** «Илгээх»-ийн бүх тест давсны дараа — хичээлийг дуусгаад мэдэгдэл буцаана. */
  onSubmitPassed?: () => Promise<SubmitNote>;
  /** Тестийн товчнуудын зүүн талд — «Тусламж». */
  helpAction?: React.ReactNode;
}

/** Нэг тест — `grader.ts`-ийн `gradeRun`-тай ижил дүрмээр хэвийн болгож харьцуулна. */
function gradeFlow(program: FlowProgram, test: LessonTestCase): TestCaseResult {
  const startedAt = performance.now();
  const run = executeFlow(program, test.stdin);
  const base = {
    actual: normalizeOutput(run.answer),
    durationMs: Math.round(performance.now() - startedAt),
  };
  if (run.error) return { ...base, status: "runtime-error", message: run.error };
  const passed = base.actual === normalizeOutput(test.expected_output);
  return { ...base, status: passed ? "passed" : "wrong-answer" };
}

export default function FlowEditor({
  initialCode,
  lessonId,
  ...exercise
}: {
  initialCode: string;
  lessonId: string;
} & ExerciseProps) {
  const { user } = useCurrentUser();
  if (!user) return <div className="p-5 text-sm">Схем ачаалж байна…</div>;
  const storageKey = `medleghub:flow:${user.id}:${lessonId}`;
  return (
    <EditorSession
      key={storageKey}
      initialCode={initialCode}
      storageKey={storageKey}
      {...exercise}
    />
  );
}

function EditorSession({
  initialCode,
  storageKey,
  exercise,
  onSubmitPassed,
  helpAction,
}: { initialCode: string; storageKey: string } & ExerciseProps) {
  const [initial] = useState(() => {
    let starter: FlowProgram;
    try {
      starter = parseProgram(initialCode);
    } catch {
      return {
        starter: emptyProgram(),
        program: emptyProgram(),
        notice: "Хичээлийн схемийг ачаалж чадсангүй. Сум дээр дарж өөрөө схем байгуулж болно.",
      };
    }
    try {
      const saved = localStorage.getItem(storageKey);
      if (saved) {
        const draft = JSON.parse(saved);
        if (draft.source === initialCode)
          return {
            starter,
            program: parseProgram(JSON.stringify(draft.program)),
            notice: "Хадгалсан схемийг сэргээлээ.",
          };
      }
    } catch {
      /* A malformed draft must not prevent opening the lesson. */
    }
    return {
      starter,
      program: starter,
      notice: "Сумны + дээр дарж дүрс нэмнэ. Дүрсэн дээр дарж утгыг нь засна.",
    };
  });
  const [program, setProgram] = useState(initial.program);
  const [past, setPast] = useState<FlowProgram[]>([]);
  const [future, setFuture] = useState<FlowProgram[]>([]);
  const [notice, setNotice] = useState(initial.notice);
  const [point, setPoint] = useState<InsertPoint | null>(null);
  const [editing, setEditing] = useState<FlowNode | null>(null);
  const [resetOpen, setResetOpen] = useState(false);
  const [zoom, setZoom] = useState(1);
  const [status, setStatus] = useState<Status>("idle");
  const [snapshot, setSnapshot] = useState<RuntimeSnapshot>(EMPTY);
  const [activeId, setActiveId] = useState<string | null>(null);
  const [error, setError] = useState("");
  const [pendingInput, setPendingInput] = useState<RuntimeEvent | null>(null);
  const [input, setInput] = useState("");
  const [inputError, setInputError] = useState("");
  const [panel, setPanel] = useState<"output" | "variables" | "tests">("output");
  const [testRun, setTestRun] = useState<TestRunState | null>(null);
  const [isTesting, setIsTesting] = useState(false);
  const testRunId = useRef(0);
  const machine = useRef<FlowRuntime | null>(null);
  const continueMode = useRef<"run" | "step">("run");
  const locked = status === "running" || status === "input" || status === "paused";
  const hasExercise = !!exercise && exercise.tests.length > 0;

  // Тестэд дараалан 3 унавал урам өгөх үг — `code-playground.tsx`-тэй ижил.
  const { user } = useCurrentUser();
  const showMotivation = user?.show_motivation ?? true;
  const failStreak = useRef(0);
  const lastMotivation = useRef<number | null>(null);
  const [motivation, setMotivation] = useState<Motivation | null>(null);

  const recordTestOutcome = (passed: boolean) => {
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
  };

  const stop = () => {
    machine.current = null;
    setStatus("idle");
    setActiveId(null);
    setPendingInput(null);
    setInputError("");
  };
  const store = (next: FlowProgram, saved = "Схем энэ хөтөчид хадгалагдсан.") => {
    try {
      localStorage.setItem(storageKey, JSON.stringify({ source: initialCode, program: next }));
      setNotice(saved);
    } catch {
      setNotice("Хөтөчид хадгалж чадсангүй. .fprg файлаар татаж аваарай.");
    }
  };
  const commit = (next: FlowProgram, saved?: string) => {
    stop();
    setError("");
    setSnapshot(EMPTY);
    setPast((items) => [...items.slice(-39), program]);
    setFuture([]);
    setProgram(next);
    store(next, saved);
  };
  const undo = () => {
    const previous = past.at(-1);
    if (!previous) return;
    stop();
    setError("");
    setSnapshot(EMPTY);
    setPast(past.slice(0, -1));
    setFuture([program, ...future]);
    setProgram(previous);
    store(previous);
  };
  const redo = () => {
    const next = future[0];
    if (!next) return;
    stop();
    setError("");
    setSnapshot(EMPTY);
    setPast([...past, program]);
    setFuture(future.slice(1));
    setProgram(next);
    store(next);
  };

  const advance = useCallback((mode: "run" | "step", answer?: string) => {
    const runtime = machine.current;
    if (!runtime) return;
    try {
      const result = runtime.iterator.next(answer);
      setSnapshot(runtime.snapshot());
      if (result.done) {
        setStatus("done");
        setActiveId(null);
        machine.current = null;
        return;
      }
      const event = result.value;
      setActiveId(event.nodeId);
      if (event.kind === "input") {
        continueMode.current = mode;
        setPendingInput(event);
        setInput("");
        setInputError("");
        setPanel("output");
        setStatus("input");
      } else if (event.kind === "breakpoint" || mode === "step") setStatus("paused");
      else setStatus("running");
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "Схемийг ажиллуулж чадсангүй.");
      setActiveId(runtime.activeId);
      setSnapshot(runtime.snapshot());
      setStatus("error");
      setPanel("output");
      machine.current = null;
    }
  }, []);

  useEffect(() => {
    if (status !== "running") return;
    const timer = setTimeout(() => advance("run"), 25);
    return () => clearTimeout(timer);
  }, [status, snapshot.steps, advance]);

  const start = (mode: "run" | "step") => {
    // «Тест» хэсэг нээлттэй байсан ч ажиллуулсан схемийн гаралт харагдана.
    setPanel((current) => (current === "tests" ? "output" : current));
    if (!machine.current) {
      machine.current = new FlowRuntime(program);
      setSnapshot(EMPTY);
      setError("");
      setInputError("");
    }
    advance(mode);
  };
  const submitInput = (event: React.FormEvent) => {
    event.preventDefault();
    if (!machine.current || !pendingInput?.variable) return;
    try {
      machine.current.validateInput(pendingInput.variable.name, input);
    } catch (cause) {
      setInputError(cause instanceof Error ? cause.message : "Оролтоо шалгана уу.");
      return;
    }
    setPendingInput(null);
    setInputError("");
    advance(continueMode.current, input);
  };

  /**
   * «Тест ажиллуулах» (`samples`) — зөвхөн жишээ тестүүд. «Илгээх» (`all`) — нууцыг
   * оролцуулан бүгд; бүгд давбал хичээл дуусна. Тест бүр шинэ `FlowRuntime`-д.
   */
  const runTests = async (mode: TestRunState["mode"]) => {
    if (!exercise || isTesting) return;
    stop();
    const indices = exercise.tests.flatMap((test, index) =>
      mode === "all" || test.sample ? [index] : [],
    );
    const id = ++testRunId.current;
    // Хуучирсан ажиллуулалт шинэ үр дүнг дарахгүй.
    const update = (change: (run: TestRunState) => TestRunState) =>
      setTestRun((current) => (current && current.id === id ? change(current) : current));

    setPanel("tests");
    setIsTesting(true);
    setTestRun({ id, mode, indices, results: indices.map(() => undefined), status: "running" });
    try {
      const results: TestCaseResult[] = [];
      for (const [position, index] of indices.entries()) {
        // Урт давталттай схем дээр ч хөтөч хөлдөхгүй, явц нь харагдана.
        await new Promise((resolve) => setTimeout(resolve, 0));
        const result = gradeFlow(program, exercise.tests[index]);
        results.push(result);
        update((run) => {
          const next = [...run.results];
          next[position] = result;
          return { ...run, results: next };
        });
      }

      const allPassed = results.every((result) => result.status === "passed");
      recordTestOutcome(allPassed);
      let note: SubmitNote;
      if (mode === "samples" && allPassed) {
        note = { tone: "success", text: mn.learn.exercise.samplesPassed };
      } else if (mode === "all" && !allPassed) {
        note = { tone: "error", text: mn.learn.exercise.submitFailed };
      }
      update((run) => ({ ...run, status: "done", results, note }));

      if (mode === "all" && allPassed && onSubmitPassed) {
        const saved = await onSubmitPassed();
        update((run) => ({ ...run, note: saved }));
      }
    } finally {
      setIsTesting(false);
    }
  };

  const insertNode = (kind: NodeKind) => {
    if (!point) return;
    setPoint(null);
    try {
      commit(
        editProgram(program, { point, node: newNode(kind) }),
        `${LABELS[kind]} дүрс нэмэгдлээ. Дүрсэн дээр дарж утгаа оруулна уу.`,
      );
    } catch (cause) {
      setNotice(cause instanceof Error ? cause.message : "Дүрс нэмэх боломжгүй байна.");
    }
  };
  const saveNode = (node: FlowNode) => {
    try {
      commit(editProgram(program, { id: node.id, node }));
    } catch (cause) {
      setNotice(cause instanceof Error ? cause.message : "Дүрсийг хадгалж чадсангүй.");
    }
    setEditing(null);
  };
  const download = () => {
    const url = URL.createObjectURL(
      new Blob([exportFprg(program)], { type: "application/xml;charset=utf-8" }),
    );
    const link = document.createElement("a");
    link.href = url;
    link.download = "medleghub.fprg";
    link.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  };

  return (
    <div className="flex h-full min-h-0 min-w-0 flex-1 flex-col" data-testid="flow-editor">
      <MotivationDialog
        motivation={motivation}
        onClose={() => setMotivation(null)}
        canDisable={user !== null}
      />
      <div className="bg-muted/30 flex shrink-0 flex-wrap items-center gap-1 border-b px-2 py-2">
        <span className="mr-2 text-sm font-semibold">Flowgorithm</span>
        {status === "running" ? (
          <Button size="sm" variant="secondary" onClick={() => setStatus("paused")}>
            <PauseIcon />
            Түр зогсоох
          </Button>
        ) : (
          <Button
            size="sm"
            variant="secondary"
            onClick={() => start("run")}
            disabled={status === "input"}
          >
            <PlayIcon />
            {status === "paused" ? "Үргэлжлүүлэх" : "Ажиллуулах"}
          </Button>
        )}
        <Button
          size="sm"
          variant="ghost"
          onClick={() => start("step")}
          disabled={status === "running" || status === "input"}
          title="Нэг дүрсээр урагшлах"
        >
          <SkipForwardIcon />
          Алхам
        </Button>
        <Button
          size="icon-sm"
          variant="ghost"
          aria-label="Зогсоох"
          onClick={stop}
          disabled={!locked}
        >
          <SquareIcon />
        </Button>
        <div className="bg-border mx-1 h-5 w-px" />
        <Button
          size="icon-sm"
          variant="ghost"
          aria-label="Буцаах"
          title="Буцаах"
          disabled={locked || past.length === 0}
          onClick={undo}
        >
          <Undo2Icon />
        </Button>
        <Button
          size="icon-sm"
          variant="ghost"
          aria-label="Дахин хийх"
          title="Дахин хийх"
          disabled={locked || future.length === 0}
          onClick={redo}
        >
          <Redo2Icon />
        </Button>
        <Button
          size="icon-sm"
          variant="ghost"
          aria-label="Анхны схем"
          title="Анхны схем"
          disabled={locked}
          onClick={() => setResetOpen(true)}
        >
          <RotateCcwIcon />
        </Button>
        <Button size="sm" variant="ghost" onClick={download} title="Flowgorithm програмд нээх файл">
          <DownloadIcon />
          .fprg
        </Button>
        <div className="ml-auto flex items-center">
          <Button
            size="icon-sm"
            variant="ghost"
            aria-label="Жижигрүүлэх"
            onClick={() => setZoom((value) => Math.max(0.4, value - 0.1))}
            disabled={zoom <= 0.4}
          >
            <ZoomOutIcon />
          </Button>
          <span className="w-10 text-center text-xs tabular-nums">{Math.round(zoom * 100)}%</span>
          <Button
            size="icon-sm"
            variant="ghost"
            aria-label="Томруулах"
            onClick={() => setZoom((value) => Math.min(1.6, value + 0.1))}
            disabled={zoom >= 1.6}
          >
            <ZoomInIcon />
          </Button>
        </div>
      </div>
      <p className="text-muted-foreground shrink-0 border-b px-3 py-1.5 text-xs" role="status">
        {notice}
      </p>
      <Chart
        program={program}
        zoom={zoom}
        activeId={activeId}
        locked={locked}
        onEdit={setEditing}
        onInsert={setPoint}
      />
      {/* «Тест ажиллуулах» нь жишээгээр, «Илгээх» нь нууц тестийг оролцуулан шалгана. */}
      {hasExercise && (
        <div className="flex shrink-0 flex-wrap items-center justify-end gap-2 border-t px-3 py-2">
          {helpAction && <div className="mr-auto">{helpAction}</div>}
          <Button
            variant="outline"
            size="sm"
            onClick={() => void runTests("samples")}
            disabled={isTesting}
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
            disabled={isTesting}
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
          "flex min-h-0 shrink-0 flex-col border-t",
          hasExercise ? "h-48 sm:h-64" : "h-48 sm:h-52",
        )}
      >
        <div className="bg-muted/30 flex shrink-0 items-center gap-1 border-b px-2 py-1">
          <Button
            size="sm"
            variant={panel === "output" ? "secondary" : "ghost"}
            onClick={() => setPanel("output")}
            aria-pressed={panel === "output"}
          >
            Гаралт
          </Button>
          <Button
            size="sm"
            variant={panel === "variables" ? "secondary" : "ghost"}
            onClick={() => setPanel("variables")}
            aria-pressed={panel === "variables"}
          >
            Хувьсагчид
          </Button>
          {hasExercise && (
            <Button
              size="sm"
              variant={panel === "tests" ? "secondary" : "ghost"}
              onClick={() => setPanel("tests")}
              aria-pressed={panel === "tests"}
            >
              {mn.learn.exercise.tabTests}
            </Button>
          )}
          <span className="text-muted-foreground ml-auto text-xs" role="status">
            {STATUS[status]} · {snapshot.steps} алхам
          </span>
        </div>
        <div className={cn("min-h-0 flex-1 overflow-auto", panel !== "tests" && "p-3 text-sm")}>
          {panel === "tests" && exercise ? (
            <TestResults
              tests={exercise.tests}
              run={testRun}
              emptyText={mn.learn.exercise.flowEmpty}
            />
          ) : panel === "output" ? (
            <>
              <pre
                className="font-mono text-sm break-words whitespace-pre-wrap"
                role="log"
                aria-label="Схемийн гаралт"
                aria-live="polite"
              >
                {snapshot.output ||
                  (status === "idle" ? "Ажиллуулах эсвэл Алхам товчийг дараарай." : "")}
              </pre>
              {error && (
                <p className="text-destructive mt-2" role="alert">
                  {error}
                </p>
              )}
              {status === "input" && pendingInput?.variable && (
                <form className="mt-2 space-y-2" onSubmit={submitInput}>
                  <Label htmlFor="flow-live-input">
                    {pendingInput.variable.name} ({pendingInput.variable.type}) утгыг оруулна уу
                  </Label>
                  <div className="flex gap-2">
                    <Input
                      key={pendingInput.nodeId + snapshot.steps}
                      id="flow-live-input"
                      autoFocus
                      value={input}
                      onChange={(event) => setInput(event.target.value)}
                      autoComplete="off"
                      maxLength={1000}
                      aria-describedby={inputError ? "flow-input-error" : undefined}
                    />
                    <Button type="submit">Оруулах</Button>
                  </div>
                  {inputError && (
                    <p id="flow-input-error" className="text-destructive text-xs" role="alert">
                      {inputError}
                    </p>
                  )}
                </form>
              )}
            </>
          ) : snapshot.variables.length ? (
            <table className="w-full text-left text-xs">
              <thead>
                <tr className="text-muted-foreground">
                  <th className="pb-2">Нэр</th>
                  <th className="pb-2">Төрөл</th>
                  <th className="pb-2">Утга</th>
                </tr>
              </thead>
              <tbody>
                {snapshot.variables.map((variable) => (
                  <tr key={variable.name} className="border-t">
                    <td className="py-1.5 font-mono">{variable.name}</td>
                    <td>{variable.type}</td>
                    <td className="max-w-48 font-mono break-words">
                      {variable.value === null ? "—" : String(variable.value)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <p className="text-muted-foreground">
              Declare дүрс ажиллахад хувьсагчид энд харагдана.
            </p>
          )}
        </div>
      </div>
      {point && <Palette onClose={() => setPoint(null)} onSelect={insertNode} />}
      {editing && (
        <NodeDialog
          key={editing.id}
          node={editing}
          onClose={() => setEditing(null)}
          onSave={saveNode}
          onDelete={() => {
            commit(editProgram(program, { id: editing.id, node: null }));
            setEditing(null);
          }}
        />
      )}
      <Dialog open={resetOpen} onOpenChange={setResetOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Схемийг дахин эхлүүлэх</DialogTitle>
            <DialogDescription>
              Хичээлийн жишээг сэргээх эсвэл хоосон Main → End схемээс эхэлж болно. Одоогийн
              өөрчлөлтөө «Буцаах»-аар сэргээнэ.
            </DialogDescription>
          </DialogHeader>
          <DialogFooter>
            <Button
              variant="outline"
              onClick={() => {
                commit(emptyProgram());
                setResetOpen(false);
              }}
            >
              Хоосон схем
            </Button>
            <Button
              onClick={() => {
                commit(initial.starter);
                setResetOpen(false);
              }}
            >
              Хичээлийн жишээ
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}
