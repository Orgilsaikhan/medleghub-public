"use client";

import { useRouter, useSearchParams } from "next/navigation";
import { useCallback } from "react";

/**
 * Нэвтэрсний дараа хаашаа буцахыг шийднэ.
 *
 * `?next=` параметрийг зөвхөн өөрийн сайт доторх зам байвал хүлээж авна —
 * гадны хаяг руу чиглүүлэх (open redirect) эмзэг байдлаас сэргийлнэ.
 */
export function useAuthRedirect() {
  const router = useRouter();
  const params = useSearchParams();
  const raw = params.get("next");

  const target = isSafeInternalPath(raw) ? raw : "/dashboard";

  const redirect = useCallback(() => {
    router.push(target);
    router.refresh();
  }, [router, target]);

  return { target, redirect };
}

export function isSafeInternalPath(value: string | null): value is string {
  if (!value) return false;
  // `//evil.com` болон `/\evil.com` нь хөтөч дээр гадны хаяг болж хувирдаг.
  return value.startsWith("/") && !value.startsWith("//") && !value.startsWith("/\\");
}
