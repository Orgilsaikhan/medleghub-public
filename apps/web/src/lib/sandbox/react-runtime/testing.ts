/**
 * React Testing Library + Jest-ийн жижиг хувилбар — дасгалын тестүүд болон
 * «Модул 13 — Тест» хичээлд ашиглагдана.
 *
 * API нь бодит сантай ИЖИЛ нэртэй (render, screen.getByRole, user.click,
 * expect(...).toHaveTextContent) тул сурагч эндээс сурсан зүйлээ бодит
 * төсөлд шууд хэрэглэнэ. Алдааны мессеж монгол хэлээр.
 */

import { act, createElement, type ReactNode } from "react";
import { createRoot, type Root } from "react-dom/client";

import { formatValue } from "@/lib/sandbox/react-runtime/format";

export class AssertionError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "AssertionError";
  }
}

const show = (value: unknown) => formatValue(value, 1);

// --- Текст -----------------------------------------------------------------

export type Matcher = string | RegExp | ((text: string, element: Element) => boolean);

interface MatchOptions {
  exact?: boolean;
}

export const normalizeText = (text: string) => text.replace(/\s+/g, " ").trim();

function matches(text: string, matcher: Matcher, element: Element, exact = true): boolean {
  const normalized = normalizeText(text);
  if (matcher instanceof RegExp) {
    matcher.lastIndex = 0;
    return matcher.test(normalized);
  }
  if (typeof matcher === "function") return matcher(normalized, element);
  const wanted = normalizeText(String(matcher));
  return exact ? normalized === wanted : normalized.toLowerCase().includes(wanted.toLowerCase());
}

function describeMatcher(matcher: Matcher): string {
  if (matcher instanceof RegExp) return matcher.toString();
  if (typeof matcher === "function") return "функц";
  return `«${matcher}»`;
}

/** Элементийн ӨӨРИЙН текст (хүүхэд элементийнхгүй) — RTL-ийн дүрэм. */
function ownText(element: Element): string {
  return Array.from(element.childNodes)
    .filter((node) => node.nodeType === Node.TEXT_NODE)
    .map((node) => node.textContent ?? "")
    .join("");
}

const IGNORED = new Set(["SCRIPT", "STYLE", "TEMPLATE", "NOSCRIPT"]);

function elementsIn(container: Element): Element[] {
  return Array.from(container.querySelectorAll("*")).filter((el) => !IGNORED.has(el.tagName));
}

// --- Хүртээмж (role, нэр) ------------------------------------------------------

export function isInaccessible(element: Element): boolean {
  for (let el: Element | null = element; el; el = el.parentElement) {
    if ((el as HTMLElement).hidden || el.getAttribute("aria-hidden") === "true") return true;
    const style = getComputedStyle(el);
    if (style.display === "none" || style.visibility === "hidden") return true;
  }
  return false;
}

const INPUT_ROLES: Record<string, string> = {
  button: "button",
  submit: "button",
  reset: "button",
  image: "button",
  checkbox: "checkbox",
  radio: "radio",
  range: "slider",
  number: "spinbutton",
  search: "searchbox",
  email: "textbox",
  tel: "textbox",
  text: "textbox",
  url: "textbox",
};

export function roleOf(element: Element): string | null {
  const explicit = element.getAttribute("role");
  if (explicit) return explicit.split(/\s+/)[0];
  const tag = element.tagName.toLowerCase();
  switch (tag) {
    case "button":
      return "button";
    case "a":
      return element.hasAttribute("href") ? "link" : null;
    case "input": {
      const type = (element.getAttribute("type") ?? "text").toLowerCase();
      return INPUT_ROLES[type] ?? null;
    }
    case "textarea":
      return "textbox";
    case "select":
      return (element as HTMLSelectElement).multiple ? "listbox" : "combobox";
    case "option":
      return "option";
    case "h1":
    case "h2":
    case "h3":
    case "h4":
    case "h5":
    case "h6":
      return "heading";
    case "ul":
    case "ol":
      return "list";
    case "li":
      return "listitem";
    case "img":
      return element.getAttribute("alt") === "" ? "presentation" : "img";
    case "nav":
      return "navigation";
    case "main":
      return "main";
    case "header":
      return "banner";
    case "footer":
      return "contentinfo";
    case "aside":
      return "complementary";
    case "form":
      return "form";
    case "article":
      return "article";
    case "section":
      return "region";
    case "table":
      return "table";
    case "tr":
      return "row";
    case "td":
      return "cell";
    case "th":
      return "columnheader";
    case "dialog":
      return "dialog";
    case "progress":
      return "progressbar";
    case "hr":
      return "separator";
    case "p":
      return "paragraph";
    case "label":
      return null;
    default:
      return null;
  }
}

