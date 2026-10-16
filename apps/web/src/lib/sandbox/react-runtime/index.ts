/**
 * React sandbox-ийн runtime — `sandbox="allow-scripts allow-forms"` iframe
 * дотор ажиллана.
 *
 *     npm run sandbox:react   →   public/sandbox/react-runtime.js
 *
 * React-ийн DEVELOPMENT хувилбар: `key`-гүй жагсаалт, буруу hook гэх мэт
 * анхааруулга console дээр гарна — сурагчид хамгийн хэрэгтэй мэдээлэл.
 *
 * Хоёр горим:
 *   - `preview` — «Хөтөч» tab. `main.jsx`-ийг ажиллуулж, console, алдаа,
 *     гарчиг, замыг хуудас руу дамжуулна.
 *   - `test` — нуугдмал iframe. Тест бүрт модулиудыг шинээр ажиллуулж,
 *     үр дүнг нэг нэгээр нь илгээнэ.
 */

import * as ReactQuery from "@tanstack/react-query";
import * as React from "react";
import * as ReactDOM from "react-dom";
import * as ReactDOMClient from "react-dom/client";
import * as JsxDevRuntime from "react/jsx-dev-runtime";
import * as JsxRuntime from "react/jsx-runtime";

import { MockApi } from "@/lib/sandbox/react-runtime/api";
import {
  captureConsole,
  installBrowserShims,
  installLoopGuard,
  installStorage,
  locate,
  MemoryStorage,
  trackTimers,
  type LogEntry,
} from "@/lib/sandbox/react-runtime/environment";
import { ModuleNotFoundError, ModuleSystem } from "@/lib/sandbox/react-runtime/modules";
import {
  configureRouterBridge,
  navigateFromParent,
  routerModule,
  setInitialPath,
} from "@/lib/sandbox/react-runtime/router";
import {
  isTestFile,
  renderReport,
  runTestFile,
  TESTING_BUILTINS,
} from "@/lib/sandbox/react-runtime/test-file";
import {
  AssertionError,
  cleanupRendered,
  expect,
  fn,
  registerRoot,
  render,
  screen,
  sleep,
  user,
  waitFor,
  within,
} from "@/lib/sandbox/react-runtime/testing";
import { CompileError, compileModule, compileTest } from "@/lib/sandbox/react-runtime/transform";
import {
  JOB_ELEMENT_ID,
  MESSAGE_SOURCE,
  RUNTIME_GLOBAL,
  TEST_TIMEOUT_MS,
  type SandboxError,
  type SandboxJob,
  type SandboxMessage,
} from "@/lib/sandbox/react/protocol";

type Outgoing = SandboxMessage extends infer M
  ? M extends { source: string; runId: number }
    ? Omit<M, "source" | "runId">
    : never
  : never;

/** `import React from "react"`, `import { useState } from "react"` хоёулаа ажиллана. */
function esm(namespace: object): Record<string, unknown> {
  const withDefault = namespace as { default?: unknown };
  return { __esModule: true, ...namespace, default: withDefault.default ?? namespace };
}

const nativeSetTimeout = window.setTimeout.bind(window);

let job: SandboxJob;
let post: (message: Outgoing) => void = () => {};
let onRootError: (error: unknown, componentStack?: string) => void = () => {};
let onRootCreated: (root: ReactDOMClient.Root, container: HTMLElement) => void = () => {};

function createRoot(
  container: Element | DocumentFragment | null,
  options?: ReactDOMClient.RootOptions,
) {
  if (!container) {
    throw new Error(
      'createRoot(...)-д элемент олдсонгүй. index.html дотор <div id="root"></div> байгаа, document.getElementById("root") зөв бичигдсэн эсэхийг шалга.',
    );
  }
  const root = ReactDOMClient.createRoot(container, {
    onUncaughtError: (error, info) => onRootError(error, info.componentStack),
    onCaughtError: (error) =>
      console.error(
        `Error boundary алдааг барьлаа: ${error instanceof Error ? `${error.name}: ${error.message}` : String(error)}`,
      ),
    onRecoverableError: (error) =>
      console.warn(`React: ${error instanceof Error ? error.message : String(error)}`),
    ...options,
  });
  onRootCreated(root, container as HTMLElement);
  return root;
}

const reactDomClient = esm({ ...ReactDOMClient, createRoot });

const BUILTINS: Record<string, unknown> = {
  react: esm(React),
  "react/jsx-runtime": esm(JsxRuntime),
  "react/jsx-dev-runtime": esm(JsxDevRuntime),
  "react-dom": esm(ReactDOM),
  "react-dom/client": reactDomClient,
  "react-router": esm(routerModule),
  "react-router-dom": esm(routerModule),
  "react-router/dom": esm(routerModule),
  "@tanstack/react-query": esm(ReactQuery),
  ...TESTING_BUILTINS,
};

