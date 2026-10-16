/**
 * Python sandbox worker-ийн эх код (мөр хэлбэрээр).
 *
 * JavaScript-ийн worker-тэй ижил зарчим: хэрэглэгчийн код зөвхөн worker дотор
 * ажиллана, гол thread нь хугацааг хэмжинэ. Ялгаа нь:
 *
 *   1. Pyodide нь ES module — тиймээс энэ worker нь `{ type: "module" }`
 *      байдлаар үүснэ. Classic worker-ийн `importScripts` ажиллахгүй.
 *
 *   2. ХАМГААЛАЛТЫН ДАРААЛАЛ УРВУУ. Pyodide өөрийн WebAssembly болон
 *      стандарт санг татахын тулд `fetch` хэрэгтэй. Тиймээс эхлээд ачаална,
 *      ДАРАА НЬ сүлжээний API-г устгана, ТЭГЭЭД хэрэглэгчийн кодыг хүлээж
 *      авна. Энэ дараалал буруу бол сүлжээ нээлттэй үлдэнэ.
 *
 *   3. Багц суулгах боломжгүй. Стандарт сан бүхэлдээ `python_stdlib.zip`
 *      дотор ирдэг тул сүлжээ хаасны дараа ч math, json, dataclasses,
 *      pathlib, collections зэрэг бүгд ажиллана. `requests`, `sqlalchemy`
 *      зэрэг гуравдагч санг татахгүй — энэ нь зориуд тавьсан хязгаарлалт.
 *
 * ГАРАЛТ
 * ──────
 * stdout/stderr-ийг байт хэлбэрээр авч мөр болгож хуваана (`write` горим).
 * Pyodide-ийн мөрөөр багцлах горим нь шинэ мөргүй төгссөн гаралтыг
 * (`print(x, end="")`) хэзээ ч гаргадаггүй байсан — ажиллуулалт бүрийн
 * төгсгөлд урсгалыг хоослож, дуусаагүй мөрийг ч харуулна.
 *
 * ТЕСТИЙН ГОРИМ (`mode: "test"`)
 * ──────────────────────────────
 * Дасгалын тест бүр ЦЭВЭР нэрийн талбарт (`__name__ == "__main__"`)
 * ажиллана — өмнөх тестийн хувьсагч дараагийнхад үлдэхгүй. `input()`-ийн
 * асуултыг гаралтад бичихгүй: хүлээгдэж буй гаралттай харьцуулдаг тул
 * «Нэрээ оруулна уу: » гэх мэт асуулт сурагчийг унагах ёсгүй.
 *
 * АНХААР: энэ файлыг `String.raw` ашиглан бичсэн тул дотор нь ` тэмдэг
 * болон ${ дараалал бичиж болохгүй — template literal тасарна.
 */

