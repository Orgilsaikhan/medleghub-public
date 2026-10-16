"use client";

import { PauseIcon, PlayIcon } from "lucide-react";
import { useEffect, useId, useRef, useState } from "react";

import { LiveMark } from "@/components/live/live-mark";
import { EYEBROW, LiveTile, TOOL_ICONS } from "@/components/live/live-ui";
import { useMediaQuery } from "@/lib/hooks/use-media-query";
import { mn } from "@/lib/i18n/mn";

const t = mn.live;

/** Толгойд AI юу бэлтгэдгийг харуулах шошгууд. */
const FEATURES = [
  { key: "guide", label: t.tools.guide },
  { key: "cards", label: t.tools.cards },
  { key: "quiz", label: t.tools.quiz },
  { key: "exam", label: t.examCard },
] as const;

/** «MedlegHub Live» → ["MedlegHub", "Live"] — бүтээгдэхүүний нэр өөр өнгөтэй. */
function splitTitle(title: string): [string, string] {
  const space = title.lastIndexOf(" ");
  return space > 0 ? [title.slice(0, space), title.slice(space + 1)] : [title, ""];
}

/**
 * `/live`-ийн толгой: Live-ийн тэмдэг гүнтэй шар хавтан дотор, түүнийг тойрсон
 * тойрог замууд (`HeroOrbits`), гарчиг, AI бэлтгэх зүйлсийн шошго. Дэвсгэр нь
 * хуудасны бүтэн өргөнөөр (`LiveBackdrop`).
 */
export function LiveHero() {
  const [brand, product] = splitTitle(t.title);
  const featuresId = useId();
  const [paused, setPaused] = useAmbientPause();
  return (
    <header className="relative">
      <div className="flex items-center gap-4 sm:gap-5">
        <HeroMark paused={paused} />
        <h1 className="text-3xl leading-tight font-bold tracking-tight sm:text-4xl lg:text-5xl">
          {brand}
          {product && (
            <>
              {" "}
              <span className="text-brand-link">{product}</span>
            </>
          )}
        </h1>
      </div>
      <p className="text-muted-foreground mt-4 max-w-2xl text-base text-pretty sm:text-lg">
        {t.subtitle}
      </p>
      <div className="mt-6 flex items-end justify-between gap-4">
        <div className="min-w-0">
          {/* Товч биш, жагсаалт — хүрээгүй тул дарагдах мэт харагдахгүй. */}
          <p id={featuresId} className={EYEBROW}>
            {t.heroFeaturesLabel}
          </p>
          <ul aria-labelledby={featuresId} className="mt-3 flex flex-wrap gap-x-5 gap-y-2.5">
            {FEATURES.map(({ key, label }) => {
              const Icon = TOOL_ICONS[key];
              return (
                <li key={key} className="inline-flex items-center gap-2 text-sm font-medium">
                  <span
                    aria-hidden
                    className="bg-accent text-accent-foreground grid size-7 place-items-center rounded-full"
                  >
                    <Icon className="size-3.5" />
                  </span>
                  {label}
                </li>
              );
            })}
          </ul>
        </div>
        {/* Чимэглэлийн тасралтгүй хөдөлгөөнийг зогсоох (WCAG 2.2.2). Хөдөлгөөн
            багасгасан бол юу ч хөдлөхгүй тул товч хэрэггүй. */}
        <button
          type="button"
          onClick={() => setPaused((value) => !value)}
          aria-label={paused ? t.motionPlay : t.motionPause}
          title={paused ? t.motionPlay : t.motionPause}
          className="bg-card/70 text-muted-foreground hover:text-foreground hover:bg-accent focus-visible:ring-ring/50 grid size-9 shrink-0 place-items-center rounded-full border backdrop-blur-sm transition-colors outline-none focus-visible:ring-3 motion-reduce:hidden"
        >
          {paused ? (
            <PlayIcon aria-hidden className="size-4" />
          ) : (
            <PauseIcon aria-hidden className="size-4" />
          )}
        </button>
      </div>
    </header>
  );
}

/**
 * Толгойн чимэглэлийн хөдөлгөөнийг зогсоох төлөв. Хуудасны бүтэн өргөний
 * дэвсгэр (`LiveBackdrop`) энэ компонентын гадна байдаг тул `<html>`-д
 * шинж тавьж, CSS (`.live-ambient`) бүгдийг нь зогсооно. Хадгалахгүй —
 * хуудсыг дахин нээхэд хөдөлгөөн эхэлнэ.
 */
function useAmbientPause() {
  const [paused, setPaused] = useState(false);
  useEffect(() => {
    const root = document.documentElement;
    root.toggleAttribute("data-live-motion-paused", paused);
    return () => root.removeAttribute("data-live-motion-paused");
  }, [paused]);
  return [paused, setPaused] as const;
}

