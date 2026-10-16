"use client";

import { useMutation, useQuery } from "@tanstack/react-query";
import {
  CheckIcon,
  CircleCheckIcon,
  CircleHelpIcon,
  LayersIcon,
  type LucideIcon,
  MousePointerClickIcon,
  RotateCcwIcon,
  TrophyIcon,
} from "lucide-react";
import Link from "next/link";
import { useEffect, useId, useRef, useState, type Ref } from "react";
import { toast } from "sonner";

import { EmptyState, ErrorState } from "@/components/common/states";
import { LiveInlineMarkdown } from "@/components/live/live-markdown";
import { LiveTile, SparkBurst } from "@/components/live/live-ui";
import { LiveToolShell } from "@/components/live/tool-shell";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { Skeleton } from "@/components/ui/skeleton";
import { listCards, reviewCard } from "@/lib/api/live";
import { liveErrorMessage, useInvalidateMaterial } from "@/lib/hooks/use-live";
import { mn } from "@/lib/i18n/mn";
import { queryKeys } from "@/lib/query-keys";
import type { LiveCard, LiveCardRating } from "@/lib/types/live";
import { cn } from "@/lib/utils";

const t = mn.live;

/** Товчлуур 1, 2, 3-ын дараалал. */
const RATINGS: LiveCardRating[] = ["again", "hard", "good"];
const EMPTY_TALLY: Record<LiveCardRating, number> = { again: 0, hard: 0, good: 0 };

/** Үнэлгээ бүрийн дүрс, хулгана дээрх өнгө. «Мэднэ» — үндсэн (шар) товч. */
const RATING_META: Record<LiveCardRating, { icon: LucideIcon; className: string }> = {
  again: { icon: RotateCcwIcon, className: "hover:border-destructive/50 hover:bg-destructive/10" },
  hard: { icon: CircleHelpIcon, className: "hover:border-primary/60 hover:bg-accent" },
  good: { icon: CheckIcon, className: "" },
};

/** Дүнгийн хавтангийн өнгө — «Мэднэ» ногоон, «Эргэлзсэн» шар, «Мэдэхгүй» улаан. */
const TALLY_TONES: Record<LiveCardRating, string> = {
  good: "border-success/30 bg-success/5",
  hard: "border-primary/35 bg-accent/60",
  again: "border-destructive/25 bg-destructive/5",
};

/** Картууд (`/live/materials/[id]/cards`, `?topic=` бол нэг сэдвийнх). */
export function Flashcards({
  materialId,
  topicId,
}: {
  materialId: string;
  topicId: string | null;
}) {
  return (
    <LiveToolShell
      materialId={materialId}
      topicId={topicId}
      tool="cards"
      fullTitle={t.cards.fullTitle}
    >
      {() => <CardSession materialId={materialId} topicId={topicId} />}
    </LiveToolShell>
  );
}

/**
 * Давталтын нэг удаа: эхлээд одоо давтах ёстой картууд (`due`); алга бол
 * «Бүгдийг давтах» (`all`). Жагсаалтыг эхэнд нь нэг удаа авч, дуустал
 * өөрчлөхгүй — карт бүрийн үнэлгээ (`reviewCard`) Leitner хайрцгийг серверт шинэчилнэ.
 */
