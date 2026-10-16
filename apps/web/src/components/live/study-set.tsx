"use client";

import {
  ArrowRightIcon,
  CircleXIcon,
  GraduationCapIcon,
  ListChecksIcon,
  RotateCcwIcon,
  UploadIcon,
} from "lucide-react";
import Link from "next/link";

import { EmptyState, ErrorState } from "@/components/common/states";
import { LiveMark } from "@/components/live/live-mark";
import {
  AiLabel,
  EYEBROW,
  LiveBackLink,
  LiveTile,
  MasteryHelp,
  MasteryRing,
  MaterialKindIcon,
  OrbitArcs,
  ShimmerBar,
  Spotlight,
  TOOL_ICONS,
  trackSpotlight,
  usePendingAnnouncement,
} from "@/components/live/live-ui";
import { SectionCard } from "@/components/live/topic-sections";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { ApiError } from "@/lib/api/client";
import { formatDate } from "@/lib/format";
import { liveErrorMessage, useLiveMaterial, useRetryMaterial } from "@/lib/hooks/use-live";
import { mn } from "@/lib/i18n/mn";
import { isGenerating, isMaterialProcessing } from "@/lib/live";
import type { LiveCardStats, LiveGenerationBrief, LiveMaterialDetail } from "@/lib/types/live";
import { cn } from "@/lib/utils";

const t = mn.live;

/**
 * Судлах сет (`/live/materials/[id]`): материалын толгой, хэсэг → сэдэв →
 * эзэмшил, баруун талд бүтэн материалын хэрэгслүүд. Утсан дээр нэг багана —
 * хэрэгслүүд товч агуулга ба хэсгүүдийн хооронд.
 *
 * AI задалж байх зуур 3 сек тутам шалгана (`useLiveMaterial`); бэлэн болоход
 * дэлгэц уншигчид мэдэгдэнэ.
 */
export function StudySet({ materialId }: { materialId: string }) {
  const query = useLiveMaterial(materialId);
  const status = query.data?.status;
  const announcement = usePendingAnnouncement(
    isMaterialProcessing(status),
    t.processingTitle,
    status === "ready" ? t.readyAnnounce : status === "failed" ? t.failedTitle : "",
  );

  const live = (
    <p role="status" className="sr-only">
      {announcement}
    </p>
  );

  if (query.isPending) {
    return (
      <>
        {live}
        <StudySetSkeleton />
      </>
    );
  }

  if (query.isError) {
    return (
      <>
        {live}
        <MaterialLoadError error={query.error} onRetry={() => void query.refetch()} />
      </>
    );
  }

  const material = query.data;

  return (
    // Бэлэн болоогүй үед нэг нарийн багана — буцах холбоос ч түүнтэй зэрэгцэнэ.
    <div className={cn("space-y-6", material.status !== "ready" && "mx-auto max-w-3xl")}>
      {live}
      <LiveBackLink href="/live" label={t.backToLive} />
      {material.status === "ready" ? (
        <ReadyStudySet material={material} />
      ) : (
        <>
          <MaterialHero material={material} />
          <MaterialPending material={material} />
        </>
      )}
    </div>
  );
}

/** 404 (устгагдсан, эсвэл Live хаалттай) — энгийн мэдэгдэл; бусад алдаа — дахин оролдох. */
export function MaterialLoadError({ error, onRetry }: { error: unknown; onRetry: () => void }) {
  if (error instanceof ApiError && error.isNotFound) {
    return (
      <EmptyState
        icon={GraduationCapIcon}
        title={t.notFound}
        description={t.notFoundBody}
        className="py-20"
        action={
          <Button asChild variant="outline">
            <Link href="/live">{t.backToLive}</Link>
          </Button>
        }
      />
    );
  }
  return <ErrorState description={liveErrorMessage(error)} onRetry={onRetry} />;
}

