import type { Metadata } from "next";

import { FootprintsView } from "@/components/footprints/footprints-view";
import { mn } from "@/lib/i18n/mn";

export const metadata: Metadata = {
  title: mn.footprints.title,
  // Нууц хуудас — хайлтын системд орохгүй.
  robots: { index: false, follow: false },
};

export default function FootprintsPage() {
  return <FootprintsView />;
}
