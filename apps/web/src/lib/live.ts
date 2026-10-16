/**
 * MedlegHub Live — UI-гүй туслахууд: төлөв, файлын төрөл, сэдэв хайх.
 *
 * Эрх, хязгаар, эзэмшлийн тооцоог зөвхөн сервер хийнэ — энд зөвхөн харуулах,
 * урьдчилан шалгахад хэрэгтэй зүйлс.
 */

import type {
  LiveGenerationStatus,
  LiveMaterialDetail,
  LiveMaterialKind,
  LiveMaterialStatus,
  LiveSection,
  LiveTopic,
} from "@/lib/types/live";

/** Материал AI-аар задлагдаж байх үеийн шалгах давтамж. */
export const MATERIAL_POLL_MS = 3000;
/** Заавар, тест, таамаг бэлтгэгдэж байх үеийн шалгах давтамж. */
export const GENERATION_POLL_MS = 2000;

/** AI ажиллаж байгаа (дараалалд эсвэл боловсруулж буй) эсэх. */
export function isMaterialProcessing(status: LiveMaterialStatus | undefined): boolean {
  return status === "queued" || status === "processing";
}

export function isGenerating(status: LiveGenerationStatus | undefined): boolean {
  return status === "queued" || status === "processing";
}

/** «Лекц 3.PDF» → ".pdf". Цэггүй бол хоосон. */
export function fileExtension(name: string): string {
  const dot = name.lastIndexOf(".");
  return dot > 0 ? name.slice(dot).toLowerCase() : "";
}

const IMAGE_EXTENSIONS = new Set([".png", ".jpg", ".jpeg", ".webp", ".gif", ".heic", ".heif"]);

/** Оруулахын өмнөх дүрсэнд — жинхэнэ төрлийг сервер файлын агуулгаар тогтооно. */
export function kindFromFilename(name: string): LiveMaterialKind | null {
  const extension = fileExtension(name);
  if (IMAGE_EXTENSIONS.has(extension)) return "image";
  if (extension === ".markdown") return "md";
  const kind = extension.slice(1);
  return kind === "pdf" || kind === "pptx" || kind === "docx" || kind === "txt" || kind === "md"
    ? kind
    : null;
}

const DOCUMENT_ORDER = [".pdf", ".pptx", ".docx", ".txt", ".md"];
const IMAGE_ORDER = [".png", ".jpg", ".webp", ".gif", ".heic"];
/** Нэг төрлийн хоёр нэр — жагсаалтад нэг л удаа. */
const ALIASES: Record<string, string> = { ".markdown": ".md", ".jpeg": ".jpg", ".heif": ".heic" };

/**
 * Серверийн өргөтгөлийн жагсаалтыг (цагаан толгойн дарааллаар, давхар нэртэй)
 * хүнд ойлгомжтой болгоно: «PDF, PPTX, DOCX, TXT, MD», зураг тусдаа.
 */
export function describeAcceptedTypes(
  accepted: string[],
  imagesLabel: (types: string) => string,
): string {
  const present = new Set(
    accepted.map((item) => ALIASES[item.toLowerCase()] ?? item.toLowerCase()),
  );
  const name = (extension: string) => extension.slice(1).toUpperCase();
  const documents = DOCUMENT_ORDER.filter((item) => present.has(item)).map(name);
  const images = IMAGE_ORDER.filter((item) => present.has(item)).map(name);
  const known = new Set([...DOCUMENT_ORDER, ...IMAGE_ORDER]);
  const other = [...present].filter((item) => !known.has(item)).map(name);
  const parts = [...documents, ...other];
  if (images.length > 0) parts.push(imagesLabel(images.join(", ")));
  return parts.join(", ");
}

/** Хуучин (.ppt, .doc) эсвэл макротой Office файл — хөрвүүлээд оруулах ёстой. */
const CONVERTIBLE_EXTENSIONS = new Set([".ppt", ".pps", ".doc", ".pptm", ".ppsm", ".docm"]);

export function needsConversion(name: string): boolean {
  return CONVERTIBLE_EXTENSIONS.has(fileExtension(name));
}

/** Файлын нэрээс өргөтгөлгүй нэр — «Нэр» талбарын placeholder. */
export function titleFromFilename(name: string): string {
  const extension = fileExtension(name);
  return extension ? name.slice(0, -extension.length) : name;
}

export interface TopicRef {
  topic: LiveTopic;
  section: LiveSection;
  /** 1-ээс эхэлсэн — «Хэсэг 2». */
  sectionNumber: number;
}

export function findTopic(material: LiveMaterialDetail, topicId: string): TopicRef | null {
  for (const [index, section] of material.sections.entries()) {
    const topic = section.topics.find((item) => item.id === topicId);
    if (topic) return { topic, section, sectionNumber: index + 1 };
  }
  return null;
}

/** Хуудасны дугаарууд: [3, 4, 5, 8] → "3–5, 8". */
export function formatPages(pages: number[]): string {
  const sorted = [...new Set(pages)].filter((page) => page > 0).sort((a, b) => a - b);
  const ranges: string[] = [];
  let start = sorted[0];
  let previous = sorted[0];
  for (const page of sorted.slice(1)) {
    if (page === previous + 1) {
      previous = page;
      continue;
    }
    ranges.push(start === previous ? `${start}` : `${start}–${previous}`);
    start = page;
    previous = page;
  }
  if (start !== undefined) ranges.push(start === previous ? `${start}` : `${start}–${previous}`);
  return ranges.join(", ");
}

/**
 * Шалгалтын бэлтгэлийн төлөвлөгөөний тэмдэглэгээ — зөвхөн энэ хөтөчид
 * (`localStorage`). Таамаг бүрт тусдаа: шинээр үүсгэвэл жагсаалт өөр.
 */
export function studyPlanStorageKey(generationId: string): string {
  return `medleghub:live-plan:${generationId}`;
}
