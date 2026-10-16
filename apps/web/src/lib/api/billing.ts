import { apiFetch, type RequestOptions } from "@/lib/api/client";
import type {
  BillingPlan,
  AdminUserPlan,
  CheckoutSession,
  PaymentStatus,
  PlanPriceInfo,
  PlanStatus,
  PromoCodeInput,
  PromoCodeItem,
  PromoPreview,
  PromoRedeemResult,
  RedemptionReceipt,
} from "@/lib/types/api";

/** Багцын төлөв. Саяхан төлсөн, хүлээгдэж буй төлбөрийг сервер давхар шалгана. */
export function getPlan(init?: RequestOptions): Promise<PlanStatus> {
  return apiFetch<PlanStatus>("/billing/plan", init);
}

/**
 * `months` сарын төлбөрийн нэхэмжлэх — хариуны `checkout_url` руу шилжинэ.
 * Промо код өгөөгүй бол ашиглаагүй урилгын хөнгөлөлтийг сервер өөрөө хэрэглэнэ.
 * `premium` — Standard-ийг мөн сараар сунгаж, Premium-ийг нэмнэ.
 */
export function startCheckout(
  months: number,
  promoCode?: string | null,
  plan: BillingPlan = "standard",
): Promise<CheckoutSession> {
  return apiFetch<CheckoutSession>("/billing/checkout", {
    method: "POST",
    json: promoCode ? { months, plan, promo_code: promoCode } : { months, plan },
  });
}

/** Промо кодыг шалгана — ашигласанд тооцохгүй. */
export function checkPromo(code: string): Promise<PromoPreview> {
  return apiFetch<PromoPreview>("/billing/promo/check", { method: "POST", json: { code } });
}

/** Үнэгүй сарын кодыг идэвхжүүлж, багцыг төлбөргүй сунгана. `redemption_id` — баримт. */
export function redeemPromo(code: string): Promise<PromoRedeemResult> {
  return apiFetch<PromoRedeemResult>("/billing/promo/redeem", {
    method: "POST",
    json: { code },
  });
}

/** Үнэгүй сарын промо кодын баримт — зөвхөн өөрийнх. */
export function getRedemption(redemptionId: string): Promise<RedemptionReceipt> {
  return apiFetch<RedemptionReceipt>(`/billing/redemptions/${encodeURIComponent(redemptionId)}`);
}

/** Админ: бүх промо код, шинэ нь эхэндээ. */
export function listPromoCodes(): Promise<PromoCodeItem[]> {
  return apiFetch<PromoCodeItem[]>("/billing/promo-codes");
}

/** Админ: шинэ промо код. */
export function createPromoCode(input: PromoCodeInput): Promise<PromoCodeItem> {
  return apiFetch<PromoCodeItem>("/billing/promo-codes", { method: "POST", json: input });
}

/** Админ: идэвхтэй эсэх, дуусах хугацаа, ашиглах дээд тоо. Өгсөн талбарыг л өөрчилнө. */
export function updatePromoCode(
  id: string,
  input: Partial<Pick<PromoCodeItem, "active" | "expires_at" | "max_uses" | "note">>,
): Promise<PromoCodeItem> {
  return apiFetch<PromoCodeItem>(`/billing/promo-codes/${encodeURIComponent(id)}`, {
    method: "PATCH",
    json: input,
  });
}

/** Төлбөрийн төлөв. Сервер нь Wire-ээс шалгаж, амжилттай бол багцыг сунгана. */
export function getPayment(paymentId: string): Promise<PaymentStatus> {
  return apiFetch<PaymentStatus>(`/billing/payments/${encodeURIComponent(paymentId)}`);
}

/** Админ: одоогийн сарын үнэ, хэн хэзээ өөрчилсөн. */
export function getPlanPrice(): Promise<PlanPriceInfo> {
  return apiFetch<PlanPriceInfo>("/billing/price");
}

/** Админ: хэрэглэгчийн багцыг имэйлээр хайна. Имэйл URL-д (логт) орохгүй — body-гоор. */
export function lookupUserPlan(email: string): Promise<AdminUserPlan> {
  return apiFetch<AdminUserPlan>("/billing/grants/lookup", { method: "POST", json: { email } });
}

/** Админ: `months` > 0 бол багцыг нэмнэ, < 0 бол хасна. Өөрчлөлт түүхэнд үлдэнэ. */
export function adjustUserPlan(
  email: string,
  months: number,
  note: string | null,
): Promise<AdminUserPlan> {
  return apiFetch<AdminUserPlan>("/billing/grants", {
    method: "POST",
    json: { email, months, note },
  });
}

/** Админ: сарын үнийг өөрчилнө. Олон сарын үнийг сервер дахин тооцно. */
export function setPlanPrice(
  priceMnt: number,
  plan: BillingPlan = "standard",
): Promise<PlanPriceInfo> {
  return apiFetch<PlanPriceInfo>("/billing/price", {
    method: "PUT",
    json: { price_mnt: priceMnt, plan },
  });
}
