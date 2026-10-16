"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useRef, useState } from "react";
import { useForm } from "react-hook-form";
import { toast } from "sonner";

import { FormField } from "@/components/auth/form-field";
import { CodeField } from "@/components/auth/verify-email-form";
import { UserAvatar } from "@/components/common/user-avatar";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Switch } from "@/components/ui/switch";
import {
  cancelDeletion,
  confirmEmailChange,
  requestEmailChange,
  scheduleDeletion,
  updateAccount,
} from "@/lib/api/account";
import { changePassword } from "@/lib/api/auth";
import { ApiError } from "@/lib/api/client";
import { deleteAvatar, uploadAvatar } from "@/lib/api/profile";
import { useCurrentUser } from "@/lib/hooks/use-auth";
import { useEditorLayout } from "@/lib/hooks/use-editor-layout";
import { useNow } from "@/lib/hooks/use-now";
import { mn } from "@/lib/i18n/mn";
import { queryKeys } from "@/lib/query-keys";
import type { EditorLayout, User } from "@/lib/types/api";
import { cn } from "@/lib/utils";
import {
  changeEmailSchema,
  changePasswordSchema,
  codeSchema,
  deleteAccountSchema,
  nameSchema,
  type ChangeEmailValues,
  type ChangePasswordValues,
  type CodeValues,
  type DeleteAccountValues,
  type NameValues,
} from "@/lib/validation/auth";

/** Сервертэй ижил дүрэм (`avatar_service`) — хэрэглэгчид хүлээлгүй хариу өгөхөд. */
const MAX_AVATAR_BYTES = 5_000_000;
const AVATAR_TYPES = ["image/png", "image/jpeg", "image/webp", "image/gif"];

export function SettingsView() {
  const { user } = useCurrentUser();
  if (!user) return null;

  return (
    <div className="max-w-2xl space-y-8">
      <div>
        <h1 className="text-2xl font-bold tracking-tight sm:text-3xl">{mn.settings.title}</h1>
        <p className="text-muted-foreground mt-1.5 text-sm">{mn.settings.subtitle}</p>
      </div>
      <AvatarSettings user={user} />
      <NameSettings user={user} />
      <EmailSettings user={user} />
      <PasswordSettings />
      <PrivacySettings user={user} />
      <EditorLayoutSettings />
      <MotivationSettings user={user} />
      <DeleteAccountSettings user={user} />
    </div>
  );
}

/** Сервер буцаасан шинэ хэрэглэгчийг толгойн цэс, профайлд шууд тусгана. */
function useUserSaved() {
  const queryClient = useQueryClient();
  return (updated: User) => {
    queryClient.setQueryData(queryKeys.currentUser, updated);
    void queryClient.invalidateQueries({ queryKey: queryKeys.me.profile });
  };
}

function toastError(error: unknown) {
  toast.error(error instanceof ApiError ? error.message : mn.common.somethingWrong);
}

function NameSettings({ user }: { user: User }) {
  const saved = useUserSaved();
  const form = useForm<NameValues>({
    resolver: zodResolver(nameSchema),
    defaultValues: { name: user.name },
  });
  const mutation = useMutation({
    mutationFn: (values: NameValues) => updateAccount({ name: values.name }),
    onSuccess: (updated) => {
      saved(updated);
      form.reset({ name: updated.name });
      toast.success(mn.settings.nameSaved);
    },
    onError: toastError,
  });

  return (
    <Panel id="name-heading" title={mn.settings.nameTitle} hint={mn.settings.nameHint}>
      <form
        onSubmit={form.handleSubmit((values) => mutation.mutate(values))}
        noValidate
        className="flex flex-col gap-3 sm:flex-row sm:items-start"
      >
        <div className="flex-1">
          <FormField
            id="account-name"
            label={mn.auth.name}
            autoComplete="name"
            error={form.formState.errors.name?.message}
            {...form.register("name")}
          />
        </div>
        <Button
          type="submit"
          className="sm:mt-[1.375rem]"
          disabled={mutation.isPending || !form.formState.isDirty}
        >
          {mutation.isPending ? mn.auth.submitting : mn.settings.save}
        </Button>
      </form>
    </Panel>
  );
}

