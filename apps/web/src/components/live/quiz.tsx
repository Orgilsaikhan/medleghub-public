"use client";

import { useMutation } from "@tanstack/react-query";
import {
  ArrowRightIcon,
  CheckIcon,
  CircleCheckIcon,
  CircleXIcon,
  ListChecksIcon,
  PlayIcon,
  RotateCcwIcon,
  XIcon,
} from "lucide-react";
import Link from "next/link";
import { type CSSProperties, useEffect, useId, useRef, useState } from "react";
import { toast } from "sonner";

import { EmptyState } from "@/components/common/states";
import { LiveInlineMarkdown, LiveMarkdown } from "@/components/live/live-markdown";
import { LiveTile, MasteryBar, OrbitArcs, SparkBurst } from "@/components/live/live-ui";
import { GenerationGate, GenerationToolbar, LiveToolShell } from "@/components/live/tool-shell";
import { Button } from "@/components/ui/button";
import { answerQuestion, finishAttempt, startAttempt } from "@/lib/api/live";
import { liveErrorMessage, useInvalidateMaterial, useLiveGeneration } from "@/lib/hooks/use-live";
import { mn } from "@/lib/i18n/mn";
import type {
  LiveAnswerResult,
  LiveAttempt,
  LiveAttemptResult,
  LiveGeneration,
  LiveQuizQuestion,
} from "@/lib/types/live";
import { cn } from "@/lib/utils";

const t = mn.live;

/** Тест (`/live/materials/[id]/quiz`, `?topic=` бол сэдвийн тест, үгүй бол бүтэн тест). */
export function LiveQuiz({ materialId, topicId }: { materialId: string; topicId: string | null }) {
  return (
    <LiveToolShell
      materialId={materialId}
      topicId={topicId}
      tool="quiz"
      fullTitle={t.quiz.fullTitle}
    >
      {() => <QuizBody materialId={materialId} topicId={topicId} />}
    </LiveToolShell>
  );
}

function QuizBody({ materialId, topicId }: { materialId: string; topicId: string | null }) {
  const state = useLiveGeneration(materialId, "quiz", topicId, true);
  return (
    <GenerationGate state={state}>
      {(generation) => (
        <div className="space-y-6">
          <GenerationToolbar state={state} />
          {/* Шинээр үүсгэвэл оролдлого шинээр эхэлнэ. */}
          <QuizRunner key={generation.id} generation={generation} materialId={materialId} />
        </div>
      )}
    </GenerationGate>
  );
}

type Phase =
  | { kind: "intro" }
  | { kind: "running"; attempt: LiveAttempt; index: number }
  | { kind: "result"; result: LiveAttemptResult };

interface Answered {
  choice: number;
  result: LiveAnswerResult;
}

/**
 * Эхлэх → асуулт нэг нэгээр (1–4 товч) → хариулмагц зөв эсэх, тайлбар, хуудас
 * → «Дараагийн» → сүүлийнхийн дараа `finishAttempt` → дүн. Хариултын түлхүүр
 * хариулт илгээсний дараа л серверээс ирнэ.
 */
