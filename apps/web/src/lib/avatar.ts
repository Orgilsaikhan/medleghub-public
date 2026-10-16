import { apiBaseUrl } from "@/lib/api/client";
import type { User } from "@/lib/types/api";

/**
 * Профайлын зургийн URL. `?v=` нь зургийн hash — зураг солигдоход URL өөрчлөгдөж,
 * хөтөч хуучныг мөнхөд кэшлэх боломжтой (`GET /users/{id}/avatar`).
 */
export function avatarUrl(user: Pick<User, "id" | "avatar_key">): string | null {
  if (!user.avatar_key) return null;
  return `${apiBaseUrl}/users/${user.id}/avatar?v=${user.avatar_key}`;
}