/** Нууц үгээ шалгуулж шинэ хаяг руу код илгээнэ → кодоо оруулна. */
function EmailSettings({ user }: { user: User }) {
  const saved = useUserSaved();
  const [pending, setPending] = useState<string | null>(null);

  const requestForm = useForm<ChangeEmailValues>({
    resolver: zodResolver(changeEmailSchema),
    defaultValues: { new_email: "", password: "" },
  });
  const codeForm = useForm<CodeValues>({
    resolver: zodResolver(codeSchema),
    defaultValues: { code: "" },
  });

  const request = useMutation({
    mutationFn: requestEmailChange,
    onSuccess: (result, input) => {
      requestForm.reset();
      if (result.verification_required) {
        setPending(input.new_email.trim().toLowerCase());
      } else {
        saved(result.user);
        toast.success(mn.settings.emailChanged);
      }
    },
    onError: (error) => {
      if (error instanceof ApiError && error.code === "WRONG_PASSWORD") {
        requestForm.setError("password", { message: error.message });
      } else if (error instanceof ApiError && ["EMAIL_TAKEN", "SAME_EMAIL"].includes(error.code)) {
        requestForm.setError("new_email", { message: error.message });
      } else toastError(error);
    },
  });

  const confirm = useMutation({
    mutationFn: (values: CodeValues) => confirmEmailChange(values.code),
    onSuccess: (updated) => {
      saved(updated);
      setPending(null);
      codeForm.reset();
      toast.success(mn.settings.emailChanged);
    },
    onError: (error) => {
      if (error instanceof ApiError && error.code === "INVALID_CODE") {
        codeForm.setError("code", { message: error.message });
      } else toastError(error);
    },
  });

  return (
    <Panel
      id="email-heading"
      title={mn.settings.emailTitle}
      hint={mn.settings.emailHint(user.email)}
    >
      {pending ? (
        <form
          onSubmit={codeForm.handleSubmit((values) => confirm.mutate(values))}
          noValidate
          className="space-y-4"
        >
          <p className="text-muted-foreground text-sm">{mn.settings.emailCodeHint(pending)}</p>
          <CodeField
            error={codeForm.formState.errors.code?.message}
            {...codeForm.register("code")}
          />
          <div className="flex gap-2">
            <Button type="submit" disabled={confirm.isPending}>
              {confirm.isPending ? mn.auth.submitting : mn.settings.emailConfirm}
            </Button>
            <Button type="button" variant="outline" onClick={() => setPending(null)}>
              {mn.settings.cancel}
            </Button>
          </div>
        </form>
      ) : (
        <form
          onSubmit={requestForm.handleSubmit((values) => request.mutate(values))}
          noValidate
          className="space-y-4"
        >
          <FormField
            id="new_email"
            type="email"
            autoComplete="email"
            label={mn.settings.newEmail}
            error={requestForm.formState.errors.new_email?.message}
            {...requestForm.register("new_email")}
          />
          <FormField
            id="email-password"
            type="password"
            autoComplete="current-password"
            label={mn.auth.password}
            error={requestForm.formState.errors.password?.message}
            {...requestForm.register("password")}
          />
          <Button type="submit" disabled={request.isPending}>
            {request.isPending ? mn.auth.submitting : mn.settings.emailSubmit}
          </Button>
        </form>
      )}
    </Panel>
  );
}

function PrivacySettings({ user }: { user: User }) {
  const saved = useUserSaved();
  const mutation = useMutation({
    mutationFn: (hidden: boolean) => updateAccount({ profile_hidden: hidden }),
    onSuccess: (updated) => {
      saved(updated);
      toast.success(
        updated.profile_hidden ? mn.settings.profileHidden : mn.settings.profileVisible,
      );
    },
    onError: toastError,
  });

  return (
    <Panel id="privacy-heading" title={mn.settings.privacyTitle} hint={mn.settings.privacyHint}>
      <div className="flex items-start justify-between gap-4">
        <div>
          <label htmlFor="profile-hidden" className="text-sm font-medium">
            {mn.settings.hideProfile}
          </label>
          <p id="profile-hidden-hint" className="text-muted-foreground mt-1 text-sm">
            {mn.settings.hideProfileHint}
          </p>
        </div>
        <Switch
          id="profile-hidden"
          aria-describedby="profile-hidden-hint"
          checked={user.profile_hidden}
          disabled={mutation.isPending}
          onCheckedChange={(checked) => mutation.mutate(checked)}
        />
      </div>
    </Panel>
  );
}