/** Сурагчийн нэг тест (`App.test.jsx` доторх) — дасгалын тестээс богино. */
const STUDENT_TEST_TIMEOUT_MS = 3000;

// --- Туслах ------------------------------------------------------------------

function filesMap(): Map<string, string> {
  return new Map(job.files.map((file) => [file.name, file.code]));
}

function injectStyle(name: string, css: string): void {
  if (document.querySelector(`style[data-file="${CSS.escape(name)}"]`)) return;
  const style = document.createElement("style");
  style.dataset.file = name;
  style.textContent = css;
  document.head.appendChild(style);
}

function describeError(error: unknown): SandboxError {
  if (error instanceof CompileError) return error.detail;
  const where = locate(
    error,
    job.files.map((file) => file.name),
  );
  const message =
    error instanceof ModuleNotFoundError || error instanceof AssertionError
      ? error.message
      : error instanceof Error
        ? `${error.name}: ${error.message}`
        : `Uncaught ${String(error)}`;
  return { kind: "runtime", message, ...where };
}

function formatError(error: SandboxError): string {
  const where = error.file ? `${error.file}${error.line ? `:${error.line}` : ""} — ` : "";
  const prefix = error.kind === "compile" ? "Синтакс алдаа: " : "";
  return `${where}${prefix}${error.message}`;
}

/** Хөрвүүлэлтийн алдааг кодыг ажиллуулахаас ӨМНӨ бүх файлаас хайна. */
function firstCompileError(): SandboxError | null {
  for (const file of job.files) {
    if (!/\.(jsx?|mjs)$/.test(file.name)) continue;
    try {
      compileModule(file.code, file.name);
    } catch (error) {
      if (error instanceof CompileError) return error.detail;
      throw error;
    }
  }
  return null;
}

function showOverlay(error: SandboxError, componentStack?: string): void {
  document.getElementById("mh-error-overlay")?.remove();
  const overlay = document.createElement("div");
  overlay.id = "mh-error-overlay";
  overlay.setAttribute("role", "alert");
  overlay.style.cssText =
    "position:fixed;inset:0;z-index:2147483647;overflow:auto;padding:20px;background:rgba(255,255,255,.97);font:14px/1.5 ui-monospace,SFMono-Regular,Menlo,monospace;color:#1f2328";
  const title = document.createElement("div");
  title.style.cssText = "color:#b42318;font-weight:700;font-size:15px;margin-bottom:8px";
  title.textContent = error.kind === "compile" ? "Синтакс алдаа" : "Алдаа гарлаа";
  const where = document.createElement("div");
  where.style.cssText = "color:#57606a;margin-bottom:8px";
  where.textContent = error.file ? `${error.file}${error.line ? `:${error.line}` : ""}` : "";
  const body = document.createElement("pre");
  body.style.cssText =
    "white-space:pre-wrap;margin:0;padding:12px;border:1px solid #f1aeb5;border-radius:8px;background:#fff5f5;color:#b42318";
  body.textContent = error.message;
  overlay.append(title, where, body);
  if (componentStack) {
    const stack = document.createElement("pre");
    stack.style.cssText = "white-space:pre-wrap;margin:12px 0 0;color:#57606a;font-size:12px";
    stack.textContent = componentStack.trim().split("\n").slice(0, 6).join("\n");
    overlay.append(stack);
  }
  const hint = document.createElement("p");
  hint.style.cssText = "color:#57606a;margin:12px 0 0;font-family:system-ui,sans-serif";
  hint.textContent = "Кодоо засаад «Ажиллуулах» дарна уу.";
  overlay.append(hint);
  document.body.appendChild(overlay);
}

/** Модулийг ажиллуулсны дараа root үүсээгүй бол default export-ийг харуулна. */
function autoRender(exports: Record<string, unknown>, rootsBefore: number, rootsNow: () => number) {
  if (rootsNow() > rootsBefore) return;
  const component = exports.default ?? exports.App;
  if (typeof component !== "function") return;
  let container = document.getElementById("root");
  if (!container) {
    container = document.createElement("div");
    container.id = "root";
    document.body.prepend(container);
  }
  createRoot(container).render(React.createElement(component as React.ComponentType));
}

// --- Урьдчилан харах ----------------------------------------------------------------