/** Хүүхдүүдийн текст, дотор нь зургийн `alt` (товч доторх дүрс). */
function textWithAlt(node: Node): string {
  if (node.nodeType === Node.TEXT_NODE) return node.textContent ?? "";
  if (!(node instanceof Element) || IGNORED.has(node.tagName)) return "";
  if (node.getAttribute("aria-hidden") === "true") return "";
  if (node.tagName === "IMG") return node.getAttribute("alt") ?? "";
  const label = node.getAttribute("aria-label");
  if (label && node !== node.ownerDocument.body) return ` ${label} `;
  return Array.from(node.childNodes).map(textWithAlt).join("");
}

function labelsOf(element: Element): string[] {
  const labels = (element as HTMLInputElement).labels;
  if (!labels) return [];
  return Array.from(labels).map((label) =>
    Array.from(label.childNodes)
      .filter(
        (node) =>
          node !== element &&
          !(node instanceof HTMLInputElement) &&
          !(node instanceof HTMLSelectElement) &&
          !(node instanceof HTMLTextAreaElement),
      )
      .map(textWithAlt)
      .join(""),
  );
}

export function accessibleName(element: Element): string {
  const labelledBy = element.getAttribute("aria-labelledby");
  if (labelledBy) {
    const text = labelledBy
      .split(/\s+/)
      .map((id) => element.ownerDocument.getElementById(id))
      .filter(Boolean)
      .map((el) => textWithAlt(el!))
      .join(" ");
    if (normalizeText(text)) return normalizeText(text);
  }
  const ariaLabel = element.getAttribute("aria-label");
  if (ariaLabel && normalizeText(ariaLabel)) return normalizeText(ariaLabel);

  const tag = element.tagName;
  if (tag === "INPUT" || tag === "SELECT" || tag === "TEXTAREA") {
    const type = (element.getAttribute("type") ?? "").toLowerCase();
    if (tag === "INPUT" && ["button", "submit", "reset"].includes(type)) {
      return normalizeText(
        (element as HTMLInputElement).value || (type === "submit" ? "Submit" : ""),
      );
    }
    const fromLabel = normalizeText(labelsOf(element).join(" "));
    if (fromLabel) return fromLabel;
    return normalizeText(
      element.getAttribute("title") ?? element.getAttribute("placeholder") ?? "",
    );
  }
  if (tag === "IMG") return normalizeText(element.getAttribute("alt") ?? "");
  const role = roleOf(element);
  const fromContent = [
    "button",
    "link",
    "heading",
    "listitem",
    "option",
    "cell",
    "columnheader",
    "row",
    "tab",
    "menuitem",
    "checkbox",
    "radio",
    "paragraph",
  ];
  if (role && fromContent.includes(role)) {
    const text = normalizeText(Array.from(element.childNodes).map(textWithAlt).join(""));
    if (text) return text;
  }
  return normalizeText(element.getAttribute("title") ?? "");
}

// --- Хайлтын функцууд ------------------------------------------------------------

interface RoleOptions {
  name?: Matcher;
  level?: number;
  checked?: boolean;
  hidden?: boolean;
}

type AllQuery<A extends unknown[]> = (container: Element, ...args: A) => Element[];

function byText(
  container: Element,
  text: Matcher,
  options: MatchOptions & { selector?: string } = {},
) {
  const candidates = elementsIn(container).filter(
    (el) => !options.selector || el.matches(options.selector),
  );
  const own = candidates.filter((el) => {
    const text_ = ownText(el);
    return normalizeText(text_) !== "" && matches(text_, text, el, options.exact);
  });
  if (own.length > 0) return own;
  // Текст хэд хэдэн элементэд хуваагдсан бол (<p>Нийт: <b>3</b></p>) — хамгийн
  // гүн, бүтэн текст нь таарах элемент.
  const whole = candidates.filter((el) => matches(el.textContent ?? "", text, el, options.exact));
  return whole.filter((el) => !whole.some((other) => other !== el && el.contains(other)));
}

function byRole(container: Element, role: string, options: RoleOptions = {}) {
  return elementsIn(container).filter((el) => {
    if (roleOf(el) !== role) return false;
    if (!options.hidden && isInaccessible(el)) return false;
    if (options.level !== undefined && el.tagName !== `H${options.level}`) {
      const ariaLevel = el.getAttribute("aria-level");
      if (ariaLevel !== String(options.level)) return false;
    }
    if (options.checked !== undefined && (el as HTMLInputElement).checked !== options.checked) {
      return false;
    }
    if (options.name !== undefined && !matches(accessibleName(el), options.name, el)) return false;
    return true;
  });
}