// Бараан горимд `destructive` товчны дэвсгэрийг бараан болгож текстийн ялгарлыг (4.5:1) хангана.
const DESTRUCTIVE_CONTRAST = "dark:bg-destructive/10 dark:hover:bg-destructive/20";

/** Засварлагчийн зүүн/баруун (шинэ) эсвэл дээр/доор (хуучин) байрлалын жижиг зураг. */
function LayoutSketch({ layout }: { layout: EditorLayout }) {
  const code = "bg-foreground/70 rounded-[2px]";
  const text = "bg-muted-foreground/40 rounded-[2px]";
  return (
    <span
      aria-hidden
      className={cn(
        "border-border grid h-10 w-14 shrink-0 gap-0.5 rounded border p-1",
        layout === "new" ? "grid-cols-2" : "grid-rows-2",
      )}
    >
      <span className={layout === "new" ? code : text} />
      <span className={layout === "new" ? text : code} />
    </span>
  );
}

/** Хичээлийн засварлагчийн байрлал — React хичээлийнх шиг (шинэ) эсвэл хуучин. */
function EditorLayoutSettings() {
  const { layout, setLayout, saving } = useEditorLayout();
  const options = [
    { value: "new", label: mn.settings.editorLayoutNew, hint: mn.settings.editorLayoutNewHint },
    {
      value: "legacy",
      label: mn.settings.editorLayoutLegacy,
      hint: mn.settings.editorLayoutLegacyHint,
    },
  ] as const;

  return (
    <Panel
      id="editor-layout-heading"
      title={mn.settings.editorLayoutTitle}
      hint={mn.settings.editorLayoutHint}
    >
      <fieldset className="grid gap-3 sm:grid-cols-2" disabled={saving}>
        <legend className="sr-only">{mn.settings.editorLayoutTitle}</legend>
        {options.map((option) => (
          <label
            key={option.value}
            className={cn(
              "flex cursor-pointer items-start gap-3 rounded-lg border p-3 text-sm",
              "has-[:focus-visible]:ring-ring/50 has-[:focus-visible]:ring-[3px]",
              layout === option.value && "border-primary bg-accent",
            )}
          >
            <input
              type="radio"
              name="editor-layout"
              value={option.value}
              checked={layout === option.value}
              onChange={() => {
                setLayout(option.value);
                toast.success(mn.settings.editorLayoutSaved);
              }}
              className="accent-primary mt-0.5 size-4 shrink-0"
            />
            <span className="min-w-0 flex-1">
              <span className="block font-medium">{option.label}</span>
              <span className="text-muted-foreground mt-0.5 block text-xs">{option.hint}</span>
            </span>
            <LayoutSketch layout={option.value} />
          </label>
        ))}
      </fieldset>
    </Panel>
  );
}

/** Дасгалын тестэд 3 удаа дараалан унавал урам өгөх үг харуулах эсэх. */
function MotivationSettings({ user }: { user: User }) {
  const saved = useUserSaved();
  const mutation = useMutation({
    mutationFn: (show: boolean) => updateAccount({ show_motivation: show }),
    onSuccess: (updated) => {
      saved(updated);
      toast.success(updated.show_motivation ? mn.settings.motivationOn : mn.settings.motivationOff);
    },
    onError: toastError,
  });

  return (
    <Panel
      id="motivation-heading"
      title={mn.settings.motivationTitle}
      hint={mn.settings.motivationHint}
    >
      <div className="flex items-center justify-between gap-4">
        <label htmlFor="show-motivation" className="text-sm font-medium">
          {mn.settings.showMotivation}
        </label>
        <Switch
          id="show-motivation"
          checked={user.show_motivation}
          disabled={mutation.isPending}
          onCheckedChange={(checked) => mutation.mutate(checked)}
        />
      </div>
    </Panel>
  );
}

/** «ЦЦ:ММ:СС» — 2 цаг хүртэлх хугацаа. */
function formatCountdown(ms: number): string {
  const total = Math.max(0, Math.ceil(ms / 1000));
  const parts = [Math.floor(total / 3600), Math.floor((total % 3600) / 60), total % 60];
  return parts.map((part) => String(part).padStart(2, "0")).join(":");
}

