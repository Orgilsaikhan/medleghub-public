import { z } from "zod";

import { categoryOrder, difficultyOrder } from "@/lib/i18n/mn";
import type { Category, Difficulty } from "@/lib/types/api";

/** Backend-ийн `app/schemas/*`-тай тохирсон дүрмүүд. */

const slug = z
  .string()
  .trim()
  .min(1, "Slug оруулна уу.")
  .max(200, "Slug хэт урт байна.")
  .regex(/^[a-z0-9]+(?:-[a-z0-9]+)*$/, "Зөвхөн жижиг латин үсэг, тоо, зураас байна.");

const title = z
  .string()
  .trim()
  .min(2, "Гарчиг дор хаяж 2 тэмдэгт байх ёстой.")
  .max(200, "Гарчиг хэт урт байна.");

const optionalUrl = z
  .string()
  .trim()
  .max(1000, "Холбоос хэт урт байна.")
  .refine((value) => value === "" || /^https?:\/\//i.test(value), {
    message: "Холбоос http:// эсвэл https:// -ээр эхлэх ёстой.",
  });

export const courseSchema = z.object({
  title,
  slug,
  description: z.string().trim().max(5000, "Тайлбар хэт урт байна."),
  thumbnail_url: optionalUrl.max(500, "Холбоос хэт урт байна."),
  difficulty: z.enum(difficultyOrder as [Difficulty, ...Difficulty[]]),
  category: z.enum(categoryOrder as [Category, ...Category[]]),
  is_free: z.boolean(),
  /** `is_free=false` үед эхний хэдэн хичээл үнэгүй вэ. */
  free_lessons: z
    .number({ message: "Тоо оруулна уу." })
    .int("Бүхэл тоо оруулна уу.")
    .min(0, "Сөрөг байж болохгүй.")
    .max(10_000, "Хэт их байна."),
  published: z.boolean(),
});

export const moduleSchema = z.object({
  title,
  description: z.string().trim().max(2000, "Тайлбар хэт урт байна."),
});

export const lessonSchema = z.object({
  title,
  slug,
  description: z.string().trim().max(2000, "Тайлбар хэт урт байна."),
  video_url: optionalUrl,
  /** Формд минутаар оруулж, API руу секундээр илгээнэ. */
  duration_minutes: z
    .number({ message: "Тоо оруулна уу." })
    .min(0, "Сөрөг байж болохгүй.")
    .max(1440, "Хэт урт байна."),
  content: z.string().max(100_000, "Агуулга хэт урт байна."),
  initial_code: z.string().max(20_000, "Код хэт урт байна."),
  published: z.boolean(),
});

export type CourseFormValues = z.infer<typeof courseSchema>;
export type ModuleFormValues = z.infer<typeof moduleSchema>;
export type LessonFormValues = z.infer<typeof lessonSchema>;

/** Standard багцын сарын үнэ — серверийн хязгаартай ижил (100₮ – 1,000,000₮). */
export const planPriceSchema = z.object({
  price_mnt: z
    .number({ message: "Тоо оруулна уу." })
    .int("Бүхэл төгрөг оруулна уу.")
    .min(100, "Хамгийн багадаа 100₮.")
    .max(1_000_000, "Хамгийн ихдээ 1,000,000₮."),
});

export type PlanPriceValues = z.infer<typeof planPriceSchema>;

/** Багцыг нь өөрчлөх хэрэглэгчийг имэйлээр хайна. */
export const userPlanLookupSchema = z.object({
  email: z
    .string()
    .trim()
    .min(1, "Имэйл хаяг оруулна уу.")
    .max(255, "Имэйл хэт урт байна.")
    .email("Имэйл хаяг буруу байна."),
});

export type UserPlanLookupValues = z.infer<typeof userPlanLookupSchema>;

/**
 * Гараар нэмэх/хасах сар — серверийн хязгаартай ижил (`plan_max_grant_months`).
 * Чиглэлийг (нэмэх, хасах) товч сонгоно.
 */
