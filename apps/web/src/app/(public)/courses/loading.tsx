import { CourseGridSkeleton } from "@/components/courses/course-grid";
import { Skeleton } from "@/components/ui/skeleton";

export default function CoursesLoading() {
  return (
    <div className="container-page py-10 lg:py-14">
      <Skeleton className="h-10 w-64" />
      <Skeleton className="mt-3 h-5 w-96 max-w-full" />
      <div className="mt-10">
        <CourseGridSkeleton wide />
      </div>
    </div>
  );
}
