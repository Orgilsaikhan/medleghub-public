import type { Metadata } from "next";

import { RequireAuth } from "@/components/auth/require-auth";
import { AdminShell } from "@/components/admin/admin-shell";
import { SiteFooter } from "@/components/layout/site-footer";
import { SiteHeader } from "@/components/layout/site-header";
import { Skeleton } from "@/components/ui/skeleton";
import { mn } from "@/lib/i18n/mn";

export const metadata: Metadata = {
  title: mn.admin.title,
  robots: { index: false, follow: false },
};

export default function AdminLayout({ children }: LayoutProps<"/admin">) {
  return (
    <>
      <SiteHeader />
      <main className="flex-1">
        {/* Эрхийг backend бас шалгана — энэ нь зөвхөн UI-ийн хамгаалалт. */}
        <RequireAuth adminOnly fallback={<AdminLoading />}>
          <AdminShell>{children}</AdminShell>
        </RequireAuth>
      </main>
      <SiteFooter />
    </>
  );
}

function AdminLoading() {
  return (
    <div className="container-wide space-y-4 py-10">
      <Skeleton className="h-9 w-48" />
      <Skeleton className="h-64 w-full" />
    </div>
  );
}
