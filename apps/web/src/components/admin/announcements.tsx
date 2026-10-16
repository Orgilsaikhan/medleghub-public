"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { EyeIcon, EyeOffIcon, MegaphoneIcon, PencilIcon } from "lucide-react";
import { useRef, useState } from "react";
import { Controller, useForm, useWatch } from "react-hook-form";
import { toast } from "sonner";

import { ConfirmDelete } from "@/components/admin/confirm-delete";
import { AnnouncementDialog } from "@/components/announcements/announcement-dialog";
import { FormField } from "@/components/auth/form-field";
import { EmptyState, ErrorState } from "@/components/common/states";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Skeleton } from "@/components/ui/skeleton";
import { Switch } from "@/components/ui/switch";
import { Textarea } from "@/components/ui/textarea";
import {
  createAnnouncement,
  deleteAnnouncement,
  listAnnouncements,
  updateAnnouncement,
} from "@/lib/api/announcements";
import { ApiError } from "@/lib/api/client";
import { formatDate } from "@/lib/format";
import { mn } from "@/lib/i18n/mn";
import { queryKeys } from "@/lib/query-keys";
import type { AnnouncementInput, AnnouncementItem } from "@/lib/types/api";
import { cn } from "@/lib/utils";
import {
  announcementSchema,
  endOfUlaanbaatarDay,
  startOfUlaanbaatarDay,
  ulaanbaatarDate,
  type AnnouncementValues,
} from "@/lib/validation/admin";

const KINDS = ["update", "feature"] as const;
const AUDIENCES = ["everyone", "signed_in", "free", "standard"] as const;

const EMPTY: AnnouncementValues = {
  kind: "update",
  title: "",
  body: "",
  cta_label: "",
  cta_url: "",
  audience: "signed_in",
  starts_on: "",
  ends_on: "",
  active: true,
};

function errorMessage(error: unknown): string {
  return error instanceof ApiError ? error.message : mn.common.somethingWrong;
}

function toValues(item: AnnouncementItem): AnnouncementValues {
  return {
    kind: item.kind,
    title: item.title,
    body: item.body,
    cta_label: item.cta_label ?? "",
    cta_url: item.cta_url ?? "",
    audience: item.audience,
    starts_on: item.starts_at ? ulaanbaatarDate(item.starts_at) : "",
    ends_on: item.ends_at ? ulaanbaatarDate(item.ends_at) : "",
    active: item.active,
  };
}

function toInput(values: AnnouncementValues): AnnouncementInput {
  return {
    kind: values.kind,
    title: values.title.trim(),
    body: values.body.trim(),
    cta_label: values.cta_label.trim() || null,
    cta_url: values.cta_url.trim() || null,
    audience: values.audience,
    starts_at: values.starts_on ? startOfUlaanbaatarDay(values.starts_on) : null,
    ends_at: values.ends_on ? endOfUlaanbaatarDay(values.ends_on) : null,
    active: values.active,
  };
}

/**
 * Зарлал (popup) бичих, засах, нийтлэх. Хэрэглэгчид `AnnouncementPopup` гаргана.
 * Эрхийг сервер шалгана.
 */
export function Announcements() {
  const [editing, setEditing] = useState<AnnouncementItem | null>(null);
  const formRef = useRef<HTMLDivElement>(null);

  return (
    <div className="space-y-8">
      <div ref={formRef}>
        <AnnouncementForm
          key={editing?.id ?? "new"}
          editing={editing}
          onDone={() => setEditing(null)}
        />
      </div>
      <AnnouncementList
        onEdit={(item) => {
          setEditing(item);
          formRef.current?.scrollIntoView({ behavior: "smooth", block: "start" });
          setTimeout(() => document.getElementById("announcement-title")?.focus(), 300);
        }}
      />
    </div>
  );
}

function useRefreshAnnouncements() {
  const queryClient = useQueryClient();
  return () => {
    void queryClient.invalidateQueries({ queryKey: queryKeys.admin.announcements });
    // Админ сайт руу буцахад өөрийнхөө нийтэлснийг шууд харна.
    void queryClient.invalidateQueries({ queryKey: ["announcements"] });
  };
}

