import { AlertCircleIcon, type LucideIcon } from "lucide-react";
import type { ReactNode } from "react";

import { Button } from "@/components/ui/button";
import { mn } from "@/lib/i18n/mn";
import { cn } from "@/lib/utils";

interface EmptyStateProps {
  icon?: LucideIcon;
  title: string;
  description?: string;
  action?: ReactNode;
  className?: string;
}

export function EmptyState({ icon: Icon, title, description, action, className }: EmptyStateProps) {
  return (
    <div
      className={cn(
        "flex flex-col items-center justify-center rounded-xl border border-dashed px-6 py-16 text-center",
        className,
      )}
    >
      {Icon && <Icon className="text-muted-foreground/60 mb-4 size-10" aria-hidden />}
      <p className="font-medium">{title}</p>
      {description && (
        <p className="text-muted-foreground mt-1.5 max-w-sm text-sm">{description}</p>
      )}
      {action && <div className="mt-6">{action}</div>}
    </div>
  );
}

interface ErrorStateProps {
  title?: string;
  description?: string;
  onRetry?: () => void;
  className?: string;
}

export function ErrorState({ title, description, onRetry, className }: ErrorStateProps) {
  return (
    <div
      role="alert"
      className={cn(
        "border-destructive/30 bg-destructive/5 flex flex-col items-center justify-center rounded-xl border px-6 py-12 text-center",
        className,
      )}
    >
      <AlertCircleIcon className="text-destructive mb-3 size-8" aria-hidden />
      <p className="font-medium">{title ?? mn.common.error}</p>
      <p className="text-muted-foreground mt-1.5 max-w-sm text-sm">
        {description ?? mn.common.somethingWrong}
      </p>
      {onRetry && (
        <Button variant="outline" size="sm" className="mt-6" onClick={onRetry}>
          {mn.common.retry}
        </Button>
      )}
    </div>
  );
}
