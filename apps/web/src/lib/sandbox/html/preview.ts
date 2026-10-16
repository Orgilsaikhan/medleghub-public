/**
 * HTML & CSS хичээлийн «Хөтөч» — сурагчийн хуудсыг sandbox iframe-д харуулна.
 *
 * Хуудас нь `srcdoc`-оор ачаалагдана. `allow-same-origin` БАЙХГҮЙ тул iframe
 * нь opaque origin-той: MedlegHub-ийн cookie, localStorage, DOM-д хүрэхгүй.
 * Хуудасны CSP-г өвлөнө (`connect-src` гэх мэт) — React sandbox-тай ижил.
 *
 * Жинхэнэ хөтөч шиг ажиллахын тулд:
 *   • `<link rel="stylesheet" href="style.css">` нь хичээлийн `style.css`-ийг
 *     `<style>` болгон оруулна. Холбоогүй CSS нөлөөлөхгүй.
 *   • Iframe доторх жижиг script (`bridge`) холбоосыг барина: `#id` нь хуудас
 *     дотроо гүйлгэнэ, `tuhai.html` нь тэр файлыг нээнэ, бусдыг хуудас
 *     тайлбарлана. `srcdoc`-ийн үндсэн хаяг нь MedlegHub-ийн хуудас тул
 *     барихгүй бол iframe манай сайт руу шилжиж хаагдана.
 *   • Форм илгээхэд хуудас солигдохгүй — илгээх байсан өгөгдлийг харуулна.
 *   • `alert()` нь цонх биш, хөтчийн доод талд мэдэгдэл болно.
 *   • CSS л өөрчлөгдвөл хуудсыг дахин ачаалалгүй `<style>`-ийг сольно —
 *     анивчихгүй, гүйлгэсэн байрлал алдагдахгүй.
 */

import type { LessonFile } from "@/lib/sandbox/react/files";

/** Бусад `postMessage`-ээс ялгах тэмдэг. */
export const PREVIEW_SOURCE = "medleghub-html-preview";

/**
 * Iframe-ийн эрх. `allow-scripts` — дээрх `bridge` болон сурагчийн script.
 * `allow-forms` — `required`, `pattern`-ийн шалгалтын бөмбөлөг харагдана
 * (үгүй бол хөтөч илгээлтийг шалгалтгүйгээр хаадаг).
 */
export const PREVIEW_PERMISSIONS = "allow-scripts allow-forms";

/** Iframe → хуудас. `runId` нь хуучирсан хуудасны мессежийг ялгана. */
export type PreviewMessage =
  | { type: "title"; title: string }
  | { type: "scroll"; y: number }
  | { type: "link"; href: string }
  | { type: "submit"; action: string; method: string; fields: [string, string][] }
  | { type: "alert"; text: string };

/** `<style data-medleghub-file="…">` — CSS-ийг дахин ачаалалгүй сольдог. */
const STYLE_ATTRIBUTE = "data-medleghub-file";

export function isPageFile(name: string): boolean {
  return name.endsWith(".html");
}

/** Хөтөч эхлээд харуулах хуудас: `index.html`, эс бөгөөс эхний `.html`. */
export function homePage(files: LessonFile[]): string | null {
  const pages = files.filter((file) => isPageFile(file.name)).map((file) => file.name);
  return pages.includes("index.html") ? "index.html" : (pages[0] ?? null);
}

const BASE = "http://preview.invalid/";

/**
 * Хуудсаас харьцангуй хаяг (`tuhai.html`, `../index.html#deed`, `/`) →
 * файлын нэр ба `#` хэсэг. Схемтэй (`https:`, `mailto:`) бол `null`.
 */
export function resolvePath(href: string, from: string): { path: string; hash: string } | null {
  const trimmed = href.trim();
  if (/^[a-z][a-z\d+.-]*:/i.test(trimmed) || trimmed.startsWith("//")) return null;
  try {
    const url = new URL(trimmed, BASE + from);
    let path = decodeURIComponent(url.pathname.slice(1));
    if (path === "" || path.endsWith("/")) path += "index.html";
    return { path, hash: decodeURIComponent(url.hash.slice(1)) };
  } catch {
    return null;
  }
}

