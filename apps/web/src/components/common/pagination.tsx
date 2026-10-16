import { ChevronLeftIcon, ChevronRightIcon } from "lucide-react";
import Link from "next/link";

import { Button } from "@/components/ui/button";
import { mn } from "@/lib/i18n/mn";

interface PaginationProps {
  page: number;
  totalPages: number;
  /** Хуудасны дугаарыг өгөөд href буцаана. */
  buildHref: (page: number) => string;
}

export function Pagination({ page, totalPages, buildHref }: PaginationProps) {
  if (totalPages <= 1) return null;

  const hasPrevious = page > 1;
  const hasNext = page < totalPages;

  return (
    <nav
      aria-label={mn.common.page(page, totalPages)}
      className="flex items-center justify-center gap-4"
    >
      <Button asChild={hasPrevious} variant="outline" size="sm" disabled={!hasPrevious}>
        {hasPrevious ? (
          <Link href={buildHref(page - 1)} rel="prev">
            <ChevronLeftIcon className="size-4" />
            {mn.common.previous}
          </Link>
        ) : (
          <span>
            <ChevronLeftIcon className="size-4" />
            {mn.common.previous}
          </span>
        )}
      </Button>

      <span className="text-muted-foreground text-sm tabular-nums">
        {mn.common.page(page, totalPages)}
      </span>

      <Button asChild={hasNext} variant="outline" size="sm" disabled={!hasNext}>
        {hasNext ? (
          <Link href={buildHref(page + 1)} rel="next">
            {mn.common.next}
            <ChevronRightIcon className="size-4" />
          </Link>
        ) : (
          <span>
            {mn.common.next}
            <ChevronRightIcon className="size-4" />
          </span>
        )}
      </Button>
    </nav>
  );
}
