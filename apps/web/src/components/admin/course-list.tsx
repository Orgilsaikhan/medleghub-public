"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { BookOpenIcon, PencilIcon, PlusIcon } from "lucide-react";
import Link from "next/link";
import { toast } from "sonner";

import { ConfirmDelete } from "@/components/admin/confirm-delete";
import { CategoryLogo } from "@/components/courses/category-logo";
import { EmptyState, ErrorState } from "@/components/common/states";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { deleteCourse } from "@/lib/api/admin";
import { ApiError } from "@/lib/api/client";
import { listCourses } from "@/lib/api/courses";
import { categoryLabels, difficultyLabels, mn } from "@/lib/i18n/mn";
import { queryKeys } from "@/lib/query-keys";

const PAGE_SIZE = 48;

export function AdminCourseList() {
  const queryClient = useQueryClient();

  // Админ эрхтэй хүсэлт нь нийтлэгдээгүй сургалтуудыг ч буцаана.
  const params = { page_size: PAGE_SIZE };
  const query = useQuery({
    queryKey: queryKeys.courses.list(params),
    queryFn: () => listCourses(params),
  });

  const remove = useMutation({
    mutationFn: deleteCourse,
    onSuccess: () => {
      toast.success(mn.admin.deleted);
      void queryClient.invalidateQueries({ queryKey: queryKeys.courses.all });
    },
    onError: (error) =>
      toast.error(error instanceof ApiError ? error.message : mn.common.somethingWrong),
  });

  if (query.isPending) {
    return (
      <div className="space-y-3">
        {Array.from({ length: 4 }, (_, index) => (
          <Skeleton key={index} className="h-20 w-full" />
        ))}
      </div>
    );
  }

  if (query.isError) return <ErrorState onRetry={() => void query.refetch()} />;

  if (query.data.items.length === 0) {
    return (
      <EmptyState
        icon={BookOpenIcon}
        title={mn.admin.emptyCourses}
        action={
          <Button asChild>
            <Link href="/admin/courses/new">
              <PlusIcon className="size-4" />
              {mn.admin.newCourse}
            </Link>
          </Button>
        }
      />
    );
  }

  return (
    <ul className="divide-y rounded-xl border">
      {query.data.items.map((course) => (
        <li key={course.id} className="flex flex-wrap items-center gap-4 p-4">
          <CategoryLogo category={course.category} className="size-9 shrink-0" />

          <div className="min-w-0 flex-1">
            <div className="flex flex-wrap items-center gap-2">
              <Link
                href={`/admin/courses/${course.id}`}
                className="truncate font-medium hover:underline"
              >
                {course.title}
              </Link>
              <Badge variant={course.published ? "default" : "secondary"}>
                {course.published ? mn.admin.published : mn.admin.draft}
              </Badge>
              {!course.is_free && <Badge variant="outline">{mn.courses.premium}</Badge>}
            </div>

            <p className="text-muted-foreground mt-1 flex flex-wrap items-center gap-x-3 text-xs">
              <span className="font-mono">{course.slug}</span>
              <span>{categoryLabels[course.category]}</span>
              <span>{difficultyLabels[course.difficulty]}</span>
              <span>{mn.courses.lessons(course.lesson_count)}</span>
            </p>
          </div>

          <div className="flex items-center gap-1">
            <Button asChild variant="ghost" size="sm">
              <Link href={`/admin/courses/${course.id}/modules`}>{mn.admin.modules}</Link>
            </Button>
            <Button asChild variant="ghost" size="icon" aria-label={mn.admin.editCourse}>
              <Link href={`/admin/courses/${course.id}`}>
                <PencilIcon className="size-4" />
              </Link>
            </Button>
            <ConfirmDelete
              compact
              name={course.title}
              isPending={remove.isPending}
              onConfirm={() => remove.mutate(course.id)}
            />
          </div>
        </li>
      ))}
    </ul>
  );
}
