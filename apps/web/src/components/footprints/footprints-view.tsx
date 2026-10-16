"use client";

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { FootprintsIcon } from "lucide-react";
import Link from "next/link";
import { useEffect, useRef, useState } from "react";

import { BadgeUnlockDialog } from "@/components/profile/badge-unlock-dialog";
import { Skeleton } from "@/components/ui/skeleton";
import { claimBadge } from "@/lib/api/profile";
import { useCurrentUser } from "@/lib/hooks/use-auth";
import { useIsHydrated } from "@/lib/hooks/use-hydrated";
import { mn } from "@/lib/i18n/mn";
import { readSession, writeSession } from "@/lib/local-storage";
import { PATH_BADGE_KEY, PATH_NOTE, PATH_QUOTES, pickIndex } from "@/lib/motivation";
import { queryKeys } from "@/lib/query-keys";
import type { BadgeStatus } from "@/lib/types/api";

const LAST_QUOTE_KEY = "medleghub:footprints-quote";

/**
 * Нууц хуудас — сайтын хөлийн MedlegHub логоноос олдоно.
 *
 * Нээх бүрд нэг үг (өмнөхөөс өөр) харуулна — хуудсыг сэргээвэл шинэ үг.
 * Нэвтэрсэн хэрэглэгчид «Through Another's Path» тэмдэг олгоно. Санамсаргүй
 * сонголт нь сервер, client хоёрын HTML-ийг зөрүүлэхгүйн тулд hydration-ы
 * дараа л хийгдэнэ.
 */
export function FootprintsView() {
  const hydrated = useIsHydrated();

  return (
    <div className="container-page flex min-h-[70vh] items-center justify-center py-16">
      <div className="w-full max-w-xl">
        {hydrated ? <PathQuote /> : <Skeleton className="h-72 w-full rounded-2xl" />}
      </div>
    </div>
  );
}

/** Энэ табд сүүлд харуулсан үгийн дугаар. */
function previousQuote(): number | null {
  const raw = readSession(LAST_QUOTE_KEY, "");
  const value = Number.parseInt(raw, 10);
  return Number.isInteger(value) ? value : null;
}

function PathQuote() {
  const [index] = useState(() => pickIndex(PATH_QUOTES.length, previousQuote()));
  const quote = PATH_QUOTES[index] ?? PATH_QUOTES[0];
  const [unlocked, setUnlocked] = useState<BadgeStatus | null>(null);
  useClaimPathBadge(setUnlocked);

  // Дараагийн сэргээлт энэ үгийг давтахгүй.
  useEffect(() => writeSession(LAST_QUOTE_KEY, String(index)), [index]);

  const { isAuthenticated, isLoading } = useCurrentUser();

  return (
    <article className="bg-card relative overflow-hidden rounded-2xl border p-8 shadow-sm sm:p-10">
      <BadgeUnlockDialog badge={unlocked} onClose={() => setUnlocked(null)} />
      <div
        aria-hidden
        className="absolute -top-24 -right-24 size-64 rounded-full bg-[conic-gradient(#f9a8d4,#c4b5fd,#93c5fd,#6ee7b7,#fde68a,#fdba74,#f9a8d4)] opacity-15 blur-3xl"
      />
      <FootprintsIcon className="text-muted-foreground size-6" aria-hidden />
      <h1 className="sr-only">{mn.footprints.title}</h1>

      <blockquote
        lang="en"
        className="mt-6 space-y-1 text-xl leading-relaxed font-medium sm:text-2xl"
      >
        {quote.map((line, lineIndex) => (
          <p key={lineIndex}>{line}</p>
        ))}
      </blockquote>

      <div lang="mn" className="text-muted-foreground mt-8 space-y-3 border-t pt-6 text-sm italic">
        {PATH_NOTE.map((paragraph, paragraphIndex) => (
          <p key={paragraphIndex}>{paragraph}</p>
        ))}
      </div>

      <div className="mt-8 flex flex-wrap items-center justify-between gap-3 text-sm">
        {!isLoading && !isAuthenticated ? (
          <Link
            href={`/login?next=${encodeURIComponent("/footprints")}`}
            className="text-brand-link underline-offset-4 hover:underline"
          >
            {mn.footprints.loginHint}
          </Link>
        ) : (
          <span />
        )}
        <Link
          href="/dashboard"
          className="text-muted-foreground hover:text-foreground transition-colors"
        >
          {mn.footprints.back}
        </Link>
      </div>
    </article>
  );
}

/** Нэвтэрсэн бол тэмдэг олгоно — нэг удаа, дахин нээхэд юу ч болохгүй. */
function useClaimPathBadge(onUnlocked: (badge: BadgeStatus) => void) {
  const queryClient = useQueryClient();
  const { isAuthenticated } = useCurrentUser();
  const claimed = useRef(false);

  const claim = useMutation({
    mutationFn: () => claimBadge(PATH_BADGE_KEY),
    onSuccess: ({ new_badge }) => {
      if (!new_badge) return;
      void queryClient.invalidateQueries({ queryKey: queryKeys.me.profile });
      onUnlocked(new_badge);
    },
  });

  useEffect(() => {
    if (!isAuthenticated || claimed.current) return;
    claimed.current = true;
    claim.mutate();
  }, [isAuthenticated, claim]);
}
