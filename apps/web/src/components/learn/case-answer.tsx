"use client";

import { ArrowRightIcon, SearchCheckIcon } from "lucide-react";
import Link from "next/link";
import { useCallback, useId, useRef, useState, type FormEvent, type ReactNode } from "react";
import { toast } from "sonner";

import { MotivationDialog } from "@/components/learn/motivation-dialog";
import { BadgeUnlockDialog } from "@/components/profile/badge-unlock-dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ApiError } from "@/lib/api/client";
import { useCurrentUser } from "@/lib/hooks/use-auth";
import { useCaseAnswer } from "@/lib/hooks/use-progress";
import { mn } from "@/lib/i18n/mn";
import { MOTIVATION_AFTER_FAILS, MOTIVATIONS, pickIndex, type Motivation } from "@/lib/motivation";
import type { BadgeUnlocked } from "@/lib/types/api";
import { cn } from "@/lib/utils";

interface CaseAnswerBarProps {
  courseSlug: string;
  lessonSlug: string;
  lessonId: string;
  nextHref: string | null;
  helpAction?: ReactNode;
}

interface Verdict {
  tone: "success" | "info" | "error";
  text: string;
  /** Зөв хариултын дараа дараагийн хичээл рүү очих холбоос харуулна. */
  next?: boolean;
}

const TONES: Record<Verdict["tone"], string> = {
  success: "text-success",
  info: "text-foreground",
  error: "text-destructive",
};

/**
 * Мөрдөгчийн хэргийн «Хариулт» мөр (SQL).
 *
 * Сурагч асуулгаа засварлагч дээр ажиллуулж, олсон хариултаа («Анужин»)
 * энд бичнэ. Зөв эсэхийг зөвхөн сервер мэднэ — хариулт хөтөчид ирдэггүй.
 * Зөв бөгөөд бүртгүүлсэн бол сервер хичээлийг дуусгана.
 */
export function CaseAnswerBar({
  courseSlug,
  lessonSlug,
  lessonId,
  nextHref,
  helpAction,
}: CaseAnswerBarProps) {
  const inputId = useId();
  const [answer, setAnswer] = useState("");
  const [verdict, setVerdict] = useState<Verdict | null>(null);
  const check = useCaseAnswer(courseSlug, lessonSlug);

  // Дараалан 3 буруу хариулт — дасгалын тесттэй адил урам өгөх үг.
  const { user } = useCurrentUser();
  const showMotivation = user?.show_motivation ?? true;
  const wrongStreak = useRef(0);
  const lastMotivation = useRef<number | null>(null);
  const [motivation, setMotivation] = useState<Motivation | null>(null);
  // Солонгон тэмдэг (жишээ нь сүүлийн хэргээр «Where the Answers Hide») том цонхонд.
  const [unlocked, setUnlocked] = useState<BadgeUnlocked | null>(null);

  const recordWrong = useCallback(() => {
    wrongStreak.current += 1;
    if (wrongStreak.current < MOTIVATION_AFTER_FAILS) return;
    wrongStreak.current = 0;
    if (!showMotivation) return;
    const index = pickIndex(MOTIVATIONS.length, lastMotivation.current);
    lastMotivation.current = index;
    setMotivation(MOTIVATIONS[index]);
  }, [showMotivation]);

  const submit = (event: FormEvent) => {
    event.preventDefault();
    const given = answer.trim();
    if (!given || check.isPending) return;
    setVerdict(null);
    check.mutate(
      { lessonId, answer: given },
      {
        onSuccess: (result) => {
          if (!result.correct) {
            setVerdict({ tone: "error", text: mn.learn.case.wrong });
            recordWrong();
            return;
          }
          wrongStreak.current = 0;
          if (result.course_progress?.percent === 100) toast.success(mn.learn.courseComplete);
          const prismatic = result.new_badges.find((badge) => badge.prismatic);
          if (prismatic) setUnlocked(prismatic);
          // Бүртгүүлээгүй бол зөв ч ахиц хадгалагдахгүй.
          setVerdict(
            result.completed
              ? { tone: "success", text: mn.learn.case.solved, next: true }
              : { tone: "info", text: mn.learn.case.solvedNotEnrolled },
          );
        },
        onError: (error) =>
          setVerdict({
            tone: "error",
            text: error instanceof ApiError ? error.message : mn.common.somethingWrong,
          }),
      },
    );
  };

  return (
    <div className="bg-muted/40 shrink-0 border-t px-3 py-2.5">
      <MotivationDialog
        motivation={motivation}
        onClose={() => setMotivation(null)}
        canDisable={user !== null}
      />
      <BadgeUnlockDialog badge={unlocked} onClose={() => setUnlocked(null)} />
      <form onSubmit={submit} className="flex flex-wrap items-center gap-2">
        <label htmlFor={inputId} className="inline-flex items-center gap-1.5 text-sm font-semibold">
          <SearchCheckIcon className="size-4" aria-hidden />
          {mn.learn.case.label}
        </label>
        <Input
          id={inputId}
          value={answer}
          onChange={(event) => setAnswer(event.target.value)}
          placeholder={mn.learn.case.placeholder}
          maxLength={200}
          autoComplete="off"
          spellCheck={false}
          aria-describedby={`${inputId}-verdict`}
          className="bg-background min-w-40 flex-1"
        />
        <Button type="submit" size="sm" disabled={!answer.trim() || check.isPending}>
          {check.isPending ? mn.learn.case.checking : mn.learn.case.check}
        </Button>
        {helpAction}
      </form>
      {/* Дэлгэц уншигчид шалгалтын хариуг зарлана. */}
      <p
        id={`${inputId}-verdict`}
        role="status"
        aria-live="polite"
        className={cn("text-sm empty:hidden", verdict && "mt-2", verdict && TONES[verdict.tone])}
      >
        {verdict?.text}
        {verdict?.next && nextHref && (
          <Link
            href={nextHref}
            className="text-brand-link ml-2 inline-flex items-center gap-1 font-medium underline-offset-4 hover:underline"
          >
            {mn.learn.case.next}
            <ArrowRightIcon className="size-3.5" aria-hidden />
          </Link>
        )}
      </p>
    </div>
  );
}
