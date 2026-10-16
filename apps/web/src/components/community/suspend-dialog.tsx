"use client";

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { BanIcon } from "lucide-react";
import { useId, useState } from "react";
import { toast } from "sonner";

import { useCommunityStatus } from "@/components/community/community-gate";
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
import { Textarea } from "@/components/ui/textarea";
import { suspendUser } from "@/lib/api/admin";
import { ApiError } from "@/lib/api/client";
import { formatDate } from "@/lib/format";
import { mn } from "@/lib/i18n/mn";
import { queryKeys } from "@/lib/query-keys";
import type { PostAuthor } from "@/lib/types/api";
import { cn } from "@/lib/utils";

const MIN_REASON = 5;
const MAX_REASON = 500;

interface SuspendDialogProps {
  user: PostAuthor;
  /** Зөвхөн дүрстэй жижиг товч (сэтгэгдэл дээр). */
  compact?: boolean;
}

/**
 * Админ: зохиогчийг Community-оос түдгэлзүүлнэ. Хэд дэх удаа, хэдэн хоног
 * гэдгийг сервер тооцно (7 → 14 → 30 хоног, дараа нь бүрмөсөн).
 */
export function SuspendDialog({ user, compact = false }: SuspendDialogProps) {
  const id = useId();
  const queryClient = useQueryClient();
  const [open, setOpen] = useState(false);
  const [reason, setReason] = useState("");
  const [touched, setTouched] = useState(false);
  const days = useCommunityStatus().data?.suspension_days ?? [];

  const trimmed = reason.trim();
  const error =
    touched && trimmed.length < MIN_REASON ? "Шалтгааныг дор хаяж 5 тэмдэгтээр бичнэ үү." : null;

  const mutation = useMutation({
    mutationFn: () => suspendUser(user.id, trimmed),
    onSuccess: (result) => {
      toast.success(
        result.ends_at
          ? mn.community.suspendedToast(user.name, formatDate(result.ends_at), result.level)
          : mn.community.suspendedForeverToast(user.name, result.level),
      );
      void queryClient.invalidateQueries({ queryKey: queryKeys.admin.suspensionsAll });
      setReason("");
      setTouched(false);
      setOpen(false);
    },
    onError: (err) => toast.error(err instanceof ApiError ? err.message : mn.common.somethingWrong),
  });

  function submit(event: React.FormEvent) {
    event.preventDefault();
    setTouched(true);
    if (trimmed.length >= MIN_REASON) mutation.mutate();
  }

  const guidelines = mn.community.guidelines;

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        {compact ? (
          <Button
            variant="ghost"
            size="icon-sm"
            aria-label={mn.community.suspend}
            title={mn.community.suspend}
          >
            <BanIcon />
          </Button>
        ) : (
          <Button variant="ghost" size="sm">
            <BanIcon />
            {mn.community.suspend}
          </Button>
        )}
      </DialogTrigger>

      <DialogContent>
        <DialogHeader>
          <DialogTitle>{mn.community.suspendTitle}</DialogTitle>
          <DialogDescription>{mn.community.suspendDescription(user.name)}</DialogDescription>
        </DialogHeader>

        {days.length > 0 && (
          <ul className="text-muted-foreground space-y-0.5 text-sm">
            {days.map((count, index) => (
              <li key={count}>{guidelines.penaltyStep(index + 1, count)}</li>
            ))}
            <li>{guidelines.penaltyPermanent(days.length + 1)}</li>
          </ul>
        )}

        <form id={`${id}-form`} onSubmit={submit} noValidate className="space-y-2">
          <Label htmlFor={`${id}-reason`}>{mn.community.suspendReason}</Label>
          <Textarea
            id={`${id}-reason`}
            rows={3}
            maxLength={MAX_REASON}
            value={reason}
            onChange={(event) => setReason(event.target.value)}
            placeholder={mn.community.suspendReasonPlaceholder}
            aria-invalid={error ? true : undefined}
            aria-describedby={error ? `${id}-reason-error` : undefined}
            className={cn(error && "border-destructive")}
          />
          {error && (
            <p id={`${id}-reason-error`} role="alert" className="text-destructive text-xs">
              {error}
            </p>
          )}
        </form>

        <DialogFooter>
          <Button variant="outline" onClick={() => setOpen(false)}>
            {mn.admin.cancel}
          </Button>
          {/* `destructive` хувилбар харанхуй горимд 4.5:1-д хүрдэггүй. */}
          <Button type="submit" form={`${id}-form`} disabled={mutation.isPending}>
            {mutation.isPending ? mn.community.suspending : mn.community.suspend}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
