"use client";

import { ChevronLeftIcon, ChevronRightIcon, PauseIcon, PlayIcon } from "lucide-react";
import { useEffect, useRef, useState } from "react";

import { CourseCard } from "@/components/courses/course-card";
import { Button } from "@/components/ui/button";
import { mn } from "@/lib/i18n/mn";
import type { CourseSummary } from "@/lib/types/api";

/** Автоматаар гүйх хурд — пиксел/миллисекунд (≈ 36 px/с). */
const SPEED = 0.036;
/** Картуудын хоорондох зай (`gap-6`) — сум дарахад нэг карт шилжүүлнэ. */
const GAP_PX = 24;
/** Хуруугаар гүйлгэсэн эсвэл сум дарсны дараа автомат гүйлгээ сэргэх хугацаа. */
const RESUME_AFTER_TOUCH_MS = 1600;
const RESUME_AFTER_NUDGE_MS = 1400;

const reducedMotion = () => window.matchMedia("(prefers-reduced-motion: reduce)").matches;

/**
 * Бүх сургалт тасралтгүй урсдаг мөр (marquee).
 *
 * CSS transform биш, жинхэнэ гүйлгэх хэсэг: Tab-аар очсон карт харагдах
 * хэсэгт өөрөө гүйлгэгдэнэ, утсан дээр хуруугаар гүйлгэж болно. Жагсаалт
 * хоёр удаа зурагдаж, эхний хуулбарын өргөнд хүрэхэд эхэнд нь буцна — зааг
 * нь мэдэгдэхгүй. Хоёр дахь хуулбар `inert`: Tab, дэлгэц уншигчид орохгүй.
 *
 * Хулгана аваачих, фокуслах, хуруугаар хүрэхэд зогсоно. «Зогсоох» товч нь
 * WCAG 2.2.2 (Pause, Stop, Hide)-ийн шаардлага. Хөдөлгөөн багасгах
 * тохиргоотой бол огт хөдлөхгүй — энгийн гүйлгэдэг мөр болно.
 */