export const userPlanAdjustSchema = z.object({
  months: z
    .number({ message: "Тоо оруулна уу." })
    .int("Бүхэл тоо оруулна уу.")
    .min(1, "Хамгийн багадаа 1 сар.")
    .max(24, "Хамгийн ихдээ 24 сар."),
  note: z.string().trim().max(500, "500 тэмдэгтээс ихгүй."),
});

export type UserPlanAdjustValues = z.infer<typeof userPlanAdjustSchema>;

/** Тоон талбарыг мөрөөр авч, хоосон бол `null` болгоно (`valueAsNumber`-ийн NaN-гүй). */
export function optionalInt(value: string): number | null {
  const trimmed = value.trim();
  return trimmed === "" ? null : Number(trimmed);
}

function inRange(value: number | null, min: number, max: number): boolean {
  return value !== null && Number.isInteger(value) && value >= min && value <= max;
}

/** Серверийн дүрэмтэй ижил: латин үсэг, тоо (зай, зураас хасагдана), 4–32 тэмдэгт. */
export function normalizePromoCode(value: string): string {
  return value.replace(/[\s_-]+/g, "").toUpperCase();
}

/**
 * Шинэ промо код. Хувь, сарын тоо, дээд тоог мөрөөр авна — төрлөөс хамаарч
 * аль нь заавал болохыг `superRefine` шалгана. Хоосон код — сервер үүсгэнэ.
 */
export const promoCodeSchema = z
  .object({
    code: z.string().max(64, "Код хэт урт байна."),
    kind: z.enum(["percent", "free_months"]),
    percent_off: z.string(),
    free_months: z.string(),
    /** `YYYY-MM-DD` эсвэл хоосон (хугацаагүй). */
    expires_on: z.string(),
    max_uses: z.string(),
    note: z.string().trim().max(500, "500 тэмдэгтээс ихгүй."),
  })
  .superRefine((values, ctx) => {
    const code = normalizePromoCode(values.code);
    if (code !== "" && !/^[A-Z0-9]{4,32}$/.test(code)) {
      ctx.addIssue({ code: "custom", path: ["code"], message: "Латин үсэг, тоо (4–32)." });
    }
    if (values.kind === "percent" && !inRange(optionalInt(values.percent_off), 1, 99)) {
      ctx.addIssue({ code: "custom", path: ["percent_off"], message: "1–99 хооронд." });
    }
    if (values.kind === "free_months" && !inRange(optionalInt(values.free_months), 1, 12)) {
      ctx.addIssue({ code: "custom", path: ["free_months"], message: "1–12 сар." });
    }
    if (values.max_uses.trim() !== "" && !inRange(optionalInt(values.max_uses), 1, 1_000_000)) {
      ctx.addIssue({ code: "custom", path: ["max_uses"], message: "1-ээс их бүхэл тоо." });
    }
    if (values.expires_on !== "" && values.expires_on < todayInUlaanbaatar()) {
      ctx.addIssue({ code: "custom", path: ["expires_on"], message: "Өнгөрсөн өдөр байна." });
    }
  });

export type PromoCodeValues = z.infer<typeof promoCodeSchema>;

/** Засах цонх: дуусах өдөр, дээд тоо, тэмдэглэл. */
export const promoCodeEditSchema = z
  .object({
    expires_on: z.string(),
    max_uses: z.string(),
    note: z.string().trim().max(500, "500 тэмдэгтээс ихгүй."),
  })
  .superRefine((values, ctx) => {
    if (values.max_uses.trim() !== "" && !inRange(optionalInt(values.max_uses), 1, 1_000_000)) {
      ctx.addIssue({ code: "custom", path: ["max_uses"], message: "1-ээс их бүхэл тоо." });
    }
  });

export type PromoCodeEditValues = z.infer<typeof promoCodeEditSchema>;

const UB_OFFSET_MS = 8 * 60 * 60 * 1000;

/** Өнөөдөр Улаанбаатарын цагаар, `YYYY-MM-DD`. */
export function todayInUlaanbaatar(now: number = Date.now()): string {
  return new Date(now + UB_OFFSET_MS).toISOString().slice(0, 10);
}

