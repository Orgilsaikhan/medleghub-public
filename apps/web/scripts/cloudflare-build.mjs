/**
 * Cloudflare Workers-д зориулсан build (`opennextjs-cloudflare build`).
 *
 * Next.js нь `NEXT_PUBLIC_*`, CSP болон `/api/v1` rewrite-ийн зорилтыг BUILD-ийн
 * үед шингээдэг. Хөгжүүлэгчийн `.env.production` (gitignore-д) хуучин эсвэл
 * түр хаяг агуулж болох тул production-ийн утгуудыг энд тогтооно. Shell-ээс
 * өгсөн утга давуу:
 *
 *   API_PROXY_TARGET=https://… npm run cf:build
 *
 * Next.js нь аль хэдийн тохируулагдсан хувьсагчийг `.env*` файлаар дарж
 * бичдэггүй — тиймээс эдгээр нь `.env.production`-оос давуу.
 */

import { spawnSync } from "node:child_process";

const PRODUCTION = {
  // Хөтөч API-г энэ сайтаар дамжуулж дуудна — cookie first-party хэвээр.
  NEXT_PUBLIC_API_URL: "/api/v1",
  NEXT_PUBLIC_SITE_URL: "https://medleghub.com",
  // `/api/v1/*` rewrite-ийн зорилт — Oracle VM дээрх API (Caddy).
  API_PROXY_TARGET: "https://api.medleghub.com",
};

const env = { ...process.env };
for (const [key, value] of Object.entries(PRODUCTION)) {
  env[key] ||= value;
}

for (const key of Object.keys(PRODUCTION)) {
  console.log(`cloudflare-build: ${key}=${env[key]}`);
}

const result = spawnSync("npx", ["opennextjs-cloudflare", "build"], {
  stdio: "inherit",
  env,
  // Windows дээр `npx` нь .cmd файл.
  shell: process.platform === "win32",
});
process.exit(result.status ?? 1);
