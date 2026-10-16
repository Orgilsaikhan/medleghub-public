"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useCallback, useEffect, useRef } from "react";
import { toast } from "sonner";

import { ApiError } from "@/lib/api/client";
import {
  getGeneration,
  getLiveConfig,
  getMaterial,
  listMaterials,
  requestGeneration,
  retryMaterial,
} from "@/lib/api/live";
import { useCurrentUser } from "@/lib/hooks/use-auth";
import { mn } from "@/lib/i18n/mn";
import {
  GENERATION_POLL_MS,
  MATERIAL_POLL_MS,
  isGenerating,
  isMaterialProcessing,
} from "@/lib/live";
import { queryKeys } from "@/lib/query-keys";
import type { LiveGenerationKind, LiveMaterialDetail, LiveMaterialSummary } from "@/lib/types/live";

export function liveErrorMessage(error: unknown): string {
  return error instanceof ApiError ? error.message : mn.common.somethingWrong;
}

/**
 * Энэ хэрэглэгчид Live нээлттэй эсэх, хязгаар, хэрэглээ.
 *
 * Толгойн «Live» холбоос ч үүнийг ашигладаг тул зөвхөн нэвтэрсэн үед дуудна.
 * Хэрэглэгч солигдоход хариу өөр тул key-д id орно.
 */
export function useLiveConfig({ staleTime = 5 * 60_000 }: { staleTime?: number } = {}) {
  const { user } = useCurrentUser();
  return useQuery({
    queryKey: queryKeys.live.config(user?.id ?? "guest"),
    queryFn: getLiveConfig,
    enabled: Boolean(user),
    staleTime,
  });
}

/** Материалын жагсаалт. AI задалж буй материал байвал 3 сек тутам шалгана. */
export function useLiveMaterials() {
  return useQuery({
    queryKey: queryKeys.live.materials,
    queryFn: listMaterials,
    staleTime: 10_000,
    refetchInterval: (query) =>
      query.state.data?.some((material) => isMaterialProcessing(material.status))
        ? MATERIAL_POLL_MS
        : false,
  });
}

/** Нэг материал — хэсэг, сэдэв, эзэмшил. Задлагдаж байх зуур 3 сек тутам шалгана. */
export function useLiveMaterial(materialId: string) {
  return useQuery({
    queryKey: queryKeys.live.material(materialId),
    queryFn: () => getMaterial(materialId),
    staleTime: 10_000,
    refetchInterval: (query) =>
      isMaterialProcessing(query.state.data?.status) ? MATERIAL_POLL_MS : false,
  });
}

/**
 * Эзэмшил өөрчлөгдсөний дараа (заавар уншсан, карт давтсан, тест дууссан)
 * материал болон жагсаалтыг хуучирсан гэж тэмдэглэнэ.
 *
 * `refetch: false` — дараагийн удаа нээхэд л дахин татна (карт бүрийн дараа
 * нээлттэй хуудсыг дахин татахгүй).
 */
export function useInvalidateMaterial(materialId: string) {
  const queryClient = useQueryClient();
  return useCallback(
    ({ refetch = true }: { refetch?: boolean } = {}) => {
      const refetchType = refetch ? "active" : "none";
      void queryClient.invalidateQueries({
        queryKey: queryKeys.live.material(materialId),
        refetchType,
      });
      void queryClient.invalidateQueries({ queryKey: queryKeys.live.materials, refetchType });
    },
    [queryClient, materialId],
  );
}

/** Амжилтгүй болсон материалыг дахин боловсруулна — төлөв `queued` болж, шалгалт сэргэнэ. */
export function useRetryMaterial(materialId: string) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: () => retryMaterial(materialId),
    onSuccess: (summary) => {
      queryClient.setQueryData<LiveMaterialSummary[]>(queryKeys.live.materials, (list) =>
        list?.map((item) => (item.id === summary.id ? summary : item)),
      );
      queryClient.setQueryData<LiveMaterialDetail>(queryKeys.live.material(materialId), (detail) =>
        detail ? { ...detail, ...summary } : detail,
      );
      void queryClient.invalidateQueries({ queryKey: queryKeys.live.material(materialId) });
      void queryClient.invalidateQueries({ queryKey: queryKeys.live.materials });
      toast.success(mn.live.retried);
    },
    onError: (error) => toast.error(liveErrorMessage(error)),
  });
}

