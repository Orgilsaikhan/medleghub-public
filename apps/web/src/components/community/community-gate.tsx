"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { BanIcon, BookOpenCheckIcon, PenSquareIcon } from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { toast } from "sonner";

import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { ApiError } from "@/lib/api/client";
import { acceptGuidelines, getCommunityStatus } from "@/lib/api/community";
import { formatDate } from "@/lib/format";
import { useCurrentUser } from "@/lib/hooks/use-auth";
import { mn } from "@/lib/i18n/mn";
import { queryKeys } from "@/lib/query-keys";

/** Дүрэм зөвшөөрсөн эсэх, түдгэлзүүлэлт. Нэг query-г бүх хэсэг хуваалцана. */
export function useCommunityStatus() {
  const { isAuthenticated } = useCurrentUser();
  return useQuery({
    queryKey: queryKeys.community.me,
    queryFn: getCommunityStatus,
    enabled: isAuthenticated,
    staleTime: 60_000,
  });
}

/** Түдгэлзсэн бол бичих, лайк дарах, мэдэгдэх товчийг нууна (сервер ч татгалзана). */
export function useIsSuspended(): boolean {
  return Boolean(useCommunityStatus().data?.suspension);
}

/**
 * Community-ийн хуудас бүрийн дээд хэсэг: түдгэлзсэн бол мэдэгдэл, дүрмийг
 * хараахан зөвшөөрөөгүй бол хаагдахгүй дүрмийн цонх (эхний удаа ороход).
 */
export function CommunityGate() {
  const { data } = useCommunityStatus();
  if (!data) return null;

  const { suspension } = data;
  return (
    <>
      {suspension && (
        <div
          role="status"
          className="border-destructive/40 bg-destructive/5 mb-6 flex gap-3 rounded-xl border p-4 text-sm"
        >
          <BanIcon aria-hidden className="text-destructive mt-0.5 size-5 shrink-0" />
          <div className="space-y-1">
            <p className="font-medium">
              {suspension.ends_at
                ? mn.community.suspendedUntil(formatDate(suspension.ends_at))
                : mn.community.suspendedForever}{" "}
              {mn.community.suspendedReadOnly}
            </p>
            <p className="text-muted-foreground break-words">
              {mn.community.suspendedReason(suspension.reason)}
            </p>
          </div>
        </div>
      )}
      {!data.guidelines_accepted && <GuidelinesDialog mode="accept" open onOpenChange={() => {}} />}
    </>
  );
}

interface GuidelinesDialogProps {
  /** `accept` — эхний удаа: зөвшөөрөх хүртэл хаагдахгүй. `read` — дахин унших. */
  mode: "accept" | "read";
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export function GuidelinesDialog({ mode, open, onOpenChange }: GuidelinesDialogProps) {
  const router = useRouter();
  const queryClient = useQueryClient();
  const { data } = useCommunityStatus();
  const days = data?.suspension_days ?? [];
  const forced = mode === "accept";

  const accept = useMutation({
    mutationFn: acceptGuidelines,
    onSuccess: (status) => queryClient.setQueryData(queryKeys.community.me, status),
    onError: (error) =>
      toast.error(error instanceof ApiError ? error.message : mn.common.somethingWrong),
  });

  const text = mn.community.guidelines;

  return (
    <Dialog open={open} onOpenChange={forced ? undefined : onOpenChange}>
      <DialogContent
        showCloseButton={!forced}
        className="max-h-[90dvh] overflow-y-auto sm:max-w-lg"
        onEscapeKeyDown={forced ? (event) => event.preventDefault() : undefined}
        onInteractOutside={forced ? (event) => event.preventDefault() : undefined}
      >
        <DialogHeader>
          <DialogTitle>{text.title}</DialogTitle>
          <DialogDescription>{text.intro}</DialogDescription>
        </DialogHeader>

        <ol className="list-decimal space-y-1.5 pl-5 text-sm">
          {text.rules.map((rule) => (
            <li key={rule}>{rule}</li>
          ))}
        </ol>

        <section aria-labelledby="guidelines-penalties" className="space-y-2 text-sm">
          <h3 id="guidelines-penalties" className="font-semibold">
            {text.penaltiesTitle}
          </h3>
          <p className="text-muted-foreground">{text.penaltiesIntro}</p>
          {days.length > 0 && (
            <ul className="border-destructive/30 bg-destructive/5 space-y-1 rounded-lg border p-3">
              {days.map((count, index) => (
                <li key={count}>{text.penaltyStep(index + 1, count)}</li>
              ))}
              <li className="font-medium">{text.penaltyPermanent(days.length + 1)}</li>
            </ul>
          )}
          <p className="text-muted-foreground">{text.outro}</p>
        </section>

        <DialogFooter>
          {forced ? (
            <>
              <Button variant="outline" onClick={() => router.push("/dashboard")}>
                {text.leave}
              </Button>
              <Button onClick={() => accept.mutate()} disabled={accept.isPending}>
                {accept.isPending ? text.accepting : text.accept}
              </Button>
            </>
          ) : (
            <Button variant="outline" onClick={() => onOpenChange(false)}>
              {text.close}
            </Button>
          )}
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}

/** Толгойн товчнууд: дүрмийг дахин унших, нийтлэл бичих (түдгэлзсэн бол нуугдана). */
export function CommunityActions() {
  const [open, setOpen] = useState(false);
  const { isAuthenticated } = useCurrentUser();
  const suspended = useIsSuspended();

  return (
    <div className="flex items-center gap-2">
      {isAuthenticated && (
        <>
          <Button variant="outline" onClick={() => setOpen(true)}>
            <BookOpenCheckIcon className="size-4" />
            {mn.community.guidelines.open}
          </Button>
          <GuidelinesDialog mode="read" open={open} onOpenChange={setOpen} />
        </>
      )}
      {!suspended && (
        <Button asChild>
          <Link href="/community/new">
            <PenSquareIcon className="size-4" />
            {mn.community.newPost}
          </Link>
        </Button>
      )}
    </div>
  );
}
