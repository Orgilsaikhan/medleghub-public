/**
 * Web Worker-ийн эх код (мөр хэлбэрээр).
 *
 * Энэ кодыг `blob:` URL болгож Worker-т ачаална. Мөр хэлбэрээр байрлуулсны
 * шалтгаан: bundler-ээс хамааралгүй, ямар ч орчинд ижилхэн ажиллана.
 *
 * АЮУЛГҮЙ БАЙДАЛ
 * ──────────────
 * Хэрэглэгчийн код зөвхөн энд ажиллана. Worker дотор:
 *   • DOM, `window`, `document`, cookie, localStorage байхгүй (Worker-ийн шинж).
 *   • Сүлжээний бүх API-г устгасан — өгөгдөл гадагш гарахгүй.
 *   • `blob:` origin тул үндсэн сайтын cookie/storage-д хандах боломжгүй.
 *   • Гол thread нь тодорхой хугацааны дараа `terminate()` дуудаж,
 *     төгсгөлгүй давталтыг таслана.
 * Backend нь хэрэглэгчийн кодыг хүлээж авахгүй, хадгалахгүй, ажиллуулахгүй.
 *
 * ОРОЛТ
 * ─────
 * `prompt()` нь хөтчийн жинхэнэ функц — энд «Оролт»-ын (тестийн) дараагийн
 * мөрийг буцаана, мөр дуусвал `null` (хөтчийн «Cancel» шиг). Асуултын текст
 * console дээр `info` болж харагдах ч гаралтад (stdout) тооцогдохгүй —
 * Python-ий тестийн `input()` шиг.
 */

