/**
 * Сурагчийн өөрийн тест файл (`App.test.jsx`) — «Модул 13 — Тест».
 *
 * Бодит төсөлтэй ИЖИЛ импорт ажиллана:
 *
 *     import { test, expect, vi } from "vitest";
 *     import { render, screen } from "@testing-library/react";
 *     import userEvent from "@testing-library/user-event";
 *
 * Эдгээр нь `testing.ts`-ийн жижиг хувилбар руу холбогдоно. «Хөтөч» дээр
 * Vitest шиг үр дүнгийн жагсаалт гарна. Дасгалын тест нь `runTestFile`-ээр
 * сурагчийн тестийг зөв болон зориуд эвдэрсэн component дээр ажиллуулж
 * шалгана.
 */

import { act } from "react";

import type { ModuleSystem } from "@/lib/sandbox/react-runtime/modules";
import {
  cleanupRendered,
  expect,
  fn,
  render,
  screen,
  user,
  waitFor,
  within,
} from "@/lib/sandbox/react-runtime/testing";

type Hook = () => unknown;

interface Registered {
  name: string;
  run: () => unknown;
  before: Hook[];
  after: Hook[];
}

interface Collector {
  tests: Registered[];
  prefix: string[];
  before: Hook[];
  after: Hook[];
}

export interface FileTestResult {
  name: string;
  passed: boolean;
  message?: string;
  durationMs: number;
}

let collector: Collector | null = null;

function current(name: string): Collector {
  if (!collector) throw new Error(`${name}() нь зөвхөн *.test.jsx файл дотор ажиллана.`);
  return collector;
}

function test(name: string, run: () => unknown) {
  const target = current("test");
  target.tests.push({
    name: [...target.prefix, name].join(" › "),
    run,
    before: [...target.before],
    after: [...target.after],
  });
}

function describe(name: string, body: () => void) {
  const target = current("describe");
  target.prefix.push(name);
  try {
    body();
  } finally {
    target.prefix.pop();
  }
}

const vitest = {
  test,
  it: test,
  describe,
  expect,
  vi: { fn },
  beforeEach: (hook: Hook) => current("beforeEach").before.push(hook),
  afterEach: (hook: Hook) => current("afterEach").after.push(hook),
};

function setValue(element: Element, value: string) {
  const prototype =
    element instanceof HTMLTextAreaElement
      ? HTMLTextAreaElement.prototype
      : element instanceof HTMLSelectElement
        ? HTMLSelectElement.prototype
        : HTMLInputElement.prototype;
  Object.getOwnPropertyDescriptor(prototype, "value")?.set?.call(element, value);
}

/** Хуучин `fireEvent` — `userEvent`-ийг илүүд үзнэ. */
const fireEvent = {
  click: (element: Element) => act(() => (element as HTMLElement).click()),
  change: (element: Element, init: { target: { value?: string; checked?: boolean } }) =>
    act(() => {
      if (init.target.value !== undefined) setValue(element, init.target.value);
      if (init.target.checked !== undefined)
        (element as HTMLInputElement).checked = init.target.checked;
      element.dispatchEvent(new Event("input", { bubbles: true }));
      element.dispatchEvent(new Event("change", { bubbles: true }));
    }),
  submit: (element: Element) =>
    act(() => {
      element.dispatchEvent(new Event("submit", { bubbles: true, cancelable: true }));
    }),
};

const userEvent = { ...user, setup: () => user };

export const TESTING_BUILTINS: Record<string, unknown> = {
  vitest: { __esModule: true, ...vitest, default: vitest },
  "@testing-library/react": {
    __esModule: true,
    render,
    screen,
    within,
    waitFor,
    act,
    fireEvent,
    cleanup: cleanupRendered,
  },
  "@testing-library/user-event": { __esModule: true, default: userEvent, userEvent },
  "@testing-library/jest-dom": { __esModule: true },
  "@testing-library/jest-dom/vitest": { __esModule: true },
};

export function isTestFile(name: string): boolean {
  return /\.test\.(jsx?|mjs)$/.test(name);
}

/** Тест файлыг ачаалж, доторх тестүүдийг дарааллаар нь ажиллуулна. */
export async function runTestFile(
  modules: ModuleSystem,
  file: string,
  describeError: (error: unknown) => string,
  timeout: <T>(promise: Promise<T>) => Promise<T>,
): Promise<FileTestResult[]> {
  const target: Collector = { tests: [], prefix: [], before: [], after: [] };
  collector = target;
  try {
    modules.load(file);
  } catch (error) {
    return [{ name: file, passed: false, message: describeError(error), durationMs: 0 }];
  } finally {
    collector = null;
  }

  if (target.tests.length === 0) {
    return [
      {
        name: file,
        passed: false,
        message: 'Файлд нэг ч test(...) алга. test("нэр", () => { … }) гэж бичнэ үү.',
        durationMs: 0,
      },
    ];
  }

  const results: FileTestResult[] = [];
  for (const registered of target.tests) {
    const started = performance.now();
    let passed = false;
    let message: string | undefined;
    try {
      for (const hook of registered.before) await hook();
      await timeout(Promise.resolve(registered.run()));
      passed = true;
    } catch (error) {
      message = describeError(error);
    }
    try {
      for (const hook of registered.after) await hook();
    } catch (error) {
      passed = false;
      message ??= describeError(error);
    }
    cleanupRendered();
    document.body.querySelectorAll(":scope > div:not(#root)").forEach((node) => node.remove());
    results.push({
      name: registered.name,
      passed,
      message,
      durationMs: Math.round(performance.now() - started),
    });
  }
  return results;
}

/** «Хөтөч» дээр Vitest шиг тайлан. */
export function renderReport(file: string, results: FileTestResult[]): void {
  const passed = results.filter((result) => result.passed).length;
  const failed = results.length - passed;
  const report = document.createElement("div");
  report.style.cssText = "font:14px/1.6 ui-monospace,SFMono-Regular,Menlo,monospace;padding:4px";
  const heading = document.createElement("div");
  heading.style.cssText = "font-weight:700;margin-bottom:8px";
  heading.textContent = `${failed === 0 ? "✓" : "✗"} ${file}`;
  report.appendChild(heading);
  for (const result of results) {
    const row = document.createElement("div");
    row.style.cssText = `color:${result.passed ? "#1a7f37" : "#b42318"};margin-left:12px`;
    row.textContent = `${result.passed ? "✓" : "✗"} ${result.name} (${result.durationMs}ms)`;
    report.appendChild(row);
    if (!result.passed && result.message) {
      const detail = document.createElement("pre");
      detail.style.cssText = "white-space:pre-wrap;margin:2px 0 6px 32px;color:#b42318";
      detail.textContent = result.message;
      report.appendChild(detail);
    }
  }
  const summary = document.createElement("div");
  summary.style.cssText = "margin-top:12px;border-top:1px solid #d0d7de;padding-top:8px";
  summary.textContent = `Тест: ${passed} амжилттай${failed ? `, ${failed} амжилтгүй` : ""} (${results.length})`;
  report.appendChild(summary);
  document.body.replaceChildren(report);
  console.info(summary.textContent);
}
