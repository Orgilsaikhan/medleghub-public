/**
 * TanStack Query-ийн бүх key нэг газар.
 *
 * Ингэснээр invalidate хийхдээ буруу key бичих эрсдэл багасна.
 */

import type { FeedbackListParams, SuspensionListParams } from "@/lib/api/admin";
import type { PostListParams } from "@/lib/api/community";
import type { CourseListParams } from "@/lib/api/courses";
import type { LiveGenerationKind } from "@/lib/types/live";

export const queryKeys = {
  currentUser: ["auth", "me"] as const,

  courses: {
    all: ["courses"] as const,
    list: (params: CourseListParams) => ["courses", "list", params] as const,
    detail: (slug: string) => ["courses", "detail", slug] as const,
    progress: (courseId: string) => ["courses", "progress", courseId] as const,
    students: (slug: string) => ["courses", "students", slug] as const,
  },

  lessons: {
    all: ["lessons"] as const,
    player: (courseSlug: string, lessonSlug: string) =>
      ["lessons", "player", courseSlug, lessonSlug] as const,
    detail: (lessonId: string) => ["lessons", "detail", lessonId] as const,
    help: (lessonId: string) => ["lessons", "help", lessonId] as const,
  },

  me: {
    courses: ["me", "courses"] as const,
    profile: ["me", "profile"] as const,
    referral: ["me", "referral"] as const,
  },

  users: {
    profile: (userId: string) => ["users", "profile", userId] as const,
  },

  community: {
    all: ["community"] as const,
    me: ["community", "me"] as const,
    /** Бүх жагсаалт — лайк, сэтгэгдлийн тоо өөрчлөгдөхөд invalidate хийнэ. */
    lists: ["community", "posts"] as const,
    posts: (params: PostListParams) => ["community", "posts", params] as const,
    post: (postId: string) => ["community", "post", postId] as const,
  },

  announcements: {
    /** Нэвтэрсэн эсэхээс хамаарч хариу өөр. */
    current: (userId: string) => ["announcements", "current", userId] as const,
  },

  live: {
    all: ["live"] as const,
    /** Хэрэглээ, эрх хэрэглэгч бүрт өөр. */
    config: (userId: string) => ["live", "config", userId] as const,
    configAll: ["live", "config"] as const,
    materials: ["live", "materials"] as const,
    material: (materialId: string) => ["live", "material", materialId] as const,
    /** `requestGeneration` — idempotent POST тул query болгосон (`use-live.ts`). */
    generationRequest: (materialId: string, kind: LiveGenerationKind, topicId: string | null) =>
      ["live", "generation-request", materialId, kind, topicId ?? "all"] as const,
    generation: (generationId: string) => ["live", "generation", generationId] as const,
    /** `round` — «Дахин давтах» бүрд шинэ жагсаалт. */
    cards: (materialId: string, topicId: string | null, mode: "due" | "all", round: number) =>
      ["live", "cards", materialId, topicId ?? "all", mode, round] as const,
  },

  billing: {
    plan: ["billing", "plan"] as const,
    payment: (paymentId: string) => ["billing", "payment", paymentId] as const,
    redemption: (redemptionId: string) => ["billing", "redemption", redemptionId] as const,
  },

  admin: {
    course: (courseId: string) => ["admin", "course", courseId] as const,
    feedbackAll: ["admin", "feedback"] as const,
    feedback: (params: FeedbackListParams) => ["admin", "feedback", params] as const,
    planPrice: ["admin", "plan-price"] as const,
    promoCodes: ["admin", "promo-codes"] as const,
    announcements: ["admin", "announcements"] as const,
    liveOverview: ["admin", "live-overview"] as const,
    liveModels: ["admin", "live-models"] as const,
    suspensionsAll: ["admin", "suspensions"] as const,
    suspensions: (params: SuspensionListParams) => ["admin", "suspensions", params] as const,
  },
} as const;
