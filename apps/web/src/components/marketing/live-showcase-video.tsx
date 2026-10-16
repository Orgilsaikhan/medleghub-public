"use client";

import { CircleCheckIcon, LockIcon, PauseIcon, PlayIcon, SparklesIcon } from "lucide-react";
import {
  type CSSProperties,
  type ReactNode,
  useEffect,
  useRef,
  useState,
  useSyncExternalStore,
} from "react";

import { LiveMark } from "@/components/live/live-mark";
import { useLivePlayback } from "@/components/marketing/live-showcase-stage";
import { useMediaQuery } from "@/lib/hooks/use-media-query";
import { mn } from "@/lib/i18n/mn";
import { cn } from "@/lib/utils";

/**
 * Хэсгийн видео. Өөрийн бичлэгээр солих бол:
 * 1. Файлаа `public/videos/`-д хийнэ. MP4 (H.264) бүх хөтөч, iPhone-д ч
 *    тоглоно; WebM-ийг хамт өгч болно — хөтөч жагсаалтаас тоглуулж чадах
 *    эхнийхийг нь авна: `{ src: "/videos/live.mp4", type: "video/mp4" }`.
 * 2. `poster`-т эхний кадрын зургийг (видеотой ижил харьцаатай), `width`,
 *    `height`-д видеоны хэмжээг бичнэ — цонх тэр харьцаагаар зурагдана.
 * 3. Агуулга нь өөр бол `mn.homeLive.videoCaption`-ыг (дэлгэц уншигчид
 *    зориулсан тайлбар) шинэчилнэ.
 * Видео үргэлж дуугүй тоглодог тул дуу хэрэггүй.
 */
export const LIVE_DEMO_VIDEO = {
  sources: [{ src: "/videos/live-demo.webm", type: 'video/webm; codecs="vp8"' }],
  poster: "/videos/live-demo-poster.webp",
  width: 1280,
  height: 800,
  /** Цонхны хаягийн мөрөнд харагдах бичвэр. */
  address: "medleghub.com/live",
};

const t = mn.homeLive;

/** Курсор байхгүй үеийн хазайлт (градус, `lg`-ээс өргөнд) — hero-гийн цонхны толин тусгал. */
const REST_X = 4;
const REST_Y = 9;
/** Хоёр давхаргын хазайлт: `--rx/--ry` курсорыг дагана, үгүй бол тайван байрлал. */
const TILT =
  "rotateX(var(--rx, var(--home-live-rest-x))) rotateY(var(--ry, var(--home-live-rest-y)))";
const PLANE = "transition-transform duration-500 ease-out motion-reduce:transition-none";
/** Видеоны хэдэн хувь нь харагдвал тоглох вэ. */
const PLAY_RATIO = 0.35;
/** Эзэмшлийн цагирагийн утга (чимэглэл). */
const MASTERY = 86;

const subscribeNever = () => () => {};

let playableCache: boolean | null = null;
/** Хөтөч эх файлуудын ядаж нэгийг тоглуулж чадах уу (жишээ нь WebM-гүй хуучин iPhone). */
function canPlaySomeSource() {
  if (playableCache === null) {
    const probe = document.createElement("video");
    playableCache = LIVE_DEMO_VIDEO.sources.some((source) => probe.canPlayType(source.type) !== "");
  }
  return playableCache;
}

/** «Өгөгдөл хэмнэх» горимд видео өөрөө тоглохгүй. */
function prefersSaveData() {
  const connection = (navigator as Navigator & { connection?: { saveData?: boolean } }).connection;
  return connection?.saveData === true;
}

/**
 * Live-ийн жишээ видео 3D цонхон дотор. Цонх hero-гийнх шиг хазайж, хулганыг
 * дагана; эргэн тойронд нь чимэглэлийн хэсгүүд өөр гүнд (`translateZ`) хөвнө.
 *
 * Хоёр давхарга ижил хазайна: (1) дэлгэц ба товч — хавтгай, учир нь
 * `preserve-3d` дотор Chromium товчийг буруу газар «дардаг»; (2) хөвөгч
 * чимэглэл — `preserve-3d`, дарагдахгүй.
 *
 * Видео дуугүй, давтагдана; харагдах хэсэгт орвол өөрөө тоглож, гарвал
 * зогсоно. Хөдөлгөөн багасгах, өгөгдөл хэмнэх тохиргоотой бол өөрөө
 * тоглохгүй — poster ба «Тоглуулах» товч. Нэг л товч (WCAG 2.2.2): тоглож
 * байхад буланд «Зогсоох», зогссон үед голд том «Тоглуулах» — нэг элемент
 * тул фокус алдагдахгүй.
 */
