"use client";

import { useQuery } from "@tanstack/react-query";

import { AdminPageHeader } from "@/components/admin/page-header";
import { LessonForm } from "@/components/admin/lesson-form";
import { ErrorState } from "@/components/common/states";
import { Skeleton } from "@/components/ui/skeleton";
import { getLesson } from "@/lib/api/admin";
import { ApiError } from "@/lib/api/client";
import { mn } from "@/lib/i18n/mn";
import { queryKeys } from "@/lib/query-keys";

export function AdminLessonEditor({ lessonId }: { lessonId: string }) {
  const query = useQuery({
    queryKey: queryKeys.lessons.detail(lessonId),
    queryFn: () => getLesson(lessonId),
  });

  if (query.isPending) {
    return (
      <div className="space-y-4">
        <Skeleton className="h-9 w-64" />
        <Skeleton className="h-96 w-full" />
      </div>
    );
  }

  if (query.isError) {
    const notFound = query.error instanceof ApiError && query.error.isNotFound;
    return (
      <ErrorState
        title={notFound ? mn.common.notFound : mn.common.error}
        description={query.error instanceof ApiError ? query.error.message : undefined}
        onRetry={notFound ? undefined : () => void query.refetch()}
      />
    );
  }

  return (
    <>
      <AdminPageHeader title={query.data.title} description={mn.admin.editLesson} />
      <LessonForm lesson={query.data} />
    </>
  );
}
