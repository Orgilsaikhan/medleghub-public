"use client";

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { CheckIcon, GiftIcon, TicketIcon, TicketPercentIcon, XIcon } from "lucide-react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { useId, useState } from "react";
import { toast } from "sonner";

import { LivePassOffer } from "@/components/billing/live-pass-offer";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Slider } from "@/components/ui/slider";
import { checkPromo, redeemPromo, startCheckout } from "@/lib/api/billing";
import { ApiError } from "@/lib/api/client";
import { rememberReturnPath, safeReturnPath } from "@/lib/billing";
import { formatDate, formatMnt } from "@/lib/format";
import { useCurrentUser } from "@/lib/hooks/use-auth";
import { usePlan } from "@/lib/hooks/use-plan";
import { mn } from "@/lib/i18n/mn";
import { queryKeys } from "@/lib/query-keys";
import type { BillingPlan, PlanOption, PlanStatus, PromoPreview } from "@/lib/types/api";
import { cn } from "@/lib/utils";

/**
 * Үнэгүй, Standard ба (MedlegHub Live нээлттэй үед) Premium багц. Багцыг 1–12
 * сараар авна — 6 сар тутамд 1 сар үнэгүй. Үнийг сервер тооцдог (`plan.options`,
 * `plan.premium_options`), энд зөвхөн харуулна. Premium = Standard + Live-ийн илүү
 * AI; төлбөр нь Standard-ийг ч мөн хугацаагаар сунгана.
 *
 * Хөнгөлөлт (нэг төлбөрт нэг, нийлэхгүй): оруулсан промо код, эс бөгөөс
 * урилгын кодоор бүртгүүлсний хөнгөлөлт (`plan.discount`). Хөнгөлөлттэй үнийг
 * мөн сервер өгнө.
 *
 * Нэг удаагийн Live эрх (`LivePassOffer`) — багц биш, нэг материал; зочин ч харна.
 * Эрх авснаас хойш хэдэн хоногт багц авбал эрхийн үнэ хасагдана
 * (`plan.upgrade_credit`, үнэд аль хэдийн орсон).
 *
 * Төлбөрийг Wire-ийн hosted хуудас (`pay.wire.mn`) авна — энэ хуудас зөвхөн
 * нэхэмжлэх үүсгэж, хэрэглэгчийг тийш шилжүүлнэ. Картын мэдээлэл энд хэзээ ч
 * орохгүй.
 */
export function PricingView({ initialPrice = null }: { initialPrice?: number | null }) {
  const params = useSearchParams();
  const returnTo = safeReturnPath(params.get("next"));
  const { data: plan } = usePlan();
  // Серверээс ирсэн (нэвтрээгүй) үнэ — хайлтын систем, JS ачаалахаас өмнө харагдана.
  const priceMnt = plan?.price_mnt ?? initialPrice;
  // Premium-ийн ялгаа нь MedlegHub Live — Live нээлттэй үед л хоёуланд нь дурдана.
  const premium = plan?.premium_available ?? false;
  const standardPerks = premium
    ? [...mn.billing.standardPerks, mn.billing.standardLivePerk]
    : mn.billing.standardPerks;

  return (
    <div
      className={cn(
        "mx-auto mt-10 grid gap-6 md:grid-cols-2",
        premium ? "max-w-6xl lg:grid-cols-3" : "max-w-4xl",
      )}
    >
      <Tier
        name={mn.billing.freeName}
        price={formatMnt(0)}
        perks={mn.billing.freePerks}
        current={plan ? !plan.has_plan : false}
      />
      <Tier
        name={mn.billing.standardName}
        price={priceMnt !== null ? formatMnt(priceMnt) : null}
        perks={standardPerks}
        current={(plan?.has_plan ?? false) && !plan?.has_premium}
        highlighted
      >
        <PlanAction kind="standard" plan={plan} returnTo={returnTo} />
      </Tier>
      {premium && plan && (
        <Tier
          name={mn.billing.premiumName}
          price={formatMnt(plan.premium_price_mnt)}
          perks={mn.billing.premiumPerks(plan.premium_usage_multiplier)}
          current={plan.has_premium}
          highlighted
        >
          <PlanAction kind="premium" plan={plan} returnTo={returnTo} />
          <p className="text-muted-foreground mt-3 text-xs">{mn.billing.premiumNote}</p>
        </Tier>
      )}

      <LivePassOffer
        returnTo={returnTo ? `/pricing?next=${encodeURIComponent(returnTo)}` : "/pricing"}
        className={cn("md:col-span-2", premium && "lg:col-span-3")}
      />

      <p
        className={cn(
          "text-muted-foreground text-center text-xs leading-relaxed md:col-span-2",
          premium && "lg:col-span-3",
        )}
      >
        {mn.billing.paymentNote}
      </p>
    </div>
  );
}

