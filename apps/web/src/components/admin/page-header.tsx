import { ChevronLeftIcon } from "lucide-react";
import Link from "next/link";
import type { ReactNode } from "react";

import { Button } from "@/components/ui/button";
import { mn } from "@/lib/i18n/mn";

interface AdminPageHeaderProps {
  title: string;
  description?: string;
  backHref?: string;
  action?: ReactNode;
}

export function AdminPageHeader({ title, description, backHref, action }: AdminPageHeaderProps) {
  return (
    <header className="mb-8">
      {backHref && (
        <Button asChild variant="ghost" size="sm" className="mb-2 -ml-2">
          <Link href={backHref}>
            <ChevronLeftIcon className="size-4" />
            {mn.admin.back}
          </Link>
        </Button>
      )}

      <div className="flex flex-wrap items-start justify-between gap-4">
        <div className="min-w-0">
          <h1 className="text-2xl font-bold tracking-tight">{title}</h1>
          {description && <p className="text-muted-foreground mt-1 text-sm">{description}</p>}
        </div>
        {action}
      </div>
    </header>
  );
}