/** HTML-ийн тайлбар (`<!-- … -->`) доторхыг алгасаж шошго хайна. */
function scanTags(html: string, tag: RegExp): RegExp {
  return new RegExp(`<!--[\\s\\S]*?(?:-->|$)|${tag.source}`, "gi");
}

function attribute(tag: string, name: string): string | null {
  const match = new RegExp(`\\s${name}\\s*=\\s*(?:"([^"]*)"|'([^']*)'|([^\\s"'>]+))`, "i").exec(
    tag,
  );
  return match ? (match[1] ?? match[2] ?? match[3] ?? "") : null;
}

/** `<link rel="stylesheet" href="style.css">` → хичээлийн файлын агуулга. */
function inlineStylesheets(html: string, page: string, files: LessonFile[], used: Set<string>) {
  return html.replace(scanTags(html, /<link\b[^>]*>/), (tag) => {
    if (tag.startsWith("<!--")) return tag;
    const rel = (attribute(tag, "rel") ?? "").toLowerCase().split(/\s+/);
    const href = attribute(tag, "href");
    if (!rel.includes("stylesheet") || href === null) return tag;
    const target = resolvePath(href, page);
    if (!target) return tag; // Гадаад CSS — CSP хаана, жинхэнэ хөтөч шиг.
    const file = files.find((candidate) => candidate.name === target.path);
    // Байхгүй файл — жинхэнэ хөтөчид 404, CSS нөлөөлөхгүй. Манай сайт руу
    // хүсэлт явуулахгүйн тулд хасна.
    if (!file) return "";
    used.add(file.name);
    return `<style ${STYLE_ATTRIBUTE}="${file.name}">${escapeStyle(file.code)}</style>`;
  });
}

function escapeStyle(css: string): string {
  return css.replace(/<\/style/gi, "<\\/style");
}

/**
 * `bridge`-ийг `<head>`-ийн эхэнд (эсвэл `<html>`, `<!DOCTYPE>`-ийн дараа)
 * оруулна. DOCTYPE-ийн өмнө юу ч бичвэл хөтөч quirks горимд орно.
 */
function inject(html: string, snippet: string): string {
  for (const tag of [/<head\b[^>]*>/, /<html\b[^>]*>/, /<!doctype\b[^>]*>/]) {
    const scanner = scanTags(html, tag);
    let match: RegExpExecArray | null;
    while ((match = scanner.exec(html))) {
      if (match[0].startsWith("<!--")) continue;
      const end = match.index + match[0].length;
      return html.slice(0, end) + snippet + html.slice(end);
    }
  }
  return snippet + html;
}

interface BridgeOptions {
  runId: number;
  /** Ачаалсны дараа гүйлгэх байрлал — засварын дараа хуудас үсрэхгүй. */
  scrollY: number;
  /** `tuhai.html#bagsh` — ачаалсны дараа энэ id руу гүйлгэнэ. */
  hash: string;
}

