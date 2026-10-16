"use client";

import { ChevronLeftIcon, ChevronRightIcon } from "lucide-react";
import Link from "next/link";
import type { ReactNode } from "react";

import { Button } from "@/components/ui/button";
import { mn } from "@/lib/i18n/mn";
import type { LessonLink } from "@/lib/types/api";

interface LessonNavProps {
  courseSlug: string;
  previous: LessonLink | null;
  next: LessonLink | null;
  /** Голд байрлах үйлдэл — ихэвчлэн «Хичээл дууссан» товч. */
  center?: ReactNode;
}

export function LessonNav({ courseSlug, previous, next, center }: LessonNavProps) {
  return (
    <div className="flex flex-wrap items-center justify-between gap-3">
      <NavButton
        href={previous ? `/learn/${courseSlug}/${previous.slug}` : null}
        label={mn.learn.previousLesson}
        direction="previous"
      />

      {/* Жижиг дэлгэц дээр гол үйлдэл нь бүтэн мөр эзэлж, эхэнд харагдана. */}
      {center && <div className="order-first w-full sm:order-none sm:w-auto">{center}</div>}

      <NavButton
        href={next ? `/learn/${courseSlug}/${next.slug}` : null}
        label={mn.learn.nextLesson}
        direction="next"
      />
    </div>
  );
}

function NavButton({
  href,
  label,
  direction,
}: {
  href: string | null;
  label: string;
  direction: "previous" | "next";
}) {
  // Байхгүй хөрш дээр зай эзлүүлж, өмнөх/дараах товч байрандаа үлдэнэ.
  if (!href) return <span className="w-px" aria-hidden />;

  const icon =
    direction === "previous" ? (
      <ChevronLeftIcon className="size-4 shrink-0" />
    ) : (
      <ChevronRightIcon className="size-4 shrink-0" />
    );

  return (
    <Button asChild variant="outline" size="sm">
      <Link href={href} rel={direction === "previous" ? "prev" : "next"}>
        {direction === "previous" && icon}
        <span className="truncate">{label}</span>
        {direction === "next" && icon}
      </Link>
    </Button>
  );
}
