import Image from "next/image";

import { LOGO_FILES } from "@/lib/logo-manifest";
import type { Category } from "@/lib/types/api";
import { cn } from "@/lib/utils";

/**
 * Ангилал бүрийн таних тэмдэг.
 *
 * Гадны CDN-ээс зураг татахгүй — бүгд inline SVG. Ингэснээр:
 *   • сүлжээний нэмэлт хүсэлт үүсэхгүй, CSP-д зөвшөөрөл нэмэх шаардлагагүй,
 *   • ямар ч хэмжээнд тод харагдана,
 *   • гэрэл/харанхуй горимд өнгийг нь тохируулж болно.
 *
 * ХУУЛЬ ЗҮЙН ТАЛ: эдгээр нь тухайн хэлийг ЗААХ зорилгоор ашиглаж буй
 * төлөөллийн дүрслэл бөгөөд албан ёсны лого файлыг хуулбарлаагүй. Брэндийн
 * өнгийг таних байдлыг хангахын тулд ашигласан. Хэрэв Oracle (Java),
 * Microsoft (C#) зэрэг эзэмшигчийн удирдамж шаардвал энэ файлыг солиход
 * бусад кодод өөрчлөлт орохгүй.
 */

interface LogoProps {
  category: Category;
  className?: string;
}

/**
 * Тэмдэгт суурьтай лого — C, C# зэрэгт.
 *
 * `fillClass` нь харанхуй горимд илүү тод өнгө өгнө: брэндийн гүн өнгө нь
 * бараан дэвсгэр дээр ялгарахгүй байдаг.
 */
function LetterMark({
  label,
  fillClass,
  color,
  fontSize = 9,
}: {
  label: string;
  fillClass: string;
  color: string;
  fontSize?: number;
}) {
  return (
    <>
      <rect x="1.5" y="1.5" width="21" height="21" rx="4.5" className={fillClass} />
      <text
        x="12"
        y="12"
        textAnchor="middle"
        dominantBaseline="central"
        fontSize={fontSize}
        fontWeight="700"
        fontFamily="var(--font-geist-mono), ui-monospace, monospace"
        fill={color}
      >
        {label}
      </text>
    </>
  );
}

const JAVASCRIPT = (
  <>
    <rect x="1.5" y="1.5" width="21" height="21" rx="4.5" fill="#F7DF1E" />
    <text
      x="21"
      y="20"
      textAnchor="end"
      fontSize="10"
      fontWeight="700"
      fontFamily="var(--font-geist-mono), ui-monospace, monospace"
      fill="#0B0B0B"
    >
      JS
    </text>
  </>
);

/** Хоёр сүлжсэн хэлбэр — Python-ийг танихуйц болгоно. */
const PYTHON = (
  <>
    <path
      d="M11.6 2h1.2c2.4 0 4.1 1.1 4.1 3.3v3.4c0 2-1.5 3.4-3.5 3.4h-3.3c-2 0-3.6 1.6-3.6 3.6v1.8H4.8C2.8 17.5 2 15.3 2 12.5S2.8 7.6 4.8 7.6h7.3V6.8H7.5V5.3C7.5 3.1 9.2 2 11.6 2Z"
      fill="#3776AB"
    />
    <circle cx="9.6" cy="4.9" r="1.05" fill="#fff" />
    <path
      d="M12.4 22h-1.2c-2.4 0-4.1-1.1-4.1-3.3v-3.4c0-2 1.5-3.4 3.5-3.4h3.3c2 0 3.6-1.6 3.6-3.6V6.5h1.7c2 0 2.8 2.2 2.8 5s-.8 4.9-2.8 4.9h-7.3v.8h4.6v1.5c0 2.2-1.7 3.3-4.1 3.3Z"
      fill="#FFD43B"
    />
    <circle cx="14.4" cy="19.1" r="1.05" fill="#fff" />
  </>
);

/** Атомын тойрог — React-ийн таних дүрс. */
const REACT_MARK = (
  <>
    <circle cx="12" cy="12" r="2" fill="#61DAFB" />
    <g stroke="#61DAFB" strokeWidth="1.1" fill="none">
      <ellipse cx="12" cy="12" rx="10" ry="4" />
      <ellipse cx="12" cy="12" rx="10" ry="4" transform="rotate(60 12 12)" />
      <ellipse cx="12" cy="12" rx="10" ry="4" transform="rotate(120 12 12)" />
    </g>
  </>
);

/** Уурлаж буй аяга — Java-г танихуйц болгоно. */
const JAVA = (
  <>
    <g stroke="#E76F00" strokeWidth="1.3" strokeLinecap="round" fill="none">
      <path d="M11 2.5c-1.6 1.4 1.4 2.4 0 3.9" />
      <path d="M14.2 4.2c-1.2 1 1 1.8 0 2.9" />
    </g>
    <path d="M6.5 9h10v5.2c0 1.9-1.6 3.3-3.6 3.3h-2.8c-2 0-3.6-1.4-3.6-3.3V9Z" fill="#5382A1" />
    <path
      d="M16.8 10.2h1.1c1.2 0 2.1.9 2.1 2s-.9 2-2.1 2h-1.1"
      stroke="#5382A1"
      strokeWidth="1.4"
      fill="none"
      strokeLinecap="round"
    />
    <rect x="4.5" y="19" width="15" height="2.2" rx="1.1" fill="#E76F00" />
  </>
);

/** Сервер тавиур — backend. */
const BACKEND = (
  <>
    <g fill="#059669">
      <rect x="3" y="4" width="18" height="4.6" rx="1.6" />
      <rect x="3" y="9.7" width="18" height="4.6" rx="1.6" />
      <rect x="3" y="15.4" width="18" height="4.6" rx="1.6" />
    </g>
    <g fill="#fff">
      <circle cx="6.4" cy="6.3" r="0.95" />
      <circle cx="6.4" cy="12" r="0.95" />
      <circle cx="6.4" cy="17.7" r="0.95" />
    </g>
  </>
);

