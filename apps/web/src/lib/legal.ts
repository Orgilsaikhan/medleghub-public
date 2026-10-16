import { readFileSync } from "node:fs";
import path from "node:path";

export type LegalDocument = "privacy" | "terms";
export type LegalLanguage = "mn" | "en";

/**
 * Хууль эрх зүйн баримт бичгийн Markdown эх (`src/content/legal/`).
 *
 * Зөвхөн build-ийн үед дуудагдана — хуудсууд `force-static` тул Cloudflare
 * Workers дээр runtime-д файлын систем рүү хандахгүй.
 */
export function readLegalDocument(doc: LegalDocument, lang: LegalLanguage): string {
  return readFileSync(path.join(process.cwd(), "src/content/legal", `${doc}.${lang}.md`), "utf8");
}
