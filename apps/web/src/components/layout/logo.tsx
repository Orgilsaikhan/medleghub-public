import Image from "next/image";
import Link from "next/link";

import { mn } from "@/lib/i18n/mn";
import { cn } from "@/lib/utils";

/**
 * Брэндийн үг тэмдэг (`public/main_logo.png`).
 *
 * Зураг нь ТУНГАЛАГ БИШ — дэвсгэр нь хар өнгөтэй. Тиймээс түүнийг өөрийг
 * нь хүрээлж дугуйруулна: хар дэвсгэр нь гэнэтийн дөрвөлжин биш, зориудын
 * хэсэг мэт харагдана. Гэрэл ба харанхуй горим хоёуланд нь ижил ажиллана.
 *
 * Тунгалаг хувилбар гарвал `rounded-md bg-black` хэсгийг хасаж болно.
 */
const LOGO_SRC = "/main_logo.png";
const LOGO_WIDTH = 370;
const LOGO_HEIGHT = 130;

export function LogoMark({ className }: { className?: string }) {
  return (
    <Image
      src={LOGO_SRC}
      alt={mn.brand.name}
      width={LOGO_WIDTH}
      height={LOGO_HEIGHT}
      priority
      className={cn("h-8 w-auto rounded-md bg-black", className)}
    />
  );
}

export function Logo({ className }: { className?: string }) {
  return (
    <Link
      href="/"
      aria-label={mn.brand.name}
      className={cn(
        "group/logo flex shrink-0 items-center rounded-md",
        "focus-visible:ring-ring focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:outline-none",
        className,
      )}
    >
      {/* Хулгана аваачихад бага зэрэг томорч, шар гэрэл тусна. */}
      <LogoMark className="transition-[translate,scale,rotate,box-shadow] duration-300 ease-out group-hover/logo:scale-[1.04] group-hover/logo:shadow-[0_0_18px_-4px_var(--primary)] group-active/logo:scale-[0.98] motion-reduce:transition-none motion-reduce:group-hover/logo:scale-100" />
    </Link>
  );
}
