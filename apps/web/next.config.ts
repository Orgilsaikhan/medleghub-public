import type { NextConfig } from "next";

/** Next-ийн анхдагч `htmlLimitedBots` (next/dist/shared/lib/router/utils/html-bots.js). */
const HTML_LIMITED_BOTS =
  "[\\w-]+-Google|Google-[\\w-]+|Chrome-Lighthouse|Slurp|DuckDuckBot|baiduspider|yandex|sogou|bitlybot|tumblr|vkShare|quora link preview|redditbot|ia_archiver|Bingbot|BingPreview|applebot|facebookexternalhit|facebookcatalog|Twitterbot|LinkedInBot|Slackbot|Discordbot|WhatsApp|SkypeUriPreview|Yeti|googleweblight";

/**
 * Content Security Policy.
 *
 * `connect-src` нь backend-ийн origin-ыг env-ээс авна — хөгжүүлэлт болон
 * production дээр өөр байна.
 *
 * `'unsafe-eval'` нь Monaco засварлагч болон sandbox worker хоёулаа
 * `new Function` ашигладаг тул шаардлагатай. Мөн Pyodide-ийн WebAssembly-г
 * хөрвүүлэхэд ч энэ зөвшөөрөл хэрэгтэй. Хэрэглэгчийн код нь тусдаа Worker
 * дотор ажилладаг тул энэ нь үндсэн хуудсанд нэмэлт эрсдэл үүсгэхгүй
 * (`docs/ARCHITECTURE.md` §8).
 *
 * Pyodide-д нэмэлт CSP дүрэм ШААРДЛАГАГҮЙ: файлууд нь `/pyodide/` дор
 * өөрсдийн origin дээр байрлах тул `script-src 'self'` болон
 * `connect-src 'self'` хангалттай. Гадаад CDN ашиглавал энэ нь өөрчлөгдөнө.
 */
function apiOrigin(): string {
  const raw = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1";
  // Харьцангуй зам (`/api/v1`) — хүсэлт нь Vercel-ийн rewrite-аар дамжиж,
  // хөтчийн хувьд ижил origin. `connect-src 'self'` хангалттай.
  if (raw.startsWith("/")) return "";
  try {
    return new URL(raw).origin;
  } catch {
    return "http://localhost:8000";
  }
}

/**
 * Видео хостлох домэйнүүд.
 *
 * HLS тоглуулагч нь сегмент бүрийг `fetch`-ээр татдаг тул домэйн нь
 * `media-src`-ээс гадна `connect-src`-д БАС байх ёстой. Зөвхөн `media-src`
 * зөвшөөрвөл `.m3u8` ачаалагдахгүй.
 *
 * Жишээ: NEXT_PUBLIC_MEDIA_ORIGINS=https://media.medleghub.mn,https://cdn.medleghub.mn
 */
function mediaOrigins(): string[] {
  return (process.env.NEXT_PUBLIC_MEDIA_ORIGINS ?? "")
    .split(",")
    .map((origin) => origin.trim())
    .filter(Boolean);
}

/**
 * Хөгжүүлэлтийн серверийг дотоод сүлжээнээс (хамт ажиллагсдын компьютер,
 * утаснаас) нээх хаягууд. Next.js нь `localhost`-оос бусад origin-ы
 * `/_next/*` хүсэлтийг анхдагчаар 403-аар хаадаг.
 *
 * Жишээ: ALLOWED_DEV_ORIGINS=192.168.1.14
 */
function allowedDevOrigins(): string[] {
  return (process.env.ALLOWED_DEV_ORIGINS ?? "")
    .split(",")
    .map((origin) => origin.trim())
    .filter(Boolean);
}

/**
 * Flux-Core чатботын widget (`src/components/layout/chat-widget.tsx`): скрипт
 * нь `flux-core.com`-оос, яриа нь `api.flux-core.com` руу `fetch`-ээр явна.
 * Shadow DOM дотор inline `<style>` ашигладаг — `'unsafe-inline'` хангалттай.
 */
const CHAT_WIDGET_SCRIPT = "https://flux-core.com/widget.js";
const CHAT_WIDGET_API = "https://api.flux-core.com";

const isDev = process.env.NODE_ENV === "development";

function contentSecurityPolicy(): string {
  const api = apiOrigin();
  const media = mediaOrigins();
  const mediaList = media.length > 0 ? ` ${media.join(" ")}` : "";
  return [
    "default-src 'self'",
    "base-uri 'self'",
    "form-action 'self'",
    "frame-ancestors 'none'",
    "object-src 'none'",
    // Next.js-ийн hydration script болон Monaco-ийн `new Function`.
    `script-src 'self' 'unsafe-inline' 'unsafe-eval' blob: ${CHAT_WIDGET_SCRIPT}`,
    "style-src 'self' 'unsafe-inline'",
    // Профайлын зураг API-аас ирнэ — API тусдаа origin бол (CI) түүнийг зөвшөөрнө.
    ["img-src 'self' data: blob: https:", api].filter(Boolean).join(" "),
    "font-src 'self' data:",
    // Видео нь тохируулсан CDN-ээс, blob: нь HLS сегментүүдэд.
    `media-src 'self' blob:${mediaList}`,
    // Sandbox болон Monaco-ийн worker-ууд.
    "worker-src 'self' blob:",
    ["connect-src 'self' blob:", api, ...media, CHAT_WIDGET_API].filter(Boolean).join(" "),
    "manifest-src 'self'",
    // Хөгжүүлэлтэд ҮГҮЙ: `http://192.168.x.x:3000` гэх мэт HTTPS-гүй хаягаар
    // нээхэд хөтөч CSS, JS-ийг https рүү сольж, хуудас загваргүй харагдана.
    // (`localhost` нь үл хамаарна — тиймээс зөвхөн сүлжээгээр нээхэд илэрдэг.)
    ...(isDev ? [] : ["upgrade-insecure-requests"]),
  ].join("; ");
}

