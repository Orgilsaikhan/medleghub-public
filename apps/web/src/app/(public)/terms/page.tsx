import type { Metadata } from "next";

import { LegalPage } from "@/components/legal/legal-page";
import { mn } from "@/lib/i18n/mn";
import { pageMetadata } from "@/lib/seo";

// Markdown-ийг build-ийн үед уншина (`src/lib/legal.ts`).
export const dynamic = "force-static";

// `?lang=en` нь ижил хуудсан дотор солигддог тул canonical нь нэг л URL.
export const metadata: Metadata = pageMetadata({
  title: mn.legal.terms,
  description: mn.legal.termsDescription,
  path: "/terms",
});

export default function TermsPage() {
  return <LegalPage doc="terms" />;
}
