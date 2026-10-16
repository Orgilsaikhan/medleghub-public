"""Authentication endpoints.

Token нь httpOnly cookie-гоор дамжина — JavaScript-д хүрэхгүй тул XSS-ээр
хулгайлагдах эрсдэлгүй. Response body-д token буцаахгүй.
"""

from typing import Annotated

import httpx
from fastapi import APIRouter, Depends, Response, status

from app.core import rate_limit
from app.core.config import settings
from app.core.deps import CurrentUser, DbSession
from app.core.rate_limit import RateLimiter
from app.core.security import create_access_token
from app.models.user import User
from app.schemas.auth import (
    ChangePasswordRequest,
    EmailRequest,
    LoginRequest,
    RegisterRequest,
    RegisterResponse,
    ResetPasswordRequest,
    UserResponse,
    VerifyEmailRequest,
)
from app.schemas.common import MessageResponse
from app.services import auth_service, email_otp

router = APIRouter(prefix="/auth", tags=["auth"])

AuthClient = Annotated[httpx.AsyncClient, Depends(email_otp.get_auth_client)]

# Frontend-д зориулсан сэжүүр cookie. Нууц утга агуулаагүй, эрх олгодоггүй —
# зөвхөн "магадгүй нэвтэрсэн" гэдгийг JavaScript-д мэдэгдэж, зочин хэрэглэгч
# тутамд `/auth/me` рүү дэмий хүсэлт илгээхээс сэргийлнэ.
SESSION_HINT_COOKIE = "suralts_session"


def _cookie_kwargs() -> dict:
    return {
        "secure": settings.auth_cookie_secure,
        "samesite": settings.auth_cookie_samesite,
        "domain": settings.auth_cookie_domain,
        "path": "/",
    }


def start_session(response: Response, user: User) -> None:
    max_age = settings.jwt_expire_minutes * 60
    response.set_cookie(
        key=settings.auth_cookie_name,
        value=create_access_token(str(user.id), user.role, user.password_version),
        max_age=max_age,
        httponly=True,
        **_cookie_kwargs(),
    )
    response.set_cookie(
        key=SESSION_HINT_COOKIE,
        value="1",
        max_age=max_age,
        httponly=False,
        **_cookie_kwargs(),
    )


def end_session(response: Response) -> None:
    response.delete_cookie(key=settings.auth_cookie_name, httponly=True, **_cookie_kwargs())
    response.delete_cookie(key=SESSION_HINT_COOKIE, httponly=False, **_cookie_kwargs())


def limit_code_sends(email: str) -> None:
    """Нэг имэйл рүү код илгээх давтамж — бусдын имэйлийг спамдахаас сэргийлнэ."""
    rate_limit.enforce(
        f"otp-send:{email}",
        settings.otp_send_rate_limit_max,
        settings.otp_send_rate_limit_window_seconds,
    )


def limit_code_attempts(key: str) -> None:
    """Нэг кодыг таах оролдлого. Supabase бүх хүсэлтийг манай IP-ээс хүлээн авдаг
    тул түүний IP-ийн хязгаар хэрэглэгч тус бүрийг хамгаалахгүй."""
    rate_limit.enforce(
        f"otp-verify:{key}",
        settings.otp_verify_rate_limit_max,
        settings.otp_verify_rate_limit_window_seconds,
    )


@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
async def register(
    payload: RegisterRequest,
    response: Response,
    db: DbSession,
    client: AuthClient,
    _: None = Depends(RateLimiter("auth:register")),
) -> RegisterResponse:
    """Имэйл баталгаажуулалт асаалттай бол код илгээж, нэвтрүүлэхгүй."""
    user, verification_required = await auth_service.register_user(db, client, payload)
    if verification_required:
        return RegisterResponse(verification_required=True, email=user.email)
    start_session(response, user)
    return RegisterResponse(
        verification_required=False, email=user.email, user=UserResponse.model_validate(user)
    )


@router.post("/verify-email", response_model=UserResponse)
async def verify_email(
    payload: VerifyEmailRequest,
    response: Response,
    db: DbSession,
    client: AuthClient,
    _: None = Depends(RateLimiter("auth:otp")),
) -> User:
    limit_code_attempts(payload.email)
    user = await auth_service.verify_email(db, client, payload)
    start_session(response, user)
    return user


@router.post("/verify-email/resend", response_model=MessageResponse)
async def resend_verification(
    payload: EmailRequest,
    db: DbSession,
    client: AuthClient,
    _: None = Depends(RateLimiter("auth:otp")),
) -> MessageResponse:
    limit_code_sends(payload.email)
    await auth_service.resend_verification(db, client, payload.email)
    return MessageResponse(message="Бүртгэл баталгаажаагүй бол таны имэйл рүү шинэ код илгээлээ.")


@router.post("/password/forgot", response_model=MessageResponse)
async def forgot_password(
    payload: EmailRequest,
    db: DbSession,
    client: AuthClient,
    _: None = Depends(RateLimiter("auth:otp")),
) -> MessageResponse:
    limit_code_sends(payload.email)
    await auth_service.forgot_password(db, client, payload.email)
    return MessageResponse(message="Энэ имэйлээр бүртгэл байвал нууц үг сэргээх код илгээлээ.")


@router.post("/password/reset", response_model=UserResponse)
async def reset_password(
    payload: ResetPasswordRequest,
    response: Response,
    db: DbSession,
    client: AuthClient,
    _: None = Depends(RateLimiter("auth:otp")),
) -> User:
    """Кодоор нууц үг солино. Бусад сесс гарч, энэ төхөөрөмж нэвтэрнэ."""
    limit_code_attempts(payload.email)
    user = await auth_service.reset_password(db, client, payload)
    start_session(response, user)
    return user


@router.post("/login", response_model=UserResponse)
async def login(
    payload: LoginRequest,
    response: Response,
    db: DbSession,
    _: None = Depends(RateLimiter("auth:login")),
) -> User:
    user = await auth_service.authenticate(db, payload)
    start_session(response, user)
    return user


@router.post("/logout", response_model=MessageResponse)
async def logout(response: Response, _: CurrentUser) -> MessageResponse:
    end_session(response)
    return MessageResponse(message="Системээс гарлаа.")


@router.post("/password", response_model=MessageResponse)
async def change_password(
    payload: ChangePasswordRequest,
    response: Response,
    db: DbSession,
    user: CurrentUser,
    _: None = Depends(RateLimiter("auth:password")),
) -> MessageResponse:
    """Нууц үг солих. Бусад төхөөрөмж дээрх сессүүд гарна — энэ сесс шинэ cookie авна."""
    await auth_service.change_password(db, user, payload)
    start_session(response, user)
    return MessageResponse(message="Нууц үг солигдлоо.")


@router.get("/me", response_model=UserResponse)
async def me(user: CurrentUser) -> User:
    return user