interface TierProps {
  name: string;
  /** `null` — үнэ ачаалж байна. */
  price: string | null;
  perks: readonly string[];
  current: boolean;
  highlighted?: boolean;
  children?: React.ReactNode;
}

function Tier({ name, price, perks, current, highlighted = false, children }: TierProps) {
  return (
    <section
      aria-label={name}
      className={cn(
        "bg-card flex flex-col rounded-xl border p-6 sm:p-8",
        highlighted && "border-primary/50 shadow-sm",
      )}
    >
      <div className="flex items-center justify-between gap-3">
        <h2 className="text-lg font-semibold">{name}</h2>
        {current && <Badge variant="secondary">{mn.billing.currentPlan}</Badge>}
      </div>

      <p className="mt-4 flex items-baseline gap-1.5">
        <span className="text-4xl font-bold tracking-tight">{price ?? "—"}</span>
        {highlighted && (
          <span className="text-muted-foreground text-sm">{mn.billing.perMonth}</span>
        )}
      </p>

      <ul className="mt-6 flex-1 space-y-3 text-sm">
        {perks.map((perk) => (
          <li key={perk} className="flex items-start gap-2.5">
            <CheckIcon className="text-success mt-0.5 size-4 shrink-0" aria-hidden />
            {perk}
          </li>
        ))}
      </ul>

      {children && <div className="mt-8">{children}</div>}
    </section>
  );
}

function PlanAction({
  kind,
  plan,
  returnTo,
}: {
  kind: BillingPlan;
  plan?: PlanStatus;
  returnTo: string | null;
}) {
  const { isAuthenticated, isLoading } = useCurrentUser();
  const premium = kind === "premium";
  const [months, setMonths] = useState(1);
  const [promo, setPromo] = useState<PromoPreview | null>(null);
  // Хувийн промо код үнийг өөрчилнө; үнэгүй сарын код тусдаа товчоор идэвхжинэ.
  const percentPromo = promo?.kind === "percent" ? promo : null;

  const checkout = useMutation({
    mutationFn: () => startCheckout(months, percentPromo?.code, kind),
    onSuccess: ({ checkout_url }) => {
      rememberReturnPath(returnTo);
      window.location.assign(checkout_url);
    },
    onError: (error) => {
      toast.error(error instanceof ApiError ? error.message : mn.common.somethingWrong);
    },
  });

  const buyLabel = premium ? mn.billing.premiumBuy : mn.billing.buy;
  if (isLoading || !plan) {
    return (
      <Button size="lg" className="w-full" disabled>
        {buyLabel}
      </Button>
    );
  }

  const options = premium
    ? (percentPromo?.premium_options ?? plan.premium_options)
    : (percentPromo?.options ?? plan.options);
  const active = premium ? plan.has_premium : plan.has_plan;
  const expiresAt = premium ? plan.premium_expires_at : plan.plan_expires_at;

  const picker = (
    <PeriodPicker
      options={options}
      monthly={premium ? plan.premium_price_mnt : plan.price_mnt}
      percentOff={percentPromo?.percent_off ?? plan.discount?.percent_off ?? 0}
      months={months}
      onChange={setMonths}
    />
  );

  if (!isAuthenticated) {
    const next = returnTo ? `/pricing?next=${encodeURIComponent(returnTo)}` : "/pricing";
    return (
      <div className="space-y-4">
        {picker}
        <Button asChild size="lg" className="w-full">
          <Link href={`/login?next=${encodeURIComponent(next)}`}>{mn.billing.loginToBuy}</Link>
        </Button>
      </div>
    );
  }

  // Шилжих хүртэл товч идэвхгүй хэвээр — давхар нэхэмжлэх үүсэхгүй.
  const busy = checkout.isPending || checkout.isSuccess;

  return (
    <div className="space-y-4">
      {active && expiresAt && (
        <p className="text-sm font-medium">{mn.billing.activeUntil(formatDate(expiresAt))}</p>
      )}
      {!active && expiresAt && (
        <p className="text-muted-foreground text-sm">
          {mn.billing.expiredOn(formatDate(expiresAt))}
        </p>
      )}
      {picker}
      {plan.upgrade_credit && (
        <p className="flex items-start gap-2 text-sm" role="status">
          <TicketIcon className="text-brand-link mt-0.5 size-4 shrink-0" aria-hidden />
          {mn.billing.passCreditNote(
            formatMnt(plan.upgrade_credit.amount_mnt),
            formatDate(plan.upgrade_credit.expires_at),
          )}
        </p>
      )}
      <PromoCodeBox plan={plan} promo={promo} onChange={setPromo} disabled={busy} />
      <Button
        size="lg"
        className="w-full"
        variant={active ? "outline" : "default"}
        disabled={busy}
        onClick={() => checkout.mutate()}
      >
        {busy ? mn.billing.redirecting : active ? mn.billing.extend(months) : buyLabel}
      </Button>
    </div>
  );
}

