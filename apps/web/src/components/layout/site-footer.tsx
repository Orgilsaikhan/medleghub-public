import { MailIcon, MessageSquareIcon, PhoneIcon } from "lucide-react";
import Link from "next/link";

import { FeedbackLink } from "@/components/feedback/feedback-link";
import { LogoMark } from "@/components/layout/logo";
import { categoryLabels, mn } from "@/lib/i18n/mn";
import { FACEBOOK_URL } from "@/lib/seo";

const LEARN_LINKS = [
  { href: "/courses?category=javascript", label: categoryLabels.javascript },
  { href: "/courses?category=html_css", label: categoryLabels.html_css },
  { href: "/courses?category=python", label: categoryLabels.python },
  { href: "/courses?category=react", label: categoryLabels.react },
];

const PLATFORM_LINKS = [
  { href: "/courses", label: mn.nav.courses },
  { href: "/dashboard", label: mn.nav.dashboard },
  { href: "/register", label: mn.nav.register },
  { href: "/login", label: mn.nav.login },
];

const CONTACT_EMAIL = "info@medleghub.com";
const CONTACT_PHONES = ["99265563", "86979766"];

export function SiteFooter() {
  return (
    <footer className="bg-muted/30 mt-auto border-t">
      <div className="container-page grid gap-10 py-12 sm:grid-cols-2 lg:grid-cols-5">
        <div className="lg:col-span-2">
          {/* Үг тэмдэг нь нэрийг өөртөө агуулдаг тул дахин бичихгүй. Нууц
              `/footprints` хуудас руу хөтөлнө — зориуд ямар ч сануулгагүй. */}
          <Link
            href="/footprints"
            className="focus-visible:ring-ring flex w-fit items-center rounded-md focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:outline-none"
          >
            <LogoMark />
          </Link>
          <p className="text-muted-foreground mt-3 max-w-sm text-sm leading-relaxed">
            {mn.footer.tagline}
          </p>
        </div>

        <FooterColumn title={mn.footer.learn} links={LEARN_LINKS} />
        <FooterColumn title={mn.footer.platform} links={PLATFORM_LINKS} />
        <ContactColumn />
      </div>

      <div className="border-t">
        <div className="container-page text-muted-foreground flex flex-col gap-3 py-6 text-xs sm:flex-row sm:items-center sm:justify-between">
          <p>{mn.footer.rights(new Date().getFullYear())}</p>
          <nav aria-label={mn.footer.legal} className="flex gap-4">
            <Link href="/privacy" className="hover:text-foreground transition-colors">
              {mn.legal.privacy}
            </Link>
            <Link href="/terms" className="hover:text-foreground transition-colors">
              {mn.legal.terms}
            </Link>
          </nav>
        </div>
      </div>
    </footer>
  );
}

function FooterColumn({
  title,
  links,
}: {
  title: string;
  links: { href: string; label: string }[];
}) {
  return (
    <div>
      <h2 className="text-sm font-semibold">{title}</h2>
      <ul className="mt-3 space-y-2">
        {links.map((link) => (
          <li key={link.href}>
            <Link
              href={link.href}
              className="text-muted-foreground hover:text-foreground inline-block text-sm transition-[color,translate,scale,rotate] hover:translate-x-0.5 motion-reduce:hover:translate-x-0"
            >
              {link.label}
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}

/**
 * Мөр бүр дүрстэй (имэйл, утас, Facebook, санал хүсэлт). Хулгана аваачихад
 * дүрс нь брэндийн өнгөөр гэрэлтэнэ.
 */
function ContactColumn() {
  const rowClass =
    "group text-muted-foreground hover:text-foreground flex min-h-6 w-fit items-center gap-2 text-sm transition-colors";
  const iconClass = "group-hover:text-brand-link size-4 shrink-0 transition-colors";

  return (
    <div>
      <h2 className="text-sm font-semibold">{mn.footer.contact}</h2>
      <ul className="mt-3 space-y-2">
        <li>
          <a href={`mailto:${CONTACT_EMAIL}`} className={rowClass}>
            <MailIcon className={iconClass} aria-hidden />
            {CONTACT_EMAIL}
          </a>
        </li>
        {CONTACT_PHONES.map((phone) => (
          <li key={phone}>
            <a href={`tel:+976${phone}`} className={rowClass}>
              <PhoneIcon className={iconClass} aria-hidden />
              {phone}
            </a>
          </li>
        ))}
        <li>
          <a href={FACEBOOK_URL} target="_blank" rel="noopener noreferrer" className={rowClass}>
            <FacebookIcon className={iconClass} />
            {mn.brand.name}
            <span className="sr-only"> — {mn.footer.facebook}</span>
          </a>
        </li>
        <li>
          <FeedbackLink
            className={rowClass}
            icon={<MessageSquareIcon className={iconClass} aria-hidden />}
          />
        </li>
      </ul>
    </div>
  );
}

/** Facebook-ийн "f" лого. lucide-react v1 брэндийн дүрсгүй тул гараар зурав. */
function FacebookIcon({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" className={className}>
      <path d="M9.101 23.691v-7.98H6.627v-3.667h2.474v-1.58c0-4.085 1.848-5.978 5.858-5.978.401 0 .955.042 1.468.103a8.68 8.68 0 0 1 1.141.195v3.325a8.623 8.623 0 0 0-.653-.036 26.805 26.805 0 0 0-.733-.009c-.707 0-1.259.096-1.675.309a1.686 1.686 0 0 0-.679.622c-.258.42-.374.995-.374 1.752v1.297h3.919l-.386 2.103-.287 1.564h-3.246v8.245C19.396 23.238 24 18.179 24 12.044c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.628 3.874 10.35 9.101 11.647Z" />
    </svg>
  );
}
