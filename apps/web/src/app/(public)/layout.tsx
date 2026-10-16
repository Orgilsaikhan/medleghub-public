import { AnnouncementPopup } from "@/components/announcements/announcement-popup";
import { SiteFooter } from "@/components/layout/site-footer";
import { SiteHeader } from "@/components/layout/site-header";

export default function PublicLayout({ children }: LayoutProps<"/">) {
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