function byLabelText(container: Element, text: Matcher, options: MatchOptions = {}) {
  const found = new Set<Element>();
  for (const label of Array.from(container.querySelectorAll("label"))) {
    const labelText = Array.from(label.childNodes)
      .filter(
        (node) =>
          !(node instanceof HTMLInputElement) &&
          !(node instanceof HTMLSelectElement) &&
          !(node instanceof HTMLTextAreaElement),
      )
      .map(textWithAlt)
      .join("");
    if (matches(labelText, text, label, options.exact) && label.control) found.add(label.control);
  }
  for (const el of elementsIn(container)) {
    const aria = el.getAttribute("aria-label");
    if (aria && matches(aria, text, el, options.exact)) found.add(el);
    if (
      el.getAttribute("aria-labelledby") &&
      matches(accessibleName(el), text, el, options.exact)
    ) {
      found.add(el);
    }
  }
  return [...found];
}

function byAttribute(attribute: string) {
  return (container: Element, text: Matcher, options: MatchOptions = {}) =>
    elementsIn(container).filter((el) => {
      const value = el.getAttribute(attribute);
      return value !== null && matches(value, text, el, options.exact);
    });
}

function byDisplayValue(container: Element, text: Matcher, options: MatchOptions = {}) {
  return elementsIn(container).filter((el) => {
    if (el instanceof HTMLSelectElement) {
      return Array.from(el.selectedOptions).some((option) =>
        matches(option.text, text, el, options.exact),
      );
    }
    if (el instanceof HTMLInputElement || el instanceof HTMLTextAreaElement) {
      return matches(el.value, text, el, options.exact);
    }
    return false;
  });
}

function byTestId(container: Element, id: Matcher, options: MatchOptions = {}) {
  return byAttribute("data-testid")(container, id, options);
}

/** Олдоогүй үед сурагчид «юу байгааг» харуулж тусална. */
function notFoundMessage(kind: string, args: unknown[], container: Element): string {
  const [first, options] = args as [Matcher, RoleOptions | undefined];
  if (kind === "Role") {
    const role = String(first);
    const same = elementsIn(container)
      .filter((el) => roleOf(el) === role && !isInaccessible(el))
      .map((el) => `«${accessibleName(el)}»`)
      .slice(0, 8);
    const named = options?.name !== undefined ? ` ${describeMatcher(options.name)} нэртэй` : "";
    const hint =
      same.length > 0
        ? ` Хуудсан дээрх ${role}: ${same.join(", ")}.`
        : ` Хуудсан дээр ${role} огт алга.`;
    return `${named} «${role}» элемент олдсонгүй.${hint}`.trim();
  }
  const label: Record<string, string> = {
    Text: "текст",
    LabelText: "label-тэй талбар",
    PlaceholderText: "placeholder-тэй талбар",
    DisplayValue: "утгатай талбар",
    AltText: "alt-тай зураг",
    Title: "title-тэй элемент",
    TestId: "data-testid",
  };
  const pageText = normalizeText(container.textContent ?? "");
  const preview = pageText
    ? ` Хуудсын текст: «${pageText.slice(0, 160)}${pageText.length > 160 ? "…" : ""}»`
    : " Хуудас хоосон байна.";
  return `${describeMatcher(first)} ${label[kind] ?? kind} олдсонгүй.${preview}`;
}

function buildQueries<A extends unknown[]>(
  kind: string,
  all: AllQuery<A>,
  container: () => Element,
) {
  const getAll = (...args: A) => {
    const found = all(container(), ...args);
    if (found.length === 0) throw new AssertionError(notFoundMessage(kind, args, container()));
    return found;
  };
  const get = (...args: A) => {
    const found = getAll(...args);
    if (found.length > 1) {
      throw new AssertionError(
        `${describeMatcher(args[0] as Matcher)} — ${found.length} элемент олдлоо, нэг л байх ёстой. getAllBy${kind} ашиглана уу.`,
      );
    }
    return found[0];
  };
  const queryAll = (...args: A) => all(container(), ...args);
  const query = (...args: A) => {
    const found = queryAll(...args);
    if (found.length > 1) {
      throw new AssertionError(
        `${describeMatcher(args[0] as Matcher)} — ${found.length} элемент олдлоо, нэг л байх ёстой.`,
      );
    }
    return found[0] ?? null;
  };
  return {
    [`getBy${kind}`]: get,
    [`getAllBy${kind}`]: getAll,
    [`queryBy${kind}`]: query,
    [`queryAllBy${kind}`]: queryAll,
    [`findBy${kind}`]: (...args: A) => waitFor(() => get(...args)),
    [`findAllBy${kind}`]: (...args: A) => waitFor(() => getAll(...args)),
  };
}

export type Queries = Record<string, (...args: never[]) => unknown> & {
  text: () => string;
};

