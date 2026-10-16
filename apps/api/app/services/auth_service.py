"""Бүртгэл, нэвтрэлт, имэйл баталгаажуулалт, нууц үг сэргээх логик.

Имэйлийн кодыг Supabase Auth илгээж, шалгадаг (`email_otp`). Баталгаажуулалт
унтраалттай үед (хөгжүүлэлт, CI) бүртгүүлмэгц баталгаажсанд тооцно.
"""

from datetime import UTC, datetime
from functools import lru_cache

import httpx
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.errors import (
    AppError,
    BadRequestError,
    ConflictError,
    ForbiddenError,
    UnauthorizedError,
)
from app.core.security import hash_password, verify_password
from app.models.enums import UserRole
from app.models.referral import Referral
from app.models.user import User
from app.schemas.auth import (
    ChangePasswordRequest,
    LoginRequest,
    RegisterRequest,
    ResetPasswordRequest,
    VerifyEmailRequest,
)
from app.services import email_otp, referral_service


@lru_cache(maxsize=1)
def _dummy_hash() -> str:
    """Хэрэглэгч олдоогүй үед ч bcrypt ажиллуулж, хариу өгөх хугацааг ижил байлгана.

    Ингэснээр хариултын хугацаагаар имэйл бүртгэлтэй эсэхийг таах боломжгүй.
    """
    return hash_password("not-a-real-password")


def _email_taken() -> ConflictError:
    return ConflictError("EMAIL_TAKEN", "Энэ имэйлээр бүртгэл аль хэдийн үүссэн байна.")


def invalid_code() -> BadRequestError:
    return BadRequestError("INVALID_CODE", "Код буруу эсвэл хугацаа нь дууссан байна.")


async def user_by_email(db: AsyncSession, email: str) -> User | None:
    return (await db.execute(select(User).where(User.email == email))).scalar_one_or_none()


async def register_user(
    db: AsyncSession, client: httpx.AsyncClient, payload: RegisterRequest
) -> tuple[User, bool]:
    """Бүртгэл үүсгэнэ. `(хэрэглэгч, код илгээсэн эсэх)`.

    Имэйл аль хэдийн бүртгэлтэй бол — баталгаажаагүй байсан ч — 409. Хэрэв
    баталгаажаагүй бүртгэлийг дахин бүртгүүлэхэд дарж бичвэл өөр хүн эзний
    имэйлээр нууц үгээ тавьж, эзэн кодоо оруулсны дараа уг бүртгэлд нэвтрэх
    боломжтой болно. Эзэн нь «Нууц үгээ мартсан»-аар кодоо авч сэргээнэ.

    Урилгын код оруулсан бол `referrals` мөр үүснэ. Урьсан хүний хөнгөлөлт
    найз имэйлээ баталгаажуулахад идэвхжинэ (баталгаажуулалт унтраалттай бол шууд).
    """
    verify = settings.email_verification_enabled
    now = datetime.now(UTC)
    referrer = None
    if payload.referral_code:
        referrer = await referral_service.find_referrer(db, payload.referral_code)
        if referrer is None:
            raise BadRequestError(
                "INVALID_REFERRAL_CODE",
                "Урилгын код олдсонгүй. Шалгаад дахин оруулна уу, эсвэл хоосон үлдээнэ үү.",
            )
    user = User(
        email=payload.email,
        password_hash=hash_password(payload.password),
        name=payload.name,
        role=UserRole.STUDENT,
        terms_accepted_at=now,
        email_verified_at=None if verify else now,
    )
    db.add(user)
    try:
        await db.flush()
    except IntegrityError as exc:
        await db.rollback()
        raise _email_taken() from exc
    if referrer is not None:
        db.add(
            Referral(
                referrer_id=referrer.id,
                friend_id=user.id,
                signup_confirmed_at=None if verify else now,
            )
        )
    await db.commit()
    await db.refresh(user)
    # Хэрэглэгчийн цэсэнд шууд харагдана. Давхцвал өөр кодоор дахин оролдоно.
    await referral_service.ensure_code(db, user)

    if verify:
        await email_otp.send_code(client, user.email)
    return user, verify


