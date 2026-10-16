"use client";

import { CheckIcon, CircleCheckBigIcon, FlaskConicalIcon } from "lucide-react";
import { useRouter } from "next/navigation";
import { toast } from "sonner";

import { Button } from "@/components/ui/button";
import { ApiError } from "@/lib/api/client";
import { useCompleteLesson } from "@/lib/hooks/use-progress";
import { mn } from "@/lib/i18n/mn";
import type { LessonLink } from "@/lib/types/api";

interface CompleteButtonProps {
  courseSlug: string;
  lessonSlug: string;
  lessonId: string;
  completed: boolean;
  enrolled: boolean;
  nextLesson: LessonLink | null;
  /** Дасгалтай хичээл — гараар биш, «Илгээх»-ийн бүх тестийг давж дуусна. */
  requiresSubmission?: boolean;
  /** `requiresSubmission`-ийн тайлбар (анхдагч — дасгалын тест). */
  submissionHint?: string;
}

export function CompleteButton({
  courseSlug,
  lessonSlug,
  lessonId,
  completed,
  enrolled,
  nextLesson,
  requiresSubmission = false,
  submissionHint = mn.learn.exercise.completeHint,
}: CompleteButtonProps) {
  const router = useRouter();
  const complete = useCompleteLesson(courseSlug, lessonSlug);

  // Бүртгүүлээгүй бол ахиц хадгалагдахгүй — эхлээд бүртгүүлэхийг санал болгоно.
  if (!enrolled) {
    return (
      <Button variant="outline" size="sm" onClick={() => router.push(`/courses/${courseSlug}`)}>
        {mn.learn.enrollNow}
      </Button>
    );
  }

  if (completed) {
    return (
      <span className="text-success inline-flex items-center gap-1.5 text-sm font-medium">
        <CircleCheckBigIcon className="size-4" aria-hidden />
        {mn.learn.completed}
      </span>
    );
  }

  if (requiresSubmission) {
    return (
      <span className="text-muted-foreground inline-flex items-center gap-1.5 text-center text-xs sm:text-sm">
        <FlaskConicalIcon className="size-4 shrink-0" aria-hidden />
        {submissionHint}
      </span>
    );
  }

  return (
    <Button
      size="sm"
      disabled={complete.isPending}
      onClick={() =>
        complete.mutate(lessonId, {
          onSuccess: (result) => {
            if (result.course_progress.percent === 100) {
              toast.success(mn.learn.courseComplete);
            }
            // Дараагийн хичээл рүү шууд аваачина — сурах урсгал тасрахгүй.
            if (nextLesson) router.push(`/learn/${courseSlug}/${nextLesson.slug}`);
          },
          onError: (error) => {
            toast.error(error instanceof ApiError ? error.message : mn.common.somethingWrong);
          },
        })
      }
    >
      <CheckIcon className="size-4" />
      {complete.isPending ? mn.learn.completing : mn.learn.complete}
    </Button>
  );
}
