"use client";

import { useMutation, useQueryClient } from "@tanstack/react-query";
import {
  ArrowUpIcon,
  CalendarIcon,
  EllipsisIcon,
  ListTreeIcon,
  PencilIcon,
  RotateCcwIcon,
  Trash2Icon,
} from "lucide-react";
import Link from "next/link";
import { useId, useState } from "react";
import { toast } from "sonner";

import { ErrorState } from "@/components/common/states";
import { LiveMark } from "@/components/live/live-mark";
import {
  KIND_GLOWS,
  MasteryBar,
  MaterialKindIcon,
  MaterialStatusChip,
  OrbitArcs,
  Spotlight,
  trackSpotlight,
} from "@/components/live/live-ui";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Skeleton } from "@/components/ui/skeleton";
import { deleteMaterial, renameMaterial } from "@/lib/api/live";
import { formatDate, formatFileSize } from "@/lib/format";
import { liveErrorMessage, useLiveMaterials, useRetryMaterial } from "@/lib/hooks/use-live";
import { mn } from "@/lib/i18n/mn";
import { isMaterialProcessing } from "@/lib/live";
import { queryKeys } from "@/lib/query-keys";
import type { LiveMaterialDetail, LiveMaterialSummary } from "@/lib/types/live";
import { cn } from "@/lib/utils";

const t = mn.live;

