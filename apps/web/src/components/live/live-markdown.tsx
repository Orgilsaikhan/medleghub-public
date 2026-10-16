import type { ReactNode } from "react";
import Markdown, { type Components } from "react-markdown";
import remarkGfm from "remark-gfm";

import { cn } from "@/lib/utils";

type HeadingTag = "h2" | "h3" | "h4";

/**
 * Markdown-ийн гарчгийн түвшинг (`#` = 1) хуудасны `h2`–`h4` болгоно. `top` —
 * эх бичвэрийн хамгийн дээд түвшин: AI ихэвчлэн `##`-аас эхэлдэг тул тэр нь `h2`
 * болно, `h1` → `h3` гэж шат алгасахгүй.
 */
function headings(top: number): Components {
  const make = (depth: number) => {
    const Tag = `h${Math.min(4, Math.max(2, depth - top + 2))}` as HeadingTag;
    return function Heading({ children }: { children?: ReactNode }) {
      return <Tag>{children}</Tag>;
    };
  };
  return { h1: make(1), h2: make(2), h3: make(3), h4: make(4), h5: make(5), h6: make(6) };
}

/** Хамгийн дээд түвшний гарчиг. Кодын блок доторх `#` (Python-ы тайлбар) тооцохгүй. */
function topHeadingDepth(source: string): number {
  let fenced = false;
  let top = 6;
  for (const line of source.split("\n")) {
    if (/^\s*(```|~~~)/.test(line)) {
      fenced = !fenced;
      continue;
    }
    const match = fenced ? null : /^ {0,3}(#{1,6})\s/.exec(line);
    if (match) top = Math.min(top, match[1].length);
  }
  return top;
}

/**
 * AI-ийн бичсэн Markdown (заавар, хариултын санаа, тайлбар).
 *
 * `CommunityMarkdown`-тай ижил хамгаалалттай: HTML нь текст болно (`skipHtml`),
 * зураг харуулахгүй (гадны зураг уншигчийн IP-г өөр сайтад задруулна),
 * холбоос шинэ цонхонд, `nofollow`-той. Ялгаа нь гарчиг: хуудас өөрийн `h1`-тэй
 * тул гарчгууд жинхэнэ `h2`/`h3`/`h4` болно (`headings`).
 */
const COMPONENTS: Components = {
  a: ({ href, children }) => (
    <a href={href} target="_blank" rel="noopener noreferrer nofollow">
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
};

/** Эх бичвэрийн дээд түвшин тус бүрт (1–6) нэг л удаа үүсгэнэ. */
const COMPONENTS_BY_TOP = [1, 2, 3, 4, 5, 6].map((top) => ({ ...COMPONENTS, ...headings(top) }));

export function LiveMarkdown({ source, className }: { source: string; className?: string }) {
  return (
    <div className={cn("lesson-prose break-words", className)}>
      <Markdown
        remarkPlugins={[remarkGfm]}
        skipHtml
        disallowedElements={["img"]}
        components={COMPONENTS_BY_TOP[topHeadingDepth(source) - 1]}
      >
        {source}
      </Markdown>
    </div>
  );
}

/**
 * Мөр доторх Markdown — тестийн асуулт, сонголт (`код`, **тод**). Догол мөр
 * үүсгэхгүй тул товч, шошго дотор ч тавьж болно.
 */
export function LiveInlineMarkdown({ text }: { text: string }) {
  return (
    <Markdown
      remarkPlugins={[remarkGfm]}
      skipHtml
      disallowedElements={["img"]}
      components={{
        ...COMPONENTS_BY_TOP[0],
        p: ({ children }: { children?: ReactNode }) => <>{children}</>,
        code: ({ children }) => (
          <code className="bg-muted rounded px-1 py-0.5 font-mono text-[0.9em]">{children}</code>
        ),
      }}
    >
      {text}
    </Markdown>
  );
}
