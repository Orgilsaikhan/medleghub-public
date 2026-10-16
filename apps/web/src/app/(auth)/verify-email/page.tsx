import type { Metadata } from "next";
import { Suspense } from "react";

import { AuthCard } from "@/components/auth/auth-card";
import { VerifyEmailForm } from "@/components/auth/verify-email-form";
import { Skeleton } from "@/components/ui/skeleton";
import { mn } from "@/lib/i18n/mn";

export const metadata: Metadata = {
  title: mn.auth.verifyTitle,
  robots: { index: false, follow: false },
};

export default function VerifyEmailPage() {
  return (
    // AuthCard болон VerifyEmailForm хоёулаа useSearchParams ашигладаг тул Suspense хэрэгтэй.
    <Suspense fallback={<Skeleton className="h-80 w-full max-w-sm" />}>
      <AuthCard
        title={mn.auth.verifyTitle}
        subtitle={mn.auth.verifyCardSubtitle}
        footerPrompt={mn.auth.hasAccount}
        footerLinkLabel={mn.auth.goLogin}
        footerHref="/login"
      >
        <VerifyEmailForm />
      </AuthCard>
    </Suspense>
  );
}
