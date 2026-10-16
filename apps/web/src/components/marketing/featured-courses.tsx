import { ArrowRightIcon } from "lucide-react";
import Link from "next/link";

import { CourseGrid } from "@/components/courses/course-grid";
import { CourseMarquee } from "@/components/courses/course-marquee";
import { EmptyState } from "@/components/common/states";
import { Section } from "@/components/marketing/section";
import { Button } from "@/components/ui/button";
import { listCourses } from "@/lib/api/courses";
import { mn } from "@/lib/i18n/mn";
import type { CourseSummary } from "@/lib/types/api";

/**
 * Server Component — эхний хуудсанд өгөгдөлтэйгээ ирнэ.
 *
 * Хүсэлт бүрт татна (`no-store`), `/courses`-тэй адил. Cloudflare Workers
 * дээрх кэш нь зөвхөн build-ийн үеийн хуудсыг уншдаг (`open-next.config.ts`)
 * тул `revalidate` нь шинэчлэгдэж чадахгүй — нүүр хуудас build-ийн үеийн
 * (backend-гүй бол хоосон) жагсаалттайгаа үлдэх байв.
 */
/** Урсгалд тасралтгүй мэдрэгдэхийн тулд дор хаяж ийм олон карт хэрэгтэй. */
const MARQUEE_MIN = 4;

async function fetchFeatured(): Promise<CourseSummary[]> {
  try {
    // Бүх нийтлэгдсэн сургалт (API-ийн дээд хэмжээ 48) — нүүр хуудсан дээр урсана.
    const page = await listCourses({ page_size: 48 }, { cache: "no-store" });
    return page.items;
  } catch {
    // Backend унтарсан ч нүүр хуудас ажиллах ёстой.
    return [];
  }
}

export async function FeaturedCourses() {
  const courses = await fetchFeatured();
  const marquee = courses.length >= MARQUEE_MIN;

  return (
    <Section
      title={mn.home.featuredTitle}
      subtitle={mn.home.featuredSubtitle}
      action={
        <Button asChild variant="ghost">
          <Link href="/courses">
            {mn.home.featuredAll}
            <ArrowRightIcon className="size-4" />
          </Link>
        </Button>
      }
    >
      {marquee ? (
        <CourseMarquee courses={courses} />
      ) : courses.length > 0 ? (
        <CourseGrid courses={courses} />
      ) : (
        <EmptyState
          title={mn.courses.empty}
          description={mn.courses.emptyHint}
          action={
            <Button asChild>
              <Link href="/courses">{mn.home.ctaPrimary}</Link>
            </Button>
          }
        />
      )}
    </Section>
  );
}
