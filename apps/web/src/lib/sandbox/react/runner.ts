/**
 * React sandbox — хуудасны тал.
 *
 * Сурагчийн код `sandbox="allow-scripts allow-forms"` iframe дотор ажиллана.
 * `allow-same-origin` БАЙХГҮЙ тул iframe нь opaque origin-той: MedlegHub-ийн
 * cookie, localStorage, DOM-д хүрэхгүй, манай API руу хүсэлт илгээж
 * чадахгүй (CORS). Мөн хуудасны CSP (`script-src`, `connect-src`)-ийг
 * өвлөнө — гадаад сүлжээ хаалттай.
 *
 * Runtime (`/sandbox/react-runtime.js`, ~1 MB) нь URL-аар ачаалагдаж хөтчийн
 * кэшд хадгалагдана. Зарим хөтөч sandbox iframe-д `'self'`-ийг зөвшөөрөхгүй
 * бол runtime «runtime-missing» гэж хэлнэ — тэгвэл текстийг нь татаж
 * `srcdoc` дотор шууд оруулна.
 */

import { entryFile, htmlOf, isHtmlFile, type LessonFile } from "@/lib/sandbox/react/files";
import {
  JOB_ELEMENT_ID,
  MESSAGE_SOURCE,
  RUNTIME_GLOBAL,
  TEST_TIMEOUT_MS,
  type SandboxCommandBody,
  type SandboxJob,
  type SandboxMessage,
} from "@/lib/sandbox/react/protocol";

export const RUNTIME_URL = "/sandbox/react-runtime.js";

/** Iframe-ийн эрх. `allow-forms` — форм илгээх үйл явдал (`onSubmit`) ажиллана. */
export const SANDBOX_PERMISSIONS = "allow-scripts allow-forms";

/** Хөтчийн анхдагч загвар — сурагч өөрийн CSS-ээр дарна. */
const BASE_STYLE =
  "html{color-scheme:light}body{font-family:system-ui,-apple-system,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif;line-height:1.5;color:#1f2328;background:#fff}";

let runCounter = 0;

export function nextRunId(): number {
  runCounter += 1;
  return runCounter;
}

export function createJob(
  files: LessonFile[],
  mode: SandboxJob["mode"],
  extra: Partial<Pick<SandboxJob, "tests" | "storage" | "path">> = {},
): SandboxJob {
  return {
    runId: nextRunId(),
    mode,
    files: files.filter((file) => !isHtmlFile(file.name)).map(({ name, code }) => ({ name, code })),
    entry: entryFile(files),
    html: htmlOf(files),
    ...extra,
  };
}

/** `</script>` болон `<!--`-ийг JSON дотор аюулгүй болгоно. */
function embedJson(value: unknown): string {
  return JSON.stringify(value).replace(/</g, "\\u003c");
}

export function buildDocument(job: SandboxJob, inlineRuntime?: string): string {
  const runtime =
    inlineRuntime !== undefined
      ? `<script>${inlineRuntime.replace(/<\/script/gi, "<\\/script")}</script>`
      : `<script src="${RUNTIME_URL}"></script>`;
  const boot =
    `(function(){var s=window.${RUNTIME_GLOBAL};if(s){s.boot();}else{` +
    `parent.postMessage({source:${JSON.stringify(MESSAGE_SOURCE)},runId:${job.runId},type:"runtime-missing"},"*");}})();`;
  return (
    '<!doctype html><html lang="mn"><head><meta charset="utf-8">' +
    '<meta name="viewport" content="width=device-width,initial-scale=1">' +
    `<title>React App</title><style>${BASE_STYLE}</style></head><body>` +
    `<script type="application/json" id="${JOB_ELEMENT_ID}">${embedJson(job)}</script>` +
    `${runtime}<script>${boot}</script></body></html>`
  );
}

let inlineRuntime: Promise<string> | null = null;

function loadInlineRuntime(): Promise<string> {
  inlineRuntime ??= fetch(RUNTIME_URL).then((response) => {
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return response.text();
  });
  inlineRuntime.catch(() => {
    inlineRuntime = null;
  });
  return inlineRuntime;
}

function isSandboxMessage(data: unknown): data is SandboxMessage {
  if (!data || typeof data !== "object") return false;
  const message = data as Record<string, unknown>;
  return (
    message.source === MESSAGE_SOURCE &&
    typeof message.runId === "number" &&
    typeof message.type === "string"
  );
}

/**
 * Iframe-д ажил ачаалж, мессежийг сонсоно. Буцаах функц нь сонсохоо зогсооно.
 * Мессежийг зөвхөн ЭНЭ iframe-ээс, ЭНЭ ажиллуулалтаас л хүлээн авна.
 */
