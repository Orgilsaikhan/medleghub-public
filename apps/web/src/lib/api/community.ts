import { apiFetch } from "@/lib/api/client";
import type {
  CommentItem,
  CourseStudents,
  LikeResult,
  MessageResult,
  Page,
  PostDetail,
  PostInput,
  PostLanguage,
  PostSummary,
  PostType,
  CommunityStatus,
  PublicProfile,
  ReportInput,
} from "@/lib/types/api";

/** Сургалтын суралцагчид, ахиц ихээс нь. Нэвтэрсэн хэрэглэгчид л. */
export function getCourseStudents(slug: string): Promise<CourseStudents> {
  return apiFetch<CourseStudents>(`/courses/${encodeURIComponent(slug)}/students`);
}

/** Өөр хэрэглэгчийн профайл — имэйлгүй, зөвхөн нэр, статистик, тэмдэг, ахиц. */
export function getPublicProfile(userId: string): Promise<PublicProfile> {
  return apiFetch<PublicProfile>(`/users/${encodeURIComponent(userId)}/profile`);
}

// --- Community нийтлэл ---------------------------------------------------------

/** Дүрэм зөвшөөрсөн эсэх, идэвхтэй түдгэлзүүлэлт. */
export function getCommunityStatus(): Promise<CommunityStatus> {
  return apiFetch<CommunityStatus>("/community/me");
}

/** Эхний удаа ороход харуулсан дүрмийг зөвшөөрнө. */
export function acceptGuidelines(): Promise<CommunityStatus> {
  return apiFetch<CommunityStatus>("/community/guidelines", { method: "POST" });
}

export interface PostListParams {
  language?: PostLanguage;
  type?: PostType;
  page?: number;
  page_size?: number;
}

/** Онцолсон нь эхэндээ, дараа нь шинэ нь. */
export function listPosts(params: PostListParams = {}): Promise<Page<PostSummary>> {
  return apiFetch<Page<PostSummary>>("/community/posts", { query: params });
}

export function getPost(postId: string): Promise<PostDetail> {
  return apiFetch<PostDetail>(`/community/posts/${encodeURIComponent(postId)}`);
}

export function createPost(input: PostInput): Promise<PostDetail> {
  return apiFetch<PostDetail>("/community/posts", { method: "POST", json: input });
}

/** Зохиогч эсвэл админ. */
export function deletePost(postId: string): Promise<MessageResult> {
  return apiFetch<MessageResult>(`/community/posts/${encodeURIComponent(postId)}`, {
    method: "DELETE",
  });
}

/** Давтан дарсан ч аюулгүй — сервер нэг л удаа тоолно. */
export function setPostLike(postId: string, liked: boolean): Promise<LikeResult> {
  return apiFetch<LikeResult>(`/community/posts/${encodeURIComponent(postId)}/like`, {
    method: liked ? "PUT" : "DELETE",
  });
}

export function addComment(postId: string, body: string): Promise<CommentItem> {
  return apiFetch<CommentItem>(`/community/posts/${encodeURIComponent(postId)}/comments`, {
    method: "POST",
    json: { body },
  });
}

/** Зохиогч эсвэл админ. */
export function deleteComment(commentId: string): Promise<MessageResult> {
  return apiFetch<MessageResult>(`/community/comments/${encodeURIComponent(commentId)}`, {
    method: "DELETE",
  });
}

/** Гомдол админы «Санал хүсэлт» хуудсанд очно. */
export function reportPost(postId: string, input: ReportInput): Promise<MessageResult> {
  return apiFetch<MessageResult>(`/community/posts/${encodeURIComponent(postId)}/report`, {
    method: "POST",
    json: input,
  });
}

export function reportComment(commentId: string, input: ReportInput): Promise<MessageResult> {
  return apiFetch<MessageResult>(`/community/comments/${encodeURIComponent(commentId)}/report`, {
    method: "POST",
    json: input,
  });
}
