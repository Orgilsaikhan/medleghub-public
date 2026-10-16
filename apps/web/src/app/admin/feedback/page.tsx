import { AdminFeedbackList } from "@/components/admin/feedback-list";
import { AdminPageHeader } from "@/components/admin/page-header";
import { mn } from "@/lib/i18n/mn";

export default function AdminFeedbackPage() {
  return (
    <>
      <AdminPageHeader title={mn.admin.feedback} description={mn.admin.feedbackSubtitle} />
      <AdminFeedbackList />
    </>
  );
}
