"use client";

import { useQuery } from "@tanstack/react-query";
import {
  BookOpenIcon,
  Columns2Icon,
  FlameIcon,
  ListTreeIcon,
  PanelLeftCloseIcon,
  PanelLeftOpenIcon,
  Rows2Icon,
} from "lucide-react";
import dynamic from "next/dynamic";
import { useCallback, useState } from "react";
import { toast } from "sonner";

import { ErrorState } from "@/components/common/states";
import { ProgressBar } from "@/components/courses/progress-bar";
import { CaseAnswerBar } from "@/components/learn/case-answer";
import { CodePlayground, type SubmitNote } from "@/components/learn/code-playground";
import { CompleteButton } from "@/components/learn/complete-button";
import { CurriculumSidebar } from "@/components/learn/curriculum-sidebar";
import { ExerciseStatement } from "@/components/learn/exercise-statement";
import { HelpButton } from "@/components/learn/help-button";
import { HtmlWorkspace } from "@/components/learn/html/html-workspace";
import { LessonContent } from "@/components/learn/lesson-content";
import { LessonMobileTabs } from "@/components/learn/lesson-mobile-tabs";
import { LessonNav } from "@/components/learn/lesson-nav";
import { LessonPaywall } from "@/components/learn/lesson-paywall";
import { LessonSkeleton } from "@/components/learn/lesson-skeleton";
import { LessonVideo } from "@/components/learn/lesson-video";
import { ReactWorkspace } from "@/components/learn/react/react-workspace";
import { ResizableSplit } from "@/components/learn/resizable-split";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { ApiError } from "@/lib/api/client";
import { getLessonPlayer } from "@/lib/api/lessons";
import { formatDuration } from "@/lib/format";
import { useMediaQuery } from "@/lib/hooks/use-media-query";
import { useEditorLayout } from "@/lib/hooks/use-editor-layout";
import { useCompleteLesson } from "@/lib/hooks/use-progress";
import { mn } from "@/lib/i18n/mn";
import { readLocal, writeLocal } from "@/lib/local-storage";
import { queryKeys } from "@/lib/query-keys";
import { supportsExercises } from "@/lib/sandbox/grader";
import { cn } from "@/lib/utils";

/** Tailwind-ийн `lg` эвдрэлийн цэг — үүнээс дээш зурагт хэсэг, доош tab. */
const DESKTOP_QUERY = "(min-width: 1024px)";

const FlowEditor = dynamic(() => import("@/components/learn/flowgorithm/flow-editor"), {
  ssr: false,
  loading: () => <div className="p-5 text-sm">Схем ачаалж байна…</div>,
});
const FlowSolution = dynamic(() => import("@/components/learn/flowgorithm/flow-solution"), {
  ssr: false,
});

interface LessonViewProps {
  courseSlug: string;
  lessonSlug: string;
}

/** Хөтөлбөрийн хэсэг эвхэгдсэн эсэх — хичээл солигдоход хадгалагдана. */
const SIDEBAR_KEY = "medleghub:lesson-sidebar";

/**
 * Хичээлийн үндсэн дэлгэц.
 *
 * Шаардлагатай бүх өгөгдлийг НЭГ API дуудлагаар авна — хичээл, curriculum,
 * ахиц, өмнөх/дараагийн холбоос бүгд нэг response дотор (Performance §22).
 *
 * Том дэлгэцийн бүтэц: зүүн талд хөтөлбөр, дараа нь засварлагч ба заавар.
 * Хэрэглэгч «Тохиргоо»-ноос (эсвэл дээд мөрний товчоор) сонгоно:
 *   • шинэ (анхдагч) — засварлагч зүүн, «Заавар» баруун: React хичээлийнх шиг;
 *   • хуучин — заавар дээр, засварлагч ба console доор.
 * React, HTML & CSS хичээл үргэлж өөрийн (шинэ) байрлалтай — баруун талд
 * «Заавар / Хөтөч».
 */
