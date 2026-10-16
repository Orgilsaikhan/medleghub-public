"use client";

import { AlertTriangleIcon, KeyboardIcon, TerminalIcon } from "lucide-react";
import { useEffect, useRef } from "react";

import { mn } from "@/lib/i18n/mn";
import type { RunResult } from "@/lib/sandbox/runner";
import { cn } from "@/lib/utils";

const LEVEL_STYLES: Record<string, string> = {
  log: "text-foreground/90",
  info: "text-brand-link",
  warn: "text-amber-600 dark:text-amber-400",
  error: "text-destructive",
};

interface ConsoleOutputProps {
  result: RunResult | null;
  isRunning: boolean;
  /** Ажиллаж байх үеийн текст. Python ачаалах, C/C++ хөрвүүлэхэд өөр мессеж. */
  statusText?: string;
  /** Юу ч ажиллуулаагүй үеийн текст. SQL-д сан дахин шинэчлэгддэгийг хэлнэ. */
  emptyText?: string;
}

export function ConsoleOutput({ result, isRunning, statusText, emptyText }: ConsoleOutputProps) {
  const endRef = useRef<HTMLDivElement>(null);

  // Шинэ гаралт гарахад доод тал руу гүйлгэнэ.
  useEffect(() => {
    endRef.current?.scrollIntoView({ block: "end" });
  }, [result]);

  if (isRunning && !result) {
    return <ConsoleShell muted>{statusText ?? mn.learn.running}</ConsoleShell>;
  }

  if (!result) {
    return (
      <ConsoleShell muted>
        <span className="flex items-center gap-2">
          <TerminalIcon className="size-3.5" aria-hidden />
          {emptyText ?? mn.learn.consoleEmpty}
        </span>
      </ConsoleShell>
    );
  }

  const isEmpty =
    result.entries.length === 0 &&
    !result.error &&
    !result.timedOut &&
    !result.compileError &&
    !result.exitCode;

  return (
    <div
      role="log"
      aria-live="polite"
      aria-label={mn.learn.console}
      className="h-full overflow-auto p-3 font-mono text-[13px] leading-relaxed"
    >
      {/* Терминалтай ижил: анхааруулга програмын гаралтаас ӨМНӨ гарна. */}
      {result.warnings && (
        <Diagnostics tone="warning" title={mn.learn.warningsTitle} text={result.warnings} />
      )}

      {result.entries.map((entry, index) =>
        entry.preformatted ? (
          // Хүснэгтийн хүрээ баганатайгаа таарах ёстой тул ороохгүй.
          <pre
            key={index}
            className={cn("overflow-x-auto py-1 whitespace-pre", LEVEL_STYLES[entry.level])}
          >
            {entry.text}
          </pre>
        ) : (
          <div key={index} className={cn("flex gap-2 py-0.5", LEVEL_STYLES[entry.level])}>
            <span aria-hidden className="text-muted-foreground/50 select-none">
              ›
            </span>
            <span className="min-w-0 break-words whitespace-pre-wrap">{entry.text}</span>
          </div>
        ),
      )}

      {result.truncated && (
        <p className="text-muted-foreground py-1 text-xs italic">
          … гаралт хэт урт тул таслав (эхний 500 мөр).
        </p>
      )}

      {result.timedOut && (
        <p className="text-destructive flex items-start gap-2 py-1">
          <AlertTriangleIcon className="mt-0.5 size-3.5 shrink-0" aria-hidden />
          <span className="whitespace-pre-wrap">{mn.learn.timeout}</span>
        </p>
      )}

      {result.compileError && (
        <Diagnostics tone="error" title={mn.learn.compileErrorTitle} text={result.compileError} />
      )}

      {result.error && (
        <div className="text-destructive flex items-start gap-2 py-1">
          <AlertTriangleIcon className="mt-0.5 size-3.5 shrink-0" aria-hidden />
          <div className="min-w-0">
            {/* Python-д traceback нь аль мөрөнд алдсаныг харуулдаг тул түүнийг
                бүтнээр нь харуулна. JavaScript-д traceback байхгүй. */}
            {result.error.traceback ? (
              <pre className="break-words whitespace-pre-wrap">{result.error.traceback}</pre>
            ) : (
              <span className="break-words whitespace-pre-wrap">
                {result.error.name}: {result.error.message}
              </span>
            )}
          </div>
        </div>
      )}

      {!!result.exitCode && !result.error && !result.timedOut && (
        <p className="text-muted-foreground py-1 text-xs italic">
          {mn.learn.exitCode(result.exitCode)}
        </p>
      )}

      {result.needsInput && (
        <p className="text-muted-foreground flex items-start gap-2 py-1 text-xs">
          <KeyboardIcon className="mt-0.5 size-3.5 shrink-0" aria-hidden />
          <span>{mn.learn.needsInput}</span>
        </p>
      )}

      {isEmpty && (
        <p className="text-muted-foreground py-0.5 text-xs italic">
          Код амжилттай ажиллалаа. Гаралт байхгүй.
        </p>
      )}

      <div ref={endRef} />
    </div>
  );
}

/**
 * Хөрвүүлэгчийн мессеж.
 *
 * `^` заагч нь алдаатай баганын яг доор байх ёстой тул мөрийг ороохгүй
 * (`whitespace-pre`) — урт мөрийг хажуу тийш гүйлгэнэ.
 */
export function Diagnostics({
  tone,
  title,
  text,
}: {
  tone: "warning" | "error";
  title: string;
  text: string;
}) {
  return (
    <div
      className={cn(
        "flex items-start gap-2 py-1",
        tone === "error" ? "text-destructive" : "text-amber-600 dark:text-amber-400",
      )}
    >
      <AlertTriangleIcon className="mt-0.5 size-3.5 shrink-0" aria-hidden />
      <div className="min-w-0 flex-1">
        <p className="font-sans text-xs font-medium">{title}</p>
        <pre className="overflow-x-auto whitespace-pre">{text}</pre>
      </div>
    </div>
  );
}

function ConsoleShell({ children, muted }: { children: React.ReactNode; muted?: boolean }) {
  return (
    <div
      className={cn(
        "flex h-full items-start p-3 font-mono text-[13px]",
        muted && "text-muted-foreground",
      )}
    >
      {children}
    </div>
  );
}
