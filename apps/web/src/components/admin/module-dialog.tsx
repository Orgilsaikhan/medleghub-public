"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation } from "@tanstack/react-query";
import { useEffect } from "react";
import { useForm } from "react-hook-form";
import { toast } from "sonner";

import { FormField } from "@/components/auth/form-field";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { createModule, updateModule } from "@/lib/api/admin";
import { ApiError } from "@/lib/api/client";
import { mn } from "@/lib/i18n/mn";
import type { ModuleWithLessons } from "@/lib/types/api";
import { moduleSchema, type ModuleFormValues } from "@/lib/validation/admin";

interface ModuleDialogProps {
  courseId: string;
  /** `null` бол шинэ модул үүсгэнэ. */
  module: ModuleWithLessons | null;
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onSaved: () => void;
}

const EMPTY: ModuleFormValues = { title: "", description: "" };

export function ModuleDialog({
  courseId,
  module: target,
  open,
  onOpenChange,
  onSaved,
}: ModuleDialogProps) {
  const form = useForm<ModuleFormValues>({
    resolver: zodResolver(moduleSchema),
    defaultValues: EMPTY,
  });

  const { reset } = form;

  // Цонх нээгдэх бүрт засварлах модулын утгыг ачаална.
  useEffect(() => {
    if (!open) return;
    reset(target ? { title: target.title, description: target.description } : EMPTY);
  }, [open, target, reset]);

  const mutation = useMutation({
    mutationFn: (values: ModuleFormValues) =>
      target ? updateModule(target.id, values) : createModule(courseId, values),
    onSuccess: () => {
      toast.success(mn.admin.saved);
      onOpenChange(false);
      onSaved();
    },
    onError: (error) =>
      toast.error(error instanceof ApiError ? error.message : mn.common.somethingWrong),
  });

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>{target ? mn.admin.modules : mn.admin.newModule}</DialogTitle>
        </DialogHeader>

        <form
          id="module-form"
          onSubmit={form.handleSubmit((values) => mutation.mutate(values))}
          noValidate
          className="space-y-4"
        >
          <FormField
            id="module-title"
            label={mn.admin.fields.title}
            error={form.formState.errors.title?.message}
            {...form.register("title")}
          />

          <div className="space-y-2">
            <Label htmlFor="module-description">{mn.admin.fields.description}</Label>
            <Textarea id="module-description" rows={3} {...form.register("description")} />
          </div>
        </form>

        <DialogFooter>
          <Button variant="outline" onClick={() => onOpenChange(false)}>
            {mn.admin.cancel}
          </Button>
          <Button type="submit" form="module-form" disabled={mutation.isPending}>
            {mutation.isPending ? mn.admin.saving : mn.admin.save}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
