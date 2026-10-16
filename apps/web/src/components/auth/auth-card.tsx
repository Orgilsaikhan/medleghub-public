import Link from "next/link";
import type { ReactNode } from "react";

import { AuthFooterLink } from "@/components/auth/auth-footer-link";
import { LogoMark } from "@/components/layout/logo";
import { mn } from "@/lib/i18n/mn";

interface AuthCardProps {
  title: string;
  subtitle: string;
  children: ReactNode;
  footerPrompt: string;
  footerLinkLabel: string;
  footerHref: string;
}

export function AuthCard({
  title,
  subtitle,
  children,
  footerPrompt,
  footerLinkLabel,
  footerHref,
}: AuthCardProps) {
  return (
    <div className="w-full max-w-sm">
      {/* Үг тэмдэг нь нэрийг өөртөө агуулдаг тул дахин бичихгүй. */}
      <Link href="/" aria-label={mn.brand.name} className="mb-8 flex items-center justify-center">
        <LogoMark />
      </Link>

      <div className="bg-card rounded-xl border p-6 shadow-sm sm:p-8">
        <h1 className="text-xl font-semibold tracking-tight">{title}</h1>
        <p className="text-muted-foreground mt-1.5 text-sm">{subtitle}</p>

        <div className="mt-6">{children}</div>
      </div>

      <p className="text-muted-foreground mt-6 text-center text-sm">
        {footerPrompt}{" "}
        <AuthFooterLink
          href={footerHref}
          className="text-foreground font-medium underline underline-offset-4"
        >
          {footerLinkLabel}
        </AuthFooterLink>
      </p>
    </div>
  );
}