export function LiveShowcaseVideo() {
  const { playback, setPlayback, setVideoActive } = useLivePlayback();
  const motionAllowed = useMediaQuery("(prefers-reduced-motion: no-preference)");
  const saveData = useSyncExternalStore(subscribeNever, prefersSaveData, () => false);
  const playable = useSyncExternalStore(subscribeNever, canPlaySomeSource, () => true);

  const frameRef = useRef<HTMLDivElement>(null);
  const stageRef = useRef<HTMLDivElement>(null);
  const videoRef = useRef<HTMLVideoElement>(null);
  const barRef = useRef<HTMLSpanElement>(null);
  const [inView, setInView] = useState(false);
  const [playing, setPlaying] = useState(false);
  /** Хөтөч өөрөө тоглуулахыг хориглосон (жишээ нь iPhone-ий батарей хэмнэх горим). */
  const [blocked, setBlocked] = useState(false);
  /** Файлыг ачаалж эсвэл задалж чадсангүй — зөвхөн эхний кадр үлдэнэ. */
  const [failed, setFailed] = useState(false);

  const canPlay = playable && !failed;
  const autoplay = motionAllowed && !saveData && !blocked;
  const active = canPlay && (playback === "playing" || (playback === "auto" && autoplay));

  // Давтагдах чимэглэл видеотой хамт л хөдөлнө — видео зогссон, өөрөө
  // тоглож чадаагүй үед ч зогсоно (WCAG 2.2.2: нэг товч хоёуланг нь удирдана).
  useEffect(() => setVideoActive(active), [active, setVideoActive]);

  useEffect(() => {
    const frame = frameRef.current;
    if (!frame) return;
    const observer = new IntersectionObserver(
      (entries) => setInView((entries.at(-1)?.intersectionRatio ?? 0) >= PLAY_RATIO),
      { threshold: [0, PLAY_RATIO] },
    );
    observer.observe(frame);
    return () => observer.disconnect();
  }, []);

  useEffect(() => {
    const video = videoRef.current;
    if (!video) return;
    if (!active || !inView) {
      video.pause();
      return;
    }
    video.muted = true;
    video.play().catch((error: unknown) => {
      // `pause()` тоглуулалтыг таслах нь (AbortError) хэвийн.
      if (!(error instanceof DOMException)) return;
      if (error.name === "NotAllowedError") setBlocked(true);
      if (error.name === "NotSupportedError") setFailed(true);
    });
  }, [active, inView]);

  // Явцын нимгэн зураас — тоглож байх үед л кадр бүрт шинэчлэгдэнэ.
  useEffect(() => {
    const video = videoRef.current;
    const bar = barRef.current;
    if (!video || !bar || !playing) return;
    let frame = 0;
    const tick = () => {
      if (video.duration > 0) bar.style.transform = `scaleX(${video.currentTime / video.duration})`;
      frame = requestAnimationFrame(tick);
    };
    frame = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(frame);
  }, [playing]);

  const toggle = () => {
    if (active) {
      setPlayback("paused");
      return;
    }
    setPlayback("playing");
    // Товч дарсан мөчид шууд — зарим хөтөч хэрэглэгчийн үйлдлийн дотор л зөвшөөрнө.
    const video = videoRef.current;
    if (video) {
      video.muted = true;
      video.play().catch(() => {});
    }
  };

  const onPointerMove = (event: React.PointerEvent<HTMLDivElement>) => {
    const stage = stageRef.current;
    if (!stage || event.pointerType !== "mouse" || !motionAllowed) return;
    const rect = event.currentTarget.getBoundingClientRect();
    const x = (event.clientX - rect.left) / rect.width - 0.5;
    const y = (event.clientY - rect.top) / rect.height - 0.5;
    // Хулгана дээр нь ирэхэд цонх шулуудаж (үзэхэд амар), курсорыг бага зэрэг дагана.
    stage.style.setProperty("--rx", `${REST_X * 0.3 - y * 8}deg`);
    stage.style.setProperty("--ry", `${REST_Y * 0.3 + x * 12}deg`);
    stage.style.setProperty("--gx", `${(x + 0.5) * 100}%`);
    stage.style.setProperty("--gy", `${(y + 0.5) * 100}%`);
  };

  const onPointerLeave = () => {
    const stage = stageRef.current;
    if (!stage) return;
    for (const name of ["--rx", "--ry", "--gx", "--gy"]) stage.style.removeProperty(name);
  };

  return (
    <figure className="relative min-w-0">
      {/* Цонхны ард шар гэрэл — аажуухан хөвнө. */}
      <div aria-hidden className="home-live-glow pointer-events-none absolute inset-0 -z-10">
        <div className="bg-primary/25 dark:bg-primary/20 motion-safe:animate-glow-drift home-live-loop absolute top-1/2 left-1/2 size-[min(36rem,120%)] -translate-x-1/2 -translate-y-1/2 rounded-full blur-3xl" />
      </div>

      <div
        onPointerMove={onPointerMove}
        onPointerLeave={onPointerLeave}
        className="relative py-6 [perspective:1400px]"
      >
        {/* Хазайлтын хувьсагч (`--rx/--ry`) энд — хоёр давхарга адил хазайна. */}
        <div
          ref={stageRef}
          className={cn(
            "home-live-frame-rise relative [perspective:1400px]",
            "[--home-live-rest-x:2deg] [--home-live-rest-y:4deg] lg:[--home-live-rest-x:4deg] lg:[--home-live-rest-y:9deg]",
          )}
        >
          {/* 1. Дэлгэц ба удирдлага — хавтгай давхарга. */}
          <div style={{ transform: TILT }} className={PLANE}>
            <div
              ref={frameRef}
              className="home-live-screen bg-card shadow-primary/15 relative overflow-hidden rounded-2xl border shadow-2xl"
            >
              <div className="bg-muted/50 flex items-center gap-3 border-b px-4 py-2.5">
                <span aria-hidden className="flex shrink-0 gap-1.5">
                  <span className="size-2.5 rounded-full bg-red-400/70" />
                  <span className="size-2.5 rounded-full bg-amber-400/70" />
                  <span className="size-2.5 rounded-full bg-green-400/70" />
                </span>
                <span className="bg-background/70 text-muted-foreground mx-auto flex min-w-0 items-center gap-1.5 rounded-md border px-3 py-0.5 font-mono text-xs">
                  <LockIcon aria-hidden className="size-3 shrink-0" />
                  <span className="truncate">{LIVE_DEMO_VIDEO.address}</span>
                </span>
                <LiveMark className="text-brand-link size-4" />
              </div>

              <div
                className="relative overflow-hidden bg-black"
                style={{ aspectRatio: `${LIVE_DEMO_VIDEO.width} / ${LIVE_DEMO_VIDEO.height}` }}
              >
                {canPlay ? (
                  <video
                    ref={videoRef}
                    muted
                    loop
                    playsInline
                    // Чимэглэлийн давталт — PiP, дамжуулах товч хэрэггүй.
                    disablePictureInPicture
                    disableRemotePlayback
                    preload="none"
                    poster={LIVE_DEMO_VIDEO.poster}
                    width={LIVE_DEMO_VIDEO.width}
                    height={LIVE_DEMO_VIDEO.height}
                    onPlaying={() => setPlaying(true)}
                    onPause={() => setPlaying(false)}
                    onError={() => setFailed(true)}
                    // Утгыг `figcaption` хэлнэ.
                    aria-hidden
                    className="absolute inset-0 size-full object-cover"
                  >
                    {LIVE_DEMO_VIDEO.sources.map((source) => (
                      <source
                        key={source.src}
                        src={source.src}
                        type={source.type}
                        onError={() => setFailed(true)}
                      />
                    ))}
                  </video>
                ) : (
                  // Тоглуулж чадахгүй хөтөчид — зөвхөн эхний кадр. Зогсоох товч байхгүй
                  // тул давтагдах чимэглэл ч зогсоно (`data-video-off`, `globals.css`).
                  // eslint-disable-next-line @next/next/no-img-element
                  <img
                    data-video-off
                    src={LIVE_DEMO_VIDEO.poster}
                    alt=""
                    width={LIVE_DEMO_VIDEO.width}
                    height={LIVE_DEMO_VIDEO.height}
                    className="absolute inset-0 size-full object-cover"
                  />
                )}

                {/* Орж ирэхэд нэг удаа гүйх «AI уншиж байна» гэрлийн зураас. */}
                <span
                  aria-hidden
                  className="home-live-scan pointer-events-none absolute inset-0 opacity-0"
                />

                {canPlay && (
                  <>
                    <span
                      aria-hidden
                      className="pointer-events-none absolute inset-x-0 bottom-0 h-0.5 bg-white/15"
                    >
                      <span
                        ref={barRef}
                        style={{ transform: "scaleX(0)" }}
                        className="bg-primary block h-full origin-left"
                      />
                    </span>
                    {/* Нэр нь төлвөө хэлнэ («зогсоох» / «тоглуулах») — aria-pressed хэрэггүй. */}
                    <button
                      type="button"
                      onClick={toggle}
                      aria-label={active ? t.videoPause : t.videoPlay}
                      className={cn(
                        "absolute z-10 grid -translate-x-1/2 -translate-y-1/2 place-items-center rounded-full outline-none",
                        "transition-[top,left,width,height,background-color] duration-300 ease-out motion-reduce:transition-none",
                        "focus-visible:outline-primary focus-visible:outline-3 focus-visible:outline-offset-2 focus-visible:outline-solid",
                        active
                          ? "top-[calc(100%-2rem)] left-[calc(100%-2rem)] size-10 bg-black/60 text-white ring-1 ring-white/25 backdrop-blur hover:bg-black/80"
                          : "bg-primary text-primary-foreground hover:bg-primary-hover top-1/2 left-1/2 size-16 shadow-xl shadow-black/40",
                      )}
                    >
                      {active ? (
                        <PauseIcon aria-hidden className="size-4 fill-current" />
                      ) : (
                        <PlayIcon aria-hidden className="ml-0.5 size-6 fill-current" />
                      )}
                    </button>
                  </>
                )}
              </div>

              {/* Курсорыг дагах гялбаа (`--gx/--gy` нь дээд элементээс). */}
              <span
                aria-hidden
                className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_var(--gx,85%)_var(--gy,0%),rgb(255_255_255/0.08),transparent_55%)]"
              />
            </div>

            {/* Дэлгэц асахад гялсхийх шугам — ТВ асах мэт. */}
            <span
              aria-hidden
              className="home-live-screen-line bg-primary pointer-events-none absolute inset-x-0 top-1/2 h-0.5 rounded-full opacity-0 shadow-[0_0_24px_4px_var(--primary)]"
            />
          </div>

          {/* 2. Хөвөгч чимэглэл — тусдаа `preserve-3d` давхарга, ижил хазайлттай:
              гүнд байгаа нь хазайхад цонхноос илүү хөдөлж гүн мэдрэгдэнэ.
              Видеоны «Зогсоох» товч баруун доод буланд — чимэглэл түүнийг халхлахгүй. */}
          <div
            aria-hidden
            style={{ transform: TILT }}
            className={cn(
              PLANE,
              "pointer-events-none absolute inset-0 [transform-style:preserve-3d]",
            )}
          >
            <Chip
              depth={90}
              delay="0s"
              pop="1.05s"
              className="-top-6 left-3 hidden sm:block 2xl:-left-8"
            >
              <MasteryChip />
            </Chip>
            <Chip depth={120} delay="-1.6s" pop="1.2s" className="-bottom-5 left-8 lg:left-12">
              <span className="bg-primary text-primary-foreground shadow-primary/30 flex items-center gap-2 rounded-full px-4 py-2 text-sm font-semibold shadow-xl">
                <SparklesIcon className="size-4" aria-hidden />
                {t.chipAi}
              </span>
            </Chip>
            <Chip
              depth={60}
              delay="-3.2s"
              pop="1.35s"
              className="top-[40%] -right-5 hidden xl:block 2xl:-right-10"
            >
              <span className="bg-card/95 flex items-center gap-2 rounded-full border px-3.5 py-2 text-sm font-medium shadow-xl backdrop-blur">
                <CircleCheckIcon className="text-success size-4" aria-hidden />
                {t.chipScore}
              </span>
            </Chip>
          </div>
        </div>
      </div>

      <figcaption className="sr-only">{t.videoCaption}</figcaption>
    </figure>
  );
}

