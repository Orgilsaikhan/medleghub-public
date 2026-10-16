import { Suspense } from "react";

import { RedirectIfAuthenticated } from "@/components/auth/redirect-if-authenticated";
import { ThemeToggle } from "@/components/layout/theme-toggle";

export default function AuthLayout({ children }: LayoutProps<"/">) {
  return (
    <main className="relative flex flex-1 items-center justify-center px-4 py-12">
      <div className="absolute top-4 right-4">
        <ThemeToggle />
      </div>
      <Suspense>
        <RedirectIfAuthenticated>{children}</RedirectIfAuthenticated>
      </Suspense>
    </main>
  );
}