export function queriesFor(container: () => Element): Queries {
  return {
    ...buildQueries("Text", byText, container),
    ...buildQueries("Role", byRole, container),
    ...buildQueries("LabelText", byLabelText, container),
    ...buildQueries("PlaceholderText", byAttribute("placeholder"), container),
    ...buildQueries("AltText", byAttribute("alt"), container),
    ...buildQueries("Title", byAttribute("title"), container),
    ...buildQueries("DisplayValue", byDisplayValue, container),
    ...buildQueries("TestId", byTestId, container),
    /** Хуудсын бүх харагдах текст — нэг мөр болгосон. */
    text: () => normalizeText(container().textContent ?? ""),
  } as Queries;
}

export const screen = queriesFor(() => document.body);
export const within = (element: Element) => queriesFor(() => element);

// --- Хүлээх ----------------------------------------------------------------------

export const sleep = (ms: number) => new Promise<void>((resolve) => setTimeout(resolve, ms));

export async function waitFor<T>(
  callback: () => T | Promise<T>,
  { timeout = 2000, interval = 25 }: { timeout?: number; interval?: number } = {},
): Promise<T> {
  const started = performance.now();
  let lastError: unknown;
  for (;;) {
    try {
      return await callback();
    } catch (error) {
      lastError = error;
    }
    if (performance.now() - started > timeout) throw lastError;
    await act(async () => {
      await sleep(interval);
    });
  }
}

// --- render ----------------------------------------------------------------------

const mounted: { root: Root; container: HTMLElement }[] = [];

/**
 * Testing Library-ийн `render` шиг sync. Mount үедээ `use(promise)`-ээр
 * зогсдог component нь sync `act` дотроос сэргэдэггүй (React 19) — тэр үед
 * `await act(async () => { render(ui); })` эсвэл `await runMain()`.
 */
export function render(ui: ReactNode) {
  const container = document.createElement("div");
  document.body.appendChild(container);
  const root = createRoot(container);
  act(() => root.render(ui));
  mounted.push({ root, container });
  return {
    container,
    rerender: (next: ReactNode) => act(() => root.render(next)),
    unmount: () => act(() => root.unmount()),
  };
}

export function registerRoot(root: Root, container: HTMLElement): void {
  mounted.push({ root, container });
}

export function cleanupRendered(): void {
  for (const { root } of mounted.splice(0)) {
    try {
      act(() => root.unmount());
    } catch {
      // Аль хэдийн unmount хийсэн.
    }
  }
}

// --- Хэрэглэгчийн үйлдэл ------------------------------------------------------------

function assertElement(value: unknown, action: string): asserts value is HTMLElement {
  if (!(value instanceof Element)) {
    throw new AssertionError(`${action}(…) элемент хүлээж байсан, ${show(value)} ирлээ.`);
  }
}

function isDisabled(element: Element): boolean {
  return (
    (element as HTMLButtonElement).disabled === true ||
    element.closest("fieldset:disabled") !== null
  );
}

function setNativeValue(element: HTMLElement, value: string): void {
  const prototype =
    element instanceof HTMLTextAreaElement
      ? HTMLTextAreaElement.prototype
      : element instanceof HTMLSelectElement
        ? HTMLSelectElement.prototype
        : HTMLInputElement.prototype;
  Object.getOwnPropertyDescriptor(prototype, "value")!.set!.call(element, value);
}

function mouse(type: string, element: Element, init: MouseEventInit = {}) {
  element.dispatchEvent(
    new MouseEvent(type, { bubbles: true, cancelable: true, composed: true, ...init }),
  );
}

function key(type: "keydown" | "keyup", element: Element, name: string) {
  return element.dispatchEvent(
    new KeyboardEvent(type, { key: name, code: name, bubbles: true, cancelable: true }),
  );
}

const SPECIAL_KEYS: Record<string, string> = {
  enter: "Enter",
  escape: "Escape",
  esc: "Escape",
  backspace: "Backspace",
  tab: "Tab",
  space: " ",
  arrowup: "ArrowUp",
  arrowdown: "ArrowDown",
  arrowleft: "ArrowLeft",
  arrowright: "ArrowRight",
};

function tokens(text: string): string[] {
  const result: string[] = [];
  for (const match of text.matchAll(/\{([^}]+)\}|([\s\S])/gu)) {
    result.push(match[1] ? `{${match[1].toLowerCase()}}` : match[2]);
  }
  return result;
}