function ReadyStudySet({ material }: { material: LiveMaterialDetail }) {
  return (
    // DOM-ийн дараалал: толгой → хэрэгслүүд → хэсгүүд. Том дэлгэцэд хэрэгслүүд
    // баруун баганад наалдана.
    <div className="grid gap-8 lg:grid-cols-[minmax(0,1fr)_20rem] lg:items-start lg:gap-10 xl:grid-cols-[minmax(0,1fr)_22rem]">
      <MaterialHero material={material} className="lg:col-start-1" />

      <aside
        aria-labelledby="live-full-set-title"
        className="space-y-4 lg:sticky lg:top-24 lg:col-start-2 lg:row-span-2 lg:row-start-1"
      >
        <h2 id="live-full-set-title" className={EYEBROW}>
          {t.fullSetTitle}
        </h2>
        <FullSetTools material={material} />
      </aside>

      <div className="space-y-5 lg:col-start-1">
        <h2 className="sr-only">{t.sectionsTitle}</h2>
        {material.sections.length === 0 ? (
          <EmptyState icon={ListChecksIcon} title={t.noTopics} />
        ) : (
          material.sections.map((section, index) => (
            <SectionCard
              key={`${index}-${section.title}`}
              section={section}
              number={index + 1}
              materialId={material.id}
              lastStudiedTopicId={material.last_studied_topic_id}
            />
          ))
        )}
      </div>
    </div>
  );
}

/**
 * Гарчиг, төрөл, хуудас, AI-ийн товч агуулга, нийт эзэмшлийн цагираг. Ард нь
 * бүдэг тор, шар туяа, тойрог замууд.
 */
function MaterialHero({
  material,
  className,
}: {
  material: LiveMaterialDetail;
  className?: string;
}) {
  const ready = material.status === "ready";
  const meta = [
    t.kinds[material.kind],
    material.page_count ? t.pageCount(material.page_count) : null,
    ready ? t.topicCount(material.topic_count) : null,
    t.addedOn(formatDate(material.created_at)),
  ].filter(Boolean);

  return (
    <header
      className={cn(
        "bg-card relative isolate overflow-hidden rounded-3xl border p-6 shadow-xs sm:p-8",
        className,
      )}
    >
      <div
        aria-hidden
        className="from-primary/12 absolute inset-0 -z-10 bg-gradient-to-br via-transparent to-transparent"
      />
      <div aria-hidden className="live-grid absolute inset-0 -z-10 [--live-grid-at:100%_0%]" />
      <OrbitArcs className="text-primary absolute -top-24 -right-36 -z-10 w-[28rem] opacity-50 sm:-right-24" />

      <div className="flex items-center gap-3">
        <MaterialKindIcon kind={material.kind} className="bg-card size-11 shadow-sm" />
        <p className="text-muted-foreground text-sm">{meta.join(" · ")}</p>
      </div>
      <h1 className="mt-5 max-w-3xl text-2xl font-bold tracking-tight text-balance sm:text-3xl lg:text-4xl">
        {material.title}
      </h1>

      {material.summary && (
        <div className="mt-5 space-y-2">
          <div className="flex flex-wrap items-center gap-2">
            <h2 className="text-sm font-semibold">{t.summaryTitle}</h2>
            <AiLabel />
          </div>
          <p className="text-foreground/85 max-w-prose leading-relaxed">{material.summary}</p>
        </div>
      )}

      {ready && (
        <div className="mt-6 flex items-center gap-5 border-t pt-6">
          <MasteryRing
            value={material.mastery}
            label={t.overallMastery}
            size={84}
            stroke={8}
            valueClassName="text-lg"
          />
          <div className="min-w-0 space-y-2">
            <p className={EYEBROW}>{t.overallMastery}</p>
            <MasteryHelp />
          </div>
        </div>
      )}
    </header>
  );
}

