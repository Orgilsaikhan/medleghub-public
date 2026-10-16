"use client";

import {
  BookOpenIcon,
  LayoutDashboardIcon,
  MegaphoneIcon,
  MessageSquareIcon,
  ReceiptIcon,
  SparklesIcon,
  TicketPercentIcon,
  UsersRoundIcon,
} from "lucide-react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import type { ReactNode } from "react";

import { mn } from "@/lib/i18n/mn";
import { cn } from "@/lib/utils";

const LINKS = [
  { href: "/admin", label: mn.admin.title, icon: LayoutDashboardIcon, exact: true },
  { href: "/admin/courses", label: mn.admin.courses, icon: BookOpenIcon, exact: false },
  { href: "/admin/feedback", label: mn.admin.feedback, icon: MessageSquareIcon, exact: false },
  { href: "/admin/community", label: mn.admin.community, icon: UsersRoundIcon, exact: false },
  { href: "/admin/billing", label: mn.admin.billing, icon: ReceiptIcon, exact: false },
  { href: "/admin/promo", label: mn.admin.promo, icon: TicketPercentIcon, exact: false },
  {
    href: "/admin/announcements",
    label: mn.admin.announcements,
    icon: MegaphoneIcon,
    exact: false,
  },
  { href: "/admin/live", label: mn.admin.live, icon: SparklesIcon, exact: false },
];

export function AdminShell({ children }: { children: ReactNode }) {
  const pathname = usePathname();

  return (
    <div className="container-wide py-8 lg:py-10">
      <nav aria-label={mn.admin.title} className="mb-8 flex flex-wrap gap-1 border-b pb-3">
        {LINKS.map((link) => {
          const active = link.exact ? pathname === link.href : pathname.startsWith(link.href);
          return (
            <Link
              key={link.href}
              href={link.href}
              aria-current={active ? "page" : undefined}
              className={cn(
                "flex items-center gap-2 rounded-md px-3 py-2 text-sm font-medium transition-colors",
                active
                  ? "bg-accent text-accent-foreground"
                  : "text-muted-foreground hover:text-foreground hover:bg-accent/50",
              )}
            >
              <link.icon className="size-4" aria-hidden />
              {link.label}
            </Link>
          );
        })}
      </nav>

      {children}
    </div>
  );
}
