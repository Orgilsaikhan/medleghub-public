/** Хугацаа, тоо форматлах туслах функцүүд. */

import { mn } from "@/lib/i18n/mn";

/**
 * Секундийг хүний уншихад тохиромжтой болгоно.
 * 0 → "0 мин", 90 → "2 мин", 3900 → "1 ц 5 мин"
 */
export function formatDuration(seconds: number): string {
  if (!seconds || seconds < 0) return mn.common.minutesShort(0);

  const totalMinutes = Math.round(seconds / 60);
  const hours = Math.floor(totalMinutes / 60);
  const minutes = totalMinutes % 60;

  if (hours === 0) return mn.common.minutesShort(minutes);
  if (minutes === 0) return mn.common.hoursShort(hours);
  return `${mn.common.hoursShort(hours)} ${mn.common.minutesShort(minutes)}`;
}

/** Секундийг `MM:SS` хэлбэрт (хичээлийн мөрөнд). */
export function formatClock(seconds: number): string {
  const safe = Math.max(0, Math.round(seconds));
  const minutes = Math.floor(safe / 60);
  const rest = safe % 60;
  return `${minutes}:${String(rest).padStart(2, "0")}`;
}

const MONTHS_MN = [
  "1 сар",
  "2 сар",
  "3 сар",
  "4 сар",
  "5 сар",
  "6 сар",
  "7 сар",
  "8 сар",
  "9 сар",
  "10 сар",
  "11 сар",
  "12 сар",
];

/**
 * Огноог монголоор.
 *
 * `Intl` нь `mn-MN` локалийг бүх хөтөч дээр дэмждэггүй (Chromium дээр англи
 * руу шилждэг) тул гараар хөрвүүлнэ.
 */
export function formatDate(iso: string): string {
  const date = new Date(iso);
  if (Number.isNaN(date.getTime())) return "";
  return `${date.getFullYear()} оны ${MONTHS_MN[date.getMonth()]}ын ${date.getDate()}`;
}

const DAY_MS = 24 * 60 * 60 * 1000;
const MINUTE_MS = 60 * 1000;
const HOUR_MS = 60 * MINUTE_MS;

/**
 * «5 минутын өмнө» хэлбэр. Долоо хоногоос хуучин бол огноогоор. Ирээдүйн
 * огноо (цагийн зөрүү) «дөнгөж сая».
 */
export function formatRelative(iso: string, now: number = Date.now()): string {
  const elapsed = now - new Date(iso).getTime();
  if (Number.isNaN(elapsed)) return "";
  if (elapsed < MINUTE_MS) return mn.community.justNow;
  if (elapsed < HOUR_MS) return mn.community.minutesAgo(Math.floor(elapsed / MINUTE_MS));
  if (elapsed < DAY_MS) return mn.community.hoursAgo(Math.floor(elapsed / HOUR_MS));
  if (elapsed < 7 * DAY_MS) return mn.community.daysAgo(Math.floor(elapsed / DAY_MS));
  return formatDate(iso);
}

/**
 * `iso` хүртэл хэдэн хоног үлдсэн. Эхэлсэн хоногийг бүтнээр тооцно (3 цаг
 * үлдсэн бол 1). Өнгөрсөн эсвэл буруу огноо бол 0.
 */
export function daysLeft(iso: string, now: number = Date.now()): number {
  const remaining = new Date(iso).getTime() - now;
  if (Number.isNaN(remaining) || remaining <= 0) return 0;
  return Math.ceil(remaining / DAY_MS);
}

/**
 * `months` сар нэмсэн (сөрөг бол хассан) огноо. Postgres-ийн `interval`-тэй
 * адил сарын сүүлээр тасална: 1-р сарын 31 + 1 сар = 2-р сарын 28/29.
 */
export function addMonths(date: Date, months: number): Date {
  const result = new Date(date);
  const day = result.getDate();
  result.setDate(1);
  result.setMonth(result.getMonth() + months);
  const lastDay = new Date(result.getFullYear(), result.getMonth() + 1, 0).getDate();
  result.setDate(Math.min(day, lastDay));
  return result;
}

/** Төгрөг: 24900 → "24,900₮". */
export function formatMnt(amount: number): string {
  return `${Math.round(amount)
    .toString()
    .replace(/\B(?=(\d{3})+(?!\d))/g, ",")}₮`;
}

/**
 * Хувь: 45.2 → "45%", 2.5 → "2.5%", 0.04 → "<0.1%", 99.8 → "99%". 10-аас
 * бага бол нэг оронтой, ингэснээр ховор амжилтуудын ялгаа харагдана. 100-д
 * хүрээгүйг «100%» гэж дугуйлахгүй — бүгд авсан мэт харагдана.
 */
export function formatPercent(value: number): string {
  if (value <= 0) return "0%";
  if (value >= 100) return "100%";
  if (value < 0.1) return "<0.1%";
  if (value < 10) return `${Number(value.toFixed(1))}%`;
  return `${Math.min(Math.round(value), 99)}%`;
}

/**
 * Файлын хэмжээ (аравтын нэгж — сервер 20 000 000 байтыг «20 MB» гэж заадаг):
 * 900 → "900 B", 52_000 → "52 KB", 1_500_000 → "1.5 MB", 20_000_000 → "20 MB".
 */
export function formatFileSize(bytes: number): string {
  if (bytes < 1000) return `${Math.max(0, Math.round(bytes))} B`;
  if (bytes < 1_000_000) return `${Math.round(bytes / 1000)} KB`;
  const megabytes = bytes / 1_000_000;
  return `${megabytes < 10 ? Number(megabytes.toFixed(1)) : Math.round(megabytes)} MB`;
}

/** Аватарын үсэг — нэрийн эхний хоёр үгийн эхний үсэг. */
export function initials(name: string): string {
  const parts = name.trim().split(/\s+/).slice(0, 2);
  return parts.map((part) => part[0]?.toUpperCase() ?? "").join("") || "?";
}

/** Гарчгаас slug санал болгоно. Кирилл үсгийг латинаар галиглана. */
const CYRILLIC_TO_LATIN: Record<string, string> = {
  а: "a",
  б: "b",
  в: "v",
  г: "g",
  д: "d",
  е: "e",
  ё: "yo",
  ж: "j",
  з: "z",
  и: "i",
  й: "i",
  к: "k",
  л: "l",
  м: "m",
  н: "n",
  о: "o",
  ө: "u",
  п: "p",
  р: "r",
  с: "s",
  т: "t",
  у: "u",
  ү: "u",
  ф: "f",
  х: "h",
  ц: "ts",
  ч: "ch",
  ш: "sh",
  щ: "sh",
  ъ: "",
  ы: "y",
  ь: "",
  э: "e",
  ю: "yu",
  я: "ya",
};

export function suggestSlug(input: string): string {
  return input
    .toLowerCase()
    .split("")
    .map((char) => CYRILLIC_TO_LATIN[char] ?? char)
    .join("")
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 200);
}
