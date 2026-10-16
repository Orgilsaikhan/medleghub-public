import type { Metadata } from "next";

import { categoryLabels, difficultyLabels, mn } from "@/lib/i18n/mn";
import type { CourseDetail, CourseSummary } from "@/lib/types/api";

/**
 * Хайлтын систем, сошиал сүлжээнд зориулсан metadata ба JSON-LD.
 *
 * Canonical, `og:url` зэрэг нь ҮРГЭЛЖ production домэйн руу заана — орчны
 * хувьсагчаас уншихгүй. `.env.production`-д хуучин (Vercel, trycloudflare)
 * хаяг үлдсэн байдаг тул түүнд найдвал буруу canonical гарах эрсдэлтэй.
 */
export const SITE_URL = "https://medleghub.com";
export const SITE_NAME = mn.brand.name;
export const CONTACT_EMAIL = "info@medleghub.com";
export const FACEBOOK_URL = "https://www.facebook.com/people/MedlegHub/61595054963587/";

/** `public/og.png` — `npm run og:image` үүсгэнэ. 1200×630 (Facebook, X, LinkedIn). */
export const OG_IMAGE = {
  url: "/og.png",
  width: 1200,
  height: 630,
  alt: mn.seo.ogImageAlt,
} as const;

const LOGO_URL = `${SITE_URL}/main_logo.png`;

export function absoluteUrl(path: string): string {
  return path === "/" ? SITE_URL : `${SITE_URL}${path}`;
}

interface PageSeo {
  /** Template (`… | MedlegHub`)-тэй нийлнэ. `absoluteTitle` бол бүтнээрээ. */
  title: string;
  description: string;
  /** `/courses` гэх мэт — canonical ба `og:url`. */
  path: string;
  absoluteTitle?: boolean;
  /** Хайлтад гаргахгүй (холбоосыг нь дагана). */
  noindex?: boolean;
  image?: { url: string; width?: number; height?: number; alt?: string };
}

/**
 * Хуудас бүрийн metadata. Next нь `openGraph`-ийг segment бүрт БҮТНЭЭР нь
 * солидог — эндээс гаргахгүй бол root layout-ын нүүр хуудасны гарчиг бүх
 * хуудсанд харагдана.
 */
export function pageMetadata({
  title,
  description,
  path,
  absoluteTitle = false,
  noindex = false,
  image = OG_IMAGE,
}: PageSeo): Metadata {
  const fullTitle = absoluteTitle ? title : `${title} | ${SITE_NAME}`;
  return {
    title: absoluteTitle ? { absolute: title } : title,
    description,
    alternates: { canonical: path },
    openGraph: {
      type: "website",
      siteName: SITE_NAME,
      locale: "mn_MN",
      url: path,
      title: fullTitle,
      description,
      images: [image],
    },
    twitter: {
      card: "summary_large_image",
      title: fullTitle,
      description,
      images: [image],
    },
    ...(noindex && { robots: { index: false, follow: true } }),
  };
}

/** Тайлбарыг ~155 тэмдэгтээр, үгийн дундуур таслахгүйгээр богиносгоно. */
export function trimDescription(text: string, max = 155): string {
  const clean = text.replace(/\s+/g, " ").trim();
  if (clean.length <= max) return clean;
  const cut = clean.slice(0, max);
  const sentence = cut.lastIndexOf(". ");
  if (sentence > max * 0.6) return cut.slice(0, sentence + 1);
  const space = cut.lastIndexOf(" ");
  return `${cut.slice(0, space > 0 ? space : max).replace(/[,;:—–-]+$/, "")}…`;
}

/**
 * «C ба C++ үндэс — C, C++ хичээл монгол хэлээр». Урт бол «монгол хэлээр»-ийг,
 * дараа нь сэдвийг хасна — гарчиг ~60 тэмдэгтээс хэтрэхгүй.
 */
