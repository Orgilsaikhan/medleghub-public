#!/usr/bin/env node
/**
 * C/C++, Python ба JavaScript дасгалын тестүүд зөв эсэхийг шалгана.
 *
 *   cd apps/api
 *   python -m app.content.exercises | node ../web/scripts/verify-exercises.mjs
 *   python -m app.content.exercises | node ../web/scripts/verify-exercises.mjs --only c-for-davtalt,c-massiv
 *
 * C/C++-д хөрвүүлэгч ажиллаж байх ёстой (`docker compose up -d compiler`).
 * Хаягийг `COMPILER_URL`-аар өөрчилнө (анхдагч http://127.0.0.1:8090).
 * Python нь `node_modules/pyodide`-оор Node дотор ажиллана — сервер хэрэггүй.
 * JavaScript нь хөтөчийн worker-ийн (`worker-source.ts`) кодоор, `prompt()`-оор
 * оролтоо уншина.
 *
 * Дасгал бүрт:
 *   1. жишиг шийдэл хөрвүүлэгдэж БҮХ тестийг давна;
 *   2. эхлэл код хөрвүүлэгдэнэ, гэхдээ бүх тестийг давах ЁСГҮЙ — эс бөгөөс
 *      сурагч юу ч бичилгүй «Илгээх» дараад хичээлээ дуусгана.
 *
 * Програмыг хөтөчтэй ЯГ ИЖИЛ worker (`native-worker-source.ts`,
 * `python-worker-source.ts` — тестийн горимоор) дээр ажиллуулж, ИЖИЛ
 * шалгагчаар (`grader.ts`) дүгнэнэ. Тэдгээрийг TypeScript
 * хэвээр нь `typescript` багцаар хөрвүүлж ачаална.
 */

import { readFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import { Worker } from "node:worker_threads";

import ts from "typescript";

const COMPILER_URL = (process.env.COMPILER_URL ?? "http://127.0.0.1:8090").replace(/\/$/, "");
const TIMEOUT_MS = 3000;
const CONCURRENCY = 2;

const src = new URL("../src/lib/sandbox/", import.meta.url);

async function importTs(name) {
  const source = await readFile(new URL(name, src), "utf8");
  const { outputText } = ts.transpileModule(source, {
    compilerOptions: { module: ts.ModuleKind.ESNext, target: ts.ScriptTarget.ES2022 },
  });
  return import(`data:text/javascript;base64,${Buffer.from(outputText).toString("base64")}`);
}

const { NATIVE_WORKER_SOURCE } = await importTs("native-worker-source.ts");
const { PYTHON_WORKER_SOURCE } = await importTs("python-worker-source.ts");
const { WORKER_SOURCE: JS_WORKER_SOURCE } = await importTs("worker-source.ts");
// Node-д Pyodide нь `file://` URL биш файлын зам хүлээнэ.
const PYODIDE_URL = fileURLToPath(new URL("../node_modules/pyodide/", import.meta.url));
const { gradeRun, firstDifference } = await importTs("grader.ts");

// Хөтөчийн `self`-ийг дуурайна. Бусад глобал (WebAssembly, crypto,
// performance, TextDecoder) Node-д бий.
const BOOTSTRAP = `
const { parentPort, workerData } = require("node:worker_threads");
const listeners = [];
const self = {
  postMessage: (message) => parentPort.postMessage(message),
  addEventListener: (_type, listener) => listeners.push(listener),
};
new Function("self", workerData.source)(self);
parentPort.on("message", (data) => listeners.forEach((listener) => listener({ data })));
`;

// JavaScript-ийн worker нь `self.console`-ийг сольж, сурагчийн код глобал
// `console`, `prompt`-ийг дууддаг — хөтөчид `self` нь глобал объект өөрөө.
const JS_BOOTSTRAP = `
const { parentPort, workerData } = require("node:worker_threads");
const listeners = {};
globalThis.self = globalThis;
globalThis.postMessage = (message) => parentPort.postMessage(message);
globalThis.addEventListener = (type, listener) => (listeners[type] ??= []).push(listener);
process.on("unhandledRejection", (reason) =>
  (listeners.unhandledrejection ?? []).forEach((listener) => listener({ reason })),
);
new Function(workerData.source)();
parentPort.on("message", (data) =>
  (listeners.message ?? []).forEach((listener) => listener({ data })),
);
`;

const AsyncFunction = Object.getPrototypeOf(async function () {}).constructor;

/** `runner.ts`-ийн `runJavaScript`-тэй ижил: ажиллуулалт бүр шинэ worker-т. */
function runJavaScriptTest(code, stdin) {
  const startedAt = performance.now();
  return new Promise((resolve) => {
    const worker = new Worker(JS_BOOTSTRAP, {
      eval: true,
      workerData: { source: JS_WORKER_SOURCE },
    });
    let settled = false;
    const finish = (outcome) => {
      if (settled) return;
      settled = true;
      clearTimeout(timer);
      void worker.terminate();
      resolve({ ...outcome, durationMs: Math.round(performance.now() - startedAt) });
    };
    const timer = setTimeout(
      () => finish({ entries: [], truncated: false, error: null, timedOut: true }),
      TIMEOUT_MS,
    );
    worker.on("message", (data) => {
      if (data.type === "result") {
        finish({
          entries: data.entries,
          truncated: data.truncated,
          error: data.error,
          timedOut: false,
        });
      }
    });
    worker.on("error", (error) =>
      finish({
        entries: [],
        truncated: false,
        error: { name: "Error", message: String(error) },
        timedOut: false,
      }),
    );
    worker.postMessage({ code, stdin });
  });
}

/** `native-runner.ts`-ийн `execute`-тэй ижил үр дүн буцаана. */
function execute(wasm, stdin) {
  const startedAt = performance.now();
  return new Promise((resolve) => {
    const worker = new Worker(BOOTSTRAP, {
      eval: true,
      workerData: { source: NATIVE_WORKER_SOURCE },
    });
    const entries = [];
    let settled = false;

    const finish = (outcome) => {
      if (settled) return;
      settled = true;
      clearTimeout(timer);
      void worker.terminate();
      resolve({ entries, ...outcome, durationMs: Math.round(performance.now() - startedAt) });
    };

    const timer = setTimeout(
      () => finish({ truncated: false, error: null, timedOut: true }),
      TIMEOUT_MS,
    );

    worker.on("message", (data) => {
      if (data.type === "output") entries.push(...data.entries);
      if (data.type === "done") {
        finish({
          truncated: data.truncated,
          error: data.error,
          timedOut: false,
          exitCode: data.exitCode,
        });
      }
    });
    worker.on("error", (error) =>
      finish({
        truncated: false,
        error: { name: "Error", message: String(error) },
        timedOut: false,
      }),
    );

    const copy = wasm.slice(0);
    worker.postMessage({ wasm: copy, stdin, echoStdin: false }, [copy]);
  });
}

// --- Python ---------------------------------------------------------------------
// Хөтөчийн `python-runner.ts` шиг НЭГ worker-ыг хадгалж, ажиллуулалтыг
// дараалуулна. Хугацаа хэтэрвэл устгаж, дараагийнх нь шинээр ачаална.
let pyWorker = null;
let pyReady = null;
let pyQueue = Promise.resolve();
let pyNextId = 1;

function startPython() {
  if (pyReady) return pyReady;
  const worker = new Worker(BOOTSTRAP, {
    eval: true,
    workerData: { source: PYTHON_WORKER_SOURCE },
  });
  pyWorker = worker;
  pyReady = new Promise((resolve, reject) => {
    const onMessage = (data) => {
      if (data.type === "ready") {
        worker.off("message", onMessage);
        resolve();
      } else if (data.type === "init-error") {
        reject(new Error(`Pyodide ачаалж чадсангүй: ${data.message}`));
      }
    };
    worker.on("message", onMessage);
    worker.on("error", reject);
    worker.postMessage({ type: "init", indexURL: PYODIDE_URL });
  });
  return pyReady;
}

function stopPython() {
  void pyWorker?.terminate();
  pyWorker = null;
  pyReady = null;
}

function runPythonTest(code, stdin) {
  const job = pyQueue.then(async () => {
    await startPython();
    const worker = pyWorker;
    const id = pyNextId++;
    const startedAt = performance.now();
    return new Promise((resolve) => {
      const done = (outcome) => {
        clearTimeout(timer);
        worker.off("message", onMessage);
        resolve({ ...outcome, durationMs: Math.round(performance.now() - startedAt) });
      };
      const onMessage = (data) => {
        if (data.type === "result" && data.id === id) {
          done({
            entries: data.entries,
            truncated: data.truncated,
            error: data.error,
            timedOut: false,
          });
        }
      };
      const timer = setTimeout(() => {
        stopPython();
        done({ entries: [], truncated: false, error: null, timedOut: true });
      }, TIMEOUT_MS);
      worker.on("message", onMessage);
      worker.postMessage({ type: "run", id, code, stdin, mode: "test" });
    });
  });
  pyQueue = job.catch(() => {});
  return job;
}

const PYTHON_SYNTAX = /^(SyntaxError|IndentationError|TabError)$/;

// --- C/C++ ----------------------------------------------------------------------

async function compile(language, source) {
  let response;
  // Хөрвүүлэгч завгүй (503) бол түр хүлээгээд дахин оролдоно.
  for (let attempt = 0; attempt < 5; attempt++) {
    response = await fetch(`${COMPILER_URL}/compile`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ language, source }),
    });
    if (response.status !== 503) break;
    await new Promise((resolve) => setTimeout(resolve, 2000 * (attempt + 1)));
  }
  if (response.ok) return { wasm: await response.arrayBuffer() };
  const body = await response.json().catch(() => ({}));
  if (response.status === 422 && body.code === "COMPILE_ERROR") {
    return { diagnostics: String(body.diagnostics ?? "") };
  }
  throw new Error(`Хөрвүүлэгч ${response.status} буцаалаа: ${JSON.stringify(body)}`);
}

