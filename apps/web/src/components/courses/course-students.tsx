"use client";

import { useQuery } from "@tanstack/react-query";
import Link from "next/link";
import { useId } from "react";

import { UserAvatar } from "@/components/common/user-avatar";
import { Skeleton } from "@/components/ui/skeleton";
import { getCourseStudents } from "@/lib/api/community";
import { useCurrentUser } from "@/lib/hooks/use-auth";
import { mn } from "@/lib/i18n/mn";
import { queryKeys } from "@/lib/query-keys";
import { cn } from "@/lib/utils";

/**
 * Сургалтын суралцагчид — зураг, нэр, энэ сургалтын ахиц. Нэр дээр дарахад
 * тухайн хүний профайл нээгдэнэ.
 *
 * Зөвхөн нэвтэрсэн хэрэглэгчид харагдана (API ч нэвтрэлт шаардана) — нэр,
 * зургийг зочинд ил гаргахгүй. Жагсаалт нь эцэг элементийн өндрөөр хязгаарлагдаж
 * дотроо гүйлгэгдэнэ (`min-h-0`) — sticky хажуу самбар дэлгэцээс хэтрэхгүй.
 */
export function CourseStudents({ slug, className }: { slug: string; className?: string }) {
  const { user, isAuthenticated } = useCurrentUser();
  // Нэг хуудсанд хоёр удаа (гар утас, desktop) render хийгддэг — id давхцахгүй.
  const titleId = useId();

  const query = useQuery({
    queryKey: queryKeys.courses.students(slug),
    queryFn: () => getCourseStudents(slug),
    enabled: isAuthenticated,
    staleTime: 60_000,
  });

  // Жагсаалт нэмэлт мэдээлэл — алдаа гарвал хуудсыг бохирдуулахгүй.
  if (!isAuthenticated || query.isError) return null;

  const hidden = query.data ? query.data.total - query.data.items.length : 0;

  return (
    <section
      aria-labelledby={titleId}
      className={cn("bg-card flex min-h-0 flex-col rounded-xl border", className)}
    >
      <div className="flex items-baseline justify-between gap-3 border-b px-6 py-4">
        <h2 id={titleId} className="text-sm font-medium">
          {mn.community.studentsTitle}
        </h2>
        {query.data && (
          <span className="text-muted-foreground text-xs tabular-nums">
            {mn.community.studentsCount(query.data.total)}
          </span>
        )}
      </div>

      {query.isPending ? (
        <div className="space-y-3 px-6 py-4">
          {Array.from({ length: 4 }, (_, index) => (
            <div key={index} className="flex items-center gap-3">
              <Skeleton className="size-8 rounded-full" />
              <Skeleton className="h-4 flex-1" />
            </div>
          ))}
        </div>
      ) : query.data.items.length === 0 ? (
        <p className="text-muted-foreground px-6 py-4 text-sm">{mn.community.studentsEmpty}</p>
      ) : (
        <ul className="max-h-96 min-h-0 overflow-y-auto p-2">
          {query.data.items.map((student) => {
            const isMe = student.id === user?.id;
            return (
              <li key={student.id}>
                <Link
                  href={isMe ? "/profile" : `/users/${student.id}`}
                  className="hover:bg-accent focus-visible:bg-accent flex items-center gap-3 rounded-lg px-4 py-2 transition-colors"
                >
                  <UserAvatar user={student} className="size-8" fallbackClassName="text-xs" />
                  <span className="min-w-0 flex-1 truncate text-sm">
                    {student.name}
                    {isMe && <span className="text-muted-foreground"> ({mn.community.you})</span>}
                  </span>
                  <span className="text-muted-foreground text-xs tabular-nums">
                    <span className="sr-only">{mn.community.progress}: </span>
                    {student.percent}%
                  </span>
                </Link>
              </li>
            );
          })}
        </ul>
      )}

      {hidden > 0 && (
        <p className="text-muted-foreground border-t px-6 py-3 text-xs">
          {mn.community.studentsMore(hidden)}
        </p>
      )}
    </section>
  );
}
