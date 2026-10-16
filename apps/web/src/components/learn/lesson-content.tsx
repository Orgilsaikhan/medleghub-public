"use client";

import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";

import { QuizBlock } from "@/components/learn/quiz-block";
import { parseQuiz } from "@/lib/quiz";

/** ```quiz блокийн текст — `pre > code.language-quiz`. */
function quizSource(node: unknown): string | null {
  const code = (node as { children?: unknown[] } | undefined)?.children?.[0] as
    | { tagName?: string; properties?: { className?: unknown }; children?: { value?: string }[] }
    | undefined;
  const classes = code?.properties?.className;
  if (code?.tagName !== "code" || !Array.isArray(classes) || !classes.includes("language-quiz")) {
    return null;
  }
  return (code.children ?? []).map((child) => child.value ?? "").join("");
}

/**
 * Хичээлийн Markdown агуулга.
 *
 * `react-markdown` нь HTML-ийг шууд оруулдаггүй (rehype-raw нэмээгүй) тул
 * контент доторх `<script>` зэрэг таг нь энгийн текст болж харагдана — админ
 * бичсэн ч гэсэн XSS үүсэхгүй.
 *
 * ```quiz блок нь «Шалгах асуулт» болж харагдана (`lib/quiz.ts`).
 */
export function LessonContent({ content }: { content: string }) {
  if (!content.trim()) return null;

  return (
    <div className="lesson-prose">
      <Markdown
        remarkPlugins={[remarkGfm]}
        components={{
          a: ({ href, children }) => (
            <a href={href} target="_blank" rel="noopener noreferrer nofollow">
              {children}
            </a>
          ),
          pre: ({ node, children, ...props }) => {
            const source = quizSource(node);
            const quiz = source === null ? null : parseQuiz(source);
            if (quiz) return <QuizBlock quiz={quiz} />;
            // Урт мөр хэвтээгээр гүйлгэгдэнэ (шинэ байрлалын нарийн «Заавар»
            // хэсэгт ялангуяа) — гарын түлхүүрээр ч хүрнэ (WCAG 2.1.1).
            return (
              <pre tabIndex={0} {...props}>
                {children}
              </pre>
            );
          },
          // Хүснэгт нарийн дэлгэц дээр хуудсыг хэвтээгээр сунгахгүй.
          table: ({ children }) => (
            <div className="overflow-x-auto">
              <table>{children}</table>
            </div>
          ),
        }}
      >
        {content}
      </Markdown>
    </div>
  );
}
