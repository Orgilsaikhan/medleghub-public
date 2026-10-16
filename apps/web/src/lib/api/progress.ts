import { apiFetch } from "@/lib/api/client";
import type {
  CaseAnswerResult,
  CourseProgress,
  EnrollmentResult,
  LessonCompleteResult,
  MyCourse,
} from "@/lib/types/api";

export function enroll(courseId: string): Promise<EnrollmentResult> {
  return apiFetch<EnrollmentResult>(`/courses/${courseId}/enroll`, { method: "POST" });
}

export function myCourses(): Promise<MyCourse[]> {
  return apiFetch<MyCourse[]>("/me/courses");
}

export function completeLesson(lessonId: string): Promise<LessonCompleteResult> {
  return apiFetch<LessonCompleteResult>(`/lessons/${lessonId}/complete`, { method: "POST" });
}

/** Мөрдөгчийн хэргийн хариулт — зөв эсэхийг зөвхөн сервер мэднэ. */
export function checkCaseAnswer(lessonId: string, answer: string): Promise<CaseAnswerResult> {
  return apiFetch<CaseAnswerResult>(`/lessons/${lessonId}/answer`, {
    method: "POST",
    json: { answer },
  });
}

export function courseProgress(courseId: string): Promise<CourseProgress> {
  return apiFetch<CourseProgress>(`/courses/${courseId}/progress`);
}
