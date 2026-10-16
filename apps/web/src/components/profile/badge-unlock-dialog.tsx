"use client";

import { useRouter } from "next/navigation";

import { BadgeIcon } from "@/components/profile/badge-icon";
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
import type { BadgeStatus } from "@/lib/types/api";
import { cn } from "@/lib/utils";

/** Нээгдсэн тэмдэг: `BadgeStatus` эсвэл хичээлээр ирсэн `BadgeUnlocked`. */
type UnlockedBadge = Pick<
  BadgeStatus,
  "key" | "name" | "description" | "shape" | "secret" | "rare" | "prismatic"
>;

/** Солонгон гэрэл — `badge-icon.tsx`-ийнхтэй ижил өнгө. */
const PRISMATIC = "bg-[conic-gradient(#f9a8d4,#c4b5fd,#93c5fd,#6ee7b7,#fde68a,#fdba74,#f9a8d4)]";

/**
 * Онцгой тэмдэг нээгдэх мөч — жижиг мэдэгдлийн оронд том цонх: дүрс, нэр,
 * тайлбар, солонгон гэрэлтэй.
 */
export function BadgeUnlockDialog({
  badge,
  onClose,
}: {
  badge: UnlockedBadge | null;
  onClose: () => void;
}) {
  const router = useRouter();

  return (
    <Dialog open={badge !== null} onOpenChange={(open) => !open && onClose()}>
      <DialogContent
        // Тайлбаргүй тэмдэгт Radix-ийн «Description дутуу» анхааруулгыг хаана.
        {...(!badge?.description && { "aria-describedby": undefined })}
        className={cn(
          "overflow-hidden p-8 sm:max-w-md",
          badge?.prismatic && "shadow-[0_0_80px_-12px_rgba(196,181,253,0.75)] ring-violet-300/40",
        )}
      >
        {badge?.prismatic && (
          <>
            <span
              aria-hidden
              className={cn(
                "absolute -top-28 left-1/2 -z-10 size-72 -translate-x-1/2 rounded-full opacity-30 blur-3xl",
                PRISMATIC,
              )}
            />
            <span
              aria-hidden
              className={cn(
                "absolute inset-x-0 bottom-0 -z-10 h-1 opacity-80 blur-[1px]",
                "bg-[linear-gradient(90deg,#f9a8d4,#c4b5fd,#93c5fd,#6ee7b7,#fde68a,#fdba74)]",
              )}
            />
          </>
        )}

        {badge && (
          <DialogHeader className="items-center gap-3 text-center">
            <BadgeIcon badge={{ ...badge, earned: true, secret: false }} className="mb-2 size-36" />
            <p className="text-muted-foreground text-xs font-medium tracking-widest uppercase">
              {badge.secret ? mn.profile.unlockedSecretEyebrow : mn.profile.unlockedEyebrow}
            </p>
            <DialogTitle className="text-2xl font-bold tracking-tight">{badge.name}</DialogTitle>
            {badge.description && (
              <DialogDescription className="text-foreground/85 text-base leading-relaxed text-pretty">
                {badge.description}
              </DialogDescription>
            )}
          </DialogHeader>
        )}

        <DialogFooter className="mt-2 sm:justify-center">
          <Button variant="outline" onClick={() => router.push("/profile")}>
            {mn.profile.newBadgeAction}
          </Button>
          <Button onClick={onClose}>{mn.profile.unlockedClose}</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
