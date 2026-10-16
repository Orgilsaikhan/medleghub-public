/** Өөрийн бүртгэл — нэр, профайл нуух, имэйл солих, бүртгэл устгах. */

import { apiFetch } from "@/lib/api/client";
import type { ChangeEmailResult, EditorLayout, ReferralSummary, User } from "@/lib/types/api";

export function updateAccount(input: {
  name?: string;
  profile_hidden?: boolean;
  show_motivation?: boolean;
  editor_layout?: EditorLayout;
}): Promise<User> {
  return apiFetch<User>("/me", { method: "PATCH", json: input });
}

/** Нууц үгээ шалгуулна. Баталгаажуулалт асаалттай бол шинэ хаяг руу код илгээнэ. */
export function requestEmailChange(input: {
  new_email: string;
  password: string;
}): Promise<ChangeEmailResult> {
  return apiFetch<ChangeEmailResult>("/me/email", { method: "POST", json: input });
}

export function confirmEmailChange(code: string): Promise<User> {
  return apiFetch<User>("/me/email/confirm", { method: "POST", json: { code } });
}

/** Бүртгэлийг 2 цагийн дараа бүрмөсөн устгахаар товлоно. */
export function scheduleDeletion(password: string): Promise<User> {
  return apiFetch<User>("/me/delete", { method: "POST", json: { password } });
}

export function cancelDeletion(): Promise<User> {
  return apiFetch<User>("/me/delete/cancel", { method: "POST" });
}

/** Найзаа урих код ба олсон шагнал. Код анх дуудахад үүснэ. */
export function getReferral(): Promise<ReferralSummary> {
  return apiFetch<ReferralSummary>("/me/referral");
}