function AnnouncementForm({
  editing,
  onDone,
}: {
  editing: AnnouncementItem | null;
  onDone: () => void;
}) {
  const refresh = useRefreshAnnouncements();
  const [preview, setPreview] = useState(false);
  const form = useForm<AnnouncementValues>({
    resolver: zodResolver(announcementSchema),
    defaultValues: editing ? toValues(editing) : EMPTY,
  });
  const errors = form.formState.errors;
  const values = useWatch({ control: form.control });
  const kind = values.kind ?? "update";

  const save = useMutation({
    mutationFn: (input: AnnouncementInput) =>
      editing ? updateAnnouncement(editing.id, input) : createAnnouncement(input),
    onSuccess: () => {
      refresh();
      toast.success(editing ? mn.admin.announcementSaved : mn.admin.announcementCreated);
      form.reset(EMPTY);
      onDone();
    },
    onError: (error) => toast.error(errorMessage(error)),
  });

  return (
    <Card className="max-w-2xl">
      <CardContent className="space-y-6">
        <h2 className="text-lg font-semibold tracking-tight">
          {editing ? mn.admin.announcementEdit : mn.admin.announcementNew}
        </h2>

        <form
          onSubmit={form.handleSubmit((submitted) => save.mutate(toInput(submitted)))}
          noValidate
          className="space-y-5"
        >
          <fieldset className="space-y-2">
            <legend className="text-sm font-medium">{mn.admin.announcementKind}</legend>
            <div className="flex flex-wrap gap-2">
              {KINDS.map((value) => (
                <RadioChip key={value} checked={kind === value}>
                  <input
                    type="radio"
                    value={value}
                    className="accent-primary size-4"
                    {...form.register("kind")}
                  />
                  {mn.admin.announcementKinds[value]}
                </RadioChip>
              ))}
            </div>
          </fieldset>

          <FormField
            id="announcement-title"
            label={mn.admin.announcementTitle}
            maxLength={120}
            error={errors.title?.message}
            {...form.register("title")}
          />

          <div className="space-y-2">
            <Label htmlFor="announcement-body">{mn.admin.announcementBody}</Label>
            <Textarea
              id="announcement-body"
              rows={5}
              maxLength={2000}
              aria-describedby="announcement-body-hint"
              aria-invalid={errors.body ? true : undefined}
              {...form.register("body")}
            />
            <p id="announcement-body-hint" className="text-muted-foreground text-xs">
              {mn.admin.announcementBodyHint}
            </p>
            {errors.body && (
              <p role="alert" className="text-destructive text-xs">
                {errors.body.message}
              </p>
            )}
          </div>

          <div className="grid gap-4 sm:grid-cols-2">
            <FormField
              id="announcement-cta-label"
              label={mn.admin.announcementCtaLabel}
              maxLength={40}
              error={errors.cta_label?.message}
              {...form.register("cta_label")}
            />
            <FormField
              id="announcement-cta-url"
              label={mn.admin.announcementCtaUrl}
              placeholder="/pricing"
              spellCheck={false}
              hint={mn.admin.announcementCtaHint}
              error={errors.cta_url?.message}
              {...form.register("cta_url")}
            />
          </div>

          <fieldset className="space-y-2">
            <legend className="text-sm font-medium">{mn.admin.announcementAudience}</legend>
            <div className="grid gap-2 sm:grid-cols-2">
              {AUDIENCES.map((value) => (
                <RadioChip key={value} checked={values.audience === value}>
                  <input
                    type="radio"
                    value={value}
                    className="accent-primary size-4"
                    {...form.register("audience")}
                  />
                  {mn.admin.announcementAudiences[value]}
                </RadioChip>
              ))}
            </div>
          </fieldset>

          <div className="grid gap-4 sm:grid-cols-2">
            <FormField
              id="announcement-starts"
              type="date"
              label={mn.admin.announcementStarts}
              hint={mn.admin.announcementStartsHint}
              error={errors.starts_on?.message}
              {...form.register("starts_on")}
            />
            <FormField
              id="announcement-ends"
              type="date"
              label={mn.admin.announcementEnds}
              hint={mn.admin.announcementEndsHint}
              error={errors.ends_on?.message}
              {...form.register("ends_on")}
            />
          </div>

          <div className="flex items-start gap-3">
            <Controller
              control={form.control}
              name="active"
              render={({ field }) => (
                <Switch
                  id="announcement-active"
                  checked={field.value}
                  onCheckedChange={field.onChange}
                  aria-describedby="announcement-active-hint"
                  className="mt-0.5"
                />
              )}
            />
            <div>
              <Label htmlFor="announcement-active">{mn.admin.announcementPublish}</Label>
              <p id="announcement-active-hint" className="text-muted-foreground text-xs">
                {mn.admin.announcementPublishHint}
              </p>
            </div>
          </div>

          <div className="flex flex-wrap gap-2">
            <Button type="submit" disabled={save.isPending}>
              {save.isPending ? mn.admin.announcementSaving : mn.admin.announcementSave}
            </Button>
            <Button
              type="button"
              variant="outline"
              disabled={!values.title?.trim() || !values.body?.trim()}
              onClick={() => setPreview(true)}
            >
              <EyeIcon className="size-4" />
              {mn.admin.announcementPreview}
            </Button>
            {editing && (
              <Button
                type="button"
                variant="ghost"
                onClick={() => {
                  form.reset(EMPTY);
                  onDone();
                }}
              >
                {mn.admin.cancel}
              </Button>
            )}
          </div>
        </form>

        <AnnouncementDialog
          announcement={{
            kind,
            title: values.title?.trim() ?? "",
            body: values.body?.trim() ?? "",
            cta_label: values.cta_label?.trim() || null,
            cta_url: values.cta_url?.trim() || null,
          }}
          open={preview}
          onClose={() => setPreview(false)}
        />
      </CardContent>
    </Card>
  );
}