export const user = {
  async click(element: unknown) {
    assertElement(element, "user.click");
    if (isDisabled(element)) return;
    await act(async () => {
      mouse("pointerdown", element);
      mouse("mousedown", element);
      if (element.tabIndex >= 0 || element.isContentEditable) element.focus();
      mouse("pointerup", element);
      mouse("mouseup", element);
      element.click();
    });
  },

  async dblClick(element: unknown) {
    await user.click(element);
    await user.click(element);
    assertElement(element, "user.dblClick");
    await act(async () => mouse("dblclick", element));
  },

  async type(element: unknown, text: string) {
    assertElement(element, "user.type");
    if (isDisabled(element)) return;
    await user.click(element);
    for (const token of tokens(text)) {
      await act(async () => {
        const target = (document.activeElement as HTMLElement | null) ?? element;
        const special = token.startsWith("{") ? SPECIAL_KEYS[token.slice(1, -1)] : undefined;
        const name = special ?? token;
        const proceed = key("keydown", target, name);
        if (proceed && "value" in target) {
          const field = target as HTMLInputElement;
          if (name === "Backspace") {
            setNativeValue(field, field.value.slice(0, -1));
            field.dispatchEvent(
              new InputEvent("input", { bubbles: true, inputType: "deleteContentBackward" }),
            );
          } else if (name === "Enter") {
            if (field instanceof HTMLTextAreaElement) {
              setNativeValue(field, `${field.value}\n`);
              field.dispatchEvent(
                new InputEvent("input", { bubbles: true, inputType: "insertLineBreak" }),
              );
            } else if (field.form) {
              field.form.requestSubmit();
            }
          } else if (!special || name === " ") {
            setNativeValue(field, field.value + name);
            field.dispatchEvent(
              new InputEvent("input", { bubbles: true, data: name, inputType: "insertText" }),
            );
          }
        }
        key("keyup", target, name);
      });
    }
  },

  async clear(element: unknown) {
    assertElement(element, "user.clear");
    await act(async () => {
      element.focus();
      setNativeValue(element, "");
      element.dispatchEvent(
        new InputEvent("input", { bubbles: true, inputType: "deleteContentBackward" }),
      );
    });
  },

  async selectOptions(element: unknown, values: string | string[]) {
    assertElement(element, "user.selectOptions");
    if (!(element instanceof HTMLSelectElement)) {
      throw new AssertionError("user.selectOptions нь <select> элемент хүлээнэ.");
    }
    const wanted = Array.isArray(values) ? values : [values];
    await act(async () => {
      for (const option of Array.from(element.options)) {
        option.selected = wanted.includes(option.value) || wanted.includes(option.text);
      }
      if (!element.multiple) {
        const chosen = Array.from(element.options).find((option) => option.selected);
        if (!chosen) throw new AssertionError(`«${wanted.join(", ")}» сонголт олдсонгүй.`);
        setNativeValue(element, chosen.value);
      }
      element.dispatchEvent(new Event("input", { bubbles: true }));
      element.dispatchEvent(new Event("change", { bubbles: true }));
    });
  },

  async keyboard(text: string) {
    for (const token of tokens(text)) {
      const special = token.startsWith("{") ? SPECIAL_KEYS[token.slice(1, -1)] : undefined;
      const target = (document.activeElement as HTMLElement | null) ?? document.body;
      await act(async () => {
        key("keydown", target, special ?? token);
        key("keyup", target, special ?? token);
      });
    }
  },

  async hover(element: unknown) {
    assertElement(element, "user.hover");
    await act(async () => {
      mouse("pointerover", element);
      mouse("mouseover", element, { relatedTarget: document.body });
    });
  },

  async unhover(element: unknown) {
    assertElement(element, "user.unhover");
    await act(async () => {
      mouse("pointerout", element);
      mouse("mouseout", element, { relatedTarget: document.body });
    });
  },
};

// --- Хуурамч функц (jest.fn) -------------------------------------------------------

export interface MockFunction {
  (...args: unknown[]): unknown;
  mock: { calls: unknown[][] };
  mockReturnValue: (value: unknown) => MockFunction;
  mockImplementation: (impl: (...args: unknown[]) => unknown) => MockFunction;
}

export function fn(implementation?: (...args: unknown[]) => unknown): MockFunction {
  let impl = implementation;
  const mockFn = ((...args: unknown[]) => {
    mockFn.mock.calls.push(args);
    return impl?.(...args);
  }) as MockFunction;
  mockFn.mock = { calls: [] };
  mockFn.mockReturnValue = (value) => {
    impl = () => value;
    return mockFn;
  };
  mockFn.mockImplementation = (next) => {
    impl = next;
    return mockFn;
  };
  return mockFn;
}

function isMock(value: unknown): value is MockFunction {
  return typeof value === "function" && "mock" in value;
}

// --- expect ------------------------------------------------------------------------

