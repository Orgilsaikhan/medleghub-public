import type { Metadata } from "next";

import { RequireAuth } from "@/components/auth/require-auth";
import { StudyGuide } from "@/components/live/study-guide";
import { Skeleton } from "@/components/ui/skeleton";
import { mn } from "@/lib/i18n/mn";

export const metadata: Metadata = {
  title: `${mn.live.tools.guide} · ${mn.live.title}`,
};

export default async function LiveGuidePage({
  params,
}: PageProps<"/live/materials/[materialId]/guide/[topicId]">) {
  const { materialId, topicId } = await params;
  return (
    // `overflow-x-clip`: толгойн чимэглэл хэвтээ гүйлгээ үүсгэхгүй.
    <div className="container-page overflow-x-clip py-8 lg:py-12">
      <RequireAuth fallback={<Skeleton className="mx-auto h-96 w-full max-w-3xl rounded-3xl" />}>
        <StudyGuide materialId={materialId} topicId={topicId} />
      </RequireAuth>
    </div>
  );
}
