"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useEffect } from "react";
import { useForm, useWatch } from "react-hook-form";
import { toast } from "sonner";

import { FormField } from "@/components/auth/form-field";
import { ErrorState } from "@/components/common/states";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { getPlanPrice, setPlanPrice } from "@/lib/api/billing";
import { ApiError } from "@/lib/api/client";
import { formatDate, formatMnt } from "@/lib/format";
import { mn } from "@/lib/i18n/mn";
import { queryKeys } from "@/lib/query-keys";
import type { BillingPlan } from "@/lib/types/api";
import { planPriceSchema, type PlanPriceValues } from "@/lib/validation/admin";

/** Олон сарын үнийн дүрэм серверийнхтэй ижил — зөвхөн урьдчилан харуулахад. */
const FREE_MONTH_EVERY = 6;

function total(monthly: number, months: number): string {
  return formatMnt(monthly * (months - Math.floor(months / FREE_MONTH_EVERY)));
}

/**
 * Standard эсвэл Premium багцын сарын үнэ, эсвэл нэг удаагийн Live эрхийн үнэ.
 * Хадгалсны дараа `/pricing` болон шинэ нэхэмжлэх шинэ үнээр — аль хэдийн үүссэн
 * нэхэмжлэхийн дүн өөрчлөгдөхгүй.
 */
export function PlanPriceForm({ plan = "standard" }: { plan?: BillingPlan }) {
  const premium = plan === "premium";
  const livePass = plan === "live_pass";
  const fieldId = `price_mnt_${plan}`;
  const queryClient = useQueryClient();
  const query = useQuery({ queryKey: queryKeys.admin.planPrice, queryFn: getPlanPrice });

  const form = useForm<PlanPriceValues>({
    resolver: zodResolver(planPriceSchema),
    defaultValues: { price_mnt: 0 },
  });
  const current = livePass
    ? query.data?.live_pass_price_mnt
    : premium
      ? query.data?.premium_price_mnt
      : query.data?.price_mnt;
  useEffect(() => {
    if (current !== undefined) form.reset({ price_mnt: current });
  }, [current, form]);

  const draft = useWatch({ control: form.control, name: "price_mnt" });

  const save = useMutation({
    mutationFn: (values: PlanPriceValues) => setPlanPrice(values.price_mnt, plan),
    onSuccess: (info) => {
      queryClient.setQueryData(queryKeys.admin.planPrice, info);
      void queryClient.invalidateQueries({ queryKey: queryKeys.billing.plan });
      toast.success(livePass ? mn.admin.priceLivePassSaved : mn.admin.priceSaved);
    },
    onError: (error) =>
      toast.error(error instanceof ApiError ? error.message : mn.common.somethingWrong),
  });

  if (query.isPending) return <Skeleton className="h-64 w-full max-w-xl rounded-xl" />;
  if (query.isError) return <ErrorState onRetry={() => void query.refetch()} />;

  const info = query.data;
  const changedAt = livePass
    ? info.live_pass_changed_at
    : premium
      ? info.premium_changed_at
      : info.changed_at;
  const changedBy = livePass
    ? info.live_pass_changed_by
    : premium
      ? info.premium_changed_by
      : info.changed_by;
  const price = livePass
    ? info.live_pass_price_mnt
    : premium
      ? info.premium_price_mnt
      : info.price_mnt;
  const changedNote = changedAt
    ? changedBy
      ? mn.admin.priceChanged(changedBy, formatDate(changedAt))
      : mn.admin.priceChangedUnknown(formatDate(changedAt))
    : mn.admin.priceDefault;
  const validDraft = Number.isInteger(draft) && draft >= 100;

  return (
    <Card className="max-w-xl">
      <CardContent className="space-y-6">
        <div>
          <h2 className="text-lg font-semibold tracking-tight">
            {livePass
              ? mn.admin.priceLivePassTitle
              : premium
                ? mn.admin.pricePremiumTitle
                : mn.admin.priceStandardTitle}
          </h2>
          {(premium || livePass) && (
            <p className="text-muted-foreground mt-1 text-sm">
              {livePass ? mn.admin.priceLivePassHint : mn.admin.pricePremiumHint}
            </p>
          )}
          <p className="text-muted-foreground mt-4 text-sm">
            {livePass ? mn.admin.priceLivePassCurrent : mn.admin.priceCurrent}
          </p>
          <p className="text-3xl font-bold tracking-tight">{formatMnt(price)}</p>
          <p className="text-muted-foreground mt-1 text-xs">{changedNote}</p>
        </div>

        <form
          onSubmit={form.handleSubmit((values) => save.mutate(values))}
          noValidate
          className="space-y-4"
        >
          <FormField
            id={fieldId}
            type="number"
            inputMode="numeric"
            min={100}
            max={1_000_000}
            step={100}
            label={livePass ? mn.admin.priceLivePassLabel : mn.admin.priceLabel}
            hint={livePass ? mn.admin.priceLivePassFieldHint : mn.admin.priceHint}
            error={form.formState.errors.price_mnt?.message}
            {...form.register("price_mnt", { valueAsNumber: true })}
          />
          {validDraft && !livePass && (
            <p className="text-muted-foreground text-sm" aria-live="polite">
              {mn.admin.pricePreview(total(draft, 6), total(draft, 12))}
            </p>
          )}
          <Button type="submit" disabled={save.isPending || !form.formState.isDirty}>
            {save.isPending ? mn.admin.saving : mn.admin.save}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}
