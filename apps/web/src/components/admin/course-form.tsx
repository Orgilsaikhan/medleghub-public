"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useRouter } from "next/navigation";
import { Controller, useForm, useWatch } from "react-hook-form";
import { toast } from "sonner";

import { FormField } from "@/components/auth/form-field";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Switch } from "@/components/ui/switch";
import { Textarea } from "@/components/ui/textarea";
import { createCourse, updateCourse } from "@/lib/api/admin";
import { ApiError } from "@/lib/api/client";
import { suggestSlug } from "@/lib/format";
import {
  categoryLabels,
  categoryOrder,
  difficultyLabels,
  difficultyOrder,
  mn,
} from "@/lib/i18n/mn";
import { queryKeys } from "@/lib/query-keys";
import type { CourseDetail } from "@/lib/types/api";
import { courseSchema, type CourseFormValues } from "@/lib/validation/admin";

interface CourseFormProps {
  /** Байхгүй бол шинэ сургалт үүсгэнэ. */
  course?: CourseDetail;
}

function toValues(course?: CourseDetail): CourseFormValues {
  return {
    title: course?.title ?? "",
    slug: course?.slug ?? "",
    description: course?.description ?? "",
    thumbnail_url: course?.thumbnail_url ?? "",
    difficulty: course?.difficulty ?? "beginner",
    category: course?.category ?? "javascript",
    is_free: course?.is_free ?? true,
    free_lessons: course?.free_lessons ?? 0,
    published: course?.published ?? false,
  };
}

export function CourseForm({ course }: CourseFormProps) {
  const router = useRouter();
  const queryClient = useQueryClient();
  const isEdit = Boolean(course);

  const form = useForm<CourseFormValues>({
    resolver: zodResolver(courseSchema),
    defaultValues: toValues(course),
  });
  const isFree = useWatch({ control: form.control, name: "is_free" });

  const mutation = useMutation({
    mutationFn: (values: CourseFormValues) => {
      const payload = { ...values, thumbnail_url: values.thumbnail_url || null };
      return course ? updateCourse(course.id, payload) : createCourse(payload);
    },
    onSuccess: (saved) => {
      toast.success(mn.admin.saved);
      void queryClient.invalidateQueries({ queryKey: queryKeys.courses.all });
      if (course) {
        void queryClient.invalidateQueries({ queryKey: queryKeys.admin.course(course.id) });
        router.refresh();
      } else {
        router.push(`/admin/courses/${saved.id}/modules`);
      }
    },
    onError: (error) => {
      if (error instanceof ApiError && error.code === "SLUG_TAKEN") {
        form.setError("slug", { message: error.message });
      }
    },
  });

  const slugHandled = mutation.error instanceof ApiError && mutation.error.code === "SLUG_TAKEN";
  const serverError =
    !slugHandled && mutation.error
      ? mutation.error instanceof ApiError
        ? mutation.error.message
        : mn.common.somethingWrong
      : null;

  return (
    <form
      onSubmit={form.handleSubmit((values) => mutation.mutate(values))}
      noValidate
      className="max-w-2xl space-y-6"
    >
      {serverError && (
        <Alert variant="destructive" className="bg-destructive/5">
          <AlertDescription>{serverError}</AlertDescription>
        </Alert>
      )}

      <FormField
        id="title"
        label={mn.admin.fields.title}
        error={form.formState.errors.title?.message}
        {...form.register("title", {
          // Шинэ сургалт үүсгэхэд гарчгаас slug-ийг автоматаар санал болгоно.
          onChange: (event) => {
            if (!isEdit && !form.formState.dirtyFields.slug) {
              form.setValue("slug", suggestSlug(event.target.value));
            }
          },
        })}
      />

      <FormField
        id="slug"
        label={mn.admin.fields.slug}
        hint={mn.admin.fields.slugHint}
        error={form.formState.errors.slug?.message}
        className="font-mono"
        {...form.register("slug")}
      />

      <div className="space-y-2">
        <Label htmlFor="description">{mn.admin.fields.description}</Label>
        <Textarea id="description" rows={4} {...form.register("description")} />
        {form.formState.errors.description && (
          <p role="alert" className="text-destructive text-xs">
            {form.formState.errors.description.message}
          </p>
        )}
      </div>

      <FormField
        id="thumbnail_url"
        label={mn.admin.fields.thumbnailUrl}
        placeholder="https://…"
        error={form.formState.errors.thumbnail_url?.message}
        {...form.register("thumbnail_url")}
      />

      <div className="grid gap-4 sm:grid-cols-2">
        <Controller
          control={form.control}
          name="category"
          render={({ field }) => (
            <div className="space-y-2">
              <Label htmlFor="category">{mn.admin.fields.category}</Label>
              <Select value={field.value} onValueChange={field.onChange}>
                <SelectTrigger id="category" className="w-full">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {categoryOrder.map((value) => (
                    <SelectItem key={value} value={value}>
                      {categoryLabels[value]}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          )}
        />

        <Controller
          control={form.control}
          name="difficulty"
          render={({ field }) => (
            <div className="space-y-2">
              <Label htmlFor="difficulty">{mn.admin.fields.difficulty}</Label>
              <Select value={field.value} onValueChange={field.onChange}>
                <SelectTrigger id="difficulty" className="w-full">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {difficultyOrder.map((value) => (
                    <SelectItem key={value} value={value}>
                      {difficultyLabels[value]}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          )}
        />
      </div>

      <div className="space-y-4 rounded-lg border p-4">
        <ToggleRow
          control={form.control}
          name="is_free"
          id="is_free"
          label={mn.admin.fields.isFree}
        />
        {!isFree && (
          <FormField
            id="free_lessons"
            type="number"
            min={0}
            step={1}
            label={mn.admin.fields.freeLessons}
            hint={mn.admin.fields.freeLessonsHint}
            error={form.formState.errors.free_lessons?.message}
            {...form.register("free_lessons", { valueAsNumber: true })}
          />
        )}
        <ToggleRow
          control={form.control}
          name="published"
          id="published"
          label={mn.admin.fields.published}
        />
      </div>

      <div className="flex gap-3">
        <Button type="submit" disabled={mutation.isPending}>
          {mutation.isPending ? mn.admin.saving : mn.admin.save}
        </Button>
        <Button type="button" variant="outline" onClick={() => router.push("/admin/courses")}>
          {mn.admin.cancel}
        </Button>
      </div>
    </form>
  );
}

function ToggleRow({
  control,
  name,
  id,
  label,
}: {
  control: ReturnType<typeof useForm<CourseFormValues>>["control"];
  name: "is_free" | "published";
  id: string;
  label: string;
}) {
  return (
    <Controller
      control={control}
      name={name}
      render={({ field }) => (
        <div className="flex items-center justify-between gap-4">
          <Label htmlFor={id} className="font-normal">
            {label}
          </Label>
          <Switch id={id} checked={field.value} onCheckedChange={field.onChange} />
        </div>
      )}
    />
  );
}
