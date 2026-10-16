"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { ArrowLeftIcon, FileXIcon, HeartIcon, MessageCircleIcon } from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useSyncExternalStore } from "react";
import { useForm } from "react-hook-form";
import { toast } from "sonner";

import { ConfirmDelete } from "@/components/admin/confirm-delete";
import { EmptyState, ErrorState } from "@/components/common/states";
import { useIsSuspended } from "@/components/community/community-gate";
import { CommunityMarkdown } from "@/components/community/community-markdown";
import { AuthorByline, PostTags, RelativeTime } from "@/components/community/post-meta";
import { ReportDialog } from "@/components/community/report-dialog";
import { SuspendDialog } from "@/components/community/suspend-dialog";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Skeleton } from "@/components/ui/skeleton";
import { Textarea } from "@/components/ui/textarea";
import { ApiError } from "@/lib/api/client";
import { addComment, deleteComment, deletePost, getPost, setPostLike } from "@/lib/api/community";
import { useCurrentUser } from "@/lib/hooks/use-auth";
import { mn } from "@/lib/i18n/mn";
import { queryKeys } from "@/lib/query-keys";
import type { CommentItem, PostAuthor, PostDetail } from "@/lib/types/api";
import { cn } from "@/lib/utils";
import { commentSchema, type CommentFormValues } from "@/lib/validation/community";

function toastError(error: unknown) {
  toast.error(error instanceof ApiError ? error.message : mn.common.somethingWrong);
}

/** Зохиогч эсвэл админ устгана. MedlegHub-ийн нийтлэлийг зөвхөн админ. */
function useCanDelete(author: PostAuthor | null): boolean {
  const { user, isAdmin } = useCurrentUser();
  return isAdmin || (author !== null && author.id === user?.id);
}

/**
 * Зохиогчийн эсрэг хийх үйлдлүүд: мэдэгдэх (өөрийнх биш, түдгэлзээгүй бол),
 * админд түдгэлзүүлэх. MedlegHub-ийн нийтлэлийг түдгэлзүүлэх зохиогчгүй.
 */
function useModeration(author: PostAuthor | null) {
  const { user, isAdmin } = useCurrentUser();
  const suspended = useIsSuspended();
  const isMine = author !== null && author.id === user?.id;
  return {
    canReport: !isMine && !suspended,
    canSuspend: isAdmin && author !== null && !isMine,
  };
}

/**
 * Нийтлэл — бүтэн агуулга, лайк, сэтгэгдэл, мэдэгдэх, устгах.
 *
 * `#comment-<id>` хаягаар орвол (админы гомдлын холбоос) тухайн сэтгэгдэл рүү
 * гүйлгэж тодруулна.
 */
export function PostView({ postId }: { postId: string }) {
  const query = useQuery({
    queryKey: queryKeys.community.post(postId),
    queryFn: () => getPost(postId),
    retry: (count, error) => !(error instanceof ApiError && error.isNotFound) && count < 2,
  });

  const hash = useSyncExternalStore(subscribeToHash, readHash, () => "");
  const highlighted = hash.startsWith("#comment-") ? hash.slice("#comment-".length) : null;

  const loaded = query.isSuccess;
  useEffect(() => {
    if (!loaded || !highlighted) return;
    const target = document.getElementById(`comment-${highlighted}`);
    target?.scrollIntoView({ block: "center" });
    target?.focus({ preventScroll: true });
  }, [loaded, highlighted]);

  return (
    <div className="mx-auto max-w-3xl">
      <Link
        href="/community"
        className="text-muted-foreground hover:text-foreground inline-flex items-center gap-1.5 rounded-md text-sm transition-colors"
      >
        <ArrowLeftIcon aria-hidden className="size-4" />
        {mn.community.back}
      </Link>

      <div className="mt-6">
        {query.isPending ? (
          <PostSkeleton />
        ) : query.isError ? (
          query.error instanceof ApiError && query.error.isNotFound ? (
            <EmptyState
              icon={FileXIcon}
              title={mn.community.postNotFound}
              description={mn.community.postNotFoundBody}
            />
          ) : (
            <ErrorState onRetry={() => void query.refetch()} />
          )
        ) : (
          <PostContent post={query.data} highlighted={highlighted} />
        )}
      </div>
    </div>
  );
}

