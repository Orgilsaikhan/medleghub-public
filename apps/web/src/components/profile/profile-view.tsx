"use client";

import { useQuery } from "@tanstack/react-query";
import {
  AwardIcon,
  CheckCircle2Icon,
  CodeIcon,
  CrownIcon,
  EyeOffIcon,
  ListChecksIcon,
  SettingsIcon,
} from "lucide-react";
import Link from "next/link";
import { useEffect } from "react";

import { ErrorState } from "@/components/common/states";
import { UserAvatar } from "@/components/common/user-avatar";
import { Stat } from "@/components/dashboard/dashboard-summary";
import { BadgeCard, revealBadgeCard } from "@/components/profile/badge-card";
import { BadgeShowcase, showcaseBadges } from "@/components/profile/badge-showcase";
import { ProfileSkeleton } from "@/components/profile/profile-skeleton";
import { ReferralCard } from "@/components/profile/referral-card";
import { ShowcaseEditor } from "@/components/profile/showcase-editor";
import { Button } from "@/components/ui/button";
import { getProfile } from "@/lib/api/profile";
import { daysLeft, formatDate } from "@/lib/format";
import { mn } from "@/lib/i18n/mn";
import { queryKeys } from "@/lib/query-keys";
import type { BadgeStatus, ProfileStats, User } from "@/lib/types/api";

/**
 * Хэрэглэгчийн профайл — мэдээлэл, статистик, тэмдгүүд.
 *
 * Бүгд нэг `/me/profile` дуудлагаас ирнэ. Сервер тэр үед тэмдгийн нөхцөлийг
 * шалгаж, хангасан ч хараахан олгоогүй тэмдгийг олгодог.
 */
export function ProfileView() {
  const query = useQuery({
    queryKey: queryKeys.me.profile,
    queryFn: getProfile,
    staleTime: 30_000,
  });

  if (query.isPending) return <ProfileSkeleton withPlan />;
  if (query.isError) return <ErrorState onRetry={() => void query.refetch()} />;

  const { user, stats, badges } = query.data;

  return (
    <div className="space-y-10">
      <section className="flex items-start gap-4 sm:items-center">
        <UserAvatar user={user} className="size-16" fallbackClassName="text-lg" />
        <div className="min-w-0 flex-1">
          <ProfileName name={user.name} badges={badges} editable />
          <p className="text-muted-foreground truncate text-sm">{user.email}</p>
          <p className="text-muted-foreground mt-1 text-xs">
            {mn.profile.memberSince(formatDate(user.created_at))}
          </p>
          {user.profile_hidden && (
            <p className="text-muted-foreground mt-1 flex items-center gap-1.5 text-xs">
              <EyeOffIcon className="size-3.5" aria-hidden />
              {mn.community.ownHidden}{" "}
              <Link href="/settings" className="text-brand-link underline-offset-4 hover:underline">
                {mn.community.ownHiddenLink}
              </Link>
            </p>
          )}
        </div>
        {/* Утсан дээр зөвхөн дүрс — нэр ба онцлох амжилтуудад зай үлдээнэ. */}
        <Button asChild variant="outline" size="sm" className="max-sm:size-8 max-sm:px-0">
          <Link href="/settings">
            <SettingsIcon className="size-4" aria-hidden />
            <span className="max-sm:sr-only">{mn.nav.settings}</span>
          </Link>
        </Button>
      </section>

      <PlanSummary user={user} />
      {/* Админ үргэлж багцтай — урилгын шагнал түүнд утгагүй. */}
      {user.role !== "admin" && <ReferralCard />}
      <ProfileStatsGrid stats={stats} />
      <BadgeSection stats={stats} badges={badges} />
    </div>
  );
}

/**
 * Багц ба хэдэн хоног үлдсэн. Админ хугацаагүйгээр бүх хичээлийг үздэг тул
 * дуусах хугацаагүй бол харуулахгүй.
 */
