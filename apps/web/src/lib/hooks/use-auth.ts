"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useRouter } from "next/navigation";

import * as authApi from "@/lib/api/auth";
import { ApiError } from "@/lib/api/client";
import { clearAuthHint, hasAuthHint } from "@/lib/auth-hint";
import { useIsHydrated } from "@/lib/hooks/use-hydrated";
import { queryKeys } from "@/lib/query-keys";
import type { User } from "@/lib/types/api";

export interface AuthState {
  user: User | null;
  /** Нэвтрэлтийн төлөв хараахан тодорхойгүй байна. */
  isLoading: boolean;
  isAuthenticated: boolean;
  isAdmin: boolean;
}

/**
 * Одоогийн хэрэглэгч.
 *
 * Token нь httpOnly cookie дотор байдаг тул JavaScript уншиж чадахгүй —
 * нэвтрэлтийн төлөвийг зөвхөн `/auth/me`-ээр л мэднэ. Гэхдээ сэжүүр cookie
 * байхгүй бол зочин гэж үзээд хүсэлт огт илгээхгүй.
 *
 * Hydration дуустал `isLoading` үргэлж `true` — сервер болон client-ийн анхны
 * HTML ялгаатай болохоос сэргийлнэ.
 */
export function useCurrentUser(): AuthState {
  const hydrated = useIsHydrated();
  const maybeSignedIn = hydrated && hasAuthHint();

  const query = useQuery<User | null>({
    queryKey: queryKeys.currentUser,
    queryFn: async () => {
      try {
        return await authApi.getCurrentUser();
      } catch (error) {
        // 401 бол "нэвтрээгүй" гэсэн хэвийн төлөв, алдаа биш.
        if (error instanceof ApiError && error.isUnauthorized) {
          clearAuthHint();
          return null;
        }
        throw error;
      }
    },
    enabled: maybeSignedIn,
    staleTime: 5 * 60_000,
    retry: false,
  });

  if (!hydrated) {
    return { user: null, isLoading: true, isAuthenticated: false, isAdmin: false };
  }
  if (!maybeSignedIn) {
    return { user: null, isLoading: false, isAuthenticated: false, isAdmin: false };
  }

  const user = query.data ?? null;
  return {
    user,
    isLoading: query.isPending,
    isAuthenticated: Boolean(user),
    isAdmin: user?.role === "admin",
  };
}

/** Нэвтэрсний дараа хуучин хэрэглэгчийн хариунууд хүчингүй болно. */
function useSignedIn() {
  const queryClient = useQueryClient();
  return (user: User) => {
    queryClient.setQueryData(queryKeys.currentUser, user);
    void queryClient.invalidateQueries({ queryKey: queryKeys.courses.all });
    void queryClient.invalidateQueries({ queryKey: queryKeys.me.courses });
    void queryClient.invalidateQueries({ queryKey: queryKeys.lessons.all });
  };
}

export function useLogin() {
  const onSuccess = useSignedIn();
  return useMutation({ mutationFn: authApi.login, onSuccess });
}

/** Имэйл баталгаажуулалт асаалттай бол `user` ирэхгүй — кодын алхам руу шилжинэ. */
export function useRegister() {
  const signedIn = useSignedIn();
  return useMutation({
    mutationFn: authApi.register,
    onSuccess: (result) => {
      if (result.user) signedIn(result.user);
    },
  });
}

export function useVerifyEmail() {
  const onSuccess = useSignedIn();
  return useMutation({ mutationFn: authApi.verifyEmail, onSuccess });
}

export function useResetPassword() {
  const onSuccess = useSignedIn();
  return useMutation({ mutationFn: authApi.resetPassword, onSuccess });
}

export function useLogout() {
  const queryClient = useQueryClient();
  const router = useRouter();

  return useMutation({
    mutationFn: authApi.logout,
    onSettled: () => {
      // Сервер дээр алдаа гарсан ч client талын төлөвийг цэвэрлэнэ.
      clearAuthHint();
      // `invalidate` биш `clear` — invalidate нь идэвхтэй query-г дахин
      // дуудаж, cookie-гүй болсон тул 401 үүсгэдэг. Гарахад бүх cache устана.
      queryClient.clear();
      router.push("/");
      router.refresh();
    },
  });
}
