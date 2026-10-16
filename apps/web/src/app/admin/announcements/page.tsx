import { AdminPageHeader } from "@/components/admin/page-header";
import { Announcements } from "@/components/admin/announcements";
import { mn } from "@/lib/i18n/mn";

export default function AdminAnnouncementsPage() {
  return (
    <>
      <AdminPageHeader
        title={mn.admin.announcements}
        description={mn.admin.announcementsSubtitle}
      />
      <Announcements />
    </>
  );
}
