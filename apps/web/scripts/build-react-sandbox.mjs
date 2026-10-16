#!/usr/bin/env node
/**
 * React sandbox-ийн runtime-ийг нэг файл болгоно:
 *
 *   src/lib/sandbox/react-runtime/index.ts  →  public/sandbox/react-runtime.js
 *
 * `predev`, `prebuild` үед автоматаар ажиллана (Monaco, Pyodide-ийн
 * хуулагчтай адил). Гаралт нь `.gitignore`-д — commit хийгдэхгүй.
 *
 * React-ийн DEVELOPMENT хувилбарыг зориуд ашиглана: `key`-гүй жагсаалт,
 * hook-ийн буруу хэрэглээ гэх мэт анхааруулга сурагчид харагдана. Мөн
 * тестүүдийн `act()` зөвхөн development хувилбарт ажилладаг.
 */

import { mkdir, stat } from "node:fs/promises";
import { fileURLToPath } from "node:url";

import { build } from "esbuild";

const root = fileURLToPath(new URL("..", import.meta.url));
const outfile = `${root}public/sandbox/react-runtime.js`;

await mkdir(`${root}public/sandbox`, { recursive: true });

await build({
  absWorkingDir: root,
  entryPoints: ["src/lib/sandbox/react-runtime/index.ts"],
  outfile,
  bundle: true,
  format: "iife",
  platform: "browser",
  target: "es2022",
  minify: true,
  legalComments: "none",
  charset: "utf8",
  define: { "process.env.NODE_ENV": '"development"' },
  logLevel: "warning",
});

const { size } = await stat(outfile);
console.log(`react-sandbox: public/sandbox/react-runtime.js (${Math.round(size / 1024)} KB)`);
