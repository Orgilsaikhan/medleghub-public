import Link from "next/link";
import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";

/**
 * Хууль эрх зүйн баримт бичгийг server дээр render хийнэ.
 *
 * `skipHtml` — эх файлын `<!-- … -->` тайлбар (хуульчид зориулсан тэмдэглэл,
 * сонголтот хэсэг) вэб сайтад харагдахгүй.
 */
export function LegalMarkdown({ source }: { source: string }) {
  return (
    <div className="lesson-prose">
      <Markdown
        remarkPlugins={[remarkGfm]}
        skipHtml
        components={{
          h1: ({ children }) => (
            <h1 className="text-3xl font-bold tracking-tight text-balance sm:text-4xl">
              {children}
            </h1>
          ),
          a: ({ href = "", children }) =>
            href.startsWith("/") ? (
              <Link href={href}>{children}</Link>
            ) : (
              <a href={href}>{children}</a>
            ),
          // Хүснэгт нарийн дэлгэц дээр хуудсыг хэвтээгээр сунгахгүй.
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
