"use client";

import {
  ArrowRightIcon,
  CalendarClockIcon,
  CrownIcon,
  SparklesIcon,
  TicketIcon,
  TriangleAlertIcon,
} from "lucide-react";
import Link from "next/link";
import { useId, type ReactNode } from "react";

import { LivePassBuyButton } from "@/components/billing/live-pass-offer";
import { EYEBROW } from "@/components/live/live-ui";
import { Skeleton } from "@/components/ui/skeleton";
import { formatDate, formatMnt } from "@/lib/format";
import { useLiveMaterials } from "@/lib/hooks/use-live";
import { usePlan } from "@/lib/hooks/use-plan";
import { mn } from "@/lib/i18n/mn";
import type { PlanStatus } from "@/lib/types/api";
import type { LiveConfig, LivePassInfo, LiveUsage } from "@/lib/types/live";
import { cn } from "@/lib/utils";

const t = mn.live;

/** Хэрэглээ хэр дөхсөн бэ — зураасны өнгө, анхааруулга үүнээс. */
type Level = "ok" | "high" | "critical" | "out";

function levelFor(percent: number): Level {
  if (percent >= 100) return "out";
  if (percent >= 90) return "critical";
  if (percent >= 75) return "high";
  return "ok";
}

const LEVELS: Record<Level, { fill: string; text: string }> = {
  ok: { fill: "from-primary to-amber-300", text: "" },
  high: { fill: "from-orange-500 to-amber-400", text: "text-orange-700 dark:text-orange-400" },
  critical: { fill: "from-destructive to-orange-500", text: "text-destructive" },
  out: { fill: "from-destructive to-destructive", text: "text-destructive" },
};

/** Анхааруулга: багцад сарын, нэг удаагийн эрхэд материалын хэрэглээ. */
const MONTH_MESSAGES: Record<Level, string | null> = {
  ok: null,
  high: t.usageHigh,
  critical: t.usageCritical,
  out: t.usageOut,
};
const PASS_MESSAGES: Record<Level, string | null> = {
  ok: null,
  high: t.passUsageHigh,
  critical: t.passUsageCritical,
  out: t.passUsageOut,
};

/**
 * Багц ба энэ сарын AI хэрэглээ. Материалын тоог харуулахгүй (эзэмшигчийн
 * шийдвэр) — зөвхөн хязгаараас хэдэн хувь (`ai_used_percent`) ашигласан.
 * Standard хэрэглэгчид Premium худалдаалагдаж байвал түүнийг санал болгоно.
 * Нэг удаагийн эрхэд: ашиглаагүй эрх, эсвэл эрхээр нээсэн материал тус бүрийн AI
 * хэрэглээ ба хэзээ хүртэл нээлттэй.
 */
export function UsagePanel({ config }: { config: LiveConfig }) {
  const tier = config.tier ?? "free";
  const { data: plan } = usePlan();
  if (tier === "pass" && config.passes) {
    return <PassPanel config={config} passes={config.passes} plan={plan} />;
  }
  const premiumMultiplier =
    tier === "standard" && plan?.premium_available && !plan.has_premium
      ? plan.premium_usage_multiplier
      : null;

  return (
    <section
      aria-labelledby="live-usage-title"
      className="from-primary/10 bg-card overflow-hidden rounded-3xl border bg-gradient-to-br via-transparent to-transparent shadow-xs"
    >
      <h2 id="live-usage-title" className="sr-only">
        {t.usageLabel}
      </h2>
      <div className="grid md:grid-cols-[minmax(0,20rem)_minmax(0,1fr)]">
        <div className="flex items-center gap-4 p-5 sm:p-6">
          <span
            aria-hidden
            className="bg-primary text-primary-foreground shadow-primary/25 grid size-12 shrink-0 place-items-center rounded-2xl shadow-lg"
          >
            <CrownIcon className="size-6" />
          </span>
          <div className="min-w-0">
            <p className={EYEBROW}>{t.planLabel}</p>
            <p className="mt-0.5 text-lg font-semibold tracking-tight">
              {t.tierPlan(t.tiers[tier])}
            </p>
            {config.tier_expires_at && (
              <p className="text-muted-foreground text-sm">
                {t.tierUntilDate(formatDate(config.tier_expires_at))}
              </p>
            )}
          </div>
        </div>

        {config.usage && <AiUsage usage={config.usage} premiumMultiplier={premiumMultiplier} />}
      </div>
    </section>
  );
}

