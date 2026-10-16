"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { CheckIcon, CopyIcon, PencilIcon, PowerIcon, TicketPercentIcon } from "lucide-react";
import { useState } from "react";
import { useForm, useWatch, type UseFormRegisterReturn } from "react-hook-form";
import { toast } from "sonner";

import { FormField } from "@/components/auth/form-field";
import { EmptyState, ErrorState } from "@/components/common/states";
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
import { Skeleton } from "@/components/ui/skeleton";
import { Textarea } from "@/components/ui/textarea";
import { createPromoCode, listPromoCodes, updatePromoCode } from "@/lib/api/billing";
import { ApiError } from "@/lib/api/client";
import { formatDate } from "@/lib/format";
import { mn } from "@/lib/i18n/mn";
import { queryKeys } from "@/lib/query-keys";
import type { PromoCodeItem } from "@/lib/types/api";
import { cn } from "@/lib/utils";
import {
  endOfUlaanbaatarDay,
  normalizePromoCode,
  optionalInt,
  promoCodeEditSchema,
  promoCodeSchema,
  todayInUlaanbaatar,
  ulaanbaatarDate,
  type PromoCodeEditValues,
  type PromoCodeValues,
} from "@/lib/validation/admin";

function errorMessage(error: unknown): string {
  return error instanceof ApiError ? error.message : mn.common.somethingWrong;
}

const EMPTY: PromoCodeValues = {
  code: "",
  kind: "percent",
  percent_off: "",
  free_months: "",
  expires_on: "",
  max_uses: "",
  note: "",
};

/**
 * Промо код үүсгэх, жагсаалт. Хувийн код — хэрэглэгч `/pricing` дээр оруулж
 * хөнгөлөлттэй төлнө; үнэгүй сарын код — идэвхжүүлэхэд багц шууд сунгагдана.
 * Эрхийг сервер шалгана.
 */
export function PromoCodes() {
  return (
    <div className="space-y-8">
      <PromoCodeForm />
      <PromoCodeList />
    </div>
  );
}

