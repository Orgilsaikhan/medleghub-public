"use client";

import { useMutation, useQueryClient } from "@tanstack/react-query";
import {
  BookOpenCheckIcon,
  CircleCheckIcon,
  CloudUploadIcon,
  LayersIcon,
  TargetIcon,
  XIcon,
} from "lucide-react";
import Link from "next/link";
import { useId, useRef, useState, type DragEvent } from "react";
import { toast } from "sonner";

import { EYEBROW, LiveTile, MaterialKindIcon, trackSpotlight } from "@/components/live/live-ui";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Progress } from "@/components/ui/progress";
import { ApiError } from "@/lib/api/client";
import { createMaterial, deleteMaterial, uploadMaterialContent } from "@/lib/api/live";
import { formatFileSize } from "@/lib/format";
import { liveErrorMessage } from "@/lib/hooks/use-live";
import { usePlan } from "@/lib/hooks/use-plan";
import { mn } from "@/lib/i18n/mn";
import {
  describeAcceptedTypes,
  fileExtension,
  kindFromFilename,
  needsConversion,
  titleFromFilename,
} from "@/lib/live";
import { queryKeys } from "@/lib/query-keys";
import type { LiveConfig, LiveMaterialKind, LiveMaterialSummary } from "@/lib/types/live";
import { cn } from "@/lib/utils";

const t = mn.live;

/** «Хэрхэн ажилладаг вэ» алхмуудын дүрс — бичвэр нь `mn.live.steps`-д. */
const STEP_ICONS = [LayersIcon, BookOpenCheckIcon, TargetIcon];

/** Чирж тавих талбайн дүрсний ард сэнс шиг дэлгэгдэх файлууд (байрлал, хөдөлгөөн). */
const FAN: { kind: LiveMaterialKind; className: string }[] = [
  {
    kind: "docx",
    className:
      "-translate-y-3 rotate-3 motion-safe:group-hover/drop:-translate-y-6 motion-safe:group-data-dragging/drop:-translate-y-9",
  },
  {
    kind: "pdf",
    className:
      "-translate-x-7 translate-y-1 -rotate-12 motion-safe:group-hover/drop:-translate-x-10 motion-safe:group-hover/drop:-rotate-[18deg] motion-safe:group-data-dragging/drop:-translate-x-14 motion-safe:group-data-dragging/drop:-rotate-[26deg]",
  },
  {
    kind: "pptx",
    className:
      "translate-x-7 translate-y-1 rotate-12 motion-safe:group-hover/drop:translate-x-10 motion-safe:group-hover/drop:rotate-[18deg] motion-safe:group-data-dragging/drop:translate-x-14 motion-safe:group-data-dragging/drop:rotate-[26deg]",
  },
];

/** Серверийнхтэй ижил дүрэм — зөвхөн хэрэглэгчид эрт мэдэгдэхэд. Эцсийн шалгалт серверт. */
function validateFile(file: File, upload: LiveConfig["upload"]): string | null {
  const types = describeAcceptedTypes(upload.accepted, t.uploadImages);
  if (needsConversion(file.name)) return t.uploadConvert(fileExtension(file.name));
  if (!upload.accepted.map((item) => item.toLowerCase()).includes(fileExtension(file.name))) {
    return t.uploadUnsupported(types);
  }
  if (file.size === 0) return t.uploadEmptyFile;
  if (file.size > upload.max_bytes) return t.uploadTooLarge(formatFileSize(upload.max_bytes));
  return null;
}

interface UploadInput {
  file: File;
  title: string;
}

/**
 * Лекцийн файл оруулах: чирж тавих эсвэл сонгох, нэр (заавал биш). Эхлээд мета
 * (`createMaterial`) — багц, хязгаарыг сервер шалгана;
 * дараа нь файлыг XHR-ээр явцтай нь илгээнэ. Илгээлт тасарвал хоосон
 * материал үлдээхгүй — устгана.
 */
