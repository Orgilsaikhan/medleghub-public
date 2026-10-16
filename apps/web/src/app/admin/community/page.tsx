import { AdminPageHeader } from "@/components/admin/page-header";
import { SuspensionList } from "@/components/admin/suspension-list";
import { mn } from "@/lib/i18n/mn";

export default function AdminCommunityPage() {
  return (
    <>
      <AdminPageHeader title={mn.admin.community} description={mn.admin.communitySubtitle} />
      <SuspensionList />
    </>
  );
}
