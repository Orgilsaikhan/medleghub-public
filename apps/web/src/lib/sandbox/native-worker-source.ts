/**
 * C/C++ програмын worker-ийн эх код (мөр хэлбэрээр).
 *
 * Сервер C/C++ кодыг WebAssembly болгож ХӨРВҮҮЛНЭ. Энэ worker нь тэр модулийг
 * сурагчийн хөтөч дотор АЖИЛЛУУЛНА — сервер кодыг хэзээ ч ажиллуулахгүй.
 * Worker-ийг ажиллуулалт бүрд шинээр үүсгэдэг тул төлөвийг цэвэрлэх
 * шаардлагагүй.
 *
 * WASI
 * ────
 * `-sSTANDALONE_WASM` модуль нь JavaScript «цавуу» кодгүй бөгөөд оронд нь
 * WASI (`wasi_snapshot_preview1`) импорт хүлээнэ. Хичээлүүдэд хэрэгтэй нь
 * цөөхөн: stdout/stderr бичих, stdin унших, цаг, санамсаргүй тоо, гарах.
 * Файлын систем, сүлжээ байхгүй — тэдгээрийг дуудвал `ENOSYS` буцна.
 *
 * АЮУЛГҮЙ БАЙДАЛ
 * ──────────────
 * WebAssembly модуль гадагш ЗӨВХӨН доорх импортоор л хандана — DOM, сүлжээ,
 * cookie руу хүрэх зам огт үгүй. Нэмэлт хамгаалалт болгож JavaScript
 * worker-тэй ижил API-уудыг устгана.
 *
 * СТАНДАРТ ОРОЛТ
 * ──────────────
 * Терминал шиг нэг удаад НЭГ мөр өгч, уншсан мөрийг гаралтад давтан
 * харуулна. Ингэснээр `scanf` бүр өөрийн мөрийг авч, хариулт нь асуултын
 * ард харагдана:
 *
 *     Нэрээ оруулна уу: Бат
 *
 * Дасгалын тест ажиллуулахад (`echoStdin: false`) оролтыг давтахгүй —
 * гаралт нь хүлээгдэж буй гаралттай яг харьцуулагдана.
 *
 * ГАРАЛТ
 * ──────
 * Гаралтыг ажиллаж байх зуур хэсэгчлэн илгээнэ. Хугацаа хэтэрч worker
 * зогсоогдсон ч түүнээс өмнөх гаралт харагдана.
 *
 * АНХААР: `String.raw` ашигласан тул дотор нь ` тэмдэг болон ${ дараалал
 * бичиж болохгүй — template literal тасарна.
 */

