import type { Metadata } from "next";
import { Suspense } from "react";

import { AuthCard } from "@/components/auth/auth-card";
import { ForgotPasswordForm } from "@/components/auth/forgot-password-form";
import { Skeleton } from "@/components/ui/skeleton";
import { mn } from "@/lib/i18n/mn";
import { pageMetadata } from "@/lib/seo";

// Маягтын хуудас — хайлтын үр дүнд гаргахгүй (sitemap-д ч байхгүй).
export const metadata: Metadata = pageMetadata({
  title: mn.auth.forgotTitle,
  description: mn.auth.forgotSubtitle,
  path: "/forgot-password",
  noindex: true,
});

export default function ForgotPasswordPage() {
  return (
    // AuthCard болон ForgotPasswordForm хоёулаа useSearchParams ашигладаг тул Suspense хэрэгтэй.
    <Suspense fallback={<Skeleton className="h-72 w-full max-w-sm" />}>
      <AuthCard
        title={mn.auth.forgotTitle}
        subtitle={mn.auth.forgotSubtitle}
        footerPrompt={mn.auth.rememberedPassword}
        footerLinkLabel={mn.auth.goLogin}
        footerHref="/login"
      >
        <ForgotPasswordForm />
      </AuthCard>
    </Suspense>
  );
}