async def authenticate(db: AsyncSession, payload: LoginRequest) -> User:
    user = await user_by_email(db, payload.email)

    password_hash = user.password_hash if user else _dummy_hash()
    password_ok = verify_password(payload.password, password_hash)

    if user is None or not password_ok:
        raise UnauthorizedError("INVALID_CREDENTIALS", "Имэйл эсвэл нууц үг буруу байна.")
    # Нууц үг зөв үед л хэлнэ — эс бөгөөс имэйл бүртгэлтэй эсэх ил болно.
    if settings.email_verification_enabled and user.email_verified_at is None:
        raise ForbiddenError("EMAIL_NOT_VERIFIED", "Имэйл хаягаа кодоор баталгаажуулна уу.")
    return user


async def verify_email(
    db: AsyncSession, client: httpx.AsyncClient, payload: VerifyEmailRequest
) -> User:
    user = await user_by_email(db, payload.email)
    if user is None:
        raise invalid_code()
    if user.email_verified_at is not None:
        raise BadRequestError("ALREADY_VERIFIED", "Имэйл аль хэдийн баталгаажсан. Нэвтэрнэ үү.")
    if not await email_otp.verify_code(client, user.email, payload.code):
        raise invalid_code()
    user.email_verified_at = datetime.now(UTC)
    await referral_service.confirm_signup(db, user.id)
    await db.commit()
    return user


async def resend_verification(db: AsyncSession, client: httpx.AsyncClient, email: str) -> None:
    """Баталгаажаагүй бүртгэл байвал код дахин илгээнэ. Хариу үргэлж ижил."""
    user = await user_by_email(db, email)
    if user is not None and user.email_verified_at is None:
        await email_otp.send_code(client, user.email)


def _require_email_codes() -> None:
    if not settings.email_verification_enabled:
        raise AppError(
            503, "EMAIL_CODES_UNAVAILABLE", "Имэйлээр код илгээх тохиргоо хийгдээгүй байна."
        )


async def forgot_password(db: AsyncSession, client: httpx.AsyncClient, email: str) -> None:
    """Бүртгэлтэй бол нууц үг сэргээх код илгээнэ. Хариу үргэлж ижил —
    имэйл бүртгэлтэй эсэхийг энэ замаар мэдэх боломжгүй."""
    _require_email_codes()
    user = await user_by_email(db, email)
    if user is not None:
        await email_otp.send_code(client, user.email)


async def reset_password(
    db: AsyncSession, client: httpx.AsyncClient, payload: ResetPasswordRequest
) -> User:
    """Кодыг шалгаж нууц үгийг солино. Бусад бүх сесс хүчингүй болно."""
    _require_email_codes()
    user = await user_by_email(db, payload.email)
    if user is None or not await email_otp.verify_code(client, user.email, payload.code):
        raise invalid_code()
    now = datetime.now(UTC)
    user.password_hash = hash_password(payload.new_password)
    user.password_changed_at = now
    # Кодыг хүлээн авсан нь имэйлийг эзэмшдэгийн баталгаа.
    user.email_verified_at = user.email_verified_at or now
    await referral_service.confirm_signup(db, user.id)
    await db.commit()
    return user


async def change_password(db: AsyncSession, user: User, payload: ChangePasswordRequest) -> None:
    """Одоогийн нууц үгийг шалгаж солино. Бусад бүх сесс хүчингүй болно.

    401 биш 400 — нэвтэрсэн хэвээр, зөвхөн оруулсан нууц үг буруу.
    """
    if not verify_password(payload.current_password, user.password_hash):
        raise BadRequestError("WRONG_PASSWORD", "Одоогийн нууц үг буруу байна.")
    if verify_password(payload.new_password, user.password_hash):
        raise BadRequestError("SAME_PASSWORD", "Шинэ нууц үг одоогийнхоос өөр байх ёстой.")

    user.password_hash = hash_password(payload.new_password)
    # Хувилбар өөрчлөгдөнө — өмнө олгосон token бүр хүчингүй (`deps`).
    user.password_changed_at = datetime.now(UTC)
    await db.commit()
