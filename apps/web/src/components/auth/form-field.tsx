import type { ComponentProps } from "react";

import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { cn } from "@/lib/utils";

interface FormFieldProps extends Omit<ComponentProps<typeof Input>, "id"> {
  id: string;
  label: string;
  error?: string;
  hint?: string;
}

/**
 * Шошго, оролт, алдаа, тайлбарыг нэг дор багцалсан талбар.
 *
 * `aria-invalid` болон `aria-describedby`-г зөв холбосноор дэлгэц уншигч
 * алдааг дуудна.
 */
export function FormField({ id, label, error, hint, className, ...props }: FormFieldProps) {
  const errorId = `${id}-error`;
  const hintId = `${id}-hint`;
  const describedBy = [error ? errorId : null, hint ? hintId : null].filter(Boolean).join(" ");

  return (
    <div className="space-y-2">
      <Label htmlFor={id}>{label}</Label>

      <Input
        id={id}
        aria-invalid={error ? true : undefined}
        aria-describedby={describedBy || undefined}
        className={cn(error && "border-destructive focus-visible:ring-destructive/30", className)}
        {...props}
      />

      {hint && !error && (
        <p id={hintId} className="text-muted-foreground text-xs">
          {hint}
        </p>
      )}

      {error && (
        <p id={errorId} role="alert" className="text-destructive text-xs">
          {error}
        </p>
      )}
    </div>
  );
}
