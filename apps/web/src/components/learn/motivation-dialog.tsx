"use client";

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { toast } from "sonner";

import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { updateAccount } from "@/lib/api/account";
import { ApiError } from "@/lib/api/client";
import { mn } from "@/lib/i18n/mn";
import type { Motivation } from "@/lib/motivation";
import { queryKeys } from "@/lib/query-keys";

interface MotivationDialogProps {
  motivation: Motivation | null;
  onClose: () => void;
  /** Нэвтрээгүй бол «Дахиж харуулахгүй» товч гарахгүй. */
  canDisable: boolean;
}

/** Дасгалын тестэд 3 удаа дараалан унасны дараах урам өгөх үг — монгол, англиар. */
export function MotivationDialog({ motivation, onClose, canDisable }: MotivationDialogProps) {
  const queryClient = useQueryClient();
  const disable = useMutation({
    mutationFn: () => updateAccount({ show_motivation: false }),
    onSuccess: (user) => {
      queryClient.setQueryData(queryKeys.currentUser, user);
      toast.success(mn.motivation.disabled);
      onClose();
    },
    onError: (error) =>
      toast.error(error instanceof ApiError ? error.message : mn.common.somethingWrong),
  });

  return (
    <Dialog open={motivation !== null} onOpenChange={(open) => !open && onClose()}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          {/* Дэлгэц уншигчид л — харагдах гарчиг хэрэггүй. */}
          <DialogTitle className="sr-only">{mn.motivation.title}</DialogTitle>
          <DialogDescription className="text-xs">{mn.motivation.context}</DialogDescription>
        </DialogHeader>

        {motivation && (
          <div className="space-y-3 py-2">
            <p lang="mn" className="text-lg leading-snug font-semibold">
              {motivation.mn.map((line, index) => (
                <span key={index} className="block">
                  {line}
                </span>
              ))}
            </p>
            <p lang="en" className="text-muted-foreground text-sm leading-relaxed italic">
              {motivation.en.map((line, index) => (
                <span key={index} className="block">
                  {line}
                </span>
              ))}
            </p>
          </div>
        )}

        <DialogFooter className="flex-row flex-wrap justify-end gap-2">
          {canDisable && (
            <Button
              variant="ghost"
              size="sm"
              disabled={disable.isPending}
              onClick={() => disable.mutate()}
            >
              {mn.motivation.disable}
            </Button>
          )}
          <Button size="sm" onClick={onClose}>
            {mn.motivation.tryAgain}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
