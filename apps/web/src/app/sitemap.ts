import type { MetadataRoute } from "next";

import { getCourse, listCourses } from "@/lib/api/courses";
import { absoluteUrl } from "@/lib/seo";
import type { CourseSummary } from "@/lib/types/api";

/**
 * Хүсэлт бүрт үүснэ. Cloudflare дээр build-ийн үеийн хариу л кэшлэгддэг
 * (`open-next.config.ts`) тул статик sitemap шинэ сургалтыг хэзээ ч харахгүй.
 * Мөлхөгч үүнийг ховор уншдаг — ачаалал бага.
 */
export const dynamic = "force-dynamic";

const PAGE_SIZE = 48;

async function publishedCourses(): Promise<CourseSummary[]> {
  const courses: CourseSummary[] = [];
  for (let page = 1; page <= 20; page += 1) {
    const result = await listCourses({ page, page_size: PAGE_SIZE }, { cache: "no-store" });
    courses.push(...result.items);
    if (page >= result.total_pages) break;
  }
  return courses;
}

/** Нийтийн, индекслэх хуудсууд л. Нэвтрэх, хувийн, админ хуудас энд ОРОХГҮЙ. */
export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const pages: MetadataRoute.Sitemap = [
    { url: absoluteUrl("/"), changeFrequency: "weekly", priority: 1 },
    { url: absoluteUrl("/courses"), changeFrequency: "weekly", priority: 0.9 },
    { url: absoluteUrl("/pricing"), changeFrequency: "monthly", priority: 0.6 },
    { url: absoluteUrl("/privacy"), changeFrequency: "yearly", priority: 0.2 },
    { url: absoluteUrl("/terms"), changeFrequency: "yearly", priority: 0.2 },
  ];

  let courses: CourseSummary[];
  try {
    // Хичээлгүй («тун удахгүй») сургалт `noindex` — sitemap-д ч оруулахгүй.
    courses = (await publishedCourses()).filter((course) => course.lesson_count > 0);
  } catch {
    // Backend унтарсан ч үндсэн хуудсууд sitemap-д үлдэнэ.
    return pages;
  }

  // Жагсаалтад шинэчилсэн огноо байхгүй — дэлгэрэнгүйгээс авна (сургалт цөөн).
  const details = await Promise.all(
    courses.map((course) => getCourse(course.slug, { cache: "no-store" }).catch(() => null)),
  );

  return [
    ...pages,
    ...courses.map((course, index) => ({
      url: absoluteUrl(`/courses/${course.slug}`),
      ...(details[index] && { lastModified: details[index].updated_at }),
      changeFrequency: "weekly" as const,
      priority: 0.8,
    })),
  ];
}
