/**
 * Pyodide-ийн ажиллахад шаардлагатай файлуудыг `public/pyodide` рүү хуулна.
 *
 * Яагаад өөрсдөө хостлох вэ (Monaco-тэй ижил шалтгаан):
 *   • Гуравдагч этгээдийн CDN рүү сурагчийн хүсэлт явахгүй (нууцлал),
 *   • CDN унасан ч хичээл ажиллана,
 *   • Хувилбар нь package-lock-оор тогтмол байна,
 *   • CSP-д гадаад домэйн нэмэх шаардлагагүй — бүгд `'self'`.
 *
 * Зөвхөн ажиллахад хэрэгтэй файлыг хуулна. Багцад багтдаг `.map`, `.d.ts`,
 * жишээ `.html`, UMD хувилбар зэрэг нь production-д хэрэггүй.
 */

import { copyFile, mkdir, stat } from "node:fs/promises";
import path from "node:path";

/**
 * Ажиллахад хангалттай хамгийн бага багц.
 *
 * `pyodide.mjs` нь ачаалагч, `pyodide.asm.mjs`/`.wasm` нь CPython орчуулагч,
 * `python_stdlib.zip` нь стандарт сан (math, json, dataclasses, …),
 * `pyodide-lock.json` нь багцын бүртгэл.
 */
const FILES = [
  "pyodide.mjs",
  "pyodide.asm.mjs",
  "pyodide.asm.wasm",
  "python_stdlib.zip",
  "pyodide-lock.json",
];

const source = path.join(process.cwd(), "node_modules", "pyodide");
const target = path.join(process.cwd(), "public", "pyodide");

const marker = path.join(target, "pyodide.asm.wasm");
const present = await stat(marker).then(
  () => true,
  () => false,
);

// Аль хэдийн хуулсан бол алгасна — dev server дахин эхлэх бүрт 13 MB хуулахгүй.
if (present && !process.argv.includes("--force")) {
  console.log("pyodide: already present, skipping");
} else {
  await mkdir(target, { recursive: true });

  let total = 0;
  for (const name of FILES) {
    const from = path.join(source, name);
    const info = await stat(from).catch(() => null);
    if (!info) {
      throw new Error(
        `pyodide: ${name} олдсонгүй. \`npm install\` ажиллуулсан эсэхээ шалгана уу.`,
      );
    }
    await copyFile(from, path.join(target, name));
    total += info.size;
  }

  const mb = (total / 1024 / 1024).toFixed(1);
  console.log(`pyodide: copied ${FILES.length} file(s), ${mb} MB -> ${target}`);
}
