"use client";

import { useQuery, useQueryClient } from "@tanstack/react-query";
import { CircleXIcon, HouseIcon, LoaderCircleIcon } from "lucide-react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";

import { ReceiptPrinter, type ReceiptPrinterStage } from "@/components/billing/receipt-printer";
import { ErrorState } from "@/components/common/states";
import { LogoMark } from "@/components/layout/logo";
import { Button } from "@/components/ui/button";
import { getPayment, getRedemption } from "@/lib/api/billing";
import { ApiError } from "@/lib/api/client";
import { recallReturnPath } from "@/lib/billing";
import { formatDate, formatMnt } from "@/lib/format";
import { useCurrentUser } from "@/lib/hooks/use-auth";
import { mn } from "@/lib/i18n/mn";
import { queryKeys } from "@/lib/query-keys";
import type { PaymentReceipt, PlanStatus } from "@/lib/types/api";
import { cn } from "@/lib/utils";

/** Банкны апп-аас баталгаажтал хэдэн секунд зарцуулагдана — 1 минут хүлээнэ. */
const POLL_MS = 3000;
const MAX_POLLS = 20;
/** Төлбөр шууд баталгаажсан ч «шалгаж байна» гэдгийг богино хугацаанд харуулна. */
const PROCESSING_MS = 900;
/** `globals.css`-ийн `receipt-feed-*` (1.75 сек) + бага зэрэг завсар. */
const PRINTING_MS = 1900;

const t = mn.billing.receipt;

/**
 * Төлбөр эсвэл үнэгүй сарын промо кодын дараах хуудас (`/billing/success`).
 *
 * - `?payment=…` — Wire-ийн төлбөрийн хуудаснаас буцна. URL-д ХЭЗЭЭ Ч
 *   итгэхгүй: сервер тухайн төлбөр энэ хэрэглэгчийнх эсэх, Wire дээр үнэхээр
 *   төлөгдсөн эсэхийг шалгаж байж багц сунгана. Шалгах зуур принтер
 *   «боловсруулж», амжилттай бол баримт хэвлэнэ. Цуцлагдсан, амжилтгүй, удаан
 *   хүлээгдсэн төлбөрт энгийн мэдэгдэл.
 * - `?redemption=…` — `/pricing` дээр үнэгүй сарын кодыг идэвхжүүлсний дараа:
 *   0₮-ийн баримт.
 */
export function PaymentSuccess() {
  const params = useSearchParams();
  const redemptionId = params.get("redemption");
  return redemptionId ? (
    <RedemptionSuccess redemptionId={redemptionId} />
  ) : (
    <PaymentFlow paymentId={params.get("payment")} />
  );
}

/** Багц идэвхжмэгц түгжээтэй хичээл, толгойн цэс зэрэг бүх зүйл шинэчлэгдэнэ. */
function useRefreshAfterGrant(granted: boolean) {
  const queryClient = useQueryClient();
  useEffect(() => {
    if (!granted) return;
    void queryClient.invalidateQueries({ queryKey: queryKeys.currentUser });
    void queryClient.invalidateQueries({ queryKey: queryKeys.billing.plan });
    void queryClient.invalidateQueries({ queryKey: queryKeys.courses.all });
    void queryClient.invalidateQueries({ queryKey: queryKeys.lessons.all });
    // Live-ийн эрх (багц эсвэл нэг удаагийн эрх) өөрчлөгдсөн.
    void queryClient.invalidateQueries({ queryKey: queryKeys.live.configAll });
    void queryClient.invalidateQueries({ queryKey: queryKeys.live.materials });
  }, [granted, queryClient]);
}

/** Принтерийн шат: `ready` болмогц богино «боловсруулж», «хэвлэж», «дууссан». */
function usePrinterStage(ready: boolean): ReceiptPrinterStage {
  const [stage, setStage] = useState<ReceiptPrinterStage>("processing");
  useEffect(() => {
    if (!ready) return;
    const toPrinting = setTimeout(() => setStage("printing"), PROCESSING_MS);
    const toComplete = setTimeout(() => setStage("complete"), PROCESSING_MS + PRINTING_MS);
    return () => {
      clearTimeout(toPrinting);
      clearTimeout(toComplete);
    };
  }, [ready]);
  return stage;
}

