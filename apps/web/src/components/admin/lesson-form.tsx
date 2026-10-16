"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useRouter } from "next/navigation";
import { Controller, useForm, useWatch } from "react-hook-form";
import { toast } from "sonner";

import { FormField } from "@/components/auth/form-field";
import { LessonContent } from "@/components/learn/lesson-content";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Textarea } from "@/components/ui/textarea";
import { createLesson, updateLesson } from "@/lib/api/admin";
import { ApiError } from "@/lib/api/client";
import { suggestSlug } from "@/lib/format";
import { mn } from "@/lib/i18n/mn";
import { queryKeys } from "@/lib/query-keys";
import type { LessonDetail } from "@/lib/types/api";
import { lessonSchema, type LessonFormValues } from "@/lib/validation/admin";

interface LessonFormProps {
  /** Байхгүй бол шинэ хичээл үүсгэнэ. */
  lesson?: LessonDetail;
  /** Шинэ хичээл аль модулд харьяалагдах вэ. */
  moduleId?: string;
  /** Хадгалсны дараа буцах сургалтын ID. */
  courseId?: string;
}

const DEFAULT_CODE = 'console.log("Сайн байна уу!");\n';

function toValues(lesson?: LessonDetail): LessonFormValues {
  return {
    title: lesson?.title ?? "",
    slug: lesson?.slug ?? "",
    description: lesson?.description ?? "",
    video_url: lesson?.video_url ?? "",
    duration_minutes: lesson ? Math.round(lesson.duration / 60) : 0,
    content: lesson?.content ?? "",
    initial_code: lesson?.initial_code ?? DEFAULT_CODE,
    published: lesson?.published ?? false,
  };
}

export function LessonForm({ lesson, moduleId, courseId }: LessonFormProps) {
  const router = useRouter();
  const queryClient = useQueryClient();
  const isEdit = Boolean(lesson);

  const form = useForm<LessonFormValues>({
    resolver: zodResolver(lessonSchema),
    defaultValues: toValues(lesson),
  });

  // `useWatch` нь `watch()`-оос ялгаатай нь дахин render-ийг нарийн хянадаг.
  const preview = useWatch({ control: form.control, name: "content" });

  const mutation = useMutation({
    mutationFn: (values: LessonFormValues) => {
      const { duration_minutes, video_url, ...rest } = values;
      const payload = {
        ...rest,
        // Формд минутаар, API-д секундээр.
        duration: Math.round(duration_minutes * 60),
        video_url: video_url || null,
        language: lesson?.language ?? ("javascript" as const),
      };
      if (lesson) return updateLesson(lesson.id, payload);
      if (!moduleId) throw new Error("moduleId required");
      return createLesson(moduleId, payload);
    },
    onSuccess: () => {
      toast.success(mn.admin.saved);
      void queryClient.invalidateQueries({ queryKey: queryKeys.lessons.all });
      if (courseId) {
        void queryClient.invalidateQueries({ queryKey: queryKeys.admin.course(courseId) });
      }
      void queryClient.invalidateQueries({ queryKey: queryKeys.courses.all });
      if (courseId) router.push(`/admin/courses/${courseId}/modules`);
      else router.refresh();
    },
    onError: (error) => {
      if (error instanceof ApiError && error.code === "LESSON_SLUG_TAKEN") {
        form.setError("slug", { message: error.message });
      }
    },
  });

  const slugHandled =
    mutation.error instanceof ApiError && mutation.error.code === "LESSON_SLUG_TAKEN";
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
      className="space-y-6"
    >
      {serverError && (
        <Alert variant="destructive" className="bg-destructive/5">
          <AlertDescription>{serverError}</AlertDescription>
        </Alert>
      )}

      <div className="grid gap-6 lg:grid-cols-2">
        <div className="space-y-6">
          <FormField
            id="title"
            label={mn.admin.fields.title}
            error={form.formState.errors.title?.message}
            {...form.register("title", {
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
            <Textarea id="description" rows={2} {...form.register("description")} />
          </div>

          <FormField
            id="video_url"
            label={mn.admin.fields.videoUrl}
            hint={mn.admin.fields.videoUrlHint}
            placeholder="https://…/video.m3u8"
            error={form.formState.errors.video_url?.message}
            {...form.register("video_url")}
          />

          <FormField
            id="duration_minutes"
            type="number"
            min={0}
            step={1}
            label={mn.admin.fields.duration}
            error={form.formState.errors.duration_minutes?.message}
            {...form.register("duration_minutes", { valueAsNumber: true })}
          />

          <Controller
            control={form.control}
            name="published"
            render={({ field }) => (
              <div className="flex items-center justify-between gap-4 rounded-lg border p-4">
                <Label htmlFor="published" className="font-normal">
                  {mn.admin.fields.published}
                </Label>
                <Switch id="published" checked={field.value} onCheckedChange={field.onChange} />
              </div>
            )}
          />
        </div>

        <div className="space-y-6">
          <div className="space-y-2">
            <Label htmlFor="content">{mn.admin.fields.content}</Label>
            <Tabs defaultValue="write">
              <TabsList>
                <TabsTrigger value="write">Markdown</TabsTrigger>
                <TabsTrigger value="preview">Урьдчилан харах</TabsTrigger>
              </TabsList>

              <TabsContent value="write">
                <Textarea
                  id="content"
                  rows={16}
                  className="font-mono text-[13px]"
                  {...form.register("content")}
                />
              </TabsContent>

              <TabsContent value="preview">
                <div className="min-h-[22rem] rounded-lg border p-4">
                  <LessonContent content={preview} />
                </div>
              </TabsContent>
            </Tabs>
            {form.formState.errors.content && (
              <p role="alert" className="text-destructive text-xs">
                {form.formState.errors.content.message}
              </p>
            )}
          </div>

          <div className="space-y-2">
            <Label htmlFor="initial_code">{mn.admin.fields.initialCode}</Label>
            <Textarea
              id="initial_code"
              rows={10}
              className="bg-code-bg font-mono text-[13px]"
              spellCheck={false}
              {...form.register("initial_code")}
            />
            {form.formState.errors.initial_code && (
              <p role="alert" className="text-destructive text-xs">
                {form.formState.errors.initial_code.message}
              </p>
            )}
          </div>
        </div>
      </div>

      <div className="flex gap-3">
        <Button type="submit" disabled={mutation.isPending}>
          {mutation.isPending ? mn.admin.saving : mn.admin.save}
        </Button>
        <Button type="button" variant="outline" onClick={() => router.back()}>
          {mn.admin.cancel}
        </Button>
      </div>
    </form>
  );
}
