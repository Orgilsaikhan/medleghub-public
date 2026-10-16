"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { useForm } from "react-hook-form";

import { FormField } from "@/components/auth/form-field";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { ApiError } from "@/lib/api/client";
import { isSafeInternalPath, useAuthRedirect } from "@/lib/hooks/use-auth-redirect";
import { useLogin } from "@/lib/hooks/use-auth";
import { mn } from "@/lib/i18n/mn";
import { loginSchema, type LoginValues } from "@/lib/validation/auth";

export function LoginForm() {
  const login = useLogin();
  const router = useRouter();
  const params = useSearchParams();
  const { redirect } = useAuthRedirect();

  const form = useForm<LoginValues>({
    resolver: zodResolver(loginSchema),
    defaultValues: { email: "", password: "" },
  });

  const onSubmit = form.handleSubmit((values) => {
    login.mutate(values, {
      onSuccess: redirect,
      onError: (error) => {
        // Имэйлээ баталгаажуулаагүй — шинэ код илгээж, кодын хуудас руу.
        if (error instanceof ApiError && error.code === "EMAIL_NOT_VERIFIED") {
          const query = new URLSearchParams({ email: values.email.trim(), resend: "1" });
          const next = params.get("next");
          if (isSafeInternalPath(next)) query.set("next", next);
          router.push(`/verify-email?${query}`);
        }
      },
    });
  });

  const unverified = login.error instanceof ApiError && login.error.code === "EMAIL_NOT_VERIFIED";
  const serverError = unverified
    ? null
    : login.error instanceof ApiError
      ? login.error.message
      : login.error
        ? mn.common.somethingWrong
        : null;

  return (
    <form onSubmit={onSubmit} noValidate className="space-y-4">
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

      <FormField
        id="password"
        type="password"
        label={mn.auth.password}
        autoComplete="current-password"
        error={form.formState.errors.password?.message}
        {...form.register("password")}
      />

      <div className="-mt-2 text-right">
        <Link
          href="/forgot-password"
          className="text-muted-foreground hover:text-foreground text-xs underline-offset-4 hover:underline"
        >
          {mn.auth.forgotLink}
        </Link>
      </div>

      <Button type="submit" className="w-full" disabled={login.isPending}>
        {login.isPending ? mn.auth.submitting : mn.auth.submitLogin}
      </Button>
    </form>
  );
}
