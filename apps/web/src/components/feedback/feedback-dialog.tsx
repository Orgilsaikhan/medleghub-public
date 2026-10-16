"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation } from "@tanstack/react-query";
import { usePathname } from "next/navigation";
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
import { sendFeedback } from "@/lib/api/feedback";
import { mn } from "@/lib/i18n/mn";
import type { FeedbackFormKind } from "@/lib/types/api";
import { cn } from "@/lib/utils";
import { feedbackSchema, type FeedbackFormValues } from "@/lib/validation/feedback";

const KINDS: FeedbackFormKind[] = ["idea", "bug", "other"];
const EMPTY: FeedbackFormValues = { kind: "idea", message: "" };

interface FeedbackDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

/**
 * Санал хүсэлт илгээх цонх. Хэрэглэгч аль хуудсанд байсныг хамт илгээнэ —
 * алдааг давтахад хэрэгтэй. Админ `/admin/feedback` дээр уншина.
 */
export function FeedbackDialog({ open, onOpenChange }: FeedbackDialogProps) {
  const pathname = usePathname();
  const form = useForm<FeedbackFormValues>({
    resolver: zodResolver(feedbackSchema),
    defaultValues: EMPTY,
  });

  const mutation = useMutation({
    mutationFn: (values: FeedbackFormValues) =>
      sendFeedback({ ...values, page: pathname.slice(0, 300) }),
    onSuccess: () => {
      toast.success(mn.feedback.sent);
      form.reset(EMPTY);
      onOpenChange(false);
    },
    onError: (error) =>
      toast.error(error instanceof ApiError ? error.message : mn.common.somethingWrong),
  });

  const messageError = form.formState.errors.message?.message;

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>{mn.feedback.title}</DialogTitle>
          <DialogDescription>{mn.feedback.description}</DialogDescription>
        </DialogHeader>

        <form
          id="feedback-form"
          onSubmit={form.handleSubmit((values) => mutation.mutate(values))}
          noValidate
          className="space-y-4"
        >
          <Controller
            control={form.control}
            name="kind"
            render={({ field }) => (
              <div className="space-y-2">
                <Label htmlFor="feedback-kind">{mn.feedback.kind}</Label>
                <Select value={field.value} onValueChange={field.onChange}>
                  <SelectTrigger id="feedback-kind" className="w-full">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {KINDS.map((kind) => (
                      <SelectItem key={kind} value={kind}>
                        {mn.feedback.kinds[kind]}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            )}
          />

          <div className="space-y-2">
            <Label htmlFor="feedback-message">{mn.feedback.message}</Label>
            <Textarea
              id="feedback-message"
              rows={5}
              maxLength={2000}
              placeholder={mn.feedback.messagePlaceholder}
              aria-invalid={messageError ? true : undefined}
              aria-describedby={messageError ? "feedback-message-error" : undefined}
              className={cn(messageError && "border-destructive")}
              {...form.register("message")}
            />
            {messageError && (
              <p id="feedback-message-error" role="alert" className="text-destructive text-xs">
                {messageError}
              </p>
            )}
          </div>
        </form>

        <DialogFooter>
          <Button variant="outline" onClick={() => onOpenChange(false)}>
            {mn.admin.cancel}
          </Button>
          <Button type="submit" form="feedback-form" disabled={mutation.isPending}>
            {mutation.isPending ? mn.feedback.sending : mn.feedback.send}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
