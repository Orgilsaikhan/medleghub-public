"use client";

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";
import { toast } from "sonner";

import { updateAccount } from "@/lib/api/account";
import { ApiError } from "@/lib/api/client";
import { useCurrentUser } from "@/lib/hooks/use-auth";
import { useIsHydrated } from "@/lib/hooks/use-hydrated";
import { mn } from "@/lib/i18n/mn";
import { readLocal, writeLocal } from "@/lib/local-storage";
import { queryKeys } from "@/lib/query-keys";
import type { EditorLayout, User } from "@/lib/types/api";

/** Нэвтрээгүй зочны сонголт — зөвхөн энэ хөтөчид. */
const GUEST_KEY = "medleghub:editor-layout";

/**
 * Хичээлийн засварлагчийн байрлал. Нэвтэрсэн бол бүртгэлд (`users.editor_layout`)
 * хадгалагдаж бүх төхөөрөмжид дагана, эс бөгөөс хөтөчид. Анхдагч нь `new`.
 */
export function useEditorLayout() {
  const { user } = useCurrentUser();
  const queryClient = useQueryClient();
  const hydrated = useIsHydrated();
  const [guestChoice, setGuestChoice] = useState<EditorLayout | null>(null);
  const stored = hydrated && readLocal(GUEST_KEY, "new") === "legacy" ? "legacy" : "new";
  const layout: EditorLayout = user ? user.editor_layout : (guestChoice ?? stored);

  const mutation = useMutation({
    mutationFn: (next: EditorLayout) => updateAccount({ editor_layout: next }),
    // Шууд сольж харуулна — хадгалж чадаагүй бол буцаана.
    onMutate: (next) => {
      const previous = queryClient.getQueryData<User>(queryKeys.currentUser);
      if (previous)
        queryClient.setQueryData(queryKeys.currentUser, { ...previous, editor_layout: next });
      return { previous };
    },
    onSuccess: (updated) => queryClient.setQueryData(queryKeys.currentUser, updated),
    onError: (error, _next, context) => {
      if (context?.previous) queryClient.setQueryData(queryKeys.currentUser, context.previous);
      toast.error(error instanceof ApiError ? error.message : mn.common.somethingWrong);
    },
  });

  const setLayout = (next: EditorLayout) => {
    if (user) {
      mutation.mutate(next);
    } else {
      writeLocal(GUEST_KEY, next);
      setGuestChoice(next);
    }
  };

  return { layout, setLayout, saving: mutation.isPending };
}
