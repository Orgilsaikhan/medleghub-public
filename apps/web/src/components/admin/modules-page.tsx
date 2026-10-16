"use client";

import { useQuery } from "@tanstack/react-query";
import Link from "next/link";

import { AdminPageHeader } from "@/components/admin/page-header";
import { CurriculumBuilder } from "@/components/admin/curriculum-builder";
import { Button } from "@/components/ui/button";
import { getAdminCourse } from "@/lib/api/admin";
import { mn } from "@/lib/i18n/mn";
import { queryKeys } from "@/lib/query-keys";

export function AdminModulesPage({ courseId }: { courseId: string }) {
  const { data } = useQuery({
    queryKey: queryKeys.admin.course(courseId),
    queryFn: () => getAdminCourse(courseId),
  });

  return (
    <>
      <AdminPageHeader
        title={data?.title ?? mn.admin.modules}
        description={mn.admin.subtitle}
        backHref="/admin/courses"
        action={
          <Button asChild variant="outline">
            <Link href={`/admin/courses/${courseId}`}>{mn.admin.editCourse}</Link>
          </Button>
        }
      />
      <CurriculumBuilder courseId={courseId} />
    </>
  );
}
