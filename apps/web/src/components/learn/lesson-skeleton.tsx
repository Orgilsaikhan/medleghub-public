import { Skeleton } from "@/components/ui/skeleton";

export function LessonSkeleton() {
  return (
    <div className="flex min-h-0 flex-1">
      <aside className="hidden w-72 shrink-0 space-y-3 border-r p-4 lg:block xl:w-80">
        <Skeleton className="h-4 w-28" />
        <Skeleton className="h-5 w-44" />
        <Skeleton className="h-2 w-full" />
        <div className="space-y-2 pt-4">
          {Array.from({ length: 6 }, (_, index) => (
            <Skeleton key={index} className="h-9 w-full" />
          ))}
        </div>
      </aside>

      <div className="flex min-h-0 min-w-0 flex-1 flex-col">
        <Skeleton className="aspect-video w-full rounded-none" />
        <div className="space-y-3 px-4 py-6 sm:px-6 lg:px-8">
          <Skeleton className="h-7 w-1/2" />
          <Skeleton className="h-4 w-full" />
          <Skeleton className="h-4 w-5/6" />
          <Skeleton className="h-4 w-2/3" />
        </div>
        <Skeleton className="h-64 w-full rounded-none" />
      </div>
    </div>
  );
}