/** Задлагдаж буй, илгээлт тасарсан, эсвэл амжилтгүй болсон материал. */
function MaterialPending({ material }: { material: LiveMaterialDetail }) {
  const retry = useRetryMaterial(material.id);

  if (material.status === "failed") {
    return (
      <div className="border-destructive/30 bg-destructive/5 rounded-3xl border p-6 text-center sm:p-8">
        <span
          aria-hidden
          className="bg-destructive/10 text-destructive mx-auto grid size-12 place-items-center rounded-2xl"
        >
          <CircleXIcon className="size-6" />
        </span>
        <p className="mt-4 font-semibold">{t.failedTitle}</p>
        <p className="text-muted-foreground mx-auto mt-2 max-w-md text-sm">
          {material.error_message ?? t.failedFallback}
        </p>
        <Button className="mt-6" disabled={retry.isPending} onClick={() => retry.mutate()}>
          <RotateCcwIcon />
          {t.retry}
        </Button>
      </div>
    );
  }

  if (material.status === "uploading") {
    return (
      <EmptyState
        icon={UploadIcon}
        title={t.uploadingTitle}
        description={t.uploadingBody}
        action={
          <Button asChild variant="outline">
            <Link href="/live">{t.backToLive}</Link>
          </Button>
        }
      />
    );
  }

  return (
    <div className="bg-card relative isolate overflow-hidden rounded-3xl border p-6 sm:p-8">
      <div
        aria-hidden
        className="from-primary/10 absolute inset-0 -z-10 bg-gradient-to-br via-transparent to-transparent"
      />
      <div className="flex items-start gap-4">
        <LiveTile>
          <LiveMark animated className="size-7" />
        </LiveTile>
        <div>
          <p className="font-semibold">{t.processingTitle}</p>
          <p className="text-muted-foreground mt-1 text-sm">{t.processingBody}</p>
        </div>
      </div>
      {/* AI материалыг «уншиж» буй мэт — мөрүүдээр гэрэл гүйж, скан доош явна. */}
      <div className="relative mt-8 space-y-3 overflow-hidden rounded-2xl" aria-hidden>
        <ShimmerBar className="h-14 w-full rounded-2xl" />
        <ShimmerBar className="h-20 w-full rounded-2xl" />
        <ShimmerBar className="h-20 w-full rounded-2xl" />
        <span className="motion-safe:animate-live-scan absolute inset-0 motion-reduce:hidden">
          <span className="from-primary/0 to-primary/20 border-primary/60 absolute inset-x-0 top-0 h-1/3 border-b-2 bg-gradient-to-b" />
        </span>
      </div>
    </div>
  );
}

type StatusTone = "idle" | "progress" | "due" | "ready" | "error";

interface ToolStatus {
  text: string;
  tone: StatusTone;
}

function cardsStatus(cards: LiveCardStats): ToolStatus {
  if (cards.total === 0) return { text: t.toolStatus.empty, tone: "idle" };
  if (cards.new === cards.total) return { text: t.toolStatus.notStarted, tone: "idle" };
  if (cards.due > 0) return { text: t.toolStatus.due(cards.due), tone: "due" };
  return { text: t.toolStatus.done, tone: "ready" };
}

function generationStatus(brief: LiveGenerationBrief | null): ToolStatus {
  if (!brief) return { text: t.toolStatus.notStarted, tone: "idle" };
  if (isGenerating(brief.status)) return { text: t.toolStatus.preparing, tone: "progress" };
  return brief.status === "ready"
    ? { text: t.toolStatus.ready, tone: "ready" }
    : { text: t.toolStatus.failed, tone: "error" };
}

/** Төлөвийн өнгө (бичвэр, цэг). «Давтах», «Бэлтгэж байна» үед цэг лугшина. */
const TONES: Record<StatusTone, { text: string; dot: string; pulse: boolean }> = {
  idle: { text: "", dot: "bg-muted-foreground", pulse: false },
  progress: { text: "text-accent-foreground", dot: "bg-primary", pulse: true },
  due: { text: "text-accent-foreground", dot: "bg-primary", pulse: true },
  ready: { text: "text-success", dot: "bg-success", pulse: false },
  error: { text: "text-destructive", dot: "bg-destructive", pulse: false },
};

