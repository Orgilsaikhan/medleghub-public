"use client";

import { useQuery } from "@tanstack/react-query";

import { getPlan } from "@/lib/api/billing";
import { useCurrentUser } from "@/lib/hooks/use-auth";
import { queryKeys } from "@/lib/query-keys";

/**
 * Standard багцын төлөв ба үнэ.
 *
 * Нэвтрээгүй зочинд ч үнийг буцаана — үнийг зөвхөн backend мэднэ (админ
 * `/admin/billing` дээр өөрчилнө), энд давхардахгүй. Нэвтэрсэн эсэх
 * өөрчлөгдөхөд хариу өөр тул key-д оруулна.
 */
export function usePlan() {
  const { user, isLoading } = useCurrentUser();
  return useQuery({
    queryKey: [...queryKeys.billing.plan, user?.id ?? "guest"],
    queryFn: getPlan,
    enabled: !isLoading,
    staleTime: 60_000,
  });
}