const indent = (text) => text.replace(/^/gm, "      ");

function describeFailure(test, index, result) {
  const lines = [`    тест ${index + 1}${test.sample ? " (жишээ)" : ""}: ${result.status}`];
  if (result.message) lines.push(`      ${result.message}`);
  if (result.status === "wrong-answer") {
    const diff = firstDifference(result.actual, test.expected_output);
    if (diff) {
      lines.push(
        `      ${diff.line}-р мөр: хүлээгдэж буй ${JSON.stringify(diff.expected)}, гарсан ${JSON.stringify(diff.actual)}`,
      );
    }
  }
  lines.push("      оролт:", indent(test.stdin || "(хоосон)"));
  return lines.join("\n");
}

async function runAll(language, source, tests) {
  if (language === "javascript") {
    // Синтакс алдаа — код огт ажиллахгүй. Worker-тэй ижлээр async функц болгож
    // зөвхөн parse хийнэ: `JSON.parse`-ийн ажиллах үеийн SyntaxError энд биш,
    // тестийн «runtime-error» болж тооцогдоно.
    try {
      new AsyncFunction('"use strict";\n' + source);
    } catch (error) {
      return { diagnostics: `${error.name}: ${error.message}` };
    }
    const results = [];
    for (const test of tests) {
      results.push(gradeRun(await runJavaScriptTest(source, test.stdin), test.expected_output));
    }
    return { results };
  }
  if (language === "python") {
    const results = [];
    for (const test of tests) {
      const run = await runPythonTest(source, test.stdin);
      // Синтакс алдаа нь C-ийн хөрвүүлэлтийн алдаатай адил — тест бүр унана.
      if (run.error && PYTHON_SYNTAX.test(run.error.name)) {
        return { diagnostics: run.error.traceback ?? run.error.message };
      }
      results.push(gradeRun(run, test.expected_output));
    }
    return { results };
  }

  const compiled = await compile(language, source);
  if (compiled.diagnostics !== undefined) return { diagnostics: compiled.diagnostics };
  const results = [];
  for (const test of tests) {
    results.push(gradeRun(await execute(compiled.wasm, test.stdin), test.expected_output));
  }
  return { results };
}

async function verify(exercise) {
  const problems = [];
  const { language, tests } = exercise;

  const solution = await runAll(language, exercise.solution, tests);
  if (solution.diagnostics !== undefined) {
    problems.push(
      `  жишиг шийдэл хөрвүүлэгдсэнгүй / синтакс алдаатай:\n${indent(solution.diagnostics)}`,
    );
  } else {
    solution.results.forEach((result, index) => {
      if (result.status !== "passed") {
        problems.push(`  жишиг шийдэл унав:\n${describeFailure(tests[index], index, result)}`);
      }
    });
  }

  const starter = await runAll(language, exercise.starter, tests);
  let starterPassed = 0;
  if (starter.diagnostics !== undefined) {
    problems.push(
      `  эхлэл код хөрвүүлэгдсэнгүй / синтакс алдаатай:\n${indent(starter.diagnostics)}`,
    );
  } else {
    starterPassed = starter.results.filter((result) => result.status === "passed").length;
    if (starterPassed === tests.length) {
      problems.push("  эхлэл код бүх тестийг давлаа — сурагч юу ч бичилгүй дуусгана");
    }
  }

  return { problems, starterPassed };
}

const raw = await new Promise((resolve, reject) => {
  let data = "";
  process.stdin.setEncoding("utf8");
  process.stdin.on("data", (chunk) => (data += chunk));
  process.stdin.on("end", () => resolve(data));
  process.stdin.on("error", reject);
});

const onlyArg = process.argv.indexOf("--only");
const only = onlyArg === -1 ? null : new Set(process.argv[onlyArg + 1].split(","));
const exercises = JSON.parse(raw).filter(
  (exercise) =>
    ["c", "cpp", "python", "javascript"].includes(exercise.language) &&
    (!only || only.has(exercise.slug)),
);

if (exercises.length === 0) {
  console.error("Шалгах дасгал олдсонгүй.");
  process.exit(1);
}

let failed = 0;
const queue = [...exercises];
const outputs = new Map();

await Promise.all(
  Array.from({ length: CONCURRENCY }, async () => {
    for (let exercise = queue.shift(); exercise; exercise = queue.shift()) {
      let report;
      try {
        report = await verify(exercise);
      } catch (error) {
        report = { problems: [`  ${error.message}`], starterPassed: 0 };
      }
      outputs.set(exercise.slug, report);
    }
  }),
);

for (const exercise of exercises) {
  const { problems, starterPassed } = outputs.get(exercise.slug);
  const total = exercise.tests.length;
  if (problems.length === 0) {
    console.log(`✓ ${exercise.slug} — ${total} тест (эхлэл код ${starterPassed}/${total})`);
  } else {
    failed++;
    console.log(`✗ ${exercise.slug}\n${problems.join("\n")}`);
  }
}

console.log(`\n${exercises.length - failed}/${exercises.length} дасгал зөв.`);
process.exit(failed ? 1 : 0);
