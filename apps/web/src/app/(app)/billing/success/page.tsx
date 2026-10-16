import type { Metadata } from "next";
import { Suspense } from "react";

import { RequireAuth } from "@/components/auth/require-auth";
import { PaymentSuccess } from "@/components/billing/payment-success";
import { Skeleton } from "@/components/ui/skeleton";
import { mn } from "@/lib/i18n/mn";

export const metadata: Metadata = {
  title: mn.billing.receipt.pageTitle,
};

/**
 * Төлбөрийн (Wire-ийн `success_url`) эсвэл үнэгүй сарын промо кодын дараах
 * хуудас — баримт хэвлэгч.
 */
export default function PaymentSuccessPage() {
  const fallback = <Skeleton className="mx-auto h-96 w-full max-w-sm rounded-3xl" />;
  return (
    <div className="container-page py-12 lg:py-16">
      <RequireAuth fallback={fallback}>
        <Suspense fallback={fallback}>
          <PaymentSuccess />
        </Suspense>
      </RequireAuth>
    </div>
  );
}
