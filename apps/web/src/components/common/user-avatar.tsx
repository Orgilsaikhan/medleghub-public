import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { avatarUrl } from "@/lib/avatar";
import { initials } from "@/lib/format";
import type { User } from "@/lib/types/api";
import { cn } from "@/lib/utils";

interface UserAvatarProps {
  user: Pick<User, "id" | "name" | "avatar_key">;
  className?: string;
  fallbackClassName?: string;
}

/**
 * Профайлын зураг, байхгүй бол нэрийн эхний үсгүүд.
 *
 * Үсэг нь `brand-link` өнгөтэй — цайвар дэвсгэр дээр `primary` (улбар шар) нь
 * 4.5:1-д хүрдэггүй. Хар толгой хэсэгт (`user-menu`) `text-primary`-оор дарна.
 */
export function UserAvatar({ user, className, fallbackClassName }: UserAvatarProps) {
  const src = avatarUrl(user);
  return (
    <Avatar className={className}>
      {/* Хажууд нь нэр бичигдсэн байдаг тул зураг нь чимэглэл — alt хоосон. */}
      {src && <AvatarImage src={src} alt="" />}
      <AvatarFallback
        className={cn("bg-primary/10 text-brand-link font-semibold", fallbackClassName)}
      >
        {initials(user.name)}
      </AvatarFallback>
    </Avatar>
  );
}
