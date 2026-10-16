import { Badge } from "@/components/ui/badge";
import { mn } from "@/lib/i18n/mn";
import type { CourseSummary } from "@/lib/types/api";

/** «Үнэгүй» / «15 хичээл үнэгүй» / «Тун удахгүй». */
export function AccessBadge({ course }: { course: CourseSummary }) {
  if (course.is_free) return <Badge variant="secondary">{mn.courses.free}</Badge>;
  if (course.lesson_count === 0) return <Badge variant="outline">{mn.courses.comingSoon}</Badge>;
  return (
    <Badge variant="outline">
      {mn.courses.freeLessons(Math.min(course.free_lessons, course.lesson_count))}
    </Badge>
  );
}
