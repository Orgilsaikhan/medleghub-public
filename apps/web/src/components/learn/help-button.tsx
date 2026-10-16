"use client";

import { useQuery } from "@tanstack/react-query";
import { CheckIcon, CopyIcon, LifeBuoyIcon, TriangleAlertIcon } from "lucide-react";
import { useId, useState } from "react";
import { toast } from "sonner";

import { ErrorState } from "@/components/common/states";
import { LessonContent } from "@/components/learn/lesson-content";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Skeleton } from "@/components/ui/skeleton";
import { ApiError } from "@/lib/api/client";
import { getLessonHelp } from "@/lib/api/lessons";
import { mn } from "@/lib/i18n/mn";
import { readLocal, writeLocal } from "@/lib/local-storage";
import { queryKeys } from "@/lib/query-keys";

/** «Дахиж анхааруулах хэрэггүй» — бүх хичээлд хамаарна. */
const DISMISS_KEY = "medleghub:help-warning-dismissed";

/**
 * «Тусламж» — дасгалын зөвлөгөө ба жишиг шийдэл.
 *
 * Шийдэл нь шууд хариу тул дарах бүрд анхааруулна (сурагч «Дахиж
 * анхааруулах хэрэггүй»-г сонгоогүй бол). Зөвлөгөө, шийдлийг анхааруулгыг
 * зөвшөөрсний ДАРАА л серверээс татна — хичээлийн хариунд байдаггүй.
 */
export function HelpButton({
  lessonId,
  renderSolution,
}: {
  lessonId: string;
  /** Шийдлийг кодын оронд өөрөөр харуулах — Flowgorithm-д блок схем. */
  renderSolution?: (solution: string) => React.ReactNode;
}) {
  const [warningOpen, setWarningOpen] = useState(false);
  const [helpOpen, setHelpOpen] = useState(false);
  const [dontWarnAgain, setDontWarnAgain] = useState(false);
  const [revealed, setRevealed] = useState(false);
  const checkboxId = useId();

  const help = useQuery({
    queryKey: queryKeys.lessons.help(lessonId),
    queryFn: () => getLessonHelp(lessonId),
    enabled: revealed,
    staleTime: Infinity,
  });

  const reveal = () => {
    setRevealed(true);
    setHelpOpen(true);
  };

  const requestHelp = () => {
    if (readLocal(DISMISS_KEY, "0") === "1") {
      reveal();
      return;
    }
    setDontWarnAgain(false);
    setWarningOpen(true);
  };

  const confirm = () => {
    if (dontWarnAgain) writeLocal(DISMISS_KEY, "1");
    setWarningOpen(false);
    reveal();
  };

  return (
    <>
      <Button variant="ghost" size="sm" onClick={requestHelp} title={mn.learn.help.buttonHint}>
        <LifeBuoyIcon className="size-3.5" />
        {mn.learn.help.button}
      </Button>

      <Dialog open={warningOpen} onOpenChange={setWarningOpen}>
        <DialogContent className="sm:max-w-md">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2">
              <TriangleAlertIcon
                className="size-4 text-amber-600 dark:text-amber-400"
                aria-hidden
              />
              {mn.learn.help.warningTitle}
            </DialogTitle>
            <DialogDescription>{mn.learn.help.warning}</DialogDescription>
          </DialogHeader>

          <label
            htmlFor={checkboxId}
            className="flex w-fit cursor-pointer items-center gap-2 text-sm"
          >
            <input
              id={checkboxId}
              type="checkbox"
              checked={dontWarnAgain}
              onChange={(event) => setDontWarnAgain(event.target.checked)}
              className="accent-primary size-4 cursor-pointer"
            />
            {mn.learn.help.dontWarnAgain}
          </label>

          <DialogFooter>
            <Button variant="outline" onClick={() => setWarningOpen(false)}>
              {mn.learn.help.cancel}
            </Button>
            <Button onClick={confirm}>{mn.learn.help.confirm}</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      <Dialog open={helpOpen} onOpenChange={setHelpOpen}>
        <DialogContent className="max-h-[85vh] grid-rows-[auto_minmax(0,1fr)] sm:max-w-3xl">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2">
              <LifeBuoyIcon className="size-4" aria-hidden />
              {mn.learn.help.title}
            </DialogTitle>
            <DialogDescription>{mn.learn.help.description}</DialogDescription>
          </DialogHeader>

          <div className="min-h-0 overflow-y-auto pr-1">
            {help.isPending ? (
              <div className="space-y-3" aria-label={mn.learn.help.loading}>
                <Skeleton className="h-4 w-2/3" />
                <Skeleton className="h-4 w-1/2" />
                <Skeleton className="h-40 w-full" />
              </div>
            ) : help.isError ? (
              <ErrorState
                title={mn.common.error}
                description={
                  help.error instanceof ApiError ? help.error.message : mn.common.somethingWrong
                }
                onRetry={() => void help.refetch()}
              />
            ) : (
              <div className="space-y-6">
                {help.data.tips.trim() && (
                  <section>
                    <h3 className="mb-2 text-sm font-semibold">{mn.learn.help.tipsTitle}</h3>
                    <LessonContent content={help.data.tips} />
                  </section>
                )}
                <section>
                  <div className="mb-2 flex items-center justify-between gap-2">
                    <h3 className="text-sm font-semibold">{mn.learn.help.solutionTitle}</h3>
                    {!renderSolution && <CopyButton text={help.data.solution} />}
                  </div>
                  {renderSolution ? (
                    renderSolution(help.data.solution)
                  ) : (
                    <pre className="bg-code-bg border-code-border overflow-x-auto rounded-lg border p-4 font-mono text-[13px] leading-relaxed">
                      {help.data.solution}
                    </pre>
                  )}
                </section>
              </div>
            )}
          </div>
        </DialogContent>
      </Dialog>
    </>
  );
}

function CopyButton({ text }: { text: string }) {
  const [copied, setCopied] = useState(false);

  const copy = async () => {
    try {
      await navigator.clipboard.writeText(text);
      setCopied(true);
      setTimeout(() => setCopied(false), 1500);
    } catch {
      toast.error(mn.learn.help.copyFailed);
    }
  };

  return (
    <Button variant="outline" size="sm" onClick={() => void copy()}>
      {copied ? <CheckIcon className="size-3.5" /> : <CopyIcon className="size-3.5" />}
      {copied ? mn.learn.help.copied : mn.learn.help.copy}
    </Button>
  );
}
