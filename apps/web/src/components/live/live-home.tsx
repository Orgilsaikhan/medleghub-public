"use client";

import { ArrowRightIcon, CircleCheckIcon, CrownIcon, TriangleAlertIcon } from "lucide-react";
import Link from "next/link";

import { LivePassOffer } from "@/components/billing/live-pass-offer";
import { ErrorState } from "@/components/common/states";
import { LiveMark } from "@/components/live/live-mark";
import { LiveTile, OrbitArcs } from "@/components/live/live-ui";
import { MaterialGridSkeleton, MaterialList } from "@/components/live/material-list";
import { UploadCard } from "@/components/live/upload-card";
import { UsagePanel, UsagePanelSkeleton } from "@/components/live/usage-panel";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { useCurrentUser } from "@/lib/hooks/use-auth";
import { liveErrorMessage, useLiveConfig } from "@/lib/hooks/use-live";
import { usePlan } from "@/lib/hooks/use-plan";
import { mn } from "@/lib/i18n/mn";

const t = mn.live;

/**
 * `/live`-ийн эхлэл: нэвтрээгүй зочинд багц ба нэг удаагийн эрхийн санал
 * (авахын тулд нэвтэрнэ), нэвтэрсэн хэрэглэгчид `LiveHome`.
 */
export function LiveEntry() {
  const { isLoading, isAuthenticated } = useCurrentUser();
  if (isLoading) return <LiveHomeSkeleton />;
  return isAuthenticated ? <LiveHome /> : <LiveGuest />;
}

/** Зочин: Live бүгдэд нээлттэй бол багц ба нэг удаагийн эрх, эс бөгөөс «удахгүй». */
function LiveGuest() {
  const plan = usePlan();
  if (plan.isPending) return <LiveHomeSkeleton />;
  if (plan.isError) return <ErrorState onRetry={() => void plan.refetch()} />;
  if (!plan.data.live_pass_available) return <LiveClosed />;
  return <PlanOffer />;
}

/**
 * `/live` — хэрэглээ, файл оруулах, материалын жагсаалт.
 *
 * Live энэ хэрэглэгчид нээлттэй эсэхийг сервер (`LIVE_ACCESS`) шийднэ; хаалттай
 * бол бусад Live дуудлага бүгд 404 буцаадаг тул зөвхөн мэдэгдэл харуулна. Багцгүй
 * (`free`) хэрэглэгчид Live нээлттэй биш — Standard, Premium эсвэл нэг удаагийн
 * эрхийг санал болгоно. Нэг удаагийн эрхтэй (`pass`) хэрэглэгч ашиглаагүй эрхээрээ
 * нэг материал оруулж, зөвхөн эрхээр нээсэн материалаа харна.
 */
function LiveHome() {
  // Хэрэглээ энд л харагдана — толгойн холбоосынхоос шинэ байх ёстой.
  const config = useLiveConfig({ staleTime: 15_000 });

  if (config.isPending) return <LiveHomeSkeleton />;
  if (config.isError) {
    return (
      <ErrorState
        description={liveErrorMessage(config.error)}
        onRetry={() => void config.refetch()}
      />
    );
  }

  const data = config.data;
  if (!data.enabled) return <LiveClosed />;

  // Live нь Standard, Premium эсвэл нэг удаагийн эрхэд — бусад Live дуудлага 402 буцаана.
  if (data.tier === "free") return <PlanOffer />;
  const canUpload = data.tier !== "pass" || (data.passes?.unused ?? false);

  return (
    <div className="space-y-10 sm:space-y-12">
      <div className="space-y-6">
        <UsagePanel config={data} />
        {!data.ai_configured && (
          <Alert>
            <TriangleAlertIcon aria-hidden />
            <AlertTitle>{t.aiOffTitle}</AlertTitle>
            <AlertDescription>{t.aiOffBody}</AlertDescription>
          </Alert>
        )}
        {canUpload && <UploadCard config={data} />}
      </div>
      <MaterialList />
    </div>
  );
}

/** Live хараахан нээгдээгүй — тэмдэг ба мэдэгдэл. */
function LiveClosed() {
  return (
    <div className="bg-card/60 flex flex-col items-center rounded-3xl border border-dashed px-6 py-20 text-center">
      <span
        aria-hidden
        className="bg-muted text-muted-foreground grid size-16 place-items-center rounded-2xl"
      >
        <LiveMark className="size-9" />
      </span>
      <p className="mt-5 font-semibold">{t.closedTitle}</p>
      <p className="text-muted-foreground mt-1.5 max-w-sm text-sm">{t.closedBody}</p>
    </div>
  );
}

/** Багцгүй хэрэглэгч, зочин: Standard, Premium багц эсвэл нэг удаагийн эрх. */
function PlanOffer() {
  return (
    <div className="space-y-6">
      <PlanRequired />
      <LivePassOffer returnTo="/live" />
    </div>
  );
}

/** Live нь Standard, Premium багцад — юу авахыг нь харуулна. */
function PlanRequired() {
  return (
    <section
      aria-labelledby="live-plan-title"
      className="bg-card relative isolate overflow-hidden rounded-3xl border shadow-xs"
    >
      <div
        aria-hidden
        className="from-primary/12 absolute inset-0 -z-10 bg-gradient-to-br via-transparent to-transparent"
      />

      <div className="grid items-center gap-8 p-6 sm:p-10 md:grid-cols-[minmax(0,1fr)_15rem] lg:grid-cols-[minmax(0,1fr)_20rem]">
        <div className="flex flex-col items-start gap-6">
          <LiveTile>
            <CrownIcon className="size-6" />
          </LiveTile>
          <div className="space-y-2">
            <h2
              id="live-plan-title"
              className="max-w-2xl text-xl font-semibold tracking-tight text-balance sm:text-2xl"
            >
              {t.planTitle}
            </h2>
            <p className="text-muted-foreground max-w-2xl text-pretty">{t.planBody}</p>
          </div>
          <ul className="space-y-2.5">
            {t.steps.map((step) => (
              <li key={step} className="flex items-start gap-2.5 text-sm">
                <CircleCheckIcon className="text-success mt-0.5 size-4 shrink-0" aria-hidden />
                {step}
              </li>
            ))}
          </ul>
          <Button asChild size="lg" className="group/cta">
            <Link href="/pricing">
              {t.planCta}
              <ArrowRightIcon
                aria-hidden
                className="transition-[translate] group-hover/cta:translate-x-0.5 motion-reduce:transition-none"
              />
            </Link>
          </Button>
        </div>

        {/* Тойрог замын төвд Live-ийн тэмдэг — өргөн дэлгэцэд л. */}
        <div aria-hidden className="relative hidden aspect-square place-items-center md:grid">
          <OrbitArcs className="text-primary absolute top-1/2 left-1/2 w-[26rem] max-w-none -translate-x-1/2 -translate-y-1/2 lg:w-[32rem]" />
          <span className="bg-primary/35 absolute size-24 rounded-full blur-2xl" />
          <LiveTile className="size-20 rounded-3xl lg:size-24">
            <LiveMark className="size-12 lg:size-14" />
          </LiveTile>
        </div>
      </div>
    </section>
  );
}

export function LiveHomeSkeleton() {
  return (
    <div className="space-y-10 sm:space-y-12" aria-hidden>
      <div className="space-y-6">
        <UsagePanelSkeleton />
        <Skeleton className="h-80 w-full rounded-3xl" />
      </div>
      <div className="space-y-5">
        <Skeleton className="h-6 w-48" />
        <MaterialGridSkeleton />
      </div>
    </div>
  );
}
