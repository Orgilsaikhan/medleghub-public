import { LiveGrantForm, LiveModelsCard, LiveOverviewCard } from "@/components/admin/live-admin";
import { AdminPageHeader } from "@/components/admin/page-header";
import { mn } from "@/lib/i18n/mn";

export default function AdminLivePage() {
  return (
    <>
      <AdminPageHeader title={mn.admin.liveTitle} description={mn.admin.liveSubtitle} />
      <div className="space-y-8">
        <LiveOverviewCard />
        <LiveModelsCard />
        <LiveGrantForm />
      </div>
    </>
  );
}
