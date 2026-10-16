import { apiFetch } from "@/lib/api/client";
import type { FeedbackInput, MessageResult } from "@/lib/types/api";

export function sendFeedback(input: FeedbackInput): Promise<MessageResult> {
  return apiFetch<MessageResult>("/feedback", { method: "POST", json: input });
}
