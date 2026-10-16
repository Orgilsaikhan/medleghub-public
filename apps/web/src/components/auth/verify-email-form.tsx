"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation } from "@tanstack/react-query";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { useEffect, useRef, useState } from "react";
import { useForm } from "react-hook-form";
import { toast } from "sonner";

import { FormField } from "@/components/auth/form-field";
import { ResendCodeButton } from "@/components/auth/resend-code-button";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { resendVerification } from "@/lib/api/auth";
import { ApiError } from "@/lib/api/client";
import { useAuthRedirect } from "@/lib/hooks/use-auth-redirect";
import { useVerifyEmail } from "@/lib/hooks/use-auth";
import { mn } from "@/lib/i18n/mn";
import { codeSchema, type CodeValues } from "@/lib/validation/auth";

/**
 * Бүртгүүлсний дараа имэйлд ирсэн кодыг оруулна. `?resend=1` бол (нэвтрэх
 * оролдлогоос ирсэн) хуудас нээгдмэгц шинэ код илгээнэ — өмнөх кодын хугацаа
 * дууссан байж болно.
 */
export function VerifyEmailForm() {
  const params = useSearchParams();
  const email = params.get("email") ?? "";
  const { redirect } = useAuthRedirect();
  const verify = useVerifyEmail();
  // Бүртгэлийн хуудаснаас ирвэл код саяхан илгээгдсэн.
  const [sentAt, setSentAt] = useState<number | null>(() =>
    params.get("resend") === "1" ? null : Date.now(),
  );

  const resend = useMutation({
    mutationFn: () => resendVerification(email),
    onSuccess: () => {
      setSentAt(Date.now());
      toast.success(mn.auth.resent);
    },
    onError: (error) =>
      toast.error(error instanceof ApiError ? error.message : mn.common.somethingWrong),
  });

  const autoSent = useRef(false);
  useEffect(() => {
    if (autoSent.current || !email || params.get("resend") !== "1") return;
    autoSent.current = true;
    resend.mutate();
  }, [email, params, resend]);

  const form = useForm<CodeValues>({
    resolver: zodResolver(codeSchema),
    defaultValues: { code: "" },
  });

  if (!email) {
    return (
      <Alert>
        <AlertDescription>
          {mn.auth.verifyMissing}{" "}
          <Link href="/login" className="font-medium underline underline-offset-4">
            {mn.auth.goLogin}
          </Link>
        </AlertDescription>
      </Alert>
    );
  }

  const serverError =
    verify.error instanceof ApiError
      ? verify.error.message
      : verify.error
        ? mn.common.somethingWrong
        : null;

  return (
    <form
      onSubmit={form.handleSubmit((values) =>
        verify.mutate({ email, code: values.code }, { onSuccess: redirect }),
      )}
      noValidate
      className="space-y-4"
    >
      <p className="text-muted-foreground text-sm">{mn.auth.verifySubtitle(email)}</p>
      {serverError && (
        <Alert variant="destructive" className="bg-destructive/5">
          <AlertDescription>{serverError}</AlertDescription>
        </Alert>
      )}
      <CodeField error={form.formState.errors.code?.message} {...form.register("code")} />
      <Button type="submit" className="w-full" disabled={verify.isPending}>
        {verify.isPending ? mn.auth.submitting : mn.auth.verifySubmit}
      </Button>
      <div className="flex flex-wrap items-center justify-between gap-2">
        <p className="text-muted-foreground text-xs">{mn.auth.checkSpam}</p>
        <ResendCodeButton
          sentAt={sentAt}
          pending={resend.isPending}
          onResend={() => resend.mutate()}
        />
      </div>
    </form>
  );
}

/** Имэйлийн нэг удаагийн код — утсан дээр тоон гар, автоматаар бөглөх. */
export function CodeField({
  error,
  ...props
}: Omit<React.ComponentProps<typeof FormField>, "id" | "label"> & { error?: string }) {
  return (
    <FormField
      id="code"
      label={mn.auth.code}
      inputMode="numeric"
      autoComplete="one-time-code"
      maxLength={10}
      placeholder="123456"
      className="font-mono tracking-[0.3em]"
      error={error}
      {...props}
    />
  );
}