/**
 * Толгойн ард бүтэн өргөнөөр: зөөлөн шар туяа, бүдэг тор, аажуухан хөвөх
 * гэрэл. Эцэг нь `relative isolate overflow-clip`.
 */
export function LiveBackdrop() {
  return (
    <div
      aria-hidden
      className="live-ambient pointer-events-none absolute inset-x-0 top-0 -z-10 h-[36rem] overflow-hidden"
    >
      <div className="from-primary/10 via-primary/[0.03] absolute inset-0 bg-gradient-to-b to-transparent" />
      <div className="live-grid absolute inset-0 [--live-grid-at:20%_0%]" />
      <div className="bg-primary/20 motion-safe:animate-glow-drift absolute -top-64 -left-48 size-[36rem] rounded-full blur-3xl" />
      <div className="bg-primary/10 motion-safe:animate-glow-drift absolute -top-32 -right-48 size-[30rem] rounded-full blur-3xl [animation-direction:alternate-reverse]" />
    </div>
  );
}

/** Гарчгийн хажуугийн тэмдэг — ард нь «амьсгалах» гэрэл ба тойрог замууд. */
function HeroMark({ paused }: { paused: boolean }) {
  return (
    <span
      aria-hidden
      className="live-ambient relative grid size-14 shrink-0 place-items-center sm:size-16"
    >
      <HeroOrbits paused={paused} />
      <span className="bg-primary/45 motion-safe:animate-live-breathe absolute -inset-3 -z-10 rounded-[1.75rem] blur-2xl" />
      <LiveTile className="size-full rounded-[1.1rem] sm:rounded-[1.3rem]">
        <LiveMark animated={!paused} className="size-8 sm:size-9" />
      </LiveTile>
    </span>
  );
}

/** Тогтмол «санамсаргүй» тоо — сервер, хөтөч хоёрт ижил (hydration зөрөхгүй). */
function seeded(seed: number) {
  let value = seed;
  return () => {
    value = (value * 16807) % 2147483647;
    return (value - 1) / 2147483646;
  };
}

const random = seeded(11);
const round = (value: number) => Math.round(value * 100) / 100;

/** Бүдэг одод — тэмдгээс баруун тийш, гарчгийн ард. */
const STARS = Array.from({ length: 36 }, () => ({
  x: Math.round(-240 + random() * 1480),
  y: Math.round(-270 + random() * 540),
  r: round(0.7 + random() * 1.1),
  opacity: round(0.15 + random() * 0.35),
}));

/** Анивчих шар одод: [x, y, хэмжээ, саатал (с)]. */
const SPARKS: [number, number, number, number][] = [
  [205, -96, 7, 0],
  [560, 34, 5, 1.3],
  [800, -150, 6.5, 2.2],
  [372, 168, 4.5, 0.7],
  [1010, 70, 5.5, 1.8],
  [-170, -130, 5, 2.8],
];

function sparkPath(size: number): string {
  const waist = size * 0.18;
  return `M0 ${-size}Q${waist} ${-waist} ${size} 0Q${waist} ${waist} 0 ${size}Q${-waist} ${waist} ${-size} 0Q${-waist} ${-waist} 0 ${-size}Z`;
}

/** Тойрог зам: хагас тэнхлэгүүд (px), нэг эргэх хугацаа (с), сарны радиус, эхлэх байрлал (0–1). */
const RINGS = [
  { rx: 118, ry: 40, seconds: 14, moon: 3.5, phase: 0.2, dotted: false },
  { rx: 262, ry: 80, seconds: 28, moon: 2.6, phase: 0.62, dotted: true },
  { rx: 452, ry: 128, seconds: 46, moon: 4, phase: 0.36, dotted: false },
  { rx: 690, ry: 186, seconds: 72, moon: 2.4, phase: 0.86, dotted: true },
  { rx: 980, ry: 252, seconds: 100, moon: 3, phase: 0.1, dotted: false },
];
const TILT = -10;

/** Зүүн цэгээс эхэлж урд талаар (доогуур) баруун тийш, араар нь буцах эллипс. */
function orbitPath(rx: number, ry: number): string {
  return `M${-rx} 0A${rx} ${ry} 0 0 0 ${rx} 0A${rx} ${ry} 0 0 0 ${-rx} 0`;
}

/**
 * Тэмдгийг тойрсон хазгай тойрог замууд (тэмдгийн цагираг шиг), тэдгээрээр
 * аажуухан эргэх сарнууд, бүдэг ба анивчих одод. Хуудасны дэвсгэр дээр,
 * текстийн ард. Хөдөлгөөн багасгах тохиргоотой бол бүгд зогсонги; дэлгэцээс
 * гарахад эсвэл «зогсоох» товчоор SMIL болон CSS хөдөлгөөн түр зогсоно.
 */
