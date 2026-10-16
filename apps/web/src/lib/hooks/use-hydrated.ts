"use client";

import { useSyncExternalStore } from "react";

/** Хэзээ ч өөрчлөгдөхгүй store — бид зөвхөн server/client snapshot-ын ялгааг ашиглана. */
const subscribe = () => () => {};
const getClientSnapshot = () => true;
const getServerSnapshot = () => false;

/**
 * Hydration дууссан эсэх.
 *
 * Сервер дээр болон client-ийн ХАМГИЙН АНХНЫ render-т `false` буцаана — ингэснээр
 * хоёр талын HTML яг таарч, hydration зөрчил үүсэхгүй. Дараагийн render-ээс
 * `true` болно. `useEffect` дотор setState дуудахаас илүү найдвартай.
 */
export function useIsHydrated(): boolean {
  return useSyncExternalStore(subscribe, getClientSnapshot, getServerSnapshot);
}
