"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation } from "@tanstack/react-query";
import { MinusIcon, PlusIcon, SearchIcon } from "lucide-react";
import { useState } from "react";
import { useForm, useWatch } from "react-hook-form";
import { toast } from "sonner";

import { FormField } from "@/components/auth/form-field";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { adjustUserPlan, lookupUserPlan } from "@/lib/api/billing";
import { ApiError } from "@/lib/api/client";
import { addMonths, daysLeft, formatDate } from "@/lib/format";
import { mn } from "@/lib/i18n/mn";
import type { AdminUserPlan, PlanAdjustment } from "@/lib/types/api";
import {
  userPlanAdjustSchema,
  userPlanLookupSchema,
  type UserPlanAdjustValues,
  type UserPlanLookupValues,
} from "@/lib/validation/admin";

function errorMessage(error: unknown): string {
  return error instanceof ApiError ? error.message : mn.common.somethingWrong;
}

/**
 * Хэрэглэгчийн Standard багцыг гараар нэмэх, хасах (`POST /billing/grants`).
 *
 * Эрхийг сервер шалгана — энэ хуудас зөвхөн админд нээгддэг ч API нь өөрөө
 * админаас бусдад 403 буцаана.
 */
export function UserPlanForm() {
  const [plan, setPlan] = useState<AdminUserPlan | null>(null);

  const form = useForm<UserPlanLookupValues>({
    resolver: zodResolver(userPlanLookupSchema),
    defaultValues: { email: "" },
  });

  const lookup = useMutation({
    mutationFn: (values: UserPlanLookupValues) => lookupUserPlan(values.email),
    onSuccess: setPlan,
    onError: (error) => {
      setPlan(null);
      if (error instanceof ApiError && error.status === 404) {
        form.setError("email", { message: mn.admin.userPlanNotFound });
      } else {
        toast.error(errorMessage(error));
      }
    },
  });

  return (
    <Card className="max-w-xl">
      <CardContent className="space-y-6">
        <div>
          <h2 className="text-lg font-semibold tracking-tight">{mn.admin.userPlanTitle}</h2>
          <p className="text-muted-foreground mt-1 text-sm">{mn.admin.userPlanHint}</p>
        </div>

        <form
          onSubmit={form.handleSubmit((values) => lookup.mutate(values))}
          noValidate
          className="space-y-4"
        >
          <FormField
            id="user-plan-email"
            type="email"
            autoComplete="off"
            label={mn.admin.userPlanEmail}
            error={form.formState.errors.email?.message}
            {...form.register("email")}
          />
          <Button type="submit" disabled={lookup.isPending}>
            <SearchIcon className="size-4" />
            {lookup.isPending ? mn.admin.userPlanSearching : mn.admin.userPlanSearch}
          </Button>
        </form>

        {plan && <UserPlanPanel key={plan.user_id} plan={plan} onChange={setPlan} />}
      </CardContent>
    </Card>
  );
}

function planStatus(plan: AdminUserPlan): string {
  if (plan.plan_expires_at && daysLeft(plan.plan_expires_at) > 0) {
    return mn.admin.userPlanActive(
      formatDate(plan.plan_expires_at),
      daysLeft(plan.plan_expires_at),
    );
  }
  // Админ үргэлж эрхтэй — дуусах хугацаагүй байж болно.
  if (plan.has_plan) return mn.admin.userPlanAlways;
  if (plan.plan_expires_at) return mn.admin.userPlanExpired(formatDate(plan.plan_expires_at));
  return mn.admin.userPlanFree;
}

