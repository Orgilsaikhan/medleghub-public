"use client";

import { ClockIcon, RefreshCwIcon, SearchXIcon } from "lucide-react";
import Link from "next/link";
import { useEffect, useRef, useState, type ReactNode } from "react";

import { EmptyState, ErrorState } from "@/components/common/states";
import { LiveMark } from "@/components/live/live-mark";
import { MaterialLoadError } from "@/components/live/study-set";
import {
  AiLabel,
  LiveBackLink,
  LiveTile,
  MasteryRing,
  OrbitArcs,
  ShimmerBar,
  TOOL_ICONS,
  usePendingAnnouncement,
} from "@/components/live/live-ui";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Skeleton } from "@/components/ui/skeleton";
import { liveErrorMessage, useLiveMaterial, type useLiveGeneration } from "@/lib/hooks/use-live";
import { mn } from "@/lib/i18n/mn";
import { findTopic, formatPages, isGenerating, type TopicRef } from "@/lib/live";
import type { LiveGeneration, LiveMaterialDetail } from "@/lib/types/live";
import { cn } from "@/lib/utils";

const t = mn.live;

export interface ToolContext {
  material: LiveMaterialDetail;
  /** Сэдвийн хэрэгсэл бол; бүтэн материалынх бол `null`. */
  topic: TopicRef | null;
}

/** Хэрэгслийн хуудас — дээд талын шилжүүлэгчид аль нь идэвхтэйг заана. */
export type LiveToolKey = keyof typeof TOOL_ICONS;

/**
 * Заавар, карт, тест, таамгийн хуудасны нийтлэг хүрээ: материал ачаалах,
 * олдоогүй / бэлэн болоогүй төлөв, «← материал» холбоос, хэрэгсэл хооронд
 * шилжих мөр, гарчиг. Хэрэгсэл өөрөө (`children`) зөвхөн материал бэлэн, сэдэв
 * олдсон үед mount хийгдэнэ.
 */
export function LiveToolShell({
  materialId,
  topicId,
  tool,
  fullTitle,
  children,
}: {
  materialId: string;
  topicId: string | null;
  tool: LiveToolKey;
  /** Бүтэн материалын (сэдэвгүй) хуудасны гарчиг. */
  fullTitle: string;
  children: (context: ToolContext) => ReactNode;
}) {
  const query = useLiveMaterial(materialId);

  if (query.isPending) return <ToolSkeleton />;
  if (query.isError) {
    return (
      <div className="mx-auto max-w-3xl">
        <MaterialLoadError error={query.error} onRetry={() => void query.refetch()} />
      </div>
    );
  }

  const material = query.data;
  const topic = topicId ? findTopic(material, topicId) : null;
  const setHref = `/live/materials/${material.id}`;
  const backToSet = (
    <Button asChild variant="outline">
      <Link href={setHref}>{t.backToSet}</Link>
    </Button>
  );

  let body: ReactNode;
  if (material.status !== "ready") {
    body = (
      <EmptyState
        icon={ClockIcon}
        title={t.notReadyTitle}
        description={t.notReadyBody}
        action={backToSet}
      />
    );
  } else if (topicId && !topic) {
    body = (
      <EmptyState
        icon={SearchXIcon}
        title={t.topicNotFound}
        description={t.topicNotFoundBody}
        action={backToSet}
      />
    );
  } else {
    body = children({ material, topic });
  }

  const pages = topic ? formatPages(topic.topic.pages) : "";
  // Олдоогүй сэдвийн хуудсанд шилжүүлэгч хэрэггүй.
  const showNav = material.status === "ready" && !(topicId && !topic);

  return (
    <div className="mx-auto max-w-3xl">
      <LiveBackLink href={setHref} label={material.title} />
      <header className="relative isolate mt-6">
        {/* Гарчгийн ард зөөлөн шар гэрэл ба бүдэг тойрог замууд (хуудас хайчилна). */}
        <span
          aria-hidden
          className="bg-primary/15 pointer-events-none absolute -top-24 -left-24 -z-10 size-72 rounded-full blur-3xl"
        />
        <OrbitArcs className="text-primary absolute -top-20 -right-36 -z-10 w-[26rem] opacity-50 sm:-right-28" />

        {showNav && <ToolNav tool={tool} material={material} topic={topic} />}
        <div className="mt-5 flex flex-wrap items-center justify-between gap-x-4 gap-y-3">
          <h1 className="min-w-0 text-2xl font-bold tracking-tight text-balance sm:text-3xl">
            {topic ? topic.topic.title : fullTitle}
          </h1>
          {topic && (
            <MasteryRing
              value={topic.topic.mastery}
              label={t.mastery}
              size={52}
              stroke={5}
              valueClassName="text-xs"
            />
          )}
        </div>
        {topic && (
          <p className="text-muted-foreground mt-2 text-sm">
            {t.sectionHeading(topic.sectionNumber, topic.section.title)}
            {pages && ` · ${t.pageRef(pages)}`}
          </p>
        )}
      </header>
      <div className="mt-8">{body}</div>
    </div>
  );
}

