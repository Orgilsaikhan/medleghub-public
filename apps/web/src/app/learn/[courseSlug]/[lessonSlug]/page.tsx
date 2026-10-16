import type { Metadata } from "next";

import { RequireAuth } from "@/components/auth/require-auth";
import { LessonSkeleton } from "@/components/learn/lesson-skeleton";
import { LessonView } from "@/components/learn/lesson-view";
import { mn } from "@/lib/i18n/mn";

export const metadata: Metadata = {
  title: mn.learn.lessonContent,
  // Хичээлийн хуудас нь хувийн агуулга — хайлтын системд индекслэхгүй.
  robots: { index: false, follow: false },
};

export default async function LessonPage({
  params,
}: PageProps<"/learn/[courseSlug]/[lessonSlug]">) {
  const { courseSlug, lessonSlug } = await params;

  return (
    <RequireAuth fallback={<LessonSkeleton />}>
      <LessonView courseSlug={courseSlug} lessonSlug={lessonSlug} />
    </RequireAuth>
  );
}