function QuizRunner({
  generation,
  materialId,
}: {
  generation: LiveGeneration;
  materialId: string;
}) {
  const invalidateMaterial = useInvalidateMaterial(materialId);
  const questions = generation.quiz?.questions ?? [];
  const [phase, setPhase] = useState<Phase>({ kind: "intro" });
  const [answers, setAnswers] = useState<Record<string, Answered>>({});

  const start = useMutation({
    mutationFn: () => startAttempt(generation.id),
    onSuccess: (attempt) => {
      setAnswers({});
      setPhase({ kind: "running", attempt, index: 0 });
    },
    onError: (error) => toast.error(liveErrorMessage(error)),
  });

  const answer = useMutation({
    mutationFn: ({
      attemptId,
      question,
      choice,
    }: {
      attemptId: string;
      question: LiveQuizQuestion;
      choice: number;
    }) => answerQuestion(attemptId, question.id, choice),
    onSuccess: (result, { question, choice }) => {
      setAnswers((current) => ({ ...current, [question.id]: { choice, result } }));
    },
    onError: (error) => toast.error(liveErrorMessage(error)),
  });

  const finish = useMutation({
    mutationFn: (attemptId: string) => finishAttempt(attemptId),
    onSuccess: (result) => {
      setPhase({ kind: "result", result });
      invalidateMaterial();
    },
    onError: (error) => toast.error(liveErrorMessage(error)),
  });

  if (questions.length === 0) {
    return <EmptyState icon={ListChecksIcon} title={t.quiz.empty} />;
  }

  if (phase.kind === "intro") {
    return (
      <div className="bg-card relative isolate overflow-hidden rounded-3xl border p-8 text-center shadow-xs sm:p-12">
        <div
          aria-hidden
          className="from-primary/12 absolute inset-0 -z-10 bg-gradient-to-b via-transparent to-transparent"
        />
        {/* Тойрог замууд дүрсийг тойрно — доорх бичвэртэй давхцахгүй. */}
        <span aria-hidden className="relative mx-auto grid w-fit place-items-center">
          <OrbitArcs className="text-primary absolute top-1/2 left-1/2 -z-10 w-[18rem] max-w-none -translate-x-1/2 -translate-y-1/2 opacity-70" />
          <LiveTile className="size-16">
            <ListChecksIcon className="size-8" />
          </LiveTile>
        </span>
        <p className="mt-8 text-3xl font-bold tracking-tight tabular-nums">
          {t.quiz.questionCount(questions.length)}
        </p>
        <p className="text-muted-foreground mx-auto mt-2 max-w-md">{t.quiz.introBody}</p>
        <Button
          size="lg"
          className="group/start mt-8 min-w-40"
          disabled={start.isPending}
          onClick={() => start.mutate()}
        >
          <PlayIcon
            aria-hidden
            className="fill-current transition-[scale] group-hover/start:scale-110 motion-reduce:transition-none"
          />
          {t.quiz.start}
        </Button>
      </div>
    );
  }

  if (phase.kind === "result") {
    return (
      <QuizResult
        result={phase.result}
        materialId={materialId}
        retaking={start.isPending}
        onRetake={() => start.mutate()}
      />
    );
  }

  const { attempt, index } = phase;
  const question = questions[index];
  const answered = answers[question.id] ?? null;
  const last = index + 1 >= questions.length;

  return (
    <QuestionView
      key={question.id}
      question={question}
      index={index}
      total={questions.length}
      outcomes={questions.map((item) => answers[item.id]?.result.correct ?? null)}
      answered={answered}
      pending={answer.isPending}
      advancing={finish.isPending}
      last={last}
      onChoose={(choice) => {
        if (answered || answer.isPending) return;
        answer.mutate({ attemptId: attempt.id, question, choice });
      }}
      onNext={() => {
        if (last) finish.mutate(attempt.id);
        else setPhase({ kind: "running", attempt, index: index + 1 });
      }}
    />
  );
}

/**
 * Асуулт бүр нэг хэсэг: хариулсан нь зөв (ногоон) эсвэл буруу (улаан), одоогийнх
 * шар, үлдсэн нь саарал. Дэлгэц уншигчид — нэг `progressbar`.
 */
function QuizProgress({
  index,
  total,
  outcomes,
  value,
}: {
  index: number;
  total: number;
  outcomes: (boolean | null)[];
  value: number;
}) {
  return (
    <div
      role="progressbar"
      aria-label={t.quiz.progressLabel}
      aria-valuemin={0}
      aria-valuemax={100}
      aria-valuenow={Math.round(value)}
      className="flex gap-1"
    >
      {Array.from({ length: total }, (_, position) => {
        const outcome = outcomes[position];
        return (
          <span
            key={position}
            className={cn(
              "h-1.5 flex-1 rounded-full transition-colors duration-300 motion-reduce:transition-none",
              outcome === true && "bg-success",
              outcome === false && "bg-destructive",
              outcome === null && position === index && "bg-primary",
              outcome === null && position !== index && "bg-foreground/10",
            )}
          />
        );
      })}
    </div>
  );
}

