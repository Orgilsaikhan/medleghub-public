"use client";

import dynamic from "next/dynamic";

import { Skeleton } from "@/components/ui/skeleton";

/**
 * Видео тоглуулагчийг зөвхөн шаардлагатай үед татна.
 *
 * Video.js нь томоохон сан — видеогүй хичээл дээр нэг ч байт татагдахгүй.
 * Сервер дээр render хийх шаардлагагүй тул `ssr: false`.
 */
const VideoPlayer = dynamic(() => import("@/components/learn/video-player"), {
  ssr: false,
  loading: () => <Skeleton className="aspect-video w-full rounded-none" />,
});

export function LessonVideo({ src }: { src: string | null }) {
  // Видеогүй хичээлд хоосон дөрвөлжин үлдээхгүй — бичмэл агуулга шууд эхэлнэ.
  if (!src) return null;

  // `key` нь хичээл солигдоход player-ийг цоо шинээр үүсгэнэ.
  return <VideoPlayer key={src} src={src} />;
}
