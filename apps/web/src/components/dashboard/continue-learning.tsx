import { ArrowRightIcon, PlayIcon } from "lucide-react";
import Link from "next/link";

import { ProgressBar } from "@/components/courses/progress-bar";
import { Button } from "@/components/ui/button";
import { formatDate } from "@/lib/format";
import { mn } from "@/lib/i18n/mn";
import type { MyCourse } from "@/lib/types/api";

/**
 * Хамгийн сүүлд суралцсан сургалтыг том картаар онцолж, нэг товшилтоор
 * зогссон газраас нь үргэлжлүүлэх боломж олгоно.
 */
export function ContinueLearning({ item }: { item: MyCourse }) {
  const { course, progress, continue_lesson, last_completed_at } = item;
  const finished = progress.percent === 100;

  return (
    <section aria-labelledby="continue-heading">
      <h2 id="continue-heading" className="text-lg font-semibold tracking-tight">
        {mn.dashboard.continueTitle}
      </h2>

      <div className="from-primary/8 mt-4 rounded-xl border bg-gradient-to-br via-transparent to-transparent p-6">
        <div className="flex flex-wrap items-start justify-between gap-4">
          <div className="min-w-0">
            <h3 className="text-xl font-bold tracking-tight">
              <Link href={`/courses/${course.slug}`} className="hover:underline">
                {course.title}
              </Link>
            </h3>

            {continue_lesson && !finished && (
              <p className="text-muted-foreground mt-1 text-sm">
                {mn.courseDetail.statusCurrent}: {continue_lesson.title}
              </p>
            )}

            {last_completed_at && (
              <p className="text-muted-foreground mt-1 text-xs">
                {mn.dashboard.lastStudied}: {formatDate(last_completed_at)}
              </p>
            )}
          </div>

          {continue_lesson && (
            <Button asChild size="lg">
              <Link href={`/learn/${course.slug}/${continue_lesson.slug}`}>
                <PlayIcon className="size-4" />
                {finished ? mn.courseDetail.review : mn.courseDetail.continue}
                <ArrowRightIcon className="size-4" />
              </Link>
            </Button>
          )}
        </div>

        <ProgressBar progress={progress} className="mt-6 max-w-xl" />
      </div>
    </section>
  );
}
