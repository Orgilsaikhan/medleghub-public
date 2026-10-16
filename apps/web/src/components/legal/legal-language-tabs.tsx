"use client";

import { useState, type ReactNode } from "react";

import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { useIsHydrated } from "@/lib/hooks/use-hydrated";
import type { LegalLanguage } from "@/lib/legal";
import { readLocal, writeLocal } from "@/lib/local-storage";

const LANGUAGE_KEY = "medleghub:legal-language";

/** `?lang=en` холбоос эсвэл өмнө сонгосон хэл. Зөвхөн hydration-ы дараа уншина. */
function preferredLanguage(): LegalLanguage {
  const fromUrl = new URLSearchParams(window.location.search).get("lang");
  if (fromUrl === "en" || fromUrl === "mn") return fromUrl;
  return readLocal(LANGUAGE_KEY, "mn") === "en" ? "en" : "mn";
}

/**
 * Монгол / англи хувилбарын хооронд шилжүүлнэ.
 *
 * Хуудас статик тул сервер үргэлж монгол хувилбарыг render хийнэ. Англи
 * хувилбарыг `?lang=en` холбоос эсвэл хадгалсан сонголтоор hydration-ы дараа нээнэ.
 */
export function LegalLanguageTabs({ mn, en }: { mn: ReactNode; en: ReactNode }) {
  const hydrated = useIsHydrated();
  const [chosen, setChosen] = useState<LegalLanguage | null>(null);
  const language = chosen ?? (hydrated ? preferredLanguage() : "mn");

  function select(value: string) {
    const next: LegalLanguage = value === "en" ? "en" : "mn";
    setChosen(next);
    writeLocal(LANGUAGE_KEY, next);
    // Хуваалцах холбоос сонгосон хэлээ хадгална.
    const url = new URL(window.location.href);
    if (next === "en") url.searchParams.set("lang", "en");
    else url.searchParams.delete("lang");
    window.history.replaceState(null, "", url);
  }

  return (
    <Tabs value={language} onValueChange={select}>
      <div className="flex justify-end">
        <TabsList aria-label="Хэл / Language">
          <TabsTrigger value="mn">Монгол</TabsTrigger>
          <TabsTrigger value="en">English</TabsTrigger>
        </TabsList>
      </div>
      <TabsContent value="mn" lang="mn" className="mt-6">
        {mn}
      </TabsContent>
      <TabsContent value="en" lang="en" className="mt-6">
        {en}
      </TabsContent>
    </Tabs>
  );
}