function CardSession({ materialId, topicId }: { materialId: string; topicId: string | null }) {
  const invalidateMaterial = useInvalidateMaterial(materialId);
  const [mode, setMode] = useState<"due" | "all">("due");
  const [round, setRound] = useState(0);
  const [index, setIndex] = useState(0);
  const [flipped, setFlipped] = useState(false);
  const [tally, setTally] = useState(EMPTY_TALLY);
  const cardRef = useRef<HTMLButtonElement>(null);

  const deck = useQuery({
    queryKey: queryKeys.live.cards(materialId, topicId, mode, round),
    queryFn: () => listCards(materialId, { topic_id: topicId ?? undefined, mode }),
    // Давталтын дундуур жагсаалт солигдохгүй; дахин нээхэд шинээр авна.
    staleTime: Infinity,
    gcTime: 0,
    retry: false,
    refetchOnReconnect: false,
  });

  const review = useMutation({
    mutationFn: ({ card, rating }: { card: LiveCard; rating: LiveCardRating; last: boolean }) =>
      reviewCard(card.id, rating),
    onSuccess: (_card, { rating, last }) => {
      setTally((current) => ({ ...current, [rating]: current[rating] + 1 }));
      setFlipped(false);
      setIndex((current) => current + 1);
      // Эзэмшил өөрчлөгдлөө — судлах сет рүү буцахад шинээр татна. Сүүлийнх бол
      // энэ хуудасны толгойн хувь ч шинэчлэгдэнэ.
      invalidateMaterial({ refetch: last });
    },
    onError: (error) => toast.error(liveErrorMessage(error)),
  });

  const cards = deck.data ?? [];
  const card = cards[index] ?? null;

  const restart = (next: "due" | "all") => {
    setMode(next);
    setRound((current) => current + 1);
    setIndex(0);
    setFlipped(false);
    setTally(EMPTY_TALLY);
  };

  const rate = (rating: LiveCardRating) => {
    if (!card || !flipped || review.isPending) return;
    review.mutate({ card, rating, last: index + 1 >= cards.length });
  };

  // Space — эргүүлэх, 1/2/3 — үнэлэх. Товч, холбоос фокустай үед Space/Enter-ийг
  // хөтөч өөрөө дарна; цонх, цэс нээлттэй үед юу ч хийхгүй.
  useEffect(() => {
    if (!card) return;
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.defaultPrevented || event.altKey || event.ctrlKey || event.metaKey) return;
      const target = event.target instanceof HTMLElement ? event.target : null;
      if (target?.closest("input, textarea, select, [role=dialog], [role=menu]")) return;
      const digit = RATINGS[Number(event.key) - 1];
      if (digit && flipped) {
        event.preventDefault();
        rate(digit);
        return;
      }
      if ((event.key === " " || event.key === "Enter") && !target?.closest("button, a")) {
        event.preventDefault();
        setFlipped((current) => !current);
      }
    };
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  });

  // Дараагийн карт руу шилжихэд фокус карт дээр — гараар үргэлжлүүлнэ.
  useEffect(() => {
    if (index > 0) cardRef.current?.focus();
  }, [index]);

  if (deck.isPending) return <DeckSkeleton />;
  if (deck.isError) {
    return (
      <ErrorState description={liveErrorMessage(deck.error)} onRetry={() => void deck.refetch()} />
    );
  }

  const setHref = `/live/materials/${materialId}`;

  if (cards.length === 0) {
    return mode === "due" ? (
      <EmptyState
        icon={CircleCheckIcon}
        title={t.cards.noneDue}
        description={t.cards.noneDueBody}
        action={
          <Button size="lg" onClick={() => restart("all")}>
            {t.cards.reviewAll}
          </Button>
        }
      />
    ) : (
      <EmptyState
        icon={LayersIcon}
        title={t.cards.empty}
        description={t.cards.emptyBody}
        action={
          <Button asChild variant="outline">
            <Link href={setHref}>{t.backToSet}</Link>
          </Button>
        }
      />
    );
  }

  if (!card) {
    return (
      <SessionDone
        count={cards.length}
        tally={tally}
        setHref={setHref}
        onAgain={() => restart("due")}
      />
    );
  }

  // Ард нь үлдсэн картууд овоолго мэт харагдана (хамгийн ихдээ хоёр давхар).
  const remaining = cards.length - index;

  return (
    <div className="space-y-6">
      <div className="space-y-2">
        <div className="flex items-baseline justify-between gap-4">
          <p className="text-sm font-semibold tabular-nums">
            {t.cards.progress(index + 1, cards.length)}
          </p>
          <p className="text-muted-foreground hidden text-xs sm:block">{t.cards.keysHint}</p>
        </div>
        <Progress
          value={(index / cards.length) * 100}
          aria-label={t.cards.progressLabel}
          className="bg-foreground/10 [&>[data-slot=progress-indicator]]:from-primary h-1.5 [&>[data-slot=progress-indicator]]:bg-gradient-to-r [&>[data-slot=progress-indicator]]:to-amber-300"
        />
      </div>

      <div className={cn("relative", remaining > 2 ? "pb-5" : remaining > 1 && "pb-2.5")}>
        {remaining > 2 && (
          <span
            aria-hidden
            className="bg-muted/40 dark:bg-muted/60 absolute inset-x-10 top-6 bottom-0 rounded-3xl border"
          />
        )}
        {remaining > 1 && (
          <span
            aria-hidden
            className="bg-muted/70 dark:bg-muted absolute inset-x-5 top-3 bottom-2.5 rounded-3xl border shadow-sm"
          />
        )}
        {/* Карт бүр шинээр «тарагдана» — өмнөхийн ар тал харагдахгүй. */}
        <FlipCard
          key={card.id}
          ref={cardRef}
          card={card}
          flipped={flipped}
          onFlip={() => setFlipped((v) => !v)}
        />
      </div>

      <p role="status" className="sr-only">
        {flipped ? t.cards.backAnnounce(card.back) : ""}
      </p>

      {flipped ? (
        <div className="space-y-3">
          <p className="text-muted-foreground text-center text-sm">{t.cards.rateLabel}</p>
          <div
            className="grid grid-cols-3 gap-2 sm:gap-3"
            role="group"
            aria-label={t.cards.rateLabel}
          >
            {RATINGS.map((rating, position) => {
              const meta = RATING_META[rating];
              return (
                <Button
                  key={rating}
                  size="lg"
                  variant={rating === "good" ? "default" : "outline"}
                  disabled={review.isPending}
                  aria-keyshortcuts={String(position + 1)}
                  onClick={() => rate(rating)}
                  className={cn(
                    "h-auto min-h-14 flex-col gap-1 rounded-xl py-2.5 whitespace-normal sm:flex-row sm:gap-2",
                    meta.className,
                  )}
                >
                  <meta.icon aria-hidden className="size-4" />
                  {t.cards.ratings[rating]}
                  <kbd
                    aria-hidden
                    className="hidden rounded border border-current/25 px-1.5 font-mono text-[0.7rem] leading-4 opacity-80 sm:inline"
                  >
                    {position + 1}
                  </kbd>
                </Button>
              );
            })}
          </div>
        </div>
      ) : (
        <p className="text-muted-foreground flex items-center justify-center gap-2 text-center text-sm">
          <MousePointerClickIcon className="size-4 shrink-0" aria-hidden />
          {t.cards.flipHint}
        </p>
      )}
    </div>
  );
}