function deepEqual(a: unknown, b: unknown): boolean {
  if (Object.is(a, b)) return true;
  if (typeof a !== "object" || typeof b !== "object" || a === null || b === null) return false;
  if (Array.isArray(a) !== Array.isArray(b)) return false;
  if (a instanceof Date && b instanceof Date) return a.getTime() === b.getTime();
  const keysA = Object.keys(a).filter((key) => (a as Record<string, unknown>)[key] !== undefined);
  const keysB = Object.keys(b).filter((key) => (b as Record<string, unknown>)[key] !== undefined);
  if (keysA.length !== keysB.length) return false;
  return keysA.every((key) =>
    deepEqual((a as Record<string, unknown>)[key], (b as Record<string, unknown>)[key]),
  );
}

function elementLabel(element: Element): string {
  const name = accessibleName(element);
  return `<${element.tagName.toLowerCase()}>${name ? ` «${name}»` : ""}`;
}

class Expectation {
  constructor(
    private actual: unknown,
    private negated = false,
  ) {}

  get not(): Expectation {
    return new Expectation(this.actual, !this.negated);
  }

  private check(pass: boolean, message: string, negatedMessage: string): void {
    if (pass === this.negated) throw new AssertionError(this.negated ? negatedMessage : message);
  }

  private element(matcher: string): Element {
    if (!(this.actual instanceof Element)) {
      throw new AssertionError(
        `expect(…).${matcher}() элемент хүлээж байсан, ${show(this.actual)} ирлээ. Элемент олдоогүй байж магадгүй — queryBy… null буцаадаг.`,
      );
    }
    return this.actual;
  }

  toBe(expected: unknown) {
    this.check(
      Object.is(this.actual, expected),
      `${show(expected)} байх ёстой, ${show(this.actual)} гарлаа.`,
      `${show(expected)} байх ёсгүй.`,
    );
  }

  toEqual(expected: unknown) {
    this.check(
      deepEqual(this.actual, expected),
      `${show(expected)} байх ёстой, ${show(this.actual)} гарлаа.`,
      `${show(expected)}-тэй тэнцүү байх ёсгүй.`,
    );
  }

  toStrictEqual(expected: unknown) {
    this.toEqual(expected);
  }

  toBeTruthy() {
    this.check(
      Boolean(this.actual),
      `Үнэн (truthy) байх ёстой, ${show(this.actual)} гарлаа.`,
      `Худал (falsy) байх ёстой, ${show(this.actual)} гарлаа.`,
    );
  }

  toBeFalsy() {
    this.check(
      !this.actual,
      `Худал (falsy) байх ёстой, ${show(this.actual)} гарлаа.`,
      `Үнэн (truthy) байх ёстой, ${show(this.actual)} гарлаа.`,
    );
  }

  toBeNull() {
    this.check(
      this.actual === null,
      `null байх ёстой, ${show(this.actual)} гарлаа.`,
      "null байх ёсгүй.",
    );
  }

  toBeUndefined() {
    this.check(
      this.actual === undefined,
      `undefined байх ёстой, ${show(this.actual)} гарлаа.`,
      "undefined байх ёсгүй.",
    );
  }

  toBeDefined() {
    this.check(
      this.actual !== undefined,
      "Утгатай байх ёстой, undefined гарлаа.",
      `undefined байх ёстой, ${show(this.actual)} гарлаа.`,
    );
  }

  toBeGreaterThan(expected: number) {
    this.check(
      Number(this.actual) > expected,
      `${expected}-аас их байх ёстой, ${show(this.actual)} гарлаа.`,
      `${expected}-аас их байх ёсгүй, ${show(this.actual)} гарлаа.`,
    );
  }

  toBeGreaterThanOrEqual(expected: number) {
    this.check(
      Number(this.actual) >= expected,
      `${expected} буюу түүнээс их байх ёстой, ${show(this.actual)} гарлаа.`,
      `${expected}-аас бага байх ёстой, ${show(this.actual)} гарлаа.`,
    );
  }

  toBeLessThan(expected: number) {
    this.check(
      Number(this.actual) < expected,
      `${expected}-аас бага байх ёстой, ${show(this.actual)} гарлаа.`,
      `${expected}-аас бага байх ёсгүй, ${show(this.actual)} гарлаа.`,
    );
  }

  toBeLessThanOrEqual(expected: number) {
    this.check(
      Number(this.actual) <= expected,
      `${expected} буюу түүнээс бага байх ёстой, ${show(this.actual)} гарлаа.`,
      `${expected}-аас их байх ёстой, ${show(this.actual)} гарлаа.`,
    );
  }

  toContain(item: unknown) {
    const actual = this.actual;
    const pass =
      typeof actual === "string"
        ? actual.includes(String(item))
        : Array.isArray(actual) && actual.includes(item);
    this.check(
      pass,
      `${show(actual)} дотор ${show(item)} байх ёстой.`,
      `${show(actual)} дотор ${show(item)} байх ёсгүй.`,
    );
  }