/** Цилиндр — өгөгдлийн сан. */
const DATABASE = (
  <>
    <ellipse cx="12" cy="5.6" rx="8.2" ry="3.1" fill="#4F46E5" />
    <path d="M3.8 5.6v12.8c0 1.7 3.7 3.1 8.2 3.1s8.2-1.4 8.2-3.1V5.6Z" fill="#4F46E5" />
    <g stroke="#fff" strokeWidth="1.1" fill="none" opacity="0.65">
      <path d="M3.8 10.4c0 1.7 3.7 3.1 8.2 3.1s8.2-1.4 8.2-3.1" />
      <path d="M3.8 15c0 1.7 3.7 3.1 8.2 3.1s8.2-1.4 8.2-3.1" />
    </g>
  </>
);

/** Салаалсан түүх — Git. */
const GIT = (
  <>
    <g stroke="#F05033" strokeWidth="1.8" fill="none" strokeLinecap="round">
      <path d="M7 20V6" />
      <path d="M7 11.5c0-2.2 1.6-3.5 3.8-3.5H17" />
    </g>
    <g fill="#F05033">
      <circle cx="7" cy="4.4" r="2.4" />
      <circle cx="7" cy="19.6" r="2.4" />
      <circle cx="17.6" cy="8" r="2.4" />
    </g>
  </>
);

/**
 * HTML ба CSS хоёрыг илэрхийлсэн хос бамбай.
 *
 * Дугаарыг гар аргаар зурсан зам биш `text`-ээр бичнэ — жижиг хэмжээнд ч
 * гажихгүй, тодорхой уншигдана. Бамбайн өргөн/өндрийн харьцаа 0.87 —
 * үүнээс нарийн болгох тугтай төстэй болж, бамбай мэт харагдахаа болино.
 */
const SHIELD_WIDTH = 9.6;
const SHIELD_HEIGHT = 11;
const SHIELD_TOP = 6.5;

function Shield({ x, fill, label }: { x: number; fill: string; label: string }) {
  const inset = SHIELD_WIDTH * 0.11;
  const shoulder = SHIELD_TOP + SHIELD_HEIGHT * 0.72;
  const centre = x + SHIELD_WIDTH / 2;

  return (
    <>
      <path
        d={
          `M${x} ${SHIELD_TOP}h${SHIELD_WIDTH}` +
          `l${-inset} ${SHIELD_HEIGHT * 0.72}` +
          `L${centre} ${SHIELD_TOP + SHIELD_HEIGHT}` +
          `L${x + inset} ${shoulder}Z`
        }
        fill={fill}
      />
      <text
        x={centre}
        y={SHIELD_TOP + SHIELD_HEIGHT * 0.42}
        textAnchor="middle"
        dominantBaseline="central"
        fontSize="6.4"
        fontWeight="700"
        fontFamily="var(--font-sans), ui-sans-serif, system-ui, sans-serif"
        fill="#fff"
      >
        {label}
      </text>
    </>
  );
}

const HTML_CSS = (
  <>
    <Shield x={1.9} fill="#E34F26" label="5" />
    <Shield x={12.5} fill="#1572B6" label="3" />
  </>
);

const LOGOS: Record<Category, React.ReactNode> = {
  javascript: JAVASCRIPT,
  python: PYTHON,
  react: REACT_MARK,
  java: JAVA,
  backend: BACKEND,
  database: DATABASE,
  git: GIT,
  flowgorithm: (
    <>
      <path
        d="M12 6v3m0 6v3M6 12H3v9h6m9-9h3v9h-6"
        fill="none"
        stroke="#0D9488"
        strokeWidth="1.5"
      />
      <rect x="7.5" y="1" width="9" height="5" rx="2.5" fill="#0D9488" />
      <path d="m12 8 6 4-6 4-6-4Z" fill="#F59E0B" />
      <rect x="8" y="18" width="8" height="5" rx="1" fill="#0D9488" />
    </>
  ),
  html_css: HTML_CSS,
  c: (
    <LetterMark
      label="C"
      fillClass="fill-[#00599C] dark:fill-[#3B8FD4]"
      color="#fff"
      fontSize={11}
    />
  ),
  csharp: <LetterMark label="C#" fillClass="fill-[#68217A] dark:fill-[#A855C7]" color="#fff" />,
};

/**
 * Албан ёсны лого файлууд.
 *
 * `LOGO_FILES` нь `public/logos/` доторх файлуудаас build хийх үед автоматаар
 * үүснэ (`scripts/generate-logo-manifest.mjs`). Файлаа `<ангилал>.svg` нэрээр
 * хийхэд л хангалттай — код засах шаардлагагүй.
 *
 * Файлтай ангилал нь доорх зурсан хувилбарыг орлоно. Файлгүй ангилал зурсан
 * хувилбараа ашигласаар байна.
 */

export function CategoryLogo({ category, className }: LogoProps) {
  const file = LOGO_FILES[category];

  if (file) {
    return (
      <Image
        src={file}
        alt=""
        aria-hidden
        width={96}
        height={96}
        className={cn("shrink-0 object-contain", className)}
        unoptimized={file.endsWith(".svg")}
      />
    );
  }

  return (
    <svg
      viewBox="0 0 24 24"
      role="img"
      aria-hidden
      className={cn("shrink-0", className)}
      xmlns="http://www.w3.org/2000/svg"
    >
      {LOGOS[category]}
    </svg>
  );
}
