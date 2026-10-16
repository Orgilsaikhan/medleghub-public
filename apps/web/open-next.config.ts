import { defineCloudflareConfig } from "@opennextjs/cloudflare";
import staticAssetsIncrementalCache from "@opennextjs/cloudflare/overrides/incremental-cache/static-assets-incremental-cache";

/**
 * Cloudflare Workers-ийн тохиргоо.
 *
 * Сайт ISR/`revalidate` ашигладаггүй — хуудас нь build-ийн үед урьдчилан
 * үүсдэг эсвэл хүсэлт бүрт (`cache: "no-store"`) render хийгддэг. Тиймээс
 * кэшийг R2/KV биш Workers Static Assets-аас уншина (нэмэлт үйлчилгээгүй).
 *
 * ЗААВАЛ `enableCacheInterception: false`: Next 16.3-т `prefetchInlining`
 * анхдагчаар асаалттай. Тэр үед OpenNext-ийн interceptor (@opennextjs/aws
 * 4.1.x) `next-router-segment-prefetch: /_tree` хүсэлтэд хуудасны БҮТЭН RSC-г
 * буцаадаг. Хөтөч түүнийг ашиглаж чадахгүй тул prefetch-ээ тасралтгүй
 * давтана: нэг таб ~140 хүсэлт/сек илгээж, 2026-09-28-нд Workers Free-ийн
 * өдрийн 100k хязгаарыг 4 цаг хүрэхгүй хугацаанд дуусгасан.
 */
export default defineCloudflareConfig({
  incrementalCache: staticAssetsIncrementalCache,
  enableCacheInterception: false,
});
