import { ArrowRightIcon } from "lucide-react";
import Link from "next/link";

import { Button } from "@/components/ui/button";
import { mn } from "@/lib/i18n/mn";

export function CtaSection() {
  return (
    <section className="py-16 lg:py-20">
      <div className="container-page">
        <div className="from-primary/10 rounded-2xl border bg-gradient-to-br via-transparent to-transparent px-6 py-12 text-center sm:px-12">
          <h2 className="text-2xl font-bold tracking-tight text-balance sm:text-3xl">
            {mn.home.ctaTitle}
          </h2>
          <p className="text-muted-foreground mx-auto mt-3 max-w-md text-pretty">
            {mn.home.ctaBody}
          </p>

          <div className="mt-8 flex flex-col justify-center gap-3 sm:flex-row">
            <Button asChild size="lg">
              <Link href="/register">
                {mn.home.ctaSecondary}
                <ArrowRightIcon className="size-4" />
              </Link>
            </Button>
            <Button asChild size="lg" variant="outline">
              <Link href="/courses">{mn.home.ctaPrimary}</Link>
            </Button>
          </div>
        </div>
      </div>
    </section>
  );
}
