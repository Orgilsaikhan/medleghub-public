import type { Metadata } from "next";
import { Suspense, cache } from "react";

import { PricingView } from "@/components/billing/pricing-view";
import { Skeleton } from "@/components/ui/skeleton";
import { getPlan } from "@/lib/api/billing";
import { formatMnt } from "@/lib/format";
import { mn } from "@/lib/i18n/mn";
import { pageMetadata } from "@/lib/seo";

/**
 * Нэвтрээгүй зочны үнэ — хүсэлт бүрт (админ үнийг өөрчилж болно). Ингэснээр
 * багцууд, үнэ HTML-д шууд орж, хайлтын систем JS-гүйгээр уншина.
 */
const loadPrice = cache(async (): Promise<number | null> => {
  try {
    return (await getPlan({ cache: "no-store" })).price_mnt;
  } catch {
    return null;
  }
});

export async function generateMetadata(): Promise<Metadata> {
  const price = await loadPrice();
  return pageMetadata({
    title: mn.seo.pricingTitle,
    description:
      price !== null
        ? mn.seo.pricingDescription(formatMnt(price))
        : mn.seo.pricingDescriptionFallback,
    path: "/pricing",
  });
}

export default async function PricingPage() {
  const price = await loadPrice();

  return (
    <div className="container-page py-10 lg:py-16">
      <div className="mx-auto max-w-2xl text-center">
        <h1 className="text-3xl font-bold tracking-tight text-balance sm:text-4xl">
          {mn.billing.title}
        </h1>
        <p className="text-muted-foreground mt-3 text-pretty">{mn.billing.subtitle}</p>
      </div>

      {/* PricingView нь `?next=`-ийг useSearchParams-аар уншдаг. */}
      <Suspense fallback={<Skeleton className="mx-auto mt-10 h-96 w-full max-w-4xl" />}>
        <PricingView initialPrice={price} />
      </Suspense>
    </div>
  );
}
