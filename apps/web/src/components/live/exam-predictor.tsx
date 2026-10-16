"use client";

import {
  BookOpenTextIcon,
  ChevronDownIcon,
  GraduationCapIcon,
  InfoIcon,
  TelescopeIcon,
} from "lucide-react";
import Link from "next/link";
import { useId, useState } from "react";

import { EmptyState } from "@/components/common/states";
import { LiveMarkdown } from "@/components/live/live-markdown";
import { EYEBROW, LikelihoodPill, LiveTile, OrbitArcs } from "@/components/live/live-ui";
import {
  GenerationGate,
  GenerationToolbar,
  LiveToolShell,
  type ToolContext,
} from "@/components/live/tool-shell";
import { useLiveGeneration } from "@/lib/hooks/use-live";
import { mn } from "@/lib/i18n/mn";
import { readLocal, writeLocal } from "@/lib/local-storage";
import { findTopic, studyPlanStorageKey } from "@/lib/live";
import type { LiveExamContent, LiveLikelihood, LiveMaterialDetail } from "@/lib/types/live";
import { cn } from "@/lib/utils";

const t = mn.live;

/** Магадлал бүрийн зүүн талын зураас ба картын тодрол — өндөр нь шараар гэрэлтэнэ. */
const LIKELIHOOD_CARD: Record<LiveLikelihood, { bar: string; card: string }> = {
  high: {
    bar: "bg-primary",
    card: "border-primary/40 shadow-[0_10px_32px_-16px_color-mix(in_oklch,var(--primary)_60%,transparent)]",
  },
  medium: { bar: "bg-primary/45", card: "" },
  low: { bar: "bg-foreground/15", card: "" },
};

/** «Шалгалтад бэлтгэх» (`/live/materials/[id]/exam`) — бүтэн материалын таамаг. */
export function ExamPredictor({ materialId }: { materialId: string }) {
  return (
    <LiveToolShell materialId={materialId} topicId={null} tool="exam" fullTitle={t.exam.title}>
      {(context) => <ExamBody context={context} />}
    </LiveToolShell>
  );
}

function ExamBody({ context }: { context: ToolContext }) {
  const { material } = context;
  const state = useLiveGeneration(material.id, "exam", null, true);
  return (
    <GenerationGate state={state}>
      {(generation) =>
        generation.exam ? (
          <div className="space-y-10">
            <div className="space-y-3">
              <GenerationToolbar state={state} />
              <p className="bg-accent/60 border-primary/25 flex items-start gap-2.5 rounded-xl border px-4 py-3 text-sm">
                <InfoIcon className="text-brand-link mt-0.5 size-4 shrink-0" aria-hidden />
                {t.exam.disclaimer}
              </p>
            </div>
            <ExamContent exam={generation.exam} material={material} />
            <StudyPlan
              key={generation.id}
              generationId={generation.id}
              items={generation.exam.study_plan}
            />
          </div>
        ) : (
          <EmptyState icon={GraduationCapIcon} title={t.exam.empty} />
        )
      }
    </GenerationGate>
  );
}

/** Сэдвийн заавар руу холбоос — таамаг сэдэвтэй холбогдсон бол. */
function TopicLink({
  material,
  topicId,
}: {
  material: LiveMaterialDetail;
  topicId: string | null;
}) {
  const ref = topicId ? findTopic(material, topicId) : null;
  if (!ref) return null;
  return (
    <Link
      href={`/live/materials/${material.id}/guide/${ref.topic.id}`}
      className="group/topic text-brand-link focus-visible:ring-ring/50 inline-flex items-center gap-1.5 rounded-md text-sm font-medium underline-offset-4 outline-none hover:underline focus-visible:ring-3"
    >
      <BookOpenTextIcon
        className="size-4 shrink-0 transition-[rotate] group-hover/topic:-rotate-6 motion-reduce:transition-none"
        aria-hidden
      />
      {t.exam.openTopic(ref.topic.title)}
    </Link>
  );
}

