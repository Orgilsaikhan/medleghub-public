import { mn } from "@/lib/i18n/mn";
import { cn } from "@/lib/utils";
import type { CourseProgress } from "@/lib/types/api";

interface ProgressBarProps {
  progress: CourseProgress;
  /** Хичээлийн тоо болон хувийг дээр нь бичих эсэх. */
  showLabel?: boolean;
  /** Дэлгэц уншигчид — анхдагч нь «Таны ахиц». */
  label?: string;
  className?: string;
}

export function ProgressBar({
  progress,
  showLabel = true,
  label = mn.courseDetail.progressLabel,
  className,
}: ProgressBarProps) {
  const complete = progress.total_lessons > 0 && progress.percent >= 100;

  return (
    <div className={cn("space-y-1.5", className)}>
      {showLabel && (
        <div className="flex items-baseline justify-between gap-2 text-xs">
          <span className="text-muted-foreground">
            {mn.dashboard.completedLessons(progress.completed_lessons, progress.total_lessons)}
          </span>
          <span className={cn("font-semibold tabular-nums", complete && "text-success")}>
            {progress.percent}%
          </span>
        </div>
      )}

      <div
        role="progressbar"
        aria-valuenow={progress.percent}
        aria-valuemin={0}
        aria-valuemax={100}
        aria-label={label}
        className="bg-muted h-2 w-full overflow-hidden rounded-full"
      >
        <div
          className={cn(
            "h-full rounded-full transition-[width] duration-500 ease-out",
            complete ? "bg-success" : "bg-primary",
          )}
          style={{ width: `${progress.percent}%` }}
        />
      </div>
    </div>
  );
}
