"use client";

import {
  BookOpenIcon,
  CrownIcon,
  LayoutDashboardIcon,
  type LucideIcon,
  SparklesIcon,
  UsersIcon,
} from "lucide-react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useLayoutEffect, useRef, useState, useSyncExternalStore } from "react";

import { Logo } from "@/components/layout/logo";
import { ThemeToggle } from "@/components/layout/theme-toggle";
import { UserMenu } from "@/components/layout/user-menu";
import { Button } from "@/components/ui/button";
import { useCurrentUser } from "@/lib/hooks/use-auth";
import { useLiveConfig } from "@/lib/hooks/use-live";
import { mn } from "@/lib/i18n/mn";
import { cn } from "@/lib/utils";

interface NavLink {
  href: string;
  label: string;
  /** Утасны цэсэнд бичвэрийн өмнө харагдана. */
  icon: LucideIcon;
  authOnly?: boolean;
}

const LINKS: NavLink[] = [
  { href: "/courses", label: mn.nav.courses, icon: BookOpenIcon },
  { href: "/pricing", label: mn.nav.pricing, icon: CrownIcon },
  { href: "/dashboard", label: mn.nav.myCourses, icon: LayoutDashboardIcon, authOnly: true },
  // Зөвхөн нэвтэрсэн хэрэглэгчид — нэр, зургийг зочинд харуулахгүй.
  { href: "/community", label: mn.nav.community, icon: UsersIcon, authOnly: true },
];

/** MedlegHub Live — сервер (`LIVE_ACCESS`) энэ хэрэглэгчид нээсэн үед л. */
const LIVE_LINK: NavLink = {
  href: "/live",
  label: mn.nav.live,
  icon: SparklesIcon,
  authOnly: true,
};

const MOBILE_NAV_ID = "mobile-nav";

function isActive(pathname: string, href: string): boolean {
  return pathname === href || pathname.startsWith(`${href}/`);
}

function subscribeToScroll(onChange: () => void): () => void {
  window.addEventListener("scroll", onChange, { passive: true });
  return () => window.removeEventListener("scroll", onChange);
}

/** Хуудас гүйлгэгдсэн эсэх — сервер дээр үргэлж `false`. */
function useScrolled(): boolean {
  return useSyncExternalStore(
    subscribeToScroll,
    () => window.scrollY > 8,
    () => false,
  );
}

let introPlayed = false;

/**
 * Орж ирэх хөдөлгөөнийг зөвхөн хуудсыг анх ачаалахад тоглуулна. `(public)` ба
 * `(app)` layout тус бүр толгойтой тул тэдгээрийн хооронд шилжихэд толгой
 * шинээр mount хийгддэг — тэр үед дахин анивчуулахгүй.
 */
function useIntro(): boolean {
  const [play] = useState(() => !introPlayed);
  useEffect(() => {
    introPlayed = true;
  }, []);
  return play;
}

/**
 * Сайтын толгой.
 *
 * Дээд хэсэгт бүрэн хар; гүйлгэхэд тунгалаг шил болж (`backdrop-blur`) доор нь
 * сүүдэр тусна. Доод зураас нь захдаа бүдгэрсэн шар гэрэл. Анх ачаалагдахад
 * лого, холбоосууд, товчнууд дараалан зөөлөн орж ирнэ — сайт дотор шилжихэд
 * толгой дахин зурагддаггүй тул зөвхөн нэг удаа.
 *
 * `md`-ээс нарийн дэлгэцэд холбоосууд burger цэсэнд орно.
 */
