import { AdminLessonEditor } from "@/components/admin/lesson-editor";

export default async function EditLessonPage({ params }: PageProps<"/admin/lessons/[id]">) {
  const { id } = await params;
  return <AdminLessonEditor lessonId={id} />;
}
