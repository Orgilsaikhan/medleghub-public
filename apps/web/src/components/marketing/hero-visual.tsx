"use client";

import { CheckCircle2Icon, PlayIcon, SmartphoneIcon } from "lucide-react";
import Image from "next/image";
import { type ReactNode, useEffect, useRef } from "react";

import { Button } from "@/components/ui/button";
import { BADGE_FILES } from "@/lib/badge-manifest";
import { useDeviceTilt } from "@/lib/hooks/use-device-tilt";
import { mn } from "@/lib/i18n/mn";
import { cn } from "@/lib/utils";

/** Hero дотор харагдах жишээ код — платформын гол санааг нэг харцаар өгнө. */
const DEMO_CODE = `const ner = "Бат";

console.log("Сайн байна уу, " + ner + "!");`;

const DEMO_OUTPUT = "Сайн байна уу, Бат!";

/** Курсор байхгүй үеийн хазайлт (градус). */
const REST_X = 6;
const REST_Y = -14;
/** Гялбааны тайван байрлал (%) — `CodeWindow`-ийн `var(--gx, 15%)`, `var(--gy, 0%)`. */
const GLARE_X = 15;
const GLARE_Y = 0;
/**
 * Утсыг хазайлгахад тайван байрлалаас хамгийн ихдээ хэдэн градус эргэх. Утас
 * босоо болоход «Ажиллуулах» консолын мөр рүү дээшилдэг тул тэр чиглэлд бага.
 * 360–1914 px өргөнд аль ч хазайлтад хөвөгч хэсэг бичвэрийг дарахгүй, хуудаснаас
 * гарахгүй байхаар хэмжиж тогтоосон — байрлалыг нь өөрчилбөл дахин шалга.
 */
const GYRO_UP = 2;
const GYRO_DOWN = 12;
const GYRO_SIDE = 12;
/** Утсыг хазайлгахад гялбаа хэдэн хувь шилжих. */
const GYRO_GLARE = 40;

const TILT_VARS = ["--rx", "--ry", "--gx", "--gy"] as const;

/** Хазайлт (градус), гялбаа (%) — CSS хувьсагчаар (React state биш). */
function setTilt(plane: HTMLElement, rx: number, ry: number, gx: number, gy: number) {
  plane.style.setProperty("--rx", `${rx}deg`);
  plane.style.setProperty("--ry", `${ry}deg`);
  plane.style.setProperty("--gx", `${gx}%`);
  plane.style.setProperty("--gy", `${gy}%`);
}

function clearTilt(plane: HTMLElement) {
  for (const name of TILT_VARS) plane.style.removeProperty(name);
}

/**
 * Hero-гийн 3D жишээ. Кодын цонх орон зайд хазайж, хулганыг дагаж эргэнэ;
 * утсан дээр утасны хазайлтыг (gyro) дагана. Эргэн тойронд нь «тест давлаа»,
 * «Ажиллуулах», шинэ амжилт гэсэн хэсгүүд өөр өөр гүнд (`translateZ`) хөвнө —
 * хазайхад тэд цонхноос илүү хөдөлж гүн мэдрэгдэнэ. Цонхон дээр курсорыг
 * дагасан гялбаа тусна.
 *
 * Байрлалыг CSS хувьсагчаар тавина (React state биш). Хөдөлгөөн багасгах
 * тохиргоотой бол тогтмол хазайлттай, хөвөхгүй.
 */
