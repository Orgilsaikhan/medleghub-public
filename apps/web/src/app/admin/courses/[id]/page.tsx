import { AdminCourseEditor } from "@/components/admin/course-editor";

export default async function EditCoursePage({ params }: PageProps<"/admin/courses/[id]">) {
  const { id } = await params;
  return <AdminCourseEditor courseId={id} />;
}