  toHaveLength(length: number) {
    const actual = (this.actual as { length?: number } | null)?.length;
    this.check(
      actual === length,
      `Урт нь ${length} байх ёстой, ${show(actual)} гарлаа.`,
      `Урт нь ${length} байх ёсгүй.`,
    );
  }

  toMatch(pattern: RegExp | string) {
    const text = String(this.actual);
    const pass = typeof pattern === "string" ? text.includes(pattern) : pattern.test(text);
    this.check(
      pass,
      `${show(text)} нь ${String(pattern)}-тэй таарах ёстой.`,
      `${show(text)} нь ${String(pattern)}-тэй таарах ёсгүй.`,
    );
  }

  toHaveProperty(name: string, ...value: unknown[]) {
    const object = this.actual as Record<string, unknown> | null;
    const has = object !== null && object !== undefined && name in Object(object);
    const pass = has && (value.length === 0 || deepEqual(object![name], value[0]));
    this.check(
      pass,
      `«${name}» талбар${value.length ? ` = ${show(value[0])}` : ""} байх ёстой.`,
      `«${name}» талбар байх ёсгүй.`,
    );
  }

  toBeInstanceOf(type: new (...args: never[]) => unknown) {
    this.check(
      this.actual instanceof type,
      `${type.name}-ийн объект байх ёстой.`,
      `${type.name}-ийн объект байх ёсгүй.`,
    );
  }

  toThrow(expected?: string | RegExp) {
    if (typeof this.actual !== "function")
      throw new AssertionError("expect(fn).toThrow() функц хүлээнэ.");
    let thrown: unknown = undefined;
    let didThrow = false;
    try {
      (this.actual as () => unknown)();
    } catch (error) {
      didThrow = true;
      thrown = error;
    }
    const message = thrown instanceof Error ? thrown.message : String(thrown);
    const pass =
      didThrow &&
      (expected === undefined ||
        (typeof expected === "string" ? message.includes(expected) : expected.test(message)));
    this.check(
      pass,
      `Алдаа шидэх ёстой${expected ? ` (${String(expected)})` : ""}.`,
      `Алдаа шидэх ёсгүй, «${message}» шидлээ.`,
    );
  }

  // --- Хуурамч функц ---

  private mockCalls(matcher: string): unknown[][] {
    if (!isMock(this.actual)) {
      throw new AssertionError(`expect(…).${matcher}() нь fn()-ээр үүсгэсэн функц хүлээнэ.`);
    }
    return this.actual.mock.calls;
  }

  toHaveBeenCalled() {
    const calls = this.mockCalls("toHaveBeenCalled");
    this.check(
      calls.length > 0,
      "Функц дуудагдах ёстой байсан, нэг ч удаа дуудагдаагүй.",
      `Функц дуудагдах ёсгүй байсан, ${calls.length} удаа дуудагдлаа.`,
    );
  }

  toHaveBeenCalledTimes(times: number) {
    const calls = this.mockCalls("toHaveBeenCalledTimes");
    this.check(
      calls.length === times,
      `Функц ${times} удаа дуудагдах ёстой, ${calls.length} удаа дуудагдлаа.`,
      `Функц ${times} удаа дуудагдах ёсгүй.`,
    );
  }

  toHaveBeenCalledWith(...args: unknown[]) {
    const calls = this.mockCalls("toHaveBeenCalledWith");
    const pass = calls.some((call) => deepEqual(call, args));
    const seen = calls.length
      ? calls.map((call) => show(call)).join(", ")
      : "нэг ч удаа дуудагдаагүй";
    this.check(
      pass,
      `Функц ${show(args)} аргументтайгаар дуудагдах ёстой. Дуудалтууд: ${seen}.`,
      `Функц ${show(args)} аргументтайгаар дуудагдах ёсгүй.`,
    );
  }

  toHaveBeenLastCalledWith(...args: unknown[]) {
    const calls = this.mockCalls("toHaveBeenLastCalledWith");
    const last = calls[calls.length - 1];
    this.check(
      last !== undefined && deepEqual(last, args),
      `Сүүлийн дуудалт ${show(args)} байх ёстой, ${show(last)} байлаа.`,
      `Сүүлийн дуудалт ${show(args)} байх ёсгүй.`,
    );
  }

  // --- DOM ---

  toBeInTheDocument() {
    const pass = this.actual instanceof Element && this.actual.isConnected;
    this.check(
      pass,
      "Элемент хуудсан дээр байх ёстой, олдсонгүй.",
      `${this.actual instanceof Element ? elementLabel(this.actual) : "Элемент"} хуудсан дээр байх ёсгүй.`,
    );
  }

