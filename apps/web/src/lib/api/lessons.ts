import { apiFetch } from "@/lib/api/client";
import type { LessonDetail, LessonHelp, LessonPlayer } from "@/lib/types/api";

/** Lesson хуудсанд хэрэгтэй бүх өгөгдлийг нэг дуудлагаар авна. */
export function getLessonPlayer(courseSlug: string, lessonSlug: string): Promise<LessonPlayer> {
  return apiFetch<LessonPlayer>(
    `/courses/${encodeURIComponent(courseSlug)}/lessons/${encodeURIComponent(lessonSlug)}`,
  );
}

export function getLesson(lessonId: string): Promise<LessonDetail> {
  return apiFetch<LessonDetail>(`/lessons/${lessonId}`);
}

/** Дасгалын зөвлөгөө ба жишиг шийдэл. */
export function getLessonHelp(lessonId: string): Promise<LessonHelp> {
  return apiFetch<LessonHelp>(`/lessons/${lessonId}/help`);
}
