import type { Metadata } from "next";
import { Suspense } from "react";

import { CourseCatalog } from "@/components/courses/course-catalog";
import { CourseFilters, CoursesHeading } from "@/components/courses/course-filters";
import { CourseGridSkeleton } from "@/components/courses/course-grid";
import { JsonLd } from "@/components/seo/json-ld";
import { listCourses, type CourseListParams } from "@/lib/api/courses";
import { categoryOrder, difficultyOrder, mn } from "@/lib/i18n/mn";
import { courseListJsonLd, pageMetadata } from "@/lib/seo";
import type { Category, CourseSummary, Difficulty, Page } from "@/lib/types/api";

/**
 * Шүүлтүүр, хуудаслалтын хувилбар бүр `/courses` руу canonical-тай — ижил
 * агуулгын олон URL индекслэгдэхгүй. Хайлтын үр дүнг (`?q=`) индекслэхгүй.
 */
export async function generateMetadata({ searchParams }: PageProps<"/courses">): Promise<Metadata> {
  const { q } = await searchParams;
  return pageMetadata({
    title: mn.seo.coursesTitle,
    description: mn.seo.coursesDescription,
    path: "/courses",
    noindex: Boolean(q),
  });
}

function isUnfiltered(params: CourseListParams): boolean {
  return !params.q && !params.category && !params.difficulty && (params.page ?? 1) === 1;
}

/** URL-аас ирсэн утгыг цэвэрлэж, зөвшөөрөгдсөн утга л дамжуулна. */
function parseParams(raw: Record<string, string | string[] | undefined>): CourseListParams {
  const single = (key: string): string | undefined => {
    const value = raw[key];
    return Array.isArray(value) ? value[0] : value;
  };

  const category = single("category");
  const difficulty = single("difficulty");
  const page = Number.parseInt(single("page") ?? "1", 10);

  return {
    q: single("q")?.trim() || undefined,
    category: categoryOrder.includes(category as Category) ? (category as Category) : undefined,
    difficulty: difficultyOrder.includes(difficulty as Difficulty)
      ? (difficulty as Difficulty)
      : undefined,
    page: Number.isFinite(page) && page > 0 ? page : 1,
  };
}

export default async function CoursesPage({ searchParams }: PageProps<"/courses">) {
  const params = parseParams(await searchParams);

  return (
    <div className="container-page py-10 lg:py-14">
      {/* Гарчиг шууд харагдана; хайлтын товч ангиллын жагсаалт ирэхэд нэмэгдэнэ. */}
      <Suspense fallback={<CoursesHeading />}>
        <SearchHeader />
      </Suspense>

      <div className="mt-10">
        {/* Шүүлтүүр солигдох бүрт шинэ Suspense boundary — skeleton зөв харагдана. */}
        <Suspense key={JSON.stringify(params)} fallback={<CourseGridSkeleton wide />}>
          <CatalogResults params={params} />
        </Suspense>
      </div>
    </div>
  );
}

/**
 * Хайлтын ангиллын товчнууд — зөвхөн сургалттай ангиллууд, `categoryOrder`-оор.
 * Backend боломжгүй бол бүх ангилал.
 */
async function SearchHeader() {
  let categories: Category[] = categoryOrder;
  try {
    const all = await listCourses({ page_size: 48 }, { cache: "no-store" });
    const present = new Set(all.items.map((course) => course.category));
    categories = categoryOrder.filter((category) => present.has(category));
  } catch {
    // Бүх ангиллыг харуулна.
  }
  return <CourseFilters categories={categories} />;
}

async function CatalogResults({ params }: { params: CourseListParams }) {
  let initialPage: Page<CourseSummary> | null = null;
  try {
    initialPage = await listCourses(params, { cache: "no-store" });
  } catch {
    // Backend боломжгүй бол client тал дахин оролдоно.
  }
  return (
    <>
      {/* Бүтэн жагсаалтын хуудсанд л — шүүсэн хувилбар canonical руу заадаг.
          Хичээлгүй сургалт `noindex` тул sitemap-тай адил хасна. */}
      {initialPage && isUnfiltered(params) && (
        <JsonLd
          data={courseListJsonLd(initialPage.items.filter((course) => course.lesson_count > 0))}
        />
      )}
      <CourseCatalog params={params} initialPage={initialPage} />
    </>
  );
}
