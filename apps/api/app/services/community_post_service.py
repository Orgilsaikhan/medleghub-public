"""Community — нийтлэл, сэтгэгдэл, лайк, гомдол.

Зөвхөн нэвтэрсэн хэрэглэгчид: нууцлалын бодлогын 4.1-д заасанчлан нэр, зургийг
зочинд харуулахгүй. Хэрэглэгч өөрийн нийтлэл, сэтгэгдлээ устгана; админ бүгдийг.
Бичих, лайк дарах, мэдэгдэхийн өмнө дүрмийг зөвшөөрсөн, түдгэлзээгүй эсэхийг
шалгана (`community_moderation`). Гомдол нь `feedback` хүснэгтэд `report`
төрлөөр орж админы «Санал хүсэлт» хуудсанд ирнэ. Мессежид гомдол гаргасан
агуулгын хуулбар орно — зохиогч дараа нь устгасан ч админ юу мэдэгдсэнийг харна.
"""

import re
import uuid

from sqlalchemy import ColumnElement, delete, exists, func, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import defer, selectinload

from app.core.errors import ForbiddenError, NotFoundError
from app.models.community_post import CommunityComment, CommunityPost, CommunityPostLike
from app.models.enums import FeedbackKind, PostLanguage, PostType
from app.models.feedback import Feedback
from app.models.user import User
from app.schemas.community_post import (
    CommentCreate,
    CommentItem,
    LikeResult,
    PostAuthor,
    PostCreate,
    PostDetail,
    PostSummary,
    ReportCreate,
    ReportReason,
)
from app.services import community_moderation

DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 50

OFFICIAL_AUTHOR = "MedlegHub"

EXCERPT_LENGTH = 200
# Жагсаалтад биеийн эхний хэсгийг л уншина. Код блок хасагдах тул илүү авна.
_EXCERPT_SOURCE = 1000
# Мөрийн эхэнд ``` — хаагаагүй бол текстийн төгсгөл хүртэл.
_CODE_BLOCK = re.compile(r"^[ \t]*```.*?(?:^[ \t]*```[^\n]*$|\Z)", re.DOTALL | re.MULTILINE)
# Жагсаалтын тэмдэг (`- `, `1. `) ба хэвтээ зураас (`---`).
_BLOCK_MARKER = re.compile(r"^[ \t]*(?:[-+*]|\d+[.)])[ \t]+|^[ \t]*[-*_]{3,}[ \t]*$", re.MULTILINE)
_LINK = re.compile(r"!?\[([^\]]*)\]\([^)]*\)")
_MARKUP = re.compile(r"[#>*_`~|]+")

# Гомдлын мессежид хуулах агуулгын урт.
_REPORT_QUOTE_LENGTH = 600
_REPORT_REASONS = {
    ReportReason.SPAM: "Спам, зар сурталчилгаа",
    ReportReason.ABUSE: "Доромжилсон, зохисгүй агуулга",
    ReportReason.OTHER: "Бусад",
}


def excerpt(body: str) -> str:
    """Markdown-аас нэг мөр энгийн текст. Код блокыг бүхэлд нь хасна."""
    text = _CODE_BLOCK.sub(" ", body)
    text = _BLOCK_MARKER.sub("", text)
    text = _LINK.sub(r"\1", text)
    text = " ".join(_MARKUP.sub("", text).split())
    if len(text) <= EXCERPT_LENGTH:
        return text
    return text[:EXCERPT_LENGTH].rsplit(" ", 1)[0] + "…"


def _like_count() -> ColumnElement[int]:
    return (
        select(func.count())
        .where(CommunityPostLike.post_id == CommunityPost.id)
        .correlate(CommunityPost)
        .scalar_subquery()
    )


def _comment_count() -> ColumnElement[int]:
    return (
        select(func.count())
        .where(CommunityComment.post_id == CommunityPost.id)
        .correlate(CommunityPost)
        .scalar_subquery()
    )


def _liked_by(user: User) -> ColumnElement[bool]:
    return (
        exists()
        .where(CommunityPostLike.post_id == CommunityPost.id, CommunityPostLike.user_id == user.id)
        .correlate(CommunityPost)
    )


def _author(user: User | None) -> PostAuthor | None:
    return None if user is None else PostAuthor.model_validate(user)