function RedemptionSuccess({ redemptionId }: { redemptionId: string }) {
  const query = useQuery({
    queryKey: queryKeys.billing.redemption(redemptionId),
    queryFn: () => getRedemption(redemptionId),
    retry: false,
  });
  const ready = Boolean(query.data);
  useRefreshAfterGrant(ready);
  const stage = usePrinterStage(ready);
  const [returnPath] = useState(recallReturnPath);

  if (query.isError) {
    const notFound = query.error instanceof ApiError && query.error.isNotFound;
    return (
      <ErrorState
        title={notFound ? t.missingRedemption : undefined}
        description={
          notFound
            ? mn.billing.return.missingBody
            : query.error instanceof ApiError
              ? query.error.message
              : mn.common.somethingWrong
        }
        onRetry={notFound ? undefined : () => void query.refetch()}
        className="mx-auto w-full max-w-md"
      />
    );
  }

  return (
    <ReceiptView
      stage={ready ? stage : "processing"}
      receipt={query.data?.receipt ?? null}
      plan={query.data?.plan ?? null}
      receiptId={redemptionId}
      returnPath={returnPath}
    />
  );
}

function PaymentFlow({ paymentId }: { paymentId: string | null }) {
  const query = useQuery({
    queryKey: queryKeys.billing.payment(paymentId ?? ""),
    queryFn: () => getPayment(paymentId ?? ""),
    enabled: Boolean(paymentId),
    retry: false,
    refetchInterval: (current) =>
      current.state.data?.status === "pending" && current.state.dataUpdateCount < MAX_POLLS
        ? POLL_MS
        : false,
  });

  const status = query.data?.status;
  const succeeded = status === "succeeded";
  useRefreshAfterGrant(succeeded);
  const stage = usePrinterStage(succeeded);

  // `RequireAuth` нэвтрэлт тодортол fallback харуулдаг тул энэ компонент
  // зөвхөн browser дээр render хийгдэнэ — `localStorage`-ийг шууд уншиж болно.
  const [returnPath] = useState(recallReturnPath);

  if (!paymentId || (query.isError && query.error instanceof ApiError && query.error.isNotFound)) {
    return (
      <ErrorState
        title={mn.billing.return.missing}
        description={mn.billing.return.missingBody}
        className="mx-auto w-full max-w-md"
      />
    );
  }

  if (query.isError) {
    return (
      <ErrorState
        description={
          query.error instanceof ApiError ? query.error.message : mn.common.somethingWrong
        }
        onRetry={() => void query.refetch()}
        className="mx-auto w-full max-w-md"
      />
    );
  }

  const polling = query.isPending || query.isFetching;
  const checking = !query.data || (status === "pending" && polling);

  if (checking || (succeeded && query.data?.receipt)) {
    return (
      <ReceiptView
        stage={checking ? "processing" : stage}
        receipt={query.data?.receipt ?? null}
        plan={query.data?.plan ?? null}
        receiptId={paymentId}
        returnPath={returnPath}
      />
    );
  }

  if (status === "pending") {
    return (
      <Panel icon={<LoaderCircleIcon className="text-muted-foreground size-10" aria-hidden />}>
        <h1 className="text-xl font-semibold">{mn.billing.return.pendingTitle}</h1>
        <p className="text-muted-foreground mt-2 text-sm">{mn.billing.return.pendingBody}</p>
        <Button className="mt-6" onClick={() => void query.refetch()}>
          {mn.billing.return.checkAgain}
        </Button>
      </Panel>
    );
  }

  return (
    <Panel icon={<CircleXIcon className="text-destructive size-10" aria-hidden />}>
      <h1 className="text-xl font-semibold">
        {status === "canceled" ? mn.billing.return.canceledTitle : mn.billing.return.failedTitle}
      </h1>
      <p className="text-muted-foreground mt-2 text-sm">{mn.billing.return.failedBody}</p>
      <Button asChild className="mt-6">
        <Link href={returnPath ? `/pricing?next=${encodeURIComponent(returnPath)}` : "/pricing"}>
          {mn.billing.return.tryAgain}
        </Link>
      </Button>
    </Panel>
  );
}

