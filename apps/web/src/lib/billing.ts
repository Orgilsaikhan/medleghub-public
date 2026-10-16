/**
 * Төлбөрийн дараа хаана буцахыг санана.
 *
 * Wire-ийн хуудаснаас манай `/billing/return` руу буцдаг — хэрэглэгч аль
 * хичээл дээр багц авахаар шийдсэнийг URL-ээр дамжуулах боломжгүй тул энд
 * хадгална. Зөвхөн дотоод `/learn/…` хаягийг хүлээж авна (open redirect биш).
 */

import { readLocal, writeLocal } from "@/lib/local-storage";

const RETURN_KEY = "medleghub:checkout-return";

export function safeReturnPath(value: string | null | undefined): string | null {
  if (!value || !value.startsWith("/learn/") || value.startsWith("//")) return null;
  return value;
}

export function rememberReturnPath(value: string | null): void {
  writeLocal(RETURN_KEY, safeReturnPath(value) ?? "");
}

export function recallReturnPath(): string | null {
  return safeReturnPath(readLocal(RETURN_KEY, ""));
}
