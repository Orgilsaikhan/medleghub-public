"use client";

import { useQuery } from "@tanstack/react-query";
import { EyeOffIcon, UserXIcon } from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect } from "react";

import { EmptyState, ErrorState } from "@/components/common/states";
import { UserAvatar } from "@/components/common/user-avatar";
import { CategoryLogo } from "@/components/courses/category-logo";
import { ProgressBar } from "@/components/courses/progress-bar";
import { BadgeSection, ProfileName, ProfileStatsGrid } from "@/components/profile/profile-view";
import { ProfileSkeleton } from "@/components/profile/profile-skeleton";
import { ApiError } from "@/lib/api/client";
import { getPublicProfile } from "@/lib/api/community";
import { formatDate } from "@/lib/format";
import { useCurrentUser } from "@/lib/hooks/use-auth";
import { mn } from "@/lib/i18n/mn";
import { queryKeys } from "@/lib/query-keys";

/**
 * Өөр суралцагчийн профайл — нэр, зураг, статистик, сургалтын ахиц, тэмдгүүд.
 *
 * Зөвхөн унших. Имэйл зэрэг хувийн мэдээллийг API өөрөө буцаадаггүй.
 */
export function PublicProfileView({ userId }: { userId: string }) {
  const router = useRouter();
  const { user: me } = useCurrentUser();
  const isMe = me?.id === userId;

  // Өөрийн профайл — засах товчтой үндсэн хуудас руу.
  useEffect(() => {
    if (isMe) router.replace("/profile");
  }, [isMe, router]);

  const query = useQuery({
    queryKey: queryKeys.users.profile(userId),
    queryFn: () => getPublicProfile(userId),
    enabled: !isMe,
    staleTime: 30_000,
    retry: (count, error) =>
      !(error instanceof ApiError && (error.isNotFound || error.isForbidden)) && count < 2,
  });

  if (isMe || query.isPending) return <ProfileSkeleton />;
  if (query.isError) {
    if (query.error instanceof ApiError && query.error.code === "PROFILE_HIDDEN") {
      return (
        <EmptyState
          icon={EyeOffIcon}
          title={mn.community.hidden}
          description={mn.community.hiddenBody}
        />
      );
    }
    if (query.error instanceof ApiError && query.error.isNotFound) {
      return (
        <EmptyState
          icon={UserXIcon}
          title={mn.community.notFound}
          description={mn.community.notFoundBody}
        />
      );
    }
    return <ErrorState onRetry={() => void query.refetch()} />;
  }

  const { user, stats, badges, courses } = query.data;

  return (
    <div className="space-y-10">
      <section className="flex items-center gap-4">
        <UserAvatar user={user} className="size-16" fallbackClassName="text-lg" />
        <div className="min-w-0 flex-1">
          <ProfileName name={user.name} badges={badges} />
          <p className="text-muted-foreground mt-1 text-xs">
            {mn.profile.memberSince(formatDate(user.created_at))}
          </p>
        </div>
      </section>

      <ProfileStatsGrid stats={stats} />

      <section aria-labelledby="courses-title">
        <h2 id="courses-title" className="text-xl font-semibold tracking-tight">
          {mn.community.coursesTitle}
        </h2>

        {courses.length === 0 ? (
          <p className="text-muted-foreground mt-4 text-sm">{mn.community.coursesEmpty}</p>
        ) : (
          <ul className="mt-4 grid gap-3 sm:grid-cols-2 sm:gap-4">
            {courses.map((course) => (
              <li key={course.slug}>
                <Link
                  href={`/courses/${course.slug}`}
                  className="bg-card hover:border-primary/40 flex items-center gap-4 rounded-xl border p-4 transition-colors"
                >
                  <CategoryLogo category={course.category} className="size-10 shrink-0" />
                  <div className="min-w-0 flex-1">
                    <p className="truncate font-medium">{course.title}</p>
                    <ProgressBar progress={course.progress} label={course.title} className="mt-2" />
                  </div>
                </Link>
              </li>
            ))}
          </ul>
        )}
      </section>

      <BadgeSection stats={stats} badges={badges} />
    </div>
  );
}