/** `YYYY-MM-DD` → тэр өдрийн 23:59:59 Улаанбаатарын цагаар (ISO). */
export function endOfUlaanbaatarDay(date: string): string {
  return `${date}T23:59:59+08:00`;
}

/** ISO огноо → `YYYY-MM-DD` Улаанбаатарын цагаар (`<input type="date">`-д). */
export function ulaanbaatarDate(iso: string): string {
  return new Date(new Date(iso).getTime() + UB_OFFSET_MS).toISOString().slice(0, 10);
}

/** `YYYY-MM-DD` → тэр өдрийн 00:00 Улаанбаатарын цагаар (ISO). */
export function startOfUlaanbaatarDay(date: string): string {
  return `${date}T00:00:00+08:00`;
}

/** Серверийн дүрэмтэй ижил: сайтын хуудас (`/…`, `//…` биш) эсвэл `https://…`. */
export function isAnnouncementUrl(value: string): boolean {
  if (/\s/.test(value)) return false;
  return (value.startsWith("/") && !value.startsWith("//")) || value.startsWith("https://");
}

/**
 * Зарлалын маягт. Өдрүүд `YYYY-MM-DD` эсвэл хоосон — API руу илгээхдээ
 * Улаанбаатарын цагийн өдрийн эхлэл, төгсгөл болгоно.
 */
export const announcementSchema = z
  .object({
    kind: z.enum(["update", "feature"]),
    title: z
      .string()
      .trim()
      .min(2, "Гарчиг дор хаяж 2 тэмдэгт байх ёстой.")
      .max(120, "120 тэмдэгтээс ихгүй."),
    body: z.string().trim().min(1, "Бичвэр оруулна уу.").max(2000, "2000 тэмдэгтээс ихгүй."),
    cta_label: z.string().trim().max(40, "40 тэмдэгтээс ихгүй."),
    cta_url: z.string().trim().max(500, "Холбоос хэт урт байна."),
    audience: z.enum(["everyone", "signed_in", "free", "standard"]),
    starts_on: z.string(),
    ends_on: z.string(),
    active: z.boolean(),
  })
  .superRefine((values, ctx) => {
    const both = "Товчны бичвэр, холбоосыг хамт оруулна уу.";
    if (values.cta_label && !values.cta_url) {
      ctx.addIssue({ code: "custom", path: ["cta_url"], message: both });
    }
    if (values.cta_url && !values.cta_label) {
      ctx.addIssue({ code: "custom", path: ["cta_label"], message: both });
    }
    if (values.cta_url && !isAnnouncementUrl(values.cta_url)) {
      ctx.addIssue({
        code: "custom",
        path: ["cta_url"],
        message: "/-ээр (сайтын хуудас) эсвэл https://-ээр эхлэх ёстой.",
      });
    }
    if (values.starts_on && values.ends_on && values.ends_on < values.starts_on) {
      ctx.addIssue({
        code: "custom",
        path: ["ends_on"],
        message: "Дуусах өдөр эхлэх өдрөөс өмнө байна.",
      });
    }
    if (values.ends_on && values.ends_on < todayInUlaanbaatar()) {
      ctx.addIssue({ code: "custom", path: ["ends_on"], message: "Өнгөрсөн өдөр байна." });
    }
  });

export type AnnouncementValues = z.infer<typeof announcementSchema>;

/** Premium гараар олгох — серверийн хязгаартай ижил (1–24 сар). */
export const liveGrantSchema = z.object({
  months: z
    .number({ message: "Тоо оруулна уу." })
    .int("Бүхэл тоо оруулна уу.")
    .min(1, "Хамгийн багадаа 1 сар.")
    .max(24, "Хамгийн ихдээ 24 сар."),
  note: z.string().trim().max(500, "500 тэмдэгтээс ихгүй."),
});

export type LiveGrantValues = z.infer<typeof liveGrantSchema>;
