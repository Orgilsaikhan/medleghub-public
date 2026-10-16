"use client";

import {
  ArrowLeftIcon,
  BookOpenTextIcon,
  CircleCheckIcon,
  CircleXIcon,
  ClockIcon,
  FileIcon,
  FileTextIcon,
  FileTypeIcon,
  GraduationCapIcon,
  ImageIcon,
  InfoIcon,
  LayersIcon,
  ListChecksIcon,
  LoaderCircleIcon,
  type LucideIcon,
  NotebookTextIcon,
  PresentationIcon,
  SparklesIcon,
  UploadIcon,
} from "lucide-react";
import Link from "next/link";
import { type CSSProperties, type PointerEvent, type ReactNode, useId, useState } from "react";

import { mn } from "@/lib/i18n/mn";
import type { LiveLikelihood, LiveMaterialKind, LiveMaterialStatus } from "@/lib/types/live";
import { cn } from "@/lib/utils";

const KIND_ICONS: Record<LiveMaterialKind, LucideIcon> = {
  pdf: FileTextIcon,
  pptx: PresentationIcon,
  docx: FileTypeIcon,
  txt: FileIcon,
  md: NotebookTextIcon,
  image: ImageIcon,
};

/** Төрөл бүр өөрийн өнгөтэй — жагсаалтад PDF, слайд, Word-ыг нүдээр ялгана. */
const KIND_TINTS: Record<LiveMaterialKind, string> = {
  pdf: "bg-red-500/12 text-red-600 dark:text-red-400",
  pptx: "bg-orange-500/12 text-orange-600 dark:text-orange-400",
  docx: "bg-blue-500/12 text-blue-600 dark:text-blue-400",
  txt: "bg-slate-500/12 text-slate-600 dark:text-slate-300",
  md: "bg-violet-500/12 text-violet-600 dark:text-violet-400",
  image: "bg-emerald-500/12 text-emerald-600 dark:text-emerald-400",
};

/** Материалын картын буланд тусах, төрлийн өнгөтэй бүдэг гэрэл. */
export const KIND_GLOWS: Record<LiveMaterialKind, string> = {
  pdf: "bg-red-500/15",
  pptx: "bg-orange-500/15",
  docx: "bg-blue-500/15",
  txt: "bg-slate-500/15",
  md: "bg-violet-500/15",
  image: "bg-emerald-500/15",
};

/** Материалын төрлийн дүрс — дөрвөлжин дэвсгэртэй. Утга нь хажуугийн бичвэрт байдаг тул чимэглэл. */
export function MaterialKindIcon({
  kind,
  className,
}: {
  kind: LiveMaterialKind | null;
  className?: string;
}) {
  const Icon = kind ? KIND_ICONS[kind] : FileIcon;
  return (
    <span
      aria-hidden
      className={cn(
        "grid size-11 shrink-0 place-items-center rounded-xl ring-1 ring-current/15 ring-inset",
        kind ? KIND_TINTS[kind] : "bg-muted text-foreground",
        className,
      )}
    >
      <Icon className="size-5" />
    </span>
  );
}

/** Судлах арга бүрийн дүрс — толгой, цэс, хэрэгслийн картад ижил. */
export const TOOL_ICONS = {
  guide: BookOpenTextIcon,
  cards: LayersIcon,
  quiz: ListChecksIcon,
  exam: GraduationCapIcon,
} satisfies Record<string, LucideIcon>;

/**
 * «Гүнтэй» шар хавтан (`.live-tile`): дээрээс гэрэл тусна. Live-ийн тэмдэг,
 * файл оруулах, дүнгийн дүрсэнд. Чимэглэл — утгыг хажуугийн бичвэр хэлнэ.
 */
