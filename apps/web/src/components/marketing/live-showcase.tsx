import { ArrowRightIcon, BookOpenCheckIcon, FileUpIcon, TargetIcon } from "lucide-react";
import Link from "next/link";
import { type CSSProperties, Fragment } from "react";

import { LiveMark } from "@/components/live/live-mark";
import { LiveTile } from "@/components/live/live-ui";
import { LiveShowcaseStage } from "@/components/marketing/live-showcase-stage";
import { LiveShowcaseVideo } from "@/components/marketing/live-showcase-video";
import { Button } from "@/components/ui/button";
import { mn } from "@/lib/i18n/mn";
import { cn } from "@/lib/utils";

const t = mn.homeLive;

/** Алхам бүрийн дүрс. AI-ийн алхамд (`null`) Live-ийн тэмдэг. */
const STEP_ICONS = [FileUpIcon, null, BookOpenCheckIcon, TargetIcon] as const;

/** `--i` — дарааллын дугаар; хөдөлгөөний саатлыг CSS үүнээс тооцно. */
const order = (index: number) => ({ "--i": index }) as CSSProperties;

/**
 * Нүүр хуудасны «Шинэ · MedlegHub Live» хэсэг: зүүн талд видео
 * (`live-showcase-video.tsx`), баруун талд танилцуулга. Утсан дээр гарчиг →
 * видео → алхмууд.
 *
 * Хэсэг харагдах хэсэгт ормогц бүх зүйл дарааллаар орж ирнэ (`globals.css` →
 * `.home-live`): видеоны дэлгэц ТВ шиг асна, гарчгийн үгс доороос гарна,
 * лекцээс шалгалт хүртэлх утас доош татагдаж алхам бүрийг асаана; дараа нь
 * утсаар гэрэл гүйнэ. Бичвэрт opacity ашиглахгүй (зөвхөн transform, mask,
 * clip-path) — хөдөлгөөний дунд ч тодрол (WCAG AA) хэвээр.
 */
