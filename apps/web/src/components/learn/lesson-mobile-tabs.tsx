"use client";

import { useState, type ReactNode } from "react";

import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { mn } from "@/lib/i18n/mn";

interface LessonMobileTabsProps {
  reading: ReactNode;
  playground: ReactNode;
  codeLabel?: string;
}

/**
 * Нарийн дэлгэц дээр унших/кодын хэсгийг «Унших / Код» tab-аар сольж харуулна.
 *
 * `forceMount` ашигласнаар идэвхгүй tab-ийн агуулгыг DOM-оос устгахгүй,
 * зөвхөн CSS-ээр нуудаг (`data-[state=inactive]:hidden`) — CodePlayground
 * (бичсэн код, stdin, console) tab солиход дахин mount болохгүй, төлөв
 * алдагдахгүй.
 */
export function LessonMobileTabs({ reading, playground, codeLabel }: LessonMobileTabsProps) {
  const [tab, setTab] = useState<"read" | "code">("read");

  return (
    <Tabs
      value={tab}
      onValueChange={(value) => setTab(value as "read" | "code")}
      className="flex min-h-0 flex-1 flex-col gap-0"
    >
      <TabsList className="mx-3 mt-2 shrink-0 self-start">
        <TabsTrigger value="read">{mn.learn.tabRead}</TabsTrigger>
        <TabsTrigger value="code">{codeLabel ?? mn.learn.tabCode}</TabsTrigger>
      </TabsList>

      <TabsContent value="read" forceMount className="min-h-0 flex-1 data-[state=inactive]:hidden">
        {reading}
      </TabsContent>

      <TabsContent
        value="code"
        forceMount
        className="flex min-h-0 flex-1 flex-col data-[state=inactive]:hidden"
      >
        {playground}
      </TabsContent>
    </Tabs>
  );
}