/**
 * Хэрэгсэл хооронд шилжих мөр: сэдвийнх (Заавар / Картууд / Тест) эсвэл бүтэн
 * материалынх. Нарийн дэлгэцэд хажуу тийш гүйлгэгдэнэ — идэвхтэйг нь харагдах
 * хэсэгт байрлуулна.
 */
function ToolNav({
  tool,
  material,
  topic,
}: {
  tool: LiveToolKey;
  material: LiveMaterialDetail;
  topic: TopicRef | null;
}) {
  const scrollerRef = useRef<HTMLElement>(null);
  const base = `/live/materials/${material.id}`;
  const items: { key: LiveToolKey; href: string; label: string }[] = topic
    ? [
        { key: "guide", href: `${base}/guide/${topic.topic.id}`, label: t.tools.guide },
        {
          key: "cards",
          href: `${base}/cards?topic=${encodeURIComponent(topic.topic.id)}`,
          label: t.tools.cards,
        },
        {
          key: "quiz",
          href: `${base}/quiz?topic=${encodeURIComponent(topic.topic.id)}`,
          label: t.tools.quiz,
        },
      ]
    : [
        { key: "cards", href: `${base}/cards`, label: t.fullCards },
        { key: "quiz", href: `${base}/quiz`, label: t.fullQuiz },
        { key: "exam", href: `${base}/exam`, label: t.examCard },
      ];

  useEffect(() => {
    const scroller = scrollerRef.current;
    const current = scroller?.querySelector<HTMLElement>("[aria-current=page]");
    if (!scroller || !current) return;
    // Хуудсыг босоо гүйлгэхгүй — зөвхөн энэ мөрийг.
    scroller.scrollLeft = current.offsetLeft - (scroller.clientWidth - current.offsetWidth) / 2;
  }, [tool]);

  return (
    <nav
      ref={scrollerRef}
      aria-label={topic ? t.studyWith : t.fullSetTitle}
      className="relative -mx-1 [scrollbar-width:none] overflow-x-auto px-1 py-1 [&::-webkit-scrollbar]:hidden"
    >
      <ul className="bg-muted/70 inline-flex gap-1 rounded-full border p-1 shadow-xs backdrop-blur-sm">
        {items.map((item) => {
          const Icon = TOOL_ICONS[item.key];
          const current = item.key === tool;
          // Бүтэн материалын нэрс урт — утсан дээр идэвхгүй нь зөвхөн дүрстэй.
          const compact = !topic && !current;
          return (
            <li key={item.key}>
              <Link
                href={item.href}
                aria-current={current ? "page" : undefined}
                className={cn(
                  "focus-visible:ring-ring/50 inline-flex items-center gap-1.5 rounded-full py-1.5 text-sm font-medium whitespace-nowrap transition-[color,background-color,box-shadow] outline-none focus-visible:ring-3 motion-reduce:transition-none",
                  compact ? "px-2.5 sm:px-3.5" : "px-3.5",
                  current
                    ? "bg-card text-foreground ring-border shadow-sm ring-1"
                    : "text-muted-foreground hover:bg-card/70 hover:text-foreground",
                )}
              >
                <Icon className={cn("size-4", current && "text-brand-link")} aria-hidden />
                <span className={cn(compact && "sr-only sm:not-sr-only")}>{item.label}</span>
              </Link>
            </li>
          );
        })}
      </ul>
    </nav>
  );
}

function ToolSkeleton() {
  return (
    <div className="mx-auto max-w-3xl space-y-6" aria-hidden>
      <Skeleton className="h-5 w-48" />
      <Skeleton className="h-10 w-72 rounded-full" />
      <Skeleton className="h-10 w-3/4" />
      <Skeleton className="h-72 w-full rounded-3xl" />
    </div>
  );
}

