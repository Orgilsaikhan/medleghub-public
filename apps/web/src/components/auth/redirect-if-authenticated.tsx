"use client";

import { useRouter } from "next/navigation";
import { useEffect, type ReactNode } from "react";

import { useCurrentUser } from "@/lib/hooks/use-auth";
import { useAuthRedirect } from "@/lib/hooks/use-auth-redirect";

/** Нэвтэрсэн хэрэглэгчийг login/register хуудсан дээр байлгах шаардлагагүй. */
export function RedirectIfAuthenticated({ children }: { children: ReactNode }) {
  const router = useRouter();
  const { isLoading, isAuthenticated } = useCurrentUser();
  const { target } = useAuthRedirect();

  useEffect(() => {
    if (!isLoading && isAuthenticated) router.replace(target);
  }, [isLoading, isAuthenticated, target, router]);

  return <>{children}</>;
}
