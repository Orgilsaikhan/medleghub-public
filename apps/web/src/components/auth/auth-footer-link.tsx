"use client";

import Link from "next/link";
import { useSearchParams } from "next/navigation";

import { isSafeInternalPath } from "@/lib/hooks/use-auth-redirect";

interface AuthFooterLinkProps {
  href: string;
  children: React.ReactNode;
  className?: string;
}

/**
 * Login ↔ Register хоорондын шилжих холбоос.
 *
 * `?next=` параметртэй ирсэн бол шилжихдээ дамжуулна — эс бөгөөс бүртгэлгүй
 * зочин сургалт руу буцах замаа алдана (login → register шилжихэд next
 * алга болдог байсан баг).
 */
export function AuthFooterLink({ href, children, className }: AuthFooterLinkProps) {
  const params = useSearchParams();
  const next = params.get("next");
  const target = isSafeInternalPath(next) ? `${href}?next=${encodeURIComponent(next)}` : href;

  return (
    <Link href={target} className={className}>
      {children}
    </Link>
  );
}