function QuestionView({
  question,
  index,
  total,
  outcomes,
  answered,
  pending,
  advancing,
  last,
  onChoose,
  onNext,
}: {
  question: LiveQuizQuestion;
  index: number;
  total: number;
  outcomes: (boolean | null)[];
  answered: Answered | null;
  pending: boolean;
  advancing: boolean;
  last: boolean;
  onChoose: (choice: number) => void;
  onNext: () => void;
}) {
  const promptId = useId();
  const nextRef = useRef<HTMLButtonElement>(null);
  const result = answered?.result ?? null;

  // 1–4 товчоор сонгоно. Цонх, цэс нээлттэй эсвэл бичих талбарт бол юу ч хийхгүй.
  useEffect(() => {
    if (answered) return;
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.defaultPrevented || event.altKey || event.ctrlKey || event.metaKey) return;
      const target = event.target instanceof HTMLElement ? event.target : null;
      if (target?.closest("input, textarea, select, [role=dialog], [role=menu]")) return;
      const choice = Number(event.key) - 1;
      if (Number.isInteger(choice) && choice >= 0 && choice < question.options.length) {
        event.preventDefault();
        onChoose(choice);
      }
    };
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  });

  // Хариулмагц фокус «Дараагийн» товч руу — Enter дарж үргэлжлүүлнэ.
  useEffect(() => {
    if (result) nextRef.current?.focus();
  }, [result]);

  return (
    <div className="space-y-6">
      <div className="space-y-2.5">
        <div className="flex items-baseline justify-between gap-4">
          <p className="text-sm font-semibold tabular-nums">{t.quiz.question(index + 1, total)}</p>
          <p className="text-muted-foreground hidden text-xs sm:block">{t.quiz.keysHint}</p>
        </div>
        <QuizProgress
          index={index}
          total={total}
          outcomes={outcomes}
          value={((index + (result ? 1 : 0)) / total) * 100}
        />
      </div>

      <div className="bg-card motion-safe:animate-in motion-safe:slide-in-from-right-4 relative rounded-3xl border p-6 shadow-xs duration-300 sm:p-8">
        {/* Дээд ирмэгийн нарийн шар гэрэл. */}
        <span
          aria-hidden
          className="via-primary/70 absolute inset-x-10 top-0 h-px bg-gradient-to-r from-transparent to-transparent"
        />
        <h2 id={promptId} className="text-lg leading-snug font-semibold sm:text-xl">
          <LiveInlineMarkdown text={question.prompt} />
        </h2>

        <div role="group" aria-labelledby={promptId} className="mt-6 grid gap-3">
          {question.options.map((option, choice) => {
            const isCorrect = result !== null && choice === result.correct_index;
            const isWrongPick = result !== null && choice === answered?.choice && !result.correct;
            return (
              <button
                key={choice}
                type="button"
                aria-keyshortcuts={String(choice + 1)}
                // Хариулсны дараа сонголт идэвхгүй — гэхдээ бичвэр тод хэвээр.
                aria-disabled={result !== null || pending || undefined}
                onClick={() => onChoose(choice)}
                className={cn(
                  "group/option flex w-full items-start gap-3 rounded-2xl border px-4 py-3.5 text-left text-base transition-[border-color,background-color,box-shadow,translate] duration-200 outline-none motion-reduce:transition-none",
                  "focus-visible:ring-ring/50 focus-visible:ring-3",
                  result === null &&
                    "hover:border-primary/60 hover:bg-accent/50 hover:shadow-sm motion-safe:hover:translate-x-1",
                  result !== null && "cursor-default",
                  isCorrect &&
                    "border-success bg-success/10 motion-safe:animate-live-pop shadow-[0_0_0_4px_color-mix(in_oklch,var(--success)_14%,transparent)]",
                  isWrongPick &&
                    "border-destructive bg-destructive/10 motion-safe:animate-live-shake",
                )}
              >
                <kbd
                  aria-hidden
                  className={cn(
                    "bg-muted grid size-7 shrink-0 place-items-center rounded-lg font-mono text-xs font-semibold transition-colors",
                    result === null &&
                      "group-hover/option:bg-primary group-hover/option:text-primary-foreground",
                    isCorrect && "bg-success text-success-foreground",
                    isWrongPick && "bg-destructive text-white",
                  )}
                >
                  {isCorrect ? (
                    <CheckIcon className="size-4" />
                  ) : isWrongPick ? (
                    <XIcon className="size-4" />
                  ) : (
                    choice + 1
                  )}
                </kbd>
                {/* Нарийн дэлгэцэд «Зөв хариулт» шошго сонголтын доор буугаад бичвэрийг шахахгүй. */}
                <span className="flex min-w-0 flex-1 flex-wrap items-baseline justify-between gap-x-3 gap-y-1 pt-0.5">
                  <span className="min-w-0">
                    <LiveInlineMarkdown text={option} />
                  </span>
                  {isCorrect && (
                    <span className="text-success flex shrink-0 items-center gap-1 self-center text-sm font-medium">
                      <CircleCheckIcon className="size-4" aria-hidden />
                      {t.quiz.correctOption}
                    </span>
                  )}
                  {isWrongPick && (
                    <span className="text-destructive flex shrink-0 items-center gap-1 self-center text-sm font-medium">
                      <CircleXIcon className="size-4" aria-hidden />
                      {t.quiz.yourChoice}
                    </span>
                  )}
                </span>
              </button>
            );
          })}
        </div>

        <div aria-live="polite">
          {result && (
            <div
              className={cn(
                "motion-safe:animate-in motion-safe:slide-in-from-top-2 mt-6 rounded-2xl border p-4 duration-300 sm:p-5",
                result.correct
                  ? "border-success/40 bg-success/5"
                  : "border-destructive/30 bg-destructive/5",
              )}
            >
              <p
                className={cn(
                  "flex items-center gap-2 font-semibold",
                  result.correct ? "text-success" : "text-destructive",
                )}
              >
                <span
                  aria-hidden
                  className={cn(
                    "grid size-7 shrink-0 place-items-center rounded-full",
                    result.correct ? "bg-success/15" : "bg-destructive/15",
                  )}
                >
                  {result.correct ? (
                    <CircleCheckIcon className="size-4" />
                  ) : (
                    <CircleXIcon className="size-4" />
                  )}
                </span>
                {result.correct
                  ? t.quiz.correct
                  : `${t.quiz.wrong} ${t.quiz.correctAnswerIs(result.correct_index + 1)}`}
              </p>
              {result.explanation && (
                <LiveMarkdown source={result.explanation} className="mt-3 text-[0.95rem]" />
              )}
              {result.page !== null && (
                <p className="text-muted-foreground mt-2 text-xs">
                  {t.pageRef(String(result.page))}
                </p>
              )}
            </div>
          )}
        </div>
      </div>

      {result && (
        <div className="flex justify-end">
          <Button
            ref={nextRef}
            size="lg"
            className="group/next"
            disabled={advancing}
            onClick={onNext}
          >
            {last ? t.quiz.finish : t.quiz.next}
            <ArrowRightIcon
              aria-hidden
              className="transition-[translate] group-hover/next:translate-x-0.5 motion-reduce:transition-none"
            />
          </Button>
        </div>
      )}
    </div>
  );
}