export const NATIVE_WORKER_SOURCE = String.raw`
// --- Нэмэлт хамгаалалт -------------------------------------------------------
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
    Object.defineProperty(self, name, { value: undefined, configurable: false, writable: false });
  } catch (_) {
    // Зарим орчинд устгах боломжгүй байж болно.
  }
}

// --- Хязгаар ------------------------------------------------------------------
const MAX_ENTRIES = 500;
const MAX_TEXT_LENGTH = 5000;

// Сервер хөрвүүлэгчийн анхааруулгыг модулийн энэ custom section-д хийдэг.
const WARNINGS_SECTION = "medleghub.warnings";

// --- WASI тогтмолууд ----------------------------------------------------------
const WASI_MODULE = "wasi_snapshot_preview1";
const ERRNO_SUCCESS = 0;
const ERRNO_BADF = 8;
const ERRNO_INVAL = 28;
const ERRNO_NOSYS = 52;
const ERRNO_SPIPE = 70;
const FILETYPE_CHARACTER_DEVICE = 2;
const CLOCK_REALTIME = 0;
const CLOCK_THREAD_CPUTIME = 3;
const EVENTTYPE_CLOCK = 0;
const SUBSCRIPTION_CLOCK_ABSTIME = 1;
const PROGRAM_NAME = "main";

// proc_exit болон гаралтын хязгаар нь WebAssembly-ийн стекийг эдгээр
// exception-оор таслан зогсооно.
class ProgramExit {
  constructor(code) {
    this.code = code;
  }
}

class OutputLimit {}

let memory = null;
let exited = false;
let exitCode = 0;

// Санах ой өсөхөд buffer солигддог тул дуудлага бүрд шинээр авна.
function bytes() {
  return new Uint8Array(memory.buffer);
}

function view() {
  return new DataView(memory.buffer);
}

// --- Гаралт -------------------------------------------------------------------
let pending = [];
let entryCount = 0;
let truncated = false;
let line = null;

function pushEntry(level, text) {
  if (entryCount >= MAX_ENTRIES) {
    truncated = true;
    throw new OutputLimit();
  }
  entryCount++;
  pending.push({ level: level, text: text });
}

function endLine(level) {
  const finished = line || { level: level, text: "" };
  line = null;
  pushEntry(finished.level, finished.text);
}

function appendText(level, text) {
  // stdout-ийн дуусаагүй мөрийн дундуур stderr бичвэл тусдаа мөр болгоно.
  if (line && line.level !== level) endLine(line.level);
  if (!line) line = { level: level, text: "" };
  line.text += text;

  // Шинэ мөргүй урт гаралтыг терминал шиг таслана.
  while (line.text.length > MAX_TEXT_LENGTH) {
    const rest = line.text.slice(MAX_TEXT_LENGTH);
    line.text = line.text.slice(0, MAX_TEXT_LENGTH);
    endLine(level);
    line = { level: level, text: rest };
  }
}

function emit(level, text) {
  let start = 0;
  for (;;) {
    const newline = text.indexOf("\n", start);
    const piece = newline === -1 ? text.slice(start) : text.slice(start, newline);
    if (piece) appendText(level, piece);
    if (newline === -1) return;
    endLine(level);
    start = newline + 1;
  }
}

// Мөр дуусмагц илгээнэ — програм дараа нь гацаж worker зогсоогдсон ч
// өмнөх гаралт харагдана. Мөрийн тоо хязгаартай тул мессеж ч цөөн.
function flush() {
  if (!pending.length) return;
  self.postMessage({ type: "output", entries: pending });
  pending = [];
}

// Олон байтын UTF-8 үсэг хоёр fd_write-д хуваагдаж болно — stream горим.
const outputDecoders = { 1: new TextDecoder("utf-8"), 2: new TextDecoder("utf-8") };

// --- Стандарт оролт -----------------------------------------------------------
let stdin = new Uint8Array(0);
let stdinOffset = 0;
let stdinEofReported = false;
// Тест ажиллуулахад ИДЭВХГҮЙ — гаралтыг хүлээгдэж буй гаралттай харьцуулдаг
// тул оролт түүнд холилдох ёсгүй.
let echoStdin = true;
const echoDecoder = new TextDecoder("utf-8");

function setStdin(text) {
  let value = text ? String(text) : "";
  // Сүүлийн мөрийн араас Enter дарсантай адил.
  if (value && value.charAt(value.length - 1) !== "\n") value += "\n";
  stdin = new TextEncoder().encode(value);
}

// --- WASI функцууд ------------------------------------------------------------
function checkRunning() {
  // Сурагчийн catch (...) нь гарах exception-ийг залгисан ч дахин шиднэ.
  if (exited) throw new ProgramExit(exitCode);
}

function forEachIovec(iovs, iovsLen, callback) {
  for (let i = 0; i < iovsLen; i++) {
    const base = iovs + i * 8;
    const dv = view();
    callback(dv.getUint32(base, true), dv.getUint32(base + 4, true));
  }
}

function nowNanoseconds(clockId) {
  if (clockId === CLOCK_REALTIME) {
    return BigInt(Math.round((performance.timeOrigin + performance.now()) * 1000)) * 1000n;
  }
  return BigInt(Math.round(performance.now() * 1000)) * 1000n;
}

const wasi = {
  fd_write: function (fd, iovs, iovsLen, nwrittenPtr) {
    checkRunning();
    if (fd !== 1 && fd !== 2) return ERRNO_BADF;

    const level = fd === 2 ? "error" : "log";
    const decoder = outputDecoders[fd];
    let written = 0;

    forEachIovec(iovs, iovsLen, function (ptr, len) {
      if (!len) return;
      emit(level, decoder.decode(bytes().subarray(ptr, ptr + len), { stream: true }));
      written += len;
    });

    view().setUint32(nwrittenPtr, written, true);
    flush();
    return ERRNO_SUCCESS;
  },

  fd_read: function (fd, iovs, iovsLen, nreadPtr) {
    checkRunning();
    if (fd !== 0) return ERRNO_BADF;

    // Терминал шиг нэг удаад нэг л мөр.
    const newline = stdin.indexOf(10, stdinOffset);
    const lineEnd = newline === -1 ? stdin.length : newline + 1;
    let read = 0;

    forEachIovec(iovs, iovsLen, function (ptr, len) {
      const count = Math.min(len, lineEnd - stdinOffset);
      if (count <= 0) return;
      const chunk = stdin.subarray(stdinOffset, stdinOffset + count);
      bytes().set(chunk, ptr);
      stdinOffset += count;
      read += count;
      // Терминал шиг уншсан мөрийг харуулна.
      if (echoStdin) emit("log", echoDecoder.decode(chunk, { stream: true }));
    });

    view().setUint32(nreadPtr, read, true);

    if (read === 0 && !stdinEofReported) {
      stdinEofReported = true;
      self.postMessage({ type: "stdin-eof" });
    }

    flush();
    return ERRNO_SUCCESS;
  },

  fd_seek: function (fd) {
    checkRunning();
    return fd <= 2 ? ERRNO_SPIPE : ERRNO_BADF;
  },

  fd_close: function (fd) {
    checkRunning();
    return fd <= 2 ? ERRNO_SUCCESS : ERRNO_BADF;
  },

  fd_fdstat_get: function (fd, statPtr) {
    checkRunning();
    if (fd > 2) return ERRNO_BADF;
    const dv = view();
    dv.setUint8(statPtr, FILETYPE_CHARACTER_DEVICE);
    dv.setUint16(statPtr + 2, 0, true);
    dv.setBigUint64(statPtr + 8, 0n, true);
    dv.setBigUint64(statPtr + 16, 0n, true);
    return ERRNO_SUCCESS;
  },

  // Урьдчилан нээсэн хавтас байхгүй — файлын систем огт үгүй.
  fd_prestat_get: function () {
    return ERRNO_BADF;
  },

  fd_prestat_dir_name: function () {
    return ERRNO_BADF;
  },

  environ_sizes_get: function (countPtr, sizePtr) {
    checkRunning();
    const dv = view();
    dv.setUint32(countPtr, 0, true);
    dv.setUint32(sizePtr, 0, true);
    return ERRNO_SUCCESS;
  },

  environ_get: function () {
    checkRunning();
    return ERRNO_SUCCESS;
  },

  args_sizes_get: function (argcPtr, bufferSizePtr) {
    checkRunning();
    const dv = view();
    dv.setUint32(argcPtr, 1, true);
    dv.setUint32(bufferSizePtr, PROGRAM_NAME.length + 1, true);
    return ERRNO_SUCCESS;
  },

  args_get: function (argvPtr, bufferPtr) {
    checkRunning();
    view().setUint32(argvPtr, bufferPtr, true);
    bytes().set(new TextEncoder().encode(PROGRAM_NAME + "\0"), bufferPtr);
    return ERRNO_SUCCESS;
  },

  clock_time_get: function (clockId, precision, timePtr) {
    checkRunning();
    if (clockId < CLOCK_REALTIME || clockId > CLOCK_THREAD_CPUTIME) return ERRNO_INVAL;
    view().setBigUint64(timePtr, nowNanoseconds(clockId), true);
    return ERRNO_SUCCESS;
  },

  clock_res_get: function (clockId, resolutionPtr) {
    checkRunning();
    if (clockId < CLOCK_REALTIME || clockId > CLOCK_THREAD_CPUTIME) return ERRNO_INVAL;
    view().setBigUint64(resolutionPtr, 1000n, true);
    return ERRNO_SUCCESS;
  },

  random_get: function (bufferPtr, length) {
    checkRunning();
    const target = bytes();
    // getRandomValues нь нэг удаад 65536 байтаас ихийг бөглөхгүй.
    for (let offset = 0; offset < length; offset += 65536) {
      const end = Math.min(length, offset + 65536);
      crypto.getRandomValues(target.subarray(bufferPtr + offset, bufferPtr + end));
    }
    return ERRNO_SUCCESS;
  },

  // sleep() — worker-ийн thread-ийг л хүлээлгэнэ. Нийт хугацааг гол thread
  // хязгаарладаг тул мөнхөд хүлээхгүй.
  poll_oneoff: function (inPtr, outPtr, subscriptions, neventsPtr) {
    checkRunning();
    const dv = view();
    let waitUntil = performance.now();

    for (let i = 0; i < subscriptions; i++) {
      const sub = inPtr + i * 48;
      if (dv.getUint8(sub + 8) !== EVENTTYPE_CLOCK) continue;
      const clockId = dv.getUint32(sub + 16, true);
      const timeout = dv.getBigUint64(sub + 24, true);
      const flags = dv.getUint16(sub + 40, true);
      const relative =
        flags & SUBSCRIPTION_CLOCK_ABSTIME ? timeout - nowNanoseconds(clockId) : timeout;
      const deadline = performance.now() + Math.max(0, Number(relative) / 1e6);
      waitUntil = Math.max(waitUntil, deadline);
    }

    while (performance.now() < waitUntil) {
      // Идэвхтэй хүлээлт — SharedArrayBuffer-гүй орчинд унтах өөр арга байхгүй.
    }

    for (let i = 0; i < subscriptions; i++) {
      const sub = inPtr + i * 48;
      const event = outPtr + i * 32;
      dv.setBigUint64(event, dv.getBigUint64(sub, true), true);
      dv.setUint16(event + 8, ERRNO_SUCCESS, true);
      dv.setUint8(event + 10, dv.getUint8(sub + 8));
    }
    dv.setUint32(neventsPtr, subscriptions, true);
    return ERRNO_SUCCESS;
  },

  sched_yield: function () {
    checkRunning();
    return ERRNO_SUCCESS;
  },

  proc_exit: function (code) {
    exited = true;
    exitCode = code;
    throw new ProgramExit(code);
  },
};

// WASI-аас гадуурх цорын ганц Emscripten импорт: санах ой өсөхөд мэдэгдэнэ.
// Buffer-ийг дуудлага бүрд шинээр авдаг тул хийх зүйлгүй.
const emscripten = {
  emscripten_notify_memory_growth: function () {},
};

function buildImports(module) {
  const imports = {};
  for (const descriptor of WebAssembly.Module.imports(module)) {
    if (descriptor.kind !== "function") continue;
    const namespace = imports[descriptor.module] || (imports[descriptor.module] = {});

    if (descriptor.module === WASI_MODULE) {
      namespace[descriptor.name] =
        wasi[descriptor.name] ||
        function () {
          return ERRNO_NOSYS;
        };
    } else if (descriptor.module === "env" && emscripten[descriptor.name]) {
      namespace[descriptor.name] = emscripten[descriptor.name];
    } else {
      namespace[descriptor.name] = function () {
        throw new Error("Дэмжигдээгүй функц: " + descriptor.module + "." + descriptor.name);
      };
    }
  }
  return imports;
}

function readWarnings(module) {
  try {
    const sections = WebAssembly.Module.customSections(module, WARNINGS_SECTION);
    return sections.length ? new TextDecoder("utf-8").decode(sections[0]) : "";
  } catch (_) {
    return "";
  }
}

// --- Алдааг сурагчид ойлгомжтой болгох ----------------------------------------
// Хөтөч бүр өөр үгээр бичдэг (Chrome, Firefox, Safari) тул уян хэвээр таньна.
const TRAP_HINTS = [
  [/divide by zero|division by zero/i, "Бүхэл тоог тэгд хуваалаа."],
  [/unrepresentable|integer overflow/i, "Бүхэл тооны хуваалтын үр дүн төрөлдөө багтсангүй."],
  [/signature mismatch|null function|table index/i, "Буруу функцийн заагчаар дуудлаа."],
  [/call stack|too much recursion/i, "Дуудлагын стек дүүрлээ. Рекурс төгсгөлгүй үргэлжилсэн байж магадгүй."],
  [
    /out of bounds|index out of range/i,
    "Санах ойн хязгаараас гадуур хандлаа. Массивын индекс, заагч эсвэл хэт гүн рекурсыг шалгана уу.",
  ],
  [
    /unreachable/i,
    "Програм гэнэт зогслоо (abort). Барьж аваагүй exception эсвэл assert байж магадгүй.",
  ],
];

function describe(thrown) {
  // main-аас гарсан C++ exception-ийг сервер барьж, g++ шиг мессеж хэвлээд
  // abort болгодог. Энд хүрсэн бол main эхлэхээс өмнө шидэгдсэн.
  if (typeof WebAssembly.Exception === "function" && thrown instanceof WebAssembly.Exception) {
    return {
      name: "Ажиллах үеийн алдаа",
      message: "Барьж аваагүй exception шидэгдлээ. try/catch-аар барина уу.",
    };
  }

  const message = (thrown && thrown.message) || String(thrown);
  for (const [pattern, hint] of TRAP_HINTS) {
    if (pattern.test(message)) {
      return { name: "Ажиллах үеийн алдаа", message: hint + " (" + message + ")" };
    }
  }
  return { name: (thrown && thrown.name) || "Error", message: message };
}

// --- Мессежийн урсгал ---------------------------------------------------------
self.addEventListener("message", async function (event) {
  const data = event.data || {};
  let error = null;

  try {
    const module = await WebAssembly.compile(data.wasm);

    const warnings = readWarnings(module);
    if (warnings) self.postMessage({ type: "warnings", text: warnings });

    setStdin(data.stdin);
    echoStdin = data.echoStdin !== false;
    const instance = await WebAssembly.instantiate(module, buildImports(module));
    memory = instance.exports.memory;

    if (typeof instance.exports._start !== "function") {
      throw new Error("Програмын эхлэх цэг (main) олдсонгүй.");
    }
    instance.exports._start();
  } catch (thrown) {
    if (thrown instanceof OutputLimit) {
      truncated = true;
    } else if (!(thrown instanceof ProgramExit)) {
      error = describe(thrown);
    }
  }

  try {
    if (line) endLine(line.level);
  } catch (_) {
    // Хязгаарт хүрсэн — сүүлийн дуусаагүй мөрийг орхино.
  }
  flush();

  self.postMessage({ type: "done", truncated: truncated, error: error, exitCode: exitCode });
});
`;