const SECURITY_HEADERS = [
  { key: "Content-Security-Policy", value: contentSecurityPolicy() },
  { key: "X-Content-Type-Options", value: "nosniff" },
  { key: "X-Frame-Options", value: "DENY" },
  { key: "Referrer-Policy", value: "strict-origin-when-cross-origin" },
  {
    key: "Permissions-Policy",
    value: "camera=(), microphone=(), geolocation=(), interest-cohort=()",
  },
  { key: "Cross-Origin-Opener-Policy", value: "same-origin" },
];

/**
 * Backend руу proxy.
 *
 * `API_PROXY_TARGET` тохируулагдсан үед хөтчийн бүх API хүсэлт нь энэ сайтын
 * өөрийн origin руу (`/api/v1/...`) явж, Vercel нь backend руу дамжуулна.
 * Ингэснээр httpOnly нэвтрэлтийн cookie нь first-party болно — тусдаа
 * домэйн шаардлагагүй, `SameSite=None` шаардлагагүй, Safari-д ч ажиллана.
 *
 * Энэ нь build-ийн үед уншигдана: Vercel дээр орчны хувьсагчийг өөрчлөсний
 * дараа ЗААВАЛ дахин deploy хийнэ.
 */
function apiProxyTarget(): string | null {
  const raw = process.env.API_PROXY_TARGET?.trim();
  if (!raw) return null;
  return raw.replace(/\/+$/, "");
}

const nextConfig: NextConfig = {
  allowedDevOrigins: allowedDevOrigins(),

  // Мөлхөгч, link preview-д metadata (title, canonical, Open Graph) <head>-д
  // шууд ирнэ — streaming-гүй. Next-ийн анхдагч жагсаалтад (Facebook/Messenger,
  // X, LinkedIn, Discord, WhatsApp, Bing, Yandex…) Googlebot байхгүй: түүнд
  // динамик хуудасны metadata <body>-д хожим ирдэг бөгөөд Google <head>-ээс
  // гадуурх canonical-ыг үл тоодог. Telegram-ыг мөн нэмэв.
  // `/.*/` (бүх хүсэлт) БҮҮ тавь: статик хуудсыг хүсэлт бүрт дахин render
  // хийлгэж, Workers дээр файл уншдаг `/privacy`, `/terms` 500 болгодог.
  htmlLimitedBots: new RegExp(`${HTML_LIMITED_BOTS}|Googlebot|TelegramBot`, "i"),

  async rewrites() {
    const target = apiProxyTarget();
    if (!target) return [];
    return [{ source: "/api/v1/:path*", destination: `${target}/api/v1/:path*` }];
  },

  async headers() {
    return [
      { source: "/:path*", headers: SECURITY_HEADERS },
      {
        // ЗААВАЛ: Vercel нь гадаад rewrite-ийн хариуг edge дээр cache хийж
        // чадна. API нь хэрэглэгч тус бүрийн хариу буцаадаг тул үүнийг
        // хаахгүй бол нэг хэрэглэгчийн өгөгдөл нөгөөд харагдаж болзошгүй.
        source: "/api/v1/:path*",
        headers: [{ key: "x-vercel-enable-rewrite-caching", value: "0" }],
      },
      {
        // Monaco-ийн файлууд нэрэндээ агуулгын hash-тай тул мөнхөд cache
        // хийж болно. Үгүй бол хичээл бүр дээр 20+ нөхцөлт хүсэлт явна.
        source: "/monaco/:path*",
        headers: [{ key: "Cache-Control", value: "public, max-age=31536000, immutable" }],
      },
      {
        // Pyodide нь 13 MB орчим. Хувилбар нь package-lock-оор тогтсон бөгөөд
        // файлын агуулга өөрчлөгддөггүй тул мөнхөд cache хийнэ. Үгүй бол
        // хичээл бүр дээр дахин татаж, Python эхлүүлэх нь тэвчишгүй удаан
        // болно.
        source: "/pyodide/:path*",
        headers: [{ key: "Cache-Control", value: "public, max-age=31536000, immutable" }],
      },
    ];
  },

  images: {
    // Зургийг байгаа хэвээр нь үйлчилнэ. Cloudflare дээр Next-ийн зураг
    // оновчлол нь Cloudflare Images-ээр хувиргалт бүрт төлбөртэй бөгөөд
    // `hostname: "**"`-тэй бол дурын гадаад зургийг манай данснаас хувиргах
    // боломж нээнэ. Тэмдэг, лого нь аль хэдийн жижиг (256px WebP) — зургийг
    // R2-т хадгалахдаа ч хэмжээг нь урьдчилан багасгана.
    unoptimized: true,
  },

  // Алдааны мөрөнд серверийн хувилбар мэдээлэхгүй.
  poweredByHeader: false,
};

export default nextConfig;
