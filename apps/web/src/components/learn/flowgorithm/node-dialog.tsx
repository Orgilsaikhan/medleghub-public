"use client";

import { useState } from "react";
import { Trash2Icon } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  declaredNames,
  HINTS,
  LABELS,
  type FlowNode,
  type DataType,
} from "@/lib/flowgorithm/model";

export function NodeDialog({
  node,
  onSave,
  onDelete,
  onClose,
}: {
  node: FlowNode;
  onSave: (node: FlowNode) => void;
  onDelete: () => void;
  onClose: () => void;
}) {
  const [draft, setDraft] = useState(node);
  const [confirmDelete, setConfirmDelete] = useState(false);
  const change = (field: keyof FlowNode, value: string | boolean) =>
    setDraft({ ...draft, [field]: value });
  const hasName = ["declare", "assign", "input", "for"].includes(node.kind);
  const hasExpression = ["assign", "output", "if", "while", "do", "comment"].includes(node.kind);
  const expressionLabel = ["if", "while", "do"].includes(node.kind)
    ? "Нөхцөл (Expression)"
    : node.kind === "comment"
      ? "Тайлбар"
      : "Илэрхийлэл (Expression)";
  const field = (
    key: "name" | "expression" | "start" | "end" | "step",
    label: string,
    placeholder?: string,
  ) => (
    <div className="space-y-1.5" key={key}>
      <Label htmlFor={`flow-${key}`}>{label}</Label>
      <Input
        id={`flow-${key}`}
        value={draft[key] ?? ""}
        onChange={(event) => change(key, event.target.value)}
        maxLength={500}
        required={key !== "expression" || node.kind !== "comment"}
        autoComplete="off"
        spellCheck={false}
        placeholder={placeholder}
      />
    </div>
  );
  return (
    <Dialog
      open
      onOpenChange={(open) => {
        if (!open) onClose();
      }}
    >
      <DialogContent className="max-h-[90dvh] overflow-y-auto sm:max-w-md">
        <DialogHeader>
          <DialogTitle>
            {LABELS[node.kind]} — {HINTS[node.kind]}
          </DialogTitle>
          <DialogDescription>Дүрсний утгыг оруулаад хадгална уу.</DialogDescription>
        </DialogHeader>
        <form
          className="space-y-4"
          onSubmit={(event) => {
            event.preventDefault();
            onSave(
              node.kind === "declare"
                ? { ...draft, name: declaredNames(draft.name).join(", ") }
                : draft,
            );
          }}
        >
          {hasName &&
            field("name", node.kind === "declare" ? "Нэр (Name)" : "Хувьсагч (Variable)", "number")}
          {node.kind === "input" && (
            <p className="text-muted-foreground text-xs">
              Нэг Input нэг хувьсагчид утга авна. Олон хувьсагчид тусдаа Input дүрс нэмнэ.
            </p>
          )}
          {node.kind === "declare" && (
            <div className="space-y-1.5">
              <Label htmlFor="flow-data-type">Төрөл (Type)</Label>
              <select
                id="flow-data-type"
                value={draft.dataType}
                onChange={(event) => change("dataType", event.target.value as DataType)}
                className="bg-background h-10 w-full rounded-md border px-3"
              >
                <option value="Integer">Integer — бүхэл тоо</option>
                <option value="Real">Real — бодит тоо</option>
                <option value="String">String — текст</option>
                <option value="Boolean">Boolean — үнэн / худал</option>
              </select>
              <p className="text-muted-foreground text-xs">
                Олон нэрийг таслалаар тусгаарлаж болно: a, b, total.
              </p>
            </div>
          )}
          {hasExpression &&
            field(
              "expression",
              expressionLabel,
              node.kind === "output" ? '"Сайн уу!"' : "number + 1",
            )}
          {node.kind === "output" && (
            <label className="flex items-center gap-2 text-sm">
              <input
                type="checkbox"
                checked={draft.newline}
                onChange={(event) => change("newline", event.target.checked)}
              />
              Шинэ мөр (New Line)
            </label>
          )}
          {node.kind === "for" && (
            <>
              <div className="grid grid-cols-3 gap-3">
                {field("start", "Эхлэл (Start)")}
                {field("end", "Төгсгөл (End)")}
                {field("step", "Алхам (Step)")}
              </div>
              <div className="space-y-1.5">
                <Label htmlFor="flow-direction">Чиглэл (Direction)</Label>
                <select
                  id="flow-direction"
                  className="bg-background h-10 w-full rounded-md border px-3"
                  value={draft.direction}
                  onChange={(event) => change("direction", event.target.value)}
                >
                  <option value="inc">Increasing — өсөх</option>
                  <option value="dec">Decreasing — буурах</option>
                </select>
              </div>
            </>
          )}
          {node.kind === "do" && (
            <p className="text-muted-foreground text-sm">
              Доторх үйлдлээ эхлээд хийнэ. Нөхцөл true байвал дахин давтана.
            </p>
          )}
          {node.kind === "breakpoint" && (
            <p className="text-muted-foreground text-sm">
              Ажиллагаа энэ дүрсэнд ирээд түр зогсоно. Үргэлжлүүлэх эсвэл алхмаар ажиллуулах
              боломжтой.
            </p>
          )}
          {hasExpression && node.kind !== "comment" && (
            <p className="text-muted-foreground text-xs">
              Текстийг давхар хашилтад бичнэ. Текст залгах: &amp; · Тэнцүү эсэх: == · Үлдэгдэл: mod
            </p>
          )}
          {confirmDelete && (
            <p className="text-destructive text-sm" role="alert">
              Доторх бүх дүрстэй нь устгах уу? Устгасны дараа «Буцаах» боломжтой.
            </p>
          )}
          <DialogFooter>
            <Button
              type="button"
              variant="destructive"
              className="sm:mr-auto"
              onClick={() => (confirmDelete ? onDelete() : setConfirmDelete(true))}
            >
              <Trash2Icon className="size-4" />
              {confirmDelete ? "Тийм, устгах" : "Устгах"}
            </Button>
            <Button type="button" variant="outline" onClick={onClose}>
              Болих
            </Button>
            <Button type="submit">Хадгалах</Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
