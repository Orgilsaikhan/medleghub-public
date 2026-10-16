"use client";

import { useSyncExternalStore } from "react";

/**
 * CSS media query-г React state болгож дагана.
 *
 * Сервер дээр `window` байхгүй тул анхны snapshot нь `false` — desktop-ийн
 * зурагт хэсэг рүү буруу орохоос сэргийлж, дуудагч тал хамгийн нарийн
 * (mobile-first) байдлыг серверийн үед үзнэ. `LessonView` шиг зөвхөн
 * өгөгдөл ирсний дараа render хийдэг хэсэгт hydration зөрчил үүсэхгүй.
 */
export function useMediaQuery(query: string): boolean {
  return useSyncExternalStore(
    (onChange) => {
      const mql = window.matchMedia(query);
      mql.addEventListener("change", onChange);
      return () => mql.removeEventListener("change", onChange);
    },
    () => window.matchMedia(query).matches,
    () => false,
  );
}
