"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation, useQuery } from "@tanstack/react-query";
import {
  CircleCheckIcon,
  CircleXIcon,
  CpuIcon,
  GiftIcon,
  type LucideIcon,
  PauseCircleIcon,
  SearchIcon,
  TriangleAlertIcon,
} from "lucide-react";
import { useState } from "react";
import { useForm, useWatch } from "react-hook-form";
import { toast } from "sonner";

import { FormField } from "@/components/auth/form-field";
import { ErrorState } from "@/components/common/states";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Skeleton } from "@/components/ui/skeleton";
import { Textarea } from "@/components/ui/textarea";
import { ApiError } from "@/lib/api/client";
import {
  getLiveAdminOverview,
  getLiveModels,
  grantLiveSubscription,
  lookupLiveSubscription,
} from "@/lib/api/live";
import { daysLeft, formatDate } from "@/lib/format";
import { mn } from "@/lib/i18n/mn";
import { queryKeys } from "@/lib/query-keys";
import type {
  LiveAdminOverview,
  LiveModelState,
  LiveModelStatus,
  LiveSubscriptionInfo,
} from "@/lib/types/live";
import { cn } from "@/lib/utils";
import {
  liveGrantSchema,
  userPlanLookupSchema,
  type LiveGrantValues,
  type UserPlanLookupValues,
} from "@/lib/validation/admin";

const a = mn.admin;

function errorMessage(error: unknown): string {
  return error instanceof ApiError ? error.message : mn.common.somethingWrong;
}

function usd(value: number): string {
  return `$${value.toFixed(2)}`;
}

/** Энэ сарын Live-ийн тойм: хандалт, AI, зардал ба төсөв, үйлдэл тус бүр, материал. */
export function LiveOverviewCard() {
  const query = useQuery({
    queryKey: queryKeys.admin.liveOverview,
    queryFn: getLiveAdminOverview,
    staleTime: 30_000,
  });

  if (query.isPending) return <Skeleton className="h-80 w-full max-w-3xl rounded-xl" />;
  if (query.isError) {
    return (
      <ErrorState
        className="max-w-3xl"
        description={errorMessage(query.error)}
        onRetry={() => void query.refetch()}
      />
    );
  }
  return <OverviewContent overview={query.data} />;
}