function AiUsage({
  usage,
  premiumMultiplier,
}: {
  usage: LiveUsage;
  premiumMultiplier: number | null;
}) {
  return (
    <UsageMeter
      percent={usage.ai_used_percent}
      scope={t.usageThisMonth}
      hint={t.usageAiHint}
      messages={MONTH_MESSAGES}
      when={t.usageAiResets(formatDate(usage.ai_period_resets_at))}
      className="border-t md:border-t-0 md:border-l"
    >
      {premiumMultiplier !== null && (
        <PanelLink href="/pricing">{t.usagePremium(premiumMultiplier)}</PanelLink>
      )}
    </UsageMeter>
  );
}

/** AI хэрэглээний хэмжүүр — хувь, өнгө, анхааруулга, доор нь хугацаа ба холбоос. */
function UsageMeter({
  percent: raw,
  scope,
  hint,
  messages,
  when,
  className,
  children,
}: {
  percent: number;
  /** «энэ сар» эсвэл материалын нэр. */
  scope: string;
  hint: string;
  messages: Record<Level, string | null>;
  when: string;
  className?: string;
  children?: ReactNode;
}) {
  const labelId = useId();
  const hintId = useId();
  const percent = Math.max(0, Math.min(100, Math.round(raw)));
  const key = levelFor(percent);
  const level = LEVELS[key];
  const message = messages[key];

  return (
    <div className={cn("p-5 sm:p-6", className)}>
      <div className="flex items-start justify-between gap-4">
        <div className="min-w-0">
          <p id={labelId} className="flex flex-wrap items-center gap-x-1.5 font-semibold">
            <SparklesIcon className="text-brand-link size-4" aria-hidden />
            {t.usageAiTitle}
            <span className="text-muted-foreground min-w-0 truncate text-sm font-normal">
              · {scope}
            </span>
          </p>
          <p id={hintId} className="text-muted-foreground mt-1 text-xs text-pretty">
            {hint}
          </p>
        </div>
        {/* Утгыг доорх `meter` хэлнэ — дэлгэц уншигчид давхардуулахгүй. */}
        <p
          aria-hidden
          className={cn("shrink-0 text-3xl leading-none font-bold tabular-nums", level.text)}
        >
          {percent}
          <span className="text-lg">%</span>
        </p>
      </div>

      <div
        role="meter"
        aria-labelledby={labelId}
        aria-describedby={hintId}
        aria-valuemin={0}
        aria-valuemax={100}
        aria-valuenow={percent}
        aria-valuetext={`${percent}%`}
        className="bg-foreground/10 relative mt-4 h-3 overflow-hidden rounded-full"
      >
        <div
          className={cn(
            "motion-safe:animate-meter-grow h-full rounded-full bg-gradient-to-r transition-[width] duration-700 ease-out motion-reduce:transition-none",
            level.fill,
          )}
          style={{ width: `${percent}%` }}
        />
        {/* Дөрөвний нэг тутмын нарийн зураас — хэмжүүр шиг уншигдана. */}
        {[25, 50, 75].map((mark) => (
          <span
            key={mark}
            aria-hidden
            className="bg-card/80 absolute inset-y-0 w-0.5 -translate-x-1/2"
            style={{ left: `${mark}%` }}
          />
        ))}
      </div>

      {message && (
        <p className={cn("mt-3 flex items-start gap-1.5 text-sm font-medium", level.text)}>
          <TriangleAlertIcon className="mt-0.5 size-4 shrink-0" aria-hidden />
          {message}
        </p>
      )}

      <div className="mt-3 flex flex-wrap items-center justify-between gap-x-4 gap-y-2 text-sm">
        <p className="text-muted-foreground flex items-center gap-1.5">
          <CalendarClockIcon className="size-4 shrink-0" aria-hidden />
          {when}
        </p>
        {children}
      </div>
    </div>
  );
}

