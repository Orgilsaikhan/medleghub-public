"use client";

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { ArrowRightIcon, PlayIcon } from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { toast } from "sonner";

import { Button } from "@/components/ui/button";
import { ApiError } from "@/lib/api/client";
import { enroll } from "@/lib/api/progress";
import { useCurrentUser } from "@/lib/hooks/use-auth";
import { mn } from "@/lib/i18n/mn";
import { queryKeys } from "@/lib/query-keys";
import type { CourseDetail } from "@/lib/types/api";

/** Дуусаагүй хамгийн эхний хичээл, эсвэл хамгийн эхнийх нь. */
function nextLessonSlug(course: CourseDetail): string | null {
  const lessons = course.modules.flatMap((section) => section.lessons);
  if (lessons.length === 0) return null;
  return (lessons.find((lesson) => !lesson.completed) ?? lessons[0]).slug;
}

export function EnrollButton({ course }: { course: CourseDetail }) {
  const router = useRouter();
  const queryClient = useQueryClient();
  const { isAuthenticated, isLoading } = useCurrentUser();
  const target = nextLessonSlug(course);

  const mutation = useMutation({
    mutationFn: () => enroll(course.id),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: queryKeys.courses.detail(course.slug) });
      void queryClient.invalidateQueries({ queryKey: queryKeys.courses.students(course.slug) });
      void queryClient.invalidateQueries({ queryKey: queryKeys.me.courses });
      if (target) router.push(`/learn/${course.slug}/${target}`);
      else router.refresh();
    },
    onError: (error) => {
      toast.error(error instanceof ApiError ? error.message : mn.common.somethingWrong);
    },
  });

  if (!target) {
    return (
      <Button size="lg" disabled className="w-full sm:w-auto">
        {mn.courses.noLessonsYet}
      </Button>
    );
  }

  if (isLoading) {
    // Нэвтрэлтийн төлөв тодрох хүртэл хамгийн магадлалтай шошгыг харуулна —
    // хоосон товч анивчихаас сэргийлж, сервер дээр ч утга нь render хийгдэнэ.
    return (
      <Button size="lg" disabled className="w-full sm:w-auto">
        {mn.courseDetail.start}
      </Button>
    );
  }

  if (!isAuthenticated) {
    // Нэвтрээгүй хэрэглэгчийг login руу явуулж, дараа нь энэ хуудас руу буцаана.
    return (
      <Button asChild size="lg" className="w-full sm:w-auto">
        <Link href={`/login?next=${encodeURIComponent(`/courses/${course.slug}`)}`}>
          {mn.courseDetail.start}
          <ArrowRightIcon className="size-4" />
        </Link>
      </Button>
    );
  }

  if (course.enrolled) {
    const finished = course.progress?.percent === 100;
    return (
      <Button asChild size="lg" className="w-full sm:w-auto">
        <Link href={`/learn/${course.slug}/${target}`}>
          <PlayIcon className="size-4" />
          {finished ? mn.courseDetail.review : mn.courseDetail.continue}
        </Link>
      </Button>
    );
  }

  return (
    <Button
      size="lg"
      className="w-full sm:w-auto"
      disabled={mutation.isPending}
      onClick={() => mutation.mutate()}
    >
      {mutation.isPending ? mn.auth.submitting : mn.courseDetail.start}
      {!mutation.isPending && <ArrowRightIcon className="size-4" />}
    </Button>
  );
}
