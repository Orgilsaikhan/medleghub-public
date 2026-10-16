"use client";

import { CircleCheckIcon, CircleXIcon, ListChecksIcon } from "lucide-react";
import { useId, useState } from "react";
import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";

import { Button } from "@/components/ui/button";
import { mn } from "@/lib/i18n/mn";
import type { Quiz } from "@/lib/quiz";
import { cn } from "@/lib/utils";

/** Асуулт, сонголтын текст — мөр доторх Markdown (`код`, **тод**). */
function Inline({ text }: { text: string }) {
  return (
    <Markdown remarkPlugins={[remarkGfm]} components={{ p: ({ children }) => <>{children}</> }}>
      {text}
    </Markdown>
  );
}

/**
 * «Шалгах асуулт» — хичээлийн дундах мэдлэг шалгах асуулт.
 *
 * Хариулт хадгалагдахгүй, оноо өгөхгүй — сурагч өөрийгөө шалгах зорилготой.
 * Буруу бол дахин сонгож болно, эсвэл «Хариуг харах».
 */
export function QuizBlock({ quiz }: { quiz: Quiz }) {
  const id = useId();
  const multiple = quiz.options.filter((option) => option.correct).length > 1;
  const [selected, setSelected] = useState<number[]>([]);
  const [result, setResult] = useState<"correct" | "wrong" | null>(null);
  const [revealed, setRevealed] = useState(false);

  const toggle = (index: number) => {
    setResult(null);
    setSelected((current) =>
      multiple
        ? current.includes(index)
          ? current.filter((item) => item !== index)
          : [...current, index]
        : [index],
    );
  };

  const check = () => {
    const correct = quiz.options.every(
      (option, index) => option.correct === selected.includes(index),
    );
    setResult(correct ? "correct" : "wrong");
    if (correct) setRevealed(true);
  };

  const showAnswer = () => {
    setSelected(quiz.options.flatMap((option, index) => (option.correct ? [index] : [])));
    setResult("correct");
    setRevealed(true);
  };

  return (
    <fieldset className="not-prose bg-card rounded-lg border p-4">
      <legend className="sr-only">{mn.learn.quiz.title}</legend>
      <p className="text-muted-foreground flex items-center gap-1.5 text-xs font-semibold tracking-wide uppercase">
        <ListChecksIcon className="size-3.5" aria-hidden />
        {mn.learn.quiz.title}
        {multiple && <span className="normal-case">· {mn.learn.quiz.multiple}</span>}
      </p>
      <div id={`${id}-question`} className="mt-2 font-medium">
        <Inline text={quiz.question} />
      </div>

      <div
        role={multiple ? "group" : "radiogroup"}
        aria-labelledby={`${id}-question`}
        className="mt-3 space-y-2"
      >
        {quiz.options.map((option, index) => {
          const checked = selected.includes(index);
          const showState = revealed && (option.correct || checked);
          return (
            <label
              key={index}
              className={cn(
                "flex cursor-pointer items-start gap-2.5 rounded-md border px-3 py-2 text-sm transition-colors",
                checked ? "border-primary bg-primary/5" : "hover:bg-muted/60",
                showState && option.correct && "border-success bg-success/10",
                showState && !option.correct && "border-destructive bg-destructive/10",
              )}
            >
              <input
                type={multiple ? "checkbox" : "radio"}
                name={id}
                checked={checked}
                onChange={() => toggle(index)}
                className="accent-primary mt-0.5 size-4 shrink-0"
              />
              <span className="min-w-0">
                <Inline text={option.text} />
              </span>
            </label>
          );
        })}
      </div>

      <div className="mt-3 flex flex-wrap items-center gap-2">
        <Button size="sm" variant="outline" onClick={check} disabled={selected.length === 0}>
          {mn.learn.quiz.check}
        </Button>
        {result === "wrong" && !revealed && (
          <Button size="sm" variant="ghost" onClick={showAnswer}>
            {mn.learn.quiz.reveal}
          </Button>
        )}
      </div>

      <div aria-live="polite">
        {result && (
          <div
            className={cn(
              "mt-3 flex items-start gap-2 text-sm",
              result === "correct" ? "text-success" : "text-destructive",
            )}
          >
            {result === "correct" ? (
              <CircleCheckIcon className="mt-0.5 size-4 shrink-0" aria-hidden />
            ) : (
              <CircleXIcon className="mt-0.5 size-4 shrink-0" aria-hidden />
            )}
            <span>{result === "correct" ? mn.learn.quiz.correct : mn.learn.quiz.wrong}</span>
          </div>
        )}
        {revealed && quiz.explanation && (
          <div className="text-foreground/90 mt-2 text-sm">
            <Inline text={quiz.explanation} />
          </div>
        )}
      </div>
    </fieldset>
  );
}
