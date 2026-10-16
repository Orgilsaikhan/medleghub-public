import type { Metadata } from "next";

import { RequireAuth } from "@/components/auth/require-auth";
import { LiveQuiz } from "@/components/live/quiz";
import { Skeleton } from "@/components/ui/skeleton";
import { mn } from "@/lib/i18n/mn";

export const metadata: Metadata = {
  title: `${mn.live.quiz.title} · ${mn.live.title}`,
};

/** `?topic=<id>` — сэдвийн тест; байхгүй бол бүтэн тест. */
export default async function LiveQuizPage({
  params,
  searchParams,
}: PageProps<"/live/materials/[materialId]/quiz">) {
  const { materialId } = await params;
  const { topic } = await searchParams;
  const topicId = (Array.isArray(topic) ? topic[0] : topic) || null;
  return (
    // `overflow-x-clip`: толгойн чимэглэл хэвтээ гүйлгээ үүсгэхгүй.
    <div className="container-page overflow-x-clip py-8 lg:py-12">
      <RequireAuth fallback={<Skeleton className="mx-auto h-96 w-full max-w-3xl rounded-3xl" />}>
        <LiveQuiz key={topicId ?? "all"} materialId={materialId} topicId={topicId} />
      </RequireAuth>
    </div>
  );
}
