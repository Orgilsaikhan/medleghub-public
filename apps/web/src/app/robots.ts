import type { MetadataRoute } from "next";

import { SITE_URL } from "@/lib/seo";

/**
 * Нийтийн хуудсууд нээлттэй. Нэвтэрсэн хэрэглэгчийн хэсэг, админ, API,
 * хичээл (нэвтрэлт шаарддаг) хаалттай — эдгээр нь `noindex`-тэй ч мөлхөх
 * шаардлагагүй. Нэвтрэх, бүртгүүлэх хуудас нээлттэй: `noindex`-ийг нь харж
 * байж л хайлтаас хасна.
 */
export default function robots(): MetadataRoute.Robots {
  return {
    rules: {
      userAgent: "*",
      allow: "/",
      disallow: [
        "/admin",
        "/api/",
        "/billing/",
        "/community",
        "/dashboard",
        "/learn/",
        "/live",
        "/profile",
        "/settings",
        "/users/",
        "/verify-email",
        "/forgot-password",
      ],
    },
    sitemap: `${SITE_URL}/sitemap.xml`,
  };
}
