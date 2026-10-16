import { PlusIcon } from "lucide-react";
import Link from "next/link";

import { AdminCourseList } from "@/components/admin/course-list";
import { AdminPageHeader } from "@/components/admin/page-header";
import { Button } from "@/components/ui/button";
import { mn } from "@/lib/i18n/mn";

export default function AdminCoursesPage() {
  return (
    <>
      <AdminPageHeader
        title={mn.admin.courses}
        action={
          <Button asChild>
            <Link href="/admin/courses/new">
              <PlusIcon className="size-4" />
              {mn.admin.newCourse}
            </Link>
          </Button>
        }
      />
      <AdminCourseList />
    </>
  );
}
