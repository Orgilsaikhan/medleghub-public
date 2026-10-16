import { CodeIcon, ListChecksIcon, PlayIcon } from "lucide-react";

import { Section } from "@/components/marketing/section";
import { mn } from "@/lib/i18n/mn";

const ICONS = [ListChecksIcon, PlayIcon, CodeIcon];

export function HowItWorks() {
  return (
    <Section title={mn.home.howTitle} subtitle={mn.home.howSubtitle} muted>
      <ol className="grid gap-6 md:grid-cols-3">
        {mn.home.howSteps.map((step, index) => {
          const Icon = ICONS[index];
          return (
            <li key={step.title} className="bg-card relative rounded-xl border p-6">
              <div className="bg-primary/10 text-primary grid size-11 place-items-center rounded-lg">
                <Icon className="size-5" aria-hidden />
              </div>

              <div className="mt-4 flex items-baseline gap-2">
                <span className="text-muted-foreground font-mono text-sm tabular-nums">
                  {String(index + 1).padStart(2, "0")}
                </span>
                <h3 className="font-semibold">{step.title}</h3>
              </div>

              <p className="text-muted-foreground mt-2 text-sm leading-relaxed">{step.body}</p>
            </li>
          );
        })}
      </ol>
    </Section>
  );
}