function HeroOrbits({ paused }: { paused: boolean }) {
  const id = useId().replace(/[^a-zA-Z0-9_-]/g, "");
  const svgRef = useRef<SVGSVGElement>(null);
  const motion = useMediaQuery("(prefers-reduced-motion: no-preference)");
  const [visible, setVisible] = useState(true);

  useEffect(() => {
    const svg = svgRef.current;
    if (!svg || !motion) return;
    // Нэг дуудлагад хэд хэдэн бичлэг ирж болно — сүүлийнх нь одоогийн төлөв.
    const observer = new IntersectionObserver((entries) => {
      setVisible(entries.at(-1)?.isIntersecting ?? true);
    });
    observer.observe(svg);
    return () => observer.disconnect();
  }, [motion]);

  // Дэлгэцээс гарсан эсвэл хэрэглэгч зогсоосон үед SMIL ба CSS хөдөлгөөн зогсоно.
  useEffect(() => {
    const svg = svgRef.current;
    if (!svg || !motion) return;
    const running = visible && !paused;
    if (running) svg.unpauseAnimations();
    else svg.pauseAnimations();
    svg.toggleAttribute("data-paused", !running);
  }, [motion, visible, paused]);

  return (
    <svg
      ref={svgRef}
      aria-hidden
      viewBox="-1280 -300 2560 600"
      fill="none"
      className="group/orbits text-primary pointer-events-none absolute top-1/2 left-1/2 -z-10 h-[37.5rem] w-[160rem] max-w-none -translate-x-1/2 -translate-y-1/2"
    >
      <defs>
        {/* Төвөөс холдох тусам (босоо чиглэлд илүү хурдан) уусна. */}
        <radialGradient
          id={`${id}-fade`}
          gradientUnits="userSpaceOnUse"
          cx="0"
          cy="0"
          r="1100"
          gradientTransform="scale(1 0.3)"
        >
          <stop offset="0" stopColor="currentColor" stopOpacity={0.75} />
          <stop offset="0.3" stopColor="currentColor" stopOpacity={0.45} />
          <stop offset="0.65" stopColor="currentColor" stopOpacity={0.18} />
          <stop offset="1" stopColor="currentColor" stopOpacity={0} />
        </radialGradient>
        {/* Гарчиг, тайлбар, шошгоны ард замууд бүдгэрнэ — сар бичвэрийн ард гялалзахгүй. */}
        <radialGradient id={`${id}-hole`}>
          <stop offset="0.5" stopColor="black" stopOpacity={0.8} />
          <stop offset="1" stopColor="black" stopOpacity={0} />
        </radialGradient>
        <mask
          id={`${id}-text`}
          maskUnits="userSpaceOnUse"
          x="-1280"
          y="-300"
          width="2560"
          height="600"
        >
          <rect x="-1280" y="-300" width="2560" height="600" fill="white" />
          <ellipse cx="330" cy="72" rx="430" ry="150" fill={`url(#${id}-hole)`} />
        </mask>
      </defs>

      <g mask={`url(#${id}-text)`}>
        <g className="text-foreground" fill="currentColor">
          {STARS.map((star, index) => (
            <circle key={index} cx={star.x} cy={star.y} r={star.r} opacity={star.opacity} />
          ))}
        </g>

        <g transform={`rotate(${TILT})`}>
          {RINGS.map((ring) => (
            <path
              key={ring.rx}
              d={orbitPath(ring.rx, ring.ry)}
              stroke={`url(#${id}-fade)`}
              strokeWidth={ring.dotted ? 1.6 : 1}
              strokeDasharray={ring.dotted ? "0.5 9" : undefined}
              strokeLinecap="round"
            />
          ))}
          {RINGS.map((ring) => {
            const angle = ring.phase * 2 * Math.PI;
            return (
              <g
                key={ring.rx}
                fill="currentColor"
                transform={
                  motion
                    ? undefined
                    : `translate(${round(-ring.rx * Math.cos(angle))} ${round(ring.ry * Math.sin(angle))})`
                }
              >
                <circle r={ring.moon * 2.8} opacity={0.16} />
                <circle r={ring.moon} />
                {motion && (
                  <animateMotion
                    dur={`${ring.seconds}s`}
                    begin={`${-round(ring.phase * ring.seconds)}s`}
                    repeatCount="indefinite"
                    path={orbitPath(ring.rx, ring.ry)}
                  />
                )}
              </g>
            );
          })}
        </g>

        <g fill="currentColor">
          {SPARKS.map(([x, y, size, delay]) => (
            <g key={`${x}-${y}`} transform={`translate(${x} ${y})`}>
              <path
                d={sparkPath(size)}
                className="motion-safe:animate-live-twinkle origin-center [transform-box:fill-box] group-data-paused/orbits:[animation-play-state:paused]"
                style={{ animationDelay: `${delay}s` }}
              />
            </g>
          ))}
        </g>
      </g>
    </svg>
  );
}
