"""Хэрэглэгч өөрийн бүртгэлийг удирдах — нэр, профайл нуух, имэйл солих, устгах.

Устгах хүсэлтээс 2 цагийн дараа `maintenance` ажил бүртгэлийг бүрмөсөн устгана.
"""

from datetime import UTC, datetime, timedelta

import httpx
from sqlalchemy import delete, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.errors import BadRequestError, ConflictError
from app.core.security import verify_password
from app.models.feedback import Feedback
from app.models.payment import Payment
from app.models.user import User
from app.schemas.auth import ChangeEmailRequest, UpdateAccountRequest
from app.services import auth_service, email_otp


def _check_password(user: User, password: str) -> None:
    # 401 биш 400 — нэвтэрсэн хэвээр, зөвхөн оруулсан нууц үг буруу.
    if not verify_password(password, user.password_hash):
        raise BadRequestError("WRONG_PASSWORD", "Нууц үг буруу байна.")


def _email_taken() -> ConflictError:
    return ConflictError("EMAIL_TAKEN", "Энэ имэйлээр өөр бүртгэл үүссэн байна.")


async def update_account(db: AsyncSession, user: User, payload: UpdateAccountRequest) -> User:
    if payload.name is not None:
        user.name = payload.name
    if payload.profile_hidden is not None:
        user.profile_hidden = payload.profile_hidden
    if payload.show_motivation is not None:
        user.show_motivation = payload.show_motivation
    if payload.editor_layout is not None:
        user.editor_layout = payload.editor_layout
    await db.commit()
    return user


async def request_email_change(
    db: AsyncSession, client: httpx.AsyncClient, user: User, payload: ChangeEmailRequest
) -> bool:
    """Нууц үгийг шалгана. Баталгаажуулалт асаалттай бол шинэ хаяг руу код
    илгээж `True`, эс бөгөөс имэйлийг шууд сольж `False` буцаана."""
    _check_password(user, payload.password)
    if payload.new_email == user.email:
        raise BadRequestError("SAME_EMAIL", "Шинэ имэйл одоогийнхоос өөр байх ёстой.")
    if await auth_service.user_by_email(db, payload.new_email) is not None:
        raise _email_taken()

    if not settings.email_verification_enabled:
        user.email = payload.new_email
        await _commit_email(db)
        return False

    user.pending_email = payload.new_email
    await db.commit()
    await email_otp.send_code(client, payload.new_email)
    return True


async def confirm_email_change(
    db: AsyncSession, client: httpx.AsyncClient, user: User, code: str
) -> User:
    """Шинэ хаяг руу илгээсэн кодыг шалгаж имэйлийг солино."""
    new_email = user.pending_email
    if not new_email:
        raise BadRequestError("NO_PENDING_EMAIL", "Имэйл солих хүсэлт олдсонгүй.")
    if not await email_otp.verify_code(client, new_email, code):
        raise auth_service.invalid_code()

    old_email = user.email
    user.email = new_email
    user.pending_email = None
    await _commit_email(db)
    await email_otp.delete_identity(client, old_email)
    return user


async def _commit_email(db: AsyncSession) -> None:
    # Хоёр хүн нэг хаягийг зэрэг авах гэвэл unique constraint шийднэ.
    try:
        await db.commit()
    except IntegrityError as exc:
        await db.rollback()
        raise _email_taken() from exc


async def schedule_deletion(db: AsyncSession, user: User, password: str) -> User:
    """Бүртгэлийг `account_deletion_delay_seconds` (2 цаг)-ийн дараа устгахаар
    товлоно. Дахин хүсэхэд хугацааг сунгахгүй — анхны товлол хэвээр."""
    _check_password(user, password)
    if user.deletion_scheduled_at is None:
        user.deletion_scheduled_at = datetime.now(UTC) + timedelta(
            seconds=settings.account_deletion_delay_seconds
        )
        await db.commit()
    return user


async def cancel_deletion(db: AsyncSession, user: User) -> User:
    user.deletion_scheduled_at = None
    await db.commit()
    return user


async def purge_due_accounts(db: AsyncSession, client: httpx.AsyncClient) -> int:
    """Хугацаа нь болсон бүртгэлүүдийг бүрмөсөн устгана. Устгасан тоог буцаана.

    Ахиц, тэмдэг, зураг, санал хүсэлт `ON DELETE CASCADE`-ээр устана. Төлбөрийн
    бүртгэл хэрэглэгчээс салж (`payments.user_id` → NULL) хадгалах хугацаандаа
    үлдэнэ. ORM-ийн cascade биш, өгөгдлийн сангийн дүрмээр устгахын тулд шууд
    DELETE ажиллуулна. Олон процесс зэрэг ажиллуулсан ч аюулгүй.
    """
    rows = await db.execute(
        delete(User)
        .where(User.deletion_scheduled_at <= func.now())
        .returning(User.email, User.pending_email)
    )
    removed = rows.all()
    await db.commit()
    for email, pending_email in removed:
        for address in (email, pending_email):
            if address:
                await email_otp.delete_identity(client, address)
    return len(removed)


async def purge_expired_records(db: AsyncSession) -> tuple[int, int]:
    """Нууцлалын бодлогод заасан хугацаа хэтэрсэн санал хүсэлт, төлбөрийн
    бүртгэлийг устгана. `(санал хүсэлт, төлбөр)` тоо."""
    now = datetime.now(UTC)
    feedback = await db.execute(
        delete(Feedback).where(
            Feedback.created_at < now - timedelta(days=settings.feedback_retention_days)
        )
    )
    payments = await db.execute(
        delete(Payment).where(
            Payment.created_at < now - timedelta(days=settings.payment_retention_days)
        )
    )
    await db.commit()
    return feedback.rowcount, payments.rowcount