export function HeroVisual() {
  const sceneRef = useRef<HTMLDivElement>(null);
  const planeRef = useRef<HTMLDivElement>(null);

  // Утсыг хазайлгахад цонх эсрэг тийш эргэж орон зайд «тогтсон» мэт харагдана:
  // баруун тал нь доошилбол цонхны баруун тал ойртоно. Гялбаа нь хулганы үеийнх
  // шиг эргэлтээ дагана. `data-gyro` үед CSS transition унтарна — rAF зөөлрүүлнэ.
  const gyro = useDeviceTilt(sceneRef, (tilt) => {
    const plane = planeRef.current;
    if (!plane) return;
    if (!tilt) {
      delete plane.dataset.gyro;
      clearTilt(plane);
      return;
    }
    plane.dataset.gyro = "";
    setTilt(
      plane,
      REST_X + tilt.y * (tilt.y > 0 ? GYRO_UP : GYRO_DOWN),
      REST_Y - tilt.x * GYRO_SIDE,
      GLARE_X - tilt.x * GYRO_GLARE,
      GLARE_Y - tilt.y * GYRO_GLARE,
    );
  });

  const onPointerMove = (event: React.PointerEvent<HTMLDivElement>) => {
    const plane = planeRef.current;
    // Утас хазайлтыг удирдаж байвал хулгана оролцохгүй.
    if (!plane || event.pointerType !== "mouse" || plane.dataset.gyro !== undefined) return;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    const rect = event.currentTarget.getBoundingClientRect();
    const x = (event.clientX - rect.left) / rect.width - 0.5;
    const y = (event.clientY - rect.top) / rect.height - 0.5;
    setTilt(plane, REST_X - y * 12, REST_Y + x * 20, (x + 0.5) * 100, (y + 0.5) * 100);
  };

  const onPointerLeave = (event: React.PointerEvent<HTMLDivElement>) => {
    const plane = planeRef.current;
    // Хуруу өргөхөд ч `pointerleave` ирдэг — утасны хазайлтыг арилгахгүй.
    if (!plane || event.pointerType !== "mouse" || plane.dataset.gyro !== undefined) return;
    clearTilt(plane);
  };

  return (
    <div
      ref={sceneRef}
      onPointerMove={onPointerMove}
      onPointerLeave={onPointerLeave}
      // `min-w-0`: торны нүд кодын урт мөрөөр тэлж, утсан дээр хуудаснаас
      // халихгүй — урт мөр цонхон дотроо гүйлгэгдэнэ.
      className="relative min-w-0 py-8 [perspective:1400px]"
    >
      <div
        ref={planeRef}
        style={{ transform: `rotateX(var(--rx, ${REST_X}deg)) rotateY(var(--ry, ${REST_Y}deg))` }}
        className="relative transition-transform duration-300 ease-out [transform-style:preserve-3d] data-gyro:transition-none motion-reduce:transition-none"
      >
        <CodeWindow />

        {/* Гүнд байгаа хэсэг перспективээр томорч, эргэлтээрээ хажуу тийш
            шилждэг. Тиймээс цонхноос гадагш цухуйлгах нь зөвхөн хажууд зай
            байгаа өргөнд — бусад үед цонхон дотор, кодын бичвэрээс зайдуу. */}
        <Floating
          depth={90}
          delay="0s"
          className="-top-5 right-3 sm:right-2 lg:-right-3 2xl:-right-6"
        >
          <span className="bg-card/95 flex items-center gap-2 rounded-full border px-3.5 py-2 text-sm font-medium shadow-xl backdrop-blur">
            <CheckCircle2Icon className="text-success size-4" aria-hidden />
            {mn.home.heroTestsPassed}
          </span>
        </Floating>

        <Floating depth={120} delay="-1.7s" className="-bottom-9 left-8 lg:-left-8">
          <span className="bg-primary text-primary-foreground shadow-primary/30 flex items-center gap-2 rounded-full px-4 py-2 text-sm font-semibold shadow-xl">
            <PlayIcon className="size-4 fill-current" aria-hidden />
            {mn.home.heroRun}
          </span>
        </Floating>

        {/* Консолын хэсэгт: lg өргөнд кодын урт мөр яг дээгүүр нь гардаг тул
            хазайхад (хулгана, утас) мөрийг дарахгүй байх зай үлдээнэ. */}
        <Floating
          depth={60}
          delay="-3.4s"
          className="top-[70%] right-4 hidden sm:block 2xl:-right-14"
        >
          <span className="bg-card/95 flex items-center gap-3 rounded-2xl border p-2.5 pr-4 shadow-xl backdrop-blur">
            {BADGE_FILES["first-commit"] && (
              <Image
                src={BADGE_FILES["first-commit"]}
                alt=""
                width={40}
                height={40}
                className="size-10 rounded-xl"
              />
            )}
            <span>
              <span className="text-muted-foreground block text-xs">{mn.home.heroNewBadge}</span>
              <span className="block text-sm font-semibold">First Commit</span>
            </span>
          </span>
        </Floating>
      </div>

      {/* iOS Safari хөдөлгөөн мэдрэгчийг зөвхөн товшилтоор зөвшөөрүүлдэг. Hero-гийн
          доод зайд байрлана — гарч ирэхэд хуудас шилжихгүй. */}
      {gyro.needsPermission && (
        <Button
          variant="outline"
          onClick={gyro.requestPermission}
          className="bg-card/90 dark:bg-card/80 motion-safe:animate-in motion-safe:fade-in-0 motion-safe:slide-in-from-top-1 absolute top-full right-0 mt-1 h-8 rounded-full px-3.5 text-xs shadow-lg backdrop-blur duration-500"
        >
          <SmartphoneIcon aria-hidden />
          {mn.home.heroGyro}
        </Button>
      )}
    </div>
  );
}

