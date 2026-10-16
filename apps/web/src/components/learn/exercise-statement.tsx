import { CircleIcon, SearchIcon } from "lucide-react";

import { LessonContent } from "@/components/learn/lesson-content";
import { mn } from "@/lib/i18n/mn";
import type { LessonExercise } from "@/lib/types/api";

/**
 * Дасгалын даалгавар — HackerRank-ийн «Problem» хэсэгтэй адил.
 *
 * Жишээ оролт/гаралтыг даалгаврын текстэд давтаж бичдэггүй — `sample`
 * тестүүдээс шууд харуулна. Ингэснээр харагдаж буй жишээ болон «Тест
 * ажиллуулах»-ын шалгадаг зүйл хэзээ ч зөрөхгүй.
 */
export function ExerciseStatement({
  exercise,
  note,
}: {
  exercise: LessonExercise;
  /** Даалгаврын доорх тайлбар — жишээ нь Flowgorithm-ийн оролтын дүрэм. */
  note?: string;
}) {
  const samples = exercise.tests.filter((test) => test.sample);
  // React-ийн DOM тест: оролт/гаралтгүй — нэр нь шаардлага болж жагсана.
  const requirements = exercise.tests.filter((test) => test.code).map((test) => test.name ?? "");

  // SQL-ийн мөрдөгчийн хэрэг: тест, жишээгүй — хариултаа доор бичнэ.
  if (exercise.kind === "answer") {
    return (
      <section aria-labelledby="exercise-title" className="mt-10 border-t pt-6">
        <h2
          id="exercise-title"
          className="inline-flex items-center gap-2 text-xl font-semibold tracking-tight"
        >
          <SearchIcon className="size-5" aria-hidden />
          {mn.learn.case.title}
        </h2>
        <div className="mt-3">
          <LessonContent content={exercise.statement} />
        </div>
        <p className="text-muted-foreground mt-4 text-sm">{mn.learn.case.hint}</p>
      </section>
    );
  }

  if (requirements.length > 0) {
    return (
      <section aria-labelledby="exercise-title" className="mt-10 border-t pt-6">
        <h2 id="exercise-title" className="text-xl font-semibold tracking-tight">
          {mn.learn.exercise.title}
        </h2>
        <div className="mt-3">
          <LessonContent content={exercise.statement} />
        </div>
        <h3 className="mt-5 text-sm font-semibold">{mn.learn.react.requirements}</h3>
        <p className="text-muted-foreground mt-0.5 text-xs">{mn.learn.react.requirementsHint}</p>
        <ul className="mt-2 space-y-1.5">
          {requirements.map((name, index) => (
            <li key={index} className="flex items-start gap-2 text-sm">
              <CircleIcon className="text-muted-foreground mt-1 size-3 shrink-0" aria-hidden />
              <span>{name}</span>
            </li>
          ))}
        </ul>
      </section>
    );
  }

  // Жишээнүүд дэлгэцийн биш уншлагын хэсгийн өргөнөөр багана болно — Flowgorithm-ийн
  // нарийн хэсэгт доошоо, өргөн хэсэгт хажуу хажуугаар.
  return (
    <section aria-labelledby="exercise-title" className="@container mt-10 border-t pt-6">
      <h2 id="exercise-title" className="text-xl font-semibold tracking-tight">
        {mn.learn.exercise.title}
      </h2>

      <div className="mt-3">
        <LessonContent content={exercise.statement} />
      </div>

      {note && <p className="text-muted-foreground mt-4 text-sm">{note}</p>}

      {samples.map((test, index) => (
        <div key={index} className="mt-5 grid gap-3 @lg:grid-cols-2">
          <SampleBlock
            title={mn.learn.exercise.sampleInput(index + 1)}
            text={test.stdin}
            placeholder={mn.learn.exercise.noInput}
          />
          <SampleBlock
            title={mn.learn.exercise.sampleOutput(index + 1)}
            text={test.expected_output}
          />
        </div>
      ))}
    </section>
  );
}

function SampleBlock({
  title,
  text,
  placeholder,
}: {
  title: string;
  text: string;
  placeholder?: string;
}) {
  // Төгсгөлийн шинэ мөр `<pre>` дотор илүү хоосон мөр болж харагдана.
  const shown = text.replace(/\n+$/, "");
  return (
    <div className="min-w-0">
      <h3 className="mb-1.5 text-sm font-semibold">{title}</h3>
      {/* Урт мөр хэвтээгээр гүйлгэгдэнэ — гарын түлхүүрээр ч хүрнэ (WCAG 2.1.1). */}
      <pre
        tabIndex={0}
        className="bg-code-bg border-code-border focus-visible:ring-ring overflow-x-auto rounded-lg border p-3 font-mono text-[13px] leading-relaxed focus-visible:ring-2 focus-visible:outline-none"
      >
        {shown ? shown : <span className="text-muted-foreground italic">{placeholder}</span>}
      </pre>
    </div>
  );
}
