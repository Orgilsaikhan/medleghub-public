import type { ReactNode } from "react";
import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";

import { cn } from "@/lib/utils";

function Heading({ children }: { children?: ReactNode }) {
  return <p className="text-foreground font-semibold">{children}</p>;
}

/**
 * Хэрэглэгчийн бичсэн Markdown (Community нийтлэл, сэтгэгдэл).
 *
 * - HTML нь текст болно (`skipHtml`, rehype-raw байхгүй); `javascript:`
 *   холбоосыг react-markdown өөрөө хасна.
 * - Зураг харуулахгүй: хавсралт оруулахгүй, мөн гадны зураг уншигчийн IP-г
 *   өөр сайтад задруулна.
 * - Гарчиг нь хуудасны гарчгийн бүтцийг эвдэхгүйн тулд тод мөр болно.
 */
export function CommunityMarkdown({ source, className }: { source: string; className?: string }) {
  return (
    <div className={cn("lesson-prose break-words", className)}>
      <Markdown
        remarkPlugins={[remarkGfm]}
        skipHtml
        disallowedElements={["img"]}
        components={{
          h1: Heading,
          h2: Heading,
          h3: Heading,
          h4: Heading,
          h5: Heading,
          h6: Heading,
          a: ({ href, children }) => (
            <a href={href} target="_blank" rel="noopener noreferrer nofollow ugc">
              {children}
            </a>
          ),
          // Урт мөр хэвтээ гүйлгэгдэнэ — гараар ч гүйлгэх боломжтой байх ёстой.
          pre: ({ children }) => <pre tabIndex={0}>{children}</pre>,
          table: ({ children }) => (
            <div className="overflow-x-auto">
              <table>{children}</table>
            </div>
          ),
        }}
      >
        {source}
      </Markdown>
    </div>
  );
}