/**
 * Бүртгэл устгах — нууц үгээр баталгаажуулж 2 цагийн дараа устгахаар товлоно.
 * Тэр хүртэл тоолуур харуулж, цуцлах боломж өгнө. Устгалыг сервер хийнэ.
 */
function DeleteAccountSettings({ user }: { user: User }) {
  const saved = useUserSaved();
  const [confirming, setConfirming] = useState<string | null>(null);
  const scheduledAt = user.deletion_scheduled_at ? Date.parse(user.deletion_scheduled_at) : null;
  const now = useNow(scheduledAt !== null);

  const form = useForm<DeleteAccountValues>({
    resolver: zodResolver(deleteAccountSchema),
    defaultValues: { password: "" },
  });

  const schedule = useMutation({
    mutationFn: scheduleDeletion,
    onSuccess: (updated) => {
      setConfirming(null);
      form.reset();
      saved(updated);
      toast.success(mn.settings.deleteScheduled);
    },
    onError: (error) => {
      setConfirming(null);
      if (error instanceof ApiError && error.code === "WRONG_PASSWORD") {
        form.setError("password", { message: error.message });
      } else toastError(error);
    },
  });

  const cancel = useMutation({
    mutationFn: cancelDeletion,
    onSuccess: (updated) => {
      saved(updated);
      toast.success(mn.settings.deleteCancelled);
    },
    onError: toastError,
  });

  return (
    <section
      aria-labelledby="delete-heading"
      className="border-destructive/40 bg-card rounded-xl border p-6"
    >
      <h2 id="delete-heading" className="text-destructive font-semibold">
        {mn.settings.deleteTitle}
      </h2>
      <p className="text-muted-foreground mt-1 text-sm">{mn.settings.deleteHint}</p>

      <div className="mt-5">
        {scheduledAt !== null ? (
          <div className="flex flex-wrap items-center justify-between gap-4">
            <div role="timer" aria-live="off">
              <p className="text-muted-foreground text-sm">{mn.settings.deleteCountdown}</p>
              <p className="text-destructive font-mono text-3xl font-bold tabular-nums">
                {scheduledAt > now ? formatCountdown(scheduledAt - now) : "00:00:00"}
              </p>
              {scheduledAt <= now && (
                <p className="text-muted-foreground text-sm">{mn.settings.deleteCountdownDone}</p>
              )}
            </div>
            <Button
              variant="outline"
              disabled={cancel.isPending || scheduledAt <= now}
              onClick={() => cancel.mutate()}
            >
              {mn.settings.deleteCancel}
            </Button>
          </div>
        ) : (
          <form
            onSubmit={form.handleSubmit((values) => setConfirming(values.password))}
            noValidate
            className="space-y-4"
          >
            <FormField
              id="delete-password"
              type="password"
              autoComplete="current-password"
              label={mn.settings.deletePassword}
              error={form.formState.errors.password?.message}
              {...form.register("password")}
            />
            <Button
              type="submit"
              variant="destructive"
              className={DESTRUCTIVE_CONTRAST}
              disabled={schedule.isPending}
            >
              {mn.settings.deleteSubmit}
            </Button>
          </form>
        )}
      </div>

      <Dialog open={confirming !== null} onOpenChange={(open) => !open && setConfirming(null)}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>{mn.settings.deleteConfirmTitle}</DialogTitle>
            <DialogDescription>{mn.settings.deleteConfirmBody}</DialogDescription>
          </DialogHeader>
          <DialogFooter>
            <Button variant="outline" onClick={() => setConfirming(null)}>
              {mn.settings.cancel}
            </Button>
            <Button
              variant="destructive"
              className={DESTRUCTIVE_CONTRAST}
              disabled={schedule.isPending}
              onClick={() => confirming && schedule.mutate(confirming)}
            >
              {schedule.isPending ? mn.auth.submitting : mn.settings.deleteConfirm}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </section>
  );
}

function Panel({
  id,
  title,
  hint,
  children,
}: {
  id: string;
  title: string;
  hint: string;
  children: React.ReactNode;
}) {
  return (
    <section aria-labelledby={id} className="bg-card rounded-xl border p-6">
      <h2 id={id} className="font-semibold">
        {title}
      </h2>
      <p className="text-muted-foreground mt-1 text-sm">{hint}</p>
      <div className="mt-5">{children}</div>
    </section>
  );
}