type GenerationState = ReturnType<typeof useLiveGeneration>;

/**
 * AI-ийн үүсгэлтийн төлөв: захиалгын алдаа (хязгаар, AI унтраалттай) →
 * «AI бэлтгэж байна…» → амжилтгүй бол «Дахин оролдох» → бэлэн бол `children`.
 * «Бэлтгэж байна» → «бэлэн» шилжилтийг дэлгэц уншигчид мэдэгдэнэ.
 */
export function GenerationGate({
  state,
  children,
}: {
  state: GenerationState;
  children: (generation: LiveGeneration) => ReactNode;
}) {
  const { request, generation, regenerate } = state;
  const pending =
    !request.isError && (!generation || isGenerating(generation.status) || regenerate.isPending);
  const announcement = usePendingAnnouncement(
    pending,
    t.generating,
    generation?.status === "ready" ? mn.live.status.ready : "",
  );

  let body: ReactNode;
  if (request.isError) {
    body = (
      <ErrorState
        title={t.generationFailed}
        description={liveErrorMessage(request.error)}
        onRetry={() => void request.refetch()}
      />
    );
  } else if (pending || !generation) {
    body = <GenerationPending />;
  } else if (generation.status === "failed") {
    body = (
      <ErrorState
        title={t.generationFailed}
        description={generation.error_message ?? mn.common.somethingWrong}
        onRetry={() => regenerate.mutate()}
      />
    );
  } else {
    body = children(generation);
  }

  return (
    <>
      <p role="status" className="sr-only">
        {announcement}
      </p>
      {body}
    </>
  );
}

/** «AI бэлтгэж байна…» — Live-ийн тэмдгийн сар эргэнэ, мөрүүдээр гялбаа гүйнэ. */
function GenerationPending() {
  return (
    <div className="bg-card relative isolate overflow-hidden rounded-3xl border p-6 shadow-xs sm:p-8">
      <div
        aria-hidden
        className="from-primary/10 absolute inset-0 -z-10 bg-gradient-to-br via-transparent to-transparent"
      />
      <div className="flex items-start gap-4">
        <LiveTile>
          <LiveMark animated className="size-7" />
        </LiveTile>
        <div>
          <p className="font-semibold">{t.generating}</p>
          <p className="text-muted-foreground mt-1 text-sm">{t.generatingBody}</p>
        </div>
      </div>
      <div className="mt-8 space-y-3" aria-hidden>
        <ShimmerBar className="h-6 w-2/3" />
        <ShimmerBar className="h-4 w-full" />
        <ShimmerBar className="h-4 w-11/12" />
        <ShimmerBar className="h-4 w-4/5" />
        <ShimmerBar className="mt-6 h-6 w-1/2" />
        <ShimmerBar className="h-4 w-full" />
        <ShimmerBar className="h-4 w-3/4" />
      </div>
    </div>
  );
}

/**
 * «AI бэлтгэсэн» шошго + «Шинээр үүсгэх». Шинээр үүсгэх нь AI хэрэглээнээс
 * хасагддаг тул үргэлж баталгаажуулна.
 */
export function GenerationToolbar({ state, extra }: { state: GenerationState; extra?: ReactNode }) {
  const [open, setOpen] = useState(false);
  return (
    <div className="flex flex-wrap items-center justify-between gap-3">
      <div className="flex flex-wrap items-center gap-2">
        <AiLabel />
        {extra}
      </div>
      <Dialog open={open} onOpenChange={setOpen}>
        <Button
          variant="ghost"
          size="sm"
          className="text-muted-foreground"
          disabled={state.regenerate.isPending}
          onClick={() => setOpen(true)}
        >
          <RefreshCwIcon aria-hidden />
          {t.regenerate}
        </Button>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>{t.regenerateTitle}</DialogTitle>
            <DialogDescription>{t.regenerateBody}</DialogDescription>
          </DialogHeader>
          <DialogFooter>
            <Button variant="outline" onClick={() => setOpen(false)}>
              {t.cancel}
            </Button>
            <Button
              onClick={() => {
                setOpen(false);
                state.regenerate.mutate();
              }}
            >
              {t.regenerateConfirm}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}
