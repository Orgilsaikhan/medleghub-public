import type { Metadata } from "next";

import { RequireAuth } from "@/components/auth/require-auth";
import { SettingsView } from "@/components/settings/settings-view";
import { Skeleton } from "@/components/ui/skeleton";
import { mn } from "@/lib/i18n/mn";

export const metadata: Metadata = {
  title: mn.settings.title,
};

export default function SettingsPage() {
  return (
    <div className="container-page py-10 lg:py-14">
      <RequireAuth fallback={<Skeleton className="h-96 w-full max-w-2xl" />}>
        <SettingsView />
      </RequireAuth>
    </div>
  );
}