function bootPreview(): void {
  const errorOnce = new Set<string>();
  const report = (error: unknown, options: { overlay?: boolean; componentStack?: string } = {}) => {
    const detail = describeError(error);
    const text = formatError(detail);
    if (errorOnce.has(text)) return;
    errorOnce.add(text);
    post({ type: "error", error: detail });
    if (options.overlay) showOverlay(detail, options.componentStack);
  };

  installLoopGuard();
  captureConsole((entry) => post({ type: "console", ...entry }));
  window.addEventListener("error", (event) => {
    event.preventDefault();
    report(event.error ?? new Error(event.message));
  });
  window.addEventListener("unhandledrejection", (event) => {
    event.preventDefault();
    const reason = event.reason;
    if (reason instanceof Error) reason.message = `(Promise) ${reason.message}`;
    report(reason);
  });
  installBrowserShims();
  installStorage(
    new MemoryStorage(job.storage, (data) => post({ type: "storage", data })),
    new MemoryStorage(),
  );
  const api = new MockApi(400);
  window.fetch = api.fetch;

  let lastTitle = "";
  const reportTitle = () => {
    if (document.title !== lastTitle) {
      lastTitle = document.title;
      post({ type: "title", title: lastTitle });
    }
  };
  reportTitle();
  setInterval(reportTitle, 250);

  configureRouterBridge({
    initialPath: job.path ?? "/",
    report: (path, canGoBack, canGoForward) =>
      post({ type: "location", path, canGoBack, canGoForward }),
  });
  window.addEventListener("message", (event) => {
    if (event.source !== window.parent) return;
    const data = event.data as { source?: string; type?: string; to?: string; path?: string };
    if (data?.source !== MESSAGE_SOURCE || data.type !== "navigate") return;
    if (data.to === "back" || data.to === "forward" || data.to === "path") {
      navigateFromParent(data.to, data.path);
    }
  });

  let roots = 0;
  onRootCreated = () => {
    roots += 1;
  };
  onRootError = (error, componentStack) => report(error, { overlay: true, componentStack });

  const modules = new ModuleSystem(filesMap(), BUILTINS, injectStyle);
  for (const file of job.files) {
    if (file.name.endsWith(".css")) injectStyle(file.name, file.code);
  }

  const compileError = firstCompileError();
  const testFiles = job.files.filter((file) => isTestFile(file.name));
  if (compileError) {
    report(new CompileError(compileError), { overlay: true });
  } else if (testFiles.length > 0) {
    // «Модул 13 — Тест»: апп биш, сурагчийн тестийн үр дүн (Vitest шиг).
    void runPreviewTests(
      testFiles.map((file) => file.name),
      modules,
    ).then(() => post({ type: "ready" }));
    return;
  } else {
    try {
      const exports = modules.load(job.entry);
      autoRender(exports, 0, () => roots);
    } catch (error) {
      report(error, { overlay: true });
    }
  }
  post({ type: "ready" });
}

async function runPreviewTests(names: string[], modules: ModuleSystem): Promise<void> {
  (globalThis as Record<string, unknown>).IS_REACT_ACT_ENVIRONMENT = true;
  const html = job.html;
  for (const name of names) {
    document.body.innerHTML = html;
    const results = await runTestFile(modules, name, failureMessage, (promise) =>
      withTimeout(promise, STUDENT_TEST_TIMEOUT_MS),
    );
    renderReport(name, results);
  }
}

// --- Тест ---------------------------------------------------------------------------

const TEST_NAMES = [
  "React",
  "act",
  "render",
  "screen",
  "within",
  "user",
  "waitFor",
  "expect",
  "fn",
  "sleep",
  "mod",
  "App",
  "runMain",
  "logs",
  "api",
  "setPath",
  "runTestFile",
];

function withTimeout<T>(promise: Promise<T>, ms: number): Promise<T> {
  return new Promise<T>((resolve, reject) => {
    const timer = nativeSetTimeout(
      () =>
        reject(
          new AssertionError(
            `Тест ${ms / 1000} секундэд дууссангүй — хүлээсэн зүйл гарч ирээгүй эсвэл давталт тасрахгүй байна.`,
          ),
        ),
      ms,
    );
    promise.then(
      (value) => {
        clearTimeout(timer);
        resolve(value);
      },
      (error) => {
        clearTimeout(timer);
        reject(error);
      },
    );
  });
}

function failureMessage(error: unknown): string {
  const first = error instanceof AggregateError && error.errors.length ? error.errors[0] : error;
  return formatError(describeError(first));
}

