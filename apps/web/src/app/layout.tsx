import type { Metadata, Viewport } from "next";
import { Inter, JetBrains_Mono } from "next/font/google";

import { ChatWidget } from "@/components/layout/chat-widget";
import { Toaster } from "@/components/ui/sonner";
import { mn } from "@/lib/i18n/mn";
import { OG_IMAGE, SITE_NAME, SITE_URL } from "@/lib/seo";

import { Providers } from "./providers";
import "./globals.css";

// Монгол кирилл үсэг зөв харагдахын тулд cyrillic subset заавал шаардлагатай.
const sans = Inter({
  variable: "--font-sans",
  subsets: ["latin", "cyrillic"],
  display: "swap",
});

const mono = JetBrains_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin", "cyrillic"],
  display: "swap",
});

/**
 * Анхдагч metadata. Хуудас бүр `pageMetadata()`-аар (`src/lib/seo.ts`) өөрийн
 * гарчиг, canonical, Open Graph-ийг тавина. Canonical-ыг ЭНД бүү тавь — өөрийн
 * canonical-гүй хуудас бүр нүүр хуудас руу заах болно.
 */
export const metadata: Metadata = {
  // Үргэлж production домэйн — орчны хувьсагчид (хуучин Vercel хаяг) найдахгүй.
  metadataBase: new URL(SITE_URL),
  title: {
    default: mn.seo.homeTitle,
    template: `%s | ${SITE_NAME}`,
  },
  description: mn.seo.homeDescription,
  applicationName: SITE_NAME,
  openGraph: {
    type: "website",
    locale: "mn_MN",
    siteName: SITE_NAME,
    title: mn.seo.homeTitle,
    description: mn.seo.homeDescription,
    images: [OG_IMAGE],
  },
  twitter: {
    card: "summary_large_image",
    title: mn.seo.homeTitle,
    description: mn.seo.homeDescription,
    images: [OG_IMAGE],
  },
};

export const viewport: Viewport = {
  themeColor: [
    { media: "(prefers-color-scheme: light)", color: "#fafafa" },
    { media: "(prefers-color-scheme: dark)", color: "#0b0b0b" },
  ],
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html
      lang="mn"
      suppressHydrationWarning
      className={`${sans.variable} ${mono.variable} h-full antialiased`}
    >
      <body className="flex min-h-full flex-col">
        <Providers>
          {children}
          <Toaster position="top-center" richColors />
        </Providers>
        <ChatWidget />
      </body>
    </html>
  );
}
