/** Админы зарлал (popup). */

import { apiFetch } from "@/lib/api/client";
import type { Announcement, AnnouncementInput, AnnouncementItem } from "@/lib/types/api";

/** Одоо харагдах зарлалууд, шинэ нь эхэнд. Нэвтрээгүй бол зөвхөн «бүгдэд» гэсэн нь. */
export function getCurrentAnnouncements(): Promise<Announcement[]> {
  return apiFetch<Announcement[]>("/announcements/current");
}

/** Админ: бүх зарлал. */
export function listAnnouncements(): Promise<AnnouncementItem[]> {
  return apiFetch<AnnouncementItem[]>("/announcements");
}

export function createAnnouncement(input: AnnouncementInput): Promise<AnnouncementItem> {
  return apiFetch<AnnouncementItem>("/announcements", { method: "POST", json: input });
}

/** Өгсөн талбарыг л өөрчилнө. */
export function updateAnnouncement(
  id: string,
  input: Partial<AnnouncementInput>,
): Promise<AnnouncementItem> {
  return apiFetch<AnnouncementItem>(`/announcements/${encodeURIComponent(id)}`, {
    method: "PATCH",
    json: input,
  });
}

export function deleteAnnouncement(id: string): Promise<void> {
  return apiFetch<void>(`/announcements/${encodeURIComponent(id)}`, { method: "DELETE" });
}
