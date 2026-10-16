import type { Metadata } from "next";

import { RequireAuth } from "@/components/auth/require-auth";
import { DashboardSkeleton } from "@/components/dashboard/dashboard-skeleton";
import { DashboardView } from "@/components/dashboard/dashboard-view";
import { mn } from "@/lib/i18n/mn";

export const metadata: Metadata = {
  title: mn.nav.dashboard,
};

export default function DashboardPage() {
  return (
    <div className="container-page py-10 lg:py-14">
      <RequireAuth fallback={<DashboardSkeleton />}>
        <DashboardView />
      </RequireAuth>
    </div>
  );
}
