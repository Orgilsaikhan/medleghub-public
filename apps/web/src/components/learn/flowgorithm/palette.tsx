"use client";

import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { HINTS, LABELS, type NodeKind } from "@/lib/flowgorithm/model";
import { Shape } from "./shape";

const groups: { title: string; kinds: NodeKind[] }[] = [
  { title: "Input / Output", kinds: ["input", "output"] },
  { title: "Variables", kinds: ["declare", "assign"] },
  { title: "Control", kinds: ["if"] },
  { title: "Looping", kinds: ["while", "for", "do"] },
];

export function Palette({
  onSelect,
  onClose,
}: {
  onSelect: (kind: NodeKind) => void;
  onClose: () => void;
}) {
  const item = (kind: NodeKind) => (
    <button
      type="button"
      key={kind}
      aria-label={`${LABELS[kind]} — ${HINTS[kind]}`}
      onClick={() => onSelect(kind)}
      className="group flex w-full flex-col items-center gap-1.5 rounded p-2 outline-offset-4 hover:bg-sky-50 focus-visible:outline-2 focus-visible:outline-sky-600"
    >
      <span className="relative flex h-12 w-full max-w-32 items-center justify-center">
        <Shape kind={kind} />
        <span className="relative z-10 text-sm text-slate-950">{LABELS[kind]}</span>
      </span>
      <span className="text-center text-[11px] text-slate-600">{HINTS[kind]}</span>
    </button>
  );
  return (
    <Dialog
      open
      onOpenChange={(open) => {
        if (!open) onClose();
      }}
    >
      <DialogContent className="max-h-[90dvh] overflow-y-auto rounded-sm bg-white p-5 text-slate-950 sm:max-w-[680px]">
        <DialogHeader>
          <DialogTitle>Дүрс нэмэх</DialogTitle>
          <DialogDescription className="text-slate-600">
            Сонгосон сумны байрлалд нэмэгдэх үйлдлээ сонгоорой.
          </DialogDescription>
        </DialogHeader>
        <div className="border border-sky-600/60 bg-sky-200 px-3 py-2 text-sm">Miscellaneous</div>
        <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
          {item("comment")}
          {item("breakpoint")}
        </div>
        <div className="border border-sky-600/60 bg-sky-200 px-3 py-2 text-sm">Statement</div>
        <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
          {groups.map((group) => (
            <div key={group.title} className="space-y-3">
              <p className="text-center text-sm text-slate-600">{group.title}</p>
              {group.kinds.map(item)}
            </div>
          ))}
        </div>
      </DialogContent>
    </Dialog>
  );
}