function OverviewContent({ overview }: { overview: LiveAdminOverview }) {
  const percent = Math.max(0, Math.min(100, Math.round(overview.budget_percent)));
  const stats: [string, string | number][] = [
    [a.liveMaterials, overview.materials_total],
    [a.liveMaterialsFailed, overview.materials_failed],
    [a.liveUsers, overview.users_with_materials],
  ];

  return (
    <Card className="max-w-3xl">
      <CardContent className="space-y-6">
        <h2 className="text-lg font-semibold tracking-tight">{a.liveOverviewTitle}</h2>

        <dl className="grid gap-3 sm:grid-cols-2">
          <div className="rounded-lg border p-3">
            <dt className="text-muted-foreground text-xs">{a.liveAccess}</dt>
            <dd className="mt-1 font-semibold">{a.liveAccessModes[overview.live_access]}</dd>
          </div>
          <div className="rounded-lg border p-3">
            <dt className="text-muted-foreground text-xs">{a.liveAi}</dt>
            <dd
              className={cn(
                "mt-1 flex items-center gap-1.5 font-semibold",
                overview.ai_configured ? "text-success" : "text-destructive",
              )}
            >
              {overview.ai_configured ? (
                <CircleCheckIcon className="size-4" aria-hidden />
              ) : (
                <CircleXIcon className="size-4" aria-hidden />
              )}
              {overview.ai_configured ? a.liveAiOn : a.liveAiOff}
            </dd>
          </div>
        </dl>

        <div className="space-y-2">
          <div className="flex flex-wrap items-baseline justify-between gap-2">
            <p className="text-sm font-medium">{a.liveSpend}</p>
            <p className="font-semibold tabular-nums">
              {a.liveSpendValue(usd(overview.month_spend_usd), usd(overview.budget_usd))}
              <span className="text-muted-foreground ml-2 text-sm font-normal">{percent}%</span>
            </p>
          </div>
          <div
            role="progressbar"
            aria-label={a.liveSpendLabel}
            aria-valuemin={0}
            aria-valuemax={100}
            aria-valuenow={percent}
            className="bg-foreground/10 h-2 w-full overflow-hidden rounded-full"
          >
            <div
              className={cn("h-full rounded-full", percent >= 90 ? "bg-destructive" : "bg-primary")}
              style={{ width: `${percent}%` }}
            />
          </div>
        </div>

        <dl className="grid grid-cols-3 divide-x rounded-lg border">
          {stats.map(([label, value]) => (
            <div key={label} className="p-3">
              <dt className="text-muted-foreground text-xs leading-snug">{label}</dt>
              <dd className="mt-1 text-xl font-bold tabular-nums">{value}</dd>
            </div>
          ))}
        </dl>

        <section aria-labelledby="live-capability-title" className="space-y-3">
          <h3 id="live-capability-title" className="text-sm font-semibold">
            {a.liveByCapability}
          </h3>
          {overview.by_capability.length === 0 ? (
            <p className="text-muted-foreground text-sm">{a.liveNoSpend}</p>
          ) : (
            // Утсан дээр хэвтээ гүйлгэгдэнэ — гараар ч гүйлгэх боломжтой байх ёстой.
            <div
              tabIndex={0}
              role="region"
              aria-labelledby="live-capability-title"
              className="focus-visible:ring-ring/50 overflow-x-auto rounded-lg border outline-none focus-visible:ring-3"
            >
              <table className="w-full text-xs sm:text-sm">
                <thead className="bg-muted/50 text-left">
                  <tr>
                    <th scope="col" className="px-2 py-2 font-medium sm:px-3">
                      {a.liveCapability}
                    </th>
                    <th scope="col" className="px-2 py-2 text-right font-medium sm:px-3">
                      {a.liveRequests}
                    </th>
                    <th scope="col" className="px-2 py-2 text-right font-medium sm:px-3">
                      {a.liveFailed}
                    </th>
                    <th scope="col" className="px-2 py-2 text-right font-medium sm:px-3">
                      {a.liveCost}
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y">
                  {overview.by_capability.map((row) => (
                    <tr key={row.capability}>
                      <th scope="row" className="px-2 py-2 text-left font-normal sm:px-3">
                        {a.liveCapabilities[row.capability] ?? row.capability}
                      </th>
                      <td className="px-2 py-2 text-right tabular-nums sm:px-3">{row.requests}</td>
                      <td className="px-2 py-2 text-right tabular-nums sm:px-3">{row.failed}</td>
                      <td className="px-2 py-2 text-right tabular-nums sm:px-3">
                        {usd(row.cost_usd)}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </section>
      </CardContent>
    </Card>
  );
}

const MODEL_STATE_META: Record<LiveModelState, { icon: LucideIcon; className: string }> = {
  ready: { icon: CircleCheckIcon, className: "border-success/40 text-success border" },
  cooling: { icon: PauseCircleIcon, className: "bg-accent text-accent-foreground" },
  near_limit: { icon: TriangleAlertIcon, className: "bg-accent text-accent-foreground" },
  not_configured: { icon: CircleXIcon, className: "bg-muted text-muted-foreground" },
  no_price: { icon: CircleXIcon, className: "bg-destructive/10 text-destructive" },
};

function clockTime(iso: string): string {
  return new Date(iso).toLocaleTimeString("mn-MN", {
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false,
  });
}

/**
 * Загвар бүр хязгаарт хүрсэн эсэх. Хөргөлт секундээр өөрчлөгддөг тул 15 сек
 * тутам шинэчилнэ. Google үлдсэн квотыг хэлдэггүй — төлөв нь Google-ийн сүүлийн
 * 429/503 хариу ба `AI_MODEL_LIMITS`-тэй харьцуулсан манай тоолол.
 */
export function LiveModelsCard() {
  const query = useQuery({
    queryKey: queryKeys.admin.liveModels,
    queryFn: getLiveModels,
    refetchInterval: 15_000,
  });

  return (
    <Card className="max-w-3xl">
      <CardContent className="space-y-4">
        <div>
          <h2 className="flex items-center gap-2 text-lg font-semibold tracking-tight">
            <CpuIcon className="text-brand-link size-5" aria-hidden />
            {a.liveModelsTitle}
          </h2>
          <p className="text-muted-foreground mt-1 text-sm">{a.liveModelsHint}</p>
        </div>
        {query.isPending ? (
          <Skeleton className="h-48 w-full rounded-lg" />
        ) : query.isError ? (
          <ErrorState
            description={errorMessage(query.error)}
            onRetry={() => void query.refetch()}
          />
        ) : query.data.length === 0 ? (
          <p className="text-muted-foreground text-sm">{a.liveModelsEmpty}</p>
        ) : (
          <ul className="divide-y rounded-lg border" aria-live="polite">
            {query.data.map((model) => (
              <ModelRow key={model.model} model={model} />
            ))}
          </ul>
        )}
      </CardContent>
    </Card>
  );
}

function ModelRow({ model }: { model: LiveModelStatus }) {
  const meta = MODEL_STATE_META[model.status];
  const Icon = meta.icon;
  const [provider, ...rest] = model.model.split(":");
  const name = rest.join(":") || model.model;
  const reason = model.reason ? (a.liveModelReasons[model.reason] ?? model.reason) : null;
  const limits = model.limits;
  const usage: [string, string][] = [
    [
      a.liveModelMinute,
      `${a.liveModelRequests(model.minute_requests, limits?.rpm)} · ${a.liveModelTokens(
        model.minute_input_tokens,
        limits?.tpm,
      )}`,
    ],
    [a.liveModelDay, a.liveModelRequests(model.day_requests, limits?.rpd)],
    [
      a.liveModelMonth,
      a.liveModelMonthValue(model.month_requests, model.month_failures, usd(model.month_cost_usd)),
    ],
  ];

  return (
    <li className="space-y-3 p-4">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <p className="min-w-0 text-sm">
          <span className="font-mono font-semibold break-all">{name}</span>
          <span className="text-muted-foreground ml-2 text-xs">
            {a.liveModelProviders[provider] ?? provider}
          </span>
        </p>
        <span
          className={cn(
            "inline-flex items-center gap-1.5 rounded-full px-2.5 py-0.5 text-xs font-medium",
            meta.className,
          )}
        >
          <Icon className="size-3.5" aria-hidden />
          {a.liveModelStates[model.status] ?? model.status}
          {reason && <span className="font-normal">· {reason}</span>}
          {model.available_at && (
            <span className="font-normal tabular-nums">
              · {a.liveModelUntil(clockTime(model.available_at))}
            </span>
          )}
        </span>
      </div>

      <ul className="flex flex-wrap gap-1.5">
        {model.tasks.map((task) => (
          <li
            key={task.task}
            className={cn(
              "rounded-md border px-2 py-0.5 text-xs",
              task.position === 1 ? "border-primary/60 font-medium" : "text-muted-foreground",
            )}
          >
            {a.liveCapabilities[task.task] ?? task.task} ·{" "}
            {task.position === 1 ? a.liveModelPrimary : a.liveModelFallback(task.position)}
          </li>
        ))}
      </ul>

      <dl className="grid gap-x-4 gap-y-1 text-sm sm:grid-cols-[auto_1fr]">
        {usage.map(([label, value]) => (
          <div key={label} className="contents">
            <dt className="text-muted-foreground">{label}</dt>
            <dd className="tabular-nums">{value}</dd>
          </div>
        ))}
      </dl>

      <p className="text-muted-foreground text-xs">
        {model.price_input_usd !== null && model.price_output_usd !== null
          ? a.liveModelPrice(usd(model.price_input_usd), usd(model.price_output_usd))
          : a.liveModelStates.no_price}
        {!limits && ` · ${a.liveModelNoLimits}`}
        {model.last_error && model.last_error_at && (
          <> · {a.liveModelLastError(model.last_error, clockTime(model.last_error_at))}</>
        )}
      </p>
    </li>
  );
}

/**
 * Хэрэглэгчид Premium-ийг гараар олгох. `UserPlanForm`-той ижил урсгал: имэйлээр
 * хайх → одоогийн эрх → олгох. Standard-ийг сервер хамт сунгана; эрхийг сервер шалгана.
 */
export function LiveGrantForm() {
  const [info, setInfo] = useState<LiveSubscriptionInfo | null>(null);

  const form = useForm<UserPlanLookupValues>({
    resolver: zodResolver(userPlanLookupSchema),
    defaultValues: { email: "" },
  });

  const lookup = useMutation({
    mutationFn: (values: UserPlanLookupValues) => lookupLiveSubscription(values.email),
    onSuccess: setInfo,
    onError: (error) => {
      setInfo(null);
      if (error instanceof ApiError && error.status === 404) {
        form.setError("email", { message: a.userPlanNotFound });
      } else {
        toast.error(errorMessage(error));
      }
    },
  });

  return (
    <Card className="max-w-xl">
      <CardContent className="space-y-6">
        <div>
          <h2 className="text-lg font-semibold tracking-tight">{a.liveGrantTitle}</h2>
          <p className="text-muted-foreground mt-1 text-sm">{a.liveGrantHint}</p>
        </div>

        <form
          onSubmit={form.handleSubmit((values) => lookup.mutate(values))}
          noValidate
          className="space-y-4"
        >
          <FormField
            id="live-grant-email"
            type="email"
            autoComplete="off"
            label={a.userPlanEmail}
            error={form.formState.errors.email?.message}
            {...form.register("email")}
          />
          <Button type="submit" disabled={lookup.isPending}>
            <SearchIcon className="size-4" />
            {lookup.isPending ? a.userPlanSearching : a.userPlanSearch}
          </Button>
        </form>

        {info && <LiveGrantPanel key={info.email} info={info} onChange={setInfo} />}
      </CardContent>
    </Card>
  );
}

function subscriptionStatus(info: LiveSubscriptionInfo): string {
  const tier = mn.live.tiers[info.tier];
  if (info.tier === "free" || !info.expires_at) return a.liveGrantStatus(tier, null);
  if (daysLeft(info.expires_at) === 0) return a.userPlanExpired(formatDate(info.expires_at));
  return a.liveGrantStatus(tier, formatDate(info.expires_at));
}

function LiveGrantPanel({
  info,
  onChange,
}: {
  info: LiveSubscriptionInfo;
  onChange: (info: LiveSubscriptionInfo) => void;
}) {
  const form = useForm<LiveGrantValues>({
    resolver: zodResolver(liveGrantSchema),
    defaultValues: { months: 1, note: "" },
  });
  const months = useWatch({ control: form.control, name: "months" });
  const validMonths = Number.isInteger(months) && months >= 1 && months <= 24 ? months : 1;
  const errors = form.formState.errors;

  const grant = useMutation({
    mutationFn: (values: LiveGrantValues) =>
      grantLiveSubscription({
        email: info.email,
        months: values.months,
        note: values.note || undefined,
      }),
    onSuccess: (updated) => {
      onChange(updated);
      form.reset({ months: 1, note: "" });
      toast.success(a.liveGrantSaved);
    },
    onError: (error) => toast.error(errorMessage(error)),
  });

  return (
    <div className="space-y-6 border-t pt-6">
      <div>
        <p className="font-medium">{info.name}</p>
        <p className="text-muted-foreground text-sm">{info.email}</p>
        <div aria-live="polite">
          <p className="text-brand-link mt-1 text-sm font-medium">{subscriptionStatus(info)}</p>
          {info.tier !== "standard" && (
            <p className="text-muted-foreground text-xs">
              {a.liveGrantPlan(info.plan_expires_at ? formatDate(info.plan_expires_at) : null)}
            </p>
          )}
        </div>
      </div>

      <form
        onSubmit={form.handleSubmit((values) => grant.mutate(values))}
        noValidate
        className="space-y-4"
      >
        <FormField
          id="live-grant-months"
          type="number"
          inputMode="numeric"
          min={1}
          max={24}
          step={1}
          label={a.liveGrantMonths}
          hint={a.liveGrantMonthsHint}
          error={errors.months?.message}
          {...form.register("months", { valueAsNumber: true })}
        />

        <div className="space-y-2">
          <Label htmlFor="live-grant-note">{a.userPlanNote}</Label>
          <Textarea
            id="live-grant-note"
            rows={2}
            maxLength={500}
            aria-describedby="live-grant-note-hint"
            aria-invalid={errors.note ? true : undefined}
            {...form.register("note")}
          />
          <p id="live-grant-note-hint" className="text-muted-foreground text-xs">
            {a.userPlanNoteHint}
          </p>
          {errors.note && (
            <p role="alert" className="text-destructive text-xs">
              {errors.note.message}
            </p>
          )}
        </div>

        <Button type="submit" disabled={grant.isPending}>
          <GiftIcon className="size-4" />
          {a.liveGrantSubmit(validMonths)}
        </Button>
      </form>
    </div>
  );
}
