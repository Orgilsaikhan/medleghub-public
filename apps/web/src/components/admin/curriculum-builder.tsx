"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { ChevronDownIcon, ChevronUpIcon, LayersIcon, PencilIcon, PlusIcon } from "lucide-react";
import Link from "next/link";
import { useState } from "react";
import { toast } from "sonner";

import { ConfirmDelete } from "@/components/admin/confirm-delete";
import { ModuleDialog } from "@/components/admin/module-dialog";
import { EmptyState, ErrorState } from "@/components/common/states";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { deleteLesson, deleteModule, getAdminCourse, updateModule } from "@/lib/api/admin";
import { ApiError } from "@/lib/api/client";
import { formatClock } from "@/lib/format";
import { mn } from "@/lib/i18n/mn";
import { queryKeys } from "@/lib/query-keys";
import type { ModuleWithLessons } from "@/lib/types/api";

/**
 * Энгийн course builder.
 *
 * Дараалал нь `position` бүхэл тоогоор удирдагдана — drag & drop-гүй (MVP §16).
 * Дээш/доош товч нь хоёр модулын position-ыг солино.
 */
export function CurriculumBuilder({ courseId }: { courseId: string }) {
  const queryClient = useQueryClient();
  const [editing, setEditing] = useState<ModuleWithLessons | null>(null);
  const [creating, setCreating] = useState(false);

  const query = useQuery({
    queryKey: queryKeys.admin.course(courseId),
    queryFn: () => getAdminCourse(courseId),
  });

  const refresh = () => {
    void queryClient.invalidateQueries({ queryKey: queryKeys.admin.course(courseId) });
    void queryClient.invalidateQueries({ queryKey: queryKeys.courses.all });
  };

  const onError = (error: unknown) =>
    toast.error(error instanceof ApiError ? error.message : mn.common.somethingWrong);

  const reorder = useMutation({
    mutationFn: async ({ from, to }: { from: ModuleWithLessons; to: ModuleWithLessons }) => {
      await updateModule(from.id, { position: to.position });
      await updateModule(to.id, { position: from.position });
    },
    onSuccess: refresh,
    onError,
  });

  const removeModule = useMutation({
    mutationFn: deleteModule,
    onSuccess: () => {
      toast.success(mn.admin.deleted);
      refresh();
    },
    onError,
  });

  const removeLesson = useMutation({
    mutationFn: deleteLesson,
    onSuccess: () => {
      toast.success(mn.admin.deleted);
      refresh();
    },
    onError,
  });

  if (query.isPending) {
    return (
      <div className="space-y-4">
        {Array.from({ length: 3 }, (_, index) => (
          <Skeleton key={index} className="h-32 w-full" />
        ))}
      </div>
    );
  }

  if (query.isError) return <ErrorState onRetry={() => void query.refetch()} />;

  const modules = query.data.modules;

  return (
    <div className="space-y-6">
      <div className="flex justify-end">
        <Button onClick={() => setCreating(true)}>
          <PlusIcon className="size-4" />
          {mn.admin.newModule}
        </Button>
      </div>

      {modules.length === 0 ? (
        <EmptyState icon={LayersIcon} title={mn.admin.emptyModules} />
      ) : (
        <ol className="space-y-4">
          {modules.map((section, index) => (
            <li key={section.id} className="rounded-xl border">
              <div className="flex flex-wrap items-center gap-3 border-b p-4">
                <span className="text-muted-foreground font-mono text-xs tabular-nums">
                  {String(index + 1).padStart(2, "0")}
                </span>

                <div className="min-w-0 flex-1">
                  <p className="truncate font-medium">{section.title}</p>
                  {section.description && (
                    <p className="text-muted-foreground truncate text-xs">{section.description}</p>
                  )}
                </div>

                <div className="flex items-center gap-1">
                  <Button
                    variant="ghost"
                    size="icon"
                    aria-label={mn.admin.moveUp}
                    title={mn.admin.moveUp}
                    disabled={index === 0 || reorder.isPending}
                    onClick={() => reorder.mutate({ from: section, to: modules[index - 1] })}
                  >
                    <ChevronUpIcon className="size-4" />
                  </Button>
                  <Button
                    variant="ghost"
                    size="icon"
                    aria-label={mn.admin.moveDown}
                    title={mn.admin.moveDown}
                    disabled={index === modules.length - 1 || reorder.isPending}
                    onClick={() => reorder.mutate({ from: section, to: modules[index + 1] })}
                  >
                    <ChevronDownIcon className="size-4" />
                  </Button>
                  <Button
                    variant="ghost"
                    size="icon"
                    aria-label={mn.admin.editCourse}
                    onClick={() => setEditing(section)}
                  >
                    <PencilIcon className="size-4" />
                  </Button>
                  <ConfirmDelete
                    compact
                    name={section.title}
                    isPending={removeModule.isPending}
                    onConfirm={() => removeModule.mutate(section.id)}
                  />
                </div>
              </div>

              <ul className="divide-y">
                {section.lessons.map((lesson) => (
                  <li key={lesson.id} className="flex flex-wrap items-center gap-3 px-4 py-3">
                    <div className="min-w-0 flex-1">
                      <div className="flex flex-wrap items-center gap-2">
                        <Link
                          href={`/admin/lessons/${lesson.id}`}
                          className="truncate text-sm font-medium hover:underline"
                        >
                          {lesson.title}
                        </Link>
                        <Badge variant={lesson.published ? "default" : "secondary"}>
                          {lesson.published ? mn.admin.published : mn.admin.draft}
                        </Badge>
                      </div>
                      <p className="text-muted-foreground mt-0.5 flex gap-3 font-mono text-xs">
                        <span>{lesson.slug}</span>
                        {lesson.duration > 0 && <span>{formatClock(lesson.duration)}</span>}
                      </p>
                    </div>

                    <div className="flex items-center gap-1">
                      <Button asChild variant="ghost" size="icon" aria-label={mn.admin.editLesson}>
                        <Link href={`/admin/lessons/${lesson.id}`}>
                          <PencilIcon className="size-4" />
                        </Link>
                      </Button>
                      <ConfirmDelete
                        compact
                        name={lesson.title}
                        isPending={removeLesson.isPending}
                        onConfirm={() => removeLesson.mutate(lesson.id)}
                      />
                    </div>
                  </li>
                ))}
              </ul>

              <div className="border-t p-3">
                <Button asChild variant="ghost" size="sm">
                  <Link href={`/admin/lessons/new?module=${section.id}&course=${courseId}`}>
                    <PlusIcon className="size-4" />
                    {mn.admin.newLesson}
                  </Link>
                </Button>
              </div>
            </li>
          ))}
        </ol>
      )}

      <ModuleDialog
        courseId={courseId}
        module={editing}
        open={creating || editing !== null}
        onOpenChange={(open) => {
          if (!open) {
            setCreating(false);
            setEditing(null);
          }
        }}
        onSaved={refresh}
      />
    </div>
  );
}