/**
 * Заавар, тест, шалгалтын таамаг.
 *
 * Хэрэгслийг нээхэд `requestGeneration` дуудна — idempotent: бэлэн эсвэл
 * бэлтгэгдэж буй нь байвал түүнийг буцаана, AI-г дахин дуудахгүй. Тиймээс
 * mutation биш query болгосон: strict mode-ийн давхар effect, давхар mount-ыг
 * TanStack нэг хүсэлт болгож нэгтгэнэ. Дараа нь бэлэн болтол 2 сек тутам
 * `getGeneration`.
 *
 * `enabled` — материал бэлэн болсон үед л (эс бөгөөс сервер 409 буцаана).
 */
export function useLiveGeneration(
  materialId: string,
  kind: LiveGenerationKind,
  topicId: string | null,
  enabled: boolean,
) {
  const queryClient = useQueryClient();
  const invalidateMaterial = useInvalidateMaterial(materialId);
  const requestKey = queryKeys.live.generationRequest(materialId, kind, topicId);

  const request = useQuery({
    queryKey: requestKey,
    queryFn: async () => {
      const generation = await requestGeneration(materialId, { kind, topic_id: topicId });
      queryClient.setQueryData(queryKeys.live.generation(generation.id), generation);
      return generation;
    },
    enabled,
    // Хэрэгслийг дахин нээх бүрд серверээс асууна (бэлэн бол шууд буцаана).
    staleTime: 0,
    gcTime: 60_000,
    retry: false,
    // POST тул цонх руу буцах, сүлжээ сэргэхэд дахин илгээхгүй (анхдагч тохиргоо
    // өөрчлөгдсөн ч).
    refetchOnWindowFocus: false,
    refetchOnReconnect: false,
  });

  const generationId = request.data?.id ?? null;
  const generation = useQuery({
    queryKey: queryKeys.live.generation(generationId ?? ""),
    queryFn: () => getGeneration(generationId ?? ""),
    enabled: generationId !== null,
    refetchInterval: (query) =>
      isGenerating(query.state.data?.status) ? GENERATION_POLL_MS : false,
  });

  // Материалын баруун баганын төлөв («Эхлээгүй» → «Бэлтгэж байна» → «Бэлэн»),
  // AI хэрэглээний хувь өөрчлөгдөнө — энэ хуудсан дээр бэлтгэгдсэн үүсгэлт бүрт
  // эхлэх, дуусахад нэг нэг удаа. Аль хэдийн бэлэн байсныг нээхэд юу ч хийхгүй.
  const generatingId = useRef<string | null>(null);
  const status = generation.data?.status;
  const currentId = generation.data?.id ?? null;
  useEffect(() => {
    if (!currentId) return;
    if (isGenerating(status)) {
      if (generatingId.current === currentId) return;
      generatingId.current = currentId;
      invalidateMaterial({ refetch: false });
      return;
    }
    if (generatingId.current !== currentId) return;
    generatingId.current = null;
    invalidateMaterial({ refetch: false });
    void queryClient.invalidateQueries({ queryKey: queryKeys.live.configAll });
  }, [currentId, status, invalidateMaterial, queryClient]);

  const regenerate = useMutation({
    mutationFn: () => requestGeneration(materialId, { kind, topic_id: topicId, regenerate: true }),
    onSuccess: (created) => {
      queryClient.setQueryData(queryKeys.live.generation(created.id), created);
      queryClient.setQueryData(requestKey, created);
    },
    onError: (error) => toast.error(liveErrorMessage(error)),
  });

  return {
    /** Захиалгын алдаа (402 хязгаар, 503 AI унтраалттай гэх мэт). */
    request,
    generation: generation.data ?? request.data ?? null,
    regenerate,
  };
}
