import type { Metadata } from "next";

import { AnnouncementPopup } from "@/components/announcements/announcement-popup";
import { SiteFooter } from "@/components/layout/site-footer";
import { SiteHeader } from "@/components/layout/site-header";

// Нэвтэрсэн хэрэглэгчийн хэсэг (самбар, профайл, тохиргоо, төлбөр) — хайлтад
// гаргахгүй. `robots.txt` ч эдгээрийг хаадаг.
export const metadata: Metadata = {
  robots: { index: false, follow: false },
};

export default function AppLayout({ children }: LayoutProps<"/">) {
  return (
    <>
      <SiteHeader />
      <main className="flex-1">{children}</main>
      <SiteFooter />
      {/* Админы зарлал. Хичээл, админ, нэвтрэх хуудсууд өөр layout-тай тул тэнд гарахгүй. */}
      <AnnouncementPopup />
    </>
  );
}
