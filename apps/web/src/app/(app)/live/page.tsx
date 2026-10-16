import type { Metadata } from "next";

import { LiveBackdrop, LiveHero } from "@/components/live/live-hero";
import { LiveEntry } from "@/components/live/live-home";
import { mn } from "@/lib/i18n/mn";

export const metadata: Metadata = {
  title: mn.live.title,
};

export default function LivePage() {
  return (
    // Толгойн дэвсгэр, тойрог замууд хуудасны бүтэн өргөнөөр — `overflow-clip`
    // нь хайчилж, хэвтээ гүйлгээ (гүйлгэх хүрээ ч) үүсгэхгүй.
    <div className="relative isolate overflow-clip">
      <LiveBackdrop />
      <div className="container-page py-10 lg:py-14">
        <div className="mx-auto max-w-6xl">
          <LiveHero />
          <div className="mt-10">
            {/* Нэвтрээгүй зочин ч багц, нэг удаагийн эрхийн саналыг харна. */}
            <LiveEntry />
          </div>
        </div>
      </div>
    </div>
  );
}
