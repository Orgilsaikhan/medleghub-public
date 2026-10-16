import { CheckIcon } from "lucide-react";

import { Section } from "@/components/marketing/section";
import { mn } from "@/lib/i18n/mn";

export function WhyLearnHere() {
  return (
    <Section title={mn.home.whyTitle} muted>
      <ul className="grid gap-6 sm:grid-cols-2">
        {mn.home.whyItems.map((item) => (
          <li key={item.title} className="flex gap-4">
            <span
              aria-hidden
              className="bg-success/10 text-success mt-0.5 grid size-8 shrink-0 place-items-center rounded-full"
            >
              <CheckIcon className="size-4" />
            </span>
            <div>
              <h3 className="font-semibold">{item.title}</h3>
              <p className="text-muted-foreground mt-1 text-sm leading-relaxed">{item.body}</p>
            </div>
          </li>
        ))}
      </ul>
    </Section>
  );
}