function PanelLink({ href, children }: { href: string; children: ReactNode }) {
  return (
    <Link
      href={href}
      className="text-brand-link focus-visible:ring-ring/50 group inline-flex items-center gap-1 rounded-md font-medium underline-offset-4 outline-none hover:underline focus-visible:ring-3"
    >
      {children}
      <ArrowRightIcon
        className="size-4 shrink-0 transition-[translate] group-hover:translate-x-0.5 motion-reduce:transition-none"
        aria-hidden
      />
    </Link>
  );
}

/**
 * Нэг удаагийн эрх: ашиглаагүй бол «1 материал оруулах эрх байна», эс бөгөөс
 * эрхээр нээсэн материал тус бүрийн AI хэрэглээ. Багц авбал эрхийн үнэ хасагдах
 * хугацаанд (`plan.upgrade_credit`) түүнийг, эс бөгөөс Standard-ийг санал болгоно.
 */
function PassPanel({
  config,
  passes,
  plan,
}: {
  config: LiveConfig;
  passes: LivePassInfo;
  plan: PlanStatus | undefined;
}) {
  const materials = useLiveMaterials();
  const titleOf = (id: string) =>
    materials.data?.find((material) => material.id === id)?.title ?? t.passMaterial;
  const upgrade = plan?.upgrade_credit
    ? mn.billing.passCreditNote(
        formatMnt(plan.upgrade_credit.amount_mnt),
        formatDate(plan.upgrade_credit.expires_at),
      )
    : t.getStandard;
  // Ашиглаагүй эрхгүй бол дахин авч болно (багцгүй — `pass` эрхтэй гэдэг нь багцгүй).
  const canBuyAgain = plan !== undefined && !passes.unused && !plan.has_unused_live_pass;

  return (
    <section
      aria-labelledby="live-usage-title"
      className="from-primary/10 bg-card overflow-hidden rounded-3xl border bg-gradient-to-br via-transparent to-transparent shadow-xs"
    >
      <h2 id="live-usage-title" className="sr-only">
        {t.usageLabel}
      </h2>
      <div className="grid md:grid-cols-[minmax(0,20rem)_minmax(0,1fr)]">
        <div className="flex flex-col justify-center gap-4 p-5 sm:p-6">
          <div className="flex items-center gap-4">
            <span
              aria-hidden
              className="bg-primary text-primary-foreground shadow-primary/25 grid size-12 shrink-0 place-items-center rounded-2xl shadow-lg"
            >
              <TicketIcon className="size-6" />
            </span>
            <div className="min-w-0">
              <p className={EYEBROW}>{t.passLabel}</p>
              <p className="mt-0.5 text-lg font-semibold tracking-tight">{t.tiers.pass}</p>
              <p className="text-muted-foreground text-sm">
                {passes.unused
                  ? t.passUnusedStatus
                  : config.tier_expires_at && t.tierUntilDate(formatDate(config.tier_expires_at))}
              </p>
            </div>
          </div>
          {canBuyAgain && (
            <LivePassBuyButton
              plan={plan}
              label={mn.billing.livePassBuyAgain}
              variant="outline"
              className="w-full sm:w-auto md:w-full"
            />
          )}
        </div>

        <div className="divide-y border-t md:border-t-0 md:border-l">
          {passes.unused && (
            <div className="p-5 sm:p-6">
              <p className="flex items-center gap-1.5 font-semibold">
                <SparklesIcon className="text-brand-link size-4" aria-hidden />
                {t.passUnusedTitle}
              </p>
              <p className="text-muted-foreground mt-1 text-sm text-pretty">
                {t.passUnusedBody(plan?.live_pass_access_days ?? 30)}
              </p>
              <div className="mt-3 text-sm">
                <PanelLink href="/pricing">{upgrade}</PanelLink>
              </div>
            </div>
          )}
          {passes.materials.map((opened) => (
            <UsageMeter
              key={opened.material_id}
              percent={opened.ai_used_percent}
              scope={titleOf(opened.material_id)}
              hint={t.passAiHint}
              messages={PASS_MESSAGES}
              when={t.passOpenUntil(formatDate(opened.expires_at))}
            >
              {!passes.unused && <PanelLink href="/pricing">{upgrade}</PanelLink>}
            </UsageMeter>
          ))}
        </div>
      </div>
    </section>
  );
}

export function UsagePanelSkeleton() {
  return <Skeleton aria-hidden className="h-56 w-full rounded-3xl md:h-36" />;
}