export function LiveTile({ className, children }: { className?: string; children: ReactNode }) {
  return (
    <span
      aria-hidden
      className={cn(
        "live-tile relative grid size-12 shrink-0 place-items-center overflow-hidden rounded-2xl",
        className,
      )}
    >
      <span className="pointer-events-none absolute inset-x-0 top-0 h-1/2 bg-gradient-to-b from-white/35 to-transparent" />
      <span className="relative grid place-items-center">{children}</span>
    </span>
  );
}

function clampPercent(value: number): number {
  return Math.max(0, Math.min(100, Math.round(value)));
}

/** Эзэмшлийн нимгэн зураас. `label` нь дэлгэц уншигчид (`Эзэмшил`, сэдвийн нэр гэх мэт). */
export function MasteryBar({
  value,
  label,
  showValue = true,
  className,
}: {
  value: number;
  label: string;
  showValue?: boolean;
  className?: string;
}) {
  const percent = clampPercent(value);
  return (
    <div className={cn("flex items-center gap-3", className)}>
      {showValue && (
        <span className="w-10 shrink-0 text-right text-sm font-semibold tabular-nums">
          {percent}%
        </span>
      )}
      <div
        role="progressbar"
        aria-label={label}
        aria-valuemin={0}
        aria-valuemax={100}
        aria-valuenow={percent}
        className="bg-foreground/10 h-1.5 min-w-12 flex-1 overflow-hidden rounded-full"
      >
        <div
          className={cn(
            "motion-safe:animate-meter-grow h-full rounded-full transition-[width] duration-500 ease-out motion-reduce:transition-none",
            percent >= 100 ? "bg-success" : "from-primary bg-gradient-to-r to-amber-300",
          )}
          style={{ width: `${percent}%` }}
        />
      </div>
    </div>
  );
}

/**
 * Эзэмшлийн цагираг — дотор нь хувь. Дэлгэц уншигчид `progressbar` (`label`),
 * доторх бичвэр нь зөвхөн нүдэнд. Нээгдэхэд 0-ээс утга хүртлээ зурагдана.
 */
export function MasteryRing({
  value,
  label,
  size = 88,
  stroke = 8,
  className,
  valueClassName,
}: {
  value: number;
  label: string;
  size?: number;
  stroke?: number;
  className?: string;
  valueClassName?: string;
}) {
  const id = useId().replace(/[^a-zA-Z0-9_-]/g, "");
  const percent = clampPercent(value);
  const radius = (size - stroke) / 2;
  const length = 2 * Math.PI * radius;
  const done = percent >= 100;

  return (
    <div
      role="progressbar"
      aria-label={label}
      aria-valuemin={0}
      aria-valuemax={100}
      aria-valuenow={percent}
      className={cn("relative grid shrink-0 place-items-center", className)}
      style={{ width: size, height: size }}
    >
      <svg
        aria-hidden
        viewBox={`0 0 ${size} ${size}`}
        fill="none"
        className="absolute inset-0 size-full -rotate-90"
      >
        <defs>
          <linearGradient id={`${id}-fill`} x1="0" y1="0" x2="1" y2="1">
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
            className="motion-safe:animate-live-ring transition-[stroke-dashoffset] duration-700 ease-out motion-reduce:transition-none"
            style={
              {
                stroke: done ? "var(--success)" : `url(#${id}-fill)`,
                "--ring-from": length,
              } as CSSProperties
            }
          />
        )}
      </svg>
      <span
        aria-hidden
        className={cn("relative font-bold tabular-nums", done && "text-success", valueClassName)}
      >
        {percent}%
      </span>
    </div>
  );
}

/** Жижиг эзэмшлийн шошго — «40%». Дэлгэц уншигч «Эзэмшил 40%» гэж сонсоно. */
export function MasteryPill({ value, className }: { value: number; className?: string }) {
  const percent = clampPercent(value);
  return (
    <span
      className={cn(
        "bg-muted text-foreground inline-flex shrink-0 items-center rounded-full px-2.5 py-0.5 text-xs font-semibold tabular-nums",
        className,
      )}
    >
      <span className="sr-only">{mn.live.mastery} </span>
      {percent}%
    </span>
  );
}

