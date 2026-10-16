import { AdminPageHeader } from "@/components/admin/page-header";
import { CourseForm } from "@/components/admin/course-form";
import { mn } from "@/lib/i18n/mn";

export default function NewCoursePage() {
  return (
    <>
      <AdminPageHeader title={mn.admin.newCourse} backHref="/admin/courses" />
      <CourseForm />
    </>
  );
}
