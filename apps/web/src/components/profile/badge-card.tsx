import { CheckIcon, SparklesIcon } from "lucide-react";

import { BadgeIcon } from "@/components/profile/badge-icon";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { formatDate, formatPercent } from "@/lib/format";
import { mn } from "@/lib/i18n/mn";
import type { BadgeStatus } from "@/lib/types/api";
import { cn } from "@/lib/utils";

/** Гүйлгэж очсон картын тодруулга хэр удаан харагдах вэ. */
const HIGHLIGHT_MS = 2000;

function badgeCardId(key: string): string {
  return `badge-${key}`;
}

/**
 * «Achievements» жагсаалтын картыг дээд цэсний доор гүйлгэж, фокуслаад түр
 * тодруулна. Карт хуудсанд байхгүй бол `false`.
 *
 * Фокус нь гар, дэлгэц уншигчийн хэрэглэгчийг картын агуулга руу шилжүүлнэ.
 * Тодруулга (`data-highlight`) нь хулганаар дарсан хүнд аль карт болохыг
 * харуулна — хулганы дараа `:focus-visible` гарахгүй.
 */
export function revealBadgeCard(key: string): boolean {
  const card = document.getElementById(badgeCardId(key));
  if (!card) return false;
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  card.scrollIntoView({ block: "start", behavior: reduceMotion ? "instant" : "smooth" });
  card.focus({ preventScroll: true });
  card.dataset.highlight = "";
  window.setTimeout(() => delete card.dataset.highlight, HIGHLIGHT_MS);
  return true;
}

/**
 * Нэг тэмдэг: дүрс, нэр, нөхцөл, хэдэн хувь нь авсан ба төлөв (авсан / явц /
 * тун удахгүй).
 *
 * `id` нь нэрийн хажуугийн онцлох амжилтын (`BadgeShowcase`) зорилт
 * (`revealBadgeCard`). Утсан дээр дээд цэс хоёр мөр тул `scroll-mt` илүү.
 */
export function BadgeCard({ badge }: { badge: BadgeStatus }) {
  const { progress } = badge;

  return (
    <li
      id={badgeCardId(badge.key)}
      tabIndex={-1}
      data-earned={badge.earned || undefined}
      className={cn(
        "bg-card focus-visible:ring-ring data-highlight:ring-ring flex scroll-mt-32 flex-col items-center gap-3 rounded-xl border p-4 text-center outline-hidden transition-shadow focus-visible:ring-2 data-highlight:ring-2",
        badge.earned && "border-primary/30",
        badge.earned &&
          badge.rare &&
          (badge.prismatic
            ? "border-violet-300/70 shadow-lg shadow-violet-400/20"
            : "border-amber-400/70 shadow-lg shadow-amber-400/15"),
      )}
    >
      <BadgeIcon badge={badge} className="size-20" />

      <div className="min-w-0">
        <h3 className={cn("text-sm font-semibold", !badge.earned && "text-muted-foreground")}>
          {badge.name}
          {badge.rare && <span className="sr-only"> — {mn.profile.rare}</span>}
        </h3>
        {badge.description && (
          <p className="text-muted-foreground mt-1 text-xs leading-snug">{badge.description}</p>
        )}
        {/* «Тун удахгүй» тэмдгийг хэн ч авах боломжгүй — хувь нь утгагүй. */}
        {badge.available && badge.earned_percent != null && (
          <p className="text-muted-foreground mt-1.5 text-xs text-balance tabular-nums">
            {mn.profile.rarity(formatPercent(badge.earned_percent))}
          </p>
        )}
      </div>

      <div className="mt-auto w-full pt-1">
        {badge.earned ? (
          <p className="text-success flex items-center justify-center gap-1 text-xs font-medium">
            <CheckIcon className="size-3.5" aria-hidden />
            {badge.awarded_at ? mn.profile.earnedOn(formatDate(badge.awarded_at)) : null}
          </p>
        ) : !badge.available ? (
          <Badge variant="secondary">{mn.profile.comingSoon}</Badge>
        ) : badge.secret ? (
          <Badge variant="secondary">
            <SparklesIcon aria-hidden />
            {mn.profile.secret}
          </Badge>
        ) : progress ? (
          <div className="space-y-1">
            <Progress
              value={Math.round((progress.current / progress.target) * 100)}
              aria-label={`${badge.name}: ${mn.profile.progress(progress.current, progress.target)}`}
            />
            <p className="text-muted-foreground text-xs tabular-nums">
              {mn.profile.progress(progress.current, progress.target)}
            </p>
          </div>
        ) : (
          <p className="text-muted-foreground text-xs">{mn.profile.locked}</p>
        )}
      </div>
    </li>
  );
}
