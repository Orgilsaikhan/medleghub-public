/**
 * react-router-ийг sandbox-д тааруулах.
 *
 * Iframe-ийн хаяг `about:srcdoc` тул `history.pushState("/courses")`
 * SecurityError шиднэ — `BrowserRouter` шууд ажиллахгүй. Оронд нь санах ойн
 * router ажиллуулж, одоогийн замыг «Хөтөч» tab-ийн хаягийн мөрөнд илгээнэ.
 * Сурагч бодит төсөлтэй ЯГ ИЖИЛ кодоор (`<BrowserRouter>`) бичнэ.
 */

import * as ReactRouter from "react-router";
import { createElement, useEffect, type ReactNode } from "react";

type Navigate = (to: number | string) => void;

export interface LocationBridge {
  /** Эхлэх зам — «дахин ачаалах» үед одоогийн замдаа үлдэнэ. */
  initialPath: string;
  report: (path: string, canGoBack: boolean, canGoForward: boolean) => void;
}

let bridge: LocationBridge = { initialPath: "/", report: () => {} };
let navigate: Navigate | null = null;

// Санах ойн түүх — хаягийн мөрний сумыг идэвхжүүлэхэд.
let entries: string[] = [];
let index = -1;
let pendingDelta = 0;

export function configureRouterBridge(next: LocationBridge): void {
  bridge = next;
  entries = [];
  index = -1;
  navigate = null;
}

export function setInitialPath(path: string): void {
  bridge = { ...bridge, initialPath: path };
}

/** Хуудаснаас ирсэн сум, хаяг. Router байхгүй бол юу ч хийхгүй. */
export function navigateFromParent(to: "back" | "forward" | "path", path?: string): void {
  if (!navigate) return;
  if (to === "back" && index > 0) {
    pendingDelta = -1;
    navigate(-1);
  } else if (to === "forward" && index < entries.length - 1) {
    pendingDelta = 1;
    navigate(1);
  } else if (to === "path" && path) {
    navigate(path.startsWith("/") ? path : `/${path}`);
  }
}

function record(path: string, action: string): void {
  if (action === "PUSH" || index === -1) {
    entries = [...entries.slice(0, index + 1), path];
    index = entries.length - 1;
  } else if (action === "REPLACE") {
    entries[index] = path;
  } else {
    // POP — бидний сум (`pendingDelta`) эсвэл сурагчийн `navigate(-1)`.
    index = Math.min(entries.length - 1, Math.max(0, index + (pendingDelta || -1)));
    pendingDelta = 0;
  }
  bridge.report(path, index > 0, index < entries.length - 1);
}

function LocationReporter(): null {
  const location = ReactRouter.useLocation();
  const action = ReactRouter.useNavigationType();
  const go = ReactRouter.useNavigate();
  const path = location.pathname + location.search + location.hash;

  useEffect(() => {
    navigate = (to) => (typeof to === "number" ? go(to) : go(to));
    return () => {
      navigate = null;
    };
  }, [go]);

  useEffect(() => {
    record(path, action);
  }, [path, action]);

  return null;
}

interface RouterProps {
  children?: ReactNode;
  basename?: string;
}

function BrowserRouter({ children, basename }: RouterProps) {
  return createElement(
    ReactRouter.MemoryRouter,
    { basename, initialEntries: [bridge.initialPath] },
    createElement(LocationReporter),
    children,
  );
}

function createBrowserRouter(
  routes: Parameters<typeof ReactRouter.createMemoryRouter>[0],
  options: Parameters<typeof ReactRouter.createMemoryRouter>[1] = {},
) {
  const router = ReactRouter.createMemoryRouter(routes, {
    ...options,
    initialEntries: [bridge.initialPath],
  });
  const current = router.state.location;
  record(current.pathname + current.search + current.hash, "PUSH");
  navigate = (to) => void (typeof to === "number" ? router.navigate(to) : router.navigate(to));
  router.subscribe((state) => {
    const location = state.location;
    record(location.pathname + location.search + location.hash, state.historyAction);
  });
  return router;
}

/** `react-router`, `react-router-dom` хоёулаа энэ объект руу холбогдоно. */
export const routerModule: Record<string, unknown> = {
  ...ReactRouter,
  BrowserRouter,
  HashRouter: BrowserRouter,
  createBrowserRouter,
  createHashRouter: createBrowserRouter,
};
