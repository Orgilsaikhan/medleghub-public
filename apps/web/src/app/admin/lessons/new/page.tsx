import { Suspense } from "react";

import { AdminNewLesson } from "@/components/admin/new-lesson";
import { Skeleton } from "@/components/ui/skeleton";

export default function NewLessonPage() {
  return (
    <Suspense fallback={<Skeleton className="h-96 w-full" />}>
      <AdminNewLesson />
    </Suspense>
  );
}
