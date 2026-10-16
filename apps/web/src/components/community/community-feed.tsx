"use client";

import { keepPreviousData, useQuery } from "@tanstack/react-query";
import { HeartIcon, MessageCircleIcon, MessagesSquareIcon, XIcon } from "lucide-react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { useTransition } from "react";

import { EmptyState, ErrorState } from "@/components/common/states";
import { useIsSuspended } from "@/components/community/community-gate";
import { Pagination } from "@/components/common/pagination";
import { AuthorByline, PostTags, RelativeTime } from "@/components/community/post-meta";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Skeleton } from "@/components/ui/skeleton";
import { listPosts, type PostListParams } from "@/lib/api/community";
import {
  mn,
  postLanguageLabels,
  postLanguageOrder,
  postTypeLabels,
  postTypeOrder,
} from "@/lib/i18n/mn";
import { queryKeys } from "@/lib/query-keys";
import type { PostLanguage, PostSummary, PostType } from "@/lib/types/api";
import { cn } from "@/lib/utils";

const ALL = "all";
const PAGE_SIZE = 20;

/** URL-аас ирсэн утгыг цэвэрлэж, зөвшөөрөгдсөн утга л дамжуулна. */
function parseParams(params: URLSearchParams): PostListParams {
  const language = params.get("language");
  const type = params.get("type");
  const page = Number.parseInt(params.get("page") ?? "1", 10);
  return {
    language: postLanguageOrder.includes(language as PostLanguage)
      ? (language as PostLanguage)
      : undefined,
    type: postTypeOrder.includes(type as PostType) ? (type as PostType) : undefined,
    page: Number.isFinite(page) && page > 0 ? page : 1,
    page_size: PAGE_SIZE,
  };
}

/**
 * Community-ийн нийтлэлүүд. Шүүлтүүр, хуудас нь URL-д — хуваалцах, буцах
 * товч, refresh зөв ажиллана.
 */
export function CommunityFeed() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [isPending, startTransition] = useTransition();
  const params = parseParams(searchParams);
  const suspended = useIsSuspended();

  const query = useQuery({
    queryKey: queryKeys.community.posts(params),
    queryFn: () => listPosts(params),
    placeholderData: keepPreviousData,
  });

  const hasFilters = Boolean(params.language || params.type);

  function apply(next: Record<string, string | null>) {
    const updated = new URLSearchParams(searchParams.toString());
    for (const [key, value] of Object.entries(next)) {
      if (!value || value === ALL) updated.delete(key);
      else updated.set(key, value);
    }
    updated.delete("page"); // шүүлтүүр солигдвол эхний хуудас руу
    const search = updated.toString();
    startTransition(() => router.replace(search ? `/community?${search}` : "/community"));
  }

  function buildHref(page: number) {
    const updated = new URLSearchParams(searchParams.toString());
    if (page > 1) updated.set("page", String(page));
    else updated.delete("page");
    const search = updated.toString();
    return search ? `/community?${search}` : "/community";
  }

  return (
    <div className="space-y-6">
      <div className="bg-muted/40 flex flex-col gap-3 rounded-xl border p-3 sm:flex-row sm:items-center">
        <div className="flex flex-1 gap-3">
          <div className="w-full sm:w-44">
            <Label htmlFor="community-language" className="sr-only">
              {mn.community.languageLabel}
            </Label>
            <Select
              value={params.language ?? ALL}
              onValueChange={(value) => apply({ language: value })}
            >
              <SelectTrigger id="community-language" className="w-full">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value={ALL}>{mn.community.allLanguages}</SelectItem>
                {postLanguageOrder.map((value) => (
                  <SelectItem key={value} value={value}>
                    {postLanguageLabels[value]}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div className="w-full sm:w-52">
            <Label htmlFor="community-type" className="sr-only">
              {mn.community.typeLabel}
            </Label>
            <Select value={params.type ?? ALL} onValueChange={(value) => apply({ type: value })}>
              <SelectTrigger id="community-type" className="w-full">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value={ALL}>{mn.community.allTypes}</SelectItem>
                {postTypeOrder.map((value) => (
                  <SelectItem key={value} value={value}>
                    {postTypeLabels[value]}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </div>

        {hasFilters && (
          <Button
            variant="ghost"
            onClick={() => apply({ language: null, type: null })}
            className="shrink-0"
          >
            <XIcon className="size-4" />
            {mn.community.clearFilters}
          </Button>
        )}
      </div>

      {query.isPending ? (
        <CommunityFeedSkeleton />
      ) : query.isError ? (
        <ErrorState onRetry={() => void query.refetch()} />
      ) : query.data.items.length === 0 ? (
        <EmptyState
          icon={MessagesSquareIcon}
          title={hasFilters ? mn.community.emptyFiltered : mn.community.empty}
          description={hasFilters ? mn.community.emptyFilteredHint : mn.community.emptyHint}
          action={
            !hasFilters &&
            !suspended && (
              <Button asChild>
                <Link href="/community/new">{mn.community.newPost}</Link>
              </Button>
            )
          }
        />
      ) : (
        <>
          <p className="text-muted-foreground text-sm" aria-live="polite">
            {mn.community.postCount(query.data.total)}
          </p>
          <ul
            className={cn(
              "space-y-3 transition-opacity",
              (isPending || query.isPlaceholderData) && "opacity-60",
            )}
          >
            {query.data.items.map((post) => (
              <li key={post.id}>
                <PostCard post={post} />
              </li>
            ))}
          </ul>
          <Pagination
            page={query.data.page}
            totalPages={query.data.total_pages}
            buildHref={buildHref}
          />
        </>
      )}
    </div>
  );
}

/** Карт бүхэлдээ дарагдана — гарчгийн холбоос картыг бүрхэнэ (`after:inset-0`). */
function PostCard({ post }: { post: PostSummary }) {
  return (
    <article className="bg-card hover:border-foreground/25 focus-within:ring-ring relative rounded-xl border p-5 transition-colors focus-within:ring-2">
      <PostTags post={post} />
      <h2 className="mt-3 text-base leading-snug font-semibold sm:text-lg">
        <Link
          href={`/community/${post.id}`}
          className="after:absolute after:inset-0 after:rounded-xl focus-visible:outline-none"
        >
          {post.title}
        </Link>
      </h2>
      {post.excerpt && (
        <p className="text-muted-foreground mt-1.5 line-clamp-2 text-sm">{post.excerpt}</p>
      )}
      <div className="text-muted-foreground mt-4 flex flex-wrap items-center gap-x-3 gap-y-2 text-xs">
        <AuthorByline author={post.author} className="max-w-full" />
        <span aria-hidden>·</span>
        <RelativeTime iso={post.created_at} />
        <span className="ml-auto flex items-center gap-3 tabular-nums">
          <span className="flex items-center gap-1">
            <HeartIcon
              aria-hidden
              className={cn("size-4", post.liked && "fill-rose-500 text-rose-500")}
            />
            <span className="sr-only">{mn.community.like}: </span>
            {post.like_count}
          </span>
          <span className="flex items-center gap-1">
            <MessageCircleIcon aria-hidden className="size-4" />
            <span className="sr-only">{mn.community.commentsTitle}: </span>
            {post.comment_count}
          </span>
        </span>
      </div>
    </article>
  );
}

export function CommunityFeedSkeleton() {
  return (
    <div className="space-y-3">
      {Array.from({ length: 4 }, (_, index) => (
        <Skeleton key={index} className="h-36 w-full rounded-xl" />
      ))}
    </div>
  );
}
