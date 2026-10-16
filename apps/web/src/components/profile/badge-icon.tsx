import Image from "next/image";

import { BADGE_FILES } from "@/lib/badge-manifest";
import type { BadgeShape, BadgeStatus } from "@/lib/types/api";
import { cn } from "@/lib/utils";

/** Солонгон гэрэл — ягаан → нил → цэнхэр → ногоон → шар → улбар. */
const PRISMATIC = "bg-[conic-gradient(#f9a8d4,#c4b5fd,#93c5fd,#6ee7b7,#fde68a,#fdba74,#f9a8d4)]";

/** 64×64 талбайд тэмдгийн хэлбэр. */
const SHAPES: Record<BadgeShape, React.ReactNode> = {
  circle: <circle cx="32" cy="32" r="27" />,
  shield: <path d="M32 5 54 13v17c0 13.5-9.3 24.3-22 29-12.7-4.7-22-15.5-22-29V13Z" />,
  hexagon: <path d="M32 4 56.2 18v28L32 60 7.8 46V18Z" />,
};

interface BadgeIconProps {
  badge: Pick<BadgeStatus, "key" | "shape" | "earned" | "rare" | "secret" | "prismatic">;
  /** `sm` — нэрийн хажуугийн жижиг дүрс: жижиг булан, нарийн хүрээ, бага гэрэл. */
  size?: "default" | "sm";
  className?: string;
}

/**
 * Тэмдгийн дүрс.
 *
 * `BADGE_FILES` нь `public/badges/` доторх файлуудаас build хийх үед
 * автоматаар үүснэ (`scripts/generate-badge-manifest.mjs`). Файлаа
 * `<түлхүүр>.svg` нэрээр хийхэд л хангалттай — код засах шаардлагагүй.
 *
 * Файлгүй тэмдэг хоосон хэлбэрээрээ харагдана: авсан бол өнгөтэй, аваагүй
 * бол тасархай хүрээтэй. Аваагүй тэмдгийн жинхэнэ дүрс саарал өнгөтэй.
 *
 * Дүрсүүд бараан дэвсгэртэй дөрвөлжин зураг тул булан нь бөөрөнхий хавтан
 * болж харагдана — гэрэл, харанхуй горимд хоёуланд нь зохицно.
 *
 * ХОВОР АМЖИЛТ
 * ────────────
 * Дүрсний АРД тусдаа бүдгэрсэн алтан давхарга гэрэлтэнэ. `filter`-ээр биш —
 * аваагүй дүрсний `grayscale`-тай зөрчилдөхгүй, дурын хэлбэрт тохирно. Авсан
 * бол алтан хүрээтэй, гэрэл нь аажуухан «амьсгална» (хөдөлгөөн багасгах
 * тохиргоотой хэрэглэгчид хөдөлгөөнгүй). Аваагүй бол бүдэг, хөдөлгөөнгүй —
 * ховор гэдгийг нь л мэдэгдэнэ.
 *
 * Солонгон (`prismatic`) тэмдэг алтны оронд солонгон өнгөөр гэрэлтэнэ.
 *
 * НУУЦ АМЖИЛТ
 * ───────────
 * Авах хүртэл жинхэнэ дүрсийн оронд «?» — нөхцөл шиг дүрс нь ч нууц.
 */
export function BadgeIcon({ badge, size = "default", className }: BadgeIconProps) {
  const file = BADGE_FILES[badge.key];
  const glowing = badge.rare && badge.earned;
  const small = size === "sm";

  const hidden = badge.secret && !badge.earned;

  const icon = hidden ? (
    <span
      data-secret
      className={cn(
        "border-muted-foreground/40 bg-muted/60 text-muted-foreground relative grid size-full place-items-center border-dashed font-bold",
        small ? "rounded-md border text-xs" : "rounded-2xl border-2 text-4xl",
      )}
    >
      ?
    </span>
  ) : file ? (
    <Image
      src={file}
      alt=""
      aria-hidden
      width={small ? 64 : 128}
      height={small ? 64 : 128}
      className={cn(
        "relative size-full object-cover shadow-sm",
        small ? "rounded-md" : "rounded-2xl",
        !badge.earned && "opacity-40 grayscale",
        glowing && (small ? "ring-1" : "ring-2"),
        glowing && (badge.prismatic ? "ring-violet-300/80" : "ring-amber-400/80"),
      )}
      unoptimized={file.endsWith(".svg")}
    />
  ) : (
    <svg
      viewBox="0 0 64 64"
      aria-hidden
      data-placeholder
      className="relative size-full"
      xmlns="http://www.w3.org/2000/svg"
    >
      <g
        strokeWidth={2}
        strokeLinejoin="round"
        className={
          glowing
            ? "fill-amber-400/20 stroke-amber-500"
            : badge.earned
              ? "fill-primary/15 stroke-primary"
              : "stroke-muted-foreground/40 fill-none [stroke-dasharray:4_4]"
        }
      >
        {SHAPES[badge.shape]}
      </g>
    </svg>
  );

  return (
    <span
      className={cn("relative isolate inline-grid shrink-0 place-items-center", className)}
      data-rare={badge.rare || undefined}
    >
      {badge.rare && (
        <span
          aria-hidden
          className={cn(
            "absolute -z-10 rounded-full",
            small ? "-inset-1 blur-md" : "-inset-2 blur-xl",
            badge.prismatic ? PRISMATIC : "bg-amber-400",
            glowing ? "motion-safe:animate-badge-glow opacity-60" : "opacity-15",
          )}
        />
      )}
      {icon}
    </span>
  );
}
