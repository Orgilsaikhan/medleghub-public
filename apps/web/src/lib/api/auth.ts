import { apiFetch } from "@/lib/api/client";
import type { MessageResult, RegisterResult, User } from "@/lib/types/api";

export interface LoginInput {
  email: string;
  password: string;
}

export interface RegisterInput extends LoginInput {
  name: string;
  /** «Би 16 нас хүрсэн» — 16 хүрээгүй бол бүртгүүлэхгүй. */
  is_16_or_older: boolean;
  accept_terms: boolean;
  /** Найзын урилгын код. Хоосон бол урилгагүй. */
  referral_code?: string;
}

export function login(input: LoginInput): Promise<User> {
  return apiFetch<User>("/auth/login", { method: "POST", json: input });
}

/** Имэйл баталгаажуулалт асаалттай бол нэвтрүүлэхгүй — код илгээнэ. */
export function register(input: RegisterInput): Promise<RegisterResult> {
  return apiFetch<RegisterResult>("/auth/register", { method: "POST", json: input });
}

/** Имэйлд ирсэн кодыг шалгаж нэвтрүүлнэ. */
export function verifyEmail(input: { email: string; code: string }): Promise<User> {
  return apiFetch<User>("/auth/verify-email", { method: "POST", json: input });
}

export function resendVerification(email: string): Promise<MessageResult> {
  return apiFetch<MessageResult>("/auth/verify-email/resend", {
    method: "POST",
    json: { email },
  });
}

/** Бүртгэлтэй эсэхээс үл хамааран ижил хариу өгнө. */
export function forgotPassword(email: string): Promise<MessageResult> {
  return apiFetch<MessageResult>("/auth/password/forgot", { method: "POST", json: { email } });
}

/** Кодоор нууц үг солино. Бусад төхөөрөмжийн сесс гарч, энэ төхөөрөмж нэвтэрнэ. */
export function resetPassword(input: {
  email: string;
  code: string;
  new_password: string;
}): Promise<User> {
  return apiFetch<User>("/auth/password/reset", { method: "POST", json: input });
}

export function logout(): Promise<MessageResult> {
  return apiFetch<MessageResult>("/auth/logout", { method: "POST" });
}

export interface ChangePasswordInput {
  current_password: string;
  new_password: string;
}

/** Бусад төхөөрөмж дээрх сессүүд гарна — энэ сесс шинэ cookie авна. */
export function changePassword(input: ChangePasswordInput): Promise<MessageResult> {
  return apiFetch<MessageResult>("/auth/password", { method: "POST", json: input });
}

export function getCurrentUser(): Promise<User> {
  return apiFetch<User>("/auth/me");
}