def _ensure_can_delete(author_id: uuid.UUID | None, user: User) -> None:
    if user.is_admin or (author_id is not None and author_id == user.id):
        return
    raise ForbiddenError("NOT_AUTHOR", "Зөвхөн өөрийн бичсэнийг устгах боломжтой.")


def _post_not_found() -> NotFoundError:
    return NotFoundError("POST_NOT_FOUND", "Нийтлэл олдсонгүй. Устгагдсан байж магадгүй.")


async def _ensure_post_exists(db: AsyncSession, post_id: uuid.UUID) -> None:
    found = (
        await db.execute(select(CommunityPost.id).where(CommunityPost.id == post_id))
    ).scalar_one_or_none()
    if found is None:
        raise _post_not_found()


async def list_posts(
    db: AsyncSession,
    viewer: User,
    *,
    language: PostLanguage | None,
    type_: PostType | None,
    page: int,
    page_size: int,
) -> tuple[list[PostSummary], int]:
    """Онцолсон нь эхэндээ, дараа нь шинэ нь."""
    filters = []
    if language is not None:
        filters.append(CommunityPost.language == language)
    if type_ is not None:
        filters.append(CommunityPost.type == type_)

    total = (
        await db.execute(select(func.count()).select_from(CommunityPost).where(*filters))
    ).scalar_one()
    rows = await db.execute(
        select(
            CommunityPost,
            _like_count(),
            _comment_count(),
            _liked_by(viewer),
            func.left(CommunityPost.body, _EXCERPT_SOURCE),
        )
        .where(*filters)
        .options(defer(CommunityPost.body), selectinload(CommunityPost.author))
        .order_by(CommunityPost.pinned.desc(), CommunityPost.created_at.desc(), CommunityPost.id)
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    items = [
        PostSummary(
            id=post.id,
            title=post.title,
            language=post.language,
            type=post.type,
            pinned=post.pinned,
            author=_author(post.author),
            created_at=post.created_at,
            like_count=like_count,
            comment_count=comment_count,
            liked=liked,
            excerpt=excerpt(body_start),
        )
        for post, like_count, comment_count, liked, body_start in rows.all()
    ]
    return items, total


async def get_post(db: AsyncSession, post_id: uuid.UUID, viewer: User) -> PostDetail:
    row = (
        await db.execute(
            select(CommunityPost, _like_count(), _liked_by(viewer))
            .where(CommunityPost.id == post_id)
            .options(selectinload(CommunityPost.author))
        )
    ).one_or_none()
    if row is None:
        raise _post_not_found()
    post, like_count, liked = row

    comments = (
        (
            await db.execute(
                select(CommunityComment)
                .where(CommunityComment.post_id == post.id)
                .options(selectinload(CommunityComment.author))
                .order_by(CommunityComment.created_at, CommunityComment.id)
            )
        )
        .scalars()
        .all()
    )
    return PostDetail(
        id=post.id,
        title=post.title,
        language=post.language,
        type=post.type,
        pinned=post.pinned,
        author=_author(post.author),
        created_at=post.created_at,
        like_count=like_count,
        comment_count=len(comments),
        liked=liked,
        body=post.body,
        comments=[CommentItem.model_validate(comment) for comment in comments],
    )


async def create_post(db: AsyncSession, user: User, payload: PostCreate) -> PostDetail:
    await community_moderation.ensure_can_participate(db, user)
    post = CommunityPost(
        author_id=user.id,
        title=payload.title,
        body=payload.body,
        language=payload.language,
        type=payload.type,
    )
    db.add(post)
    await db.commit()
    return await get_post(db, post.id, user)


async def delete_post(db: AsyncSession, post_id: uuid.UUID, user: User) -> None:
    """Сэтгэгдэл, лайк нь `ON DELETE CASCADE`-ээр хамт устана."""
    author_id = (
        await db.execute(select(CommunityPost.author_id).where(CommunityPost.id == post_id))
    ).one_or_none()
    if author_id is None:
        raise _post_not_found()
    _ensure_can_delete(author_id[0], user)
    await db.execute(delete(CommunityPost).where(CommunityPost.id == post_id))
    await db.commit()


async def set_like(db: AsyncSession, post_id: uuid.UUID, user: User, liked: bool) -> LikeResult:
    """Давтан дарсан ч аюулгүй — лайк нэг л удаа тоологдоно."""
    await community_moderation.ensure_can_participate(db, user)
    await _ensure_post_exists(db, post_id)
    if liked:
        await db.execute(
            insert(CommunityPostLike)
            .values(post_id=post_id, user_id=user.id)
            .on_conflict_do_nothing()
        )
    else:
        await db.execute(
            delete(CommunityPostLike).where(
                CommunityPostLike.post_id == post_id, CommunityPostLike.user_id == user.id
            )
        )
    await db.commit()
    like_count = (
        await db.execute(
            select(func.count())
            .select_from(CommunityPostLike)
            .where(CommunityPostLike.post_id == post_id)
        )
    ).scalar_one()
    return LikeResult(liked=liked, like_count=like_count)


async def add_comment(
    db: AsyncSession, post_id: uuid.UUID, user: User, payload: CommentCreate
) -> CommentItem:
    await community_moderation.ensure_can_participate(db, user)
    await _ensure_post_exists(db, post_id)
    comment = CommunityComment(post_id=post_id, author=user, body=payload.body)
    db.add(comment)
    await db.commit()
    await db.refresh(comment, ["created_at"])
    return CommentItem.model_validate(comment)


async def _load_comment(db: AsyncSession, comment_id: uuid.UUID) -> CommunityComment:
    comment = (
        await db.execute(
            select(CommunityComment)
            .where(CommunityComment.id == comment_id)
            .options(selectinload(CommunityComment.author))
        )
    ).scalar_one_or_none()
    if comment is None:
        raise NotFoundError("COMMENT_NOT_FOUND", "Сэтгэгдэл олдсонгүй. Устгагдсан байж магадгүй.")
    return comment


async def delete_comment(db: AsyncSession, comment_id: uuid.UUID, user: User) -> None:
    comment = await _load_comment(db, comment_id)
    _ensure_can_delete(comment.author_id, user)
    await db.execute(delete(CommunityComment).where(CommunityComment.id == comment_id))
    await db.commit()


def _quote(text: str) -> str:
    text = text.strip()
    if len(text) <= _REPORT_QUOTE_LENGTH:
        return text
    return text[:_REPORT_QUOTE_LENGTH] + "…"


def _report_message(target: str, payload: ReportCreate, context: list[str], quote: str) -> str:
    lines = [f"Гомдол · {target} · {_REPORT_REASONS[payload.reason]}"]
    if payload.details:
        lines.append(f"Тайлбар: {payload.details}")
    return "\n".join([*lines, "", *context, "", _quote(quote)])


async def _save_report(db: AsyncSession, user: User, message: str, page: str) -> None:
    db.add(Feedback(user_id=user.id, kind=FeedbackKind.REPORT, message=message, page=page))
    await db.commit()


async def report_post(
    db: AsyncSession, post_id: uuid.UUID, user: User, payload: ReportCreate
) -> None:
    await community_moderation.ensure_can_participate(db, user)
    post = (
        await db.execute(
            select(CommunityPost)
            .where(CommunityPost.id == post_id)
            .options(selectinload(CommunityPost.author))
        )
    ).scalar_one_or_none()
    if post is None:
        raise _post_not_found()
    author = post.author.name if post.author else OFFICIAL_AUTHOR
    message = _report_message(
        "Нийтлэл", payload, [f"Зохиогч: {author}", f"Нийтлэл: «{post.title}»"], post.body
    )
    await _save_report(db, user, message, f"/community/{post.id}")


async def report_comment(
    db: AsyncSession, comment_id: uuid.UUID, user: User, payload: ReportCreate
) -> None:
    await community_moderation.ensure_can_participate(db, user)
    comment = await _load_comment(db, comment_id)
    title = (
        await db.execute(select(CommunityPost.title).where(CommunityPost.id == comment.post_id))
    ).scalar_one()
    message = _report_message(
        "Сэтгэгдэл",
        payload,
        [f"Зохиогч: {comment.author.name}", f"Нийтлэл: «{title}»"],
        comment.body,
    )
    await _save_report(db, user, message, f"/community/{comment.post_id}#comment-{comment.id}")
