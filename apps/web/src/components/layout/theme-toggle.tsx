"use client";

import { MoonIcon, SunIcon } from "lucide-react";
import { useTheme } from "next-themes";

import { Button } from "@/components/ui/button";
import { mn } from "@/lib/i18n/mn";

/**
 * Гэрэл/харанхуй солих товч.
 *
 * Хоёр дүрсийг хоёуланг нь render хийж, CSS-ээр нэгийг нь нуудаг — сервер дээр
 * идэвхтэй загварыг мэдэх шаардлагагүй тул hydration зөрчил үүсэхгүй.
 */
export function ThemeToggle() {
  const { resolvedTheme, setTheme } = useTheme();

  return (
    <Button
      variant="ghost"
      size="icon"
      aria-label={mn.nav.theme}
      title={mn.nav.theme}
      onClick={() => setTheme(resolvedTheme === "dark" ? "light" : "dark")}
    >
      <MoonIcon className="size-4 dark:hidden" aria-hidden />
      <SunIcon className="hidden size-4 dark:block" aria-hidden />
    </Button>
  );
}