/**
 * Промо код. Хувийн код — доорх үнийг хөнгөлөлттэйгээр харуулж, checkout-д
 * дамжина. Үнэгүй сарын код — «N сар үнэгүй идэвхжүүлэх» товчоор багцыг шууд
 * сунгана. Ашиглаагүй урилгын хөнгөлөлт байвал аль нь орохыг хэлнэ.
 */
function PromoCodeBox({
  plan,
  promo,
  onChange,
  disabled,
}: {
  plan: PlanStatus;
  promo: PromoPreview | null;
  onChange: (promo: PromoPreview | null) => void;
  disabled: boolean;
}) {
  const queryClient = useQueryClient();
  const router = useRouter();
  const inputId = useId();
  const errorId = `${inputId}-error`;
  const [open, setOpen] = useState(false);
  const [code, setCode] = useState("");
  const [error, setError] = useState<string | null>(null);

  const check = useMutation({
    mutationFn: (value: string) => checkPromo(value),
    onSuccess: (preview) => {
      setError(null);
      onChange(preview);
    },
    onError: (err) => setError(err instanceof ApiError ? err.message : mn.common.somethingWrong),
  });

  const redeem = useMutation({
    mutationFn: (value: string) => redeemPromo(value),
    onSuccess: (updated) => {
      void queryClient.invalidateQueries({ queryKey: queryKeys.billing.plan });
      void queryClient.invalidateQueries({ queryKey: queryKeys.currentUser });
      void queryClient.invalidateQueries({ queryKey: queryKeys.me.profile });
      // Төлбөртэй адил баримт хэвлэгч рүү — 0₮, промо код, нэмэгдсэн сар.
      router.push(`/billing/success?redemption=${encodeURIComponent(updated.redemption_id)}`);
    },
    onError: (err) => toast.error(err instanceof ApiError ? err.message : mn.common.somethingWrong),
  });

  const referral = plan.discount?.source === "referral" ? plan.discount : null;

  if (promo) {
    const free = promo.kind === "free_months" && promo.free_months !== null;
    return (
      <div className="bg-muted/50 space-y-3 rounded-lg border p-3 text-sm">
        <div className="flex items-start justify-between gap-3">
          <p className="flex items-start gap-2" role="status">
            {free ? (
              <GiftIcon className="text-brand-link mt-0.5 size-4 shrink-0" aria-hidden />
            ) : (
              <TicketPercentIcon className="text-brand-link mt-0.5 size-4 shrink-0" aria-hidden />
            )}
            <span>
              <span className="font-medium">
                {free
                  ? mn.billing.promoFree(promo.code, promo.free_months ?? 0)
                  : mn.billing.promoApplied(promo.code, promo.percent_off ?? 0)}
              </span>
              {promo.expires_at && (
                <span className="text-muted-foreground block text-xs">
                  {mn.billing.promoValidUntil(formatDate(promo.expires_at))}
                </span>
              )}
            </span>
          </p>
          <Button
            type="button"
            variant="ghost"
            size="sm"
            disabled={disabled || redeem.isPending}
            onClick={() => onChange(null)}
          >
            <XIcon className="size-4" aria-hidden />
            {mn.billing.promoRemove}
          </Button>
        </div>
        {free && (
          <Button
            type="button"
            className="w-full"
            // Амжилттай бол баримт руу шилжих хүртэл дахин дарагдахгүй.
            disabled={redeem.isPending || redeem.isSuccess}
            onClick={() => redeem.mutate(promo.code)}
          >
            {redeem.isPending || redeem.isSuccess
              ? mn.billing.promoRedeeming
              : mn.billing.promoRedeem(promo.free_months ?? 0)}
          </Button>
        )}
        {!free && referral && (
          <p className="text-muted-foreground text-xs">
            {mn.billing.referralDiscountSaved(referral.percent_off)}
          </p>
        )}
      </div>
    );
  }

  return (
    <div className="space-y-2 text-sm">
      {referral && (
        <p className="flex items-start gap-2" role="status">
          <GiftIcon className="text-brand-link mt-0.5 size-4 shrink-0" aria-hidden />
          {mn.billing.referralDiscount(referral.percent_off)}
        </p>
      )}
      {open ? (
        <form
          className="space-y-2"
          noValidate
          onSubmit={(event) => {
            event.preventDefault();
            const value = code.trim();
            if (!value) {
              setError(mn.billing.promoRequired);
              return;
            }
            check.mutate(value);
          }}
        >
          <Label htmlFor={inputId}>{mn.billing.promoLabel}</Label>
          <div className="flex gap-2">
            <Input
              id={inputId}
              value={code}
              onChange={(event) => {
                setCode(event.target.value.toUpperCase());
                setError(null);
              }}
              autoComplete="off"
              autoCapitalize="characters"
              spellCheck={false}
              maxLength={64}
              placeholder="HELLOWORLD2026"
              aria-invalid={error ? true : undefined}
              aria-describedby={error ? errorId : undefined}
              className={cn("uppercase", error && "border-destructive")}
            />
            <Button type="submit" variant="outline" disabled={check.isPending}>
              {check.isPending ? mn.billing.promoChecking : mn.billing.promoApply}
            </Button>
          </div>
          {error && (
            <p id={errorId} role="alert" className="text-destructive text-xs">
              {error}
            </p>
          )}
        </form>
      ) : (
        <Button
          type="button"
          variant="link"
          size="sm"
          className="h-auto px-0"
          onClick={() => {
            setOpen(true);
            setTimeout(() => document.getElementById(inputId)?.focus(), 0);
          }}
        >
          {mn.billing.promoToggle}
        </Button>
      )}
    </div>
  );
}

