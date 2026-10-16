"use client";

import {
  type ComponentProps,
  createContext,
  useContext,
  useEffect,
  useMemo,
  useRef,
  useState,
} from "react";

/**
 * Видеоны тоглуулалт — бүх хэсэгт нэг:
 * - `auto` — анхдагч: хөдөлгөөн зөвшөөрөгдсөн бол харагдах үед өөрөө тоглоно;
 * - `playing` — хэрэглэгч «Тоглуулах» дарсан (хөдөлгөөн багасгасан ч тоглоно);
 * - `paused` — хэрэглэгч зогсоосон: видео ба давтагдах чимэглэл хоёул зогсоно.
 */
export type LivePlayback = "auto" | "playing" | "paused";

const PlaybackContext = createContext<{
  playback: LivePlayback;
  setPlayback: (next: LivePlayback) => void;
  /** Видео тоглож байгаа (эсвэл тоглох гэж байгаа) эсэх — давтагдах чимэглэл түүнийг дагана. */
  setVideoActive: (active: boolean) => void;
} | null>(null);

export function useLivePlayback() {
  const value = useContext(PlaybackContext);
  if (!value) throw new Error("useLivePlayback нь LiveShowcaseStage дотор л ажиллана");
  return value;
}

/**
 * Нүүрний Live хэсгийн `<section>`. Хэсэг харагдах хэсэгт орж ирмэгц
 * `data-revealed` тавьж орох хөдөлгөөнийг (`globals.css` → `.live-show`) нэг
 * удаа эхлүүлнэ. Дэлгэцээс гарсан эсвэл видео тоглохгүй байгаа (хэрэглэгч
 * зогсоосон, өөрөө тоглож чадаагүй) үед `data-paused` — давтагдах хөдөлгөөн
 * зогсоно (дэлгэцээс гадуур CPU зарцуулахгүй).
 *
 * Агуулга нь сервер дээр бүтнээрээ зурагдана; JS-гүй, хөдөлгөөн багасгасан
 * үед нуугдахгүй (CSS нь `scripting: enabled`, `no-preference` үед л нууна).
 */
export function LiveShowcaseStage({ children, ...props }: ComponentProps<"section">) {
  const ref = useRef<HTMLElement>(null);
  const [revealed, setRevealed] = useState(false);
  const [visible, setVisible] = useState(false);
  const [playback, setPlayback] = useState<LivePlayback>("auto");
  const [videoActive, setVideoActive] = useState(false);

  useEffect(() => {
    const section = ref.current;
    if (!section) return;
    // Дээд тал нь дэлгэцийн доод 20%-иас дээш гармагц орж ирнэ.
    const reveal = new IntersectionObserver(
      (entries) => {
        if (!entries.at(-1)?.isIntersecting) return;
        setRevealed(true);
        reveal.disconnect();
      },
      { rootMargin: "0px 0px -20% 0px" },
    );
    const presence = new IntersectionObserver((entries) => {
      setVisible(entries.at(-1)?.isIntersecting ?? false);
    });
    reveal.observe(section);
    presence.observe(section);
    return () => {
      reveal.disconnect();
      presence.disconnect();
    };
  }, []);

  const context = useMemo(() => ({ playback, setPlayback, setVideoActive }), [playback]);

  return (
    <PlaybackContext value={context}>
      <section
        ref={ref}
        data-revealed={revealed || undefined}
        data-paused={!visible || !videoActive || undefined}
        {...props}
      >
        {children}
      </section>
    </PlaybackContext>
  );
}