function UserPlanPanel({
  plan,
  onChange,
}: {
  plan: AdminUserPlan;
  onChange: (plan: AdminUserPlan) => void;
}) {
  // Хасахыг баталгаажуулах цонх нээлттэй үед шалгагдсан утгууд.
  const [pendingRemove, setPendingRemove] = useState<UserPlanAdjustValues | null>(null);

  const form = useForm<UserPlanAdjustValues>({
    resolver: zodResolver(userPlanAdjustSchema),
    defaultValues: { months: 1, note: "" },
  });
  const months = useWatch({ control: form.control, name: "months" });
  const validMonths = Number.isInteger(months) && months >= 1 && months <= 24;

  const expiresAt = plan.plan_expires_at ? new Date(plan.plan_expires_at) : null;
  const active = plan.plan_expires_at !== null && daysLeft(plan.plan_expires_at) > 0;

  // Серверийнхтэй ижил дүрэм — зөвхөн урьдчилан харуулахад.
  const now = new Date();
  const addBase = expiresAt && expiresAt > now ? expiresAt : now;
  const afterAdd = validMonths ? addMonths(addBase, months) : null;
  const afterRemove = validMonths && active && expiresAt ? addMonths(expiresAt, -months) : null;
  const removeEndsNow = afterRemove !== null && afterRemove <= now;

  const adjust = useMutation({
    mutationFn: ({ delta, note }: { delta: number; note: string }) =>
      adjustUserPlan(plan.email, delta, note || null),
    onSuccess: (updated) => {
      onChange(updated);
      form.reset({ months: 1, note: "" });
      toast.success(mn.admin.userPlanSaved);
    },
    onError: (error) => toast.error(errorMessage(error)),
  });

  return (
    <div className="space-y-6 border-t pt-6">
      <div>
        <p className="font-medium">{plan.name}</p>
        <p className="text-muted-foreground text-sm">{plan.email}</p>
        <p
          id="user-plan-status"
          className="text-brand-link mt-1 text-sm font-medium"
          aria-live="polite"
        >
          {planStatus(plan)}
        </p>
      </div>

      <form
        onSubmit={form.handleSubmit((values) =>
          adjust.mutate({ delta: values.months, note: values.note }),
        )}
        noValidate
        className="space-y-4"
      >
        <FormField
          id="user-plan-months"
          type="number"
          inputMode="numeric"
          min={1}
          max={24}
          step={1}
          label={mn.admin.userPlanMonths}
          hint={mn.admin.userPlanMonthsHint}
          error={form.formState.errors.months?.message}
          {...form.register("months", { valueAsNumber: true })}
        />

        <div className="space-y-2">
          <Label htmlFor="user-plan-note">{mn.admin.userPlanNote}</Label>
          <Textarea
            id="user-plan-note"
            rows={2}
            maxLength={500}
            aria-describedby="user-plan-note-hint"
            aria-invalid={form.formState.errors.note ? true : undefined}
            {...form.register("note")}
          />
          <p id="user-plan-note-hint" className="text-muted-foreground text-xs">
            {mn.admin.userPlanNoteHint}
          </p>
          {form.formState.errors.note && (
            <p role="alert" className="text-destructive text-xs">
              {form.formState.errors.note.message}
            </p>
          )}
        </div>

        {afterAdd && (
          <div className="text-muted-foreground space-y-0.5 text-sm" aria-live="polite">
            <p>{mn.admin.userPlanPreviewAdd(formatDate(afterAdd.toISOString()))}</p>
            {afterRemove && (
              <p>
                {removeEndsNow
                  ? mn.admin.userPlanPreviewRemoveEnds
                  : mn.admin.userPlanPreviewRemove(formatDate(afterRemove.toISOString()))}
              </p>
            )}
          </div>
        )}

        <div className="flex flex-wrap items-center gap-2">
          <Button type="submit" disabled={adjust.isPending}>
            <PlusIcon className="size-4" />
            {mn.admin.userPlanAdd(validMonths ? months : 1)}
          </Button>
          <Button
            type="button"
            variant="outline"
            disabled={adjust.isPending || !active}
            onClick={() => void form.handleSubmit(setPendingRemove)()}
          >
            <MinusIcon className="size-4" />
            {mn.admin.userPlanRemove(validMonths ? months : 1)}
          </Button>
        </div>
        {!active && <p className="text-muted-foreground text-xs">{mn.admin.userPlanNoActive}</p>}
      </form>

      <Dialog
        open={pendingRemove !== null}
        onOpenChange={(open) => {
          if (!open) setPendingRemove(null);
        }}
      >
        {pendingRemove && (
          <DialogContent>
            <DialogHeader>
              <DialogTitle>{mn.admin.userPlanRemoveConfirm(pendingRemove.months)}</DialogTitle>
              <DialogDescription>
                {mn.admin.userPlanRemoveDescription(
                  plan.name,
                  afterRemove && !removeEndsNow ? formatDate(afterRemove.toISOString()) : null,
                )}
              </DialogDescription>
            </DialogHeader>
            <DialogFooter>
              <Button variant="outline" onClick={() => setPendingRemove(null)}>
                {mn.admin.cancel}
              </Button>
              <Button
                variant="destructive"
                disabled={adjust.isPending}
                onClick={() => {
                  setPendingRemove(null);
                  adjust.mutate({ delta: -pendingRemove.months, note: pendingRemove.note });
                }}
              >
                {mn.admin.userPlanRemove(pendingRemove.months)}
              </Button>
            </DialogFooter>
          </DialogContent>
        )}
      </Dialog>

      <AdjustmentHistory items={plan.adjustments} />
    </div>
  );
}

function AdjustmentHistory({ items }: { items: PlanAdjustment[] }) {
  return (
    <section aria-labelledby="user-plan-history" className="space-y-3">
      <h3 id="user-plan-history" className="text-sm font-semibold">
        {mn.admin.userPlanHistory}
      </h3>
      {items.length === 0 ? (
        <p className="text-muted-foreground text-sm">{mn.admin.userPlanHistoryEmpty}</p>
      ) : (
        <ul className="divide-y rounded-lg border">
          {items.map((item) => (
            <li key={item.id} className="space-y-1 p-3 text-sm">
              <div className="flex flex-wrap items-center gap-2">
                <Badge variant={item.months > 0 ? "secondary" : "outline"}>
                  {mn.admin.userPlanDelta(item.months)}
                </Badge>
                <span className="text-muted-foreground text-xs">
                  {mn.admin.userPlanBy(
                    item.admin_name ?? mn.admin.userPlanDeletedAdmin,
                    formatDate(item.created_at),
                  )}
                </span>
              </div>
              <p className="text-xs tabular-nums">
                {mn.admin.userPlanChange(
                  item.expires_before ? formatDate(item.expires_before) : mn.admin.userPlanNone,
                  formatDate(item.expires_after),
                )}
              </p>
              {item.note && <p className="text-muted-foreground text-xs">{item.note}</p>}
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
