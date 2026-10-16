"use client";

import { ChevronRightIcon, ChevronUpIcon, HistoryIcon } from "lucide-react";
import Link from "next/link";
import { useId, useState } from "react";

import { EYEBROW, MasteryPill, TOOL_ICONS } from "@/components/live/live-ui";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { mn } from "@/lib/i18n/mn";
import type { LiveSection, LiveTopic } from "@/lib/types/live";
import { cn } from "@/lib/utils";

const t = mn.live;

/**
 * Нэг хэсэг — дугаар, «Хэсэг 1: …», сэдвийн тоо, эвхэх товч; дотор нь «СЭДЭВ …
 * ЭЗЭМШИЛ» толгойтой сэдвүүдийн мөр. Сэдвийг дарахад судлах аргын жижиг цонх
 * нээгдэнэ.
 */
export function SectionCard({
  section,
  number,
  materialId,
  lastStudiedTopicId,
}: {
  section: LiveSection;
  number: number;
  materialId: string;
  lastStudiedTopicId: string | null;
}) {
  const [open, setOpen] = useState(true);
  const panelId = useId();

  return (
    <section className="bg-card overflow-hidden rounded-2xl border shadow-xs">
      <h3>
        <button
          type="button"
          aria-expanded={open}
          aria-controls={panelId}
          onClick={() => setOpen((value) => !value)}
          className="group/section hover:bg-muted/40 focus-visible:ring-ring/50 flex w-full items-center gap-3 px-4 py-4 text-left transition-colors outline-none focus-visible:ring-3 focus-visible:ring-inset motion-reduce:transition-none sm:gap-4 sm:px-6 sm:py-5"
        >
          {/* Дугаар нь гарчигт бий — дэлгэц уншигчид давхардуулахгүй. */}
          <span
            aria-hidden
            className="bg-accent text-accent-foreground ring-primary/25 grid size-9 shrink-0 place-items-center rounded-xl text-sm font-bold tabular-nums ring-1 ring-inset"
          >
            {number}
          </span>
          <span className="min-w-0 flex-1 text-base leading-snug font-semibold sm:text-lg">
            {t.sectionHeading(number, section.title)}
          </span>
          {/* Утсан дээр нүдэнд баганын толгойд харагдана — энд зөвхөн дэлгэц уншигчид. */}
          <span className="text-muted-foreground sr-only shrink-0 text-sm sm:not-sr-only">
            {t.topicCount(section.topics.length)}
          </span>
          <span
            aria-hidden
            className="bg-muted group-hover/section:bg-accent group-hover/section:text-accent-foreground grid size-8 shrink-0 place-items-center rounded-full transition-colors"
          >
            <ChevronUpIcon
              className={cn(
                "size-4 transition-transform duration-300 motion-reduce:transition-none",
                !open && "rotate-180",
              )}
            />
          </span>
        </button>
      </h3>

      <div id={panelId} hidden={!open}>
        {/* Баганын нэр — мөр бүрийн утга өөрөө шошготой тул дэлгэц уншигчид давхардуулахгүй. */}
        <div
          aria-hidden
          className={cn(
            EYEBROW,
            "bg-muted/40 flex items-center gap-4 border-y px-5 py-2.5 sm:px-6",
          )}
        >
          <span className="flex-1">
            {t.columnTopic}
            {/* Утсан дээр сэдвийн тоо энд. */}
            <span className="sm:hidden"> · {t.topicCount(section.topics.length)}</span>
          </span>
          <span className="w-28 shrink-0 sm:w-44">{t.columnMastery}</span>
          <span className="hidden w-4 shrink-0 sm:block" />
        </div>
        <ul className="divide-y">
          {section.topics.map((topic) => (
            <li key={topic.id}>
              <TopicRow
                topic={topic}
                materialId={materialId}
                lastStudied={topic.id === lastStudiedTopicId}
              />
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}

function LastStudiedChip({ className }: { className?: string }) {
  return (
    <span
      className={cn(
        "bg-accent text-accent-foreground ring-primary/30 items-center gap-1 rounded-full px-2 py-0.5 text-xs font-medium whitespace-nowrap ring-1 ring-inset",
        className,
      )}
    >
      <HistoryIcon className="size-3.5" aria-hidden />
      {t.lastStudied}
    </span>
  );
}

interface StudyTool {
  key: "guide" | "cards" | "quiz";
  href: string;
}

/** Сэдвийн мөр — дарахад мөрнөөс «СУДЛАХ АРГА»-ын цонх (Заавар / Картууд / Тест) нээгдэнэ. */
function TopicRow({
  topic,
  materialId,
  lastStudied,
}: {
  topic: LiveTopic;
  materialId: string;
  lastStudied: boolean;
}) {
  const percent = Math.max(0, Math.min(100, Math.round(topic.mastery)));
  const base = `/live/materials/${materialId}`;
  const topicQuery = `?topic=${encodeURIComponent(topic.id)}`;
  const tools: StudyTool[] = [
    { key: "guide", href: `${base}/guide/${topic.id}` },
    { key: "cards", href: `${base}/cards${topicQuery}` },
    { key: "quiz", href: `${base}/quiz${topicQuery}` },
  ];

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <button
          type="button"
          className="group/topic hover:bg-muted/40 data-[state=open]:bg-accent/50 focus-visible:ring-ring/50 relative flex w-full items-center gap-4 px-5 py-5 text-left transition-colors outline-none focus-visible:ring-3 focus-visible:ring-inset motion-reduce:transition-none sm:px-6 sm:py-6"
        >
          {/* Хулгана дээр эсвэл цонх нээлттэй үед зүүн талд шар зураас. */}
          <span
            aria-hidden
            className="bg-primary absolute inset-y-3 left-0 w-1 scale-y-0 rounded-r-full transition-[scale] duration-300 group-hover/topic:scale-y-100 group-data-[state=open]/topic:scale-y-100 motion-reduce:transition-none"
          />
          <span className="min-w-0 flex-1">
            <span className="block text-base leading-snug font-medium sm:text-lg">
              {topic.title}
            </span>
            {lastStudied && <LastStudiedChip className="mt-2 inline-flex sm:hidden" />}
          </span>
          {lastStudied && <LastStudiedChip className="hidden sm:inline-flex" />}
          <span className="flex w-28 shrink-0 items-center gap-3 sm:w-44">
            <span className="w-10 shrink-0 text-right text-sm font-semibold tabular-nums">
              <span className="sr-only">{t.mastery} </span>
              {percent}%
            </span>
            <span
              aria-hidden
              className="bg-foreground/10 h-1.5 flex-1 overflow-hidden rounded-full"
            >
              <span
                className={cn(
                  "motion-safe:animate-meter-grow block h-full rounded-full",
                  percent >= 100 ? "bg-success" : "from-primary bg-gradient-to-r to-amber-300",
                )}
                style={{ width: `${percent}%` }}
              />
            </span>
          </span>
          <ChevronRightIcon
            aria-hidden
            className="text-muted-foreground hidden size-4 shrink-0 transition-[translate,rotate] group-hover/topic:translate-x-0.5 group-data-[state=open]/topic:rotate-90 motion-reduce:transition-none sm:block"
          />
        </button>
      </DropdownMenuTrigger>

      <DropdownMenuContent
        align="start"
        sideOffset={6}
        className="w-[min(22rem,calc(100vw-2rem))] rounded-2xl p-4"
      >
        <DropdownMenuLabel className="p-0 font-normal">
          <span className="flex items-start justify-between gap-3">
            <span className="text-foreground text-base leading-snug font-semibold">
              {topic.title}
            </span>
            <MasteryPill value={topic.mastery} />
          </span>
          {topic.summary && (
            <span className="text-muted-foreground mt-1.5 line-clamp-3 block text-xs leading-relaxed">
              {topic.summary}
            </span>
          )}
          <span className={cn(EYEBROW, "mt-4 block")}>{t.studyWith}</span>
        </DropdownMenuLabel>
        <div className="mt-2 grid grid-cols-3 gap-2">
          {tools.map((tool, index) => {
            const Icon = TOOL_ICONS[tool.key];
            return (
              <DropdownMenuItem
                key={tool.key}
                asChild
                className={cn(
                  "group/tool flex h-auto flex-col items-start gap-2.5 rounded-xl border p-3 text-sm font-medium",
                  "focus:ring-ring/60 focus:ring-2",
                  // «Заавар» — эхлэхэд санал болгох арга.
                  index === 0 && "border-primary/50 bg-accent text-accent-foreground",
                )}
              >
                <Link href={tool.href}>
                  <span
                    aria-hidden
                    className={cn(
                      "grid size-9 place-items-center rounded-lg transition-[scale] duration-300 group-hover/tool:scale-110 group-focus/tool:scale-110 motion-reduce:transition-none",
                      index === 0
                        ? "live-tile"
                        : "bg-accent text-accent-foreground ring-primary/20 ring-1 ring-inset",
                    )}
                  >
                    <Icon className="size-4.5" />
                  </span>
                  {t.tools[tool.key]}
                </Link>
              </DropdownMenuItem>
            );
          })}
        </div>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}
