"use client";

import { useEffect, useState } from "react";

/** Одоогийн цаг (мс), `active` үед секунд тутам шинэчлэгдэнэ — тоолуурт. */
export function useNow(active: boolean): number {
  const [now, setNow] = useState(() => Date.now());
  useEffect(() => {
    if (!active) return;
    const tick = () => setNow(Date.now());
    // Идэвхжсэн даруйд нэг шинэчилнэ — эс бөгөөс эхний секундэд хуучин цаг харагдана.
    const first = window.setTimeout(tick, 0);
    const id = window.setInterval(tick, 1000);
    return () => {
      window.clearTimeout(first);
      window.clearInterval(id);
    };
  }, [active]);
  return now;
}