/**
 * Эргэдэг карт. Нүүр, ар хоёр нэг нүдэнд давхцана (өндөр нь урт талынхаар);
 * харагдахгүй тал нь `aria-hidden` тул товчны нэр нь зөвхөн харагдаж буй тал.
 * Шинэ карт доороос «тарагдаж» орж ирнэ. «Хөдөлгөөн багасгах» үед эргэлтгүй,
 * шууд солигдоно.
 */
function FlipCard({
  ref,
  card,
  flipped,
  onFlip,
}: {
  ref: Ref<HTMLButtonElement>;
  card: LiveCard;
  flipped: boolean;
  onFlip: () => void;
}) {
  const hintId = useId();
  const face =
    "bg-card relative flex min-h-72 flex-col items-center justify-center gap-5 overflow-hidden rounded-3xl border p-8 text-center shadow-sm transition-[border-color,box-shadow] duration-300 backface-hidden [grid-area:1/1] group-hover/card:shadow-lg sm:min-h-80 sm:p-12";

  return (
    <div className="motion-safe:animate-in motion-safe:fade-in-0 motion-safe:zoom-in-95 motion-safe:slide-in-from-bottom-3 relative duration-300">
      <div className="perspective-[1600px]">
        <span id={hintId} className="sr-only">
          {t.cards.flipHint}
        </span>
        <button
          ref={ref}
          type="button"
          onClick={onFlip}
          aria-describedby={hintId}
          className={cn(
            "group/card focus-visible:ring-ring/50 grid w-full rounded-3xl transition-transform duration-500 ease-[cubic-bezier(0.2,0.8,0.2,1)] outline-none transform-3d focus-visible:ring-3 motion-reduce:transition-none",
            flipped && "rotate-y-180",
          )}
        >
          <span aria-hidden={flipped} className={cn(face, "group-hover/card:border-primary/40")}>
            {/* Нүүр: цэгэн хээ, дээд талаас шар туяа. */}
            <span
              aria-hidden
              className="live-dots pointer-events-none absolute inset-0 [mask-image:radial-gradient(ellipse_at_center,#000,transparent_72%)] opacity-70"
            />
            <span
              aria-hidden
              className="bg-primary/15 pointer-events-none absolute -top-28 left-1/2 size-60 -translate-x-1/2 rounded-full blur-3xl"
            />
            <span className="bg-muted text-muted-foreground relative rounded-full px-3 py-1 text-[0.7rem] font-semibold tracking-wider uppercase">
              {t.cards.front}
            </span>
            <span className="relative text-2xl leading-snug font-semibold text-balance sm:text-3xl">
              <LiveInlineMarkdown text={card.front} />
            </span>
          </span>
          <span
            aria-hidden={!flipped}
            className={cn(
              face,
              "border-primary/30 group-hover/card:border-primary/50 rotate-y-180",
            )}
          >
            {/* Ар: шар өнгөөр ялгарна. */}
            <span
              aria-hidden
              className="from-accent pointer-events-none absolute inset-0 bg-gradient-to-b to-transparent"
            />
            <span className="bg-accent text-accent-foreground ring-primary/30 relative rounded-full px-3 py-1 text-[0.7rem] font-semibold tracking-wider uppercase ring-1 ring-inset">
              {t.cards.back}
            </span>
            <span className="relative text-lg leading-relaxed text-pretty sm:text-xl">
              <LiveInlineMarkdown text={card.back} />
            </span>
            {card.page !== null && (
              <span className="text-muted-foreground relative text-xs">
                {t.pageRef(String(card.page))}
              </span>
            )}
          </span>
        </button>
      </div>
    </div>
  );
}

