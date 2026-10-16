/**
 * АВТОМАТААР ҮҮССЭН ФАЙЛ — гараар засахгүй.
 *
 * Үүсгэгч: scripts/generate-logo-manifest.mjs
 * Лого нэмэхдээ `public/logos/<ангилал>.svg` файлыг хийгээд build хийнэ.
 */

import type { Category } from "@/lib/types/api";

export const LOGO_FILES: Partial<Record<Category, string>> = {
  html_css: "/logos/html_css.png",
  c: "/logos/c.png",
};
