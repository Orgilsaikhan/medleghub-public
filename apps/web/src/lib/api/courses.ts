import { apiFetch, type RequestOptions } from "@/lib/api/client";
import type { Category, CourseDetail, CourseSummary, Difficulty, Page } from "@/lib/types/api";

export interface CourseListParams {
  q?: string;
  category?: Category;
  difficulty?: Difficulty;
  page?: number;
  page_size?: number;
}

export function listCourses(
  params: CourseListParams = {},
  init?: RequestOptions,
): Promise<Page<CourseSummary>> {
  return apiFetch<Page<CourseSummary>>("/courses", { query: params, ...init });
}

export function getCourse(slug: string, init?: RequestOptions): Promise<CourseDetail> {
  return apiFetch<CourseDetail>(`/courses/${encodeURIComponent(slug)}`, init);
}
