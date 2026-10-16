"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useRouter } from "next/navigation";
import { toast } from "sonner";

import { checkCaseAnswer, completeLesson, myCourses } from "@/lib/api/progress";
import { mn } from "@/lib/i18n/mn";
import { queryKeys } from "@/lib/query-keys";
import type { LessonPlayer, MyCourse } from "@/lib/types/api";

export function useMyCourses() {
  return useQuery<MyCourse[]>({
    queryKey: queryKeys.me.courses,
    queryFn: myCourses,
    staleTime: 30_000,
  });
}

/**
 * Хичээлийг дуусгах.
 *
 * Ахицын эцсийн эх сурвалж нь сервер. Гэхдээ хариу ирэхийг хүлээлгүй
 * curriculum дээрх тэмдэглэгээг шууд шинэчилж, хэрэглэгчид хурдан мэдрэгддэг
 * болгоно (optimistic update). Алдаа гарвал өмнөх төлөвт буцаана.
 */
export function useCompleteLesson(courseSlug: string, lessonSlug: string) {
  const queryClient = useQueryClient();
  const router = useRouter();
  const playerKey = queryKeys.lessons.player(courseSlug, lessonSlug);

  return useMutation({
    mutationFn: (lessonId: string) => completeLesson(lessonId),

    onMutate: async (lessonId) => {
      await queryClient.cancelQueries({ queryKey: playerKey });
      const previous = queryClient.getQueryData<LessonPlayer>(playerKey);

      if (previous && !previous.lesson.completed) {
        queryClient.setQueryData<LessonPlayer>(playerKey, markCompleted(previous, lessonId));
      }
      return { previous };
    },

    onError: (_error, _lessonId, context) => {
      if (context?.previous) queryClient.setQueryData(playerKey, context.previous);
    },

    onSuccess: (result) => {
      // Серверийн тооцоолсон ахиц нь эцсийн үнэн.
      queryClient.setQueryData<LessonPlayer>(playerKey, (current) =>
        current ? { ...current, progress: result.course_progress } : current,
      );

      // Шинэ тэмдэг бүрд мэдэгдэл — «Харах» нь профайл руу аваачна.
      for (const badge of result.new_badges ?? []) {
        toast.success(mn.profile.newBadge(badge.name), {
          action: { label: mn.profile.newBadgeAction, onClick: () => router.push("/profile") },
        });
      }
    },

    onSettled: () => {
      // Бусад дэлгэц (dashboard, сургалтын хуудас) шинэ ахицыг тусгана.
      void queryClient.invalidateQueries({ queryKey: queryKeys.me.courses });
      void queryClient.invalidateQueries({ queryKey: queryKeys.me.profile });
      void queryClient.invalidateQueries({ queryKey: queryKeys.courses.detail(courseSlug) });
      void queryClient.invalidateQueries({ queryKey: queryKeys.courses.all });
    },
  });
}

/**
 * Мөрдөгчийн хэргийн хариулт илгээх. Зөв бөгөөд бүртгүүлсэн бол сервер
 * хичээлийг дуусгана — тэр үед `useCompleteLesson`-той ижил кэшийг шинэчилнэ.
 */
export function useCaseAnswer(courseSlug: string, lessonSlug: string) {
  const queryClient = useQueryClient();
  const router = useRouter();
  const playerKey = queryKeys.lessons.player(courseSlug, lessonSlug);

  return useMutation({
    mutationFn: ({ lessonId, answer }: { lessonId: string; answer: string }) =>
      checkCaseAnswer(lessonId, answer),

    onSuccess: (result, { lessonId }) => {
      if (!result.completed) return;
      queryClient.setQueryData<LessonPlayer>(playerKey, (current) => {
        if (!current) return current;
        const updated = current.lesson.completed ? current : markCompleted(current, lessonId);
        return result.course_progress ? { ...updated, progress: result.course_progress } : updated;
      });
      // Солонгон тэмдгийг `CaseAnswerBar` том цонхонд нээнэ.
      for (const badge of result.new_badges.filter((badge) => !badge.prismatic)) {
        toast.success(mn.profile.newBadge(badge.name), {
          action: { label: mn.profile.newBadgeAction, onClick: () => router.push("/profile") },
        });
      }
      void queryClient.invalidateQueries({ queryKey: queryKeys.me.courses });
      void queryClient.invalidateQueries({ queryKey: queryKeys.me.profile });
      void queryClient.invalidateQueries({ queryKey: queryKeys.courses.detail(courseSlug) });
      void queryClient.invalidateQueries({ queryKey: queryKeys.courses.all });
    },
  });
}

function markCompleted(player: LessonPlayer, lessonId: string): LessonPlayer {
  const completed = player.progress.completed_lessons + 1;
  const total = player.progress.total_lessons;

  return {
    ...player,
    lesson: { ...player.lesson, completed: true },
    modules: player.modules.map((section) => ({
      ...section,
      lessons: section.lessons.map((lesson) =>
        lesson.id === lessonId ? { ...lesson, completed: true } : lesson,
      ),
    })),
    progress: {
      completed_lessons: Math.min(completed, total),
      total_lessons: total,
      percent: total ? Math.min(Math.round((completed / total) * 100), 100) : 0,
    },
  };
}
