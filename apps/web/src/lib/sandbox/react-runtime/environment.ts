/**
 * Iframe-ийн орчин: console, localStorage, alert, холбоос/форм, timer.
 *
 * Iframe нь `sandbox="allow-scripts allow-forms"` — өөрийн (opaque) origin-той
 * тул `localStorage` нь SecurityError шидэж, `alert` чимээгүй хаагдана.
 * Хичээлүүд эдгээрийг хэрэглэдэг тул санах ойн хувилбараар орлуулна.
 */

import { formatArgs } from "@/lib/sandbox/react-runtime/format";
import { LOOP_GUARD } from "@/lib/sandbox/react-runtime/transform";
import type { ConsoleLevel } from "@/lib/sandbox/react/protocol";

export interface LogEntry {
  level: ConsoleLevel;
  text: string;
}

const MAX_ENTRIES = 500;

// --- Console ------------------------------------------------------------

export function captureConsole(onEntry: (entry: LogEntry) => void): void {
  let count = 0;
  const record =
    (level: ConsoleLevel) =>
    (...args: unknown[]) => {
      if (count >= MAX_ENTRIES) return;
      count += 1;
      onEntry({ level, text: formatArgs(args) });
      if (count === MAX_ENTRIES) {
        onEntry({ level: "warn", text: `… console ${MAX_ENTRIES} мөрөөс хэтэрсэн тул таслав.` });
      }
    };
  const target = console as unknown as Record<string, unknown>;
  target.log = record("log");
  target.debug = record("log");
  target.table = record("log");
  target.dir = record("log");
  target.trace = record("log");
  target.group = record("log");
  target.groupCollapsed = record("log");
  target.info = record("info");
  target.warn = record("warn");
  target.error = record("error");
  target.groupEnd = () => {};
  target.assert = (condition: unknown, ...rest: unknown[]) => {
    if (!condition) record("error")("Assertion failed:", ...rest);
  };
}

// --- localStorage --------------------------------------------------------

export class MemoryStorage {
  private items = new Map<string, string>();

  constructor(
    initial: Record<string, string> = {},
    private onChange?: (data: Record<string, string>) => void,
  ) {
    for (const [key, value] of Object.entries(initial)) this.items.set(key, String(value));
  }

  get length(): number {
    return this.items.size;
  }

  key(index: number): string | null {
    return [...this.items.keys()][index] ?? null;
  }

  getItem(key: string): string | null {
    return this.items.get(String(key)) ?? null;
  }

  setItem(key: string, value: unknown): void {
    this.items.set(String(key), String(value));
    this.changed();
  }

  removeItem(key: string): void {
    this.items.delete(String(key));
    this.changed();
  }

  clear(): void {
    this.items.clear();
    this.changed();
  }

  snapshot(): Record<string, string> {
    return Object.fromEntries(this.items);
  }

  private changed(): void {
    this.onChange?.(this.snapshot());
  }
}

export function installStorage(local: MemoryStorage, session: MemoryStorage): void {
  Object.defineProperty(window, "localStorage", { configurable: true, get: () => local });
  Object.defineProperty(window, "sessionStorage", { configurable: true, get: () => session });
}

// --- alert, холбоос, форм ---------------------------------------------------

export function installBrowserShims(): void {
  window.alert = (message?: unknown) => console.info(`alert: ${String(message ?? "")}`);
  window.confirm = (message?: string) => {
    console.info(`confirm: ${message ?? ""} → true`);
    return true;
  };
  window.prompt = (message?: string, fallback?: string) => {
    console.info(`prompt: ${message ?? ""} → "${fallback ?? ""}"`);
    return fallback ?? "";
  };

  // React-ийн handler-ууд root дээр ажилладаг тул document-ийн bubble
  // үе шатанд л «preventDefault хийгээгүй» эсэхийг зөв мэднэ.
  document.addEventListener("click", (event) => {
    if (event.defaultPrevented) return;
    const link = (event.target as Element | null)?.closest?.("a[href]");
    if (!link) return;
    const href = link.getAttribute("href") ?? "";
    if (href.startsWith("#")) return;
    event.preventDefault();
    console.info(
      `Холбоос «${href}» — sandbox дотор өөр хуудас руу шилжихгүй. Апп доторх хуудсуудад react-router-ийн <Link> ашиглана.`,
    );
  });

  document.addEventListener("submit", (event) => {
    if (event.defaultPrevented) return;
    event.preventDefault();
    console.warn(
      "Форм илгээгдэж хуудас дахин ачаалагдах гэлээ — onSubmit дотор e.preventDefault() дуудаагүй байна.",
    );
  });
}

