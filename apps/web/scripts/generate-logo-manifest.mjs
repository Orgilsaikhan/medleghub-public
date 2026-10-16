/**
 * `public/logos/` доторх файлуудыг уншиж, лого бүртгэлийг үүсгэнэ.
 *
 * Файлын нэр нь ангиллын түлхүүртэй таарах ёстой:
 *   public/logos/html_css.png  →  html_css ангилал
 *   public/logos/python.svg    →  python ангилал
 *
 * Ингэснээр шинэ лого нэмэхэд код засах шаардлагагүй — файлаа хийгээд
 * дахин build хийхэд хангалттай.
 *
 * Яагаад бүртгэл үүсгэдэг вэ: component нь browser дээр ажиллах тул файлын
 * системийг уншиж чадахгүй. Байхгүй файл руу хандвал 404 болж, зураг
 * эвдэрсэн байдалтай харагдана. Тиймээс байгаа файлуудыг build хийх үед
 * тогтоож, кодонд бичнэ.
 */

import { readdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";

/** `app/models/enums.py` доторх Category-тэй тааруулсан жагсаалт. */
const CATEGORIES = [
  "html_css",
  "javascript",
  "python",
  "c",
  "csharp",
  "java",
  "react",
  "backend",
  "database",
  "git",
  "flowgorithm",
];

/** Зөвшөөрөгдөх өргөтгөлүүд — тохирох нь эхэнд. */
const EXTENSIONS = [".svg", ".png", ".webp"];

/**
 * PNG нь тунгалаг давхаргатай эсэхийг шалгана.
 *
 * Интернэтээс татсан "тунгалаг" PNG-үүд ихэвчлэн шатрын хээг зурагтаа
 * шингээсэн байдаг. Тэдгээр нь картын өнгөт дэвсгэр дээр цагаан хайрцаг
 * болж харагдана. Нэмэлт сан ашиглалгүй PNG-ийн толгойг шууд уншина.
 */
async function pngHasAlpha(filePath) {
  const data = await readFile(filePath);
  if (data.length < 26 || data.readUInt32BE(0) !== 0x89504e47) return true;

  // IHDR нь үргэлж эхний хэсэг: 8 байт гарын үсэг + 8 байт толгой.
  const colourType = data[25];
  if (colourType === 4 || colourType === 6) return true; // alpha суваг бүхий
  if (colourType !== 3) return false; // саарал эсвэл RGB — тунгалаг байх аргагүй

  // Палитртай зураг нь tRNS хэсэгтэй бол тунгалаг байж чадна.
  let offset = 8;
  while (offset + 8 <= data.length) {
    const length = data.readUInt32BE(offset);
    const type = data.toString("ascii", offset + 4, offset + 8);
    if (type === "tRNS") return true;
    if (type === "IEND") break;
    offset += 12 + length;
  }
  return false;
}

const LOGO_DIR = path.join(process.cwd(), "public", "logos");
const OUTPUT = path.join(process.cwd(), "src", "lib", "logo-manifest.ts");

const entries = await readdir(LOGO_DIR).catch(() => []);

/** Нэг ангилалд олон файл байвал жагсаалтын эхний өргөтгөлийг сонгоно. */
const found = new Map();
const skipped = [];
const warnings = [];

for (const name of entries) {
  const extension = path.extname(name).toLowerCase();
  const base = path.basename(name, extension);

  if (extension === ".md") continue;

  if (!EXTENSIONS.includes(extension)) {
    skipped.push(`${name} (дэмжигдээгүй өргөтгөл)`);
    continue;
  }
  if (!CATEGORIES.includes(base)) {
    skipped.push(`${name} (ангилалд тохирохгүй нэр)`);
    continue;
  }

  const current = found.get(base);
  if (current && EXTENSIONS.indexOf(path.extname(current)) <= EXTENSIONS.indexOf(extension)) {
    continue;
  }
  found.set(base, `/logos/${name}`);

  if (extension === ".png" && !(await pngHasAlpha(path.join(LOGO_DIR, name)))) {
    warnings.push(
      `${name} нь тунгалаг давхаргагүй — картын өнгөт дэвсгэр дээр цагаан ` +
        `хайрцаг болж харагдана. SVG ашиглах, эсвэл дэвсгэрийг нь арилгана уу.`,
    );
  }
}

const lines = CATEGORIES.filter((category) => found.has(category)).map(
  (category) => `  ${category}: ${JSON.stringify(found.get(category))},`,
);

const contents = `/**
 * АВТОМАТААР ҮҮССЭН ФАЙЛ — гараар засахгүй.
 *
 * Үүсгэгч: scripts/generate-logo-manifest.mjs
 * Лого нэмэхдээ \`public/logos/<ангилал>.svg\` файлыг хийгээд build хийнэ.
 */

import type { Category } from "@/lib/types/api";

export const LOGO_FILES: Partial<Record<Category, string>> = {
${lines.join("\n")}${lines.length > 0 ? "\n" : ""}};
`;

const previous = await readFile(OUTPUT, "utf8").catch(() => null);
if (previous === contents) {
  console.log(`logos: ${found.size} file(s), manifest unchanged`);
} else {
  await writeFile(OUTPUT, contents, "utf8");
  console.log(`logos: wrote manifest with ${found.size} file(s)`);
}

for (const note of skipped) {
  console.warn(`logos: skipped ${note}`);
}

for (const note of warnings) {
  console.warn(`logos: WARNING ${note}`);
}