function ExamContent({ exam, material }: { exam: LiveExamContent; material: LiveMaterialDetail }) {
  return (
    <>
      {exam.overview && (
        <section
          aria-labelledby="exam-overview"
          className="bg-card relative isolate overflow-hidden rounded-3xl border p-6 shadow-xs sm:p-8"
        >
          <div
            aria-hidden
            className="from-primary/12 absolute inset-0 -z-10 bg-gradient-to-br via-transparent to-transparent"
          />
          <OrbitArcs className="text-primary absolute -top-16 -right-28 -z-10 w-[26rem] opacity-50" />
          <div className="flex items-center gap-3">
            <LiveTile className="size-10 rounded-xl">
              <TelescopeIcon className="size-5" />
            </LiveTile>
            <h2 id="exam-overview" className="text-lg font-semibold tracking-tight">
              {t.exam.overview}
            </h2>
          </div>
          <LiveMarkdown source={exam.overview} className="mt-4" />
        </section>
      )}

      {exam.predictions.length > 0 && (
        <section aria-labelledby="exam-predictions" className="space-y-4">
          <h2 id="exam-predictions" className="text-lg font-semibold tracking-tight">
            {t.exam.predictions}
          </h2>
          <ul className="grid gap-3 sm:grid-cols-2">
            {exam.predictions.map((prediction, index) => {
              const tone = LIKELIHOOD_CARD[prediction.likelihood];
              return (
                <li
                  key={`${index}-${prediction.title}`}
                  className={cn(
                    "bg-card relative flex flex-col gap-3 overflow-hidden rounded-2xl border p-5 pl-6 shadow-xs",
                    tone.card,
                  )}
                >
                  {/* Магадлалын өнгөт зураас — утгыг шошгоны бичвэр хэлнэ. */}
                  <span
                    aria-hidden
                    className={cn("absolute inset-y-4 left-0 w-1 rounded-r-full", tone.bar)}
                  />
                  <div className="flex flex-wrap items-start justify-between gap-2">
                    <h3 className="min-w-0 flex-1 leading-snug font-semibold">
                      {prediction.title}
                    </h3>
                    <LikelihoodPill level={prediction.likelihood} />
                  </div>
                  <p className="text-muted-foreground text-sm leading-relaxed">
                    {prediction.reason}
                  </p>
                  <div className="mt-auto">
                    <TopicLink material={material} topicId={prediction.topic_id} />
                  </div>
                </li>
              );
            })}
          </ul>
        </section>
      )}

      {exam.questions.length > 0 && (
        <section aria-labelledby="exam-questions" className="space-y-4">
          <h2 id="exam-questions" className="text-lg font-semibold tracking-tight">
            {t.exam.questions}
          </h2>
          <ol className="space-y-3">
            {exam.questions.map((question, index) => (
              <ExamQuestionItem
                key={`${index}-${question.question}`}
                number={index + 1}
                question={question}
                material={material}
              />
            ))}
          </ol>
        </section>
      )}
    </>
  );
}

function ExamQuestionItem({
  number,
  question,
  material,
}: {
  number: number;
  question: LiveExamContent["questions"][number];
  material: LiveMaterialDetail;
}) {
  const [open, setOpen] = useState(false);
  const panelId = useId();

  return (
    <li className="bg-card rounded-2xl border p-5 shadow-xs sm:p-6">
      <div className="flex gap-4">
        {/* Дугаарыг жагсаалт (`ol`) өөрөө хэлнэ. */}
        <span
          aria-hidden
          className="bg-accent text-accent-foreground ring-primary/25 grid size-9 shrink-0 place-items-center rounded-xl text-sm font-bold tabular-nums ring-1 ring-inset"
        >
          {number}
        </span>
        <div className="min-w-0 flex-1">
          <div className="flex flex-wrap items-center gap-2">
            <span className={EYEBROW}>{t.exam.types[question.type]}</span>
            <LikelihoodPill level={question.likelihood} />
          </div>
          <p className="mt-2 leading-relaxed font-medium">{question.question}</p>
          <div className="mt-4 flex flex-wrap items-center justify-between gap-3">
            <button
              type="button"
              aria-expanded={open}
              aria-controls={panelId}
              onClick={() => setOpen((value) => !value)}
              className="text-brand-link hover:bg-accent focus-visible:ring-ring/50 aria-expanded:bg-accent inline-flex items-center gap-1.5 rounded-full border px-3 py-1.5 text-sm font-semibold transition-colors outline-none focus-visible:ring-3 motion-reduce:transition-none"
            >
              <ChevronDownIcon
                aria-hidden
                className={cn(
                  "size-4 transition-transform duration-200 motion-reduce:transition-none",
                  open && "rotate-180",
                )}
              />
              {t.exam.answerOutline}
            </button>
            <TopicLink material={material} topicId={question.topic_id} />
          </div>
          <div
            id={panelId}
            hidden={!open}
            className="bg-muted/50 border-primary/60 motion-safe:animate-in motion-safe:slide-in-from-top-1 mt-4 rounded-xl border-l-2 p-4 duration-200"
          >
            <LiveMarkdown source={question.answer_outline} className="text-[0.95rem]" />
          </div>
        </div>
      </div>
    </li>
  );
}