export function CourseMarquee({ courses }: { courses: CourseSummary[] }) {
  const scrollerRef = useRef<HTMLDivElement>(null);
  const groupRef = useRef<HTMLDivElement>(null);
  /** Энэ мөч хүртэл автомат гүйлгээ хүлээнэ (`Infinity` — хулгана дээр нь). */
  const holdUntil = useRef(0);
  const visible = useRef(true);
  const [paused, setPaused] = useState(false);

  const hold = (ms = Number.POSITIVE_INFINITY) => {
    holdUntil.current = performance.now() + ms;
  };

  // Дэлгэцэн дээр харагдахгүй үед гүйлгэхгүй.
  useEffect(() => {
    const scroller = scrollerRef.current;
    if (!scroller) return;
    const observer = new IntersectionObserver(([entry]) => {
      visible.current = entry?.isIntersecting ?? true;
    });
    observer.observe(scroller);
    return () => observer.disconnect();
  }, []);

  useEffect(() => {
    const scroller = scrollerRef.current;
    const group = groupRef.current;
    if (!scroller || !group || paused || reducedMotion()) return;

    // Бутархай байрлалыг өөрөө хадгална — `scrollLeft` бүхэл тоо руу дугуйрдаг.
    let position = scroller.scrollLeft;
    let last = performance.now();
    let frame = 0;
    const step = (now: number) => {
      const elapsed = Math.min(now - last, 64);
      last = now;
      if (now < holdUntil.current) {
        position = scroller.scrollLeft; // гараар гүйлгэснийг дагана
      } else if (visible.current) {
        const loop = group.offsetWidth;
        position += SPEED * elapsed;
        if (position >= loop) position -= loop;
        scroller.scrollLeft = position;
      }
      frame = requestAnimationFrame(step);
    };
    frame = requestAnimationFrame(step);
    return () => cancelAnimationFrame(frame);
  }, [paused]);

  /** Сумаар нэг карт шилжүүлнэ. Хуулбарын заагт ойртвол ижил байрлал руу үсэрнэ. */
  const nudge = (direction: 1 | -1) => {
    const scroller = scrollerRef.current;
    const group = groupRef.current;
    if (!scroller || !group) return;
    const card = (group.firstElementChild as HTMLElement | null)?.offsetWidth ?? 320;
    const reduced = reducedMotion();
    if (!reduced) {
      const loop = group.offsetWidth;
      if (direction < 0 && scroller.scrollLeft < card) scroller.scrollLeft += loop;
      if (direction > 0 && scroller.scrollLeft > loop) scroller.scrollLeft -= loop;
    }
    hold(RESUME_AFTER_NUDGE_MS);
    scroller.scrollBy({ left: direction * (card + GAP_PX), behavior: reduced ? "auto" : "smooth" });
  };

  return (
    <div className="relative isolate">
      {/* Захын шар гэрэл — картууд гэрлээс уусаж гарч ирээд, гэрэл рүү уусаж орно. */}
      <span
        aria-hidden
        className="bg-primary/20 pointer-events-none absolute inset-y-10 left-0 -z-10 w-24 rounded-full blur-3xl sm:w-40"
      />
      <span
        aria-hidden
        className="bg-primary/20 pointer-events-none absolute inset-y-10 right-0 -z-10 w-24 rounded-full blur-3xl sm:w-40"
      />
      <div
        ref={scrollerRef}
        onPointerEnter={(event) => event.pointerType === "mouse" && hold()}
        onPointerLeave={(event) => event.pointerType === "mouse" && hold(0)}
        onPointerDown={(event) => event.pointerType !== "mouse" && hold()}
        onPointerUp={(event) => event.pointerType !== "mouse" && hold(RESUME_AFTER_TOUCH_MS)}
        onPointerCancel={() => hold(RESUME_AFTER_TOUCH_MS)}
        onFocus={() => hold()}
        onBlur={(event) => {
          if (!event.currentTarget.contains(event.relatedTarget as Node | null)) hold(0);
        }}
        // «Онцлох сургалтууд» гарчгийн өргөнд; хоёр зах нь уусч бүдгэрнэ.
        className="-my-8 [scrollbar-width:none] overflow-x-auto [mask-image:linear-gradient(to_right,transparent,#000_14%,#000_86%,transparent)] py-8 [&::-webkit-scrollbar]:hidden"
      >
        <div className="flex w-max">
          <div ref={groupRef} className="flex gap-6 pr-6">
            {courses.map((course) => (
              <Slide key={course.id} course={course} />
            ))}
          </div>
          {/* Тасралтгүй урсгалын хуулбар — зөвхөн нүдэнд. */}
          <div aria-hidden inert className="flex gap-6 pr-6 motion-reduce:hidden">
            {courses.map((course) => (
              <Slide key={course.id} course={course} />
            ))}
          </div>
        </div>
      </div>

      <div className="mt-6 flex items-center justify-end gap-2">
        <Button
          variant="outline"
          size="icon"
          aria-label={mn.home.marqueePrev}
          onClick={() => nudge(-1)}
        >
          <ChevronLeftIcon aria-hidden />
        </Button>
        <Button
          variant="outline"
          size="icon"
          aria-label={mn.home.marqueeNext}
          onClick={() => nudge(1)}
        >
          <ChevronRightIcon aria-hidden />
        </Button>
        {/* Нэр нь төлвөө хэлнэ («зогсоох» / «үргэлжлүүлэх») — aria-pressed хэрэггүй. */}
        <Button
          variant="outline"
          onClick={() => setPaused((value) => !value)}
          className="motion-reduce:hidden"
        >
          {paused ? <PlayIcon aria-hidden /> : <PauseIcon aria-hidden />}
          {paused ? mn.home.marqueePlay : mn.home.marqueePause}
        </Button>
      </div>
    </div>
  );
}

/**
 * `marquee-slide` (`globals.css`): гүйлгэлтээр удирдагдах хөдөлгөөн — захад
 * саарал, 3D-ээр эргэсэн; голд ирэхэд өнгө нь уусаж орж шулуудна.
 */
function Slide({ course }: { course: CourseSummary }) {
  return (
    <div className="marquee-slide w-[18.5rem] shrink-0 sm:w-[21rem]">
      <CourseCard course={course} className="h-full" />
    </div>
  );
}
