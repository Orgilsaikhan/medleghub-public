"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation } from "@tanstack/react-query";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { toast } from "sonner";

import { FormField } from "@/components/auth/form-field";
import { ResendCodeButton } from "@/components/auth/resend-code-button";
import { CodeField } from "@/components/auth/verify-email-form";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { forgotPassword } from "@/lib/api/auth";
import { ApiError } from "@/lib/api/client";
import { useAuthRedirect } from "@/lib/hooks/use-auth-redirect";
import { useResetPassword } from "@/lib/hooks/use-auth";
import { mn } from "@/lib/i18n/mn";
import {
  forgotPasswordSchema,
  resetPasswordSchema,
  type ForgotPasswordValues,
  type ResetPasswordValues,
} from "@/lib/validation/auth";

function errorMessage(error: unknown): string | null {
  if (!error) return null;
  return error instanceof ApiError ? error.message : mn.common.somethingWrong;
}

/** Хоёр алхам: имэйлээ оруулж код авах → код, шинэ нууц үгээ оруулах. */
export function ForgotPasswordForm() {
  const [email, setEmail] = useState<string | null>(null);
  const [sentAt, setSentAt] = useState<number | null>(null);

  const send = useMutation({
    mutationFn: forgotPassword,
    onSuccess: (_, sentTo) => {
      setEmail(sentTo);
      setSentAt(Date.now());
    },
  });

  if (!email) {
    return <RequestStep pending={send.isPending} error={send.error} onSubmit={send.mutate} />;
  }
  return (
    <ResetStep
      email={email}
      sentAt={sentAt}
      resending={send.isPending}
      onResend={() =>
        send.mutate(email, {
          onSuccess: () => toast.success(mn.auth.resent),
          onError: (error) => toast.error(errorMessage(error)),
        })
      }
      onChangeEmail={() => setEmail(null)}
    />
  );
}

function RequestStep({
  pending,
  error,
  onSubmit,
}: {
  pending: boolean;
  error: unknown;
  onSubmit: (email: string) => void;
}) {
  const form = useForm<ForgotPasswordValues>({
    resolver: zodResolver(forgotPasswordSchema),
    defaultValues: { email: "" },
  });
  const serverError = errorMessage(error);

  return (
    <form
      onSubmit={form.handleSubmit((values) => onSubmit(values.email))}
      noValidate
      className="space-y-4"
    >
      {serverError && (
        <Alert variant="destructive" className="bg-destructive/5">
          <AlertDescription>{serverError}</AlertDescription>
        </Alert>
      )}
      <FormField
        id="email"
        type="email"
        label={mn.auth.email}
        autoComplete="email"
        placeholder="name@example.com"
        error={form.formState.errors.email?.message}
        {...form.register("email")}
      />
      <Button type="submit" className="w-full" disabled={pending}>
        {pending ? mn.auth.submitting : mn.auth.sendCode}
      </Button>
    </form>
  );
}

function ResetStep({
  email,
  sentAt,
  resending,
  onResend,
  onChangeEmail,
}: {
  email: string;
  sentAt: number | null;
  resending: boolean;
  onResend: () => void;
  onChangeEmail: () => void;
}) {
  const reset = useResetPassword();
  const { redirect } = useAuthRedirect();
  const form = useForm<ResetPasswordValues>({
    resolver: zodResolver(resetPasswordSchema),
    defaultValues: { code: "", new_password: "", confirm_password: "" },
  });
  const serverError = errorMessage(reset.error);

  return (
    <form
      onSubmit={form.handleSubmit((values) =>
        reset.mutate(
          { email, code: values.code, new_password: values.new_password },
          { onSuccess: redirect },
        ),
      )}
      noValidate
      className="space-y-4"
    >
      <p className="text-muted-foreground text-sm">{mn.auth.resetSubtitle(email)}</p>
      {serverError && (
        <Alert variant="destructive" className="bg-destructive/5">
          <AlertDescription>{serverError}</AlertDescription>
        </Alert>
      )}
      <CodeField error={form.formState.errors.code?.message} {...form.register("code")} />
      <FormField
        id="new_password"
        type="password"
        autoComplete="new-password"
        label={mn.settings.newPassword}
        hint={mn.auth.passwordHint}
        error={form.formState.errors.new_password?.message}
        {...form.register("new_password")}
      />
      <FormField
        id="confirm_password"
        type="password"
        autoComplete="new-password"
        label={mn.settings.confirmPassword}
        error={form.formState.errors.confirm_password?.message}
        {...form.register("confirm_password")}
      />
      <Button type="submit" className="w-full" disabled={reset.isPending}>
        {reset.isPending ? mn.auth.submitting : mn.auth.resetSubmit}
      </Button>
      <div className="flex flex-wrap items-center justify-between gap-2">
        <Button
          type="button"
          variant="link"
          size="sm"
          className="h-auto px-0"
          onClick={onChangeEmail}
        >
          {mn.auth.otherEmail}
        </Button>
        <ResendCodeButton sentAt={sentAt} pending={resending} onResend={onResend} />
      </div>
    </form>
  );
}
