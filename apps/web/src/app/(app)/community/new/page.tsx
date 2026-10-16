import type { Metadata } from "next";

import { RequireAuth } from "@/components/auth/require-auth";
import { CommunityGate } from "@/components/community/community-gate";
import { PostForm } from "@/components/community/post-form";
import { Skeleton } from "@/components/ui/skeleton";
import { mn } from "@/lib/i18n/mn";

export const metadata: Metadata = {
  title: mn.community.newTitle,
};

export default function NewPostPage() {
  return (
    <div className="container-page py-10 lg:py-14">
      <div className="mx-auto max-w-3xl">
        <header>
          <h1 className="text-3xl font-bold tracking-tight sm:text-4xl">{mn.community.newTitle}</h1>
          <p className="text-muted-foreground mt-2">{mn.community.newSubtitle}</p>
        </header>

        <div className="mt-8">
          <RequireAuth fallback={<Skeleton className="h-[34rem] w-full rounded-xl" />}>
            <CommunityGate />
            <PostForm />
          </RequireAuth>
        </div>
      </div>
    </div>
  );
}