/** Бэлтгэлийн төлөвлөгөө — тэмдэглэгээ зөвхөн энэ хөтөчид (`localStorage`). */
function StudyPlan({ generationId, items }: { generationId: string; items: string[] }) {
  const storageKey = studyPlanStorageKey(generationId);
  // `RequireAuth` нэвтрэлт тодортол fallback харуулдаг тул энэ нь зөвхөн
  // browser дээр render хийгдэнэ — `localStorage`-ийг шууд уншиж болно.
  const [done, setDone] = useState<number[]>(() => {
    try {
      const value: unknown = JSON.parse(readLocal(storageKey, "[]"));
      return Array.isArray(value) ? value.filter((item) => typeof item === "number") : [];
    } catch {
      return [];
    }
  });
  const baseId = useId();

  if (items.length === 0) return null;

  const toggle = (index: number, checked: boolean) => {
    const next = checked ? [...done, index] : done.filter((item) => item !== index);
    setDone(next);
    writeLocal(storageKey, JSON.stringify(next));
  };
  const doneCount = items.filter((_, index) => done.includes(index)).length;
  const complete = doneCount === items.length;

  return (
    <section
      aria-labelledby="exam-plan"
      className="bg-card rounded-3xl border p-6 shadow-xs sm:p-8"
    >
      <div className="flex flex-wrap items-baseline justify-between gap-2">
        <h2 id="exam-plan" className="text-lg font-semibold tracking-tight">
          {t.exam.plan}
        </h2>
        <p className="text-muted-foreground text-sm tabular-nums" aria-live="polite">
          {t.exam.planProgress(doneCount, items.length)}
        </p>
      </div>
      {/* Хийсэн хувь — утгыг дээрх бичвэр хэлнэ. */}
      <div aria-hidden className="bg-foreground/10 mt-4 h-1.5 overflow-hidden rounded-full">
        <div
          className={cn(
            "h-full rounded-full transition-[width] duration-500 ease-out motion-reduce:transition-none",
            complete ? "bg-success" : "from-primary bg-gradient-to-r to-amber-300",
          )}
          style={{ width: `${(doneCount / items.length) * 100}%` }}
        />
      </div>
      <ul className="mt-5 space-y-2">
        {items.map((item, index) => {
          const id = `${baseId}-${index}`;
          const checked = done.includes(index);
          return (
            <li key={id}>
              <label
                htmlFor={id}
                className={cn(
                  "hover:bg-muted/50 flex cursor-pointer items-start gap-3 rounded-xl border px-4 py-3 text-sm leading-relaxed transition-colors motion-reduce:transition-none",
                  "has-[:focus-visible]:ring-ring/50 has-[:focus-visible]:ring-3",
                  checked && "border-success/30 bg-success/5 hover:bg-success/10",
                )}
              >
                <input
                  id={id}
                  type="checkbox"
                  checked={checked}
                  onChange={(event) => toggle(index, event.target.checked)}
                  className="accent-primary mt-0.5 size-4 shrink-0"
                />
                <span className={cn(checked && "text-muted-foreground line-through")}>{item}</span>
              </label>
            </li>
          );
        })}
      </ul>
      <p className="text-muted-foreground mt-3 text-xs">{t.exam.planHint}</p>
    </section>
  );
}
