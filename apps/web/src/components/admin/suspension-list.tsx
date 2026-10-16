"use client";

import { keepPreviousData, useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { ChevronLeftIcon, ChevronRightIcon, ShieldCheckIcon, UndoIcon } from "lucide-react";
import { useState } from "react";
import { toast } from "sonner";

import { EmptyState, ErrorState } from "@/components/common/states";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { liftSuspension, listSuspensions } from "@/lib/api/admin";
import { ApiError } from "@/lib/api/client";
import { formatDate } from "@/lib/format";
import { mn } from "@/lib/i18n/mn";
import { queryKeys } from "@/lib/query-keys";
import type { SuspensionItem } from "@/lib/types/api";
import { cn } from "@/lib/utils";

const PAGE_SIZE = 20;

function stateLabel(item: SuspensionItem): string {
  if (item.active) return mn.admin.suspensionStateActive;
  return item.lifted_at ? mn.admin.suspensionStateLifted : mn.admin.suspensionStateEnded;
}

/**
 * Community-ийн түдгэлзүүлэлтүүд — шинэ нь эхэндээ, анхдагчаар идэвхтэйг нь.
 * Цуцалсан түдгэлзүүлэлт дараагийн удааг тоолоход орохгүй.
 */
export function SuspensionList() {
  const queryClient = useQueryClient();
  const [showAll, setShowAll] = useState(false);
  const [page, setPage] = useState(1);

  const params = { active: showAll ? undefined : true, page, page_size: PAGE_SIZE };
  const query = useQuery({
    queryKey: queryKeys.admin.suspensions(params),
    queryFn: () => listSuspensions(params),
    placeholderData: keepPreviousData,
  });

  const lift = useMutation({
    mutationFn: (item: SuspensionItem) => liftSuspension(item.id),
    onSuccess: () => {
      toast.success(mn.admin.suspensionLifted);
      void queryClient.invalidateQueries({ queryKey: queryKeys.admin.suspensionsAll });
    },
    onError: (error) =>
      toast.error(error instanceof ApiError ? error.message : mn.common.somethingWrong),
  });

  function selectFilter(all: boolean) {
    setShowAll(all);
    setPage(1);
  }

  return (
    <div className="space-y-4">
      <div role="group" aria-label={mn.admin.community} className="flex gap-1">
        <Button
          size="sm"
          variant={showAll ? "ghost" : "secondary"}
          aria-pressed={!showAll}
          onClick={() => selectFilter(false)}
        >
          {mn.admin.suspensionsActive}
        </Button>
        <Button
          size="sm"
          variant={showAll ? "secondary" : "ghost"}
          aria-pressed={showAll}
          onClick={() => selectFilter(true)}
        >
          {mn.admin.suspensionsAll}
        </Button>
      </div>

      {query.isPending ? (
        <div className="space-y-3">
          {Array.from({ length: 3 }, (_, index) => (
            <Skeleton key={index} className="h-28 w-full" />
          ))}
        </div>
      ) : query.isError ? (
        <ErrorState onRetry={() => void query.refetch()} />
      ) : query.data.items.length === 0 ? (
        <EmptyState icon={ShieldCheckIcon} title={mn.admin.suspensionsEmpty} />
      ) : (
        <>
          <ul className="divide-y rounded-xl border">
            {query.data.items.map((item) => (
              <li key={item.id} className={cn("space-y-2 p-4", !item.active && "opacity-80")}>
                <div className="flex flex-wrap items-center gap-2 text-xs">
                  <Badge
                    variant="outline"
                    className={cn(item.active && "border-destructive/40 text-destructive")}
                  >
                    {stateLabel(item)}
                  </Badge>
                  <Badge variant="secondary">{mn.admin.suspensionLevel(item.level)}</Badge>
                  <span className="text-muted-foreground">
                    {item.ends_at
                      ? mn.admin.suspensionPeriod(
                          formatDate(item.created_at),
                          formatDate(item.ends_at),
                        )
                      : mn.admin.suspensionPermanent(formatDate(item.created_at))}
                  </span>
                </div>

                <p className="text-sm break-words whitespace-pre-wrap">{item.reason}</p>

                <div className="flex flex-wrap items-center justify-between gap-3">
                  <p className="text-muted-foreground flex flex-wrap items-center gap-x-3 text-xs">
                    <span className="text-foreground font-medium">{item.user.name}</span>
                    <a href={`mailto:${item.user.email}`} className="hover:underline">
                      {item.user.email}
                    </a>
                    <span>
                      {item.admin
                        ? mn.admin.suspensionBy(item.admin.name)
                        : mn.admin.suspensionByDeleted}
                    </span>
                  </p>

                  {item.active && (
                    <Button
                      size="sm"
                      variant="outline"
                      disabled={lift.isPending && lift.variables?.id === item.id}
                      onClick={() => lift.mutate(item)}
                    >
                      <UndoIcon className="size-4" />
                      {mn.admin.suspensionLift}
                    </Button>
                  )}
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
