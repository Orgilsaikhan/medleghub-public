"use client";

import { keepPreviousData, useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import {
  CheckIcon,
  ChevronLeftIcon,
  ChevronRightIcon,
  MessageSquareIcon,
  UndoIcon,
} from "lucide-react";
import Link from "next/link";
import { useState } from "react";
import { toast } from "sonner";

import { EmptyState, ErrorState } from "@/components/common/states";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { listFeedback, setFeedbackResolved } from "@/lib/api/admin";
import { ApiError } from "@/lib/api/client";
import { formatDate } from "@/lib/format";
import { mn } from "@/lib/i18n/mn";
import { queryKeys } from "@/lib/query-keys";
import type { FeedbackItem } from "@/lib/types/api";
import { cn } from "@/lib/utils";

const PAGE_SIZE = 20;

/** Хэрэглэгчдийн санал хүсэлт — шинэ нь эхэндээ, анхдагчаар шийдээгүйг нь. */
export function AdminFeedbackList() {
  const queryClient = useQueryClient();
  const [showAll, setShowAll] = useState(false);
  const [page, setPage] = useState(1);

  const params = { resolved: showAll ? undefined : false, page, page_size: PAGE_SIZE };
  const query = useQuery({
    queryKey: queryKeys.admin.feedback(params),
    queryFn: () => listFeedback(params),
    placeholderData: keepPreviousData,
  });

  const toggle = useMutation({
    mutationFn: (item: FeedbackItem) => setFeedbackResolved(item.id, !item.resolved),
    onSuccess: () => void queryClient.invalidateQueries({ queryKey: queryKeys.admin.feedbackAll }),
    onError: (error) =>
      toast.error(error instanceof ApiError ? error.message : mn.common.somethingWrong),
  });

  function selectFilter(all: boolean) {
    setShowAll(all);
    setPage(1);
  }

  return (
    <div className="space-y-4">
      <div role="group" aria-label={mn.admin.feedback} className="flex gap-1">
        <Button
          size="sm"
          variant={showAll ? "ghost" : "secondary"}
          aria-pressed={!showAll}
          onClick={() => selectFilter(false)}
        >
          {mn.admin.feedbackOpen}
        </Button>
        <Button
          size="sm"
          variant={showAll ? "secondary" : "ghost"}
          aria-pressed={showAll}
          onClick={() => selectFilter(true)}
        >
          {mn.admin.feedbackAll}
        </Button>
      </div>

      {query.isPending ? (
        <div className="space-y-3">
          {Array.from({ length: 4 }, (_, index) => (
            <Skeleton key={index} className="h-28 w-full" />
          ))}
        </div>
      ) : query.isError ? (
        <ErrorState onRetry={() => void query.refetch()} />
      ) : query.data.items.length === 0 ? (
        <EmptyState icon={MessageSquareIcon} title={mn.admin.feedbackEmpty} />
      ) : (
        <>
          <ul className="divide-y rounded-xl border">
            {query.data.items.map((item) => (
              <li key={item.id} className={cn("space-y-2 p-4", item.resolved && "opacity-70")}>
                <div className="flex flex-wrap items-center gap-2 text-xs">
                  {/* `destructive` хувилбарын цайвар дэвсгэр гэрэл горимд 4.5:1-д хүрдэггүй —
                      хүрээтэй, улаан текстээр. */}
                  <Badge
                    variant="outline"
                    className={cn(
                      (item.kind === "bug" || item.kind === "report") &&
                        "border-destructive/40 text-destructive",
                    )}
                  >
                    {mn.feedback.kinds[item.kind]}
                  </Badge>
                  {item.resolved && <Badge variant="secondary">{mn.admin.feedbackResolved}</Badge>}
                  <span className="text-muted-foreground">{formatDate(item.created_at)}</span>
                </div>

                <p className="text-sm break-words whitespace-pre-wrap">{item.message}</p>

                <div className="flex flex-wrap items-center justify-between gap-3">
                  <p className="text-muted-foreground flex flex-wrap items-center gap-x-3 text-xs">
                    <span className="text-foreground font-medium">{item.user.name}</span>
                    <a href={`mailto:${item.user.email}`} className="hover:underline">
                      {item.user.email}
                    </a>
                    {/* Backend зөвхөн `/`-ээр эхэлсэн дотоод замыг хүлээж авдаг. */}
                    {item.page && (
                      <Link href={item.page} className="font-mono hover:underline">
                        {item.page}
                      </Link>
                    )}
                  </p>

                  <Button
                    size="sm"
                    variant="outline"
                    disabled={toggle.isPending && toggle.variables?.id === item.id}
                    onClick={() => toggle.mutate(item)}
                  >
                    {item.resolved ? (
                      <>
                        <UndoIcon className="size-4" />
                        {mn.admin.feedbackReopen}
                      </>
                    ) : (
                      <>
                        <CheckIcon className="size-4" />
                        {mn.admin.feedbackResolve}
                      </>
                    )}
                  </Button>
                </div>
              </li>
            ))}
          </ul>

          {query.data.total_pages > 1 && (
            <nav
              aria-label={mn.common.page(page, query.data.total_pages)}
              className="flex items-center justify-center gap-4"
            >
              <Button
                variant="outline"
                size="sm"
                disabled={page <= 1}
                onClick={() => setPage(page - 1)}
              >
                <ChevronLeftIcon className="size-4" />
                {mn.common.previous}
              </Button>
              <span className="text-muted-foreground text-sm tabular-nums">
                {mn.common.page(page, query.data.total_pages)}
              </span>
              <Button
                variant="outline"
                size="sm"
                disabled={page >= query.data.total_pages}
                onClick={() => setPage(page + 1)}
              >
                {mn.common.next}
                <ChevronRightIcon className="size-4" />
              </Button>
            </nav>
          )}
        </>
      )}
    </div>
  );
}