/** Эзэмшлийн цагираг — орж ирэхэд 0-ээс дүүрнэ. */
function MasteryChip() {
  return (
    <span className="bg-card/95 flex items-center gap-3 rounded-2xl border p-2.5 pr-4 shadow-xl backdrop-blur">
      <svg viewBox="0 0 40 40" className="size-10 -rotate-90">
        <circle
          cx="20"
          cy="20"
          r="16"
          fill="none"
          strokeWidth="4"
          className="stroke-foreground/10"
        />
        <circle
          cx="20"
          cy="20"
          r="16"
          fill="none"
          strokeWidth="4"
          strokeLinecap="round"
          pathLength={100}
          strokeDasharray="100"
          strokeDashoffset={100 - MASTERY}
          className="home-live-ring stroke-primary"
        />
      </svg>
      <span>
        <span className="text-muted-foreground block text-xs">{t.chipMastery}</span>
        <span className="block text-sm font-semibold tabular-nums">{MASTERY}%</span>
      </span>
    </span>
  );
}

/**
 * Цонхны өмнө хөвөх чимэглэл. `depth` — цонхноос хэр урагш (px), `pop` —
 * орж ирэх хөдөлгөөний саатал. Хөвөх нь `translate` шинжээр тул 3D
 * `transform`-той давхцахгүй.
 */
function Chip({
  depth,
  delay,
  pop,
  className,
  children,
}: {
  depth: number;
  delay: string;
  pop: string;
  className?: string;
  children: ReactNode;
}) {
  return (
    <div style={{ transform: `translateZ(${depth}px)` }} className={cn("absolute", className)}>
      <div className="home-live-pop" style={{ "--home-live-delay": pop } as CSSProperties}>
        <div style={{ animationDelay: delay }} className="motion-safe:animate-float home-live-loop">
          {children}
        </div>
      </div>
    </div>
  );
}