/** Хэрэглэгчийн материалууд. AI задалж буй нь байвал жагсаалт өөрөө шинэчлэгдэнэ. */
export function MaterialList() {
  const query = useLiveMaterials();

  return (
    <section aria-labelledby="live-materials-title" className="space-y-5">
      <h2 id="live-materials-title" className="text-xl font-semibold tracking-tight">
        {t.materialsTitle}
      </h2>

      {query.isPending ? (
        <MaterialGridSkeleton />
      ) : query.isError ? (
        <ErrorState
          description={liveErrorMessage(query.error)}
          onRetry={() => void query.refetch()}
        />
      ) : query.data.length === 0 ? (
        <MaterialsEmpty />
      ) : (
        <ul className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
          {query.data.map((material) => (
            <li key={material.id} className="flex">
              <MaterialCard material={material} />
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}

export function MaterialGridSkeleton() {
  return (
    <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3" aria-hidden>
      {Array.from({ length: 3 }, (_, index) => (
        <Skeleton key={index} className="h-56 w-full rounded-2xl" />
      ))}
    </div>
  );
}

/** Материалгүй үед — тойрог замтай Live-ийн тэмдэг, дээрх талбай руу заана. */
function MaterialsEmpty() {
  return (
    <div className="bg-card/50 relative isolate flex flex-col items-center overflow-hidden rounded-3xl border border-dashed px-6 py-14 text-center">
      <span aria-hidden className="relative mb-6 grid size-20 place-items-center">
        <OrbitArcs className="text-primary absolute top-1/2 left-1/2 -z-10 w-80 max-w-none -translate-x-1/2 -translate-y-1/2" />
        <span className="bg-card text-brand-link grid size-16 place-items-center rounded-2xl border shadow-sm">
          <LiveMark className="size-9" />
        </span>
      </span>
      <p className="font-semibold">{t.empty}</p>
      <p className="text-muted-foreground mt-1.5 flex max-w-sm items-center gap-1.5 text-sm">
        <ArrowUpIcon className="size-4 shrink-0" aria-hidden />
        {t.emptyHint}
      </p>
    </div>
  );
}

/**
 * Материалын карт. Бүх карт нь холбоос (`after:`); цэс, «Дахин оролдох» нь
 * дээр нь. Хулгана дээр нь курсорыг дагах гэрэл, карт өргөгдөж, төрлийн дүрс
 * «үсэрнэ». AI задалж байх зуур доод талд нь гэрэл гүйнэ.
 */
function MaterialCard({ material }: { material: LiveMaterialSummary }) {
  const retry = useRetryMaterial(material.id);
  const [dialog, setDialog] = useState<"rename" | "delete" | null>(null);
  const ready = material.status === "ready";
  const meta = [
    t.kinds[material.kind],
    material.page_count ? t.pageCount(material.page_count) : null,
    formatFileSize(material.size_bytes),
  ].filter(Boolean);

  return (
    <article
      onPointerMove={trackSpotlight}
      className="group/spot bg-card hover:border-primary/40 hover:shadow-primary/10 relative isolate flex w-full flex-col overflow-hidden rounded-2xl border p-5 shadow-xs transition-[border-color,box-shadow,translate] duration-300 hover:shadow-xl motion-safe:hover:-translate-y-1 motion-reduce:transition-none"
    >
      <Spotlight />
      <span
        aria-hidden
        className={cn(
          "pointer-events-none absolute -top-20 -right-16 -z-10 size-48 rounded-full opacity-70 blur-3xl transition-opacity duration-500 group-hover/spot:opacity-100",
          KIND_GLOWS[material.kind],
        )}
      />

      <div className="flex items-start gap-3">
        <MaterialKindIcon
          kind={material.kind}
          className="transition-[translate,rotate,scale] duration-500 ease-[cubic-bezier(0.34,1.56,0.64,1)] group-hover/spot:scale-105 motion-safe:group-hover/spot:-translate-y-0.5 motion-safe:group-hover/spot:-rotate-6 motion-reduce:transition-none"
        />
        <div className="min-w-0 flex-1">
          <h3 className="line-clamp-2 leading-snug font-semibold">
            {/* Бүх карт дарагдана (`after:`); цэс, товч нь дээр нь (`relative z-30`). */}
            <Link
              href={`/live/materials/${material.id}`}
              className="focus-visible:after:ring-ring/50 outline-none after:absolute after:inset-0 after:rounded-2xl focus-visible:after:ring-3 focus-visible:after:ring-inset"
            >
              {material.title}
            </Link>
          </h3>
          <p className="text-muted-foreground mt-1 truncate text-xs">{meta.join(" · ")}</p>
        </div>
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button
              variant="ghost"
              size="icon-sm"
              className="relative z-30 -mt-1 -mr-2"
              aria-label={t.actions(material.title)}
            >
              <EllipsisIcon />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent
            align="end"
            className="w-44"
            // Цонх нээгдэхэд focus-ийг цэсний товч руу буцаахгүй — цонхных болно.
            onCloseAutoFocus={(event) => {
              if (dialog) event.preventDefault();
            }}
          >
            <DropdownMenuItem onSelect={() => setDialog("rename")}>
              <PencilIcon />
              {t.rename}
            </DropdownMenuItem>
            <DropdownMenuItem variant="destructive" onSelect={() => setDialog("delete")}>
              <Trash2Icon />
              {t.delete}
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>

      <div className="mt-4 flex flex-wrap items-center gap-x-3 gap-y-2">
        <MaterialStatusChip status={material.status} title={material.title} />
        {ready && (
          <span className="text-muted-foreground inline-flex items-center gap-1 text-xs">
            <ListTreeIcon className="size-3.5" aria-hidden />
            {t.topicCount(material.topic_count)}
          </span>
        )}
      </div>

      {material.status === "failed" && (
        <div className="mt-3 space-y-3">
          <p className="text-destructive text-sm">{material.error_message ?? t.failedFallback}</p>
          <Button
            variant="outline"
            size="sm"
            className="relative z-30"
            disabled={retry.isPending}
            onClick={() => retry.mutate()}
          >
            <RotateCcwIcon />
            {t.retry}
          </Button>
        </div>
      )}

      <div className="mt-auto space-y-3 pt-5">
        {ready && (
          <div className="space-y-1.5">
            <p className="flex items-baseline justify-between gap-2 text-xs">
              <span className="text-muted-foreground">{t.mastery}</span>
              <span className="font-semibold tabular-nums">{Math.round(material.mastery)}%</span>
            </p>
            <MasteryBar value={material.mastery} label={t.mastery} showValue={false} />
          </div>
        )}
        {/* AI задалж байх зуур — зогсолтгүй гүйх гэрэл (утгыг төлөвийн шошго хэлнэ). */}
        {isMaterialProcessing(material.status) && (
          <span
            aria-hidden
            className="bg-foreground/10 relative block h-1.5 overflow-hidden rounded-full"
          >
            <span className="via-primary motion-safe:animate-live-shimmer motion-reduce:bg-primary/60 absolute inset-0 bg-gradient-to-r from-transparent to-transparent motion-reduce:w-1/3" />
          </span>
        )}
        <p className="text-muted-foreground flex items-center gap-1.5 text-xs">
          <CalendarIcon className="size-3.5 shrink-0" aria-hidden />
          {t.addedOn(formatDate(material.created_at))}
        </p>
      </div>

      <RenameDialog
        material={material}
        open={dialog === "rename"}
        onOpenChange={(open) => setDialog(open ? "rename" : null)}
      />
      <DeleteDialog
        material={material}
        open={dialog === "delete"}
        onOpenChange={(open) => setDialog(open ? "delete" : null)}
      />
    </article>
  );
}

interface MaterialDialogProps {
  material: LiveMaterialSummary;
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

function RenameDialog({ material, open, onOpenChange }: MaterialDialogProps) {
  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      {/* Нээх бүрд одоогийн нэрээр эхэлнэ. */}
      {open && <RenameForm material={material} onDone={() => onOpenChange(false)} />}
    </Dialog>
  );
}

function RenameForm({ material, onDone }: { material: LiveMaterialSummary; onDone: () => void }) {
  const queryClient = useQueryClient();
  const inputId = useId();
  const [title, setTitle] = useState(material.title);
  const [error, setError] = useState<string | null>(null);

  const rename = useMutation({
    mutationFn: (value: string) => renameMaterial(material.id, value),
    onSuccess: (updated) => {
      queryClient.setQueryData<LiveMaterialSummary[]>(queryKeys.live.materials, (list) =>
        list?.map((item) => (item.id === updated.id ? updated : item)),
      );
      queryClient.setQueryData<LiveMaterialDetail>(queryKeys.live.material(updated.id), (detail) =>
        detail ? { ...detail, title: updated.title } : detail,
      );
      toast.success(t.renamed);
      onDone();
    },
    onError: (failure) => setError(liveErrorMessage(failure)),
  });

  return (
    <DialogContent>
      <form
        noValidate
        className="grid gap-4"
        onSubmit={(event) => {
          event.preventDefault();
          const value = title.trim();
          if (!value) {
            setError(t.renameRequired);
            return;
          }
          rename.mutate(value);
        }}
      >
        <DialogHeader>
          <DialogTitle>{t.renameTitle}</DialogTitle>
        </DialogHeader>
        <div className="space-y-2">
          <Label htmlFor={inputId}>{t.renameLabel}</Label>
          <Input
            id={inputId}
            value={title}
            maxLength={200}
            autoFocus
            aria-invalid={error ? true : undefined}
            aria-describedby={error ? `${inputId}-error` : undefined}
            onChange={(event) => {
              setTitle(event.target.value);
              setError(null);
            }}
          />
          {error && (
            <p id={`${inputId}-error`} role="alert" className="text-destructive text-xs">
              {error}
            </p>
          )}
        </div>
        <DialogFooter>
          <Button type="button" variant="outline" onClick={onDone}>
            {t.cancel}
          </Button>
          <Button type="submit" disabled={rename.isPending}>
            {t.save}
          </Button>
        </DialogFooter>
      </form>
    </DialogContent>
  );
}

function DeleteDialog({ material, open, onOpenChange }: MaterialDialogProps) {
  const queryClient = useQueryClient();
  const remove = useMutation({
    mutationFn: () => deleteMaterial(material.id),
    onSuccess: () => {
      onOpenChange(false);
      queryClient.setQueryData<LiveMaterialSummary[]>(queryKeys.live.materials, (list) =>
        list?.filter((item) => item.id !== material.id),
      );
      queryClient.removeQueries({ queryKey: queryKeys.live.material(material.id) });
      void queryClient.invalidateQueries({ queryKey: queryKeys.live.configAll });
      // Бэлэн болоогүй материалд ашигласан нэг удаагийн эрх буцна.
      void queryClient.invalidateQueries({ queryKey: queryKeys.billing.plan });
      toast.success(t.deleted);
    },
    onError: (error) => toast.error(liveErrorMessage(error)),
  });

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>{t.deleteTitle}</DialogTitle>
          <DialogDescription>{t.deleteBody(material.title)}</DialogDescription>
        </DialogHeader>
        <DialogFooter>
          <Button variant="outline" onClick={() => onOpenChange(false)}>
            {t.cancel}
          </Button>
          <Button variant="destructive" disabled={remove.isPending} onClick={() => remove.mutate()}>
            <Trash2Icon />
            {t.delete}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