function ReceiptView({
  stage,
  receipt,
  plan,
  receiptId,
  returnPath,
}: {
  stage: ReceiptPrinterStage;
  receipt: PaymentReceipt | null;
  plan: PlanStatus | null;
  /** Төлбөр эсвэл промо кодын бичлэгийн id — баримтын дугаар, зураасан код. */
  receiptId: string;
  returnPath: string | null;
}) {
  const { user } = useCurrentUser();
  const complete = stage === "complete";
  // Нэг удаагийн эрх багцыг сунгахгүй — «… хүртэл идэвхтэй» гэж бичихгүй.
  const livePass = receipt?.plan === "live_pass";
  const expires = livePass ? null : (plan?.plan_expires_at ?? null);
  const accessDays = plan?.live_pass_access_days ?? null;

  return (
    <div className="flex flex-col items-center">
      <h1 className="sr-only">{t.pageTitle}</h1>

      <ReceiptPrinter.Root stage={stage}>
        <ReceiptPrinter.Machine>
          <ReceiptPrinter.Header>
            <LogoMark className="h-7" />
            <Button
              asChild
              size="sm"
              variant="outline"
              className="border-zinc-600 bg-zinc-900/60 text-zinc-100 hover:bg-zinc-900 hover:text-white"
            >
              <Link href="/dashboard">
                <HouseIcon className="size-3.5" aria-hidden />
                {t.home}
              </Link>
            </Button>
          </ReceiptPrinter.Header>

          <ReceiptPrinter.Screen>
            <div className="space-y-4">
              <div className="flex items-start justify-between gap-3 text-sm">
                <div className="min-w-0">
                  <p className="font-medium">{receipt ? planName(receipt) : t.plan}</p>
                  <p className="text-xs text-zinc-400">
                    {receipt ? periodText(receipt, accessDays) : "…"}
                  </p>
                </div>
                <strong className="font-mono tabular-nums">
                  {receipt ? formatMnt(receipt.amount_mnt) : "—"}
                </strong>
              </div>
              <ReceiptPrinter.Status />
            </div>
          </ReceiptPrinter.Screen>
        </ReceiptPrinter.Machine>

        {receipt && (
          <ReceiptPrinter.Output>
            <ReceiptPrinter.Paper>
              <ReceiptBody
                receipt={receipt}
                receiptId={receiptId}
                customer={user?.name ?? null}
                expires={expires}
                accessDays={accessDays}
              />
            </ReceiptPrinter.Paper>
          </ReceiptPrinter.Output>
        )}
      </ReceiptPrinter.Root>

      {/* Баримт бүрэн гарсны дараа л үйлдлийн товч — хэвлэлтэд саад болохгүй. */}
      <div
        className={cn(
          "mt-6 flex flex-col items-center text-center transition-opacity duration-300",
          complete ? "opacity-100" : "pointer-events-none opacity-0",
        )}
        aria-hidden={!complete}
        inert={!complete}
      >
        <p className="text-lg font-semibold">
          {receipt?.kind === "promo"
            ? t.giftTitle(receipt.months)
            : livePass
              ? mn.billing.return.passSuccessTitle
              : receipt?.plan === "premium"
                ? mn.billing.return.premiumSuccessTitle
                : mn.billing.return.successTitle}
        </p>
        {expires && (
          <p className="text-muted-foreground mt-1 text-sm">
            {mn.billing.return.successBody(formatDate(expires))}
          </p>
        )}
        {livePass && (
          <p className="text-muted-foreground mt-1 max-w-md text-sm text-pretty">
            {mn.billing.return.passSuccessBody}
            {plan?.upgrade_credit &&
              ` ${mn.billing.passCreditNote(
                formatMnt(plan.upgrade_credit.amount_mnt),
                formatDate(plan.upgrade_credit.expires_at),
              )}`}
          </p>
        )}
        <div className="mt-5 flex flex-wrap justify-center gap-3">
          {livePass ? (
            <Button asChild>
              <Link href="/live">{mn.billing.return.goLive}</Link>
            </Button>
          ) : (
            returnPath && (
              <Button asChild>
                <Link href={returnPath}>{mn.billing.return.continueLesson}</Link>
              </Button>
            )
          )}
          <Button asChild variant={livePass || returnPath ? "outline" : "default"}>
            <Link href="/dashboard">{mn.billing.return.goDashboard}</Link>
          </Button>
        </div>
      </div>
    </div>
  );
}

function planName(receipt: PaymentReceipt): string {
  if (receipt.plan === "live_pass") return t.planLivePass;
  return receipt.plan === "premium" ? t.planPremium : t.plan;
}

/** Үнэгүй сарын кодод — нэмэгдсэн сар; эрхэд — нэг материал; багцад — хугацаа. */
function periodText(receipt: PaymentReceipt, accessDays: number | null): string {
  if (receipt.kind === "promo") return t.gift(receipt.months);
  if (receipt.plan === "live_pass") return t.passPeriod(accessDays);
  return t.period(receipt.months, receipt.free_months);
}

/** `2026.09.30 14:05` — хэрэглэгчийн цагийн бүсээр. */
function formatStamp(iso: string): string {
  const date = new Date(iso);
  const pad = (value: number) => String(value).padStart(2, "0");
  return `${date.getFullYear()}.${pad(date.getMonth() + 1)}.${pad(date.getDate())} ${pad(
    date.getHours(),
  )}:${pad(date.getMinutes())}`;
}

