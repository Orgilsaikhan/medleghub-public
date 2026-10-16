"use client";

import {
  CheckIcon,
  CopyIcon,
  CreditCardIcon,
  GiftIcon,
  LayoutDashboardIcon,
  LogOutIcon,
  MessageSquareIcon,
  SettingsIcon,
  ShieldIcon,
  UserIcon,
} from "lucide-react";
import Link from "next/link";
import { useState } from "react";
import { toast } from "sonner";

import { UserAvatar } from "@/components/common/user-avatar";
import { FeedbackDialog } from "@/components/feedback/feedback-dialog";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Skeleton } from "@/components/ui/skeleton";
import { formatDate } from "@/lib/format";
import { useCurrentUser, useLogout } from "@/lib/hooks/use-auth";
import { mn } from "@/lib/i18n/mn";

export function UserMenu() {
  const { user, isLoading, isAdmin } = useCurrentUser();
  const logout = useLogout();
  const [feedbackOpen, setFeedbackOpen] = useState(false);
  const [codeCopied, setCodeCopied] = useState(false);

  const copyReferralCode = async (code: string) => {
    try {
      await navigator.clipboard.writeText(code);
      setCodeCopied(true);
      toast.success(mn.profile.referral.menuCopied);
      setTimeout(() => setCodeCopied(false), 1500);
    } catch {
      toast.error(mn.profile.referral.copyFailed);
    }
  };

  if (isLoading) {
    return <Skeleton className="size-9 rounded-full" />;
  }

  if (!user) {
    // Утсан дээр эдгээр нь burger цэсэнд (`site-header.tsx`) — толгой нэг мөрөнд багтана.
    return (
      <div className="hidden items-center gap-2 md:flex">
        <Button asChild variant="outline" size="sm">
          <Link href="/login">{mn.nav.login}</Link>
        </Button>
        <Button asChild size="sm">
          <Link href="/register">{mn.nav.register}</Link>
        </Button>
      </div>
    );
  }

  return (
    <>
      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <Button variant="ghost" size="icon" className="rounded-full" aria-label={mn.nav.menu}>
            {/* Толгой хэсэг хоёр горимд хар — энд тод улбар шар үсэг уншигдана. */}
            <UserAvatar user={user} className="size-8" fallbackClassName="text-primary text-xs" />
          </Button>
        </DropdownMenuTrigger>

        <DropdownMenuContent
          align="end"
          className="w-56"
          // Санал хүсэлтийн цонх нээгдэхэд focus-ийг цэсний товч руу буцаахгүй —
          // эс бөгөөс цонхны focus-той мөргөлдөнө.
          onCloseAutoFocus={(event) => {
            if (feedbackOpen) event.preventDefault();
          }}
        >
          <DropdownMenuLabel className="font-normal">
            <p className="truncate text-sm font-medium">{user.name}</p>
            <p className="text-muted-foreground truncate text-xs">{user.email}</p>
            <p className="text-brand-link mt-1 truncate text-xs font-medium">
              {user.has_plan
                ? user.plan_expires_at
                  ? mn.billing.menuStandard(formatDate(user.plan_expires_at))
                  : mn.billing.standardName
                : mn.billing.menuFree}
            </p>
          </DropdownMenuLabel>
          <DropdownMenuSeparator />

          {/* Урилгын код — дарахад хуулна, цэс нээлттэй хэвээр. Админ урилгад оролцохгүй. */}
          {!isAdmin && user.referral_code && (
            <>
              <DropdownMenuItem
                aria-label={mn.profile.referral.menuCopy(user.referral_code)}
                onSelect={(event) => {
                  event.preventDefault();
                  void copyReferralCode(user.referral_code ?? "");
                }}
              >
                <GiftIcon className="size-4" />
                <span className="min-w-0 flex-1">
                  <span className="text-muted-foreground block text-xs">
                    {mn.profile.referral.menuLabel}
                  </span>
                  <span className="font-mono font-semibold tracking-wider">
                    {user.referral_code}
                  </span>
                </span>
                {codeCopied ? (
                  <CheckIcon className="size-4" />
                ) : (
                  <CopyIcon className="text-muted-foreground size-4" />
                )}
              </DropdownMenuItem>
              <DropdownMenuSeparator />
            </>
          )}

          <DropdownMenuItem asChild>
            <Link href="/dashboard">
              <LayoutDashboardIcon className="size-4" />
              {mn.nav.dashboard}
            </Link>
          </DropdownMenuItem>

          <DropdownMenuItem asChild>
            <Link href="/profile">
              <UserIcon className="size-4" />
              {mn.nav.profile}
            </Link>
          </DropdownMenuItem>

          <DropdownMenuItem asChild>
            <Link href="/settings">
              <SettingsIcon className="size-4" />
              {mn.nav.settings}
            </Link>
          </DropdownMenuItem>

          <DropdownMenuItem asChild>
            <Link href="/pricing">
              <CreditCardIcon className="size-4" />
              {mn.billing.title}
            </Link>
          </DropdownMenuItem>

          <DropdownMenuItem onSelect={() => setFeedbackOpen(true)}>
            <MessageSquareIcon className="size-4" />
            {mn.feedback.open}
          </DropdownMenuItem>

          {isAdmin && (
            <DropdownMenuItem asChild>
              <Link href="/admin">
                <ShieldIcon className="size-4" />
                {mn.nav.admin}
              </Link>
            </DropdownMenuItem>
          )}

          <DropdownMenuSeparator />
          <DropdownMenuItem onSelect={() => logout.mutate()} disabled={logout.isPending}>
            <LogOutIcon className="size-4" />
            {mn.nav.logout}
          </DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
      <FeedbackDialog open={feedbackOpen} onOpenChange={setFeedbackOpen} />
    </>
  );
}