function PlanSummary({ user }: { user: User }) {
  const expiresAt = user.plan_expires_at;
  const days = expiresAt ? daysLeft(expiresAt) : 0;
  if (user.role === "admin" && days === 0) return null;

  const active = days > 0;
  let detail: string = mn.profile.planFreeHint;
  if (expiresAt) {
    detail = active
      ? mn.profile.planUntil(formatDate(expiresAt))
      : mn.profile.planExpired(formatDate(expiresAt));
  }

  return (
    <section
      aria-labelledby="plan-title"
      className="bg-card flex flex-wrap items-center justify-between gap-4 rounded-xl border p-4 sm:p-5"
    >
      <div className="flex min-w-0 items-center gap-3">
        <span className="bg-muted text-brand-link grid size-10 shrink-0 place-items-center rounded-lg">
          <CrownIcon className="size-5" aria-hidden />
        </span>
        <div className="min-w-0">
          <h2 id="plan-title" className="font-semibold">
            {active ? mn.profile.planStandard : mn.profile.planFree}
          </h2>
          <p className="text-muted-foreground text-sm">{detail}</p>
        </div>
      </div>

      <div className="flex items-center gap-4">
        {active && (
          <p className="flex items-baseline gap-1.5">
            <span className="text-2xl font-bold tabular-nums">{days}</span>
            <span className="text-muted-foreground text-sm">{mn.profile.planDaysLeft}</span>
          </p>
        )}
        <Button asChild size="sm" variant={active ? "outline" : "default"}>
          <Link href="/pricing">{active ? mn.profile.planExtend : mn.profile.planBuy}</Link>
        </Button>
      </div>
    </section>
  );
}

/**
 * Нэр ба түүний хажууд хэрэглэгчийн сонгосон онцлох амжилтууд. Зай хүрэхгүй
 * бол (утсан дээр) дүрсүүд нэрийн доор шилжиж, урт нэр хоёр мөрт багтана.
 *
 * `editable` — өөрийн профайл: сонгох/засах товчтой.
 */
export function ProfileName({
  name,
  badges,
  editable = false,
}: {
  name: string;
  badges: BadgeStatus[];
  editable?: boolean;
}) {
  const canEdit = editable && badges.some((badge) => badge.earned);
  const hasShowcase = showcaseBadges(badges).length > 0;

  return (
    <div className="flex flex-wrap items-center gap-x-3 gap-y-1.5">
      <h1 className="line-clamp-2 max-w-full min-w-0 text-2xl font-bold tracking-tight break-words sm:line-clamp-1 sm:text-3xl">
        {name}
      </h1>
      {(hasShowcase || canEdit) && (
        <div className="flex flex-wrap items-center gap-1.5">
          <BadgeShowcase badges={badges} />
          {canEdit && <ShowcaseEditor badges={badges} />}
        </div>
      )}
    </div>
  );
}

/** Дууссан хичээл, дасгал, сургалт, тэмдгийн тоо. */
export function ProfileStatsGrid({ stats }: { stats: ProfileStats }) {
  return (
    <div className="grid grid-cols-2 gap-3 sm:grid-cols-4 sm:gap-4">
      <Stat icon={ListChecksIcon} value={stats.completed_lessons} label={mn.profile.statLessons} />
      <Stat icon={CodeIcon} value={stats.completed_exercises} label={mn.profile.statExercises} />
      <Stat
        icon={CheckCircle2Icon}
        value={stats.completed_courses}
        label={mn.profile.statCourses}
      />
      <Stat
        icon={AwardIcon}
        value={`${stats.earned_badges}/${stats.total_badges}`}
        label={mn.profile.statBadges}
      />
    </div>
  );
}

export function BadgeSection({ stats, badges }: { stats: ProfileStats; badges: BadgeStatus[] }) {
  // Шинэ цонхонд нээсэн `…#badge-<key>` холбоос: картууд өгөгдөл ирсний дараа
  // зурагддаг тул хөтөч өөрөө гүйлгэж амжихгүй.
  useEffect(() => {
    const hash = decodeURIComponent(window.location.hash.slice(1));
    if (hash.startsWith("badge-")) revealBadgeCard(hash.slice("badge-".length));
  }, []);

  return (
    <section aria-labelledby="badges-title">
      <div className="flex items-baseline justify-between gap-4">
        <h2 id="badges-title" className="text-xl font-semibold tracking-tight">
          {mn.profile.badgesTitle}
        </h2>
        <span className="text-muted-foreground text-sm tabular-nums">
          {mn.profile.badgesCount(stats.earned_badges, stats.total_badges)}
        </span>
      </div>

      <ul className="mt-4 grid grid-cols-2 gap-3 sm:grid-cols-3 sm:gap-4 lg:grid-cols-4 xl:grid-cols-5">
        {badges.map((badge) => (
          <BadgeCard key={badge.key} badge={badge} />
        ))}
      </ul>
    </section>
  );
}
