import Link from "next/link";

import { Button } from "@/components/ui/button";
import { mn } from "@/lib/i18n/mn";

export default function NotFound() {
  return (
    <main className="flex flex-1 items-center justify-center px-4 py-24">
      <div className="text-center">
        <p className="text-brand-link font-mono text-sm font-semibold">404</p>
        <h1 className="mt-3 text-3xl font-bold tracking-tight">{mn.common.notFound}</h1>
        <p className="text-muted-foreground mx-auto mt-3 max-w-sm text-pretty">
          {mn.common.notFoundBody}
        </p>
        <Button asChild className="mt-8">
          <Link href="/">{mn.common.goHome}</Link>
        </Button>
      </div>
    </main>
  );
}
