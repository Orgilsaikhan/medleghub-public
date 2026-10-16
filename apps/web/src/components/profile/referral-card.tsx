"use client";

import { useQuery } from "@tanstack/react-query";
import { CheckIcon, CopyIcon, GiftIcon, Share2Icon } from "lucide-react";
import { useId, useState } from "react";
import { toast } from "sonner";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Skeleton } from "@/components/ui/skeleton";
import { getReferral } from "@/lib/api/account";
import { useIsHydrated } from "@/lib/hooks/use-hydrated";
import { mn } from "@/lib/i18n/mn";
import { queryKeys } from "@/lib/query-keys";
import { SITE_URL } from "@/lib/seo";

/**
 * Найзаа урих: урилгын холбоос, дүрэм, олсон шагнал. Урьсан найзуудаас 3 нь
 * багц авах бүрд 1 сар үнэгүй; кодоор бүртгүүлсэн найз өөрөө 10% хөнгөлөлт авна.
 * Найзуудын нэр, төлбөрийг харуулахгүй — сервер зөвхөн нийт тоо буцаана.
 */
export function ReferralCard() {
  const linkId = useId();
  const query = useQuery({
    queryKey: queryKeys.me.referral,
    queryFn: getReferral,
    staleTime: 60_000,
  });
  const hydrated = useIsHydrated();
  // Хөгжүүлэлтэд localhost, production-д medleghub.com — хуулсан холбоос ажиллана.
  const origin = hydrated ? window.location.origin : SITE_URL;
  const canShare = hydrated && typeof navigator.share === "function";
  const [copied, setCopied] = useState(false);

  if (query.isPending) return <Skeleton className="h-72 w-full rounded-xl" />;
  // Урилга нь профайлын гол зүйл биш — алдаа гарвал картыг л харуулахгүй.
  if (query.isError) return null;

  const referral = query.data;
  const link = `${origin}/register?ref=${encodeURIComponent(referral.code)}`;
  const t = mn.profile.referral;

  const copy = async () => {
    try {
      await navigator.clipboard.writeText(link);
      setCopied(true);
      setTimeout(() => setCopied(false), 1500);
    } catch {
      toast.error(t.copyFailed);
    }
  };

  const share = async () => {
    try {
      await navigator.share({ title: mn.brand.name, text: t.shareText, url: link });
    } catch {
      // Хэрэглэгч цуцалсан — юу ч хийхгүй.
    }
  };

  return (
    <section
      aria-labelledby="referral-title"
      className="bg-card space-y-5 rounded-xl border p-4 sm:p-5"
    >
      <div className="flex items-start gap-3">
        <span className="bg-muted text-brand-link grid size-10 shrink-0 place-items-center rounded-lg">
          <GiftIcon className="size-5" aria-hidden />
        </span>
        <div className="min-w-0 space-y-1">
          <h2 id="referral-title" className="font-semibold">
            {t.title}
          </h2>
          <p className="text-muted-foreground text-sm">
            {t.rewardRule(referral.friends_per_reward, referral.reward_months)}
          </p>
          <p className="text-muted-foreground text-sm">
            {t.friendRule(referral.friend_percent_off)}
          </p>
        </div>
      </div>

      <div className="space-y-2">
        <p className="text-muted-foreground text-xs">
          {t.code}:{" "}
          <span className="text-foreground font-mono text-sm font-semibold tracking-wider">
            {referral.code}
          </span>
        </p>
        <Label htmlFor={linkId}>{t.link}</Label>
        <div className="flex flex-col gap-2 sm:flex-row">
          <Input
            id={linkId}
            value={link}
            readOnly
            onFocus={(event) => event.currentTarget.select()}
            className="font-mono text-xs sm:text-sm"
          />
          <div className="flex gap-2">
            <Button type="button" variant="outline" onClick={() => void copy()}>
              {copied ? (
                <CheckIcon className="size-4" aria-hidden />
              ) : (
                <CopyIcon className="size-4" aria-hidden />
              )}
              <span aria-live="polite">{copied ? t.copied : t.copyLink}</span>
            </Button>
            {canShare && (
              <Button type="button" variant="outline" onClick={() => void share()}>
                <Share2Icon className="size-4" aria-hidden />
                {t.share}
              </Button>
            )}
          </div>
        </div>
      </div>

      {/* Утасны өргөнд ч нэг мөрөнд багтана — тоо дээр, шошго доор. */}
      <dl className="grid grid-cols-3 divide-x rounded-lg border">
        {(
          [
            [t.friends, referral.friends],
            [t.payingFriends, referral.paying_friends],
            [t.monthsEarned, referral.months_earned],
          ] as const
        ).map(([label, value]) => (
          <div key={label} className="flex flex-col-reverse gap-1 px-2 py-3 text-center sm:px-4">
            <dt className="text-muted-foreground text-xs leading-snug sm:text-sm">{label}</dt>
            <dd className="text-xl font-bold tabular-nums sm:text-2xl">{value}</dd>
          </div>
        ))}
      </dl>
      <p className="text-muted-foreground -mt-3 text-xs">
        {t.nextReward(referral.friends_to_next_reward, referral.reward_months)}
      </p>
    </section>
  );
}