export function courseSeoTitle(course: Pick<CourseSummary, "title" | "category">): string {
  const topic = mn.seo.courseTopic[course.category];
  const separator = course.title.includes("—") ? ": " : " — ";
  const candidates = [
    `${course.title}${separator}${topic} ${mn.seo.inMongolian}`,
    `${course.title}${separator}${topic}`,
  ];
  return candidates.find((title) => title.length <= 60) ?? course.title;
}

// --- JSON-LD ------------------------------------------------------------------

const organizationRef = { "@id": `${SITE_URL}/#organization` };

export function organizationJsonLd() {
  return {
    "@context": "https://schema.org",
    "@type": "Organization",
    "@id": organizationRef["@id"],
    name: SITE_NAME,
    url: SITE_URL,
    logo: LOGO_URL,
    email: CONTACT_EMAIL,
    description: mn.footer.tagline,
    sameAs: [FACEBOOK_URL],
  };
}

export function websiteJsonLd() {
  return {
    "@context": "https://schema.org",
    "@type": "WebSite",
    "@id": `${SITE_URL}/#website`,
    name: SITE_NAME,
    url: SITE_URL,
    inLanguage: "mn",
    publisher: organizationRef,
  };
}

export function breadcrumbJsonLd(items: { name: string; path: string }[]) {
  return {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    itemListElement: items.map((item, index) => ({
      "@type": "ListItem",
      position: index + 1,
      name: item.name,
      item: absoluteUrl(item.path),
    })),
  };
}

export function courseListJsonLd(courses: Pick<CourseSummary, "slug" | "title">[]) {
  return {
    "@context": "https://schema.org",
    "@type": "ItemList",
    itemListElement: courses.map((course, index) => ({
      "@type": "ListItem",
      position: index + 1,
      url: absoluteUrl(`/courses/${course.slug}`),
      name: course.title,
    })),
  };
}

/** Секундийг ISO 8601 хугацаа болгоно: 5400 → "PT1H30M". */
function isoDuration(seconds: number): string {
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.round((seconds % 3600) / 60);
  return `PT${hours ? `${hours}H` : ""}${minutes || !hours ? `${minutes}M` : ""}`;
}

/**
 * Сургалтын бодит өгөгдлөөс л — багш, үнэлгээ зэрэг байхгүй мэдээллийг
 * зохиохгүй. Үнэ нь сургалтынх биш, сарын багцынх тул `price` бичихгүй.
 */
export function courseJsonLd(course: CourseDetail) {
  const lessons = course.modules.flatMap((module) => module.lessons);
  const category = course.is_free
    ? "Free"
    : course.free_lessons > 0
      ? "Partially Free"
      : "Subscription";

  return {
    "@context": "https://schema.org",
    "@type": "Course",
    "@id": `${absoluteUrl(`/courses/${course.slug}`)}#course`,
    name: course.title,
    description: trimDescription(course.description, 500),
    url: absoluteUrl(`/courses/${course.slug}`),
    image: course.thumbnail_url ?? absoluteUrl(OG_IMAGE.url),
    inLanguage: "mn",
    educationalLevel: difficultyLabels[course.difficulty],
    about: categoryLabels[course.category],
    isAccessibleForFree: course.is_free,
    provider: { ...organizationRef, "@type": "Organization", name: SITE_NAME, sameAs: SITE_URL },
    offers: [{ "@type": "Offer", category }],
    hasCourseInstance: [
      {
        "@type": "CourseInstance",
        courseMode: "Online",
        inLanguage: "mn",
        ...(course.duration > 0 && { courseWorkload: isoDuration(course.duration) }),
      },
    ],
    ...(lessons.length > 0 && {
      syllabusSections: course.modules
        .filter((module) => module.lessons.length > 0)
        .map((module) => ({
          "@type": "Syllabus",
          name: module.title,
          ...(module.description && { description: module.description }),
        })),
    }),
    datePublished: course.created_at,
    dateModified: course.updated_at,
  };
}
