import { Skeleton } from "@/components/ui/skeleton";

/** `withPlan` — өөрийн профайл: багцын мөрийн байрыг урьдчилан эзэлнэ. */
export function ProfileSkeleton({ withPlan = false }: { withPlan?: boolean }) {
  return (
    <div className="space-y-10">
      <div className="flex items-center gap-4">
        <Skeleton className="size-16 rounded-full" />
        <div className="space-y-2">
          <Skeleton className="h-8 w-56" />
          <Skeleton className="h-4 w-40" />
        </div>
      </div>
      {withPlan && <Skeleton className="h-[4.5rem] w-full rounded-xl" />}
      <div className="grid grid-cols-2 gap-3 sm:grid-cols-4 sm:gap-4">
        {Array.from({ length: 4 }, (_, index) => (
          <Skeleton key={index} className="h-16 w-full rounded-xl" />
        ))}
      </div>
      <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 sm:gap-4 lg:grid-cols-4 xl:grid-cols-5">
        {Array.from({ length: 10 }, (_, index) => (
          <Skeleton key={index} className="h-52 w-full rounded-xl" />
        ))}
      </div>
    </div>
  );
}
