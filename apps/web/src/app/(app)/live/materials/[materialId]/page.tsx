import type { Metadata } from "next";

import { RequireAuth } from "@/components/auth/require-auth";
import { StudySet, StudySetSkeleton } from "@/components/live/study-set";
import { mn } from "@/lib/i18n/mn";

export const metadata: Metadata = {
  title: mn.live.title,
};

export default async function LiveMaterialPage({
  params,
}: PageProps<"/live/materials/[materialId]">) {
  const { materialId } = await params;
  return (
    <div className="container-page py-8 lg:py-12">
      <RequireAuth fallback={<StudySetSkeleton />}>
        <StudySet materialId={materialId} />
      </RequireAuth>
    </div>
  );
}
