"use client";

import { useQuery } from "@tanstack/react-query";
import { SearchXIcon } from "lucide-react";

import { EmptyState, ErrorState } from "@/components/common/states";
import { Pagination } from "@/components/common/pagination";
import { CourseGrid, CourseGridSkeleton } from "@/components/courses/course-grid";
import { listCourses, type CourseListParams } from "@/lib/api/courses";
import { useCurrentUser } from "@/lib/hooks/use-auth";
import { mn } from "@/lib/i18n/mn";
import { queryKeys } from "@/lib/query-keys";
import type { CourseSummary, Page } from "@/lib/types/api";

interface CourseCatalogProps {
  params: CourseListParams;
  /** Server Component-ээс ирсэн нийтийн жагсаалт. */
  initialPage: Page<CourseSummary> | null;
}

/**
 * Каталогийн жагсаалт.
 *
 * Нийтийн өгөгдөл нь сервер дээр аль хэдийн render хийгдсэн байдаг. Нэвтэрсэн
 * хэрэглэгчид л «бүртгүүлсэн / ахиц» мэдээллийг авахын тулд дахин татна —
 * зочид нэмэлт хүсэлт үүсгэхгүй.
 */
export function CourseCatalog({ params, initialPage }: CourseCatalogProps) {
  const { isAuthenticated, isLoading: authLoading } = useCurrentUser();

  const query = useQuery({
    queryKey: queryKeys.courses.list(params),
    queryFn: () => listCourses(params),
    initialData: initialPage ?? undefined,
    // Серверийн хариу нь нэвтрээгүй байдлаар авагдсан тул шууд хуучирсанд
    // тооцно — эс бөгөөс «бүртгүүлсэн / ахиц» мэдээлэл хэзээ ч ирэхгүй.
    initialDataUpdatedAt: 0,
    enabled: isAuthenticated,
  });

  if (query.isError && !query.data) {
    return <ErrorState onRetry={() => void query.refetch()} />;
  }

  if (!query.data) {
    return authLoading || query.isPending ? <CourseGridSkeleton wide /> : <ErrorState />;
  }

  const { items, page, total_pages: totalPages, total } = query.data;

  if (items.length === 0) {
    return (
      <EmptyState icon={SearchXIcon} title={mn.courses.empty} description={mn.courses.emptyHint} />
    );
  }

  return (
    <div className="space-y-8">
      <p className="text-muted-foreground text-sm">{mn.courses.resultCount(total)}</p>
      <CourseGrid courses={items} wide />
      <Pagination
        page={page}
        totalPages={totalPages}
        buildHref={(next) => buildHref(params, next)}
      />
    </div>
  );
}

function buildHref(params: CourseListParams, page: number): string {
  const search = new URLSearchParams();
  if (params.q) search.set("q", params.q);
  if (params.category) search.set("category", params.category);
  if (params.difficulty) search.set("difficulty", params.difficulty);
  if (page > 1) search.set("page", String(page));
  const query = search.toString();
  return query ? `/courses?${query}` : "/courses";
}
