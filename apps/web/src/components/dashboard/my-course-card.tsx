import { BookOpenIcon, CheckCircle2Icon } from "lucide-react";
import Link from "next/link";

import { CategoryLogo } from "@/components/courses/category-logo";
import { ProgressBar } from "@/components/courses/progress-bar";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { categoryLabels, difficultyLabels, mn } from "@/lib/i18n/mn";
import type { MyCourse } from "@/lib/types/api";

export function MyCourseCard({ item }: { item: MyCourse }) {
  const { course, progress, continue_lesson } = item;
  const finished = progress.percent === 100 && progress.total_lessons > 0;

  return (
    <article className="bg-card flex flex-col rounded-xl border p-5">
      <div className="flex flex-wrap items-center gap-2">
        <Badge variant="outline">{categoryLabels[course.category]}</Badge>
        <Badge variant="outline">{difficultyLabels[course.difficulty]}</Badge>
        {finished && (
          <Badge variant="outline" className="border-success/40 text-success gap-1">
            <CheckCircle2Icon className="size-3" aria-hidden />
            {mn.dashboard.allDone}
          </Badge>
        )}
      </div>

      <div className="mt-3 flex items-start gap-3">
        <CategoryLogo category={course.category} className="mt-0.5 size-8" />
        <h3 className="text-base leading-snug font-semibold">
          <Link href={`/courses/${course.slug}`} className="hover:underline">
            {course.title}
          </Link>
        </h3>
      </div>

      <p className="text-muted-foreground mt-2 flex items-center gap-1.5 text-xs">
        <BookOpenIcon className="size-3.5" aria-hidden />
        {mn.courses.lessons(course.lesson_count)}
      </p>

      <div className="mt-auto pt-5">
        <ProgressBar progress={progress} />

        {continue_lesson && (
          <Button asChild variant="outline" size="sm" className="mt-4 w-full">
            <Link href={`/learn/${course.slug}/${continue_lesson.slug}`}>
              {finished ? mn.courseDetail.review : mn.courseDetail.continue}
            </Link>
          </Button>
        )}
      </div>
    </article>
  );
}