  toHaveTextContent(text: string | RegExp) {
    const element = this.element("toHaveTextContent");
    const content = normalizeText(element.textContent ?? "");
    const pass =
      typeof text === "string" ? content.includes(normalizeText(text)) : text.test(content);
    this.check(
      pass,
      `${elementLabel(element)} дотор ${typeof text === "string" ? `«${text}»` : text} текст байх ёстой. Одоо: «${content}».`,
      `${elementLabel(element)} дотор ${typeof text === "string" ? `«${text}»` : text} текст байх ёсгүй.`,
    );
  }

  toHaveValue(value: unknown) {
    const element = this.element("toHaveValue") as HTMLInputElement;
    const actual =
      element.type === "number"
        ? element.value === ""
          ? null
          : Number(element.value)
        : element.value;
    this.check(
      deepEqual(actual, value),
      `${elementLabel(element)}-ийн утга ${show(value)} байх ёстой, ${show(actual)} байна.`,
      `${elementLabel(element)}-ийн утга ${show(value)} байх ёсгүй.`,
    );
  }

  toBeChecked() {
    const element = this.element("toBeChecked") as HTMLInputElement;
    const checked = element.checked === true || element.getAttribute("aria-checked") === "true";
    this.check(
      checked,
      `${elementLabel(element)} чагтлагдсан байх ёстой.`,
      `${elementLabel(element)} чагтлагдаагүй байх ёстой.`,
    );
  }

  toBeDisabled() {
    const element = this.element("toBeDisabled");
    this.check(
      isDisabled(element),
      `${elementLabel(element)} идэвхгүй (disabled) байх ёстой.`,
      `${elementLabel(element)} идэвхтэй байх ёстой.`,
    );
  }

  toBeEnabled() {
    const element = this.element("toBeEnabled");
    this.check(
      !isDisabled(element),
      `${elementLabel(element)} идэвхтэй байх ёстой.`,
      `${elementLabel(element)} идэвхгүй байх ёстой.`,
    );
  }

  toHaveAttribute(name: string, ...value: unknown[]) {
    const element = this.element("toHaveAttribute");
    const actual = element.getAttribute(name);
    const pass = actual !== null && (value.length === 0 || actual === String(value[0]));
    this.check(
      pass,
      `${elementLabel(element)}-д ${name}${value.length ? `="${String(value[0])}"` : ""} attribute байх ёстой${actual !== null ? `, одоо "${actual}"` : ""}.`,
      `${elementLabel(element)}-д ${name} attribute байх ёсгүй.`,
    );
  }

  toHaveClass(...names: string[]) {
    const element = this.element("toHaveClass");
    const pass = names.every((name) => element.classList.contains(name));
    this.check(
      pass,
      `${elementLabel(element)}-д «${names.join(" ")}» класс байх ёстой. Одоо: «${element.className}».`,
      `${elementLabel(element)}-д «${names.join(" ")}» класс байх ёсгүй.`,
    );
  }

  toHaveStyle(expected: Record<string, string | number> | string) {
    const element = this.element("toHaveStyle");
    // Хүлээгдэж буй утгыг хөтчөөр тооцуулна: "red" → "rgb(255, 0, 0)".
    const probe = document.createElement("div");
    if (typeof expected === "string") probe.setAttribute("style", expected);
    else Object.assign(probe.style, expected);
    document.body.appendChild(probe);
    const wanted = getComputedStyle(probe);
    const computed = getComputedStyle(element);
    const mismatched = Array.from(probe.style).filter(
      (property) => computed.getPropertyValue(property) !== wanted.getPropertyValue(property),
    );
    probe.remove();
    this.check(
      mismatched.length === 0,
      `${elementLabel(element)}-ийн загвар таарахгүй: ${mismatched.map((property) => `${property}: ${computed.getPropertyValue(property)}`).join("; ")}.`,
      `${elementLabel(element)} ийм загвартай байх ёсгүй.`,
    );
  }

  toBeVisible() {
    const element = this.element("toBeVisible");
    const visible = element.isConnected && !isInaccessible(element);
    this.check(
      visible,
      `${elementLabel(element)} харагдах ёстой.`,
      `${elementLabel(element)} харагдах ёсгүй.`,
    );
  }

  toHaveFocus() {
    const element = this.element("toHaveFocus");
    this.check(
      document.activeElement === element,
      `${elementLabel(element)} дээр фокус байх ёстой.`,
      `${elementLabel(element)} дээр фокус байх ёсгүй.`,
    );
  }

  toBeEmptyDOMElement() {
    const element = this.element("toBeEmptyDOMElement");
    this.check(
      element.innerHTML.trim() === "",
      `${elementLabel(element)} хоосон байх ёстой.`,
      `${elementLabel(element)} хоосон байх ёсгүй.`,
    );
  }
}

export function expect(actual: unknown): Expectation {
  return new Expectation(actual);
}

/** Тестийн кодод бичих `React` (JSX-ийн classic runtime). */
export { act, createElement };
