"use client";

import { useId } from "react";

import { useMediaQuery } from "@/lib/hooks/use-media-query";
import { cn } from "@/lib/utils";

// Бүх хэмжээ 24×24 viewBox дотор. Гараг ба түүний цагираг (эргүүлэхээс өмнөх
// координатаар), баруун дээд буланд AI-ийн од.
const CX = 11;
const CY = 13;
const PLANET_R = 6;
const RX = 10.4;
const RY = 2.2;
const TILT = -15;
const LEFT = `${CX - RX} ${CY}`;
const RIGHT = `${CX + RX} ${CY}`;
/** Цагирагийн ар тал — гарагийн ард нуугдана. */
const BACK_ARC = `M${LEFT} A${RX} ${RY} 0 0 1 ${RIGHT}`;
/** Урд тал — гарагийн өмнүүр гарна. */
const FRONT_ARC = `M${LEFT} A${RX} ${RY} 0 0 0 ${RIGHT}`;
/** Цэгийн зам: урдуур нь зүүнээс баруун тийш, араар нь буцна. */
const ORBIT = `${FRONT_ARC} A${RX} ${RY} 0 0 0 ${LEFT}`;
/** AI-ийн дөрвөн салаа од. */
const SPARKLE =
  "M19.6 1.1Q20.52 3.48 22.9 4.4Q20.52 5.32 19.6 7.7Q18.68 5.32 16.3 4.4Q18.68 3.48 19.6 1.1Z";
const ORBIT_SECONDS = 6;

/**
 * MedlegHub Live-ийн тэмдэг: хазгай цагирагтай гараг ба AI-ийн од. Цагирагийн
 * ар тал гарагийн ард нуугдаж, урд тал нь өмнүүр нь гарна. `animated` бол
 * цагирагаар жижиг сар эргэнэ — араар явахдаа гарагийн ард орно. Хөдөлгөөн
 * багасгах тохиргоотой бол сар зогсоно.
 *
 * Өнгө нь `currentColor`. Чимэглэл (`aria-hidden`) — утгыг хажуугийн бичвэр
 * хэлнэ.
 */
export function LiveMark({
  animated = false,
  className,
}: {
  animated?: boolean;
  className?: string;
}) {
  // SVG mask, clipPath-ийн id хуудсанд давтагдахгүй байх ёстой.
  const id = useId().replace(/[^a-zA-Z0-9_-]/g, "");
  const motion = useMediaQuery("(prefers-reduced-motion: no-preference)");
  const orbiting = animated && motion;

  // Сар хоёр удаа зурагдана: нэг нь гарагийн ард, нөгөө нь зөвхөн урд талд.
  const moon = orbiting ? (
    <circle r="1.45" fill="currentColor" stroke="none">
      <animateMotion dur={`${ORBIT_SECONDS}s`} repeatCount="indefinite" path={ORBIT} />
    </circle>
  ) : (
    // Зогсонги үед урд талын баруун хэсэгт.
    <circle cx="18.97" cy="14.41" r="1.45" fill="currentColor" stroke="none" />
  );

  return (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth={1.75}
      strokeLinecap="round"
      aria-hidden
      className={cn("size-6 shrink-0", className)}
    >
      <defs>
        {/* Гарагаас: урд талын цагирагийн дагуу зай гаргана — цагираг өмнүүр харагдана. */}
        <mask id={`${id}-planet`} maskUnits="userSpaceOnUse" x="-4" y="-4" width="32" height="32">
          <rect x="-4" y="-4" width="32" height="32" fill="white" />
          <path
            d={FRONT_ARC}
            transform={`rotate(${TILT} ${CX} ${CY})`}
            fill="none"
            stroke="black"
            strokeWidth={3.2}
          />
        </mask>
        {/* Ар талаас: гарагийн эргэн тойронд зай — цагираг ард нь орсон мэт. */}
        <mask id={`${id}-back`} maskUnits="userSpaceOnUse" x="-4" y="-4" width="32" height="32">
          <rect x="-4" y="-4" width="32" height="32" fill="white" />
          <circle cx={CX} cy={CY} r={PLANET_R + 1.3} fill="black" />
        </mask>
        {/* Урд талын хагас (эргүүлсэн координатаар доод тал). */}
        <clipPath id={`${id}-front`}>
          <rect x="-8" y={CY} width="40" height="20" />
        </clipPath>
      </defs>

      <g transform={`rotate(${TILT} ${CX} ${CY})`}>
        <g mask={`url(#${id}-back)`}>
          <path d={BACK_ARC} opacity={0.9} />
          {moon}
        </g>
      </g>

      <circle
        cx={CX}
        cy={CY}
        r={PLANET_R}
        fill="currentColor"
        stroke="none"
        mask={`url(#${id}-planet)`}
      />

      <g transform={`rotate(${TILT} ${CX} ${CY})`}>
        <path d={FRONT_ARC} />
        <g clipPath={`url(#${id}-front)`}>{moon}</g>
      </g>

      <path d={SPARKLE} fill="currentColor" stroke="none" />
    </svg>
  );
}
