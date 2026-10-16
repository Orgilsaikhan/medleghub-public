import { AdminPageHeader } from "@/components/admin/page-header";
import { PromoCodes } from "@/components/admin/promo-codes";
import { mn } from "@/lib/i18n/mn";

export default function AdminPromoPage() {
  return (
    <>
      <AdminPageHeader title={mn.admin.promo} description={mn.admin.promoSubtitle} />
      <PromoCodes />
    </>
  );
}
