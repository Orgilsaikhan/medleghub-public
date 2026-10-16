/** Админы CRUD дуудлагууд. Эрхийг backend шалгана — эдгээр нь зөвхөн дамжуулагч. */

import { apiFetch } from "@/lib/api/client";
import type {
  CourseDetail,
  CourseInput,
  CourseSummary,
  FeedbackItem,
  LessonDetail,
  LessonInput,
  MessageResult,
  ModuleInput,
  ModuleWithLessons,
  Page,
  SuspensionItem,
} from "@/lib/types/api";

// --- Courses --------------------------------------------------------------

/** Админ дэлгэцэд нийтлэгдээгүй модул, хичээл ч харагдана. */
export function getAdminCourse(courseId: string): Promise<CourseDetail> {
  return apiFetch<CourseDetail>(`/admin/courses/${courseId}`);
}

export function createCourse(input: CourseInput): Promise<CourseSummary> {
  return apiFetch<CourseSummary>("/courses", { method: "POST", json: input });
}

export function updateCourse(
  courseId: string,
  input: Partial<CourseInput>,
): Promise<CourseSummary> {
  return apiFetch<CourseSummary>(`/courses/${courseId}`, { method: "PATCH", json: input });
}

export function deleteCourse(courseId: string): Promise<MessageResult> {
  return apiFetch<MessageResult>(`/courses/${courseId}`, { method: "DELETE" });
}

// --- Modules --------------------------------------------------------------

export function createModule(courseId: string, input: ModuleInput): Promise<ModuleWithLessons> {
  return apiFetch<ModuleWithLessons>(`/courses/${courseId}/modules`, {
    method: "POST",
    json: input,
  });
}

export function updateModule(
  moduleId: string,
  input: Partial<ModuleInput>,
): Promise<ModuleWithLessons> {
  return apiFetch<ModuleWithLessons>(`/modules/${moduleId}`, { method: "PATCH", json: input });
}

export function deleteModule(moduleId: string): Promise<MessageResult> {
  return apiFetch<MessageResult>(`/modules/${moduleId}`, { method: "DELETE" });
}

// --- Lessons --------------------------------------------------------------

export function getLesson(lessonId: string): Promise<LessonDetail> {
  return apiFetch<LessonDetail>(`/lessons/${lessonId}`);
}

export function createLesson(moduleId: string, input: LessonInput): Promise<LessonDetail> {
  return apiFetch<LessonDetail>(`/modules/${moduleId}/lessons`, { method: "POST", json: input });
}

export function updateLesson(
  lessonId: string,
  input: Partial<LessonInput> & { module_id?: string },
): Promise<LessonDetail> {
  return apiFetch<LessonDetail>(`/lessons/${lessonId}`, { method: "PATCH", json: input });
}

export function deleteLesson(lessonId: string): Promise<MessageResult> {
  return apiFetch<MessageResult>(`/lessons/${lessonId}`, { method: "DELETE" });
}

// --- Санал хүсэлт ------------------------------------------------------------

export interface FeedbackListParams {
  /** `undefined` бол бүгд. */
  resolved?: boolean;
  page?: number;
  page_size?: number;
}

export function listFeedback(params: FeedbackListParams = {}): Promise<Page<FeedbackItem>> {
  return apiFetch<Page<FeedbackItem>>("/admin/feedback", { query: params });
}

export function setFeedbackResolved(feedbackId: string, resolved: boolean): Promise<FeedbackItem> {
  return apiFetch<FeedbackItem>(`/admin/feedback/${feedbackId}`, {
    method: "PATCH",
    json: { resolved },
  });
}

// --- Community-ийн түдгэлзүүлэлт -------------------------------------------------

export interface SuspensionListParams {
  /** `undefined` бол бүгд. */
  active?: boolean;
  page?: number;
  page_size?: number;
}

export function listSuspensions(params: SuspensionListParams = {}): Promise<Page<SuspensionItem>> {
  return apiFetch<Page<SuspensionItem>>("/admin/community/suspensions", { query: params });
}

/** Дараагийн шатны хугацаагаар (сервер тооцно). */
export function suspendUser(userId: string, reason: string): Promise<SuspensionItem> {
  return apiFetch<SuspensionItem>("/admin/community/suspensions", {
    method: "POST",
    json: { user_id: userId, reason },
  });
}

export function liftSuspension(suspensionId: string): Promise<SuspensionItem> {
  return apiFetch<SuspensionItem>(`/admin/community/suspensions/${suspensionId}/lift`, {
    method: "POST",
  });
}
