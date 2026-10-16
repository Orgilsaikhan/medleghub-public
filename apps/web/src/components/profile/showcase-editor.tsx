"use client";

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { PencilIcon, SparklesIcon } from "lucide-react";
import { useState } from "react";
import { toast } from "sonner";

import { BadgeIcon } from "@/components/profile/badge-icon";
import { showcaseBadges } from "@/components/profile/badge-showcase";
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
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip";
import { ApiError } from "@/lib/api/client";
import { updateShowcase } from "@/lib/api/profile";
import { formatPercent } from "@/lib/format";
import { mn } from "@/lib/i18n/mn";
import { queryKeys } from "@/lib/query-keys";
import type { BadgeStatus, Profile } from "@/lib/types/api";
import { cn } from "@/lib/utils";

/** API-ийн `SHOWCASE_MAX`-тай (`app/models/badge.py`) ижил байх ёстой. */
export const BADGE_SHOWCASE_MAX = 5;

/**
 * Өөрийн профайл дээр онцлох амжилтаа сонгох товч ба цонх.
 *
 * Сонгоогүй бол «Онцлох амжилт сонгох» товч, сонгосон бол дүрсүүдийн ард
 * жижиг харандаа харагдана. Нэг ч амжилт аваагүй бол юу ч зурахгүй.
 *
 * Товчнууд нь `DialogTrigger` — цонх хаагдахад фокус товч руугаа буцна.
 * Хадгалж байх үед цонхыг хаахгүй: дуусаагүй хүсэлт дараа нь дахин нээсэн
 * цонхыг хаачихна.
 */
export function ShowcaseEditor({ badges }: { badges: BadgeStatus[] }) {
  const queryClient = useQueryClient();
  const [open, setOpen] = useState(false);

  const mutation = useMutation({
    mutationFn: updateShowcase,
    onSuccess: ({ badge_keys }) => {
      queryClient.setQueryData<Profile>(queryKeys.me.profile, (old) =>
        old
          ? {
              ...old,
              badges: old.badges.map((badge) => {
                const index = badge_keys.indexOf(badge.key);
                return { ...badge, showcase_position: index === -1 ? null : index + 1 };
              }),
            }
          : old,
      );
      toast.success(mn.profile.showcaseSaved);
      setOpen(false);
    },
    onError: (error) =>
      toast.error(error instanceof ApiError ? error.message : mn.common.somethingWrong),
  });

  if (!badges.some((badge) => badge.earned)) return null;
  const pending = mutation.isPending;

  return (
    <Dialog
      open={open}
      onOpenChange={(next) => {
        if (!pending) setOpen(next);
      }}
    >
      {showcaseBadges(badges).length > 0 ? (
        <TooltipProvider delayDuration={150}>
          <Tooltip>
            <TooltipTrigger asChild>
              <DialogTrigger asChild>
                <Button variant="ghost" size="icon-sm" aria-label={mn.profile.showcaseEdit}>
                  <PencilIcon aria-hidden />
                </Button>
              </DialogTrigger>
            </TooltipTrigger>
            <TooltipContent>
              {/* Товчны нэрэнд байгаа — дэлгэц уншигчид давтахгүй. */}
              <span aria-hidden>{mn.profile.showcaseEdit}</span>
            </TooltipContent>
          </Tooltip>
        </TooltipProvider>
      ) : (
        // Нарийн дэлгэцэд мөр шилжинэ — «Тохиргоо» товч руу давхцахгүй.
        <DialogTrigger asChild>
          <Button
            variant="outline"
            size="sm"
            className="h-auto min-h-7 max-w-full text-left whitespace-normal"
          >
            <SparklesIcon aria-hidden />
            {mn.profile.showcaseAdd}
          </Button>
        </DialogTrigger>
      )}

      {/* Намхан дэлгэцэд (хэвтээ утас) жагсаалт нь багасч, толгой, товчнууд харагдана. */}
      <DialogContent className="max-h-[calc(100dvh-2rem)] grid-rows-[auto_auto_minmax(0,1fr)_auto] sm:max-w-lg">
        {/* Цонх нээгдэх бүрт шинээр mount хийгдэж, одоогийн сонголтоос эхэлнэ. */}
        <ShowcasePicker
          badges={badges}
          pending={pending}
          onSave={(keys) => mutation.mutate(keys)}
          onCancel={() => setOpen(false)}
        />
      </DialogContent>
    </Dialog>
  );
}