export function LiveShowcase() {
  const words = t.title.split(" ");

  return (
    <LiveShowcaseStage
      aria-labelledby="home-live-title"
      className="home-live relative isolate overflow-hidden border-b py-16 lg:py-20"
    >
      {/* Дээд захын шар гэрэл — «шинэ» гэдгийг дуугүй хэлнэ. */}
      <span
        aria-hidden
        className="via-primary/50 pointer-events-none absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent to-transparent"
      />
      <span
        aria-hidden
        className="bg-primary/8 motion-safe:animate-glow-drift home-live-loop pointer-events-none absolute -right-48 bottom-0 -z-10 size-[34rem] rounded-full blur-3xl [animation-direction:alternate-reverse]"
      />

      <div
        className={cn(
          "container-page grid gap-10 [grid-template-areas:'head'_'video'_'body']",
          "lg:grid-cols-[minmax(0,1.1fr)_minmax(0,1fr)] lg:[grid-template-rows:1fr_auto_auto_1fr] lg:gap-x-12 lg:gap-y-0 xl:gap-x-20",
          "lg:[grid-template-areas:'video_.'_'video_head'_'video_body'_'video_.']",
        )}
      >
        <div className="[grid-area:head]">
          <p className="home-live-badge relative inline-flex overflow-hidden rounded-full p-px shadow-sm">
            {/* Хүрээгээр гүйх гэрэл: эргэдэг conic градиент, дотор талыг карт халхална. */}
            <span aria-hidden className="bg-border absolute inset-0" />
            <span
              aria-hidden
              className="home-live-beam home-live-loop absolute top-1/2 left-1/2 aspect-square w-[160%] -translate-x-1/2 -translate-y-1/2 bg-[conic-gradient(transparent_0deg_250deg,var(--primary)_320deg,transparent_360deg)]"
            />
            <span className="bg-card relative inline-flex items-center gap-2 rounded-full px-3.5 py-1.5 text-sm font-medium">
              <span aria-hidden className="bg-primary size-2 rounded-full" />
              <span className="text-brand-link font-semibold">{t.badgeNew}</span>
              <span aria-hidden className="text-muted-foreground">
                ·
              </span>
              {t.badgeName}
            </span>
          </p>

          {/* Live-ийн толгойтой (`live-hero.tsx`) ижил шар хавтан + тэмдэг. */}
          <div className="mt-5 flex items-center gap-4 sm:gap-5">
            <LiveTile className="home-live-tile size-14 rounded-2xl xl:size-16 xl:rounded-[1.3rem]">
              <LiveMark className="size-8 xl:size-9" />
            </LiveTile>
            <h2
              id="home-live-title"
              className="text-4xl leading-[1.1] font-bold tracking-tight text-balance lg:text-5xl xl:text-6xl"
            >
              {/* Үгсийг тус тусад нь хөдөлгөнө — дэлгэц уншигч бүтэн өгүүлбэрийг уншина. */}
              <span className="sr-only">{t.title}</span>
              <span aria-hidden>
                {words.map((word, index) => (
                  <Fragment key={`${word}-${index}`}>
                    {index > 0 && " "}
                    <TitleWord word={word} index={index} highlight={word === t.titleHighlight} />
                  </Fragment>
                ))}
              </span>
            </h2>
          </div>

          <p className="home-live-lede text-muted-foreground mt-5 max-w-xl text-lg leading-relaxed text-pretty">
            {t.body}
          </p>
        </div>

        <div className="min-w-0 [grid-area:video] lg:self-center">
          <LiveShowcaseVideo />
        </div>

        <div className="[grid-area:body] lg:mt-9">
          <ol aria-label={t.stepsLabel} className="max-w-xl">
            {t.steps.map((step, index) => {
              const Icon = STEP_ICONS[index];
              const last = index === t.steps.length - 1;
              return (
                <li
                  key={step.title}
                  style={order(index)}
                  className="relative flex gap-4 pb-5 last:pb-0"
                >
                  {!last && <Wire />}
                  <span
                    aria-hidden
                    className="home-live-node bg-card text-brand-link relative grid size-10 shrink-0 place-items-center rounded-xl border shadow-xs"
                  >
                    {Icon ? <Icon className="size-5" /> : <LiveMark className="size-5" />}
                    <span className="home-live-node-ping home-live-loop ring-primary/70 absolute -inset-1 rounded-[0.95rem] opacity-0 ring-2" />
                  </span>
                  <div className="home-live-step-text min-w-0 pt-1">
                    <h3 className="font-semibold">{step.title}</h3>
                    <p className="text-muted-foreground mt-1 text-sm leading-relaxed text-pretty">
                      {step.body}
                    </p>
                  </div>
                </li>
              );
            })}
          </ol>

          <div className="home-live-cta mt-9 flex flex-col gap-3 sm:flex-row">
            <Button asChild size="lg">
              <Link href="/live">
                {t.ctaPrimary}
                <ArrowRightIcon className="size-4" />
              </Link>
            </Button>
            <Button asChild size="lg" variant="outline">
              <Link href="/pricing">{t.ctaSecondary}</Link>
            </Button>
          </div>
          <p className="home-live-note text-muted-foreground mt-4 text-sm text-pretty">{t.note}</p>
        </div>
      </div>
    </LiveShowcaseStage>
  );
}

/**
 * Гарчгийн нэг үг. Гадна `span` нь халхавч (`clip-path`): үг түүний доороос
 * гарч ирнэ. Онцлох үг («Live») шар өнгөтэй, доор нь зураас татагдана.
 */
function TitleWord({
  word,
  index,
  highlight,
}: {
  word: string;
  index: number;
  highlight: boolean;
}) {
  const masked = (
    <span className="home-live-word-mask inline-block">
      <span className="home-live-word inline-block" style={order(index)}>
        {word}
      </span>
    </span>
  );
  if (!highlight) return masked;

  return (
    <span className="text-brand-link relative inline-block">
      {masked}
      <svg
        viewBox="0 0 100 12"
        preserveAspectRatio="none"
        className="text-primary absolute -bottom-2 left-0 h-3 w-full overflow-visible"
      >
        <path
          className="home-live-swoosh"
          d="M2 8.5C24 3.2 60 2.4 98 6.2"
          fill="none"
          stroke="currentColor"
          strokeWidth="3.5"
          strokeLinecap="round"
          pathLength={1}
        />
      </svg>
    </span>
  );
}

/**
 * Алхмуудыг холбох утас: суурь зураас, орж ирэхэд доош татагдах шар зураас,
 * дараа нь утсаар гүйх гэрэл (`home-live-wire-pulse`).
 */
function Wire() {
  return (
    <span
      aria-hidden
      className="pointer-events-none absolute top-12 bottom-1 left-5 w-3 -translate-x-1/2 overflow-hidden"
    >
      <span className="bg-border absolute inset-y-0 left-1/2 w-px -translate-x-1/2" />
      <span className="home-live-wire-fill from-primary/80 to-primary/25 absolute inset-y-0 left-1/2 w-0.5 -translate-x-1/2 rounded-full bg-gradient-to-b" />
      <span className="home-live-wire-pulse home-live-loop absolute inset-0 opacity-0" />
    </span>
  );
}
