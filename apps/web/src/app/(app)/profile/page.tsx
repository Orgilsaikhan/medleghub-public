import type { Metadata } from "next";

import { RequireAuth } from "@/components/auth/require-auth";
import { ProfileSkeleton } from "@/components/profile/profile-skeleton";
import { ProfileView } from "@/components/profile/profile-view";
import { mn } from "@/lib/i18n/mn";

export const metadata: Metadata = {
  title: mn.nav.profile,
};

export default function ProfilePage() {
  return (
    <div className="container-page py-10 lg:py-14">
      <RequireAuth fallback={<ProfileSkeleton withPlan />}>
        <ProfileView />
      </RequireAuth>
    </div>
  );
}
