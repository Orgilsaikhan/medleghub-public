/**
 * `public/badges/` доторх файлуудыг уншиж, тэмдгийн дүрсний бүртгэлийг үүсгэнэ.
 *
 * Файлын нэр нь тэмдгийн түлхүүртэй таарах ёстой. Зураас, доогуур зураас,
 * том жижиг үсгийг үл тооно:
 *   public/badges/first-commit.svg  →  «First Commit»
 *   public/badges/nightowl.png      →  «Night Owl»
 *   public/badges/Ahead_Of_Time.png →  «Ahead of Time»
 *
 * Ингэснээр дүрс нэмэхэд код засах шаардлагагүй — файлаа хийгээд дахин
 * build хийхэд (эсвэл `npm run dev`-ийг дахин эхлүүлэхэд) хангалттай. Файлгүй
 * тэмдэг хоосон хэлбэрээрээ харагдана.
 *
 * `scripts/generate-logo-manifest.mjs`-тэй ижил шалтгаанаар бүртгэл үүсгэдэг:
 * browser нь файлын системийг уншиж чадахгүй, байхгүй файл руу хандвал
 * эвдэрсэн зураг харагдана.
 */

import { readdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";

/**
 * `apps/api/app/content/badges.py`-ийн түлхүүрүүд — дарааллаар нь.
 * Тэнд тэмдэг нэмбэл энд ч нэмнэ; `apps/api/tests/test_badges.py` зөрүүг барина.
 */
const BADGE_KEYS = [
  "first-commit",
  "hello-world",
  "unstoppable",
  "code-smith",
  "bug-hunter",
  "debugger",
  "compiler",
  "mastery",
  "polyglot",
  "speed-coder",
  "night-owl",
  "early-bird",
  "persistent",
  "stack-overflow",
  "recursion",
  "clean-code",
  "code-warrior",
  "perfect-run",
  "perfectionist",
  "knowledge-seeker",
  "century",
  "mentor",
  "architect",
  "hidden-gem",
  "ahead-of-time",
  "where-the-answers-hide",
  "through-anothers-path",
];

/** `first-commit`, `FirstCommit`, `first_commit` бүгд ижил. */
const normalize = (name) => name.toLowerCase().replace(/[-_\s]/g, "");
const KEY_BY_NAME = new Map(BADGE_KEYS.map((key) => [normalize(key), key]));

/** Зөвшөөрөгдөх өргөтгөлүүд — тохирох нь эхэнд. */
const EXTENSIONS = [".svg", ".png", ".webp"];

const BADGE_DIR = path.join(process.cwd(), "public", "badges");
const OUTPUT = path.join(process.cwd(), "src", "lib", "badge-manifest.ts");

const entries = await readdir(BADGE_DIR).catch(() => []);

const found = new Map();
const skipped = [];

for (const name of entries) {
  const extension = path.extname(name).toLowerCase();
  const base = path.basename(name, extension);

  if (name.startsWith(".") || extension === ".md") continue;

  if (!EXTENSIONS.includes(extension)) {
    skipped.push(`${name} (дэмжигдээгүй өргөтгөл — ${EXTENSIONS.join(", ")})`);
    continue;
  }
  const key = KEY_BY_NAME.get(normalize(base));
  if (!key) {
    skipped.push(`${name} (тэмдгийн түлхүүртэй таарахгүй нэр)`);
    continue;
  }

  const current = found.get(key);
  if (current && EXTENSIONS.indexOf(path.extname(current)) <= EXTENSIONS.indexOf(extension)) {
    continue;
  }
  found.set(key, `/badges/${name}`);
}

// Prettier-ийн `quoteProps: "as-needed"` — зөвхөн шаардлагатай түлхүүрт хашилт.
const property = (key) => (/^[A-Za-z_$][\w$]*$/.test(key) ? key : JSON.stringify(key));
const lines = BADGE_KEYS.filter((key) => found.has(key)).map(
  (key) => `  ${property(key)}: ${JSON.stringify(found.get(key))},`,
);

const contents = `/**
 * АВТОМАТААР ҮҮССЭН ФАЙЛ — гараар засахгүй.
 *
 * Үүсгэгч: scripts/generate-badge-manifest.mjs
 * Дүрс нэмэхдээ \`public/badges/<түлхүүр>.svg\` файлыг хийгээд build хийнэ.
 */

export const BADGE_FILES: Partial<Record<string, string>> = {${
  lines.length > 0 ? `\n${lines.join("\n")}\n` : ""
}};
`;

const previous = await readFile(OUTPUT, "utf8").catch(() => null);
if (previous === contents) {
  console.log(`badges: ${found.size}/${BADGE_KEYS.length} icon(s), manifest unchanged`);
} else {
  await writeFile(OUTPUT, contents, "utf8");
  console.log(`badges: wrote manifest with ${found.size}/${BADGE_KEYS.length} icon(s)`);
}

for (const note of skipped) {
  console.warn(`badges: skipped ${note}`);
}

const missing = BADGE_KEYS.filter((key) => !found.has(key));
if (missing.length > 0) {
  console.warn(`badges: no icon yet for ${missing.join(", ")}`);
}
