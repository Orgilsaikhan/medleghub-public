"use client";

import { LockIcon } from "lucide-react";
import Link from "next/link";

import { Button } from "@/components/ui/button";
import { formatMnt } from "@/lib/format";
import { usePlan } from "@/lib/hooks/use-plan";
import { mn } from "@/lib/i18n/mn";

interface LessonPaywallProps {
  title: string;
  description: string;
  /** Төлбөрийн дараа буцах хаяг — энэ хичээл. */
  returnTo: string;
}

/**
 * Түгжигдсэн хичээлийн агуулгын оронд.
 *
 * Сервер нь агуулга, код, дасгалыг огт илгээгээгүй — энэ нь зөвхөн UX.
 * Хөтөлбөр, өмнөх/дараагийн холбоос хэвээр тул сурагч үнэгүй хэсэг рүүгээ
 * буцаж чадна.
 */
export function LessonPaywall({ title, description, returnTo }: LessonPaywallProps) {
  const { data: plan } = usePlan();

  return (
    <div
      tabIndex={0}
      role="region"
      aria-label={mn.learn.lessonContent}
      className="min-h-0 flex-1 overflow-y-auto"
    >
      <div className="mx-auto flex max-w-lg flex-col items-center px-6 py-16 text-center">
        <span className="bg-primary/10 text-primary grid size-12 place-items-center rounded-full">
          <LockIcon className="size-5" aria-hidden />
        </span>

        <h1 className="mt-6 text-xl font-bold tracking-tight text-balance sm:text-2xl">{title}</h1>
        {description && <p className="text-muted-foreground mt-1.5 text-sm">{description}</p>}

        <div className="bg-card mt-8 w-full rounded-xl border p-6">
          <h2 className="font-semibold">{mn.learn.paywall.title}</h2>
          <p className="text-muted-foreground mt-2 text-sm leading-relaxed">
            {mn.learn.paywall.body}
          </p>
          {plan && (
            <p className="mt-4 text-2xl font-bold tracking-tight">
              {mn.learn.paywall.price(formatMnt(plan.price_mnt))}
            </p>
          )}
          <Button asChild size="lg" className="mt-5 w-full sm:w-auto">
            <Link href={`/pricing?next=${encodeURIComponent(returnTo)}`}>
              {mn.learn.paywall.cta}
            </Link>
          </Button>
        </div>
      </div>
    </div>
  );
}
