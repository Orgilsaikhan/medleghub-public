"use client";

import { ChevronDownIcon, ChevronUpIcon, Trash2Icon } from "lucide-react";

import { ConsoleOutput } from "@/components/learn/console-output";
import { Button } from "@/components/ui/button";
import { mn } from "@/lib/i18n/mn";
import type { ConsoleEntry } from "@/lib/sandbox/runner";
import { cn } from "@/lib/utils";

interface ConsolePanelProps {
  entries: ConsoleEntry[];
  open: boolean;
  onToggle: () => void;
  onClear: () => void;
  className?: string;
}

/** «Хөтөч»-ийн console — `console.log`, React-ийн анхааруулга, алдаа. */
export function ConsolePanel({ entries, open, onToggle, onClear, className }: ConsolePanelProps) {
  const title = mn.learn.console;
  return (
    <section
      aria-label={title}
      className={cn(
        "flex shrink-0 flex-col border-t transition-[height] duration-150",
        open ? "h-48 xl:h-56" : "h-11",
        className,
      )}
    >
      <div className="flex shrink-0 items-center gap-2 border-b px-3 py-1.5">
        <button
          type="button"
          onClick={onToggle}
          aria-expanded={open}
          title={open ? mn.learn.react.panelHide(title) : mn.learn.react.panelShow(title)}
          className="hover:text-foreground -mx-1.5 flex items-center gap-1.5 rounded px-1.5 py-0.5 text-sm font-semibold"
        >
          {open ? (
            <ChevronDownIcon className="size-3.5" aria-hidden />
          ) : (
            <ChevronUpIcon className="size-3.5" aria-hidden />
          )}
          {title}
          {!open && entries.length > 0 && (
            <span className="text-muted-foreground font-mono text-xs font-normal tabular-nums">
              ({entries.length})
            </span>
          )}
        </button>
        <Button
          variant="ghost"
          size="sm"
          className="ml-auto h-8 px-2"
          onClick={onClear}
          disabled={entries.length === 0}
          aria-label={mn.learn.clearConsole}
          title={mn.learn.clearConsole}
        >
          <Trash2Icon className="size-3.5" />
        </Button>
      </div>
      {open && (
        <div className="bg-code-bg min-h-0 flex-1">
          <ConsoleOutput
            result={
              entries.length > 0
                ? { entries, truncated: false, error: null, timedOut: false, durationMs: 0 }
                : null
            }
            isRunning={false}
            emptyText={mn.learn.react.consoleEmpty}
          />
        </div>
      )}
    </section>
  );
}