export function UploadCard({ config }: { config: LiveConfig }) {
  const queryClient = useQueryClient();
  const inputRef = useRef<HTMLInputElement>(null);
  const abortRef = useRef<AbortController | null>(null);
  const ids = {
    input: useId(),
    limits: useId(),
    fileError: useId(),
    title: useId(),
  };

  const [file, setFile] = useState<File | null>(null);
  const [title, setTitle] = useState("");
  const [dragging, setDragging] = useState(false);
  const [fileError, setFileError] = useState<string | null>(null);
  const [serverError, setServerError] = useState<string | null>(null);
  // Багц дууссан (жишээ нь хуудас нээлттэй байхад) — Standard багцад Live багтсан тул тийш нь заана.
  const [needsPlan, setNeedsPlan] = useState(false);
  const [progress, setProgress] = useState<number | null>(null);

  const types = describeAcceptedTypes(config.upload.accepted, t.uploadImages);
  const { data: plan } = usePlan();

  const upload = useMutation({
    mutationFn: async ({ file: selected, title: name }: UploadInput) => {
      const created = await createMaterial({
        filename: selected.name,
        size_bytes: selected.size,
        title: name.trim() || undefined,
      });
      // Жагсаалтад «Илгээж байна» төлөвтэй шууд гарна.
      queryClient.setQueryData<LiveMaterialSummary[]>(queryKeys.live.materials, (list) =>
        list ? [created, ...list.filter((item) => item.id !== created.id)] : [created],
      );
      const controller = new AbortController();
      abortRef.current = controller;
      try {
        return await uploadMaterialContent(
          created.id,
          selected,
          (fraction) => setProgress(Math.round(fraction * 100)),
          controller.signal,
        );
      } catch (error) {
        // Агуулгагүй материал ашиггүй — жагсаалтад гацаж үлдэхгүй.
        await deleteMaterial(created.id).catch(() => undefined);
        throw error;
      } finally {
        abortRef.current = null;
      }
    },
    onMutate: () => {
      setServerError(null);
      setNeedsPlan(false);
      setProgress(0);
    },
    onSuccess: (material) => {
      queryClient.setQueryData<LiveMaterialSummary[]>(queryKeys.live.materials, (list) =>
        list?.map((item) => (item.id === material.id ? material : item)),
      );
      toast.success(t.uploadDone);
      setFile(null);
      setTitle("");
      if (inputRef.current) inputRef.current.value = "";
    },
    onError: (error) => {
      // «Болих» дарсан — алдаа биш.
      if (error instanceof ApiError && error.code === "ABORTED") return;
      const message = liveErrorMessage(error);
      setServerError(message);
      setNeedsPlan(
        error instanceof ApiError &&
          (error.code === "LIVE_PLAN_REQUIRED" || error.code === "LIVE_PASS_USED"),
      );
      toast.error(message);
    },
    onSettled: () => {
      setProgress(null);
      void queryClient.invalidateQueries({ queryKey: queryKeys.live.materials });
      void queryClient.invalidateQueries({ queryKey: queryKeys.live.configAll });
      // Нэг удаагийн эрх ашиглагдсан эсэх (`has_unused_live_pass`).
      void queryClient.invalidateQueries({ queryKey: queryKeys.billing.plan });
    },
  });

  const choose = (selected: File | null) => {
    setServerError(null);
    if (!selected) return;
    const error = validateFile(selected, config.upload);
    setFileError(error);
    setFile(error ? null : selected);
  };

  const clearFile = () => {
    setFile(null);
    setFileError(null);
    if (inputRef.current) inputRef.current.value = "";
  };

  const onDrop = (event: DragEvent<HTMLLabelElement>) => {
    event.preventDefault();
    setDragging(false);
    if (upload.isPending) return;
    choose(event.dataTransfer.files[0] ?? null);
  };

  const submit = () => {
    const missingFile = file ? null : (fileError ?? t.uploadFileRequired);
    setFileError(missingFile);
    if (!file) {
      inputRef.current?.focus();
      return;
    }
    upload.mutate({ file, title });
  };

  const sending = upload.isPending;
  const fileDescribedBy = [ids.limits, fileError ? ids.fileError : null].filter(Boolean).join(" ");

  return (
    <section
      aria-labelledby="live-upload-title"
      className="bg-card rounded-3xl border p-5 shadow-xs sm:p-7"
    >
      <h2 id="live-upload-title" className="text-lg font-semibold tracking-tight">
        {t.uploadTitle}
      </h2>
      {config.tier === "pass" && (
        <p className="text-muted-foreground mt-1 text-sm text-pretty">
          {t.uploadPassNote(plan?.live_pass_access_days ?? 30)}
        </p>
      )}

      <form
        noValidate
        onSubmit={(event) => {
          event.preventDefault();
          submit();
        }}
        className="mt-5 grid gap-6 lg:grid-cols-[minmax(0,1.15fr)_minmax(0,1fr)] lg:gap-8"
      >
        {/* Чирж тавих талбай баганаа дүүргэнэ — хоёр багана ижил өндөртэй. */}
        <div className="flex flex-col gap-3">
          {/* Бүх талбай нь файл сонгох шошго — гараар Tab-аар оролт руу орно. Хулгана
              дээр нь курсорыг дагах гэрэл, чирж байхад хүрээгээр гэрэл эргэлдэнэ,
              илгээж байхад «скан» гүйнэ. */}
          <label
            htmlFor={ids.input}
            data-dragging={dragging || undefined}
            data-disabled={sending || undefined}
            onPointerMove={trackSpotlight}
            onDragOver={(event) => {
              event.preventDefault();
              if (!sending) setDragging(true);
            }}
            onDragLeave={(event) => {
              // Доторх дүрс, бичвэр дээгүүр шилжихэд ч `dragleave` ирдэг — тэрийг үл тооно.
              if (event.currentTarget.contains(event.relatedTarget as Node | null)) return;
              setDragging(false);
            }}
            onDrop={onDrop}
            className={cn(
              "group/drop relative isolate flex min-h-52 flex-1 cursor-pointer flex-col items-center justify-center gap-3 rounded-2xl border-2 border-dashed px-6 py-9 text-center transition-[border-color,background-color] duration-300 motion-reduce:transition-none",
              "hover:border-primary/60 hover:bg-accent/30",
              "data-dragging:border-primary/40 data-dragging:bg-accent/60",
              "has-[input:focus-visible]:border-ring has-[input:focus-visible]:ring-ring/50 has-[input:focus-visible]:ring-3",
              "data-disabled:border-primary/50 data-disabled:pointer-events-none",
              fileError && "border-destructive/60",
            )}
          >
            <input
              ref={inputRef}
              id={ids.input}
              type="file"
              accept={config.upload.accepted.join(",")}
              className="sr-only"
              disabled={sending}
              aria-label={t.uploadFileLabel}
              aria-describedby={fileDescribedBy}
              aria-invalid={fileError ? true : undefined}
              onChange={(event) => choose(event.currentTarget.files?.[0] ?? null)}
            />

            {/* Чимэглэлийн давхаргууд — талбайн хүрээнээс гарахгүй. */}
            <span
              aria-hidden
              className="pointer-events-none absolute inset-0 -z-10 overflow-hidden rounded-[calc(var(--radius)*1.8_-_2px)]"
            >
              <span className="live-dots absolute inset-0 [mask-image:radial-gradient(ellipse_at_center,#000_20%,transparent_75%)] opacity-70" />
              <span className="absolute inset-0 opacity-0 transition-opacity duration-300 [background:radial-gradient(260px_circle_at_var(--spot-x,50%)_var(--spot-y,50%),color-mix(in_oklch,var(--primary)_14%,transparent),transparent_70%)] group-hover/drop:opacity-100" />
              {sending && (
                <span className="motion-safe:animate-live-scan absolute inset-0 motion-reduce:hidden">
                  <span className="from-primary/0 via-primary/10 to-primary/25 border-primary/70 absolute inset-x-0 top-0 h-2/5 border-b-2 bg-gradient-to-b" />
                </span>
              )}
            </span>
            {/* Чирж байх үед хүрээгээр эргэлдэх гэрэл — зөвхөн тэр үед хөдөлнө. */}
            <span
              aria-hidden
              className="live-beam motion-safe:group-data-dragging/drop:animate-live-beam pointer-events-none absolute -inset-[2px] rounded-[inherit] opacity-0 transition-opacity duration-300 group-data-dragging/drop:opacity-100"
            />

            <span className="relative mb-1 grid place-items-center">
              {/* Дэмжих файлууд ард нь сэнс шиг — хулгана дээр нь дэлгэгдэж, чирж
                  байхад бүр өргөн тархана. */}
              {FAN.map(({ kind, className }) => (
                <span
                  key={kind}
                  aria-hidden
                  className={cn(
                    "bg-card absolute rounded-xl shadow-md transition-[translate,rotate] duration-500 ease-[cubic-bezier(0.34,1.56,0.64,1)] motion-reduce:transition-none",
                    className,
                  )}
                >
                  <MaterialKindIcon kind={kind} className="size-11" />
                </span>
              ))}
              {/* Чирж байхад дүрсний эргэн тойронд долгио тархана. */}
              {dragging && (
                <span
                  aria-hidden
                  className="border-primary/60 absolute inset-0 rounded-2xl border-2 motion-safe:animate-ping"
                />
              )}
              <LiveTile className="size-14 transition-[translate,scale] duration-300 ease-[cubic-bezier(0.34,1.56,0.64,1)] group-data-dragging/drop:scale-110 motion-safe:group-hover/drop:-translate-y-1 motion-reduce:transition-none">
                <CloudUploadIcon className="size-7" />
              </LiveTile>
            </span>
            <span className="mt-1 text-base font-semibold">
              {dragging ? t.uploadDropActive : t.uploadDrop}
            </span>
            <span className="bg-card text-foreground group-hover/drop:border-primary/50 rounded-full border px-3.5 py-1 text-sm font-medium shadow-xs transition-colors">
              {t.uploadChoose}
            </span>
            <span id={ids.limits} className="text-muted-foreground text-xs text-balance">
              {t.uploadLimits(
                types,
                formatFileSize(config.upload.max_bytes),
                config.upload.max_pages,
              )}
            </span>
          </label>

          {fileError && (
            <p id={ids.fileError} role="alert" className="text-destructive text-sm">
              {fileError}
            </p>
          )}

          {file && (
            <div className="bg-muted/40 motion-safe:animate-in motion-safe:slide-in-from-top-1 flex items-center gap-3 rounded-2xl border p-3 duration-200">
              <MaterialKindIcon kind={kindFromFilename(file.name)} className="size-10" />
              <div className="min-w-0 flex-1">
                <p className="truncate text-sm font-medium">{file.name}</p>
                <p className="text-muted-foreground flex items-center gap-1 text-xs">
                  <CircleCheckIcon className="text-success size-3.5 shrink-0" aria-hidden />
                  {formatFileSize(file.size)}
                </p>
              </div>
              <Button
                type="button"
                variant="ghost"
                size="icon-sm"
                disabled={sending}
                aria-label={t.uploadRemove}
                onClick={clearFile}
              >
                <XIcon />
              </Button>
            </div>
          )}
        </div>

        <div className="flex flex-col gap-5">
          <div className="space-y-2">
            <Label htmlFor={ids.title}>{t.uploadTitleLabel}</Label>
            <Input
              id={ids.title}
              value={title}
              maxLength={200}
              disabled={sending}
              placeholder={file ? titleFromFilename(file.name) : undefined}
              aria-describedby={`${ids.title}-hint`}
              onChange={(event) => setTitle(event.target.value)}
              className="h-10"
            />
            <p id={`${ids.title}-hint`} className="text-muted-foreground text-xs">
              {t.uploadTitleHint}
            </p>
          </div>

          {serverError && (
            <p
              role="alert"
              className="border-destructive/30 bg-destructive/5 text-destructive rounded-xl border px-3 py-2.5 text-sm"
            >
              {serverError}
              {needsPlan && (
                <>
                  {" "}
                  <Link href="/pricing" className="font-semibold underline underline-offset-2">
                    {t.getStandard}
                  </Link>
                </>
              )}
            </p>
          )}

          {/* Ширээний дэлгэцэд чирж тавих талбайн хажуугийн зайд — оруулсны дараа юу
              болохыг. Алхмууд нэг шугамаар холбогдоно. */}
          <div className="hidden lg:block">
            <p className={EYEBROW}>{t.stepsTitle}</p>
            <div className="relative mt-4">
              <span
                aria-hidden
                className="from-primary/60 to-border absolute top-4 bottom-4 left-4 w-px -translate-x-1/2 bg-gradient-to-b"
              />
              <ol className="relative space-y-3.5">
                {t.steps.map((step, index) => {
                  const Icon = STEP_ICONS[index] ?? LayersIcon;
                  return (
                    <li key={step} className="relative flex items-center gap-3 text-sm">
                      <span
                        aria-hidden
                        className="bg-card text-accent-foreground ring-primary/35 grid size-8 shrink-0 place-items-center rounded-full shadow-xs ring-1"
                      >
                        <Icon className="size-4" />
                      </span>
                      {step}
                    </li>
                  );
                })}
              </ol>
            </div>
          </div>

          <div className="mt-auto space-y-3">
            {progress !== null && (
              <div className="space-y-1.5">
                <p className="text-muted-foreground text-xs tabular-nums">
                  {t.uploadSending(progress)}
                </p>
                <Progress
                  value={progress}
                  aria-label={t.uploadProgressLabel}
                  className="bg-foreground/10 [&>[data-slot=progress-indicator]]:from-primary h-2 [&>[data-slot=progress-indicator]]:bg-gradient-to-r [&>[data-slot=progress-indicator]]:to-amber-300"
                />
              </div>
            )}
            <div className="flex flex-wrap gap-2">
              <Button type="submit" size="lg" disabled={sending} className="min-w-32">
                <CloudUploadIcon className="size-4" aria-hidden />
                {t.uploadSubmit}
              </Button>
              {sending && (
                <Button
                  type="button"
                  size="lg"
                  variant="outline"
                  onClick={() => abortRef.current?.abort()}
                >
                  {t.uploadCancel}
                </Button>
              )}
            </div>
          </div>
        </div>
      </form>
    </section>
  );
}