function ReceiptBody({
  receipt,
  receiptId,
  customer,
  expires,
  accessDays,
}: {
  receipt: PaymentReceipt;
  receiptId: string;
  customer: string | null;
  expires: string | null;
  accessDays: number | null;
}) {
  const number = receiptId.replace(/-/g, "").slice(0, 8).toUpperCase();
  const discountLabel =
    receipt.discount_source === "promo" && receipt.promo_code
      ? t.discountPromo(receipt.discount_percent, receipt.promo_code)
      : receipt.discount_source === "referral"
        ? t.discountReferral(receipt.discount_percent)
        : t.discount(receipt.discount_percent);

  return (
    <div className="space-y-4 text-[13px] leading-relaxed">
      <header className="text-center">
        <p className="text-base font-bold tracking-[0.2em]">MEDLEGHUB</p>
        <p className="text-xs text-zinc-500">medleghub.com</p>
        <h2 className="mt-2 text-sm font-semibold">{t.title}</h2>
      </header>

      <Rule />

      <dl className="space-y-1">
        <Line label={t.number} value={number} />
        <Line label={t.date} value={formatStamp(receipt.paid_at ?? receipt.created_at)} />
        {customer && <Line label={t.customer} value={customer} />}
      </dl>

      <Rule />

      <dl className="space-y-1">
        <div>
          <dt className="font-semibold">{planName(receipt)}</dt>
          <dd className="flex justify-between gap-3">
            {/* Үнэгүй сарын кодод үнэ байхгүй — хэдэн сар нэмэгдсэн нь л. */}
            <span>{periodText(receipt, accessDays)}</span>
            <span className="tabular-nums">{formatMnt(receipt.list_price_mnt)}</span>
          </dd>
        </div>
        {receipt.kind === "promo" && receipt.promo_code && (
          <Line label={t.promoCode(receipt.promo_code)} value={t.gift(receipt.months)} />
        )}
        {receipt.discount_mnt > 0 && (
          <Line label={discountLabel} value={`−${formatMnt(receipt.discount_mnt)}`} money />
        )}
        {receipt.credit_mnt > 0 && (
          <Line label={t.passCredit} value={`−${formatMnt(receipt.credit_mnt)}`} money />
        )}
      </dl>

      <Rule />

      <dl>
        <Line
          label={t.total}
          value={formatMnt(receipt.amount_mnt)}
          className="text-base font-bold"
          money
        />
      </dl>

      <Rule />

      <dl className="space-y-1 text-xs">
        {expires && <Line label={t.activeUntil} value={t.until(formatDate(expires))} />}
        {receipt.plan === "live_pass" && <Line label={t.passValid} value={t.passValidValue} />}
        {receipt.reference && <Line label={t.reference} value={receipt.reference} breakValue />}
      </dl>

      <p className="pt-1 text-center text-xs">{t.thanks}</p>
      <Barcode seed={receiptId} />
    </div>
  );
}

function Line({
  label,
  value,
  className,
  money = false,
  breakValue = false,
}: {
  label: string;
  value: string;
  className?: string;
  /** Дүн — хэзээ ч таслагдахгүй, урт шошго («Хөнгөлөлт 20% (КОД)») мөр шилжинэ. */
  money?: boolean;
  /** Гүйлгээний урт дугаар — тэмдэгтээр тасарна. */
  breakValue?: boolean;
}) {
  // Энгийн мөрөнд богино шошго бүтэн үлдэж, утга (огноо, нэр) мөр шилжинэ.
  return (
    <div className={cn("flex justify-between gap-3", className)}>
      <dt className={money ? "min-w-0" : "shrink-0"}>{label}</dt>
      <dd
        className={cn(
          "min-w-0 text-right tabular-nums",
          money && "shrink-0 whitespace-nowrap",
          breakValue && "break-all",
        )}
      >
        {value}
      </dd>
    </div>
  );
}

function Rule() {
  return <hr className="border-t border-dashed border-zinc-400" />;
}

/** Чимэглэлийн зураасан код — төлбөрийн id-аас тогтвортой үүснэ. */
function Barcode({ seed }: { seed: string }) {
  const digits = seed.replace(/[^0-9a-f]/gi, "");
  const bars = Array.from({ length: 36 }, (_, index) => {
    const value = parseInt(digits[index % digits.length] ?? "0", 16);
    return { width: 1 + (value % 3), gap: 1 + ((value >> 2) % 2) };
  });
  return (
    <div aria-hidden className="flex h-10 items-stretch justify-center pt-2">
      {bars.map((bar, index) => (
        <span
          key={index}
          className="bg-zinc-900"
          style={{ width: `${bar.width}px`, marginRight: `${bar.gap}px` }}
        />
      ))}
    </div>
  );
}

function Panel({ icon, children }: { icon: React.ReactNode; children: React.ReactNode }) {
  return (
    <div
      role="status"
      className="bg-card mx-auto flex max-w-md flex-col items-center rounded-xl border p-8 text-center"
    >
      {icon}
      <div className="mt-4">{children}</div>
    </div>
  );
}
