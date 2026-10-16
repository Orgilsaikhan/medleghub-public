"use client";

import { Button } from "@/components/ui/button";
import { useNow } from "@/lib/hooks/use-now";
import { mn } from "@/lib/i18n/mn";

/** Supabase нэг хэрэглэгчид 60 секундэд нэг л код илгээдэг. */
const RESEND_COOLDOWN_SECONDS = 60;

interface ResendCodeButtonProps {
  /** Сүүлд код илгээсэн мөч (мс). `null` бол хүлээлгүй. */
  sentAt: number | null;
  pending: boolean;
  onResend: () => void;
}

/** «Код дахин илгээх» — илгээснээс хойш 60 секунд идэвхгүй. */
export function ResendCodeButton({ sentAt, pending, onResend }: ResendCodeButtonProps) {
  const now = useNow(sentAt !== null);
  const left =
    sentAt === null ? 0 : Math.ceil((sentAt + RESEND_COOLDOWN_SECONDS * 1000 - now) / 1000);
  const seconds = Math.min(Math.max(left, 0), RESEND_COOLDOWN_SECONDS);

  return (
    <Button
      type="button"
      variant="link"
      size="sm"
      className="h-auto px-0"
      disabled={pending || seconds > 0}
      onClick={onResend}
    >
      {seconds > 0 ? mn.auth.resendIn(seconds) : mn.auth.resend}
    </Button>
  );
}
