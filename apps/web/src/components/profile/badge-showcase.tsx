"use client";

import { revealBadgeCard } from "@/components/profile/badge-card";
import { BadgeIcon } from "@/components/profile/badge-icon";
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip";
import { formatPercent } from "@/lib/format";
import { mn } from "@/lib/i18n/mn";
import type { BadgeStatus } from "@/lib/types/api";

/** Хэрэглэгчийн сонгосон онцлох амжилтууд — байрных нь дарааллаар. */
export function showcaseBadges(badges: BadgeStatus[]): BadgeStatus[] {
  return badges
    .filter((badge) => badge.earned && badge.showcase_position != null)
    .sort((a, b) => (a.showcase_position ?? 0) - (b.showcase_position ?? 0));
}

/**
 * Энгийн дарлтыг хуудсан дотор нь шийднэ: карт руу гүйлгэж, фокуслана.
 *
 * Хөтчийн `#hash` шилжилтийг хэрэглэхгүй: тэр нь `history.state`-гүй бичлэг
 * үүсгэдэг бөгөөд Next.js үүнийг үл тоодог тул дараа нь өөр хуудас руу ороод
 * «Буцах» дарахад хуудас солигдохгүй. Шинэ цонхонд нээх (Ctrl, дунд товч)
 * хэвээр ажиллана — тэр үед `BadgeSection` hash-аар нь гүйлгэнэ.
 */
function onShowcaseClick(event: React.MouseEvent<HTMLAnchorElement>, key: string) {
  if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) {
    return;
  }
  if (revealBadgeCard(key)) event.preventDefault();
}

/**
 * Нэрийн хажууд харагдах онцлох амжилтууд — хэрэглэгч өөрөө сонгосон
 * хамгийн ихдээ 5 жижиг дүрс.
 *
 * Хулгана аваачих эсвэл Tab-аар очиход амжилтын нэр, хэдэн хувь нь авсныг
 * tooltip-оор харуулна. Дүрс бүр доорх «Achievements» жагсаалтын картын
 * холбоос тул hover-гүй утсан дээр дарахад тухайн карт руу гүйлгэнэ.
 *
 * Сонгоогүй бол юу ч зурахгүй.
 */
export function BadgeShowcase({ badges }: { badges: BadgeStatus[] }) {
  const items = showcaseBadges(badges);
  if (items.length === 0) return null;

  return (
    <TooltipProvider delayDuration={150}>
      <ul aria-label={mn.profile.showcase} className="flex flex-wrap items-center gap-1.5">
        {items.map((badge) => (
          <li key={badge.key} className="flex">
            <Tooltip>
              <TooltipTrigger asChild>
                <a
                  href={`#badge-${badge.key}`}
                  aria-label={badge.rare ? `${badge.name} — ${mn.profile.rare}` : badge.name}
                  onClick={(event) => onShowcaseClick(event, badge.key)}
                  className="focus-visible:ring-ring focus-visible:ring-offset-background flex rounded-md outline-hidden focus-visible:ring-2 focus-visible:ring-offset-2"
                >
                  <BadgeIcon badge={badge} size="sm" className="size-7" />
                </a>
              </TooltipTrigger>
              <TooltipContent className="text-center">
                {/* Нэр нь холбоосын нэрэнд аль хэдийн байгаа — дэлгэц уншигчид давтахгүй. */}
                <p aria-hidden className="font-semibold">
                  {badge.name}
                </p>
                {badge.earned_percent != null && (
                  <p className="opacity-80">
                    {mn.profile.rarity(formatPercent(badge.earned_percent))}
                  </p>
                )}
              </TooltipContent>
            </Tooltip>
          </li>
        ))}
      </ul>
    </TooltipProvider>
  );
}
