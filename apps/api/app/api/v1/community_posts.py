"""Community — нийтлэл, сэтгэгдэл, лайк, гомдол, дүрэм ба түдгэлзүүлэлт.

Зөвхөн нэвтэрсэн хэрэглэгчид. Түдгэлзүүлэлтийг зөвхөн админ удирдана.
"""

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from app.core import rate_limit
from app.core.config import settings
from app.core.deps import AdminUser, CurrentUser, DbSession
from app.models.enums import PostLanguage, PostType
from app.schemas.common import MessageResponse, Page
from app.schemas.community_post import (
    CommentCreate,
    CommentItem,
    CommunityStatus,
    LikeResult,
    PostCreate,
    PostDetail,
    PostSummary,
    ReportCreate,
    SuspensionCreate,
    SuspensionItem,
)
from app.services import community_moderation, community_post_service

router = APIRouter(prefix="/community", tags=["community"])
admin_router = APIRouter(prefix="/admin/community", tags=["admin"])


async def limit_posts(user: CurrentUser) -> None:
    rate_limit.enforce(
        f"community-post:{user.id}",
        settings.community_post_rate_limit_max,
        settings.community_post_rate_limit_window_seconds,
    )


async def limit_comments(user: CurrentUser) -> None:
    rate_limit.enforce(
        f"community-comment:{user.id}",
        settings.community_comment_rate_limit_max,
        settings.community_comment_rate_limit_window_seconds,
    )


async def limit_reports(user: CurrentUser) -> None:
    """Гомдол нь санал хүсэлт болж хадгалагдана — нэг хязгаарыг хуваалцана."""
    rate_limit.enforce(
        f"feedback:{user.id}",
        settings.feedback_rate_limit_max,
        settings.feedback_rate_limit_window_seconds,
    )


REPORTED = "Баярлалаа! Админ шалгаж үзнэ."


@router.get("/me", response_model=CommunityStatus)
async def my_status(db: DbSession, user: CurrentUser) -> CommunityStatus:
    """Дүрмийг зөвшөөрсөн эсэх, идэвхтэй түдгэлзүүлэлт, түдгэлзүүлэх шатлал."""
    return await community_moderation.status(db, user)


@router.post("/guidelines", response_model=CommunityStatus)
async def accept_guidelines(db: DbSession, user: CurrentUser) -> CommunityStatus:
    """Эхний удаа ороход харуулсан дүрмийг зөвшөөрнө. Давтан дуудсан ч аюулгүй."""
    return await community_moderation.accept_guidelines(db, user)


@router.get("/posts", response_model=Page[PostSummary])
async def list_posts(
    db: DbSession,
    user: CurrentUser,
    language: PostLanguage | None = None,
    type_: Annotated[PostType | None, Query(alias="type")] = None,
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=community_post_service.MAX_PAGE_SIZE)] = (
        community_post_service.DEFAULT_PAGE_SIZE
    ),
) -> Page[PostSummary]:
    items, total = await community_post_service.list_posts(
        db, user, language=language, type_=type_, page=page, page_size=page_size
    )
    return Page[PostSummary](
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=max(1, -(-total // page_size)),
    )


@router.post(
    "/posts",
    response_model=PostDetail,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(limit_posts)],
)
async def create_post(payload: PostCreate, db: DbSession, user: CurrentUser) -> PostDetail:
    return await community_post_service.create_post(db, user, payload)


@router.get("/posts/{post_id}", response_model=PostDetail)
async def get_post(post_id: uuid.UUID, db: DbSession, user: CurrentUser) -> PostDetail:
    return await community_post_service.get_post(db, post_id, user)


@router.delete("/posts/{post_id}", response_model=MessageResponse)
async def delete_post(post_id: uuid.UUID, db: DbSession, user: CurrentUser) -> MessageResponse:
    """Зохиогч эсвэл админ. Сэтгэгдэл, лайк нь хамт устана."""
    await community_post_service.delete_post(db, post_id, user)
    return MessageResponse(message="Нийтлэл устгагдлаа.")


@router.put("/posts/{post_id}/like", response_model=LikeResult)
async def like_post(post_id: uuid.UUID, db: DbSession, user: CurrentUser) -> LikeResult:
    return await community_post_service.set_like(db, post_id, user, liked=True)


@router.delete("/posts/{post_id}/like", response_model=LikeResult)
async def unlike_post(post_id: uuid.UUID, db: DbSession, user: CurrentUser) -> LikeResult:
    return await community_post_service.set_like(db, post_id, user, liked=False)


@router.post(
    "/posts/{post_id}/comments",
    response_model=CommentItem,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(limit_comments)],
)
async def add_comment(
    post_id: uuid.UUID, payload: CommentCreate, db: DbSession, user: CurrentUser
) -> CommentItem:
    return await community_post_service.add_comment(db, post_id, user, payload)


@router.delete("/comments/{comment_id}", response_model=MessageResponse)
async def delete_comment(
    comment_id: uuid.UUID, db: DbSession, user: CurrentUser
) -> MessageResponse:
    """Зохиогч эсвэл админ."""
    await community_post_service.delete_comment(db, comment_id, user)
    return MessageResponse(message="Сэтгэгдэл устгагдлаа.")


@router.post(
    "/posts/{post_id}/report",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(limit_reports)],
)
async def report_post(
    post_id: uuid.UUID, payload: ReportCreate, db: DbSession, user: CurrentUser
) -> MessageResponse:
    """Админы «Санал хүсэлт» хуудсанд `report` төрлөөр очно."""
    await community_post_service.report_post(db, post_id, user, payload)
    return MessageResponse(message=REPORTED)


@router.post(
    "/comments/{comment_id}/report",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(limit_reports)],
)
async def report_comment(
    comment_id: uuid.UUID, payload: ReportCreate, db: DbSession, user: CurrentUser
) -> MessageResponse:
    await community_post_service.report_comment(db, comment_id, user, payload)
    return MessageResponse(message=REPORTED)


# --- Админ: түдгэлзүүлэлт ------------------------------------------------------


@admin_router.get("/suspensions", response_model=Page[SuspensionItem])
async def list_suspensions(
    db: DbSession,
    _: AdminUser,
    active: bool | None = None,
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=community_moderation.MAX_PAGE_SIZE)] = (
        community_moderation.DEFAULT_PAGE_SIZE
    ),
) -> Page[SuspensionItem]:
    items, total = await community_moderation.list_suspensions(
        db, active=active, page=page, page_size=page_size
    )
    return Page[SuspensionItem](
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=max(1, -(-total // page_size)),
    )


@admin_router.post(
    "/suspensions", response_model=SuspensionItem, status_code=status.HTTP_201_CREATED
)
async def suspend_user(
    payload: SuspensionCreate, db: DbSession, admin: AdminUser
) -> SuspensionItem:
    """Дараагийн шатны хугацаагаар (7 → 14 → 30 хоног, дараа нь бүрмөсөн)."""
    return await community_moderation.suspend(db, admin, payload)


@admin_router.post("/suspensions/{suspension_id}/lift", response_model=SuspensionItem)
async def lift_suspension(suspension_id: uuid.UUID, db: DbSession, _: AdminUser) -> SuspensionItem:
    """Цуцалсан түдгэлзүүлэлт дараагийн удааг тоолоход орохгүй."""
    return await community_moderation.lift(db, suspension_id)
