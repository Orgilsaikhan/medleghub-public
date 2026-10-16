import type { Metadata } from "next";

import { RequireAuth } from "@/components/auth/require-auth";
import { ProfileSkeleton } from "@/components/profile/profile-skeleton";
import { PublicProfileView } from "@/components/profile/public-profile-view";
import { mn } from "@/lib/i18n/mn";

export const metadata: Metadata = {
  title: mn.nav.profile,
  // Суралцагчийн профайл хайлтын системд орох ёсгүй.
  robots: { index: false, follow: false },
};

export default async function UserProfilePage({ params }: PageProps<"/users/[id]">) {
  const { id } = await params;
  return (
    <div className="container-page py-10 lg:py-14">
      <RequireAuth fallback={<ProfileSkeleton />}>
        <PublicProfileView userId={id} />
      </RequireAuth>
    </div>
  );
}
