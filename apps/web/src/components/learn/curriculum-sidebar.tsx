"use client";

import { ChevronLeftIcon } from "lucide-react";
import Link from "next/link";

import { CurriculumList } from "@/components/courses/curriculum-list";
import { ProgressBar } from "@/components/courses/progress-bar";
import { mn } from "@/lib/i18n/mn";
import type { CourseProgress, ModuleWithLessons } from "@/lib/types/api";

interface CurriculumSidebarProps {
  courseTitle: string;
  courseSlug: string;
  modules: ModuleWithLessons[];
  progress: CourseProgress;
  currentSlug: string;
}

export function CurriculumSidebar({
  courseTitle,
  courseSlug,
  modules,
  progress,
  currentSlug,
}: CurriculumSidebarProps) {
  return (
    <div className="flex h-full flex-col">
      <div className="shrink-0 border-b p-4">
        <Link
          href={`/courses/${courseSlug}`}
          className="text-muted-foreground hover:text-foreground inline-flex items-center gap-1 text-xs transition-colors"
        >
          <ChevronLeftIcon className="size-3.5" aria-hidden />
          {mn.learn.backToCourse}
        </Link>

        <h2 className="mt-2 text-sm leading-snug font-semibold">{courseTitle}</h2>

        <ProgressBar progress={progress} className="mt-3" />
      </div>

      <nav aria-label={mn.learn.curriculum} className="min-h-0 flex-1 overflow-y-auto p-4">
        <CurriculumList
          modules={modules}
          courseSlug={courseSlug}
          linkLessons
          currentSlug={currentSlug}
        />
      </nav>
    </div>
  );
}
