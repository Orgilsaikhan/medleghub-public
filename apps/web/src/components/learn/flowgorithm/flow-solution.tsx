"use client";

import { parseProgram } from "@/lib/flowgorithm/model";
import { Chart } from "./chart";

/** «Тусламж»-ийн жишиг шийдэл — JSON биш, засварлагчийн адил блок схемээр. */
export default function FlowSolution({ source }: { source: string }) {
  let program;
  try {
    program = parseProgram(source);
  } catch {
    return (
      <pre className="bg-code-bg border-code-border overflow-x-auto rounded-lg border p-4 font-mono text-[13px]">
        {source}
      </pre>
    );
  }
  return (
    <div className="flex h-[55vh] min-h-72 flex-col overflow-hidden rounded-lg border">
      <Chart
        program={program}
        zoom={0.9}
        activeId={null}
        locked
        onEdit={() => {}}
        onInsert={() => {}}
      />
    </div>
  );
}
