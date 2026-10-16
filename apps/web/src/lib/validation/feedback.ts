import { z } from "zod";

/** Backend-ийн `app/schemas/feedback.py`-тай тохирсон дүрмүүд. */
export const feedbackSchema = z.object({
  kind: z.enum(["idea", "bug", "other"]),
  message: z
    .string()
    .trim()
    .min(5, "Дор хаяж 5 тэмдэгт бичнэ үү.")
    .max(2000, "Мессеж 2000 тэмдэгтээс хэтэрсэн байна."),
});

export type FeedbackFormValues = z.infer<typeof feedbackSchema>;
