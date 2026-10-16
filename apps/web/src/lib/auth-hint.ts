/**
 * Нэвтрэлтийн "сэжүүр" cookie.
 *
 * JWT нь httpOnly cookie дотор байдаг тул JavaScript түүнийг уншиж чадахгүй.
 * Backend нь түүнтэй зэрэг нууц утга агуулаагүй энгийн `suralts_session=1`
 * cookie тавьдаг. Үүнийг уншсанаар зочин хэрэглэгч тутамд `/auth/me` рүү
 * дэмий хүсэлт илгээхгүй (мөн browser console-д 401 алдаа гарахгүй).
 *
 * Энэ cookie нь эрх олгодоггүй — зөвхөн UI-д зориулсан сануулга. Эрхийг зөвхөн
 * сервер тал httpOnly token-оор шалгана.
 */

export const AUTH_HINT_COOKIE = "suralts_session";

export function hasAuthHint(): boolean {
  if (typeof document === "undefined") return false;
  return document.cookie
    .split(";")
    .some((entry) => entry.trim().startsWith(`${AUTH_HINT_COOKIE}=`));
}

/** Token хүчингүй болсон үед (401) хуучирсан сэжүүрийг цэвэрлэнэ. */
export function clearAuthHint(): void {
  if (typeof document === "undefined") return;
  document.cookie = `${AUTH_HINT_COOKIE}=; Max-Age=0; Path=/; SameSite=Lax`;
}
