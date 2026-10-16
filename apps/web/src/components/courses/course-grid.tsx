import { CourseCard, CourseCardSkeleton } from "@/components/courses/course-card";
import type { CourseSummary } from "@/lib/types/api";
import { cn } from "@/lib/utils";

/**
 * `wide` — сургалтын жагсаалт: маш өргөн дэлгэцэд 4 багана, карт хэт
 * томрохгүй. Нүүр хуудасны 3 онцлох сургалт 3 баганадаа үлдэнэ.
 */
function gridClass(wide: boolean) {
  return cn("grid gap-6 sm:grid-cols-2 lg:grid-cols-3", wide && "2xl:grid-cols-4");
}

export function CourseGrid({
  courses,
  wide = false,
}: {
  courses: CourseSummary[];
  wide?: boolean;
}) {
  return (
    <div className={gridClass(wide)}>
      {courses.map((course) => (
        <CourseCard key={course.id} course={course} />
      ))}
    </div>
  );
}

export function CourseGridSkeleton({
  count = 6,
  wide = false,
}: {
  count?: number;
  wide?: boolean;
}) {
  return (
    <div className={gridClass(wide)}>
      {Array.from({ length: count }, (_, index) => (
        <CourseCardSkeleton key={index} />
      ))}
    </div>
  );
}
