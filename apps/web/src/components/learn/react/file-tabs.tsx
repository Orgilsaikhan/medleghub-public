"use client";

import { FileCodeIcon, LockIcon } from "lucide-react";
import { useRef, type KeyboardEvent, type ReactNode } from "react";

import { mn } from "@/lib/i18n/mn";
import type { LessonFile } from "@/lib/sandbox/react/files";
import { cn } from "@/lib/utils";

interface FileTabsProps {
  files: LessonFile[];
  active: string;
  onSelect: (name: string) => void;
  /** `id` — tabpanel-ийн `aria-labelledby`. */
  idPrefix: string;
  /** Баруун талын үйлдлүүд — «Дахин эхлүүлэх». */
  actions?: ReactNode;
}

/** `components/Header.jsx` → `Header.jsx`, давхцвал бүтэн зам. */
function tabLabels(files: LessonFile[]): string[] {
  const base = files.map((file) => file.name.split("/").pop() ?? file.name);
  return files.map((file, index) =>
    base.filter((name) => name === base[index]).length > 1 ? file.name : base[index],
  );
}

/**
 * `App.jsx | 🔒 main.jsx | 🔒 index.html` — react-tutorial.app шиг файлууд
 * тусдаа tab-д. Түгжигдсэн файл нь зөвхөн уншигдана.
 *
 * WAI-ARIA tabs: сумаар шилжиж, Home/End-ээр эхний/сүүлийн файл руу үсэрнэ.
 */
export function FileTabs({ files, active, onSelect, idPrefix, actions }: FileTabsProps) {
  const listRef = useRef<HTMLDivElement>(null);
  const labels = tabLabels(files);

  const onKeyDown = (event: KeyboardEvent<HTMLButtonElement>, index: number) => {
    const last = files.length - 1;
    const next =
      event.key === "ArrowRight"
        ? index === last
          ? 0
          : index + 1
        : event.key === "ArrowLeft"
          ? index === 0
            ? last
            : index - 1
          : event.key === "Home"
            ? 0
            : event.key === "End"
              ? last
              : null;
    if (next === null) return;
    event.preventDefault();
    onSelect(files[next].name);
    listRef.current?.querySelectorAll<HTMLButtonElement>("[role=tab]")[next]?.focus();
  };

  return (
    <div className="bg-muted/60 flex shrink-0 items-stretch border-b">
      <div
        ref={listRef}
        role="tablist"
        aria-label={mn.learn.react.files}
        className="flex min-w-0 flex-1 overflow-x-auto"
      >
        {files.map((file, index) => {
          const selected = file.name === active;
          return (
            <button
              key={file.name}
              type="button"
              role="tab"
              id={`${idPrefix}-tab-${index}`}
              aria-selected={selected}
              aria-controls={`${idPrefix}-panel`}
              tabIndex={selected ? 0 : -1}
              onClick={() => onSelect(file.name)}
              onKeyDown={(event) => onKeyDown(event, index)}
              title={file.locked ? `${file.name} — ${mn.learn.react.lockedMessage}` : file.name}
              className={cn(
                "relative flex shrink-0 items-center gap-1.5 border-r px-3 py-2 font-mono text-xs transition-colors",
                "focus-visible:ring-ring focus-visible:ring-2 focus-visible:outline-none focus-visible:ring-inset",
                selected
                  ? "bg-background text-foreground after:bg-primary after:absolute after:inset-x-0 after:top-0 after:h-0.5"
                  : "text-muted-foreground hover:text-foreground",
              )}
            >
              {file.locked ? (
                <LockIcon className="size-3" aria-hidden />
              ) : (
                <FileCodeIcon className="size-3" aria-hidden />
              )}
              {labels[index]}
              {labels[index] !== file.name && <span className="sr-only"> ({file.name})</span>}
              {file.locked && <span className="sr-only"> ({mn.learn.react.locked})</span>}
            </button>
          );
        })}
      </div>
      {actions && <div className="flex shrink-0 items-center gap-1 px-2">{actions}</div>}
    </div>
  );
}