function RadioChip({ checked, children }: { checked: boolean; children: React.ReactNode }) {
  return (
    <label
      className={cn(
        "flex cursor-pointer items-center gap-2 rounded-md border px-3 py-2 text-sm",
        "has-[:focus-visible]:ring-ring/50 has-[:focus-visible]:ring-[3px]",
        checked && "border-primary bg-accent",
      )}
    >
      {children}
    </label>
  );
}

function AnnouncementList({ onEdit }: { onEdit: (item: AnnouncementItem) => void }) {
  const refresh = useRefreshAnnouncements();
  const query = useQuery({ queryKey: queryKeys.admin.announcements, queryFn: listAnnouncements });

  const toggle = useMutation({
    mutationFn: (item: AnnouncementItem) => updateAnnouncement(item.id, { active: !item.active }),
    onSuccess: () => {
      refresh();
      toast.success(mn.admin.announcementSaved);
    },
    onError: (error) => toast.error(errorMessage(error)),
  });

  const remove = useMutation({
    mutationFn: (item: AnnouncementItem) => deleteAnnouncement(item.id),
    onSuccess: () => {
      refresh();
      toast.success(mn.admin.announcementDeleted);
    },
    onError: (error) => toast.error(errorMessage(error)),
  });

  return (
    <section aria-labelledby="announcement-list-title" className="space-y-4">
      <h2 id="announcement-list-title" className="text-lg font-semibold tracking-tight">
        {mn.admin.announcementListTitle}
      </h2>

      {query.isPending ? (
        <div className="space-y-3">
          {Array.from({ length: 2 }, (_, index) => (
            <Skeleton key={index} className="h-28 w-full" />
          ))}
        </div>
      ) : query.isError ? (
        <ErrorState onRetry={() => void query.refetch()} />
      ) : query.data.length === 0 ? (
        <EmptyState icon={MegaphoneIcon} title={mn.admin.announcementEmpty} />
      ) : (
        <ul className="divide-y rounded-xl border">
          {query.data.map((item) => (
            <li key={item.id} className="space-y-2 p-4">
              <div className="flex flex-wrap items-center gap-2">
                <span className="font-semibold">{item.title}</span>
                <Badge
                  variant="outline"
                  className={cn(item.status !== "live" && "text-muted-foreground")}
                >
                  {mn.admin.announcementStatus[item.status]}
                </Badge>
                <Badge variant="secondary">{mn.admin.announcementKinds[item.kind]}</Badge>
              </div>
              <p className="text-muted-foreground flex flex-wrap gap-x-3 gap-y-1 text-xs">
                <span className="text-foreground font-medium">
                  {mn.admin.announcementAudiences[item.audience]}
                </span>
                <span>
                  {mn.admin.announcementPeriod(
                    item.starts_at ? formatDate(item.starts_at) : null,
                    item.ends_at ? formatDate(item.ends_at) : null,
                  )}
                </span>
                <span>
                  {item.created_by
                    ? mn.admin.announcementBy(item.created_by, formatDate(item.created_at))
                    : formatDate(item.created_at)}
                </span>
              </p>
              <p className="text-muted-foreground line-clamp-2 text-sm">{item.body}</p>

              <div className="flex flex-wrap gap-2 pt-1">
                <Button size="sm" variant="outline" onClick={() => onEdit(item)}>
                  <PencilIcon className="size-4" />
                  {mn.admin.promoEdit}
                </Button>
                <Button
                  size="sm"
                  variant="outline"
                  disabled={toggle.isPending && toggle.variables?.id === item.id}
                  onClick={() => toggle.mutate(item)}
                >
                  {item.active ? <EyeOffIcon className="size-4" /> : <EyeIcon className="size-4" />}
                  {item.active ? mn.admin.announcementUnpublish : mn.admin.announcementPublish}
                </Button>
                <ConfirmDelete
                  name={item.title}
                  isPending={remove.isPending && remove.variables?.id === item.id}
                  onConfirm={() => remove.mutate(item)}
                />
              </div>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
