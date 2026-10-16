"use client";

import { BookOpenIcon, ClockIcon } from "lucide-react";
import Image from "next/image";
import Link from "next/link";

import { AccessBadge } from "@/components/courses/access-badge";
import { CategoryLogo } from "@/components/courses/category-logo";
import { ProgressBar } from "@/components/courses/progress-bar";
import { Badge } from "@/components/ui/badge";
import { formatDuration } from "@/lib/format";
import { categoryLabels, difficultyLabels, mn } from "@/lib/i18n/mn";
import type { CourseSummary } from "@/lib/types/api";
import { cn } from "@/lib/utils";

/** Ангилал бүрт тогтмол өнгө — каталог дээр нүдээр ялгахад тусална. */
const CATEGORY_TINT: Record<string, string> = {
  javascript: "from-amber-500/25 to-amber-500/5",
  html_css: "from-orange-500/25 to-orange-500/5",
  python: "from-blue-500/25 to-blue-500/5",
  react: "from-cyan-500/25 to-cyan-500/5",
  c: "from-slate-500/25 to-slate-500/5",
  csharp: "from-violet-500/25 to-violet-500/5",
  java: "from-red-500/25 to-red-500/5",
  backend: "from-emerald-500/25 to-emerald-500/5",
  database: "from-indigo-500/25 to-indigo-500/5",
  git: "from-rose-500/25 to-rose-500/5",
  flowgorithm: "from-teal-500/25 to-teal-500/5",
};

/**
 * Курсорын байрлалыг CSS хувьсагчид бичнэ — гэрэл (`--spot-x/y`, px) болон
 * 3D хазайлт (`--tilt-x/y`, -1…1) түүнийг дагана. React state биш: хулгана
 * хөдлөх бүрд дахин зурахгүй.
 */
function trackPointer(event: React.PointerEvent<HTMLElement>) {
  const card = event.currentTarget;
  const rect = card.getBoundingClientRect();
  const x = event.clientX - rect.left;
  const y = event.clientY - rect.top;
  card.style.setProperty("--spot-x", `${x}px`);
  card.style.setProperty("--spot-y", `${y}px`);
  card.style.setProperty("--tilt-x", `${(x / rect.width) * 2 - 1}`);
  card.style.setProperty("--tilt-y", `${(y / rect.height) * 2 - 1}`);
}

/**
 * Сургалтын карт.
 *
 * Хулгана аваачихад карт дээш өргөгдөж, курсор руугаа 3D-ээр бага зэрэг
 * хазайна; курсорыг дагасан шар гэрэл картын дотор ба хүрээн дээр тусна;
 * лого нь «үсэрнэ». Хөдөлгөөн багасгах тохиргоотой бол өргөгдөх, хазайх,
 * эргэх хөдөлгөөнгүй.
 */
export function CourseCard({ course, className }: { course: CourseSummary; className?: string }) {
  const tint = CATEGORY_TINT[course.category] ?? "from-primary/20 to-primary/5";

  return (
    <article
      onPointerMove={trackPointer}
      className={cn(
        "group bg-card relative flex flex-col overflow-hidden rounded-xl border",
        "hover:border-primary/40 hover:shadow-primary/10 transition-[translate,scale,rotate,transform,box-shadow,border-color] duration-300 ease-out hover:shadow-xl motion-safe:hover:-translate-y-1.5",
        "motion-safe:hover:[transform:perspective(900px)_rotateX(calc(var(--tilt-y,0)*-5deg))_rotateY(calc(var(--tilt-x,0)*7deg))]",
        className,
      )}
    >
      {/* Курсорыг дагах гэрэл — картын дотор… */}
      <span
        aria-hidden
        className="pointer-events-none absolute inset-0 z-10 opacity-0 transition-opacity duration-300 [background:radial-gradient(360px_circle_at_var(--spot-x,50%)_var(--spot-y,50%),color-mix(in_oklch,var(--primary)_13%,transparent),transparent_65%)] group-hover:opacity-100"
      />
      {/* …ба 1px хүрээн дээр (дотор талыг mask-аар хасна). */}
      <span
        aria-hidden
        className="pointer-events-none absolute inset-0 z-20 rounded-[inherit] p-px opacity-0 transition-opacity duration-300 [background:radial-gradient(240px_circle_at_var(--spot-x,50%)_var(--spot-y,50%),var(--primary),transparent_70%)] [mask:linear-gradient(#000_0_0)_content-box_exclude,linear-gradient(#000_0_0)] group-hover:opacity-100"
      />

      <div className={cn("relative aspect-video w-full bg-gradient-to-br", tint)}>
        {course.thumbnail_url ? (
          <Image
            src={course.thumbnail_url}
            alt=""
            fill
            sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw"
            className="object-cover"
          />
        ) : (
          <span className="absolute inset-0 grid place-items-center">
            <CategoryLogo
              category={course.category}
              className="size-14 drop-shadow-sm transition-transform duration-500 ease-[cubic-bezier(0.34,1.56,0.64,1)] group-hover:scale-110 motion-safe:group-hover:-translate-y-1 motion-safe:group-hover:-rotate-6"
            />
          </span>
        )}

        <div className="absolute top-3 right-3">
          <AccessBadge course={course} />
        </div>
      </div>

      <div className="flex flex-1 flex-col p-5">
        <div className="flex flex-wrap items-center gap-2">
          <Badge variant="outline">{categoryLabels[course.category]}</Badge>
          <Badge variant="outline">{difficultyLabels[course.difficulty]}</Badge>
          {course.enrolled && (
            <Badge variant="outline" className="border-primary/40 text-brand-link">
              {mn.courses.enrolled}
            </Badge>
          )}
        </div>

        <h3 className="mt-3 text-base leading-snug font-semibold">
          {/* Карт бүхэлдээ дарагдахаар — линкийг картын хэмжээгээр тэлнэ. */}
          <Link href={`/courses/${course.slug}`} className="after:absolute after:inset-0">
            {course.title}
          </Link>
        </h3>

        <p className="text-muted-foreground mt-2 line-clamp-2 text-sm leading-relaxed">
          {course.description}
        </p>

        <div className="text-muted-foreground mt-4 flex items-center gap-4 text-xs">
          <span className="flex items-center gap-1.5">
            <BookOpenIcon className="size-3.5" aria-hidden />
            {course.lesson_count > 0
              ? mn.courses.lessons(course.lesson_count)
              : mn.courses.noLessonsYet}
          </span>
          {course.duration > 0 && (
            <span className="flex items-center gap-1.5">
              <ClockIcon className="size-3.5" aria-hidden />
              {formatDuration(course.duration)}
            </span>
          )}
        </div>

        {course.progress && course.progress.total_lessons > 0 && (
          <ProgressBar progress={course.progress} className="mt-4" />
        )}
      </div>
    </article>
  );
}

export function CourseCardSkeleton() {
  return (
    <div className="bg-card overflow-hidden rounded-xl border">
      <div className="bg-muted aspect-video w-full animate-pulse" />
      <div className="space-y-3 p-5">
        <div className="flex gap-2">
          <div className="bg-muted h-5 w-20 animate-pulse rounded-full" />
          <div className="bg-muted h-5 w-24 animate-pulse rounded-full" />
        </div>
        <div className="bg-muted h-5 w-3/4 animate-pulse rounded" />
        <div className="bg-muted h-4 w-full animate-pulse rounded" />
        <div className="bg-muted h-4 w-2/3 animate-pulse rounded" />
        <div className="bg-muted h-3 w-1/2 animate-pulse rounded" />
      </div>
    </div>
  );
}