export function SiteHeader() {
  const pathname = usePathname();
  const { user, isLoading } = useCurrentUser();
  const liveEnabled = useLiveConfig().data?.enabled === true;
  const scrolled = useScrolled();
  const intro = useIntro() ? "motion-safe:animate-header-in" : undefined;

  // Цэс аль хуудсан дээр нээгдсэнийг санана — өөр хуудас руу шилжихэд
  // effect-гүйгээр өөрөө хаагдана.
  const [openAt, setOpenAt] = useState<string | null>(null);
  const mobileOpen = openAt === pathname;
  const menuButtonRef = useRef<HTMLButtonElement>(null);
  const closeMobile = () => setOpenAt(null);

  useEffect(() => {
    if (!mobileOpen) return;
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key !== "Escape") return;
      setOpenAt(null);
      menuButtonRef.current?.focus();
    };
    document.addEventListener("keydown", onKeyDown);
    // Цэс нээлттэй үед ард нь хуудас гүйлгэгдэхгүй (`globals.css`, зөвхөн утсанд).
    document.documentElement.dataset.mobileNavOpen = "";
    return () => {
      document.removeEventListener("keydown", onKeyDown);
      delete document.documentElement.dataset.mobileNavOpen;
    };
  }, [mobileOpen]);

  const visible = LINKS.filter((link) => !link.authOnly || user);
  if (user && liveEnabled) visible.push(LIVE_LINK);

  return (
    <header
      data-scrolled={scrolled || undefined}
      className={cn(
        "site-header bg-header-background text-foreground sticky top-0 z-50 transition-[background-color,box-shadow] duration-300",
        "data-scrolled:bg-header-background/80 data-scrolled:shadow-[0_12px_32px_-16px_rgb(0_0_0/0.7)] data-scrolled:backdrop-blur-xl",
        "after:via-primary/45 after:pointer-events-none after:absolute after:inset-x-0 after:bottom-0 after:h-px after:bg-gradient-to-r after:from-white/10 after:to-white/10",
      )}
    >
      <div className="container-page flex min-h-16 items-center gap-x-4 py-2">
        <Logo className={intro} />

        <DesktopNav links={visible} pathname={pathname} intro={intro} />

        <div
          className={cn("ml-auto flex items-center gap-1", intro)}
          style={{ animationDelay: "240ms" }}
        >
          <ThemeToggle />
          <UserMenu />
          <MenuButton
            ref={menuButtonRef}
            open={mobileOpen}
            onClick={() => setOpenAt(mobileOpen ? null : pathname)}
          />
        </div>
      </div>

      <MobileNav
        open={mobileOpen}
        links={visible}
        pathname={pathname}
        showAuth={!isLoading && !user}
        onClose={closeMobile}
      />
    </header>
  );
}

/** Burger-ийн нэг зураас. Tailwind v4-т `rotate`/`scale` нь тусдаа CSS шинж. */
const BAR =
  "absolute left-0 h-0.5 w-5 rounded-full bg-current transition-[top,translate,scale,rotate,opacity] duration-300 ease-[cubic-bezier(0.2,0.8,0.2,1)] motion-reduce:transition-none";

/** Burger товч — нээхэд гурван зураас «X» болж хувирна. */
function MenuButton({
  ref,
  open,
  onClick,
}: {
  ref: React.Ref<HTMLButtonElement>;
  open: boolean;
  onClick: () => void;
}) {
  return (
    <Button
      ref={ref}
      variant="ghost"
      size="icon"
      className="md:hidden"
      // «Цэс» нь хэрэглэгчийн цэсний товчных — давхцахгүй өөр нэр.
      aria-label={mn.nav.navigation}
      aria-expanded={open}
      aria-controls={MOBILE_NAV_ID}
      onClick={onClick}
    >
      <span aria-hidden className="relative block h-3.5 w-5">
        <span className={cn(BAR, open ? "top-1.5 rotate-45" : "top-0")} />
        <span className={cn(BAR, "top-1.5", open && "scale-x-0 opacity-0")} />
        <span className={cn(BAR, open ? "top-1.5 -rotate-45" : "top-3")} />
      </span>
    </Button>
  );
}

/**
 * Утасны цэс — толгойн доор гулсаж нээгдэнэ, мөрүүд нь дараалан орж ирнэ.
 * Ард нь бүдгэрсэн дэвсгэр: дарахад хаагдана. Хаалттай үед `inert` — Tab-аар
 * ч, дэлгэц уншигчаар ч орохгүй. Зочинд нэвтрэх, бүртгүүлэх товч нь энд.
 */
