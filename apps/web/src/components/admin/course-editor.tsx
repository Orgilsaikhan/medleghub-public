"use client";

import { useQuery } from "@tanstack/react-query";
import Link from "next/link";

import { AdminPageHeader } from "@/components/admin/page-header";
import { CourseForm } from "@/components/admin/course-form";
import { ErrorState } from "@/components/common/states";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { getAdminCourse } from "@/lib/api/admin";
import { ApiError } from "@/lib/api/client";
import { mn } from "@/lib/i18n/mn";
import { queryKeys } from "@/lib/query-keys";

export function AdminCourseEditor({ courseId }: { courseId: string }) {
  const query = useQuery({
    queryKey: queryKeys.admin.course(courseId),
    queryFn: () => getAdminCourse(courseId),
  });

  if (query.isPending) {
    return (
      <div className="max-w-2xl space-y-4">
        <Skeleton className="h-9 w-64" />
        {Array.from({ length: 6 }, (_, index) => (
          <Skeleton key={index} className="h-12 w-full" />
        ))}
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
      <AdminPageHeader
        title={query.data.title}
        description={mn.admin.editCourse}
        backHref="/admin/courses"
        action={
          <Button asChild variant="outline">
            <Link href={`/admin/courses/${courseId}/modules`}>{mn.admin.modules}</Link>
          </Button>
        }
      />
      <CourseForm course={query.data} />
    </>
  );
}