export function mountSandbox(
  iframe: HTMLIFrameElement,
  job: SandboxJob,
  onMessage: (message: SandboxMessage) => void,
): () => void {
  let active = true;
  const listener = (event: MessageEvent) => {
    if (event.source !== iframe.contentWindow || !isSandboxMessage(event.data)) return;
    const message = event.data;
    if (message.runId !== job.runId) return;
    if (message.type === "runtime-missing") {
      loadInlineRuntime().then(
        (text) => {
          if (active) iframe.srcdoc = buildDocument(job, text);
        },
        () => {
          if (!active) return;
          onMessage({
            source: MESSAGE_SOURCE,
            runId: job.runId,
            type: "error",
            error: {
              kind: "runtime",
              message:
                "Sandbox ачаалж чадсангүй. Интернэт холболтоо шалгаад хуудсаа дахин ачаална уу.",
            },
          });
        },
      );
      return;
    }
    onMessage(message);
  };
  window.addEventListener("message", listener);
  iframe.srcdoc = buildDocument(job);
  return () => {
    active = false;
    window.removeEventListener("message", listener);
  };
}

export function sendCommand(iframe: HTMLIFrameElement | null, command: SandboxCommandBody) {
  iframe?.contentWindow?.postMessage({ source: MESSAGE_SOURCE, ...command }, "*");
}

// --- Тест --------------------------------------------------------------------

export interface ReactTestResult {
  passed: boolean;
  message?: string;
}

/**
 * Тест БҮРИЙГ шинэ iframe-д дарааллаар нь ажиллуулна.
 *
 * Нэг iframe-д олон тест ажиллуулбал нэг тестийн дуусаагүй зүйл (async
 * Action, timer, window-ийн listener) дараагийнхыг бохирдуулдаг — жишээ нь
 * React-ийн дуусаагүй Action нь дараагийн тестүүдийн `isPending`-ийг үүрд
 * `true` болгоно. Тест бүр өөрийн React, DOM, timer-тэй тул бие биедээ
 * нөлөөлөхгүй. Runtime нь хөтчийн кэшээс ачаалагдах тул нэмэлт хугацаа бага.
 */
export async function runReactTests(
  files: LessonFile[],
  tests: { name: string; code: string }[],
  onResult: (index: number, result: ReactTestResult) => void,
): Promise<ReactTestResult[]> {
  const results: ReactTestResult[] = [];
  for (const [index, test] of tests.entries()) {
    const [result] = await runInFrame(files, [test]);
    results.push(result);
    onResult(index, result);
  }
  return results;
}

/**
 * Нуугдмал iframe. `display:none` биш — зарим хөтөч тийм iframe-ийн timer-ийг
 * удаашруулдаг тул дэлгэцийн гадна байрлуулна.
 */
function runInFrame(
  files: LessonFile[],
  tests: { name: string; code: string }[],
): Promise<ReactTestResult[]> {
  const job = createJob(files, "test", { tests });
  const results: (ReactTestResult | undefined)[] = tests.map(() => undefined);

  return new Promise((resolve) => {
    const iframe = document.createElement("iframe");
    iframe.setAttribute("sandbox", SANDBOX_PERMISSIONS);
    iframe.setAttribute("aria-hidden", "true");
    iframe.tabIndex = -1;
    iframe.title = "tests";
    iframe.style.cssText =
      "position:fixed;left:-10000px;top:0;width:1024px;height:768px;border:0;opacity:0;pointer-events:none";

    let stop = () => {};
    const finish = () => {
      clearTimeout(timer);
      stop();
      iframe.remove();
      resolve(
        results.map(
          (result) =>
            result ?? {
              passed: false,
              message:
                "Тест дуусаагүй — хугацаа хэтэрлээ. Төгсгөлгүй давталт байгаа эсэхийг шалга.",
            },
        ),
      );
    };
    // Нэг тестийн хязгаар нь runtime дотор. Энэ нь бүхэл iframe гацсан үеийнх.
    const timer = setTimeout(finish, 8000 + tests.length * TEST_TIMEOUT_MS);

    document.body.appendChild(iframe);
    stop = mountSandbox(iframe, job, (message) => {
      if (message.type === "test-result" && message.index >= 0 && message.index < tests.length) {
        results[message.index] = { passed: message.passed === true, message: message.message };
      } else if (message.type === "tests-done") {
        finish();
      } else if (message.type === "error") {
        results.forEach((result, index) => {
          if (!result) results[index] = { passed: false, message: message.error.message };
        });
        finish();
      }
    });
  });
}