function MobileNav({
  open,
  links,
  pathname,
  showAuth,
  onClose,
}: {
  open: boolean;
  links: NavLink[];
  pathname: string;
  showAuth: boolean;
  onClose: () => void;
}) {
  const rows = links.length + (showAuth ? 1 : 0);
  const rowClass =
    "-translate-x-2 opacity-0 transition-[opacity,translate,scale,rotate] duration-300 ease-out group-data-open/mnav:translate-x-0 group-data-open/mnav:opacity-100 motion-reduce:transition-none";
  const delay = (index: number) => ({ transitionDelay: open ? `${60 + index * 45}ms` : "0ms" });

  return (
    <div className="md:hidden">
      <div
        aria-hidden
        data-open={open || undefined}
        onClick={onClose}
        className="invisible absolute inset-x-0 top-full h-[100dvh] bg-black/60 opacity-0 backdrop-blur-sm transition-[opacity,visibility] duration-300 data-open:visible data-open:opacity-100 motion-reduce:transition-none"
      />
      <nav
        id={MOBILE_NAV_ID}
        aria-label={mn.nav.menu}
        inert={!open}
        data-open={open || undefined}
        className="group/mnav bg-header-background/95 invisible absolute inset-x-0 top-full max-h-[calc(100dvh-4rem)] -translate-y-2 overflow-y-auto border-b border-white/10 opacity-0 shadow-2xl backdrop-blur-xl transition-[opacity,translate,scale,rotate,visibility] duration-300 ease-[cubic-bezier(0.2,0.8,0.2,1)] data-open:visible data-open:translate-y-0 data-open:opacity-100 motion-reduce:transition-none"
      >
        <ul className="container-page grid gap-1 py-3">
          {links.map((link, index) => {
            const active = isActive(pathname, link.href);
            const Icon = link.icon;
            return (
              <li key={link.href} className={rowClass} style={delay(index)}>
                <Link
                  href={link.href}
                  aria-current={active ? "page" : undefined}
                  onClick={onClose}
                  className={cn(
                    "flex min-h-12 items-center gap-3 rounded-xl px-4 text-base font-medium transition-colors",
                    "focus-visible:ring-ring focus-visible:ring-2 focus-visible:outline-none",
                    active
                      ? "bg-accent text-accent-foreground"
                      : "text-muted-foreground hover:text-foreground hover:bg-white/5",
                  )}
                >
                  <Icon className="size-5 shrink-0" aria-hidden />
                  {link.label}
                  {active && (
                    <span
                      aria-hidden
                      className="bg-primary ml-auto size-1.5 rounded-full shadow-[0_0_8px_var(--primary)]"
                    />
                  )}
                </Link>
              </li>
            );
          })}
          {showAuth && (
            <li className={cn(rowClass, "mt-2 grid grid-cols-2 gap-2")} style={delay(rows - 1)}>
              <Button asChild variant="outline" size="lg">
                <Link href="/login" onClick={onClose}>
                  {mn.nav.login}
                </Link>
              </Button>
              <Button asChild size="lg">
                <Link href="/register" onClick={onClose}>
                  {mn.nav.register}
                </Link>
              </Button>
            </li>
          )}
        </ul>
      </nav>
    </div>
  );
}

/**
 * `list`-ийн дотор `el`-ийн байрлалыг CSS хувьсагчид бичнэ (`--hover-*` эсвэл
 * `--active-*`). React state биш: хулгана хөдлөх бүрд дахин зурахгүй, зөвхөн
 * CSS transition гулсуулна.
 */
function placeIndicator(list: HTMLElement, kind: "hover" | "active", el: HTMLElement | null) {
  if (!el) {
    delete list.dataset[kind];
    return;
  }
  // Шар зураас нь бичвэрийн доор (холбоосын дотор зайгүй), гэрэлтсэн дэвсгэр бүтэн.
  const inset = kind === "active" ? 14 : 0;
  list.style.setProperty(`--${kind}-left`, `${el.offsetLeft + inset}px`);
  list.style.setProperty(`--${kind}-width`, `${el.offsetWidth - inset * 2}px`);
  list.dataset[kind] = "";
}

/**
 * Том дэлгэцийн холбоосууд капсул дотор. Хулгана аваачих (эсвэл Tab-аар
 * очих) холбоос руу гэрэлтсэн дэвсгэр гулсаж очно; идэвхтэй хуудасны шар
 * зураас хуудас солигдоход шинэ холбоос руу гулсана.
 *
 * Эхний байрлалыг transition-гүй тавина (`data-ready`), эс бөгөөс зураас
 * зүүн захаас «нисэж» ирнэ. Өргөн өөрчлөгдөх, фонт ачаалагдахад дахин хэмжинэ.
 */