/** Бүтэн картууд, бүтэн тест, шалгалтад бэлтгэх. */
function FullSetTools({ material }: { material: LiveMaterialDetail }) {
  const base = `/live/materials/${material.id}`;
  return (
    <ul className="space-y-4">
      <li>
        <ToolCard
          href={`${base}/cards`}
          tool="cards"
          title={t.fullCards}
          body={t.fullCardsBody(material.cards.total)}
          status={cardsStatus(material.cards)}
        />
      </li>
      <li>
        <ToolCard
          href={`${base}/quiz`}
          tool="quiz"
          title={t.fullQuiz}
          body={t.fullQuizBody}
          status={generationStatus(material.full_quiz)}
        />
      </li>
      <li>
        <ToolCard
          href={`${base}/exam`}
          tool="exam"
          title={t.examCard}
          body={t.examCardBody}
          status={generationStatus(material.exam)}
        />
      </li>
    </ul>
  );
}

function ToolCard({
  href,
  tool,
  title,
  body,
  status,
}: {
  href: string;
  tool: keyof typeof TOOL_ICONS;
  title: string;
  body: string;
  status: ToolStatus;
}) {
  const Icon = TOOL_ICONS[tool];
  const tone = TONES[status.tone];
  return (
    // Утсан дээр дүрс зүүн талд — гурван карт хэсгүүдийг хэт доош түлхэхгүй.
    <Link
      href={href}
      onPointerMove={trackSpotlight}
      className="group/spot bg-card hover:border-primary/50 hover:shadow-primary/10 focus-visible:ring-ring/50 relative isolate flex items-start gap-4 overflow-hidden rounded-2xl border p-5 shadow-xs transition-[border-color,box-shadow,translate] duration-300 outline-none hover:shadow-lg focus-visible:ring-3 motion-safe:hover:-translate-y-0.5 motion-reduce:transition-none lg:block"
    >
      <Spotlight />
      <span
        aria-hidden
        className="bg-accent text-accent-foreground ring-primary/25 grid size-11 shrink-0 place-items-center rounded-xl ring-1 transition-[scale,rotate] duration-500 ease-[cubic-bezier(0.34,1.56,0.64,1)] ring-inset group-hover/spot:scale-110 motion-safe:group-hover/spot:-rotate-6 motion-reduce:transition-none"
      >
        <Icon className="size-5" />
      </span>
      <span
        aria-hidden
        className="bg-muted text-muted-foreground group-hover/spot:bg-primary group-hover/spot:text-primary-foreground absolute top-4 right-4 grid size-7 place-items-center rounded-full transition-colors duration-300"
      >
        <ArrowRightIcon className="size-3.5 transition-[translate] group-hover/spot:translate-x-0.5 motion-reduce:transition-none" />
      </span>
      <div className="min-w-0 pr-8 lg:pr-0">
        <h3 className="text-lg leading-snug font-semibold lg:mt-4">{title}</h3>
        <p className="text-muted-foreground mt-1 text-sm">{body}</p>
        <p className={cn(EYEBROW, "mt-3 flex items-center gap-2", tone.text)}>
          <span aria-hidden className="relative flex size-2">
            {tone.pulse && (
              <span
                className={cn(
                  // Гурван удаа л — тасралтгүй анивчихгүй (WCAG 2.2.2).
                  "absolute inset-0 rounded-full motion-safe:animate-ping motion-safe:[animation-iteration-count:3]",
                  tone.dot,
                )}
              />
            )}
            <span className={cn("relative size-2 rounded-full", tone.dot)} />
          </span>
          {status.text}
        </p>
      </div>
    </Link>
  );
}

export function StudySetSkeleton() {
  return (
    <div
      className="grid gap-8 lg:grid-cols-[minmax(0,1fr)_20rem] lg:gap-10 xl:grid-cols-[minmax(0,1fr)_22rem]"
      aria-hidden
    >
      <div className="space-y-5">
        <Skeleton className="h-5 w-40" />
        <Skeleton className="h-64 w-full rounded-3xl" />
        <Skeleton className="h-64 w-full rounded-2xl" />
      </div>
      <div className="space-y-4">
        <Skeleton className="h-40 w-full rounded-2xl" />
        <Skeleton className="h-40 w-full rounded-2xl" />
        <Skeleton className="h-40 w-full rounded-2xl" />
      </div>
    </div>
  );
}
