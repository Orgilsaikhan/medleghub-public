"""Өөрийн бүртгэл — нэр, профайл нуух, имэйл солих, бүртгэл устгах (2 цагийн дараа)."""

from fastapi import APIRouter, Depends

from app.api.v1.auth import AuthClient, limit_code_attempts
from app.core import rate_limit
from app.core.config import settings
from app.core.deps import CurrentUser, DbSession
from app.core.rate_limit import RateLimiter
from app.models.user import User
from app.schemas.auth import (
    ChangeEmailRequest,
    ChangeEmailResponse,
    ConfirmEmailRequest,
    DeleteAccountRequest,
    UpdateAccountRequest,
    UserResponse,
)
from app.schemas.promo import ReferralSummary
from app.services import account_service, referral_service

router = APIRouter(tags=["account"])


@router.patch("/me", response_model=UserResponse)
async def update_me(payload: UpdateAccountRequest, db: DbSession, user: CurrentUser) -> User:
    return await account_service.update_account(db, user, payload)


@router.get("/me/referral", response_model=ReferralSummary)
async def my_referral(db: DbSession, user: CurrentUser) -> ReferralSummary:
    """Найзаа урих код ба олсон шагнал. Код анх энд үүснэ."""
    return await referral_service.summary(db, user)


@router.post(
    "/me/email",
    response_model=ChangeEmailResponse,
    dependencies=[Depends(RateLimiter("auth:password"))],
)
async def change_email(
    payload: ChangeEmailRequest, db: DbSession, user: CurrentUser, client: AuthClient
) -> ChangeEmailResponse:
    """Нууц үгээ шалгуулна. Баталгаажуулалт асаалттай бол шинэ хаяг руу код илгээнэ."""
    rate_limit.enforce(
        f"otp-send:email-change:{user.id}",
        settings.otp_send_rate_limit_max,
        settings.otp_send_rate_limit_window_seconds,
    )
    sent = await account_service.request_email_change(db, client, user, payload)
    return ChangeEmailResponse(verification_required=sent, user=UserResponse.model_validate(user))


@router.post("/me/email/confirm", response_model=UserResponse)
async def confirm_email(
    payload: ConfirmEmailRequest, db: DbSession, user: CurrentUser, client: AuthClient
) -> User:
    limit_code_attempts(f"email-change:{user.id}")
    return await account_service.confirm_email_change(db, client, user, payload.code)


@router.post(
    "/me/delete",
    response_model=UserResponse,
    dependencies=[Depends(RateLimiter("auth:password"))],
)
async def delete_me(payload: DeleteAccountRequest, db: DbSession, user: CurrentUser) -> User:
    """Бүртгэлийг 2 цагийн дараа бүрмөсөн устгахаар товлоно. Нууц үг шаардлагатай.

    Тэр хүртэл хэрэглэгч нэвтэрсэн хэвээр бөгөөд `POST /me/delete/cancel`-ээр цуцална.
    """
    return await account_service.schedule_deletion(db, user, payload.password)


@router.post("/me/delete/cancel", response_model=UserResponse)
async def cancel_delete_me(db: DbSession, user: CurrentUser) -> User:
    return await account_service.cancel_deletion(db, user)