// Client-ийн шилжилтээр орвол URL (hash-тай) render-ийн дараа солигддог тул
// эхний render дээр биш, дараагийнх дээр (өгөгдөл ирэхэд) уншигдана.
function subscribeToHash(onChange: () => void) {
  window.addEventListener("hashchange", onChange);
  return () => window.removeEventListener("hashchange", onChange);
}

function readHash() {
  return window.location.hash;
}

function PostContent({ post, highlighted }: { post: PostDetail; highlighted: string | null }) {
  const router = useRouter();
  const queryClient = useQueryClient();
  const canDelete = useCanDelete(post.author);
  const { canReport, canSuspend } = useModeration(post.author);

  const remove = useMutation({
    mutationFn: () => deletePost(post.id),
    onSuccess: () => {
      toast.success(mn.community.postDeleted);
      void queryClient.invalidateQueries({ queryKey: queryKeys.community.lists });
      router.replace("/community");
      queryClient.removeQueries({ queryKey: queryKeys.community.post(post.id) });
    },
    onError: toastError,
  });

  return (
    <>
      <article>
        <PostTags post={post} />
        <h1 className="mt-3 text-2xl font-bold tracking-tight text-balance break-words sm:text-3xl">
          {post.title}
        </h1>
        <div className="text-muted-foreground mt-4 flex flex-wrap items-center gap-x-3 gap-y-1 text-sm">
          <AuthorByline author={post.author} link />
          <span aria-hidden>·</span>
          <RelativeTime iso={post.created_at} />
        </div>

        <CommunityMarkdown source={post.body} className="mt-6" />

        <div className="mt-8 flex flex-wrap items-center gap-2 border-t pt-4">
          <LikeButton post={post} />
          <span className="text-muted-foreground flex items-center gap-1.5 px-2 text-sm tabular-nums">
            <MessageCircleIcon aria-hidden className="size-4" />
            {mn.community.commentCount(post.comment_count)}
          </span>
          <div className="ml-auto flex items-center gap-1">
            {canReport && <ReportDialog target={{ kind: "post", id: post.id }} />}
            {canSuspend && post.author && <SuspendDialog user={post.author} />}
            {canDelete && (
              <ConfirmDelete
                name={mn.community.deletePostName(post.title)}
                onConfirm={() => remove.mutate()}
                isPending={remove.isPending}
              />
            )}
          </div>
        </div>
      </article>

      <Comments post={post} highlighted={highlighted} />
    </>
  );
}

function LikeButton({ post }: { post: PostDetail }) {
  const queryClient = useQueryClient();
  const suspended = useIsSuspended();
  const key = queryKeys.community.post(post.id);

  const like = useMutation({
    mutationFn: (liked: boolean) => setPostLike(post.id, liked),
    // Дармагц харагдана — серверийн хариугаар тоог засна.
    onMutate: (liked) => {
      queryClient.setQueryData<PostDetail>(key, (old) =>
        old && old.liked !== liked
          ? { ...old, liked, like_count: old.like_count + (liked ? 1 : -1) }
          : old,
      );
    },
    onSuccess: (result) => {
      queryClient.setQueryData<PostDetail>(key, (old) => old && { ...old, ...result });
    },
    onError: (error) => {
      toastError(error);
      void queryClient.invalidateQueries({ queryKey: key });
    },
    onSettled: () => void queryClient.invalidateQueries({ queryKey: queryKeys.community.lists }),
  });

  return (
    <Button
      variant="ghost"
      size="sm"
      aria-pressed={post.liked}
      disabled={suspended}
      onClick={() => like.mutate(!post.liked)}
      className="tabular-nums"
    >
      <HeartIcon
        aria-hidden
        className={cn("size-4", post.liked && "fill-rose-500 text-rose-500")}
      />
      <span className="sr-only">{mn.community.like}, </span>
      {post.like_count}
    </Button>
  );
}

function Comments({ post, highlighted }: { post: PostDetail; highlighted: string | null }) {
  const suspended = useIsSuspended();
  return (
    <section aria-labelledby="comments-title" className="mt-10">
      <h2 id="comments-title" className="text-lg font-semibold">
        {mn.community.commentsTitle}
        <span className="text-muted-foreground ml-2 text-base font-normal tabular-nums">
          {post.comment_count}
        </span>
      </h2>

      {post.comments.length === 0 ? (
        <p className="text-muted-foreground mt-3 text-sm">{mn.community.commentsEmpty}</p>
      ) : (
        <ul className="bg-card mt-4 divide-y rounded-xl border">
          {post.comments.map((comment) => (
            <CommentRow
              key={comment.id}
              postId={post.id}
              comment={comment}
              highlighted={comment.id === highlighted}
            />
          ))}
        </ul>
      )}

      {!suspended && <CommentForm postId={post.id} />}
    </section>
  );
}

