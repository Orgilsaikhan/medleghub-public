import type { Metadata } from "next";

import { RequireAuth } from "@/components/auth/require-auth";
import { CommunityGate } from "@/components/community/community-gate";
import { PostSkeleton, PostView } from "@/components/community/post-view";
import { mn } from "@/lib/i18n/mn";

export const metadata: Metadata = {
  title: mn.community.title,
};

export default async function PostPage({ params }: PageProps<"/community/[id]">) {
  const { id } = await params;
  return (
    <div className="container-page py-10 lg:py-14">
      <RequireAuth fallback={<PostSkeleton />}>
        <div className="mx-auto max-w-3xl">
          <CommunityGate />
        </div>
        <PostView postId={id} />
      </RequireAuth>
    </div>
  );
}