async function bootTests(): Promise<void> {
  (globalThis as Record<string, unknown>).IS_REACT_ACT_ENVIRONMENT = true;
  installLoopGuard();
  const timers = trackTimers();
  const logs: LogEntry[] = [];
  captureConsole((entry) => logs.push(entry));

  let errors: unknown[] = [];
  window.addEventListener("error", (event) => {
    event.preventDefault();
    errors.push(event.error ?? new Error(event.message));
  });
  window.addEventListener("unhandledrejection", (event) => {
    event.preventDefault();
    errors.push(event.reason);
  });
  installBrowserShims();
  const api = new MockApi(20);
  window.fetch = api.fetch;
  configureRouterBridge({ initialPath: "/", report: () => {} });
  onRootCreated = (root, container) => registerRoot(root, container);
  onRootError = (error) => errors.push(error);

  const tests = job.tests ?? [];
  const html = job.html;
  const modules = new ModuleSystem(filesMap(), BUILTINS, injectStyle);
  for (const file of job.files) {
    if (file.name.endsWith(".css")) injectStyle(file.name, file.code);
  }

  const compileError = firstCompileError();
  if (compileError) {
    const message = formatError(compileError);
    tests.forEach((_, index) => post({ type: "test-result", index, passed: false, message }));
    post({ type: "tests-done" });
    return;
  }

  const appFile = ["App.jsx", "App.js"].find((name) => modules.has(name));

  for (const [index, test] of tests.entries()) {
    document.body.innerHTML = html;
    document.title = "React App";
    modules.reset();
    api.reset();
    installStorage(new MemoryStorage(), new MemoryStorage());
    setInitialPath("/");
    logs.length = 0;
    errors = [];

    let passed = false;
    let message: string | undefined;
    try {
      const run = (0, eval)(compileTest(test.code, TEST_NAMES)) as (scope: object) => Promise<void>;
      const scope = {
        React,
        act: React.act,
        render,
        screen,
        within,
        user,
        waitFor,
        expect,
        fn,
        sleep,
        mod: (path: string) => modules.require(path.startsWith(".") ? path : `./${path}`, ""),
        App: undefined as unknown,
        runMain: async () => {
          let roots = 0;
          const previous = onRootCreated;
          onRootCreated = (root, container) => {
            roots += 1;
            registerRoot(root, container);
          };
          try {
            await React.act(async () => {
              const exports = modules.load(job.entry);
              autoRender(exports, 0, () => roots);
            });
          } finally {
            onRootCreated = previous;
          }
          return document.getElementById("root");
        },
        logs,
        api,
        setPath: setInitialPath,
        /**
         * Сурагчийн тест файлыг ажиллуулна. `overrides` — файлыг орлох код
         * (зориуд эвдэрсэн component): сурагчийн тест алдааг барих ёстой.
         */
        runTestFile: async (file?: string, overrides: Record<string, string> = {}) => {
          const map = filesMap();
          for (const [name, code] of Object.entries(overrides)) map.set(name, code);
          const target = file ?? [...map.keys()].find(isTestFile);
          if (!target) throw new AssertionError("*.test.jsx файл алга.");
          const isolated = new ModuleSystem(map, BUILTINS, injectStyle);
          const results = await runTestFile(isolated, target, failureMessage, (promise) =>
            withTimeout(promise, STUDENT_TEST_TIMEOUT_MS),
          );
          document.body.innerHTML = html;
          return results;
        },
      };
      if (appFile) {
        const exports = modules.load(appFile);
        scope.App = exports.default ?? exports.App;
      }
      await withTimeout(run(scope), TEST_TIMEOUT_MS);
      if (errors.length > 0) throw errors[0];
      passed = true;
    } catch (error) {
      message = failureMessage(error);
    }

    try {
      cleanupRendered();
    } catch {
      // Цэвэрлэгээний алдаа дараагийн тестэд нөлөөлөхгүй.
    }
    timers.clearAll();
    post({ type: "test-result", index, passed, message });
    // Урт тест хуудсыг гацаахгүй — тест бүрийн хооронд event loop-д зай өгнө.
    await new Promise((resolve) => nativeSetTimeout(resolve, 0));
  }
  post({ type: "tests-done" });
}

// --- Эхлүүлэх -------------------------------------------------------------------------

function boot(): void {
  const element = document.getElementById(JOB_ELEMENT_ID);
  job = JSON.parse(element?.textContent ?? "{}") as SandboxJob;
  element?.remove();
  post = (message) =>
    window.parent.postMessage({ source: MESSAGE_SOURCE, runId: job.runId, ...message }, "*");

  if (job.mode === "test") {
    document.body.innerHTML = job.html;
    void bootTests();
  } else {
    document.body.insertAdjacentHTML("afterbegin", job.html);
    bootPreview();
  }
}

(window as unknown as Record<string, unknown>)[RUNTIME_GLOBAL] = { boot };
