import { AdminModulesPage } from "@/components/admin/modules-page";

export default async function CourseModulesPage({
  params,
}: PageProps<"/admin/courses/[id]/modules">) {
  const { id } = await params;
  return <AdminModulesPage courseId={id} />;
}