interface ShowcasePickerProps {
  badges: BadgeStatus[];
  pending: boolean;
  onSave: (keys: string[]) => void;
  onCancel: () => void;
}

/**
 * Авсан амжилтуудын жагсаалт — дарж сонгох, дахин дарж болих. Сонгосон
 * дарааллаараа нэрийн хажууд харагдана (1, 2, …).
 */
function ShowcasePicker({ badges, pending, onSave, onCancel }: ShowcasePickerProps) {
  const earned = badges.filter((badge) => badge.earned);
  const [selected, setSelected] = useState(() => showcaseBadges(badges).map((badge) => badge.key));
  const full = selected.length >= BADGE_SHOWCASE_MAX;

  function toggle(key: string) {
    setSelected((current) => {
      if (current.includes(key)) return current.filter((item) => item !== key);
      return current.length >= BADGE_SHOWCASE_MAX ? current : [...current, key];
    });
  }

  return (
    <>
      <DialogHeader>
        <DialogTitle>{mn.profile.showcase}</DialogTitle>
        <DialogDescription>{mn.profile.showcaseHint(BADGE_SHOWCASE_MAX)}</DialogDescription>
      </DialogHeader>

      <p aria-live="polite" className="text-muted-foreground text-sm tabular-nums">
        {mn.profile.showcaseCount(selected.length, BADGE_SHOWCASE_MAX)}
        {full && ` · ${mn.profile.showcaseFull(BADGE_SHOWCASE_MAX)}`}
      </p>

      <ul className="-mx-1 grid max-h-[55vh] min-h-0 gap-2 overflow-y-auto p-1 sm:grid-cols-2">
        {earned.map((badge) => {
          const index = selected.indexOf(badge.key);
          const isSelected = index !== -1;
          return (
            <li key={badge.key}>
              <button
                type="button"
                aria-pressed={isSelected}
                disabled={pending || (!isSelected && full)}
                onClick={() => toggle(badge.key)}
                className={cn(
                  "hover:bg-muted/60 focus-visible:ring-ring flex w-full items-center gap-3 rounded-lg border p-2 text-left outline-hidden transition-colors focus-visible:ring-2 disabled:cursor-not-allowed disabled:opacity-50",
                  isSelected && "border-primary bg-primary/10 hover:bg-primary/15",
                )}
              >
                <BadgeIcon badge={badge} size="sm" className="size-9" />
                <span className="min-w-0 flex-1">
                  <span className="line-clamp-2 text-sm font-medium break-words">{badge.name}</span>
                  {badge.earned_percent != null && (
                    <span className="text-muted-foreground block text-xs text-balance">
                      {mn.profile.rarity(formatPercent(badge.earned_percent))}
                    </span>
                  )}
                </span>
                <span
                  aria-hidden
                  className={cn(
                    "grid size-6 shrink-0 place-items-center rounded-full border text-xs font-semibold tabular-nums",
                    isSelected
                      ? "border-primary bg-primary text-primary-foreground"
                      : "border-muted-foreground/40",
                  )}
                >
                  {isSelected ? index + 1 : null}
                </span>
                {isSelected && (
                  <span className="sr-only">, {mn.profile.showcasePosition(index + 1)}</span>
                )}
              </button>
            </li>
          );
        })}
      </ul>

      <DialogFooter>
        <Button variant="outline" onClick={onCancel} disabled={pending}>
          {mn.profile.showcaseCancel}
        </Button>
        <Button onClick={() => onSave(selected)} disabled={pending}>
          {pending ? mn.profile.showcaseSaving : mn.profile.showcaseSave}
        </Button>
      </DialogFooter>
    </>
  );
}
