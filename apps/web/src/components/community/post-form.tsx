"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Controller, useForm } from "react-hook-form";
import { toast } from "sonner";

import { useIsSuspended } from "@/components/community/community-gate";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";
import { ApiError } from "@/lib/api/client";
import { createPost } from "@/lib/api/community";
import {
  mn,
  postLanguageLabels,
  postLanguageOrder,
  postTypeLabels,
  postTypeOrder,
} from "@/lib/i18n/mn";
import { queryKeys } from "@/lib/query-keys";
import { cn } from "@/lib/utils";
import { postSchema, type PostFormValues } from "@/lib/validation/community";

/** Шинэ нийтлэл — хэл, төрлийн шошго заавал. Хавсралтгүй, зөвхөн текст. */
export function PostForm() {
  const router = useRouter();
  const queryClient = useQueryClient();
  const suspended = useIsSuspended();
  const form = useForm<PostFormValues>({
    resolver: zodResolver(postSchema),
    defaultValues: { title: "", body: "" },
  });

  const mutation = useMutation({
    mutationFn: createPost,
    onSuccess: (post) => {
      queryClient.setQueryData(queryKeys.community.post(post.id), post);
      void queryClient.invalidateQueries({ queryKey: queryKeys.community.lists });
      toast.success(mn.community.published);
      router.push(`/community/${post.id}`);
    },
    onError: (error) =>
      toast.error(error instanceof ApiError ? error.message : mn.common.somethingWrong),
  });

  const { errors } = form.formState;
  // Дээд талын `CommunityGate` түдгэлзсэн тухай мэдэгдлийг харуулна.
  if (suspended) return null;

  return (
    <form
      onSubmit={form.handleSubmit((values) => mutation.mutate(values))}
      noValidate
      className="bg-card space-y-6 rounded-xl border p-6"
    >
      <div className="grid gap-4 sm:grid-cols-2">
        <Controller
          control={form.control}
          name="language"
          render={({ field }) => (
            <div className="space-y-2">
              <Label htmlFor="post-language">{mn.community.languageLabel}</Label>
              <Select value={field.value ?? ""} onValueChange={field.onChange}>
                <SelectTrigger
                  id="post-language"
                  className="w-full"
                  aria-invalid={errors.language ? true : undefined}
                  aria-describedby={errors.language ? "post-language-error" : undefined}
                >
                  <SelectValue placeholder={mn.community.chooseLanguage} />
                </SelectTrigger>
                <SelectContent>
                  {postLanguageOrder.map((value) => (
                    <SelectItem key={value} value={value}>
                      {postLanguageLabels[value]}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              <FieldError id="post-language-error" message={errors.language?.message} />
            </div>
          )}
        />

        <Controller
          control={form.control}
          name="type"
          render={({ field }) => (
            <div className="space-y-2">
              <Label htmlFor="post-type">{mn.community.typeLabel}</Label>
              <Select value={field.value ?? ""} onValueChange={field.onChange}>
                <SelectTrigger
                  id="post-type"
                  className="w-full"
                  aria-invalid={errors.type ? true : undefined}
                  aria-describedby={errors.type ? "post-type-error" : undefined}
                >
                  <SelectValue placeholder={mn.community.chooseType} />
                </SelectTrigger>
                <SelectContent>
                  {postTypeOrder.map((value) => (
                    <SelectItem key={value} value={value}>
                      {postTypeLabels[value]}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              <FieldError id="post-type-error" message={errors.type?.message} />
            </div>
          )}
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="post-title">{mn.community.postTitle}</Label>
        <Input
          id="post-title"
          maxLength={150}
          placeholder={mn.community.postTitlePlaceholder}
          aria-invalid={errors.title ? true : undefined}
          aria-describedby={errors.title ? "post-title-error" : undefined}
          className={cn(errors.title && "border-destructive")}
          {...form.register("title")}
        />
        <FieldError id="post-title-error" message={errors.title?.message} />
      </div>

      <div className="space-y-2">
        <Label htmlFor="post-body">{mn.community.postBody}</Label>
        <Textarea
          id="post-body"
          rows={10}
          maxLength={10_000}
          placeholder={mn.community.postBodyPlaceholder}
          aria-invalid={errors.body ? true : undefined}
          aria-describedby={cn("post-body-hint", errors.body && "post-body-error")}
          className={cn(
            "min-h-48 font-mono text-sm md:text-sm",
            errors.body && "border-destructive",
          )}
          {...form.register("body")}
        />
        <p id="post-body-hint" className="text-muted-foreground text-xs">
          {mn.community.markdownHint}
        </p>
        <FieldError id="post-body-error" message={errors.body?.message} />
      </div>

      <div className="flex justify-end gap-2">
        <Button asChild variant="outline">
          <Link href="/community">{mn.admin.cancel}</Link>
        </Button>
        <Button type="submit" disabled={mutation.isPending}>
          {mutation.isPending ? mn.community.publishing : mn.community.publish}
        </Button>
      </div>
    </form>
  );
}

function FieldError({ id, message }: { id: string; message?: string }) {
  if (!message) return null;
  return (
    <p id={id} role="alert" className="text-destructive text-xs">
      {message}
    </p>
  );
}
