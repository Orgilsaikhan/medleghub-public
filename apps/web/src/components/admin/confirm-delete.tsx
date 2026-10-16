"use client";

import { Trash2Icon } from "lucide-react";
import { useState } from "react";

import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { mn } from "@/lib/i18n/mn";

interface ConfirmDeleteProps {
  /** Устгах зүйлийн нэр — баталгаажуулах цонхонд харагдана. */
  name: string;
  onConfirm: () => void;
  isPending?: boolean;
  /** Зөвхөн дүрстэй жижиг товч эсэх. */
  compact?: boolean;
}

/** Устгах үйлдэл буцаагдахгүй тул үргэлж баталгаажуулна. */
export function ConfirmDelete({ name, onConfirm, isPending, compact }: ConfirmDeleteProps) {
  const [open, setOpen] = useState(false);

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        {compact ? (
          <Button variant="ghost" size="icon" aria-label={mn.admin.delete} title={mn.admin.delete}>
            <Trash2Icon className="size-4" />
          </Button>
        ) : (
          <Button variant="outline" size="sm">
            <Trash2Icon className="size-4" />
            {mn.admin.delete}
          </Button>
        )}
      </DialogTrigger>

      <DialogContent>
        <DialogHeader>
          <DialogTitle>{mn.admin.deleteConfirm}</DialogTitle>
          <DialogDescription>{name}</DialogDescription>
        </DialogHeader>

        <DialogFooter>
          <Button variant="outline" onClick={() => setOpen(false)}>
            {mn.admin.cancel}
          </Button>
          <Button
            variant="destructive"
            disabled={isPending}
            onClick={() => {
              setOpen(false);
              onConfirm();
            }}
          >
            {mn.admin.delete}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
