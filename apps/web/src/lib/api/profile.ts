import { apiFetch } from "@/lib/api/client";
import type { BadgeClaimResult, Profile, User } from "@/lib/types/api";

/** Профайлын хуудсанд хэрэгтэй бүгд — хэрэглэгч, статистик, тэмдгүүд. */
export function getProfile(): Promise<Profile> {
  return apiFetch<Profile>("/me/profile");
}

/** Үйлдлээр олгогдох тэмдэг (жишээ нь нууц `/footprints` хуудас). */
export function claimBadge(key: string): Promise<BadgeClaimResult> {
  return apiFetch<BadgeClaimResult>(`/me/badges/${encodeURIComponent(key)}`, { method: "POST" });
}

/**
 * Нэрийн хажууд харуулах онцлох амжилтууд — харагдах дарааллаар, хамгийн
 * ихдээ 5. Хоосон жагсаалт нь бүгдийг арилгана.
 */
export function updateShowcase(badgeKeys: string[]): Promise<{ badge_keys: string[] }> {
  return apiFetch<{ badge_keys: string[] }>("/me/showcase", {
    method: "PUT",
    json: { badge_keys: badgeKeys },
  });
}

/** Сервер зургийг 256×256 WebP болгон дахин кодлоно. */
export function uploadAvatar(file: File): Promise<User> {
  const form = new FormData();
  form.append("file", file);
  return apiFetch<User>("/me/avatar", { method: "PUT", form });
}

export function deleteAvatar(): Promise<User> {
  return apiFetch<User>("/me/avatar", { method: "DELETE" });
}