function praise(percent: number): string {
  if (percent >= 80) return t.quiz.praise.high;
  if (percent >= 50) return t.quiz.praise.mid;
  return t.quiz.praise.low;
}

/** Дүнгийн том цагираг — 0-ээс дүн хүртлээ зурагдана; 80%-аас дээш бол ногоон. */
function ScoreRing({ percent }: { percent: number }) {
  const id = useId().replace(/[^a-zA-Z0-9_-]/g, "");
  const size = 176;
  const stroke = 12;
  const radius = (size - stroke) / 2;
  const length = 2 * Math.PI * radius;
  const high = percent >= 80;

  return (
    <div className="relative grid size-44 place-items-center">
      {/* Дотор нь бүтэн дэвсгэр — ард нь тойрог зам харагдахгүй. */}
      <span aria-hidden className="bg-card absolute inset-2 rounded-full shadow-inner" />
      <svg
        aria-hidden
        viewBox={`0 0 ${size} ${size}`}
        fill="none"
        className="absolute inset-0 size-full -rotate-90"
      >
        <defs>
          <linearGradient id={`${id}-score`} x1="0" y1="0" x2="1" y2="1">
            <stop offset="0" style={{ stopColor: "oklch(0.87 0.15 88)" }} />
            <stop offset="1" style={{ stopColor: "var(--primary)" }} />
          </linearGradient>
        </defs>
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          strokeWidth={stroke}
          className="stroke-foreground/10"
        />
        {percent > 0 && (
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            strokeWidth={stroke}
            strokeLinecap="round"
            strokeDasharray={length}
            strokeDashoffset={length * (1 - percent / 100)}
            className="motion-safe:animate-live-ring"
            style={
              {
                stroke: high ? "var(--success)" : `url(#${id}-score)`,
                "--ring-from": length,
              } as CSSProperties
            }
          />
        )}
      </svg>
      {/* «100%» гурван оронтой — цагирагт багтахаар жижигхэн. */}
      <p
        className={cn(
          "relative font-bold tracking-tight tabular-nums",
          percent >= 100 ? "text-[2.5rem]" : "text-5xl",
        )}
      >
        {percent}%
      </p>
    </div>
  );
}