interface CommentRowProps {
  postId: string;
  comment: CommentItem;
  /** Гомдлын холбоосоор орсон бол тодруулна. */
  highlighted: boolean;
}

function CommentRow({ postId, comment, highlighted }: CommentRowProps) {
  const queryClient = useQueryClient();
  const canDelete = useCanDelete(comment.author);
  const { canReport, canSuspend } = useModeration(comment.author);

  const remove = useMutation({
    mutationFn: () => deleteComment(comment.id),
    onSuccess: () => {
      toast.success(mn.community.commentDeleted);
      queryClient.setQueryData<PostDetail>(queryKeys.community.post(postId), (old) =>
        old
          ? {
              ...old,
              comments: old.comments.filter((item) => item.id !== comment.id),
              comment_count: old.comment_count - 1,
            }
          : old,
      );
      void queryClient.invalidateQueries({ queryKey: queryKeys.community.lists });
    },
    onError: toastError,
  });

  const preview = comment.body.length > 120 ? `${comment.body.slice(0, 120)}…` : comment.body;

  return (
    <li
      id={`comment-${comment.id}`}
      tabIndex={-1}
      className={cn("scroll-mt-24 px-5 py-4 outline-none", highlighted && "bg-accent/60")}
    >
      <div className="text-muted-foreground flex flex-wrap items-center gap-x-3 gap-y-1 text-xs">
        <AuthorByline author={comment.author} link />
        <span aria-hidden>·</span>
        <RelativeTime iso={comment.created_at} />
        <div className="ml-auto flex items-center">
          {canReport && <ReportDialog target={{ kind: "comment", id: comment.id }} compact />}
          {canSuspend && <SuspendDialog user={comment.author} compact />}
          {canDelete && (
            <ConfirmDelete
              name={preview}
              onConfirm={() => remove.mutate()}
              isPending={remove.isPending}
              compact
            />
          )}
        </div>
      </div>
      <CommunityMarkdown source={comment.body} className="mt-2 text-sm" />
    </li>
  );
}

function CommentForm({ postId }: { postId: string }) {
  const queryClient = useQueryClient();
  const form = useForm<CommentFormValues>({
    resolver: zodResolver(commentSchema),
    defaultValues: { body: "" },
  });

  const mutation = useMutation({
    mutationFn: (values: CommentFormValues) => addComment(postId, values.body),
    onSuccess: (comment) => {
      queryClient.setQueryData<PostDetail>(queryKeys.community.post(postId), (old) =>
        old
          ? {
              ...old,
              comments: [...old.comments, comment],
              comment_count: old.comment_count + 1,
            }
          : old,
      );
      void queryClient.invalidateQueries({ queryKey: queryKeys.community.lists });
      form.reset({ body: "" });
    },
    onError: toastError,
  });

  const error = form.formState.errors.body?.message;

  return (
    <form
      onSubmit={form.handleSubmit((values) => mutation.mutate(values))}
      noValidate
      className="mt-6 space-y-2"
    >
      <Label htmlFor="comment-body">{mn.community.commentLabel}</Label>
      <Textarea
        id="comment-body"
        rows={3}
        maxLength={3000}
        placeholder={mn.community.commentPlaceholder}
        aria-invalid={error ? true : undefined}
        aria-describedby={cn("comment-body-hint", error && "comment-body-error")}
        className={cn(error && "border-destructive")}
        {...form.register("body")}
      />
      {error && (
        <p id="comment-body-error" role="alert" className="text-destructive text-xs">
          {error}
        </p>
      )}
      <div className="flex flex-wrap items-start justify-between gap-3">
        <p id="comment-body-hint" className="text-muted-foreground max-w-md text-xs">
          {mn.community.markdownHint}
        </p>
        <Button type="submit" disabled={mutation.isPending}>
          {mutation.isPending ? mn.community.commentSending : mn.community.commentSend}
        </Button>
      </div>
    </form>
  );
}

export function PostSkeleton() {
  return (
    <div className="space-y-4">
      <Skeleton className="h-5 w-40" />
      <Skeleton className="h-9 w-3/4" />
      <Skeleton className="h-5 w-48" />
      <Skeleton className="h-40 w-full" />
    </div>
  );
}
