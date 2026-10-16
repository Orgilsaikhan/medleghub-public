"use client";

import { useRouter } from "next/navigation";
import { useEffect, useRef, type ReactNode } from "react";

import { useCurrentUser } from "@/lib/hooks/use-auth";

interface RequireAuthProps {
  children: ReactNode;
  /** Зөвхөн админд нээлттэй хуудас эсэх. */
  adminOnly?: boolean;
  /** Нэвтрэлт тодрох хүртэл харуулах агуулга. */
  fallback?: ReactNode;
}

/**
 * Хамгаалагдсан хуудасны бүрхүүл.
 *
 * ЭНЭ НЬ ХАМГААЛАЛТ БИШ — зөвхөн UX. Жинхэнэ эрхийг backend шалгана: нэвтрээгүй
 * хэрэглэгч энэ шалгуурыг тойрсон ч API нь 401/403 буцаана.
 */
export function RequireAuth({ children, adminOnly = false, fallback }: RequireAuthProps) {
  const router = useRouter();
  const { isLoading, isAuthenticated, isAdmin } = useCurrentUser();

  // Хэрэглэгч энэ хуудсан дээр нэвтэрсэн байсан эсэх.
  const wasAuthenticated = useRef(false);
  const allowed = isAuthenticated && (!adminOnly || isAdmin);

  useEffect(() => {
    if (isLoading) return;

    if (isAuthenticated) {
      wasAuthenticated.current = true;
      if (adminOnly && !isAdmin) router.replace("/dashboard");
      return;
    }

    // Гарсан эсвэл сесс дууссан тохиолдол: нүүр хуудас руу. Ингэснээр «Гарах»
    // товчны шилжилттэй мөргөлдөхгүй бөгөөд толгой хэсэгт нэвтрэх холбоос байна.
    if (wasAuthenticated.current) {
      router.replace("/");
      return;
    }

    const next = `${window.location.pathname}${window.location.search}`;
    router.replace(`/login?next=${encodeURIComponent(next)}`);
  }, [isLoading, isAuthenticated, isAdmin, adminOnly, router]);

  if (isLoading || !allowed) {
    return <>{fallback ?? null}</>;
  }

  return <>{children}</>;
}
