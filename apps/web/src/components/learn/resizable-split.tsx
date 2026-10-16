"use client";

import { ChevronDownIcon, ChevronUpIcon } from "lucide-react";
import { useCallback, useRef, useState } from "react";

import { readLocalNumber, writeLocal } from "@/lib/local-storage";
import { cn } from "@/lib/utils";

/**
 * Босоо чиглэлд хуваагдсан, чирж хэмжээг нь өөрчилж болох хоёр хэсэг.
 *
 * ЯАГААД ХУВИЙГ ХАДГАЛДАГ ВЭ (px биш)
 * ───────────────────────────────────
 * Цонхны өндөр өөрчлөгдөхөд харьцаа хадгалагдана — цонхыг жижигрүүлэхэд
 * доод хэсэг алга болохгүй. Мөн `role="separator"` нь фокустай үедээ
 * `aria-valuenow` шаарддаг бөгөөд хувь нь шууд тохирно (WCAG 4.1.2).
 *
 * Гараар ажиллуулах: сум дээш/доош нь 4%-иар, Home нь бүрэн эвхэж, End нь
 * дээд хязгаарт хүргэнэ (WCAG 2.1.1 — хулганагүйгээр бүх үйлдэл хийгдэнэ).
 */

/** Дээд хэсгийн хамгийн их эзлэх хувь — доод хэсэг үргэлж харагдана. */
const MAX_TOP = 80;
const STEP = 4;

interface ResizableSplitProps {
  top: React.ReactNode;
  bottom: React.ReactNode;
  /** `localStorage`-д хадгалах түлхүүр. Хичээл солигдоход хэмжээ хадгалагдана. */
  storageKey: string;
  /** Анхдагч хувь (дээд хэсэг). */
  defaultTop?: number;
  label: string;
  className?: string;
}

function readStored(key: string, fallback: number): number {
  return Math.min(MAX_TOP, Math.max(0, readLocalNumber(key, fallback)));
}

function store(key: string, value: number) {
  writeLocal(key, String(value));
}

export function ResizableSplit({
  top,
  bottom,
  storageKey,
  defaultTop = 45,
  label,
  className,
}: ResizableSplitProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [topPercent, setTopPercent] = useState(() => readStored(storageKey, defaultTop));
  const [dragging, setDragging] = useState(false);

  // Эвхэхээс өмнөх хэмжээ — дахин нээхэд байрандаа буцна.
  const restoreRef = useRef(defaultTop);

  const commit = useCallback((next: number) => {
    const clamped = Math.min(MAX_TOP, Math.max(0, next));
    setTopPercent(clamped);
    return clamped;
  }, []);

  const handlePointerDown = useCallback((event: React.PointerEvent<HTMLDivElement>) => {
    const container = containerRef.current;
    if (!container) return;

    event.preventDefault();
    event.currentTarget.setPointerCapture(event.pointerId);
    setDragging(true);
  }, []);

  const handlePointerMove = useCallback(
    (event: React.PointerEvent<HTMLDivElement>) => {
      if (!dragging) return;
      const container = containerRef.current;
      if (!container) return;

      const rect = container.getBoundingClientRect();
      if (rect.height === 0) return;

      commit(((event.clientY - rect.top) / rect.height) * 100);
    },
    [dragging, commit],
  );

  const handlePointerUp = useCallback(
    (event: React.PointerEvent<HTMLDivElement>) => {
      if (!dragging) return;
      event.currentTarget.releasePointerCapture(event.pointerId);
      setDragging(false);
      if (topPercent > 0) restoreRef.current = topPercent;
      store(storageKey, topPercent);
    },
    [dragging, topPercent, storageKey],
  );

  const handleKeyDown = useCallback(
    (event: React.KeyboardEvent<HTMLDivElement>) => {
      const moves: Record<string, number | undefined> = {
        ArrowUp: topPercent - STEP,
        ArrowDown: topPercent + STEP,
        Home: 0,
        End: MAX_TOP,
      };
      const next = moves[event.key];
      if (next === undefined) return;

      event.preventDefault();
      const applied = commit(next);
      if (applied > 0) restoreRef.current = applied;
      store(storageKey, applied);
    },
    [topPercent, commit, storageKey],
  );

  const collapsed = topPercent <= 0;

  const toggle = useCallback(() => {
    const next = collapsed ? Math.max(STEP, restoreRef.current) : 0;
    if (!collapsed) restoreRef.current = topPercent;
    commit(next);
    store(storageKey, next);
  }, [collapsed, topPercent, commit, storageKey]);

  return (
    <div
      ref={containerRef}
      className={cn("flex min-h-0 flex-1 flex-col", dragging && "select-none", className)}
    >
      <div
        className="min-h-0 overflow-hidden"
        style={{ flex: `0 0 ${topPercent}%` }}
        // Эвхэгдсэн үед доторх агуулга нь фокус авахгүй байх ёстой.
        inert={collapsed}
      >
        {top}
      </div>

      {/* Чирэх зурвас ба эвхэх товч нэг мөрөнд. Товч нь тусдаа элемент тул
          чирэх үйлдэлтэй зөрчилдөхгүй. */}
      <div className="bg-muted/30 flex h-7 shrink-0 items-center border-y">
        <div
          className={cn(
            "group flex h-full flex-1 cursor-row-resize touch-none items-center justify-center",
            "hover:bg-muted focus-visible:ring-ring transition-colors",
            "focus-visible:ring-2 focus-visible:-outline-offset-2 focus-visible:outline-none",
            dragging && "bg-primary/20",
          )}
          role="separator"
          aria-orientation="horizontal"
          aria-label={label}
          aria-valuenow={Math.round(topPercent)}
          aria-valuemin={0}
          aria-valuemax={MAX_TOP}
          tabIndex={0}
          onPointerDown={handlePointerDown}
          onPointerMove={handlePointerMove}
          onPointerUp={handlePointerUp}
          onPointerCancel={handlePointerUp}
          onKeyDown={handleKeyDown}
        >
          <span
            aria-hidden
            className="bg-border group-hover:bg-muted-foreground/50 h-0.5 w-10 rounded-full transition-colors"
          />
        </div>

        <button
          type="button"
          onClick={toggle}
          aria-expanded={!collapsed}
          className={cn(
            "text-muted-foreground hover:text-foreground hover:bg-muted",
            "focus-visible:ring-ring flex h-full shrink-0 items-center gap-1.5 px-3",
            "text-xs focus-visible:ring-2 focus-visible:-outline-offset-2 focus-visible:outline-none",
          )}
        >
          {collapsed ? (
            <ChevronDownIcon className="size-3.5" aria-hidden />
          ) : (
            <ChevronUpIcon className="size-3.5" aria-hidden />
          )}
          <span className="hidden sm:inline">{label}</span>
        </button>
      </div>

      <div className="flex min-h-0 flex-1 flex-col">{bottom}</div>
    </div>
  );
}
