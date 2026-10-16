import type { Metadata } from "next";
import { Suspense } from "react";

import { AuthCard } from "@/components/auth/auth-card";
import { LoginForm } from "@/components/auth/login-form";
import { Skeleton } from "@/components/ui/skeleton";
import { mn } from "@/lib/i18n/mn";
import { pageMetadata } from "@/lib/seo";

// Маягтын хуудас — хайлтын үр дүнд гаргахгүй (sitemap-д ч байхгүй).
export const metadata: Metadata = pageMetadata({
  title: mn.auth.loginTitle,
  description: mn.auth.loginSubtitle,
  path: "/login",
  noindex: true,
});

export default function LoginPage() {
  return (
    // AuthCard болон LoginForm хоёулаа useSearchParams ашигладаг тул Suspense хэрэгтэй.
    <Suspense fallback={<Skeleton className="h-96 w-full max-w-sm" />}>
      <AuthCard
        title={mn.auth.loginTitle}
        subtitle={mn.auth.loginSubtitle}
        footerPrompt={mn.auth.noAccount}
        footerLinkLabel={mn.auth.goRegister}
        footerHref="/register"
      >
        <LoginForm />
      </AuthCard>
    </Suspense>
  );
}
