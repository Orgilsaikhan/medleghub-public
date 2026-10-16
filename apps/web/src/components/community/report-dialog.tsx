"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation } from "@tanstack/react-query";
import { FlagIcon } from "lucide-react";
import { useId, useState } from "react";
import { Controller, useForm } from "react-hook-form";
import { toast } from "sonner";

import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
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
import { reportComment, reportPost } from "@/lib/api/community";
import { mn } from "@/lib/i18n/mn";
import type { ReportReason } from "@/lib/types/api";
import { cn } from "@/lib/utils";
import { reportSchema, type ReportFormValues } from "@/lib/validation/community";

const REASONS: ReportReason[] = ["spam", "abuse", "other"];
const EMPTY: ReportFormValues = { reason: "spam", details: "" };

interface ReportDialogProps {
  target: { kind: "post" | "comment"; id: string };
  /** Зөвхөн дүрстэй жижиг товч (сэтгэгдэл дээр). */
  compact?: boolean;
}

/**
 * «Мэдэгдэх» — гомдол админы «Санал хүсэлт» хуудсанд очно. Сервер нь
 * агуулгын хуулбарыг хамт хадгална, зохиогч дараа нь устгасан ч админ харна.
 */
export function ReportDialog({ target, compact = false }: ReportDialogProps) {
  const [open, setOpen] = useState(false);
  const id = useId();
  const form = useForm<ReportFormValues>({
    resolver: zodResolver(reportSchema),
    defaultValues: EMPTY,
  });

  const mutation = useMutation({
    mutationFn: (values: ReportFormValues) => {
      const input = { reason: values.reason, details: values.details || null };
      return target.kind === "post"
        ? reportPost(target.id, input)
        : reportComment(target.id, input);
    },
    onSuccess: () => {
      toast.success(mn.community.reported);
      form.reset(EMPTY);
      setOpen(false);
    },
    onError: (error) =>
      toast.error(error instanceof ApiError ? error.message : mn.common.somethingWrong),
  });

  const detailsError = form.formState.errors.details?.message;
  const title =
    target.kind === "post" ? mn.community.reportPostTitle : mn.community.reportCommentTitle;

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        {compact ? (
          <Button
            variant="ghost"
            size="icon-sm"
            aria-label={mn.community.report}
            title={mn.community.report}
          >
            <FlagIcon />
          </Button>
        ) : (
          <Button variant="ghost" size="sm">
            <FlagIcon />
            {mn.community.report}
          </Button>
        )}
      </DialogTrigger>

      <DialogContent>
        <DialogHeader>
          <DialogTitle>{title}</DialogTitle>
          <DialogDescription>{mn.community.reportDescription}</DialogDescription>
        </DialogHeader>

        <form
          id={`${id}-form`}
          onSubmit={form.handleSubmit((values) => mutation.mutate(values))}
          noValidate
          className="space-y-4"
        >
          <Controller
            control={form.control}
            name="reason"
            render={({ field }) => (
              <div className="space-y-2">
                <Label htmlFor={`${id}-reason`}>{mn.community.reportReason}</Label>
                <Select value={field.value} onValueChange={field.onChange}>
                  <SelectTrigger id={`${id}-reason`} className="w-full">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {REASONS.map((reason) => (
                      <SelectItem key={reason} value={reason}>
                        {mn.community.reportReasons[reason]}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            )}
          />

          <div className="space-y-2">
            <Label htmlFor={`${id}-details`}>{mn.community.reportDetails}</Label>
            <Textarea
              id={`${id}-details`}
              rows={3}
              maxLength={500}
              aria-invalid={detailsError ? true : undefined}
              aria-describedby={detailsError ? `${id}-details-error` : undefined}
              className={cn(detailsError && "border-destructive")}
              {...form.register("details")}
            />
            {detailsError && (
              <p id={`${id}-details-error`} role="alert" className="text-destructive text-xs">
                {detailsError}
              </p>
            )}
          </div>
        </form>

        <DialogFooter>
          <Button variant="outline" onClick={() => setOpen(false)}>
            {mn.admin.cancel}
          </Button>
          <Button type="submit" form={`${id}-form`} disabled={mutation.isPending}>
            {mutation.isPending ? mn.community.reportSending : mn.community.report}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
