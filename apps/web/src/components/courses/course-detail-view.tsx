"use client";

import { useQuery } from "@tanstack/react-query";
import {
  BookOpenIcon,
  ChevronRightIcon,
  ClockIcon,
  InfoIcon,
  LayersIcon,
  SignalIcon,
} from "lucide-react";
import Link from "next/link";

import { EmptyState } from "@/components/common/states";
import { AccessBadge } from "@/components/courses/access-badge";
import { CategoryLogo } from "@/components/courses/category-logo";
import { CourseStudents } from "@/components/courses/course-students";
import { CurriculumList } from "@/components/courses/curriculum-list";
import { EnrollButton } from "@/components/courses/enroll-button";
import { ProgressBar } from "@/components/courses/progress-bar";
import { Badge } from "@/components/ui/badge";
import { getCourse } from "@/lib/api/courses";
import { COURSE_PREREQUISITES } from "@/lib/course-prerequisites";
import { formatDuration, formatMnt } from "@/lib/format";
import { useCurrentUser } from "@/lib/hooks/use-auth";
import { usePlan } from "@/lib/hooks/use-plan";
import { categoryLabels, difficultyLabels, mn } from "@/lib/i18n/mn";
import { queryKeys } from "@/lib/query-keys";
import type { CourseDetail } from "@/lib/types/api";

/**
 * Сургалтын дэлгэрэнгүй.
 *
 * Нийтийн хэсэг нь сервер дээр render хийгдсэн байна. Нэвтэрсэн хэрэглэгчийн
 * «бүртгүүлсэн / ахиц» мэдээллийг л client тал дээр нэмж татна.
 */
export function CourseDetailView({ initialCourse }: { initialCourse: CourseDetail }) {
  const { isAuthenticated } = useCurrentUser();

  const { data: course = initialCourse } = useQuery({
    queryKey: queryKeys.courses.detail(initialCourse.slug),
    queryFn: () => getCourse(initialCourse.slug),
    initialData: initialCourse,
    // Серверийн хариу нь нэвтрээгүй байдлаар авагдсан тул шууд хуучирсанд
    // тооцно — эс бөгөөс «бүртгүүлсэн / ахиц» мэдээлэл хэзээ ч ирэхгүй.
    initialDataUpdatedAt: 0,
    enabled: isAuthenticated,
  });

  const hasLessons = course.modules.some((section) => section.lessons.length > 0);

  return (
    <div className="container-page py-10 lg:py-14">
      <CourseBreadcrumb title={course.title} />

      <div className="grid gap-10 lg:grid-cols-[1fr_22rem] lg:gap-14">
        <div className="min-w-0">
          <div className="flex flex-wrap items-center gap-2">
            <Badge variant="outline">{categoryLabels[course.category]}</Badge>
            <Badge variant="outline">{difficultyLabels[course.difficulty]}</Badge>
            <AccessBadge course={course} />
          </div>

          <div className="mt-4 flex items-center gap-4">
            <CategoryLogo category={course.category} className="size-12 shrink-0 sm:size-14" />
            <h1 className="text-3xl font-bold tracking-tight text-balance sm:text-4xl">
              {course.title}
            </h1>
          </div>

          <p className="text-muted-foreground mt-4 max-w-2xl leading-relaxed text-pretty">
            {course.description}
          </p>

          <Prerequisites slug={course.slug} />

          <div className="mt-8 lg:hidden">
            <CourseSidebar course={course} />
          </div>

          <section className="mt-12" aria-labelledby="curriculum-heading">
            <h2 id="curriculum-heading" className="text-xl font-semibold tracking-tight">
              {mn.courseDetail.curriculum}
            </h2>

            <div className="mt-6">
              {hasLessons ? (
                <CurriculumList
                  modules={course.modules}
                  courseSlug={course.slug}
                  linkLessons={course.enrolled}
                />
              ) : (
                <EmptyState icon={BookOpenIcon} title={mn.courseDetail.emptyCurriculum} />
              )}
            </div>
          </section>

          <CourseStudents slug={course.slug} className="mt-12 lg:hidden" />
        </div>

        <aside className="hidden lg:block">
          {/* Дэлгэцийн өндрөөс хэтрэхгүй — суралцагчдын жагсаалт дотроо гүйлгэгдэнэ. */}
          <div className="sticky top-24 flex max-h-[calc(100dvh-7rem)] flex-col gap-6">
            <CourseSidebar course={course} />
            <CourseStudents slug={course.slug} className="min-h-40" />
          </div>
        </aside>
      </div>
    </div>
  );
}

