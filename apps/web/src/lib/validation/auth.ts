import { z } from "zod";

/** Frontend-ийн шалгалт нь backend-ийн дүрэмтэй тохирно (`app/schemas/auth.py`). */

const email = z
  .string()
  .trim()
  .min(1, "Имэйл хаягаа оруулна уу.")
  .max(255, "Имэйл хэт урт байна.")
  .email("Имэйл хаяг буруу байна.");

const password = z
  .string()
  .min(8, "Нууц үг дор хаяж 8 тэмдэгт байх ёстой.")
  .max(72, "Нууц үг хэт урт байна.");

export const loginSchema = z.object({
  email,
  password: z.string().min(1, "Нууц үгээ оруулна уу."),
});

const strongPassword = password
  .refine((value) => /[a-zA-Zа-яөүА-ЯӨҮ]/.test(value), {
    message: "Нууц үг дор хаяж нэг үсэг агуулсан байх ёстой.",
  })
  .refine((value) => /\d/.test(value), {
    message: "Нууц үг дор хаяж нэг тоо агуулсан байх ёстой.",
  });

export const changePasswordSchema = z
  .object({
    current_password: z.string().min(1, "Одоогийн нууц үгээ оруулна уу."),
    new_password: strongPassword,
    confirm_password: z.string(),
  })
  .refine((values) => values.new_password === values.confirm_password, {
    message: "Шинэ нууц үг таарахгүй байна.",
    path: ["confirm_password"],
  });

const name = z
  .string()
  .trim()
  .min(2, "Нэр дор хаяж 2 тэмдэгт байх ёстой.")
  .max(120, "Нэр хэт урт байна.");

/** Supabase-ийн имэйл код — 6 орон (тохиргоогоор 10 хүртэл). */
const code = z
  .string()
  .trim()
  .regex(/^\d{6,10}$/, "Имэйлд ирсэн кодоо оруулна уу.");

export const registerSchema = z.object({
  name,
  email,
  password: strongPassword,
  is_16_or_older: z.boolean().refine(Boolean, {
    message: "Бүртгүүлэхийн тулд 16 нас хүрсэн байх ёстой.",
  }),
  accept_terms: z.boolean().refine(Boolean, {
    message: "Үйлчилгээний нөхцөл, Нууцлалын бодлогыг зөвшөөрнө үү.",
  }),
  /** Заавал биш. Байгаа эсэхийг сервер шалгана (`INVALID_REFERRAL_CODE`). */
  referral_code: z.string().trim().max(64, "Код хэт урт байна."),
});

export const codeSchema = z.object({ code });

export const forgotPasswordSchema = z.object({ email });

export const resetPasswordSchema = z
  .object({
    code,
    new_password: strongPassword,
    confirm_password: z.string(),
  })
  .refine((values) => values.new_password === values.confirm_password, {
    message: "Шинэ нууц үг таарахгүй байна.",
    path: ["confirm_password"],
  });

export const nameSchema = z.object({ name });

export const changeEmailSchema = z.object({
  new_email: email,
  password: z.string().min(1, "Нууц үгээ оруулна уу."),
});

export const deleteAccountSchema = z.object({
  password: z.string().min(1, "Нууц үгээ оруулна уу."),
});

export type LoginValues = z.infer<typeof loginSchema>;
export type RegisterValues = z.infer<typeof registerSchema>;
export type ChangePasswordValues = z.infer<typeof changePasswordSchema>;
export type CodeValues = z.infer<typeof codeSchema>;
export type ForgotPasswordValues = z.infer<typeof forgotPasswordSchema>;
export type ResetPasswordValues = z.infer<typeof resetPasswordSchema>;
export type NameValues = z.infer<typeof nameSchema>;
export type ChangeEmailValues = z.infer<typeof changeEmailSchema>;
export type DeleteAccountValues = z.infer<typeof deleteAccountSchema>;
