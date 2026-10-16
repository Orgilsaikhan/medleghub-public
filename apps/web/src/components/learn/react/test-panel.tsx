"use client";

import {
  ArrowRightIcon,
  ChevronDownIcon,
  ChevronUpIcon,
  CircleCheckIcon,
  CircleIcon,
  CircleXIcon,
  LoaderCircleIcon,
  PlayIcon,
} from "lucide-react";
import Link from "next/link";
import type { ReactNode } from "react";

import { Button } from "@/components/ui/button";
import { mn } from "@/lib/i18n/mn";
import type { ReactTestResult } from "@/lib/sandbox/react/runner";
import { cn } from "@/lib/utils";

export type TestSlot = ReactTestResult | "running" | undefined;

export interface TestNote {
  tone: "success" | "info" | "error";
  text: string;
}

interface TestPanelProps {
  names: string[];
  results: TestSlot[];
  running: boolean;
  note?: TestNote;
  open: boolean;
  onToggle: () => void;
  onRun: () => void;
  /** «Тусламж» — шийдэл ба зөвлөгөө (react-tutorial-ийн «Solution»). */
  helpAction?: ReactNode;
  nextHref?: string | null;
  className?: string;
}

/**
 * «Тестүүд (1 / 3)» — react-tutorial.app-ийн адил бүх шаардлага эхнээсээ
 * жагсаалтаар харагдана. «Ажиллуулах» нь кодыг «Хөтөч» дээр дахин ачаалж,
 * зэрэг тестүүдийг шалгана. Амжилтгүй тестийн доор шалтгаан нь бичигдэнэ.
 */
export function TestPanel({
  names,
  results,
  running,
  note,
  open,
  onToggle,
  onRun,
  helpAction,
  nextHref,
  className,
}: TestPanelProps) {
  const hasTests = names.length > 0;
  const passed = results.filter((result) => typeof result === "object" && result.passed).length;
  const title = hasTests
    ? mn.learn.react.testsTitle(passed, names.length)
    : mn.learn.react.noTestsTitle;

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
          className="hover:text-foreground -mx-1.5 flex min-w-0 items-center gap-1.5 rounded px-1.5 py-0.5 text-sm font-semibold"
        >
          {open ? (
            <ChevronDownIcon className="size-3.5 shrink-0" aria-hidden />
          ) : (
            <ChevronUpIcon className="size-3.5 shrink-0" aria-hidden />
          )}
          <span className="truncate tabular-nums">{title}</span>
        </button>
        <div className="ml-auto flex shrink-0 items-center gap-1.5">
          {helpAction}
          <Button
            size="sm"
            onClick={onRun}
            disabled={running}
            title={hasTests ? mn.learn.react.runHint : mn.learn.react.runNoTestsHint}
          >
            {running ? (
              <LoaderCircleIcon className="size-3.5 animate-spin" />
            ) : (
              <PlayIcon className="size-3.5" />
            )}
            {running ? mn.learn.react.running : mn.learn.react.run}
          </Button>
        </div>
      </div>

      {open && (
        <div className="min-h-0 flex-1 overflow-y-auto" aria-live="polite">
          {note && (
            <div
              role="status"
              className={cn(
                "flex flex-wrap items-center gap-x-3 gap-y-1 border-b px-3 py-2 text-sm",
                note.tone === "success" && "text-success",
                note.tone === "error" && "text-destructive",
              )}
            >
              <span>{note.text}</span>
              {note.tone === "success" && nextHref && (
                <Link
                  href={nextHref}
                  className="text-brand-link inline-flex items-center gap-1 font-medium underline-offset-4 hover:underline"
                >
                  {mn.learn.react.nextLesson}
                  <ArrowRightIcon className="size-3.5" aria-hidden />
                </Link>
              )}
            </div>
          )}

          {hasTests ? (
            <ul className="divide-y">
              {names.map((name, index) => (
                <TestRow key={index} name={name} slot={results[index]} />
              ))}
            </ul>
          ) : (
            <p className="text-muted-foreground p-3 text-sm">{mn.learn.react.noTests}</p>
          )}
        </div>
      )}
    </section>
  );
}

function TestRow({ name, slot }: { name: string; slot: TestSlot }) {
  const state =
    slot === undefined
      ? "pending"
      : slot === "running"
        ? "running"
        : slot.passed
          ? "passed"
          : "failed";
  const label = {
    pending: mn.learn.react.testPending,
    running: mn.learn.react.testRunning,
    passed: mn.learn.react.testPassed,
    failed: mn.learn.react.testFailed,
  }[state];

  return (
    <li className="px-3 py-2">
      <div className="flex items-start gap-2 text-sm">
        {state === "passed" ? (
          <CircleCheckIcon className="text-success mt-0.5 size-4 shrink-0" aria-hidden />
        ) : state === "failed" ? (
          <CircleXIcon className="text-destructive mt-0.5 size-4 shrink-0" aria-hidden />
        ) : state === "running" ? (
          <LoaderCircleIcon
            className="text-muted-foreground mt-0.5 size-4 shrink-0 animate-spin"
            aria-hidden
          />
        ) : (
          <CircleIcon className="text-muted-foreground mt-0.5 size-4 shrink-0" aria-hidden />
        )}
        <span className={cn("min-w-0", state === "pending" && "text-muted-foreground")}>
          {name}
          <span className="sr-only"> — {label}</span>
        </span>
      </div>
      {typeof slot === "object" && !slot.passed && slot.message && (
        <p className="text-destructive mt-1 ml-6 font-mono text-xs leading-relaxed break-words whitespace-pre-wrap">
          {slot.message}
        </p>
      )}
    </li>
  );
}
