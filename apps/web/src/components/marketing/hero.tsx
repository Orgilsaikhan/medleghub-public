import { ArrowRightIcon } from "lucide-react";
import Link from "next/link";

import { HeroVisual } from "@/components/marketing/hero-visual";
import { Button } from "@/components/ui/button";
import { mn } from "@/lib/i18n/mn";

export function Hero() {
  return (
    <section className="relative isolate overflow-hidden border-b">
      {/* Зөөлөн өнгөт дэвсгэр — контентоос анхаарал сарниулахгүй. */}
      <div
        aria-hidden
        className="from-primary/8 pointer-events-none absolute inset-0 -z-10 bg-gradient-to-br via-transparent to-transparent"
      />
      {/* Бүдэг тор ба хоёр талын гэрэлтэлт — өргөн дэлгэцэд хоёр тал хоосон
          харагдахгүй. Гэрэл аажуухан хөвнө (хөдөлгөөн багасгавал хөдлөхгүй). */}
      <div aria-hidden className="hero-grid pointer-events-none absolute inset-0 -z-10" />
      <div
        aria-hidden
        className="bg-primary/15 motion-safe:animate-glow-drift pointer-events-none absolute -top-48 -left-48 -z-10 size-[38rem] rounded-full blur-3xl"
      />
      <div
        aria-hidden
        className="bg-primary/10 motion-safe:animate-glow-drift pointer-events-none absolute -right-56 -bottom-64 -z-10 size-[42rem] rounded-full blur-3xl [animation-direction:alternate-reverse]"
      />

      <div className="container-page relative grid items-center gap-12 py-16 lg:grid-cols-2 lg:py-24 xl:gap-20">
        <div>
          <h1 className="text-4xl leading-[1.1] font-bold tracking-tight text-balance sm:text-5xl lg:text-6xl xl:text-7xl">
            {mn.home.heroTitle}
          </h1>

          <p className="text-muted-foreground mt-6 max-w-xl text-lg leading-relaxed text-pretty">
            {mn.home.heroSubtitle}
          </p>

          <div className="mt-8 flex flex-col gap-3 sm:flex-row">
            <Button asChild size="lg">
              <Link href="/courses">
                {mn.home.ctaPrimary}
                <ArrowRightIcon className="size-4" />
              </Link>
            </Button>
            <Button asChild size="lg" variant="outline">
              <Link href="/register">{mn.home.ctaSecondary}</Link>
            </Button>
          </div>
        </div>

        {/* 3D кодын цонх — хулганыг дагаж хазайна (`hero-visual.tsx`). */}
        <HeroVisual />
      </div>
    </section>
  );
}