/** Эзэмшил юунаас бүрддэгийг нэг мөрөөр. */
export function MasteryHelp({ className }: { className?: string }) {
  return (
    <p className={cn("text-muted-foreground flex items-start gap-1.5 text-xs", className)}>
      <InfoIcon className="mt-px size-3.5 shrink-0" aria-hidden />
      <span>
        <span className="sr-only">{mn.live.masteryHelpLabel} </span>
        {mn.live.masteryHelp}
      </span>
    </p>
  );
}

/** «AI бэлтгэсэн» — заавар, тест, таамаг AI-ийн бүтээл гэдгийг үргэлж харуулна. */
export function AiLabel({ className }: { className?: string }) {
  return (
    <span
      className={cn(
        "text-muted-foreground bg-card/80 inline-flex items-center gap-1 rounded-full border px-2 py-0.5 text-xs font-medium",
        className,
      )}
    >
      <SparklesIcon className="text-brand-link size-3" aria-hidden />
      {mn.live.aiLabel}
    </span>
  );
}

const STATUS_META: Record<LiveMaterialStatus, { icon: LucideIcon; className: string }> = {
  uploading: { icon: UploadIcon, className: "bg-muted text-muted-foreground" },
  queued: { icon: ClockIcon, className: "bg-muted text-muted-foreground" },
  processing: {
    icon: LoaderCircleIcon,
    className: "bg-accent text-accent-foreground ring-1 ring-primary/30 ring-inset",
  },
  ready: { icon: CircleCheckIcon, className: "text-success ring-1 ring-success/40 ring-inset" },
  failed: {
    icon: CircleXIcon,
    className: "bg-destructive/10 text-destructive ring-1 ring-destructive/25 ring-inset",
  },
};

/**
 * Материалын төлөв — дүрс + бичвэр (зөвхөн өнгөөр биш). `aria-live` тул
 * «Боловсруулж байна» → «Бэлэн» болоход дэлгэц уншигч материалын нэртэй нь сонсоно.
 */
export function MaterialStatusChip({
  status,
  title,
}: {
  status: LiveMaterialStatus;
  title: string;
}) {
  const meta = STATUS_META[status];
  const Icon = meta.icon;
  return (
    <span aria-live="polite" aria-atomic="true" className="inline-flex">
      <span
        className={cn(
          "relative inline-flex items-center gap-1.5 overflow-hidden rounded-full px-2.5 py-0.5 text-xs font-medium",
          meta.className,
        )}
      >
        {/* AI ажиллаж байхад шошгоор гялбаа гүйнэ. */}
        {status === "processing" && (
          <span
            aria-hidden
            className="motion-safe:animate-live-shimmer pointer-events-none absolute inset-0 bg-gradient-to-r from-transparent via-white/25 to-transparent motion-reduce:hidden dark:via-white/10"
          />
        )}
        <Icon
          aria-hidden
          className={cn("relative size-3.5", status === "processing" && "motion-safe:animate-spin")}
        />
        <span className="sr-only">{title}: </span>
        <span className="relative">{mn.live.status[status]}</span>
      </span>
    </span>
  );
}

const LIKELIHOOD_META: Record<LiveLikelihood, { bars: number; className: string }> = {
  high: { bars: 3, className: "bg-primary text-primary-foreground" },
  medium: { bars: 2, className: "bg-accent text-accent-foreground" },
  low: { bars: 1, className: "bg-muted text-muted-foreground" },
};

