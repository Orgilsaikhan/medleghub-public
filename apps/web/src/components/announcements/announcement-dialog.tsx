"use client";

import { MegaphoneIcon, SparklesIcon } from "lucide-react";
import Link from "next/link";

import { CommunityMarkdown } from "@/components/community/community-markdown";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { mn } from "@/lib/i18n/mn";
import type { Announcement } from "@/lib/types/api";

/** Сайтын хуудас мөн эсэх — гадны `https://` холбоосыг шинэ цонхонд нээнэ. */
function isInternal(url: string): boolean {
  return url.startsWith("/") && !url.startsWith("//");
}

/**
 * Зарлалын цонх — хэрэглэгчид гарах болон админы «Урьдчилан харах» хоёуланд.
 * Бичвэр нь Community-ийнх шиг Markdown (HTML, зураггүй).
 */
export function AnnouncementDialog({
  announcement,
  open,
  onClose,
}: {
  announcement: Pick<Announcement, "kind" | "title" | "body" | "cta_label" | "cta_url">;
  open: boolean;
  /** Хаасан, эсвэл товчийг дарсан — аль алинд нь дахин харуулахгүй. */
  onClose: () => void;
}) {
  const Icon = announcement.kind === "feature" ? MegaphoneIcon : SparklesIcon;
  const { cta_label: label, cta_url: url } = announcement;

  return (
    <Dialog open={open} onOpenChange={(next) => !next && onClose()}>
      <DialogContent className="gap-5 p-6 sm:max-w-md">
        <DialogHeader className="gap-3">
          <p className="text-brand-link flex items-center gap-2 text-xs font-semibold tracking-widest uppercase">
            <Icon className="size-4" aria-hidden />
            {mn.announcements.eyebrow[announcement.kind]}
          </p>
          <DialogTitle className="text-xl font-bold tracking-tight text-balance">
            {announcement.title}
          </DialogTitle>
          <DialogDescription asChild>
            <div className="text-foreground/85 text-sm leading-relaxed">
              <CommunityMarkdown source={announcement.body} />
            </div>
          </DialogDescription>
        </DialogHeader>

        <DialogFooter className="gap-2 sm:justify-end">
          {label && url ? (
            <>
              <Button variant="outline" onClick={onClose}>
                {mn.announcements.close}
              </Button>
              <Button asChild>
                {isInternal(url) ? (
                  <Link href={url} onClick={onClose}>
                    {label}
                  </Link>
                ) : (
                  <a href={url} target="_blank" rel="noopener noreferrer" onClick={onClose}>
                    {label}
                  </a>
                )}
              </Button>
            </>
          ) : (
            <Button onClick={onClose}>{mn.announcements.gotIt}</Button>
          )}
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