/** Iframe дотор ажиллах script. Сурагчийн хуудаснаас өмнө ачаалагдана. */
function bridge({ runId, scrollY, hash }: BridgeOptions): string {
  return `(function () {
  var SOURCE = ${JSON.stringify(PREVIEW_SOURCE)}, RUN = ${runId};
  var restoreY = ${Math.max(0, Math.round(scrollY))}, restoreHash = ${JSON.stringify(hash)};
  var userScrolled = false;
  function post(message) {
    message.source = SOURCE;
    message.runId = RUN;
    parent.postMessage(message, "*");
  }
  function decode(text) {
    try { return decodeURIComponent(text); } catch (error) { return text; }
  }
  function jump(id) {
    var target = id ? document.getElementById(id) : null;
    if (target) target.scrollIntoView();
    else if (!id || id === "top") window.scrollTo(0, 0);
  }
  function restore() {
    if (userScrolled) return;
    if (restoreHash) jump(restoreHash);
    else if (restoreY) window.scrollTo(0, restoreY);
  }
  window.alert = function (text) {
    post({ type: "alert", text: String(text === undefined ? "" : text) });
  };
  document.addEventListener("DOMContentLoaded", function () {
    post({ type: "title", title: document.title });
    restore();
  });
  /* Зураг ачаалагдаж байрлал өөрчлөгдсөн байж болно. */
  window.addEventListener("load", restore);
  ["wheel", "touchstart", "keydown"].forEach(function (name) {
    window.addEventListener(name, function () { userScrolled = true; }, { passive: true });
  });
  var timer = 0;
  window.addEventListener("scroll", function () {
    clearTimeout(timer);
    timer = setTimeout(function () { post({ type: "scroll", y: window.scrollY }); }, 120);
  }, { passive: true });
  window.addEventListener("click", function (event) {
    if (event.defaultPrevented) return;
    var node = event.target;
    var link = node && node.closest ? node.closest("a[href]") : null;
    if (!link) return;
    event.preventDefault();
    var href = link.getAttribute("href");
    if (href.charAt(0) === "#") {
      userScrolled = true;
      jump(decode(href.slice(1)));
      return;
    }
    post({ type: "link", href: href });
  });
  window.addEventListener("submit", function (event) {
    if (event.defaultPrevented) return;
    event.preventDefault();
    var form = event.target, fields = [], data;
    try { data = new FormData(form, event.submitter); } catch (error) { data = new FormData(form); }
    data.forEach(function (value, key) {
      fields.push([key, typeof value === "string" ? value : value.name]);
    });
    post({
      type: "submit",
      action: form.getAttribute("action") || "",
      method: (form.getAttribute("method") || "get").toLowerCase(),
      fields: fields
    });
  });
  window.addEventListener("message", function (event) {
    var data = event.data;
    if (event.source !== parent || !data || data.source !== SOURCE || data.type !== "style") return;
    var nodes = document.querySelectorAll("style[${STYLE_ATTRIBUTE}]");
    for (var i = 0; i < nodes.length; i++) {
      if (nodes[i].getAttribute("${STYLE_ATTRIBUTE}") === data.file) nodes[i].textContent = data.code;
    }
  });
})();`;
}

export interface BuiltPreview {
  srcdoc: string;
  /** Хуудсанд `<style>` болж орсон CSS файлууд — өөрчлөгдвөл шууд солигдоно. */
  styles: string[];
}

export function buildPreview(
  files: LessonFile[],
  page: string,
  options: BridgeOptions,
): BuiltPreview {
  const html = files.find((file) => file.name === page)?.code ?? "";
  const used = new Set<string>();
  const withStyles = inlineStylesheets(html, page, files, used);
  const script = `<script>${bridge(options).replace(/<\/script/gi, "<\\/script")}</script>`;
  return { srcdoc: inject(withStyles, script), styles: [...used] };
}

/** Хуудас → iframe: CSS файлыг дахин ачаалалгүй солих. */
export function sendStyle(iframe: HTMLIFrameElement | null, file: string, code: string) {
  iframe?.contentWindow?.postMessage({ source: PREVIEW_SOURCE, type: "style", file, code }, "*");
}

/** Iframe-ээс ирсэн мессежийг шалгана — хэлбэр нь сурагчийн кодоос хамаарч болно. */
export function readPreviewMessage(data: unknown, runId: number): PreviewMessage | null {
  if (!data || typeof data !== "object") return null;
  const message = data as Record<string, unknown>;
  if (message.source !== PREVIEW_SOURCE || message.runId !== runId) return null;
  const text = (value: unknown, max = 2000) =>
    typeof value === "string" ? value.slice(0, max) : "";
  switch (message.type) {
    case "title":
      return { type: "title", title: text(message.title, 200) };
    case "scroll":
      return typeof message.y === "number" && Number.isFinite(message.y)
        ? { type: "scroll", y: message.y }
        : null;
    case "link":
      return { type: "link", href: text(message.href) };
    case "alert":
      return { type: "alert", text: text(message.text) };
    case "submit": {
      const fields = Array.isArray(message.fields)
        ? message.fields
            .filter((pair): pair is [unknown, unknown] => Array.isArray(pair) && pair.length === 2)
            .slice(0, 50)
            .map(([key, value]): [string, string] => [text(key, 200), text(value, 500)])
        : [];
      return {
        type: "submit",
        action: text(message.action),
        method: text(message.method, 10) || "get",
        fields,
      };
    }
    default:
      return null;
  }
}