/** Шалгалтад гарах магадлал — баганан дүрс + бичвэр. */
export function LikelihoodPill({ level }: { level: LiveLikelihood }) {
  const meta = LIKELIHOOD_META[level];
  return (
    <span
      className={cn(
        "inline-flex shrink-0 items-center gap-1.5 rounded-full px-2.5 py-0.5 text-xs font-semibold",
        meta.className,
      )}
    >
      <span aria-hidden className="flex h-3 items-end gap-px">
        {[1, 2, 3].map((bar) => (
          <span
            key={bar}
            className={cn("w-[3px] rounded-sm bg-current", bar > meta.bars && "opacity-30")}
            style={{ height: `${bar * 4}px` }}
          />
        ))}
      </span>
      {mn.live.exam.likelihood[level]}
    </span>
  );
}

/** Дээд хэсгийн «← Буцах» холбоос. */
export function LiveBackLink({ href, label }: { href: string; label: string }) {
  return (
    <Link
      href={href}
      className="group/back text-muted-foreground hover:text-foreground focus-visible:ring-ring/50 inline-flex max-w-full items-center gap-1.5 rounded-md text-sm font-medium transition-colors outline-none focus-visible:ring-3"
    >
      <ArrowLeftIcon
        className="size-4 shrink-0 transition-[translate] group-hover/back:-translate-x-0.5 motion-reduce:transition-none"
        aria-hidden
      />
      <span className="truncate">{label}</span>
    </Link>
  );
}

/** Жижиг хэсгийн гарчиг — «СЭДЭВ», «СУДЛАХ АРГА» маягийн том үсэгтэй саарал бичвэр. */
export const EYEBROW = "text-muted-foreground text-[0.7rem] font-semibold tracking-wider uppercase";

/**
 * Курсорын байрлалыг CSS хувьсагчид (`--spot-x/y`) бичнэ — `Spotlight` түүнийг
 * дагана. React state биш: хулгана хөдлөх бүрд дахин зурахгүй.
 */
export function trackSpotlight(event: PointerEvent<HTMLElement>) {
  const card = event.currentTarget;
  const rect = card.getBoundingClientRect();
  card.style.setProperty("--spot-x", `${event.clientX - rect.left}px`);
  card.style.setProperty("--spot-y", `${event.clientY - rect.top}px`);
}

/**
 * Курсорыг дагах шар гэрэл — картын дотор ба 1px хүрээн дээр (`course-card.tsx`
 * шиг). Эцэг нь `group/spot relative overflow-hidden` ба
 * `onPointerMove={trackSpotlight}`.
 */
export function Spotlight() {
  return (
    <>
      <span
        aria-hidden
        className="pointer-events-none absolute inset-0 z-10 opacity-0 transition-opacity duration-300 [background:radial-gradient(340px_circle_at_var(--spot-x,50%)_var(--spot-y,50%),color-mix(in_oklch,var(--primary)_12%,transparent),transparent_65%)] group-hover/spot:opacity-100"
      />
      <span
        aria-hidden
        className="pointer-events-none absolute inset-0 z-20 rounded-[inherit] p-px opacity-0 transition-opacity duration-300 [background:radial-gradient(220px_circle_at_var(--spot-x,50%)_var(--spot-y,50%),var(--primary),transparent_70%)] [mask:linear-gradient(#000_0_0)_content-box_exclude,linear-gradient(#000_0_0)] group-hover/spot:opacity-100"
      />
    </>
  );
}

/** Live-ийн тэмдгийн дөрвөн салаа од (24×24 дотор, төв нь 12,12). */
const SPARKLE = "M12 3Q13 11 21 12Q13 13 12 21Q11 13 3 12Q11 11 12 3Z";

/**
 * Хэсгийн буланд тавих бүдэг тойрог замууд — Live-ийн тэмдгийн хазгай цагираг
 * шиг, хоёр сар, нэг одтой. Хөдөлгөөнгүй чимэглэл; өнгө нь `currentColor`.
 */
