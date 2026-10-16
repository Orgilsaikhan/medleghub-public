"use client";

import Link from "next/link";
import { type ReactNode, useState } from "react";

import { FeedbackDialog } from "@/components/feedback/feedback-dialog";
import { useCurrentUser } from "@/lib/hooks/use-auth";
import { mn } from "@/lib/i18n/mn";
import { cn } from "@/lib/utils";

/**
 * Хөлийн «Санал хүсэлт» холбоос. Нэвтрээгүй бол нэвтрэх хуудас руу.
 *
 * `icon` — бичвэрийн өмнөх дүрс (хөлийн «Холбоо барих» мөрүүдтэй ижил).
 */
export function FeedbackLink({ className, icon }: { className?: string; icon?: ReactNode }) {
  const { isAuthenticated } = useCurrentUser();
  const [open, setOpen] = useState(false);

  if (!isAuthenticated) {
    return (
      <Link href="/login" className={className}>
        {icon}
        {mn.feedback.open}
      </Link>
    );
  }

  return (
    <>
      <button
        type="button"
        onClick={() => setOpen(true)}
        className={cn("cursor-pointer", className)}
      >
        {icon}
        {mn.feedback.open}
      </button>
      <FeedbackDialog open={open} onOpenChange={setOpen} />
    </>
  );
}
