/**
 * React хичээлийн олон файлыг нэг `initial_code` мөрөнд хадгалах хэлбэр.
 *
 *     // @file App.jsx
 *     export default function App() { … }
 *     // @file main.jsx locked
 *     import { createRoot } from "react-dom/client";
 *     …
 *     // @file index.html locked
 *     <div id="root"></div>
 *
 * `// @file <нэр>` мөр бүр шинэ файл эхлүүлнэ. `locked` бол засварлагч
 * зөвхөн уншигдана (react-tutorial.app-ийн 🔒 index.html шиг). Тэмдэггүй код
 * бүхэлдээ ганц `App.jsx` болно.
 *
 * Жишиг шийдэл (`solution`) ч мөн энэ хэлбэртэй — зөвхөн өөрчлөгдөх
 * файлуудаа агуулна, бусад нь эхлэл кодоос авна (`overlayFiles`).
 *
 * HTML & CSS хичээл ч энэ хэлбэртэй (`index.html` + `style.css`); тэмдэггүй
 * код нь `index.html` эсвэл `style.css` болно — `defaultName`.
 *
 * `apps/api/app/content/react/`, `apps/api/app/content/html_css/common.py`
 * дахь Python талын шалгалт энэ дүрмийг давтдаг — өөрчилбөл хамтад нь засна.
 */

export interface LessonFile {
  name: string;
  code: string;
  locked: boolean;
}

const MARKER = /^\/\/ @file (\S+)( locked)?\s*$/;

/** Тэмдэггүй кодын анхдагч нэр. */
export const DEFAULT_FILE = "App.jsx";

export const DEFAULT_HTML = '<div id="root"></div>';

export function parseLessonFiles(source: string, defaultName = DEFAULT_FILE): LessonFile[] {
  const lines = source.replace(/\r\n?/g, "\n").split("\n");
  const files: LessonFile[] = [];
  let current: { name: string; locked: boolean; lines: string[] } | null = null;
  const preamble: string[] = [];

  const flush = () => {
    if (!current) return;
    files.push({ name: current.name, locked: current.locked, code: tidy(current.lines) });
  };

  for (const line of lines) {
    const match = MARKER.exec(line);
    if (match) {
      flush();
      current = { name: match[1], locked: Boolean(match[2]), lines: [] };
    } else if (current) {
      current.lines.push(line);
    } else {
      preamble.push(line);
    }
  }
  flush();

  if (files.length === 0) {
    return [{ name: defaultName, locked: false, code: tidy(preamble) }];
  }
  return files;
}

/** Эхний болон төгсгөлийн хоосон мөрийг авч, нэг шинэ мөрөөр төгсгөнө. */
function tidy(lines: string[]): string {
  let start = 0;
  let end = lines.length;
  while (start < end && lines[start].trim() === "") start++;
  while (end > start && lines[end - 1].trim() === "") end--;
  return lines.slice(start, end).join("\n") + "\n";
}

/** Шийдлийн файлууд эхлэл кодын ижил нэртэй файлыг орлоно. */
export function overlayFiles(base: LessonFile[], overlay: LessonFile[]): LessonFile[] {
  const byName = new Map(overlay.map((file) => [file.name, file]));
  const merged = base.map((file) =>
    byName.has(file.name) ? { ...file, code: byName.get(file.name)!.code } : file,
  );
  for (const file of overlay) {
    if (!base.some((existing) => existing.name === file.name)) merged.push(file);
  }
  return merged;
}

export function isHtmlFile(name: string): boolean {
  return name.endsWith(".html");
}

/**
 * Эхлэх файл: Vite-ийн `main.jsx`, дараа нь `index.jsx`/`index.js`, эс бөгөөс
 * эхний JavaScript файл.
 */
export function entryFile(files: LessonFile[]): string {
  const names = files.map((file) => file.name);
  for (const candidate of ["main.jsx", "main.js", "index.jsx", "index.js"]) {
    if (names.includes(candidate)) return candidate;
  }
  return names.find((name) => /\.(jsx?|mjs)$/.test(name)) ?? DEFAULT_FILE;
}

/** `index.html`-ийн агуулга — iframe-ийн `<body>` болно. */
export function htmlOf(files: LessonFile[]): string {
  return files.find((file) => isHtmlFile(file.name))?.code ?? DEFAULT_HTML;
}

/** Monaco-ийн хэлний ID. */
export function monacoLanguage(name: string): string {
  if (name.endsWith(".html")) return "html";
  if (name.endsWith(".css")) return "css";
  if (name.endsWith(".json")) return "json";
  return "javascript";
}