export function OrbitArcs({ className }: { className?: string }) {
  return (
    <svg
      aria-hidden
      viewBox="0 0 400 240"
      fill="none"
      className={cn("pointer-events-none", className)}
    >
      <g transform="rotate(-14 200 120)" stroke="currentColor" strokeWidth={1}>
        <ellipse cx="200" cy="120" rx="78" ry="22" strokeOpacity={0.55} />
        <ellipse
          cx="200"
          cy="120"
          rx="138"
          ry="42"
          strokeOpacity={0.4}
          strokeDasharray="1 7"
          strokeLinecap="round"
          strokeWidth={1.5}
        />
        <ellipse cx="200" cy="120" rx="196" ry="62" strokeOpacity={0.25} />
        <circle cx="122" cy="120" r="4" fill="currentColor" stroke="none" />
        <circle cx="286" cy="149" r="2.5" fill="currentColor" stroke="none" fillOpacity={0.7} />
      </g>
      <path d={SPARKLE} transform="translate(300 34) scale(0.9)" fill="currentColor" />
      <path
        d={SPARKLE}
        transform="translate(76 168) scale(0.5)"
        fill="currentColor"
        opacity={0.6}
      />
    </svg>
  );
}

/** Тархах гялбаанууд: [x, y (төвөөс, px), хэмжээ (px), саатал (мс)]. */
const BURST: [number, number, number, number][] = [
  [0, -118, 20, 0],
  [84, -84, 14, 60],
  [126, -8, 22, 120],
  [88, 76, 14, 40],
  [10, 120, 18, 160],
  [-80, 84, 20, 80],
  [-128, 6, 14, 20],
  [-90, -80, 22, 140],
  [44, -150, 12, 200],
  [-46, 150, 12, 220],
  [150, 52, 10, 260],
  [-152, -46, 10, 240],
];

/**
 * Амжилтын үед (давталт дуусах, өндөр дүн) төвөөс нэг удаа тархах шар
 * гялбаанууд. Эцгийн төвд байрлуулна. Хөдөлгөөн багасгавал харагдахгүй.
 */
export function SparkBurst({ className }: { className?: string }) {
  return (
    <span
      aria-hidden
      className={cn("pointer-events-none absolute size-0 motion-reduce:hidden", className)}
    >
      {BURST.map(([x, y, size, delay], index) => (
        <svg
          key={index}
          viewBox="0 0 24 24"
          className={cn(
            "motion-safe:animate-live-burst absolute opacity-0",
            index % 3 === 0 ? "text-amber-300" : "text-primary",
          )}
          style={
            {
              width: size,
              height: size,
              left: -size / 2,
              top: -size / 2,
              "--dx": `${x}px`,
              "--dy": `${y}px`,
              animationDelay: `${delay}ms`,
            } as CSSProperties
          }
        >
          <path d={SPARKLE} fill="currentColor" />
        </svg>
      ))}
    </span>
  );
}

/** AI бэлтгэж буй агуулгын оронд — гялбаа гүйдэг саарал мөр. */
export function ShimmerBar({ className }: { className?: string }) {
  return (
    <span
      aria-hidden
      className={cn("bg-muted relative block overflow-hidden rounded-md", className)}
    >
      <span className="motion-safe:animate-live-shimmer via-foreground/[0.07] absolute inset-0 bg-gradient-to-r from-transparent to-transparent motion-reduce:hidden" />
    </span>
  );
}

/**
 * AI ажиллаж буй төлөвийг дэлгэц уншигчид мэдэгдэх бичвэр. Хуудас нээхэд аль
 * хэдийн бэлэн байсан бол юу ч хэлэхгүй — зөвхөн «бэлтгэж байна» → «бэлэн»
 * шилжилтийг.
 */
export function usePendingAnnouncement(pending: boolean, pendingText: string, doneText: string) {
  const [sawPending, setSawPending] = useState(pending);
  // Өмнөх render-ийн мэдээллийг state-д хадгалах React-ийн баримтжуулсан арга.
  if (pending && !sawPending) setSawPending(true);
  if (pending) return pendingText;
  return sawPending ? doneText : "";
}
