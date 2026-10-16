"use client";

import { ArrowRightIcon, LayersIcon, ListChecksIcon, type LucideIcon } from "lucide-react";
import Link from "next/link";
import { useEffect, useRef } from "react";

import { LiveMarkdown } from "@/components/live/live-markdown";
import { LiveTile, OrbitArcs, Spotlight, trackSpotlight } from "@/components/live/live-ui";
import { GenerationGate, GenerationToolbar, LiveToolShell } from "@/components/live/tool-shell";
import { markGuideRead } from "@/lib/api/live";
import { useInvalidateMaterial, useLiveGeneration } from "@/lib/hooks/use-live";
import { mn } from "@/lib/i18n/mn";
import type { LiveGeneration } from "@/lib/types/live";
import { cn } from "@/lib/utils";

const t = mn.live;

/** Сэдвийн заавар (`/live/materials/[id]/guide/[topicId]`). */
export function StudyGuide({ materialId, topicId }: { materialId: string; topicId: string }) {
  return (
    <LiveToolShell materialId={materialId} topicId={topicId} tool="guide" fullTitle={t.tools.guide}>
      {() => <GuideBody materialId={materialId} topicId={topicId} />}
    </LiveToolShell>
  );
}

function GuideBody({ materialId, topicId }: { materialId: string; topicId: string }) {
  const state = useLiveGeneration(materialId, "guide", topicId, true);
  return (
    <GenerationGate state={state}>
      {(generation) => (
        <div className="space-y-8">
          <GenerationToolbar state={state} />
          <GuideArticle generation={generation} materialId={materialId} topicId={topicId} />
        </div>
      )}
    </GenerationGate>
  );
}

function GuideArticle({
  generation,
  materialId,
  topicId,
}: {
  generation: LiveGeneration;
  materialId: string;
  topicId: string;
}) {
  const invalidateMaterial = useInvalidateMaterial(materialId);

  // Бэлэн заавар харагдмагц нэг удаа «уншсан» (+10% эзэмшил). Strict mode-ийн
  // давхар effect-ийг ref хаана.
  const marked = useRef<string | null>(null);
  useEffect(() => {
    if (marked.current === topicId) return;
    marked.current = topicId;
    markGuideRead(topicId)
      .then(() => invalidateMaterial())
      // Тэмдэглэж чадаагүй ч заавар уншигдана — дараагийн удаа дахин оролдоно.
      .catch(() => undefined);
  }, [topicId, invalidateMaterial]);

  const base = `/live/materials/${materialId}`;
  const topicQuery = `?topic=${encodeURIComponent(topicId)}`;

  return (
    <>
      <article className="bg-card relative rounded-3xl border p-6 shadow-xs sm:p-10">
        {/* Дээд ирмэгийн нарийн шар гэрэл. */}
        <span
          aria-hidden
          className="via-primary/70 absolute inset-x-10 top-0 h-px bg-gradient-to-r from-transparent to-transparent"
        />
        <LiveMarkdown source={generation.guide?.markdown ?? ""} className="text-[1.0625rem]" />
      </article>

      <section
        aria-labelledby="guide-next-title"
        className="bg-card relative isolate overflow-hidden rounded-3xl border p-6 shadow-xs sm:p-8"
      >
        <div
          aria-hidden
          className="from-primary/12 absolute inset-0 -z-10 bg-gradient-to-br via-transparent to-transparent"
        />
        <OrbitArcs className="text-primary absolute -top-16 -right-24 -z-10 w-[24rem] opacity-50" />
        <h2 id="guide-next-title" className="text-lg font-semibold tracking-tight">
          {t.guide.nextTitle}
        </h2>
        <p className="text-muted-foreground mt-1 text-sm">{t.guide.nextBody}</p>
        <div className="mt-6 grid gap-3 sm:grid-cols-2">
          <NextStep
            href={`${base}/cards${topicQuery}`}
            icon={LayersIcon}
            title={t.guide.toCards}
            hint={t.guide.toCardsHint}
            primary
          />
          <NextStep
            href={`${base}/quiz${topicQuery}`}
            icon={ListChecksIcon}
            title={t.guide.toQuiz}
            hint={t.guide.toQuizHint}
          />
        </div>
      </section>
    </>
  );
}

/** «Дараагийн алхам»-ын том холбоос — дүрс, нэр, эзэмшилд хэр нэмэгдэх. */
function NextStep({
  href,
  icon: Icon,
  title,
  hint,
  primary = false,
}: {
  href: string;
  icon: LucideIcon;
  title: string;
  hint: string;
  primary?: boolean;
}) {
  return (
    <Link
      href={href}
      onPointerMove={trackSpotlight}
      className={cn(
        "group/spot bg-card hover:border-primary/50 hover:shadow-primary/10 focus-visible:ring-ring/50 relative isolate flex items-center gap-4 overflow-hidden rounded-2xl border p-4 transition-[border-color,box-shadow,translate] duration-300 outline-none hover:shadow-lg focus-visible:ring-3 motion-safe:hover:-translate-y-0.5 motion-reduce:transition-none",
        primary && "border-primary/40",
      )}
    >
      <Spotlight />
      {primary ? (
        <LiveTile className="size-11 rounded-xl">
          <Icon className="size-5" />
        </LiveTile>
      ) : (
        <span
          aria-hidden
          className="bg-accent text-accent-foreground ring-primary/25 grid size-11 shrink-0 place-items-center rounded-xl ring-1 ring-inset"
        >
          <Icon className="size-5" />
        </span>
      )}
      <span className="min-w-0 flex-1">
        <span className="block font-semibold">{title}</span>
        <span className="text-muted-foreground block text-xs">{hint}</span>
      </span>
      <ArrowRightIcon
        aria-hidden
        className="text-muted-foreground group-hover/spot:text-foreground size-4 shrink-0 transition-[translate,color] group-hover/spot:translate-x-0.5 motion-reduce:transition-none"
      />
    </Link>
  );
}