// --- Төгсгөлгүй давталт ------------------------------------------------------

/** Event loop үүнээс удаан гацвал давталт тасарна. */
const LOOP_LIMIT_MS = 2000;

export function installLoopGuard(): void {
  let lastBeat = performance.now();
  setInterval(() => {
    lastBeat = performance.now();
  }, 100);
  let calls = 0;
  (globalThis as Record<string, unknown>)[LOOP_GUARD] = () => {
    if ((++calls & 1023) !== 0) return;
    if (performance.now() - lastBeat > LOOP_LIMIT_MS) {
      throw new RangeError(
        "Давталт 2 секундээс удаан үргэлжилсэн тул зогсоов — төгсгөлгүй давталт байж магадгүй. Давталтын нөхцөлөө шалга.",
      );
    }
  };
}

// --- Timer-ийг тестийн хооронд цэвэрлэх -----------------------------------------

export function trackTimers(): { clearAll: () => void } {
  const timeouts = new Set<number>();
  const intervals = new Set<number>();
  const frames = new Set<number>();

  const { setTimeout: nativeTimeout, setInterval: nativeInterval } = window;
  const { clearTimeout: nativeClearTimeout, clearInterval: nativeClearInterval } = window;
  const nativeFrame = window.requestAnimationFrame.bind(window);
  const nativeCancelFrame = window.cancelAnimationFrame.bind(window);

  window.setTimeout = ((handler: TimerHandler, timeout?: number, ...args: unknown[]) => {
    const id = nativeTimeout(
      (...inner: unknown[]) => {
        timeouts.delete(id);
        if (typeof handler === "function") handler(...inner);
      },
      timeout,
      ...args,
    );
    timeouts.add(id);
    return id;
  }) as typeof window.setTimeout;
  window.clearTimeout = ((id?: number) => {
    if (id !== undefined) timeouts.delete(id);
    nativeClearTimeout(id);
  }) as typeof window.clearTimeout;
  window.setInterval = ((handler: TimerHandler, timeout?: number, ...args: unknown[]) => {
    const id = nativeInterval(handler, timeout, ...args);
    intervals.add(id);
    return id;
  }) as typeof window.setInterval;
  window.clearInterval = ((id?: number) => {
    if (id !== undefined) intervals.delete(id);
    nativeClearInterval(id);
  }) as typeof window.clearInterval;
  window.requestAnimationFrame = (callback: FrameRequestCallback) => {
    const id = nativeFrame((time) => {
      frames.delete(id);
      callback(time);
    });
    frames.add(id);
    return id;
  };
  window.cancelAnimationFrame = (id: number) => {
    frames.delete(id);
    nativeCancelFrame(id);
  };

  return {
    clearAll() {
      for (const id of timeouts) nativeClearTimeout(id);
      for (const id of intervals) nativeClearInterval(id);
      for (const id of frames) nativeCancelFrame(id);
      timeouts.clear();
      intervals.clear();
      frames.clear();
    },
  };
}

// --- Алдааны байршил ---------------------------------------------------------

/** Stack-аас сурагчийн файлын эхний мөрийг олно: «App.jsx:12:5». */
export function locate(
  error: unknown,
  files: Iterable<string>,
): { file: string; line: number; column: number } | undefined {
  const stack = error instanceof Error ? (error.stack ?? "") : "";
  const names = new Set(files);
  for (const match of stack.matchAll(/([\w./-]+\.(?:jsx|js|mjs)):(\d+):(\d+)/g)) {
    const file = match[1].replace(/^.*\//, "");
    const full = [...names].find(
      (name) => name === match[1] || name.endsWith(`/${file}`) || name === file,
    );
    if (full) return { file: full, line: Number(match[2]), column: Number(match[3]) };
  }
  return undefined;
}