/**
 * Цонхны өмнө хөвөх чимэглэл. `depth` — цонхноос хэр урагш (px). Хөвөх
 * хөдөлгөөн нь `translate` шинжээр тул 3D `transform`-той давхцахгүй.
 */
function Floating({
  depth,
  delay,
  className,
  children,
}: {
  depth: number;
  delay: string;
  className?: string;
  children: ReactNode;
}) {
  return (
    <div
      aria-hidden
      style={{ transform: `translateZ(${depth}px)`, animationDelay: delay }}
      className={cn("motion-safe:animate-float pointer-events-none absolute", className)}
    >
      {children}
    </div>
  );
}

function CodeWindow() {
  const preRef = useRef<HTMLPreElement>(null);

  // Утсан дээр урт мөр хэвтээгээр гүйлгэгдэнэ — тэр үед л Tab-аар очиж гарын
  // түлхүүрээр гүйлгэнэ (WCAG 2.1.1); өргөн дэлгэцэд илүү зогсоол нэмэхгүй.
  useEffect(() => {
    const pre = preRef.current;
    if (!pre) return;
    const sync = () => {
      if (pre.scrollWidth > pre.clientWidth) pre.tabIndex = 0;
      else pre.removeAttribute("tabindex");
    };
    const observer = new ResizeObserver(sync);
    observer.observe(pre);
    // Фонт ачаалагдахад мөрийн урт өөрчлөгдөж болно.
    void document.fonts?.ready.then(sync);
    return () => observer.disconnect();
  }, []);

  return (
    <div className="bg-card shadow-primary/10 relative overflow-hidden rounded-xl border shadow-2xl">
      <div className="bg-muted/50 flex items-center gap-2 border-b px-4 py-2.5">
        <span aria-hidden className="flex gap-1.5">
          <span className="size-2.5 rounded-full bg-red-400/70" />
          <span className="size-2.5 rounded-full bg-amber-400/70" />
          <span className="size-2.5 rounded-full bg-green-400/70" />
        </span>
        <span className="text-muted-foreground ml-2 font-mono text-xs">hicheel.js</span>
      </div>

      <pre
        ref={preRef}
        className="bg-code-bg focus-visible:ring-ring overflow-x-auto p-5 font-mono text-sm leading-relaxed focus-visible:ring-2 focus-visible:outline-none focus-visible:ring-inset"
      >
        <code>{DEMO_CODE}</code>
      </pre>

      <div className="border-t">
        <div className="text-muted-foreground bg-muted/30 px-4 py-2 font-mono text-xs">
          {mn.learn.console}
        </div>
        <div className="px-5 py-4 font-mono text-sm">
          <span className="text-success">›</span> {DEMO_OUTPUT}
        </div>
      </div>

      {/* Курсор, утасны хазайлтыг дагах гялбаа (`--gx/--gy` нь дээд элементээс). */}
      <span
        aria-hidden
        className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_var(--gx,15%)_var(--gy,0%),rgb(255_255_255/0.09),transparent_55%)]"
      />
    </div>
  );
}
