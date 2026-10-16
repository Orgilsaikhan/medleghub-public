"use client";

import { useEffect, useRef } from "react";
import type Player from "video.js/dist/types/player";

import { mn } from "@/lib/i18n/mn";

interface VideoPlayerProps {
  src: string;
  /** Хичээл солигдоход player-ийг дахин үүсгэхэд ашиглагдана. */
  poster?: string | null;
}

/** Өргөтгөлөөс видеоны төрлийг таана. `.m3u8` бол HLS. */
function guessType(src: string): string {
  const path = src.split("?")[0].toLowerCase();
  if (path.endsWith(".m3u8")) return "application/x-mpegURL";
  if (path.endsWith(".mpd")) return "application/dash+xml";
  if (path.endsWith(".webm")) return "video/webm";
  return "video/mp4";
}

/**
 * Video.js тоглуулагч.
 *
 * `next/dynamic`-аар lazy ачаалагдана (`lesson-video.tsx`), тиймээс видеогүй
 * хичээл дээр энэ сангийн bundle огт татагдахгүй. HLS дэмжлэг нь video.js-д
 * шууд орсон (`@videojs/http-streaming`).
 */
export default function VideoPlayer({ src, poster }: VideoPlayerProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const playerRef = useRef<Player | null>(null);

  useEffect(() => {
    let disposed = false;
    const container = containerRef.current;
    if (!container) return;

    // Video.js нь DOM элементийг өөрчилдөг тул React-ийн удирддаг элемент рүү
    // биш, өөрийн үүсгэсэн элемент рүү холбоно.
    const element = document.createElement("video-js");
    element.classList.add("vjs-big-play-centered", "h-full", "w-full");
    container.appendChild(element);

    void (async () => {
      const videojs = (await import("video.js")).default;
      await import("video.js/dist/video-js.css");
      if (disposed) return;

      playerRef.current = videojs(element, {
        controls: true,
        preload: "metadata",
        fluid: false,
        responsive: true,
        playbackRates: [0.75, 1, 1.25, 1.5, 1.75, 2],
        poster: poster ?? undefined,
        sources: [{ src, type: guessType(src) }],
        language: "mn",
      });
    })();

    return () => {
      disposed = true;
      const player = playerRef.current;
      playerRef.current = null;
      if (player && !player.isDisposed()) player.dispose();
      container.replaceChildren();
    };
  }, [src, poster]);

  return (
    <div
      ref={containerRef}
      aria-label={mn.learn.lessonContent}
      className="aspect-video w-full overflow-hidden bg-black"
    />
  );
}