/** Урьдчилсан мэдлэг — зөвхөн анхааруулга, сургалтыг хаадаггүй. */
function Prerequisites({ slug }: { slug: string }) {
  const courses = COURSE_PREREQUISITES[slug];
  if (!courses?.length) return null;
  return (
    <aside
      aria-labelledby="prerequisites-heading"
      className="mt-6 flex max-w-2xl gap-3 rounded-lg border border-amber-500/40 bg-amber-500/10 p-4"
    >
      <InfoIcon className="mt-0.5 size-4 shrink-0 text-amber-700 dark:text-amber-400" aria-hidden />
      <div className="min-w-0 text-sm leading-relaxed">
        <h2 id="prerequisites-heading" className="font-semibold">
          {mn.learn.react.prerequisiteTitle}
        </h2>
        <p className="mt-1">{mn.learn.react.prerequisite}</p>
        <ul className="mt-2 flex flex-wrap gap-x-4 gap-y-1">
          {courses.map((course) => (
            <li key={course.slug}>
              <Link
                href={`/courses/${course.slug}`}
                className="text-brand-link font-medium underline underline-offset-4"
              >
                {course.title}
              </Link>
            </li>
          ))}
        </ul>
      </div>
    </aside>
  );
}

/** Нүүр › Сургалтууд › сургалт — `BreadcrumbList` JSON-LD-тэй ижил. */
function CourseBreadcrumb({ title }: { title: string }) {
  const separator = <ChevronRightIcon className="size-3.5 shrink-0" aria-hidden />;
  return (
    <nav aria-label={mn.seo.breadcrumb} className="text-muted-foreground mb-6 text-sm">
      <ol className="flex min-w-0 items-center gap-1.5">
        <li className="shrink-0">
          <Link href="/" className="hover:text-foreground transition-colors">
            {mn.seo.home}
          </Link>
        </li>
        <li className="flex shrink-0 items-center gap-1.5">
          {separator}
          <Link href="/courses" className="hover:text-foreground transition-colors">
            {mn.courses.title}
          </Link>
        </li>
        <li className="flex min-w-0 items-center gap-1.5">
          {separator}
          <span aria-current="page" className="text-foreground truncate">
            {title}
          </span>
        </li>
      </ol>
    </nav>
  );
}

function CourseSidebar({ course }: { course: CourseDetail }) {
  return (
    <div className="bg-card rounded-xl border p-6">
      {course.enrolled && course.progress && course.progress.total_lessons > 0 && (
        <div className="mb-6">
          <p className="mb-2 text-sm font-medium">{mn.courseDetail.progressLabel}</p>
          <ProgressBar progress={course.progress} />
        </div>
      )}

      <EnrollButton course={course} />

      {!course.is_free && course.lesson_count > course.free_lessons && (
        <PlanNotice course={course} />
      )}

      <dl className="mt-6 space-y-3 border-t pt-6 text-sm">
        <Fact icon={BookOpenIcon} label={mn.courseDetail.lessonCount}>
          {course.lesson_count > 0
            ? mn.courses.lessons(course.lesson_count)
            : mn.courses.noLessonsYet}
        </Fact>
        {course.duration > 0 && (
          <Fact icon={ClockIcon} label={mn.courseDetail.duration}>
            {formatDuration(course.duration)}
          </Fact>
        )}
        <Fact icon={SignalIcon} label={mn.courseDetail.difficulty}>
          {difficultyLabels[course.difficulty]}
        </Fact>
        <Fact icon={LayersIcon} label={mn.courseDetail.category}>
          {categoryLabels[course.category]}
        </Fact>
      </dl>
    </div>
  );
}

/** Хэдэн хичээл үнэгүй, үлдсэн нь ямар багцад багтах вэ. */
function PlanNotice({ course }: { course: CourseDetail }) {
  const { data: plan } = usePlan();

  if (plan?.has_plan) {
    return <p className="text-muted-foreground mt-3 text-xs">{mn.courseDetail.planActiveNotice}</p>;
  }

  return (
    <p className="text-muted-foreground mt-3 text-xs leading-relaxed">
      {plan
        ? mn.courseDetail.planNotice(
            course.free_lessons,
            course.lesson_count - course.free_lessons,
            formatMnt(plan.price_mnt),
          )
        : null}{" "}
      <Link
        href="/pricing"
        className="text-brand-link font-medium underline-offset-4 hover:underline"
      >
        {mn.courseDetail.seePlans}
      </Link>
    </p>
  );
}

function Fact({
  icon: Icon,
  label,
  children,
}: {
  icon: typeof BookOpenIcon;
  label: string;
  children: React.ReactNode;
}) {
  return (
    <div className="flex items-center justify-between gap-3">
      <dt className="text-muted-foreground flex items-center gap-2">
        <Icon className="size-4" aria-hidden />
        {label}
      </dt>
      <dd className="font-medium">{children}</dd>
    </div>
  );
}