export const WORKER_SOURCE = String.raw`
// --- Сүлжээ болон гадаад нөөцийн хандалтыг хаана --------------------------
const BLOCKED = [
  "fetch",
  "XMLHttpRequest",
  "WebSocket",
  "EventSource",
  "importScripts",
  "indexedDB",
  "caches",
  "SharedWorker",
  "Worker",
  "BroadcastChannel",
  "Notification",
];

for (const name of BLOCKED) {
  try {
    Object.defineProperty(self, name, {
      value: undefined,
      configurable: false,
      writable: false,
    });
  } catch (_) {
    // Зарим орчинд устгах боломжгүй байж болно — доорх navigator хязгаарлалт үлдэнэ.
  }
}

try {
  Object.defineProperty(self, "navigator", { value: undefined, configurable: false });
} catch (_) {}

// Top-level await-ийг дэмжихэд ашиглагдана.
const AsyncFunction = Object.getPrototypeOf(async function () {}).constructor;

// --- Console-ийг барьж авах ------------------------------------------------
const MAX_ENTRIES = 500;
const MAX_TEXT_LENGTH = 5000;
const MAX_DEPTH = 4;

let entries = [];
let truncated = false;

function formatValue(value, depth, seen) {
  if (value === null) return "null";
  if (value === undefined) return "undefined";

  const type = typeof value;
  if (type === "string") return depth === 0 ? value : JSON.stringify(value);
  if (type === "number" || type === "boolean" || type === "bigint") return String(value);
  if (type === "symbol") return value.toString();
  if (type === "function") return "[Function: " + (value.name || "anonymous") + "]";

  if (value instanceof Error) {
    return value.name + ": " + value.message;
  }

  if (seen.has(value)) return "[Circular]";
  if (depth >= MAX_DEPTH) return Array.isArray(value) ? "[Array]" : "[Object]";
  seen.add(value);

  try {
    if (Array.isArray(value)) {
      const shown = value.slice(0, 100).map((item) => formatValue(item, depth + 1, seen));
      if (value.length > 100) shown.push("… " + (value.length - 100) + " more");
      return "[" + shown.join(", ") + "]";
    }
    if (value instanceof Map) {
      const pairs = [];
      for (const [key, item] of value) {
        pairs.push(formatValue(key, depth + 1, seen) + " => " + formatValue(item, depth + 1, seen));
        if (pairs.length >= 100) break;
      }
      return "Map(" + value.size + ") {" + pairs.join(", ") + "}";
    }
    if (value instanceof Set) {
      const items = [];
      for (const item of value) {
        items.push(formatValue(item, depth + 1, seen));
        if (items.length >= 100) break;
      }
      return "Set(" + value.size + ") {" + items.join(", ") + "}";
    }
    if (value instanceof Date) return value.toISOString();
    if (value instanceof RegExp) return value.toString();
    if (value instanceof Promise) return "Promise { <pending> }";

    const keys = Object.keys(value).slice(0, 100);
    const body = keys
      .map((key) => key + ": " + formatValue(value[key], depth + 1, seen))
      .join(", ");
    const name = value.constructor && value.constructor.name;
    const prefix = name && name !== "Object" ? name + " " : "";
    return prefix + "{" + (body ? " " + body + " " : "") + "}";
  } catch (error) {
    return "[Unserializable]";
  } finally {
    seen.delete(value);
  }
}

function record(level, args) {
  if (entries.length >= MAX_ENTRIES) {
    truncated = true;
    return;
  }
  let text = Array.prototype.map
    .call(args, (arg) => formatValue(arg, 0, new Set()))
    .join(" ");
  if (text.length > MAX_TEXT_LENGTH) {
    text = text.slice(0, MAX_TEXT_LENGTH) + "…";
  }
  entries.push({ level: level, text: text });
}

self.console = {
  log: function () { record("log", arguments); },
  info: function () { record("info", arguments); },
  debug: function () { record("log", arguments); },
  warn: function () { record("warn", arguments); },
  error: function () { record("error", arguments); },
  table: function () { record("log", arguments); },
  dir: function () { record("log", arguments); },
  trace: function () { record("log", arguments); },
  group: function () { record("log", arguments); },
  groupEnd: function () {},
  time: function () {},
  timeEnd: function () {},
  assert: function (condition) {
    if (!condition) {
      record("error", Array.prototype.slice.call(arguments, 1));
    }
  },
  count: function () {},
  clear: function () { entries = []; },
};

// --- Оролт: prompt() -------------------------------------------------------
let stdinLines = [];
let stdinIndex = 0;

self.prompt = function (message) {
  if (message !== undefined && message !== null && String(message) !== "") {
    record("info", [String(message)]);
  }
  if (stdinIndex >= stdinLines.length) return null;
  return stdinLines[stdinIndex++];
};

function finish(error) {
  self.postMessage({
    type: "result",
    entries: entries,
    truncated: truncated,
    error: error
      ? { name: error.name || "Error", message: error.message || String(error) }
      : null,
  });
}

// Хэрэглэгчийн барьж аваагүй promise-ийн алдааг ч харуулна.
self.addEventListener("unhandledrejection", function (event) {
  const reason = event.reason;
  record("error", [
    "Uncaught (in promise) " +
      (reason && reason.message ? reason.name + ": " + reason.message : String(reason)),
  ]);
});

self.addEventListener("message", function (event) {
  const code = event.data && event.data.code;
  entries = [];
  truncated = false;
  // Төгсгөлийн шинэ мөр нь «хоосон мөр» болж prompt()-т ирэхгүй.
  const stdin = String((event.data && event.data.stdin) || "").replace(/\r\n?/g, "\n");
  stdinLines = stdin === "" ? [] : stdin.replace(/\n$/, "").split("\n");
  stdinIndex = 0;

  try {
    // Шууд eval биш — хэрэглэгчийн код worker-ийн дотоод хувьсагчдад хүрэхгүй.
    // AsyncFunction ашигласнаар суралцагч top-level await бичиж чадна.
    const run = new AsyncFunction('"use strict";\n' + code);
    const returned = run();

    if (returned && typeof returned.then === "function") {
      returned.then(
        function () { finish(null); },
        function (error) { finish(error); },
      );
      return;
    }
    finish(null);
  } catch (error) {
    finish(error);
  }
});
`;