export function LessonView({ courseSlug, lessonSlug }: LessonViewProps) {
  const query = useQuery({
    queryKey: queryKeys.lessons.player(courseSlug, lessonSlug),
    queryFn: () => getLessonPlayer(courseSlug, lessonSlug),
    staleTime: 30_000,
  });

  const isDesktop = useMediaQuery(DESKTOP_QUERY);
  const complete = useCompleteLesson(courseSlug, lessonSlug);
  const { layout, setLayout } = useEditorLayout();
  const sideBySide = layout === "new";

  // Сервер дээр `LessonSkeleton` render хийгддэг тул энэ төлөв нь зөвхөн
  // browser дээр хэрэглэгдэнэ — hydration зөрчил үүсэхгүй.
  const [sidebarCollapsed, setSidebarCollapsed] = useState(
    () => readLocal(SIDEBAR_KEY, "0") === "1",
  );

  const toggleSidebar = useCallback(() => {
    setSidebarCollapsed((collapsed) => {
      writeLocal(SIDEBAR_KEY, collapsed ? "0" : "1");
      return !collapsed;
    });
  }, []);

  if (query.isPending) return <LessonSkeleton />;

  if (query.isError) {
    const error = query.error;
    const notFound = error instanceof ApiError && error.isNotFound;
    return (
      <div className="container-page flex flex-1 items-center justify-center py-24">
        <ErrorState
          title={notFound ? mn.common.notFound : mn.common.error}
          description={error instanceof ApiError ? error.message : mn.common.somethingWrong}
          onRetry={notFound ? undefined : () => void query.refetch()}
          className="w-full max-w-md"
        />
      </div>
    );
  }

  const { course, lesson, modules, progress, enrolled, previous_lesson, next_lesson } = query.data;
  const isFlowgorithm = course.slug === "flowgorithm-undes";
  // React хичээл — react-tutorial.app маягийн засварлагч (файлууд, «Заавар /
  // Хөтөч», тест, console). Бусад хэл хуучин байршлаараа.
  const isReact = lesson.language === "jsx";
  // HTML & CSS — файлууд tab-аар, баруун талд шууд шинэчлэгдэх «Хөтөч».
  const isWeb = lesson.language === "html" || lesson.language === "css";
  const ownLayout = isReact || isWeb;

  // Шалгагч нь C/C++, Python-ийн worker, React-ийн sandbox, Flowgorithm-ийн
  // схемийн runtime дээр ажилладаг.
  const exercise =
    lesson.exercise &&
    lesson.exercise.kind !== "answer" &&
    (isFlowgorithm || supportsExercises(lesson.language))
      ? lesson.exercise
      : null;
  // SQL-ийн мөрдөгчийн хэрэг — тестгүй, хариултыг сервер шалгана.
  const caseFile =
    lesson.language === "mysql" && lesson.exercise?.kind === "answer" ? lesson.exercise : null;
  const statement = exercise ?? caseFile;
  const nextHref = next_lesson ? `/learn/${course.slug}/${next_lesson.slug}` : null;
  // Flowgorithm-д асуулт шалгалтад орохгүйг оролттой даалгаврын доор тайлбарлана.
  const statementNote =
    isFlowgorithm && exercise?.tests.some((test) => test.stdin.trim())
      ? mn.learn.exercise.flowInputNote
      : exercise && lesson.language === "javascript"
        ? mn.learn.exercise.jsInputNote
        : undefined;

  /** «Илгээх»-ийн бүх тест давсан — хичээлийг дуусгана. */
  const handleSubmitPassed = async (): Promise<SubmitNote> => {
    if (!enrolled) return { tone: "info", text: mn.learn.exercise.submitPassedNotEnrolled };
    if (lesson.completed) return { tone: "success", text: mn.learn.exercise.submitPassedAgain };
    try {
      const result = await complete.mutateAsync(lesson.id);
      if (result.course_progress.percent === 100) toast.success(mn.learn.courseComplete);
      return { tone: "success", text: mn.learn.exercise.submitPassed };
    } catch (error) {
      return {
        tone: "error",
        text: error instanceof ApiError ? error.message : mn.learn.exercise.submitSaveFailed,
      };
    }
  };

  const flowEditor = isFlowgorithm ? (
    <FlowEditor
      key={lesson.id}
      initialCode={lesson.initial_code}
      lessonId={lesson.id}
      exercise={exercise}
      onSubmitPassed={handleSubmitPassed}
      helpAction={
        exercise ? (
          <HelpButton
            lessonId={lesson.id}
            renderSolution={(solution) => <FlowSolution source={solution} />}
          />
        ) : undefined
      }
    />
  ) : null;

  /** Засварлагч, console — мөн SQL-ийн хэргийн «Хариулт» мөр. */
  const playground = (
    <>
      <CodePlayground
        key={lesson.id}
        initialCode={lesson.initial_code}
        language={lesson.language}
        exercise={exercise}
        onSubmitPassed={handleSubmitPassed}
        helpAction={exercise ? <HelpButton lessonId={lesson.id} /> : undefined}
      />
      {caseFile && (
        <CaseAnswerBar
          key={`case-${lesson.id}`}
          courseSlug={course.slug}
          lessonSlug={lesson.slug}
          lessonId={lesson.id}
          nextHref={nextHref}
          helpAction={<HelpButton lessonId={lesson.id} />}
        />
      )}
    </>
  );

  /** Шинэ байрлалын баруун тал — React хичээлийн «Заавар» tab шиг толгойтой. */
  const instructionsPane = (className: string) => (
    <section aria-label={mn.learn.instructions} className={cn("flex min-h-0 flex-col", className)}>
      <div className="flex h-10 shrink-0 items-center gap-2 border-b px-4 text-sm font-medium">
        <BookOpenIcon className="size-4" aria-hidden />
        {mn.learn.instructions}
      </div>
      <div className="min-h-0 flex-1">{reading}</div>
    </section>
  );

  const sidebar = (
    <CurriculumSidebar
      courseTitle={course.title}
      courseSlug={course.slug}
      modules={modules}
      progress={progress}
      currentSlug={lesson.slug}
    />
  );

  const reading = (
    /* Уншлагын хэсэг — тусдаа гүйлгэгдэнэ.
       `tabIndex` нь гарын түлхүүрээр гүйлгэх боломж олгоно (WCAG 2.1.1). */
    <div
      tabIndex={0}
      role="region"
      aria-label={mn.learn.lessonContent}
      className="h-full overflow-y-auto"
    >
      <LessonVideo src={lesson.video_url} />

      <div className="px-4 py-6 sm:px-6 lg:px-8">
        <div className="flex flex-wrap items-baseline justify-between gap-x-4 gap-y-1">
          <h1 className="text-xl font-bold tracking-tight sm:text-2xl">{lesson.title}</h1>
          <div className="flex items-center gap-3">
            {lesson.challenging && (
              <Badge
                title={mn.learn.challengingHint}
                className="border-yellow-500/60 bg-yellow-300 text-black"
              >
                <FlameIcon aria-hidden />
                {mn.learn.challenging}
                <span className="sr-only">. {mn.learn.challengingHint}</span>
              </Badge>
            )}
            {lesson.duration > 0 && (
              <span className="text-muted-foreground font-mono text-xs tabular-nums">
                {formatDuration(lesson.duration)}
              </span>
            )}
          </div>
        </div>

        {lesson.description && (
          <p className="text-muted-foreground mt-1.5 text-sm">{lesson.description}</p>
        )}

        <div className="mt-6">
          <LessonContent content={lesson.content} />
        </div>

        {statement && <ExerciseStatement exercise={statement} note={statementNote} />}

        <div className="mt-8 lg:hidden">
          <ProgressBar progress={progress} />
        </div>
      </div>
    </div>
  );

  return (
    <div className="flex min-h-0 flex-1">
      {/* Эвхэгдсэн үед өргөн нь тэг болно. `overflow-hidden` нь доторх
          агуулгыг гаргахгүй, `inert` нь фокус орохоос сэргийлнэ. */}
      <aside
        inert={sidebarCollapsed}
        className={cn(
          "hidden shrink-0 overflow-hidden transition-[width] duration-200 lg:block",
          sidebarCollapsed ? "lg:w-0" : "lg:w-72 lg:border-r xl:w-80",
        )}
      >
        {sidebar}
      </aside>

      <div className="flex min-h-0 min-w-0 flex-1 flex-col">
        {/* Хөтөлбөрийг нууж, кодод илүү зай гаргах товч. */}
        <div className="hidden shrink-0 items-center gap-2 border-b px-2 py-1.5 lg:flex">
          <Button
            variant="ghost"
            size="sm"
            onClick={toggleSidebar}
            aria-expanded={!sidebarCollapsed}
          >
            {sidebarCollapsed ? (
              <PanelLeftOpenIcon className="size-4" aria-hidden />
            ) : (
              <PanelLeftCloseIcon className="size-4" aria-hidden />
            )}
            {mn.learn.curriculum}
          </Button>
          <span className="text-muted-foreground truncate text-xs">{course.title}</span>
          {/* React, HTML & CSS хичээл өөрийн байрлалтай — сонголт хамаарахгүй. */}
          {!ownLayout && !lesson.locked && (
            <Button
              variant="ghost"
              size="sm"
              className="ml-auto"
              onClick={() => setLayout(sideBySide ? "legacy" : "new")}
              title={sideBySide ? mn.learn.layoutToLegacyHint : mn.learn.layoutToNewHint}
            >
              {sideBySide ? (
                <Rows2Icon className="size-4" aria-hidden />
              ) : (
                <Columns2Icon className="size-4" aria-hidden />
              )}
              {sideBySide ? mn.learn.layoutToLegacy : mn.learn.layoutToNew}
            </Button>
          )}
          <span
            className={cn(
              "text-muted-foreground shrink-0 font-mono text-xs tabular-nums",
              (ownLayout || lesson.locked) && "ml-auto",
            )}
          >
            {progress.completed_lessons} / {progress.total_lessons}
          </span>
        </div>

        {/* Жижиг дэлгэц дээр хөтөлбөр эвхэгддэг хэсэгт орно. */}
        <details className="shrink-0 border-b lg:hidden">
          <summary className="flex cursor-pointer list-none items-center gap-2 px-4 py-3 text-sm font-medium">
            <ListTreeIcon className="size-4" aria-hidden />
            {mn.learn.curriculum}
            <span className="text-muted-foreground ml-auto text-xs tabular-nums">
              {progress.completed_lessons} / {progress.total_lessons}
            </span>
          </summary>
          <div className="max-h-[50vh] overflow-y-auto border-t">{sidebar}</div>
        </details>

        {lesson.locked ? (
          <LessonPaywall
            title={lesson.title}
            description={lesson.description}
            returnTo={`/learn/${course.slug}/${lesson.slug}`}
          />
        ) : isFlowgorithm ? (
          isDesktop ? (
            sideBySide ? (
              <div className="flex min-h-0 min-w-0 flex-1">
                <div className="flex min-h-0 min-w-0 flex-1 flex-col border-r">{flowEditor}</div>
                {instructionsPane("w-[38%] min-w-72 shrink-0")}
              </div>
            ) : (
              <div className="flex min-h-0 min-w-0 flex-1">
                <div className="w-[35%] min-w-64 shrink-0 border-r">{reading}</div>
                <div className="flex min-h-0 min-w-0 flex-1 flex-col">{flowEditor}</div>
              </div>
            )
          ) : (
            <LessonMobileTabs reading={reading} playground={flowEditor} codeLabel="Схем" />
          )
        ) : isReact ? (
          <ReactWorkspace
            key={lesson.id}
            lessonId={lesson.id}
            initialCode={lesson.initial_code}
            exercise={exercise}
            instructions={reading}
            isDesktop={isDesktop}
            onSubmitPassed={handleSubmitPassed}
            helpAction={exercise ? <HelpButton lessonId={lesson.id} /> : undefined}
            nextHref={nextHref}
          />
        ) : isWeb ? (
          <HtmlWorkspace
            key={lesson.id}
            lessonId={lesson.id}
            language={lesson.language}
            initialCode={lesson.initial_code}
            instructions={reading}
            isDesktop={isDesktop}
          />
        ) : sideBySide && isDesktop ? (
          /* Шинэ байрлал: засварлагч зүүн, «Заавар» баруун — React хичээл шиг. */
          <div className="flex min-h-0 min-w-0 flex-1">
            <div className="flex min-h-0 w-1/2 min-w-0 flex-col border-r">{playground}</div>
            {instructionsPane("w-1/2 min-w-0")}
          </div>
        ) : sideBySide ? (
          <LessonMobileTabs reading={reading} playground={playground} />
        ) : (
          /* Хуучин байрлал: тайлбар дээр, засварлагч доор. Хоорондын зурвасыг
             чирж хэмжээг нь өөрчилнө — эсвэл бүрэн эвхэж, зөвхөн код харна. */
          <ResizableSplit
            storageKey="medleghub:lesson-split"
            label={mn.learn.lessonContent}
            top={reading}
            bottom={playground}
          />
        )}

        <div className="shrink-0 border-t px-4 py-3 sm:px-6 lg:px-8">
          <LessonNav
            courseSlug={course.slug}
            previous={previous_lesson}
            next={next_lesson}
            center={
              lesson.locked ? undefined : (
                <CompleteButton
                  courseSlug={course.slug}
                  lessonSlug={lesson.slug}
                  lessonId={lesson.id}
                  completed={lesson.completed}
                  enrolled={enrolled}
                  nextLesson={next_lesson}
                  requiresSubmission={!!exercise || !!caseFile}
                  submissionHint={caseFile ? mn.learn.case.completeHint : undefined}
                />
              )
            }
          />
        </div>
      </div>
    </div>
  );
}
