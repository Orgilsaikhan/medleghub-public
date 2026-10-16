"use client";

import { useMutation } from "@tanstack/react-query";
import { CheckIcon, TicketIcon } from "lucide-react";
import Link from "next/link";
import { useId } from "react";
import { toast } from "sonner";

import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { startCheckout } from "@/lib/api/billing";
import { ApiError } from "@/lib/api/client";
import { rememberReturnPath } from "@/lib/billing";
import { formatMnt } from "@/lib/format";
import { useCurrentUser } from "@/lib/hooks/use-auth";
import { usePlan } from "@/lib/hooks/use-plan";
import { mn } from "@/lib/i18n/mn";
import type { PlanStatus } from "@/lib/types/api";
import { cn } from "@/lib/utils";

const t = mn.billing;

/**
 * Нэг удаагийн Live эрх — багц биш, нэг материал. `/pricing` ба `/live` дээр,
 * нэвтрээгүй зочинд ч харагдана; авахын тулд нэвтэрнэ эсвэл бүртгүүлнэ (эрх
 * бүртгэлд холбогдоно). Үнэ, нөхцөлийн тоог сервер өгнө (`GET /billing/plan`).
 *
 * Live бүгдэд нээгдээгүй (`live_pass_available` = false) бол юу ч харуулахгүй.
 */
export function LivePassOffer({
  returnTo,
  className,
}: {
  /** Нэвтэрсэн/бүртгүүлсний дараа буцах хуудас. */
  returnTo: string;
  className?: string;
}) {
  const titleId = useId();
  const { data: plan } = usePlan();
  if (!plan?.live_pass_available) return null;

  const price = formatMnt(plan.live_pass_price_mnt);
  return (
    <section
      aria-labelledby={titleId}
      className={cn(
        "bg-card grid gap-6 rounded-xl border p-6 sm:p-8 md:grid-cols-[minmax(0,1fr)_18rem] md:items-center",
        className,
      )}
    >
      <div className="min-w-0">
        <div className="flex items-center gap-2.5">
          <span
            aria-hidden
            className="bg-primary/10 text-primary grid size-9 shrink-0 place-items-center rounded-lg"
          >
            <TicketIcon className="size-5" />
          </span>
          <h2 id={titleId} className="text-lg font-semibold">
            {t.livePassName}
          </h2>
        </div>
        <p className="text-muted-foreground mt-2 text-sm text-pretty">{t.livePassLead}</p>
        <ul className="mt-4 grid gap-2.5 text-sm sm:grid-cols-2">
          {t
            .livePassPerks(plan.live_pass_access_days, plan.live_pass_upgrade_days, price)
            .map((perk) => (
              <li key={perk} className="flex items-start gap-2.5">
                <CheckIcon className="text-success mt-0.5 size-4 shrink-0" aria-hidden />
                {perk}
              </li>
            ))}
        </ul>
      </div>

      <div className="space-y-4">
        <p className="flex items-baseline gap-1.5">
          <span className="text-4xl font-bold tracking-tight">{price}</span>
          <span className="text-muted-foreground text-sm">{t.livePassUnit}</span>
        </p>
        <LivePassAction plan={plan} returnTo={returnTo} />
      </div>
    </section>
  );
}

function LivePassAction({ plan, returnTo }: { plan: PlanStatus; returnTo: string }) {
  const { isAuthenticated, isLoading } = useCurrentUser();

  if (isLoading) {
    return <Skeleton className="h-10 w-full rounded-md" />;
  }

  if (!isAuthenticated) {
    const next = encodeURIComponent(returnTo);
    return (
      <div className="space-y-3">
        <p className="text-muted-foreground text-xs text-pretty">{t.livePassAuthNote}</p>
        <div className="grid gap-2 sm:grid-cols-2 md:grid-cols-1 lg:grid-cols-2">
          <Button asChild>
            <Link href={`/login?next=${next}`}>{t.livePassLogin}</Link>
          </Button>
          <Button asChild variant="outline">
            <Link href={`/register?next=${next}`}>{t.livePassRegister}</Link>
          </Button>
        </div>
      </div>
    );
  }

  if (plan.has_plan) {
    return <p className="text-muted-foreground text-sm">{t.livePassIncluded}</p>;
  }

  if (plan.has_unused_live_pass) {
    return (
      <div className="space-y-3">
        <p className="text-sm font-medium">{t.livePassUnused}</p>
        <Button asChild variant="outline" className="w-full">
          <Link href="/live">{t.livePassUse}</Link>
        </Button>
      </div>
    );
  }

  return <LivePassBuyButton plan={plan} className="w-full" />;
}

/**
 * Нэг удаагийн эрхийн нэхэмжлэх үүсгэж Wire-ийн төлбөрийн хуудас руу шилжүүлнэ.
 * Багцгүй, ашиглаагүй эрхгүй, нэвтэрсэн хэрэглэгчид л харуулна (сервер ч шалгана).
 */
export function LivePassBuyButton({
  plan,
  label,
  variant = "default",
  className,
}: {
  plan: PlanStatus;
  label?: string;
  variant?: "default" | "outline";
  className?: string;
}) {
  const checkout = useMutation({
    mutationFn: () => startCheckout(1, null, "live_pass"),
    onSuccess: ({ checkout_url }) => {
      // Баримтын хуудас эрхэд «Live руу очих»-ыг санал болгоно — хуучин хичээлийн хаяг үлдээхгүй.
      rememberReturnPath(null);
      window.location.assign(checkout_url);
    },
    onError: (error) => {
      toast.error(error instanceof ApiError ? error.message : mn.common.somethingWrong);
    },
  });
  // Шилжих хүртэл идэвхгүй — давхар нэхэмжлэх үүсэхгүй.
  const busy = checkout.isPending || checkout.isSuccess;

  return (
    <Button
      size="lg"
      variant={variant}
      className={className}
      disabled={busy}
      onClick={() => checkout.mutate()}
    >
      {busy ? t.redirecting : (label ?? t.livePassBuy(formatMnt(plan.live_pass_price_mnt)))}
    </Button>
  );
}
