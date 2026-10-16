"use client";

import { CircleCheckIcon, LoaderCircleIcon } from "lucide-react";
import { createContext, useContext, type ComponentPropsWithoutRef, type ReactNode } from "react";

import { mn } from "@/lib/i18n/mn";
import { cn } from "@/lib/utils";

/**
 * Баримт хэвлэгч — төлбөр амжилттай болоход баримт принтерээс гарч ирнэ.
 *
 *     <ReceiptPrinter.Root stage="printing">
 *       <ReceiptPrinter.Machine>
 *         <ReceiptPrinter.Header>…</ReceiptPrinter.Header>
 *         <ReceiptPrinter.Screen>… <ReceiptPrinter.Status /></ReceiptPrinter.Screen>
 *       </ReceiptPrinter.Machine>
 *       <ReceiptPrinter.Output>
 *         <ReceiptPrinter.Paper>…</ReceiptPrinter.Paper>
 *       </ReceiptPrinter.Output>
 *     </ReceiptPrinter.Root>
 *
 * `processing` → цаас нуугдмал; `printing` → цаас 1.75 секундэд мөр мөрөөр
 * («stepped») эсвэл жигд («smooth») гарна; `complete` → бүрэн гарсан. Хөдөлгөөнийг
 * CSS keyframe (`globals.css`) хийдэг — хөдөлгөөн багасгах тохиргоотой бол шууд
 * харагдана. Баримтыг зөвхөн `complete` үед дэлгэц уншигчид нээнэ.
 */

export type ReceiptPrinterStage = "processing" | "printing" | "complete";
export type ReceiptFeedMotion = "smooth" | "stepped";

type RootProps = Omit<ComponentPropsWithoutRef<"section">, "children"> & {
  children: ReactNode;
  /** Цаас мөр мөрөөр (`stepped`) эсвэл жигд (`smooth`) гарах. */
  feedMotion?: ReceiptFeedMotion;
  stage: ReceiptPrinterStage;
};

interface PrinterContext {
  feedMotion: ReceiptFeedMotion;
  stage: ReceiptPrinterStage;
}

const PrinterContext = createContext<PrinterContext | null>(null);

function usePrinter(component: string): PrinterContext {
  const context = useContext(PrinterContext);
  if (!context) throw new Error(`${component} нь ReceiptPrinter.Root дотор байна.`);
  return context;
}

/** Цаасны доод ирмэгийн шүд — дулааны цаасыг урж авсан мэт. */
const TOOTH_COUNT = 40;
const TOOTH_DEPTH = 4;
const toothPoints = Array.from({ length: TOOTH_COUNT * 2 }, (_, index) => {
  const x = 100 - ((index + 1) * 100) / (TOOTH_COUNT * 2);
  const y = index % 2 === 0 ? "100%" : `calc(100% - ${TOOTH_DEPTH}px)`;
  return `${x}% ${y}`;
}).join(", ");
const PAPER_CLIP = `polygon(0 0, 100% 0, 100% calc(100% - ${TOOTH_DEPTH}px), ${toothPoints})`;

function Root({
  children,
  className,
  feedMotion = "stepped",
  stage,
  "aria-label": ariaLabel = mn.billing.receipt.printer,
  ...props
}: RootProps) {
  return (
    <PrinterContext.Provider value={{ feedMotion, stage }}>
      <section
        aria-label={ariaLabel}
        data-stage={stage}
        className={cn("relative isolate flex w-full max-w-sm flex-col items-center", className)}
        {...props}
      >
        {children}
      </section>
    </PrinterContext.Provider>
  );
}

/** Принтерийн их бие — бараан хуванцар, доод талд цаас гарах нүх. */
function Machine({ children, className, ...props }: ComponentPropsWithoutRef<"div">) {
  return (
    <div
      className={cn(
        "relative isolate w-full overflow-hidden rounded-3xl border p-3 pb-8",
        "border-zinc-900 bg-zinc-800 text-zinc-100",
        "shadow-[0_20px_36px_-20px_rgb(0_0_0/0.55),0_6px_14px_-8px_rgb(0_0_0/0.25),inset_0_1px_0_rgb(255_255_255/0.08),inset_0_-1px_0_rgb(0_0_0/0.5)]",
        "dark:border-zinc-600 dark:bg-zinc-700",
        "before:pointer-events-none before:absolute before:inset-0 before:z-0 before:rounded-[inherit]",
        "before:bg-[url('/textures/plastic-noise.svg')] before:bg-[length:180px_180px] before:bg-repeat",
        "before:opacity-25 before:mix-blend-overlay before:content-['']",
        className,
      )}
      {...props}
    >
      {children}
      <div
        aria-hidden
        className="absolute inset-x-6 bottom-3 z-40 h-2 rounded-sm border border-black bg-black shadow-inner"
      />
    </div>
  );
}

