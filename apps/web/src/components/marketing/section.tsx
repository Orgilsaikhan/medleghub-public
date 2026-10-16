import type { ReactNode } from "react";

import { cn } from "@/lib/utils";

interface SectionProps {
  id?: string;
  title: string;
  subtitle?: string;
  children: ReactNode;
  action?: ReactNode;
  className?: string;
  muted?: boolean;
}

/** Нүүр хуудасны бүх хэсэг ижил босоо зай, гарчгийн хэмнэлтэй байх. */
export function Section({
  id,
  title,
  subtitle,
  children,
  action,
  className,
  muted = false,
}: SectionProps) {
  return (
    <section id={id} className={cn("border-b py-16 lg:py-20", muted && "bg-muted/30", className)}>
      <div className="container-page">
        <div className="flex flex-wrap items-end justify-between gap-4">
          <div>
            <h2 className="text-2xl font-bold tracking-tight sm:text-3xl">{title}</h2>
            {subtitle && <p className="text-muted-foreground mt-2 text-base">{subtitle}</p>}
          </div>
          {action}
        </div>

        <div className="mt-10">{children}</div>
      </div>
    </section>
  );
}
