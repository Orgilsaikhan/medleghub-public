import { AdminPageHeader } from "@/components/admin/page-header";
import { PlanPriceForm } from "@/components/admin/plan-price-form";
import { UserPlanForm } from "@/components/admin/user-plan-form";
import { mn } from "@/lib/i18n/mn";

export default function AdminBillingPage() {
  return (
    <>
      <AdminPageHeader title={mn.admin.billing} description={mn.admin.billingSubtitle} />
      <div className="space-y-8">
        <PlanPriceForm />
        <PlanPriceForm plan="premium" />
        <PlanPriceForm plan="live_pass" />
        <UserPlanForm />
      </div>
    </>
  );
}