export const PYTHON_WORKER_SOURCE = String.raw`
// --- Гаралт цуглуулах ------------------------------------------------------
const MAX_ENTRIES = 500;
const MAX_TEXT_LENGTH = 5000;

let entries = [];
let truncated = false;

function record(level, text) {
  if (entries.length >= MAX_ENTRIES) {
    truncated = true;
    return;
  }
  let line = String(text);
  if (line.length > MAX_TEXT_LENGTH) {
    line = line.slice(0, MAX_TEXT_LENGTH) + "…";
  }
  entries.push({ level: level, text: line });
}

// Урсгал бүрийн дуусаагүй мөр. Олон байтын UTF-8 үсэг хоёр write-д
// хуваагдаж болох тул decoder нь stream горимтой.
const streams = {
  log: { decoder: new TextDecoder("utf-8"), line: "" },
  error: { decoder: new TextDecoder("utf-8"), line: "" },
};

function writer(level) {
  return function (buffer) {
    const stream = streams[level];
    const parts = (stream.line + stream.decoder.decode(buffer, { stream: true })).split("\n");
    stream.line = parts.pop();
    for (const part of parts) record(level, part);
    return buffer.length;
  };
}

// Ажиллуулалтын төгсгөлд — Python-ий буфер болон дуусаагүй мөрийг гаргана.
function flushOutput() {
  try {
    pyodide.runPython("import sys\nsys.stdout.flush()\nsys.stderr.flush()");
  } catch (_) {
    // Сурагч sys.stdout-ийг сольсон байж болно — бидний мөр л хангалттай.
  }
  for (const level of ["log", "error"]) {
    const stream = streams[level];
    stream.line += stream.decoder.decode();
    if (stream.line) record(level, stream.line);
    stream.line = "";
  }
}

// --- Стандарт оролт --------------------------------------------------------
// input() дуудагдах бүрд дараагийн мөрийг өгнө. Мөр дуусвал null буцааж
// EOF мэдэгдэнэ — Python талд EOFError болно.
let stdinLines = [];
let stdinIndex = 0;

function nextStdinLine() {
  if (stdinIndex >= stdinLines.length) return null;
  return stdinLines[stdinIndex++];
}

// --- Алдааны мөрийг цэвэрлэх ----------------------------------------------
// Pyodide-ийн traceback нь өөрийн дотоод frame-үүдийг агуулдаг
// (_pyodide/_base.py гэх мэт). Сурагчид тэдгээр нь утгагүй — зөвхөн
// өөрийнх нь кодын мөрийг үлдээнэ.
function cleanTraceback(message) {
  const lines = String(message).split("\n");
  const kept = [];

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const isFrame = /^\s*File "/.test(line);

    if (isFrame) {
      const internal =
        line.indexOf("/lib/python") !== -1 ||
        line.indexOf("_pyodide") !== -1 ||
        line.indexOf("pyodide/_package") !== -1;

      // Дотоод frame болон түүний доорх эх кодын мөрийг алгасна.
      if (internal) {
        while (i + 1 < lines.length && /^\s{4,}\S/.test(lines[i + 1]) && !/^\s*File "/.test(lines[i + 1])) {
          i++;
        }
        continue;
      }
      kept.push(line.replace(/File "<exec>", /, "").replace(/File "<unknown>", /, ""));
      continue;
    }
    kept.push(line);
  }

  return kept.join("\n").replace(/\n{3,}/g, "\n\n").trim();
}

// --- Pyodide-ийг ачаалах ---------------------------------------------------
let pyodide = null;

// Тестийн горимын туслахууд. Сурагчийн (Run горимын) нэрийн талбарт орохгүйн
// тулд тусдаа dict-д тодорхойлно.
//   quiet_input    — асуултгүй input: «Нэрээ оруулна уу: » гаралтад орохгүй.
//   enter_test_dir — тест бүр шинэ хоосон хавтаст ажиллана: өмнөх тест эсвэл
//                    «Код ажиллуулах»-ын үлдээсэн файл нөлөөлөхгүй. Мөн
//                    logging-ийн тохиргоог буцаана — Pyodide нь logging-ийг
//                    өөрөө ачаалдаг тул basicConfig өмнөх ажиллуулалтаас үлдэж,
//                    дараагийнх нь «юу ч хийгээгүй» мэт харагддаг байв.
const TEST_HELPERS = [
  "import builtins, logging, os, shutil, tempfile",
  "HOME = os.getcwd()",
  "BOOT_LOGGERS = set(logging.Logger.manager.loggerDict)",
  "BOOT_ROOT = (list(logging.root.handlers), logging.root.level)",
  "def quiet_input(prompt=''):",
  "    return builtins.input()",
  "def reset_logging():",
  "    logging.root.handlers[:] = BOOT_ROOT[0]",
  "    logging.root.setLevel(BOOT_ROOT[1])",
  "    for name in list(logging.Logger.manager.loggerDict):",
  "        if name not in BOOT_LOGGERS:",
  "            del logging.Logger.manager.loggerDict[name]",
  "def enter_test_dir():",
  "    reset_logging()",
  "    path = tempfile.mkdtemp(prefix='medleghub-test-')",
  "    os.chdir(path)",
  "    return path",
  "def leave_test_dir(path):",
  "    os.chdir(HOME)",
  "    shutil.rmtree(path, ignore_errors=True)",
].join("\n");

let quietInput = null;
let enterTestDir = null;
let leaveTestDir = null;

async function boot(indexURL) {
  const { loadPyodide } = await import(indexURL + "pyodide.mjs");

  pyodide = await loadPyodide({ indexURL: indexURL });

  // isatty — терминал шиг мөр бүрээр гаргана, stdout ба stderr-ийн дараалал
  // хадгалагдана.
  pyodide.setStdout({ write: writer("log"), isatty: true });
  pyodide.setStderr({ write: writer("error"), isatty: true });
  pyodide.setStdin({ stdin: nextStdinLine, autoEOF: true });

  const helpers = pyodide.globals.get("dict")();
  pyodide.runPython(TEST_HELPERS, { globals: helpers });
  quietInput = helpers.get("quiet_input");
  enterTestDir = helpers.get("enter_test_dir");
  leaveTestDir = helpers.get("leave_test_dir");

  // --- Ачаалсны ДАРАА сүлжээг хаана ---------------------------------------
  // Эндээс хойш ямар ч код гадагш хүсэлт илгээж чадахгүй. Стандарт сан нь
  // аль хэдийн санах ойд байгаа тул хичээлүүд хэвийн ажиллана.
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
      // Зарим орчинд устгах боломжгүй байж болно.
    }
  }
}

// --- Мессежийн урсгал ------------------------------------------------------
self.addEventListener("message", async function (event) {
  const data = event.data || {};

  if (data.type === "init") {
    try {
      await boot(data.indexURL);
      self.postMessage({ type: "ready" });
    } catch (error) {
      self.postMessage({
        type: "init-error",
        message: (error && error.message) || String(error),
      });
    }
    return;
  }

  if (data.type !== "run") return;

  entries = [];
  truncated = false;
  // Сүүлийн "\n" нь Enter — илүү хоосон мөр биш. Эс бөгөөс EOF хүртэл уншдаг
  // програм (for line in sys.stdin) жинхэнэ Python-оос нэг илүү мөр авна.
  const stdinText = data.stdin ? String(data.stdin) : "";
  stdinLines = stdinText ? stdinText.replace(/\n$/, "").split("\n") : [];
  stdinIndex = 0;

  let failure = null;
  let scope = null;
  let testDir = null;

  try {
    if (data.mode === "test") {
      testDir = enterTestDir();
      scope = pyodide.globals.get("dict")();
      scope.set("__name__", "__main__");
      scope.set("input", quietInput);
      await pyodide.runPythonAsync(data.code, { globals: scope });
    } else {
      await pyodide.runPythonAsync(data.code);
    }
  } catch (error) {
    const raw = (error && error.message) || String(error);
    const cleaned = cleanTraceback(raw);

    // Сүүлийн мөр нь ихэвчлэн "ExceptionName: тайлбар" хэлбэртэй.
    const last = cleaned.split("\n").filter(Boolean).pop() || "Error";
    const split = last.indexOf(": ");

    failure = {
      name: split > 0 ? last.slice(0, split) : "Error",
      message: split > 0 ? last.slice(split + 2) : last,
      traceback: cleaned,
    };
  } finally {
    flushOutput();
    if (scope) scope.destroy();
    if (testDir !== null) leaveTestDir(testDir);
  }

  self.postMessage({
    type: "result",
    id: data.id,
    entries: entries,
    truncated: truncated,
    error: failure,
  });
});
`;
