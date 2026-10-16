"use client";

import { useEffect } from "react";

import { SITE_URL } from "@/lib/seo";

/** Flux-Core-ийн самбарын «Сувгууд → Вэбсайт» хэсгийн tag. Түлхүүр нь нийтийн. */
const WIDGET_SRC = "https://flux-core.com/widget.js";
const WIDGET_KEY = "wk_KvP-neC3XuGXmmReX6RFAjpL";
const WIDGET_API = "https://api.flux-core.com";

/**
 * Flux-Core чатбот — бүх хуудасны баруун доод буланд товч.
 *
 * Скриптийг `</body>`-ийн өмнө нэмнэ (Flux-Core-ийн заавар). Зөвхөн production
 * домэйн дээр ачаална: Flux-Core бусад сайтад (localhost, CI) 403 өгдөг бөгөөд
 * хөтөч үүнийг console-д алдаа гэж бичиж e2e-г унагана.
 *
 * Хичээлийн хуудсанд товч нуугдана (`globals.css`, `data-hide-chat-widget`).
 * CSP-ийн зөвшөөрөл: `next.config.ts`.
 */
export function ChatWidget() {
  useEffect(() => {
    if (window.location.hostname !== new URL(SITE_URL).hostname) return;
    if (document.querySelector(`script[src="${WIDGET_SRC}"]`)) return;
    const script = document.createElement("script");
    script.src = WIDGET_SRC;
    script.async = true;
    script.dataset.widget = WIDGET_KEY;
    script.dataset.api = WIDGET_API;
    document.body.appendChild(script);
  }, []);

  return null;
}
