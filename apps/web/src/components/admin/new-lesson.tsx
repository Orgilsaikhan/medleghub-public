"use client";

import { useSearchParams } from "next/navigation";

import { AdminPageHeader } from "@/components/admin/page-header";
import { LessonForm } from "@/components/admin/lesson-form";
import { ErrorState } from "@/components/common/states";
import { mn } from "@/lib/i18n/mn";

/** Шинэ хичээл нь `?module=…&course=…` параметрээр аль модулд орохоо мэднэ. */
export function AdminNewLesson() {
  const params = useSearchParams();
  const moduleId = params.get("module");
  const courseId = params.get("course") ?? undefined;

  if (!moduleId) {
    return <ErrorState title={mn.common.error} description={mn.admin.emptyModules} />;
  }

  return (
    <>
      <AdminPageHeader
        title={mn.admin.newLesson}
        backHref={courseId ? `/admin/courses/${courseId}/modules` : "/admin/courses"}
      />
      <LessonForm moduleId={moduleId} courseId={courseId} />
    </>
  );
}