/** Хугацааг слайдераар сонгоно — нийт үнэ, үнэгүй сар, хөнгөлөлтийг доор нь харуулна. */
function PeriodPicker({
  options,
  monthly,
  percentOff,
  months,
  onChange,
}: {
  options: PlanOption[];
  monthly: number;
  /** Энэ төлбөрт орох хөнгөлөлт — үнийг сервер тооцсон (`final_price_mnt`). */
  percentOff: number;
  months: number;
  onChange: (months: number) => void;
}) {
  const labelId = useId();
  const option = options.find((item) => item.months === months) ?? options[0];
  if (!option) return null;

  const max = options.length;
  const regular = monthly * option.months;
  // Үнэгүй сар эхлэх цэгүүд (6, 12) — слайдерын доор тэмдэглэнэ.
  const marks = options.filter(
    (item, index) => item.free_months > (options[index - 1]?.free_months ?? 0),
  );
  const describe = (item: PlanOption) =>
    item.free_months > 0
      ? `${mn.billing.months(item.months)} · ${mn.billing.freeMonths(item.free_months)}`
      : mn.billing.months(item.months);

  return (
    <div className="space-y-2">
      <div className="flex items-baseline justify-between gap-3">
        <span id={labelId} className="text-sm font-medium">
          {mn.billing.period}
        </span>
        <span className="text-sm font-semibold tabular-nums">
          {mn.billing.months(option.months)}
        </span>
      </div>

      <Slider
        min={1}
        max={max}
        step={1}
        value={[option.months]}
        onValueChange={([value]) => {
          if (value) onChange(value);
        }}
        className="py-2"
        thumbProps={{ "aria-labelledby": labelId, "aria-valuetext": describe(option) }}
      />

      {/* Бариул нь замын хоёр үзүүрээс хагас өргөнөөрөө (10px) дотогш байрладаг. */}
      <div aria-hidden className="text-muted-foreground relative h-4 text-xs tabular-nums">
        <span className="absolute left-0">{mn.billing.months(1)}</span>
        {marks
          .filter((item) => item.months < max)
          .map((item) => {
            const ratio = (item.months - 1) / (max - 1);
            return (
              <span
                key={item.months}
                className="absolute -translate-x-1/2"
                style={{ left: `calc(${ratio * 100}% + ${(1 - 2 * ratio) * 10}px)` }}
              >
                {mn.billing.months(item.months)}
              </span>
            );
          })}
        <span className="absolute right-0">{mn.billing.months(max)}</span>
      </div>

      <p className="flex flex-wrap items-center gap-x-2 gap-y-1 pt-1 text-sm" aria-live="polite">
        <span className="text-muted-foreground">{mn.billing.total}</span>
        <span className="font-semibold tabular-nums">{formatMnt(option.final_price_mnt)}</span>
        {option.final_price_mnt < regular && (
          <s className="text-muted-foreground tabular-nums">
            <span className="sr-only">{mn.billing.regularPrice}: </span>
            {formatMnt(regular)}
          </s>
        )}
        {option.free_months > 0 && (
          <Badge variant="secondary">{mn.billing.freeMonths(option.free_months)}</Badge>
        )}
        {percentOff > 0 && option.final_price_mnt < option.price_mnt && (
          <Badge variant="secondary">{mn.billing.discountBadge(percentOff)}</Badge>
        )}
        {option.credit_mnt > 0 && (
          <Badge variant="secondary">{mn.billing.creditBadge(formatMnt(option.credit_mnt))}</Badge>
        )}
      </p>
    </div>
  );
}
