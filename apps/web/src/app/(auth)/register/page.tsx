import type { Metadata } from "next";
import { Suspense } from "react";

import { AuthCard } from "@/components/auth/auth-card";
import { RegisterForm } from "@/components/auth/register-form";
import { Skeleton } from "@/components/ui/skeleton";
import { mn } from "@/lib/i18n/mn";
import { pageMetadata } from "@/lib/seo";

// Маягтын хуудас — хайлтын үр дүнд гаргахгүй (sitemap-д ч байхгүй).
export const metadata: Metadata = pageMetadata({
  title: mn.auth.registerTitle,
  description: mn.auth.registerSubtitle,
  path: "/register",
  noindex: true,
});

export default function RegisterPage() {
  return (
    // AuthCard болон RegisterForm хоёулаа useSearchParams ашигладаг тул Suspense хэрэгтэй.
    <Suspense fallback={<Skeleton className="h-[26rem] w-full max-w-sm" />}>
      <AuthCard
        title={mn.auth.registerTitle}
        subtitle={mn.auth.registerSubtitle}
        footerPrompt={mn.auth.hasAccount}
        footerLinkLabel={mn.auth.goLogin}
        footerHref="/login"
      >
        <RegisterForm />
      </AuthCard>
    </Suspense>
  );
}
