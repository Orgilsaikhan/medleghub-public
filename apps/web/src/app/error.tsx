"use client";

import { useEffect } from "react";

import { ErrorState } from "@/components/common/states";

export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    // Production дээр энэ нь log цуглуулагч руу очно.
    console.error(error);
  }, [error]);

  return (
    <main className="container-page flex flex-1 items-center justify-center py-24">
      <ErrorState onRetry={reset} className="w-full max-w-md" />
    </main>
  );
}