function SessionDone({
  count,
  tally,
  setHref,
  onAgain,
}: {
  count: number;
  tally: Record<LiveCardRating, number>;
  setHref: string;
  onAgain: () => void;
}) {
  const headingRef = useRef<HTMLHeadingElement>(null);
  // Дэлгэц уншигч, гарын хэрэглэгч дүнгээс эхэлнэ.
  useEffect(() => headingRef.current?.focus(), []);

  return (
    <div className="bg-card relative isolate overflow-hidden rounded-3xl border p-8 text-center shadow-xs sm:p-12">
      <div
        aria-hidden
        className="from-primary/12 absolute inset-0 -z-10 bg-gradient-to-b via-transparent to-transparent"
      />
      <span className="relative mx-auto grid w-fit place-items-center">
        <SparkBurst className="top-1/2 left-1/2" />
        <span aria-hidden className="bg-primary/40 absolute size-16 rounded-full blur-2xl" />
        <LiveTile className="size-16">
          <TrophyIcon className="size-8" />
        </LiveTile>
      </span>
      <h2 ref={headingRef} tabIndex={-1} className="mt-6 text-2xl font-bold outline-none">
        {t.cards.doneTitle}
      </h2>
      <p className="text-muted-foreground mx-auto mt-2 max-w-md">{t.cards.doneBody(count)}</p>
      <dl className="mx-auto mt-7 grid max-w-md grid-cols-3 gap-2 sm:gap-3">
        {(["good", "hard", "again"] as const).map((rating) => (
          <div key={rating} className={cn("rounded-2xl border p-3", TALLY_TONES[rating])}>
            <dt className="text-muted-foreground text-xs">{t.cards.ratings[rating]}</dt>
            <dd className="mt-0.5 text-2xl font-bold tabular-nums">{tally[rating]}</dd>
          </div>
        ))}
      </dl>
      <div className="mt-8 flex flex-col justify-center gap-2 sm:flex-row">
        <Button size="lg" onClick={onAgain}>
          {t.cards.reviewAgain}
        </Button>
        <Button asChild size="lg" variant="outline">
          <Link href={setHref}>{t.backToSet}</Link>
        </Button>
      </div>
    </div>
  );
}

function DeckSkeleton() {
  return (
    <div className="space-y-6" aria-hidden>
      <Skeleton className="h-4 w-24" />
      <Skeleton className="h-72 w-full rounded-3xl sm:h-80" />
      <Skeleton className="mx-auto h-4 w-48" />
    </div>
  );
}
