import { Skeleton } from "@/components/ui/skeleton";

export default function CourseDetailLoading() {
  return (
    <div className="container-page py-10 lg:py-14">
      <div className="grid gap-10 lg:grid-cols-[1fr_22rem] lg:gap-14">
        <div className="space-y-4">
          <Skeleton className="h-6 w-56" />
          <Skeleton className="h-10 w-3/4" />
          <Skeleton className="h-4 w-full" />
          <Skeleton className="h-4 w-5/6" />

          <div className="space-y-3 pt-10">
            <Skeleton className="h-6 w-40" />
            {Array.from({ length: 5 }, (_, index) => (
              <Skeleton key={index} className="h-10 w-full" />
            ))}
          </div>
        </div>
        <Skeleton className="hidden h-80 w-full lg:block" />
      </div>
    </div>
  );
}