function Header({ children, className, ...props }: ComponentPropsWithoutRef<"div">) {
  return (
    <div
      className={cn("relative z-10 flex h-11 items-start justify-between gap-3", className)}
      {...props}
    >
      {children}
    </div>
  );
}

/** Жижиг хар дэлгэц — захиалгын товч мэдээлэл ба төлөв. */
function Screen({ children, className, ...props }: ComponentPropsWithoutRef<"div">) {
  return (
    <div
      className={cn(
        "relative isolate z-10 overflow-hidden rounded-xl border border-black bg-zinc-950 p-4 text-zinc-100",
        "shadow-inner after:pointer-events-none after:absolute after:inset-0 after:z-20 after:rounded-[inherit]",
        "after:shadow-[inset_0_0_24px_4px_rgb(0_0_0/0.5)] after:content-['']",
        className,
      )}
      {...props}
    >
      <div className="relative z-10">{children}</div>
    </div>
  );
}

function Status({ children, className, ...props }: ComponentPropsWithoutRef<"div">) {
  const { stage } = usePrinter("ReceiptPrinter.Status");
  const complete = stage === "complete";

  return (
    <div className={cn("flex min-w-0 items-center gap-2", className)} {...props}>
      <span aria-hidden className="grid size-5 shrink-0 place-items-center">
        {complete ? (
          <CircleCheckIcon
            key="complete"
            className="animate-in zoom-in-90 fade-in-0 size-[18px] text-emerald-400 duration-150"
          />
        ) : (
          <LoaderCircleIcon
            key="working"
            className="size-[18px] animate-spin text-zinc-400 motion-reduce:animate-none"
          />
        )}
      </span>
      <div role="status" aria-live="polite" className="grid min-w-0 flex-1 items-center">
        {/* `key` солигдоход шинэ бичвэр доороос гулсаж гарна. */}
        <span
          key={stage}
          className="animate-in fade-in-0 slide-in-from-bottom-1 truncate text-xs leading-none font-medium text-zinc-300 duration-200"
        >
          {children ?? mn.billing.receipt.status[stage]}
        </span>
      </div>
    </div>
  );
}

/** Цаас гарах хэсэг — цаас нүхнээс дээш нуугдмал байж, доош гулсаж гарна. */
function Output({ children, className, ...props }: ComponentPropsWithoutRef<"div">) {
  const { feedMotion, stage } = usePrinter("ReceiptPrinter.Output");
  const visible = stage !== "processing";

  return (
    <div
      className={cn(
        "relative z-50 -mt-4 w-[calc(80%+3rem)] max-w-full overflow-hidden px-6",
        className,
      )}
      {...props}
    >
      {visible && (
        <div
          aria-hidden
          className="pointer-events-none absolute inset-x-6 -top-1 z-20 h-2 bg-black/70 blur-[6px]"
        />
      )}
      <div
        aria-hidden={stage !== "complete"}
        className={cn(
          "relative isolate transition-opacity duration-150",
          // Цаасны сүүдэр.
          "before:pointer-events-none before:absolute before:inset-x-3 before:top-3 before:bottom-4 before:z-0",
          "before:rounded-sm before:shadow-[0_8px_24px_rgb(0_0_0/0.22)] before:content-['']",
          visible ? "opacity-100" : "-translate-y-[calc(100%-2px)] opacity-0",
          stage === "printing" &&
            (feedMotion === "stepped" ? "receipt-feed-stepped" : "receipt-feed-smooth"),
        )}
      >
        {children}
      </div>
    </div>
  );
}

/** Дулааны цаас — цагаан, үзэг бичгийн фонт, доод ирмэг нь шүдтэй. */
function Paper({ children, className, style, ...props }: ComponentPropsWithoutRef<"article">) {
  return (
    <article
      className={cn(
        "relative z-10 min-h-80 bg-zinc-50 bg-[url('/textures/receipt-paper.svg')] bg-cover px-6 pt-7 pb-8",
        "font-mono text-zinc-900 bg-blend-multiply",
        className,
      )}
      style={{ clipPath: PAPER_CLIP, ...style }}
      {...props}
    >
      {children}
    </article>
  );
}

export const ReceiptPrinter = { Root, Machine, Header, Screen, Status, Output, Paper };
