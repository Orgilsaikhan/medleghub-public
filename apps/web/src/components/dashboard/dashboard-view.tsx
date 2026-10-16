"use client";

import { GraduationCapIcon } from "lucide-react";
import Link from "next/link";
import { useState } from "react";

import { EmptyState, ErrorState } from "@/components/common/states";
import { ContinueLearning } from "@/components/dashboard/continue-learning";
import { DashboardSkeleton } from "@/components/dashboard/dashboard-skeleton";
import { DashboardSummary } from "@/components/dashboard/dashboard-summary";
import { MyCourseCard } from "@/components/dashboard/my-course-card";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { useCurrentUser } from "@/lib/hooks/use-auth";
import { useMyCourses } from "@/lib/hooks/use-progress";
import { mn } from "@/lib/i18n/mn";
import type { MyCourse } from "@/lib/types/api";

type CourseFilter = "all" | "in_progress" | "finished";

function matchesFilter(item: MyCourse, filter: CourseFilter): boolean {
  const finished = item.progress.total_lessons > 0 && item.progress.percent === 100;
  if (filter === "finished") return finished;
  if (filter === "in_progress") return !finished;
  return true;
}

/**
 * Оюутны хяналтын самбар.
 *
 * Бүх өгөгдөл нэг `/me/courses` дуудлагаас ирнэ — «үргэлжлүүлэх» карт болон
 * сургалтын жагсаалт хоёулаа тэр хариунаас тооцоологдоно.
 */
export function DashboardView() {
  const { user } = useCurrentUser();
  const query = useMyCourses();
  const [filter, setFilter] = useState<CourseFilter>("all");

  if (query.isPending) return <DashboardSkeleton />;

  if (query.isError) {
    return <ErrorState onRetry={() => void query.refetch()} />;
  }

  const courses = query.data;
  const current = pickCurrent(courses);
  const visible = courses.filter((item) => matchesFilter(item, filter));

  return (
    <div className="space-y-12">
      <h1 className="text-2xl font-bold tracking-tight sm:text-3xl">
        {mn.dashboard.greeting(user?.name ?? "")}
      </h1>

      {courses.length === 0 ? (
        <EmptyState
          icon={GraduationCapIcon}
          title={mn.dashboard.emptyTitle}
          description={mn.dashboard.empty}
          className="py-20"
          action={
            <Button asChild size="lg">
              <Link href="/courses">{mn.dashboard.emptyCta}</Link>
            </Button>
          }
        />
      ) : (
        <>
          {current && <ContinueLearning item={current} />}

          <DashboardSummary courses={courses} />

          <section aria-labelledby="my-courses-heading">
            {/* Жагсаалт нь `TabsContent` дотор байх ёстой — эс бөгөөс идэвхтэй
                табын `aria-controls` байхгүй id руу заана (axe: aria-valid-attr-value). */}
            <Tabs
              value={filter}
              onValueChange={(value) => setFilter(value as CourseFilter)}
              className="flex-col gap-4"
            >
              <div className="flex flex-wrap items-center justify-between gap-4">
                <h2 id="my-courses-heading" className="text-lg font-semibold tracking-tight">
                  {mn.dashboard.myCoursesTitle}
                </h2>

                <TabsList>
                  <TabsTrigger value="all">{mn.dashboard.filterAll}</TabsTrigger>
                  <TabsTrigger value="in_progress">{mn.dashboard.filterInProgress}</TabsTrigger>
                  <TabsTrigger value="finished">{mn.dashboard.filterFinished}</TabsTrigger>
                </TabsList>
              </div>

              <TabsContent
                value={filter}
                className="grid gap-6 text-base sm:grid-cols-2 lg:grid-cols-3"
              >
                {visible.map((item) => (
                  <MyCourseCard key={item.course.id} item={item} />
                ))}
              </TabsContent>
            </Tabs>
          </section>
        </>
      )}
    </div>
  );
}

/**
 * Аль сургалтыг онцлох вэ.
 *
 * Сүүлд хичээл дуусгасан, дуусаагүй сургалтыг эхэнд тавина. Дуусаагүй нь
 * байхгүй бол хамгийн сүүлд бүртгүүлсэнийг.
 */
function pickCurrent(courses: MyCourse[]): MyCourse | null {
  if (courses.length === 0) return null;

  const unfinished = courses.filter((item) => item.progress.percent < 100);
  const pool = unfinished.length > 0 ? unfinished : courses;

  return [...pool].sort((a, b) => {
    const left = a.last_completed_at ?? a.enrolled_at;
    const right = b.last_completed_at ?? b.enrolled_at;
    return right.localeCompare(left);
  })[0];
}
