import { redirect } from "next/navigation";

/**
 * Хуучин буцах хаяг. 2026-09-30-аас Wire `/billing/success` руу буцаадаг —
 * өмнө нь үүссэн нэхэмжлэхүүд энд ирсэн ч баримтын хуудас руу шилжинэ.
 */
export default async function PaymentReturnPage({ searchParams }: PageProps<"/billing/return">) {
  const { payment } = await searchParams;
  const id = Array.isArray(payment) ? payment[0] : payment;
  redirect(id ? `/billing/success?payment=${encodeURIComponent(id)}` : "/billing/success");
}
