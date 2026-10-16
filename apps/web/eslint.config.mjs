import { defineConfig, globalIgnores } from "eslint/config";
import nextVitals from "eslint-config-next/core-web-vitals";
import nextTs from "eslint-config-next/typescript";

const eslintConfig = defineConfig([
  ...nextVitals,
  ...nextTs,
  // Override default ignores of eslint-config-next.
  globalIgnores([
    // Default ignores of eslint-config-next:
    ".next/**",
    "out/**",
    "build/**",
    "next-env.d.ts",
    // Гуравдагч этгээдийн бэлэн бүтээгдсэн файлууд. Эдгээрийг `scripts/`
    // доторх хуулагчид `node_modules`-оос авчирдаг бөгөөд бид засдаггүй.
    // Шалгавал өөрсдийн кодын алдааг дарж, хуурамч уналт үүсгэнэ.
    "public/monaco/**",
    "public/pyodide/**",
    // `scripts/build-react-sandbox.mjs`-ийн гаралт — React-ийг багтаасан bundle.
    "public/sandbox/**",
    // Cloudflare-ийн build гаралт (`npm run cf:build`) — олон MB bundle.
    ".open-next/**",
    ".wrangler/**",
  ]),
]);

export default eslintConfig;
