/**
 * React sandbox-ийн хөтөч (гол хуудас) ба iframe хоорондын гэрээ.
 *
 * Энэ файлыг хоёр тал ИЖИЛХЭН импортолно: `runner.ts` (Next апп) болон
 * `react-runtime/` (esbuild-ээр `public/sandbox/react-runtime.js` болж
 * iframe дотор ажиллана). Иймээс энд зөвхөн төрөл, тогтмол байна.
 */

/** Iframe-д өгөх ажил. `srcdoc` доторх JSON-оор дамжина. */
export interface SandboxJob {
  runId: number;
  mode: "preview" | "test";
  /** Засварлагдах болон түгжигдсэн JS/CSS файлууд (`index.html`-ээс бусад). */
  files: { name: string; code: string }[];
  /** Ажиллуулж эхлэх файл — `main.jsx` гэх мэт. */
  entry: string;
  /** `index.html`-ийн агуулга — `<body>`-д орно. */
  html: string;
  /** Router-ийн эхлэх зам. «Дахин ачаалах» үед одоогийн замдаа үлдэнэ. */
  path?: string;
  /** Туршилтын горимд л: дасгалын тестүүд. */
  tests?: { name: string; code: string }[];
  /** Өмнөх ажиллуулалтаас үлдсэн `localStorage` — «дахин ачаалах» мэт. */
  storage?: Record<string, string>;
}

export type ConsoleLevel = "log" | "info" | "warn" | "error";

export interface SandboxError {
  /** `compile` — синтакс алдаа, код огт ажиллаагүй. */
  kind: "compile" | "runtime";
  message: string;
  file?: string;
  line?: number;
  column?: number;
}

/** Iframe → хуудас. `runId` нь хуучирсан ажиллуулалтын мессежийг ялгана. */
export type SandboxMessage =
  | { source: typeof MESSAGE_SOURCE; runId: number; type: "ready" }
  | { source: typeof MESSAGE_SOURCE; runId: number; type: "runtime-missing" }
  | {
      source: typeof MESSAGE_SOURCE;
      runId: number;
      type: "console";
      level: ConsoleLevel;
      text: string;
    }
  | { source: typeof MESSAGE_SOURCE; runId: number; type: "error"; error: SandboxError }
  | { source: typeof MESSAGE_SOURCE; runId: number; type: "title"; title: string }
  | {
      source: typeof MESSAGE_SOURCE;
      runId: number;
      type: "location";
      path: string;
      canGoBack: boolean;
      canGoForward: boolean;
    }
  | {
      source: typeof MESSAGE_SOURCE;
      runId: number;
      type: "storage";
      data: Record<string, string>;
    }
  | {
      source: typeof MESSAGE_SOURCE;
      runId: number;
      type: "test-result";
      index: number;
      passed: boolean;
      message?: string;
    }
  | { source: typeof MESSAGE_SOURCE; runId: number; type: "tests-done" };

/** Хуудас → iframe: хаягийн мөрний сум, хаяг. */
export type SandboxCommandBody =
  { type: "navigate"; to: "back" | "forward" } | { type: "navigate"; to: "path"; path: string };

export type SandboxCommand = SandboxCommandBody & { source: typeof MESSAGE_SOURCE };

/** Бусад `postMessage`-ээс ялгах тэмдэг (Monaco, өргөтгөл гэх мэт). */
export const MESSAGE_SOURCE = "medleghub-react-sandbox";

/** Iframe дотор runtime-ийг хадгалах глобал нэр. */
export const RUNTIME_GLOBAL = "__medleghubSandbox";

/** Ажлыг `srcdoc` дотор хадгалах `<script type="application/json">`-ийн id. */
export const JOB_ELEMENT_ID = "medleghub-job";

/**
 * Нэг тестийн хугацааны хязгаар. `waitFor` (2 сек) болон «Модул 13»-ын
 * сурагчийн тест файлыг хоёр удаа ажиллуулах хугацаа багтана.
 */
export const TEST_TIMEOUT_MS = 8000;
