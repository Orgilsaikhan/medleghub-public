#!/usr/bin/env node
/**
 * React хичээлүүдийг бодит хөтөч дотор шалгана.
 *
 *   cd apps/api
 *   python -m app.content.exercises --react | node ../web/scripts/verify-react-exercises.mjs
 *   … | node ../web/scripts/verify-react-exercises.mjs --only react-counter,react-props
 *
 * `npm run verify:react` нь дээрхийг хийнэ. Runtime нь
 * `public/sandbox/react-runtime.js` — эхлээд `npm run sandbox:react`.
 *
 * Хичээл бүрт (Playwright Chromium, сайтын CSP-тэй ижил хуудсанд):
 *   1. эхлэл код «Хөтөч» дээр алдаагүй ажиллана;
 *   2. дасгалтай бол жишиг шийдэл БҮХ тестийг давна, «Хөтөч» дээр алдаагүй;
 *   3. эхлэл код бүх тестийг давах ЁСГҮЙ — эс бөгөөс сурагч юу ч бичилгүй
 *      «Ажиллуулах» дараад хичээлээ дуусгана.
 *
 * Хуудас нь сурагчийн хөтөчтэй ЯГ ИЖИЛ `runner.ts`-ийг ашиглана.
 */

import { readFile } from "node:fs/promises";
import http from "node:http";
import { fileURLToPath } from "node:url";

import { build } from "esbuild";
import { chromium } from "playwright";

const root = fileURLToPath(new URL("..", import.meta.url));
const only = process.argv.includes("--only")
  ? new Set(process.argv[process.argv.indexOf("--only") + 1].split(","))
  : null;

// Сайтын үйлдвэрлэлийн CSP-ийн iframe-д хамаатай хэсэг (`next.config.ts`).
const CSP = [
  "default-src 'self'",
  "base-uri 'self'",
  "form-action 'self'",
  "object-src 'none'",
  "script-src 'self' 'unsafe-inline' 'unsafe-eval' blob:",
  "style-src 'self' 'unsafe-inline'",
  "img-src 'self' data: blob: https:",
  "font-src 'self' data:",
  "worker-src 'self' blob:",
  "connect-src 'self' blob:",
].join("; ");

const input = await new Promise((resolve) => {
  let data = "";
  process.stdin.setEncoding("utf8");
  process.stdin.on("data", (chunk) => (data += chunk));
  process.stdin.on("end", () => resolve(data));
});
const lessons = JSON.parse(input).filter((lesson) => !only || only.has(lesson.slug));
if (lessons.length === 0) {
  console.error("Шалгах React хичээл алга.");
  process.exit(1);
}

const bundle = await build({
  stdin: {
    contents: `
      import { overlayFiles, parseLessonFiles } from "@/lib/sandbox/react/files";
      import { createJob, mountSandbox, runReactTests, SANDBOX_PERMISSIONS } from "@/lib/sandbox/react/runner";

      function preview(files) {
        return new Promise((resolve) => {
          const iframe = document.createElement("iframe");
          iframe.setAttribute("sandbox", SANDBOX_PERMISSIONS);
          iframe.style.cssText = "width:1024px;height:768px";
          document.body.appendChild(iframe);
          const errors = [];
          const logs = [];
          let settle = null;
          const done = () => { stop(); iframe.remove(); resolve({ errors, logs }); };
          const stop = mountSandbox(iframe, createJob(files, "preview"), (message) => {
            if (message.type === "error") errors.push(message.error);
            if (message.type === "console") logs.push(message);
            // fetch, timer зэрэг асинхрон алдааг ч барина.
            if (message.type === "ready" && !settle) settle = setTimeout(done, 900);
          });
          setTimeout(() => { if (!settle) { errors.push({ message: "ready мессеж ирсэнгүй (гацсан?)" }); done(); } }, 10000);
        });
      }

      window.verifyLesson = async (lesson) => {
        const starter = parseLessonFiles(lesson.starter);
        const report = { starterPreview: await preview(starter) };
        if (lesson.tests && lesson.tests.length) {
          const solved = overlayFiles(starter, parseLessonFiles(lesson.solution));
          report.solutionPreview = await preview(solved);
          report.solution = await runReactTests(solved, lesson.tests, () => {});
          report.starter = await runReactTests(starter, lesson.tests, () => {});
        }
        return report;
      };
    `,
    resolveDir: root,
    loader: "ts",
  },
  absWorkingDir: root,
  bundle: true,
  format: "iife",
  write: false,
  logLevel: "warning",
});
const verifyJs = bundle.outputFiles[0].text;
const runtimeJs = await readFile(`${root}public/sandbox/react-runtime.js`, "utf8").catch(() => {
  console.error("public/sandbox/react-runtime.js алга — эхлээд `npm run sandbox:react`.");
  process.exit(1);
});

const server = http.createServer((request, response) => {
  if (request.url === "/sandbox/react-runtime.js") {
    response.writeHead(200, { "Content-Type": "text/javascript; charset=utf-8" });
    response.end(runtimeJs);
  } else if (request.url === "/verify.js") {
    response.writeHead(200, { "Content-Type": "text/javascript; charset=utf-8" });
    response.end(verifyJs);
  } else {
    response.writeHead(200, {
      "Content-Type": "text/html; charset=utf-8",
      "Content-Security-Policy": CSP,
    });
    response.end('<!doctype html><meta charset="utf-8"><body><script src="/verify.js"></script>');
  }
});
await new Promise((resolve) => server.listen(0, "127.0.0.1", resolve));
const { port } = server.address();

const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto(`http://127.0.0.1:${port}/`);

let failures = 0;
const fail = (slug, text) => {
  failures += 1;
  console.log(`  ✗ ${slug}: ${text}`);
};

for (const lesson of lessons) {
  const report = await page.evaluate((item) => window.verifyLesson(item), lesson);
  const before = failures;

  for (const error of report.starterPreview.errors) {
    fail(
      lesson.slug,
      `эхлэл код алдаатай — ${error.file ?? ""}:${error.line ?? ""} ${error.message}`,
    );
  }
  if (report.solution) {
    for (const error of report.solutionPreview.errors) {
      fail(
        lesson.slug,
        `шийдэл «Хөтөч» дээр алдаатай — ${error.file ?? ""}:${error.line ?? ""} ${error.message}`,
      );
    }
    report.solution.forEach((result, index) => {
      if (!result.passed) {
        fail(lesson.slug, `шийдэл «${lesson.tests[index].name}» тестэд унав — ${result.message}`);
      }
    });
    if (report.starter.every((result) => result.passed)) {
      fail(lesson.slug, "эхлэл код бүх тестийг давчихлаа — сурагч юу ч бичихгүйгээр дуусгана");
    }
  }
  if (failures === before) {
    const tests = report.solution ? `, ${report.solution.length} тест` : "";
    console.log(`  ✓ ${lesson.slug}${tests}`);
  }
}

await browser.close();
server.close();
console.log(
  failures === 0
    ? `\nБүгд зөв — ${lessons.length} хичээл.`
    : `\n${failures} алдаа (${lessons.length} хичээл).`,
);
process.exit(failures === 0 ? 0 : 1);
