"use client";

import { useQuery } from "@tanstack/react-query";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";

import { AnnouncementDialog } from "@/components/announcements/announcement-dialog";
import { getCurrentAnnouncements } from "@/lib/api/announcements";
import { useCurrentUser } from "@/lib/hooks/use-auth";
import { useIsHydrated } from "@/lib/hooks/use-hydrated";
import { readLocal, readSession, writeLocal, writeSession } from "@/lib/local-storage";
import { queryKeys } from "@/lib/query-keys";

/** Хаасан зарлалуудын id — дахин харуулахгүй. Хамгийн сүүлийн 50-ыг л санана. */
const SEEN_KEY = "medleghub:announcements-seen";
/** Энэ табын сесст аль зарлал гарсан — нэг сесст нэгээс илүү цонх гаргахгүй. */
const SESSION_KEY = "medleghub:announcement-shown";
const SEEN_LIMIT = 50;
/** Хуудас ачаалж дуусаад гарна — шууд гарвал хэрэглэгчийг цочроодог. */
const DELAY_MS = 1200;

/**
 * Өөрийн цонхтой (Community-ийн дүрэм, нууц тэмдэг) эсвэл төлбөрийн хуудсанд
 * зарлал гаргахгүй — хоёр цонх давхцахгүй, төлбөрт саад болохгүй. Live-ийн
 * судлах хуудсууд (карт, тест) ч — давталтын дундуур цонх гарахгүй.
 */
const HIDDEN_PATHS = ["/community", "/footprints", "/billing", "/live/materials"];

function readSeen(): string[] {
  try {
    const value: unknown = JSON.parse(readLocal(SEEN_KEY, "[]"));
    return Array.isArray(value) ? value.filter((id): id is string => typeof id === "string") : [];
  } catch {
    return [];
  }
}

function markSeen(id: string): void {
  const seen = readSeen().filter((item) => item !== id);
  writeLocal(SEEN_KEY, JSON.stringify([...seen, id].slice(-SEEN_LIMIT)));
}

/**
 * Админы зарлал (`/admin/announcements`) — хамгийн шинэ, хараахан хаагаагүй
 * нэгийг нь цонх болгон гаргана.
 *
 * - Хаасныг (эсвэл товчийг дарсныг) хөтөч санаж, дахин харуулахгүй. Сервер
 *   хэн юу харсныг хадгалахгүй.
 * - Нэг табын сесст нэг л цонх: хэд хэдэн шинэ зарлал байвал дараагийнх нь
 *   дараагийн удаа орж ирэхэд гарна.
 */
export function AnnouncementPopup() {
  const pathname = usePathname();
  const hydrated = useIsHydrated();
  const { user, isLoading } = useCurrentUser();
  const [ready, setReady] = useState(false);
  const [closed, setClosed] = useState<string | null>(null);

  const query = useQuery({
    queryKey: queryKeys.announcements.current(user?.id ?? "guest"),
    queryFn: getCurrentAnnouncements,
    enabled: hydrated && !isLoading,
    staleTime: 5 * 60_000,
  });

  useEffect(() => {
    const timer = setTimeout(() => setReady(true), DELAY_MS);
    return () => clearTimeout(timer);
  }, []);

  // Хөтчийн санах ойг зөвхөн hydration-ы дараа уншина — серверийн HTML-тэй таарна.
  const seen = hydrated ? readSeen() : [];
  const shownThisSession = hydrated ? readSession(SESSION_KEY, "") : "";
  const next = query.data?.find((item) => !seen.includes(item.id) && item.id !== closed);
  const hiddenHere = HIDDEN_PATHS.some(
    (path) => pathname === path || pathname.startsWith(`${path}/`),
  );
  const open =
    ready &&
    next !== undefined &&
    !hiddenHere &&
    (shownThisSession === "" || shownThisSession === next.id);

  useEffect(() => {
    if (open && next) writeSession(SESSION_KEY, next.id);
  }, [open, next]);

  if (!next) return null;

  return (
    <AnnouncementDialog
      announcement={next}
      open={open}
      onClose={() => {
        markSeen(next.id);
        setClosed(next.id);
      }}
    />
  );
}
