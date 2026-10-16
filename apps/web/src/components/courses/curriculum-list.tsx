import { CheckIcon, CircleIcon, LockIcon, PlayIcon } from "lucide-react";
import Link from "next/link";

import { formatClock } from "@/lib/format";
import { mn } from "@/lib/i18n/mn";
import type { LessonSummary, ModuleWithLessons } from "@/lib/types/api";
import { cn } from "@/lib/utils";

export type LessonState = "completed" | "current" | "pending";

interface CurriculumListProps {
  modules: ModuleWithLessons[];
  courseSlug: string;
  /** Хичээл рүү шууд орох боломжтой эсэх (бүртгүүлсэн эсэхээс шалтгаална). */
  linkLessons: boolean;
  /** Одоо үзэж буй хичээлийн slug. */
  currentSlug?: string;
}

/** Дуусаагүй хамгийн эхний хичээл нь «одоогийн» гэж тэмдэглэгдэнэ. */
function resolveCurrentSlug(modules: ModuleWithLessons[]): string | undefined {
  for (const section of modules) {
    for (const lesson of section.lessons) {
      if (!lesson.completed) return lesson.slug;
    }
  }
  return undefined;
}

export function CurriculumList({
  modules,
  courseSlug,
  linkLessons,
  currentSlug,
}: CurriculumListProps) {
  const activeSlug = currentSlug ?? resolveCurrentSlug(modules);

  return (
    <ol className="space-y-6">
      {modules.map((section, moduleIndex) => (
        <li key={section.id}>
          <div className="flex items-baseline gap-2">
            <span className="text-muted-foreground font-mono text-xs tabular-nums">
              {String(moduleIndex + 1).padStart(2, "0")}
            </span>
            <h3 className="font-semibold">{section.title}</h3>
          </div>

          {section.description && (
            <p className="text-muted-foreground mt-1 ml-7 text-sm">{section.description}</p>
          )}

          <ul className="mt-3 ml-7 space-y-1">
            {section.lessons.map((lesson) => (
              <LessonRow
                key={lesson.id}
                lesson={lesson}
                courseSlug={courseSlug}
                state={
                  lesson.completed
                    ? "completed"
                    : lesson.slug === activeSlug
                      ? "current"
                      : "pending"
                }
                linkable={linkLessons}
              />
            ))}
          </ul>
        </li>
      ))}
    </ol>
  );
}

interface LessonRowProps {
  lesson: LessonSummary;
  courseSlug: string;
  state: LessonState;
  linkable: boolean;
}

export function LessonRow({ lesson, courseSlug, state, linkable }: LessonRowProps) {
  // Дууссан хичээл түгжигдсэн ч (багц дууссан) дууссан хэвээр харагдана.
  const locked = lesson.locked && state !== "completed";
  const label = locked
    ? mn.courseDetail.statusLocked
    : state === "completed"
      ? mn.courseDetail.statusCompleted
      : state === "current"
        ? mn.courseDetail.statusCurrent
        : mn.courseDetail.statusPending;

  const content = (
    <>
      {locked ? <LockedIcon /> : <StatusIcon state={state} />}
      <span className="flex-1 truncate">{lesson.title}</span>
      {lesson.duration > 0 && (
        <span className="text-muted-foreground shrink-0 font-mono text-xs tabular-nums">
          {formatClock(lesson.duration)}
        </span>
      )}
      <span className="sr-only">{label}</span>
    </>
  );

  // `relative` нь ЗААВАЛ хэрэгтэй. Доорх `sr-only` шошго нь
  // `position: absolute` бөгөөд байрлалтай эцэг олдохгүй бол `body`-г
  // барина. Тэгвэл хичээлийн дэлгэцийн хөтөлбөр (`overflow-y: auto`,
  // байрлалгүй `nav`) түүнийг таслахгүй тул хөтөлбөр урт болох тусам
  // ХУУДАС БҮХЭЛДЭЭ гүйлгэгддэг болно.
  const className = cn(
    "relative flex w-full items-center gap-3 rounded-md px-3 py-2 text-sm transition-colors",
    state === "current" && "bg-accent text-accent-foreground font-medium",
    state !== "current" && "text-foreground/90",
  );

  if (!linkable) {
    return (
      <li>
        <div className={cn(className, "cursor-default")}>{content}</div>
      </li>
    );
  }

  return (
    <li>
      <Link
        href={`/learn/${courseSlug}/${lesson.slug}`}
        aria-current={state === "current" ? "step" : undefined}
        className={cn(
          className,
          "hover:bg-accent/60 focus-visible:ring-ring focus-visible:ring-2 focus-visible:outline-none",
        )}
      >
        {content}
      </Link>
    </li>
  );
}

function LockedIcon() {
  return (
    <span className="text-muted-foreground grid size-5 shrink-0 place-items-center">
      <LockIcon className="size-3.5" aria-hidden />
    </span>
  );
}

function StatusIcon({ state }: { state: LessonState }) {
  if (state === "completed") {
    return (
      <span className="bg-success/15 text-success grid size-5 shrink-0 place-items-center rounded-full">
        <CheckIcon className="size-3" aria-hidden />
      </span>
    );
  }
  if (state === "current") {
    return (
      <span className="bg-primary/15 text-primary grid size-5 shrink-0 place-items-center rounded-full">
        <PlayIcon className="size-2.5 fill-current" aria-hidden />
      </span>
    );
  }
  return (
    <span className="text-muted-foreground/50 grid size-5 shrink-0 place-items-center">
      <CircleIcon className="size-3.5" aria-hidden />
    </span>
  );
}
