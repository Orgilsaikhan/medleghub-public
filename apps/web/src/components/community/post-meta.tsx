"use client";

import { BadgeCheckIcon, PinIcon } from "lucide-react";
import Link from "next/link";

import { UserAvatar } from "@/components/common/user-avatar";
import { Badge } from "@/components/ui/badge";
import { formatDate, formatRelative } from "@/lib/format";
import { useCurrentUser } from "@/lib/hooks/use-auth";
import { mn, postLanguageLabels, postTypeLabels } from "@/lib/i18n/mn";
import type { PostAuthor, PostLanguage, PostType } from "@/lib/types/api";
import { cn } from "@/lib/utils";

interface PostTagsProps {
  post: { language: PostLanguage; type: PostType; pinned: boolean };
  className?: string;
}

/** Хэл, төрлийн шошго. Онцолсон бол эхэнд нь тэмдэг. */
export function PostTags({ post, className }: PostTagsProps) {
  return (
    <div className={cn("flex flex-wrap items-center gap-1.5", className)}>
      {post.pinned && (
        <Badge>
          <PinIcon aria-hidden />
          {mn.community.pinned}
        </Badge>
      )}
      <Badge variant="secondary">
        <span className="sr-only">{mn.community.languageLabel}: </span>
        {postLanguageLabels[post.language]}
      </Badge>
      <Badge variant="outline">
        <span className="sr-only">{mn.community.typeLabel}: </span>
        {postTypeLabels[post.type]}
      </Badge>
    </div>
  );
}

interface AuthorBylineProps {
  /** `null` бол MedlegHub. */
  author: PostAuthor | null;
  /** Профайл руу холбоос болгох эсэх (нийтлэлийн карт бүхэлдээ холбоос тул тэнд үгүй). */
  link?: boolean;
  className?: string;
}

/** Зураг ба нэр. MedlegHub-ийн нийтлэлд брэндийн тэмдэг. */
export function AuthorByline({ author, link = false, className }: AuthorBylineProps) {
  const { user } = useCurrentUser();

  if (author === null) {
    return (
      <span className={cn("flex min-w-0 items-center gap-2", className)}>
        <span
          aria-hidden
          className="grid size-6 shrink-0 place-items-center rounded-full bg-black text-[10px] font-bold text-white"
        >
          M
        </span>
        <span className="text-foreground font-medium">{mn.community.official}</span>
        <BadgeCheckIcon aria-hidden className="text-brand-link size-4 shrink-0" />
        <span className="sr-only">({mn.community.officialBadge})</span>
      </span>
    );
  }

  const isMe = author.id === user?.id;
  const content = (
    <>
      <UserAvatar user={author} className="size-6" fallbackClassName="text-[10px]" />
      <span className="text-foreground truncate font-medium">
        {author.name}
        {isMe && <span className="text-muted-foreground font-normal"> ({mn.community.you})</span>}
      </span>
    </>
  );

  // Профайлаа нуусан хүний профайл 403 буцаадаг тул холбоос хийхгүй.
  if (!link || (author.profile_hidden && !isMe)) {
    return <span className={cn("flex min-w-0 items-center gap-2", className)}>{content}</span>;
  }
  return (
    <Link
      href={isMe ? "/profile" : `/users/${author.id}`}
      className={cn("flex min-w-0 items-center gap-2 rounded-md hover:underline", className)}
    >
      {content}
    </Link>
  );
}

/** «5 минутын өмнө». Бүтэн огноо нь `title`-д. */
export function RelativeTime({ iso }: { iso: string }) {
  return (
    <time dateTime={iso} title={formatDate(iso)}>
      {formatRelative(iso)}
    </time>
  );
}