function QuizResult({
  result,
  materialId,
  retaking,
  onRetake,
}: {
  result: LiveAttemptResult;
  materialId: string;
  retaking: boolean;
  onRetake: () => void;
}) {
  const headingRef = useRef<HTMLHeadingElement>(null);
  // Дүн гармагц фокус гарчиг дээр — дэлгэц уншигч дүнгээс эхэлж уншина.
  useEffect(() => headingRef.current?.focus(), []);
  const percent = Math.round(result.percent);
  const base = `/live/materials/${materialId}`;

  return (
    <div className="space-y-6">
      <div className="bg-card relative isolate overflow-hidden rounded-3xl border p-8 text-center shadow-xs sm:p-12">
        <div
          aria-hidden
          className="from-primary/12 absolute inset-0 -z-10 bg-gradient-to-b via-transparent to-transparent"
        />
        <h2 ref={headingRef} tabIndex={-1} className="text-lg font-semibold outline-none">
          {t.quiz.resultTitle}
        </h2>
        {/* Дүнгийн цагираг тойрог замын төвд — гараг шиг. */}
        <div className="relative mx-auto mt-6 grid w-fit place-items-center">
          <OrbitArcs className="text-primary absolute top-1/2 left-1/2 -z-10 w-[30rem] max-w-none -translate-x-1/2 -translate-y-1/2 opacity-50" />
          {percent >= 80 && <SparkBurst className="top-1/2 left-1/2" />}
          <ScoreRing percent={percent} />
        </div>
        <p className="mt-6 font-medium">{t.quiz.resultScore(result.correct_count, result.total)}</p>
        <p className="text-muted-foreground mx-auto mt-2 max-w-md text-sm">{praise(percent)}</p>
      </div>

      {result.topics.length > 0 && (
        <section
          aria-labelledby="quiz-topics-title"
          className="bg-card overflow-hidden rounded-3xl border shadow-xs"
        >
          <h3 id="quiz-topics-title" className="px-6 pt-5 pb-3 font-semibold">
            {t.quiz.byTopic}
          </h3>
          <ul className="divide-y border-t">
            {result.topics.map((topic) => (
              <li
                key={topic.topic_id}
                className="flex flex-col gap-2 px-6 py-4 sm:flex-row sm:items-center sm:gap-4"
              >
                <div className="min-w-0 flex-1">
                  <Link
                    href={`${base}/guide/${topic.topic_id}`}
                    className="text-foreground hover:text-brand-link font-medium underline-offset-4 transition-colors hover:underline"
                  >
                    {topic.title}
                  </Link>
                  <p className="text-muted-foreground text-xs">
                    {t.quiz.topicScore(topic.correct, topic.total)}
                  </p>
                </div>
                <MasteryBar
                  value={topic.mastery}
                  label={`${topic.title}: ${t.masteryValue(Math.round(topic.mastery))}`}
                  className="sm:w-48"
                />
              </li>
            ))}
          </ul>
        </section>
      )}

      <div className="flex flex-col gap-2 sm:flex-row sm:justify-end">
        <Button asChild size="lg" variant="outline">
          <Link href={base}>{t.backToSet}</Link>
        </Button>
        <Button size="lg" disabled={retaking} onClick={onRetake}>
          <RotateCcwIcon aria-hidden />
          {t.quiz.retake}
        </Button>
      </div>
    </div>
  );
}
