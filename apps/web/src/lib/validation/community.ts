import { z } from "zod";

import { postLanguageOrder, postTypeOrder } from "@/lib/i18n/mn";

/** Backend-ийн `app/schemas/community_post.py`-тай тохирсон дүрмүүд. */
export const postSchema = z.object({
  title: z
    .string()
    .trim()
    .min(5, "Гарчиг дор хаяж 5 тэмдэгт байна.")
    .max(150, "Гарчиг 150 тэмдэгтээс хэтэрсэн байна."),
  body: z
    .string()
    .trim()
    .min(10, "Агуулга дор хаяж 10 тэмдэгт байна.")
    .max(10_000, "Агуулга 10,000 тэмдэгтээс хэтэрсэн байна."),
  language: z.enum(postLanguageOrder, { error: "Хэлээ сонгоно уу." }),
  type: z.enum(postTypeOrder, { error: "Төрлөө сонгоно уу." }),
});

export type PostFormValues = z.infer<typeof postSchema>;

export const commentSchema = z.object({
  body: z
    .string()
    .trim()
    .min(1, "Сэтгэгдлээ бичнэ үү.")
    .max(3000, "Сэтгэгдэл 3000 тэмдэгтээс хэтэрсэн байна."),
});

export type CommentFormValues = z.infer<typeof commentSchema>;

export const reportSchema = z.object({
  reason: z.enum(["spam", "abuse", "other"]),
  details: z.string().trim().max(500, "Тайлбар 500 тэмдэгтээс хэтэрсэн байна."),
});

export type ReportFormValues = z.infer<typeof reportSchema>;