function PromoCodeForm() {
  const queryClient = useQueryClient();
  const form = useForm<PromoCodeValues>({
    resolver: zodResolver(promoCodeSchema),
    defaultValues: EMPTY,
  });
  const kind = useWatch({ control: form.control, name: "kind" });
  const errors = form.formState.errors;

  const create = useMutation({
    mutationFn: (values: PromoCodeValues) =>
      createPromoCode({
        code: normalizePromoCode(values.code) || null,
        kind: values.kind,
        percent_off: values.kind === "percent" ? optionalInt(values.percent_off) : null,
        free_months: values.kind === "free_months" ? optionalInt(values.free_months) : null,
        expires_at: values.expires_on ? endOfUlaanbaatarDay(values.expires_on) : null,
        max_uses: optionalInt(values.max_uses),
        note: values.note || null,
      }),
    onSuccess: (created) => {
      queryClient.setQueryData<PromoCodeItem[]>(queryKeys.admin.promoCodes, (items) =>
        items ? [created, ...items] : [created],
      );
      form.reset(EMPTY);
      toast.success(mn.admin.promoCreated(created.code));
    },
    onError: (error) => {
      if (error instanceof ApiError && error.code === "PROMO_CODE_TAKEN") {
        form.setError("code", { message: error.message }, { shouldFocus: true });
      } else {
        toast.error(errorMessage(error));
      }
    },
  });

  return (
    <Card className="max-w-xl">
      <CardContent className="space-y-6">
        <h2 className="text-lg font-semibold tracking-tight">{mn.admin.promoCreateTitle}</h2>

        <form
          onSubmit={form.handleSubmit((values) => create.mutate(values))}
          noValidate
          className="space-y-4"
        >
          <FormField
            id="promo-code"
            label={mn.admin.promoCode}
            hint={mn.admin.promoCodeHint}
            autoComplete="off"
            autoCapitalize="characters"
            spellCheck={false}
            placeholder="HELLOWORLD2026"
            className="font-mono uppercase"
            error={errors.code?.message}
            {...form.register("code")}
          />

          <fieldset className="space-y-2">
            <legend className="text-sm font-medium">{mn.admin.promoKind}</legend>
            <div className="flex flex-wrap gap-2">
              {(
                [
                  ["percent", mn.admin.promoKindPercent],
                  ["free_months", mn.admin.promoKindFreeMonths],
                ] as const
              ).map(([value, label]) => (
                <label
                  key={value}
                  className={cn(
                    "flex cursor-pointer items-center gap-2 rounded-md border px-3 py-2 text-sm",
                    "has-[:focus-visible]:ring-ring/50 has-[:focus-visible]:ring-[3px]",
                    kind === value && "border-primary bg-accent",
                  )}
                >
                  <input
                    type="radio"
                    value={value}
                    className="accent-primary size-4"
                    {...form.register("kind")}
                  />
                  {label}
                </label>
              ))}
            </div>
          </fieldset>

          {kind === "percent" ? (
            <FormField
              key="percent"
              id="promo-percent"
              type="number"
              inputMode="numeric"
              min={1}
              max={99}
              step={1}
              label={mn.admin.promoPercent}
              hint={mn.admin.promoPercentHint}
              error={errors.percent_off?.message}
              {...form.register("percent_off")}
            />
          ) : (
            <FormField
              key="months"
              id="promo-months"
              type="number"
              inputMode="numeric"
              min={1}
              max={12}
              step={1}
              label={mn.admin.promoFreeMonths}
              hint={mn.admin.promoFreeMonthsHint}
              error={errors.free_months?.message}
              {...form.register("free_months")}
            />
          )}

          <FormField
            id="promo-expires"
            type="date"
            min={todayInUlaanbaatar()}
            label={mn.admin.promoExpires}
            hint={mn.admin.promoExpiresHint}
            error={errors.expires_on?.message}
            {...form.register("expires_on")}
          />

          <FormField
            id="promo-max-uses"
            type="number"
            inputMode="numeric"
            min={1}
            step={1}
            label={mn.admin.promoMaxUses}
            hint={mn.admin.promoMaxUsesHint}
            error={errors.max_uses?.message}
            {...form.register("max_uses")}
          />

          <NoteField
            id="promo-note"
            error={errors.note?.message}
            registration={form.register("note")}
          />

          <Button type="submit" disabled={create.isPending}>
            {create.isPending ? mn.admin.promoCreating : mn.admin.promoCreate}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}

function NoteField({
  id,
  error,
  registration,
}: {
  id: string;
  error?: string;
  registration: UseFormRegisterReturn<"note">;
}) {
  return (
    <div className="space-y-2">
      <Label htmlFor={id}>{mn.admin.promoNote}</Label>
      <Textarea
        id={id}
        rows={2}
        maxLength={500}
        aria-describedby={`${id}-hint`}
        aria-invalid={error ? true : undefined}
        {...registration}
      />
      <p id={`${id}-hint`} className="text-muted-foreground text-xs">
        {mn.admin.promoNoteHint}
      </p>
      {error && (
        <p role="alert" className="text-destructive text-xs">
          {error}
        </p>
      )}
    </div>
  );
}

function PromoCodeList() {
  const queryClient = useQueryClient();
  const query = useQuery({ queryKey: queryKeys.admin.promoCodes, queryFn: listPromoCodes });
  const [editing, setEditing] = useState<PromoCodeItem | null>(null);

  const replace = (updated: PromoCodeItem) =>
    queryClient.setQueryData<PromoCodeItem[]>(queryKeys.admin.promoCodes, (items) =>
      items?.map((item) => (item.id === updated.id ? updated : item)),
    );

  const toggle = useMutation({
    mutationFn: (item: PromoCodeItem) => updatePromoCode(item.id, { active: !item.active }),
    onSuccess: (updated) => {
      replace(updated);
      toast.success(mn.admin.promoSaved);
    },
    onError: (error) => toast.error(errorMessage(error)),
  });

  return (
    <section aria-labelledby="promo-list-title" className="space-y-4">
      <h2 id="promo-list-title" className="text-lg font-semibold tracking-tight">
        {mn.admin.promoListTitle}
      </h2>

      {query.isPending ? (
        <div className="space-y-3">
          {Array.from({ length: 3 }, (_, index) => (
            <Skeleton key={index} className="h-24 w-full" />
          ))}
        </div>
      ) : query.isError ? (
        <ErrorState onRetry={() => void query.refetch()} />
      ) : query.data.length === 0 ? (
        <EmptyState icon={TicketPercentIcon} title={mn.admin.promoEmpty} />
      ) : (
        <ul className="divide-y rounded-xl border">
          {query.data.map((item) => (
            <li key={item.id} className="space-y-2 p-4">
              <div className="flex flex-wrap items-center gap-2">
                <span className="font-mono text-base font-semibold tracking-wide">{item.code}</span>
                <CopyCodeButton code={item.code} />
                <Badge
                  variant="outline"
                  className={cn(item.status !== "active" && "text-muted-foreground")}
                >
                  {mn.admin.promoStatus[item.status]}
                </Badge>
                <Badge variant="secondary">
                  {item.kind === "percent"
                    ? mn.admin.promoValuePercent(item.percent_off ?? 0)
                    : mn.admin.promoValueMonths(item.free_months ?? 0)}
                </Badge>
              </div>

              <p className="text-muted-foreground flex flex-wrap gap-x-3 gap-y-1 text-xs">
                <span className="text-foreground font-medium tabular-nums">
                  {mn.admin.promoUses(item.uses, item.max_uses)}
                </span>
                <span>
                  {item.expires_at
                    ? mn.admin.promoUntil(formatDate(item.expires_at))
                    : mn.admin.promoNoExpiry}
                </span>
                <span>
                  {item.created_by
                    ? mn.admin.promoBy(item.created_by, formatDate(item.created_at))
                    : formatDate(item.created_at)}
                </span>
              </p>
              {item.note && <p className="text-muted-foreground text-sm">{item.note}</p>}

              <div className="flex flex-wrap gap-2 pt-1">
                <Button size="sm" variant="outline" onClick={() => setEditing(item)}>
                  <PencilIcon className="size-4" />
                  {mn.admin.promoEdit}
                </Button>
                <Button
                  size="sm"
                  variant="outline"
                  disabled={toggle.isPending && toggle.variables?.id === item.id}
                  onClick={() => toggle.mutate(item)}
                >
                  <PowerIcon className="size-4" />
                  {item.active ? mn.admin.promoDisable : mn.admin.promoEnable}
                </Button>
              </div>
            </li>
          ))}
        </ul>
      )}

      <Dialog
        open={editing !== null}
        onOpenChange={(open) => {
          if (!open) setEditing(null);
        }}
      >
        {editing && (
          <EditPromoDialog
            key={editing.id}
            item={editing}
            onSaved={(updated) => {
              replace(updated);
              setEditing(null);
              toast.success(mn.admin.promoSaved);
            }}
            onCancel={() => setEditing(null)}
          />
        )}
      </Dialog>
    </section>
  );
}

function EditPromoDialog({
  item,
  onSaved,
  onCancel,
}: {
  item: PromoCodeItem;
  onSaved: (item: PromoCodeItem) => void;
  onCancel: () => void;
}) {
  const form = useForm<PromoCodeEditValues>({
    resolver: zodResolver(promoCodeEditSchema),
    defaultValues: {
      expires_on: item.expires_at ? ulaanbaatarDate(item.expires_at) : "",
      max_uses: item.max_uses === null ? "" : String(item.max_uses),
      note: item.note ?? "",
    },
  });
  const errors = form.formState.errors;

  const save = useMutation({
    mutationFn: (values: PromoCodeEditValues) =>
      updatePromoCode(item.id, {
        expires_at: values.expires_on ? endOfUlaanbaatarDay(values.expires_on) : null,
        max_uses: optionalInt(values.max_uses),
        note: values.note || null,
      }),
    onSuccess: onSaved,
    onError: (error) => toast.error(errorMessage(error)),
  });

  return (
    <DialogContent>
      <DialogHeader>
        <DialogTitle>{mn.admin.promoEditTitle(item.code)}</DialogTitle>
        <DialogDescription>{mn.admin.promoEditDescription}</DialogDescription>
      </DialogHeader>
      <form
        id="promo-edit-form"
        onSubmit={form.handleSubmit((values) => save.mutate(values))}
        noValidate
        className="space-y-4"
      >
        <FormField
          id="promo-edit-expires"
          type="date"
          label={mn.admin.promoExpires}
          hint={mn.admin.promoExpiresHint}
          error={errors.expires_on?.message}
          {...form.register("expires_on")}
        />
        <FormField
          id="promo-edit-max-uses"
          type="number"
          inputMode="numeric"
          min={1}
          step={1}
          label={mn.admin.promoMaxUses}
          hint={mn.admin.promoMaxUsesHint}
          error={errors.max_uses?.message}
          {...form.register("max_uses")}
        />
        <NoteField
          id="promo-edit-note"
          error={errors.note?.message}
          registration={form.register("note")}
        />
      </form>
      <DialogFooter>
        <Button variant="outline" onClick={onCancel}>
          {mn.admin.cancel}
        </Button>
        <Button type="submit" form="promo-edit-form" disabled={save.isPending}>
          {save.isPending ? mn.admin.saving : mn.admin.save}
        </Button>
      </DialogFooter>
    </DialogContent>
  );
}

function CopyCodeButton({ code }: { code: string }) {
  const [copied, setCopied] = useState(false);
  const copy = async () => {
    try {
      await navigator.clipboard.writeText(code);
      setCopied(true);
      setTimeout(() => setCopied(false), 1500);
    } catch {
      toast.error(mn.profile.referral.copyFailed);
    }
  };
  return (
    <Button
      size="icon-sm"
      variant="ghost"
      aria-label={copied ? mn.profile.referral.copied : `${code} — ${mn.learn.help.copy}`}
      onClick={() => void copy()}
    >
      {copied ? <CheckIcon className="size-4" /> : <CopyIcon className="size-4" />}
    </Button>
  );
}