function AvatarSettings({ user }: { user: User }) {
  const queryClient = useQueryClient();
  const input = useRef<HTMLInputElement>(null);

  const onSaved = (updated: User, message: string) => {
    // Толгойн цэс, профайл хоёулаа шинэ зургийг шууд харуулна.
    queryClient.setQueryData(queryKeys.currentUser, updated);
    void queryClient.invalidateQueries({ queryKey: queryKeys.me.profile });
    toast.success(message);
  };
  const onError = (error: unknown) =>
    toast.error(error instanceof ApiError ? error.message : mn.common.somethingWrong);

  const upload = useMutation({
    mutationFn: uploadAvatar,
    onSuccess: (updated) => onSaved(updated, mn.settings.avatarSaved),
    onError,
  });
  const remove = useMutation({
    mutationFn: deleteAvatar,
    onSuccess: (updated) => onSaved(updated, mn.settings.avatarRemoved),
    onError,
  });
  const busy = upload.isPending || remove.isPending;

  const onFile = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    event.target.value = ""; // Ижил файлыг дахин сонгож болохоор.
    if (!file) return;
    if (!AVATAR_TYPES.includes(file.type)) return void toast.error(mn.settings.avatarWrongType);
    if (file.size > MAX_AVATAR_BYTES) return void toast.error(mn.settings.avatarTooLarge);
    upload.mutate(file);
  };

  return (
    <Panel id="avatar-heading" title={mn.settings.avatarTitle} hint={mn.settings.avatarHint}>
      <div className="flex flex-wrap items-center gap-5">
        <UserAvatar user={user} className="size-20" fallbackClassName="text-xl" />
        <div className="flex flex-wrap gap-2">
          <input
            ref={input}
            id="avatar-file"
            type="file"
            accept={AVATAR_TYPES.join(",")}
            className="sr-only"
            tabIndex={-1}
            aria-hidden
            onChange={onFile}
          />
          <Button type="button" disabled={busy} onClick={() => input.current?.click()}>
            {upload.isPending
              ? mn.settings.avatarUploading
              : user.avatar_key
                ? mn.settings.avatarChange
                : mn.settings.avatarUpload}
          </Button>
          {user.avatar_key && (
            <Button type="button" variant="outline" disabled={busy} onClick={() => remove.mutate()}>
              {mn.settings.avatarRemove}
            </Button>
          )}
        </div>
      </div>
    </Panel>
  );
}

function PasswordSettings() {
  const form = useForm<ChangePasswordValues>({
    resolver: zodResolver(changePasswordSchema),
    defaultValues: { current_password: "", new_password: "", confirm_password: "" },
  });

  const mutation = useMutation({
    mutationFn: (values: ChangePasswordValues) =>
      changePassword({
        current_password: values.current_password,
        new_password: values.new_password,
      }),
    onSuccess: () => {
      form.reset();
      toast.success(mn.settings.passwordChanged);
    },
    onError: (error) => {
      if (error instanceof ApiError && error.code === "WRONG_PASSWORD") {
        form.setError("current_password", { message: error.message });
      } else if (error instanceof ApiError && error.code === "SAME_PASSWORD") {
        form.setError("new_password", { message: error.message });
      }
    },
  });

  const fieldHandled =
    mutation.error instanceof ApiError &&
    ["WRONG_PASSWORD", "SAME_PASSWORD"].includes(mutation.error.code);
  const serverError =
    mutation.error && !fieldHandled
      ? mutation.error instanceof ApiError
        ? mutation.error.message
        : mn.common.somethingWrong
      : null;

  return (
    <Panel id="password-heading" title={mn.settings.passwordTitle} hint={mn.settings.passwordHint}>
      <form
        onSubmit={form.handleSubmit((values) => mutation.mutate(values))}
        noValidate
        className="space-y-4"
      >
        {serverError && (
          <Alert variant="destructive" className="bg-destructive/5">
            <AlertDescription>{serverError}</AlertDescription>
          </Alert>
        )}
        <FormField
          id="current_password"
          type="password"
          autoComplete="current-password"
          label={mn.settings.currentPassword}
          error={form.formState.errors.current_password?.message}
          {...form.register("current_password")}
        />
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
        <Button type="submit" disabled={mutation.isPending}>
          {mutation.isPending ? mn.auth.submitting : mn.settings.passwordSubmit}
        </Button>
      </form>
    </Panel>
  );
}
