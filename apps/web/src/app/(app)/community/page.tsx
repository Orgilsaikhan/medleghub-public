import type { Metadata } from "next";
import { Suspense } from "react";

import { RequireAuth } from "@/components/auth/require-auth";
import { CommunityActions, CommunityGate } from "@/components/community/community-gate";
import { CommunityFeed, CommunityFeedSkeleton } from "@/components/community/community-feed";
import { mn } from "@/lib/i18n/mn";

export const metadata: Metadata = {
  title: mn.community.title,
};

export default function CommunityPage() {
  return (
    <div className="container-page py-10 lg:py-14">
      <div className="mx-auto max-w-3xl">
        <header className="flex flex-wrap items-end justify-between gap-4">
          <div>
            <h1 className="text-3xl font-bold tracking-tight sm:text-4xl">{mn.community.title}</h1>
            <p className="text-muted-foreground mt-2">{mn.community.subtitle}</p>
          </div>
          <CommunityActions />
        </header>

        <div className="mt-8">
          <RequireAuth fallback={<CommunityFeedSkeleton />}>
            {/* Түдгэлзсэн бол мэдэгдэл; эхний удаа бол дүрмийн цонх. */}
            <CommunityGate />
            {/* Шүүлтүүр URL-аас уншдаг (`useSearchParams`). */}
            <Suspense fallback={<CommunityFeedSkeleton />}>
              <CommunityFeed />
            </Suspense>
          </RequireAuth>
        </div>
      </div>
    </div>
  );
}
