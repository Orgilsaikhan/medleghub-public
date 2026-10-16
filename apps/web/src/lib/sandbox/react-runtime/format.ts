/**
 * `console.log`-ийн утгыг текст болгох — JavaScript sandbox-ийн
 * `worker-source.ts`-тэй ижил хэлбэр, дээр нь DOM элемент, React элемент.
 */

const MAX_DEPTH = 4;
const MAX_ITEMS = 100;
export const MAX_TEXT_LENGTH = 5000;

const REACT_ELEMENT = Symbol.for("react.transitional.element");
const REACT_LEGACY_ELEMENT = Symbol.for("react.element");

function isReactElement(value: object): value is { type: unknown; props: object } {
  const tag = (value as { $$typeof?: symbol }).$$typeof;
  return tag === REACT_ELEMENT || tag === REACT_LEGACY_ELEMENT;
}

function typeName(type: unknown): string {
  if (typeof type === "string") return type;
  if (typeof type === "function") return type.name || "Component";
  if (typeof type === "symbol") return type.description?.replace(/^react\./, "") ?? "Fragment";
  return "Component";
}

function describeElement(node: Element): string {
  const id = node.id ? `#${node.id}` : "";
  const classes =
    typeof node.className === "string" && node.className.trim()
      ? "." + node.className.trim().split(/\s+/).join(".")
      : "";
  return `<${node.tagName.toLowerCase()}${id}${classes}>`;
}

export function formatValue(value: unknown, depth = 0, seen = new Set<object>()): string {
  if (value === null) return "null";
  if (value === undefined) return "undefined";

  switch (typeof value) {
    case "string":
      return depth === 0 ? value : JSON.stringify(value);
    case "number":
    case "boolean":
    case "bigint":
      return String(value);
    case "symbol":
      return value.toString();
    case "function":
      return `[Function: ${value.name || "anonymous"}]`;
  }

  const object = value as object;
  if (object instanceof Error) return `${object.name}: ${object.message}`;
  if (typeof Element !== "undefined" && object instanceof Element) return describeElement(object);
  if (typeof Node !== "undefined" && object instanceof Node) return `[${object.nodeName}]`;
  if (isReactElement(object)) return `<${typeName(object.type)} />`;

  if (seen.has(object)) return "[Circular]";
  if (depth >= MAX_DEPTH) return Array.isArray(object) ? "[Array]" : "[Object]";
  seen.add(object);

  try {
    if (Array.isArray(object)) {
      const shown = object.slice(0, MAX_ITEMS).map((item) => formatValue(item, depth + 1, seen));
      if (object.length > MAX_ITEMS) shown.push(`… ${object.length - MAX_ITEMS} more`);
      return `[${shown.join(", ")}]`;
    }
    if (object instanceof Map) {
      const pairs: string[] = [];
      for (const [key, item] of object) {
        pairs.push(`${formatValue(key, depth + 1, seen)} => ${formatValue(item, depth + 1, seen)}`);
        if (pairs.length >= MAX_ITEMS) break;
      }
      return `Map(${object.size}) {${pairs.join(", ")}}`;
    }
    if (object instanceof Set) {
      const items: string[] = [];
      for (const item of object) {
        items.push(formatValue(item, depth + 1, seen));
        if (items.length >= MAX_ITEMS) break;
      }
      return `Set(${object.size}) {${items.join(", ")}}`;
    }
    if (object instanceof Date) return object.toISOString();
    if (object instanceof RegExp) return object.toString();
    if (object instanceof Promise) return "Promise { <pending> }";

    const record = object as Record<string, unknown>;
    const body = Object.keys(record)
      .slice(0, MAX_ITEMS)
      .map((key) => `${key}: ${formatValue(record[key], depth + 1, seen)}`)
      .join(", ");
    const name = object.constructor?.name;
    const prefix = name && name !== "Object" ? `${name} ` : "";
    return `${prefix}{${body ? ` ${body} ` : ""}}`;
  } catch {
    return "[Unserializable]";
  } finally {
    seen.delete(object);
  }
}

/**
 * `console.error("… %s …", a)` — React-ийн анхааруулга ийм хэлбэртэй ирдэг.
 * `%c`-ийн загварыг хаяна.
 */
export function formatArgs(args: unknown[]): string {
  let rest = args;
  let head = "";
  if (typeof args[0] === "string" && /%[sdifoOc]/.test(args[0])) {
    let index = 1;
    head = args[0].replace(/%([sdifoOc%])/g, (whole, kind: string) => {
      if (kind === "%") return "%";
      if (index >= args.length) return whole;
      const arg = args[index++];
      if (kind === "c") return "";
      if (kind === "d" || kind === "i") return String(Number.parseInt(String(arg), 10));
      if (kind === "f") return String(Number(arg));
      return formatValue(arg, kind === "s" ? 0 : 1);
    });
    rest = args.slice(index);
  } else if (args.length > 0) {
    head = formatValue(args[0]);
    rest = args.slice(1);
  }

  let text = [head, ...rest.map((arg) => formatValue(arg))].join(" ");
  if (text.length > MAX_TEXT_LENGTH) text = `${text.slice(0, MAX_TEXT_LENGTH)}…`;
  return text;
}
