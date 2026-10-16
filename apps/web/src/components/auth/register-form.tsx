"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";

import { FormField } from "@/components/auth/form-field";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { ApiError } from "@/lib/api/client";
import { isSafeInternalPath, useAuthRedirect } from "@/lib/hooks/use-auth-redirect";
import { useIsHydrated } from "@/lib/hooks/use-hydrated";
import { useRegister } from "@/lib/hooks/use-auth";
import { mn } from "@/lib/i18n/mn";
import { readLocal, writeLocal } from "@/lib/local-storage";
import { registerSchema, type RegisterValues } from "@/lib/validation/auth";

/** Урилгын холбоосоор (`/register?ref=…`) ирээд өөр хуудас үзсэн ч код мартагдахгүй. */
const REFERRAL_KEY = "medleghub:referral-code";

/**
 * Бүртгэл. Яг насыг асуухгүй — «Би 16 нас хүрсэн» тэмдэглэгээ заавал; 16 хүрээгүй бол
 * бүртгүүлэхгүй. Имэйл баталгаажуулалт асаалттай бол кодын хуудас руу шилжинэ.
 *
 * Урилгын код заавал биш: `?ref=` эсвэл өмнө нь ирсэн холбоосоос бөглөгдөнө,
 * эс бөгөөс «Урилгын код байна уу?» товчоор нээнэ.
 */
export function RegisterForm() {
  const register = useRegister();
  const router = useRouter();
  const params = useSearchParams();
  const { redirect } = useAuthRedirect();
  const linkCode = params.get("ref")?.trim().slice(0, 64) ?? "";
  // Өмнө нь урилгын холбоосоор ирсэн бол — зөвхөн client дээр уншина (hydration таарна).
  const hydrated = useIsHydrated();
  const savedCode = hydrated && !linkCode ? readLocal(REFERRAL_KEY, "").slice(0, 64) : "";
  const [opened, setOpened] = useState(false);

  const form = useForm<RegisterValues>({
    resolver: zodResolver(registerSchema),
    defaultValues: {
      name: "",
      email: "",
      password: "",
      is_16_or_older: false,
      accept_terms: false,
      referral_code: linkCode,
    },
  });
  const errors = form.formState.errors;
  // Код бөглөгдсөн бол талбар нээлттэй — хэрэглэгч арилгасан ч алга болохгүй.
  const showReferral =
    opened || linkCode !== "" || savedCode !== "" || Boolean(errors.referral_code);

  useEffect(() => {
    if (linkCode) writeLocal(REFERRAL_KEY, linkCode);
  }, [linkCode]);

  useEffect(() => {
    if (savedCode && !form.getValues("referral_code")) form.setValue("referral_code", savedCode);
  }, [savedCode, form]);

  const onSubmit = form.handleSubmit((values) => {
    register.mutate(values, {
      onSuccess: (result) => {
        // Нэг төхөөрөмж дээр дараагийн бүртгэлд хуучин код бөглөгдөхгүй.
        writeLocal(REFERRAL_KEY, "");
        if (!result.verification_required) return redirect();
        const next = params.get("next");
        const query = new URLSearchParams({ email: result.email });
        if (isSafeInternalPath(next)) query.set("next", next);
        router.push(`/verify-email?${query}`);
      },
      onError: (error) => {
        // Сервер талын талбарын алдааг (жишээ нь давхардсан имэйл) тухайн талбар дээр харуулна.
        if (error instanceof ApiError && error.code === "EMAIL_TAKEN") {
          form.setError("email", { message: error.message });
        }
        if (error instanceof ApiError && error.code === "INVALID_REFERRAL_CODE") {
          form.setError("referral_code", { message: error.message }, { shouldFocus: true });
        }
      },
    });
  });

  const emailTaken = register.error instanceof ApiError && register.error.code === "EMAIL_TAKEN";
  const badReferral =
    register.error instanceof ApiError && register.error.code === "INVALID_REFERRAL_CODE";
  const serverError =
    emailTaken || badReferral
      ? null
      : register.error instanceof ApiError
        ? register.error.message
        : register.error
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
        id="name"
        label={mn.auth.name}
        autoComplete="name"
        placeholder="Бат"
        error={errors.name?.message}
        {...form.register("name")}
      />

      <div>
        <FormField
          id="email"
          type="email"
          label={mn.auth.email}
          autoComplete="email"
          placeholder="name@example.com"
          error={errors.email?.message}
          {...form.register("email")}
        />
        {emailTaken && (
          <Link
            href="/forgot-password"
            className="text-brand-link mt-1.5 inline-block text-xs font-medium underline-offset-4 hover:underline"
          >
            {mn.auth.emailTakenHint}
          </Link>
        )}
      </div>

      <FormField
        id="password"
        type="password"
        label={mn.auth.password}
        autoComplete="new-password"
        hint={mn.auth.passwordHint}
        error={errors.password?.message}
        {...form.register("password")}
      />

      {showReferral ? (
        <FormField
          id="referral_code"
          label={mn.auth.referralCode}
          autoComplete="off"
          autoCapitalize="characters"
          spellCheck={false}
          hint={mn.auth.referralHint}
          error={errors.referral_code?.message}
          {...form.register("referral_code")}
        />
      ) : (
        <Button
          type="button"
          variant="link"
          size="sm"
          className="h-auto px-0"
          onClick={() => {
            setOpened(true);
            // Товч алга болж талбар гарч ирнэ — фокусыг тийш шилжүүлнэ.
            setTimeout(() => form.setFocus("referral_code"), 0);
          }}
        >
          {mn.auth.referralToggle}
        </Button>
      )}

      <Checkbox
        id="is_16_or_older"
        error={errors.is_16_or_older?.message}
        {...form.register("is_16_or_older")}
      >
        {mn.auth.age16Confirm}
      </Checkbox>

      <Checkbox
        id="accept_terms"
        error={errors.accept_terms?.message}
        {...form.register("accept_terms")}
      >
        <Link
          href="/terms"
          target="_blank"
          className="text-brand-link underline underline-offset-4"
        >
          {mn.auth.termsLink}
        </Link>
        ,{" "}
        <Link
          href="/privacy"
          target="_blank"
          className="text-brand-link underline underline-offset-4"
        >
          {mn.auth.privacyLink}
        </Link>
        {mn.auth.acceptTermsSuffix}
      </Checkbox>

      <Button type="submit" className="w-full" disabled={register.isPending}>
        {register.isPending ? mn.auth.submitting : mn.auth.submitRegister}
      </Button>
    </form>
  );
}

function Checkbox({
  id,
  error,
  children,
  ...props
}: React.ComponentProps<"input"> & { id: string; error?: string }) {
  const errorId = `${id}-error`;
  return (
    <div className="space-y-1.5">
      <label htmlFor={id} className="flex items-start gap-2.5 text-sm leading-snug">
        <input
          id={id}
          type="checkbox"
          className="accent-primary mt-0.5 size-4 shrink-0"
          aria-invalid={error ? true : undefined}
          aria-describedby={error ? errorId : undefined}
          {...props}
        />
        <span>{children}</span>
      </label>
      {error && (
        <p id={errorId} role="alert" className="text-destructive text-xs">
          {error}
        </p>
      )}
    </div>
  );
}
