import { CheckCircle2Icon, GraduationCapIcon, ListChecksIcon } from "lucide-react";
import type { LucideIcon } from "lucide-react";

import { mn } from "@/lib/i18n/mn";
import type { MyCourse } from "@/lib/types/api";

/**
 * Бодит өгөгдлөөр тооцсон гурван товч үзүүлэлт.
 *
 * Backend-д тусдаа stats endpoint байхгүй тул `/me/courses`-оос аль хэдийн
 * ирсэн жагсаалтаас тооцно — нэмэлт дуудлага үүсгэхгүй.
 */
export function DashboardSummary({ courses }: { courses: MyCourse[] }) {
  const enrolled = courses.length;
  const lessonsDone = courses.reduce((sum, item) => sum + item.progress.completed_lessons, 0);
  const finished = courses.filter(
    (item) => item.progress.total_lessons > 0 && item.progress.percent === 100,
  ).length;

  return (
    <div className="grid grid-cols-3 gap-3 sm:gap-4">
      <Stat icon={GraduationCapIcon} value={enrolled} label={mn.dashboard.summaryEnrolled} />
      <Stat icon={ListChecksIcon} value={lessonsDone} label={mn.dashboard.summaryLessonsDone} />
      <Stat icon={CheckCircle2Icon} value={finished} label={mn.dashboard.summaryFinished} />
    </div>
  );
}

export function Stat({
  icon: Icon,
  value,
  label,
}: {
  icon: LucideIcon;
  value: number | string;
  label: string;
}) {
  return (
    <div className="bg-card flex flex-col gap-2 rounded-xl border p-4 sm:flex-row sm:items-center sm:gap-3">
      <span className="bg-muted text-muted-foreground grid size-9 shrink-0 place-items-center rounded-lg">
        <Icon className="size-4.5" aria-hidden />
      </span>
      <div className="min-w-0">
        <p className="text-xl font-bold tabular-nums sm:text-2xl">{value}</p>
        <p className="text-muted-foreground truncate text-xs leading-snug sm:text-sm">{label}</p>
      </div>
    </div>
  );
}