function DesktopNav({
  links,
  pathname,
  intro,
}: {
  links: NavLink[];
  pathname: string;
  /** Орж ирэх хөдөлгөөний класс — зөвхөн анх ачаалахад. */
  intro?: string;
}) {
  const listRef = useRef<HTMLDivElement>(null);
  const activeHref = links.find((link) => isActive(pathname, link.href))?.href;

  useLayoutEffect(() => {
    const list = listRef.current;
    if (!list) return;
    const place = () => {
      const active = activeHref
        ? list.querySelector<HTMLElement>(`[data-nav-href="${activeHref}"]`)
        : null;
      placeIndicator(list, "active", active);
      // Анх хулгана орж ирэхэд гэрэл нь идэвхтэй (эсвэл эхний) холбооснос эхэлнэ.
      if (!("hover" in list.dataset)) {
        const start = active ?? list.querySelector<HTMLElement>("[data-nav-href]");
        if (start) {
          list.style.setProperty("--hover-left", `${start.offsetLeft}px`);
          list.style.setProperty("--hover-width", `${start.offsetWidth}px`);
        }
      }
    };
    place();
    const frame = requestAnimationFrame(() => {
      list.dataset.ready = "";
    });
    const observer = new ResizeObserver(place);
    observer.observe(list);
    void document.fonts?.ready.then(place);
    return () => {
      cancelAnimationFrame(frame);
      observer.disconnect();
    };
  }, [activeHref, links.length]);

  const clearHover = () => {
    if (listRef.current) delete listRef.current.dataset.hover;
  };

  return (
    <nav aria-label={mn.nav.menu} className="hidden md:block">
      <div
        ref={listRef}
        onPointerLeave={clearHover}
        onBlur={(event) => {
          if (!event.currentTarget.contains(event.relatedTarget as Node | null)) clearHover();
        }}
        className="group/nav relative flex items-center gap-0.5 rounded-full border border-white/10 bg-white/[0.04] p-1 shadow-[inset_0_1px_0_rgb(255_255_255/0.06)]"
      >
        <span
          aria-hidden
          style={{ left: "var(--hover-left)", width: "var(--hover-width)" }}
          className="pointer-events-none absolute inset-y-1 rounded-full bg-white/10 opacity-0 transition-opacity duration-200 group-data-[hover]/nav:opacity-100 motion-safe:group-data-[ready]/nav:transition-[left,width,opacity] motion-safe:group-data-[ready]/nav:duration-300 motion-safe:group-data-[ready]/nav:ease-[cubic-bezier(0.2,0.8,0.2,1)]"
        />
        <span
          aria-hidden
          style={{ left: "var(--active-left)", width: "var(--active-width)" }}
          className="bg-primary pointer-events-none absolute bottom-[3px] h-0.5 rounded-full opacity-0 shadow-[0_0_10px_var(--primary)] group-data-[active]/nav:opacity-100 motion-safe:group-data-[ready]/nav:transition-[left,width,opacity] motion-safe:group-data-[ready]/nav:duration-500 motion-safe:group-data-[ready]/nav:ease-[cubic-bezier(0.2,0.8,0.2,1)]"
        />

        {links.map((link, index) => {
          const active = link.href === activeHref;
          return (
            <Link
              key={link.href}
              href={link.href}
              data-nav-href={link.href}
              aria-current={active ? "page" : undefined}
              onPointerEnter={(event) => {
                if (listRef.current) placeIndicator(listRef.current, "hover", event.currentTarget);
              }}
              onFocus={(event) => {
                if (listRef.current) placeIndicator(listRef.current, "hover", event.currentTarget);
              }}
              style={{ animationDelay: `${80 + index * 60}ms` }}
              className={cn(
                intro,
                "relative z-10 rounded-full px-3.5 py-1.5 text-sm font-medium transition-colors duration-200",
                "focus-visible:ring-ring focus-visible:ring-2 focus-visible:outline-none",
                active ? "text-foreground" : "text-muted-foreground hover:text-foreground",
              )}
            >
              {link.label}
            </Link>
          );
        })}
      </div>
    </nav>
  );
}
