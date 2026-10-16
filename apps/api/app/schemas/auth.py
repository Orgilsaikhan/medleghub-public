import uuid
from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, EmailStr, Field, StringConstraints, field_validator

from app.models.enums import EditorLayout
from app.schemas.common import ORMModel

Password = Annotated[str, StringConstraints(min_length=8, max_length=72)]
Name = Annotated[str, StringConstraints(min_length=2, max_length=120, strip_whitespace=True)]
# Supabase-ийн имэйл код — анхдагчаар 6 орон, тохиргоогоор 10 хүртэл.
OtpCode = Annotated[str, StringConstraints(pattern=r"^\d{6,10}$", strip_whitespace=True)]


def check_password_strength(value: str) -> str:
    """Дор хаяж нэг үсэг, нэг тоо шаардана."""
    if not any(ch.isalpha() for ch in value) or not any(ch.isdigit() for ch in value):
        raise ValueError("Нууц үг дор хаяж нэг үсэг, нэг тоо агуулсан байх ёстой.")
    return value


def normalize_email(value: str) -> str:
    return value.strip().lower()


class RegisterRequest(BaseModel):
    email: EmailStr = Field(max_length=255)
    password: Password
    name: Name
    # Яг насыг асуухгүй — «Би 16 нас хүрсэн» тэмдэглэгээ. 16 хүрээгүй бол
    # бүртгүүлэхгүй (Үйлчилгээний нөхцөл §2).
    is_16_or_older: bool
    accept_terms: bool
    # Найзын урилгын код (`/register?ref=…`). Заавал биш; буруу бол 400.
    referral_code: str | None = Field(default=None, max_length=64)

    @field_validator("password")
    @classmethod
    def password_strength(cls, value: str) -> str:
        return check_password_strength(value)

    @field_validator("email")
    @classmethod
    def _normalize_email(cls, value: str) -> str:
        return normalize_email(value)

    @field_validator("referral_code")
    @classmethod
    def blank_referral_is_none(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return value.strip() or None

    @field_validator("accept_terms")
    @classmethod
    def terms_accepted(cls, value: bool) -> bool:
        if not value:
            raise ValueError("Үйлчилгээний нөхцөл, Нууцлалын бодлогыг зөвшөөрнө үү.")
        return value

    @field_validator("is_16_or_older")
    @classmethod
    def old_enough(cls, value: bool) -> bool:
        if not value:
            raise ValueError("Бүртгүүлэхийн тулд 16 нас хүрсэн байх ёстой.")
        return value


class EmailRequest(BaseModel):
    email: EmailStr = Field(max_length=255)

    @field_validator("email")
    @classmethod
    def _normalize_email(cls, value: str) -> str:
        return normalize_email(value)


class VerifyEmailRequest(EmailRequest):
    code: OtpCode


class ResetPasswordRequest(EmailRequest):
    code: OtpCode
    new_password: Password

    @field_validator("new_password")
    @classmethod
    def password_strength(cls, value: str) -> str:
        return check_password_strength(value)


CurrentPassword = Annotated[str, StringConstraints(min_length=1, max_length=72)]


class LoginRequest(BaseModel):
    email: EmailStr = Field(max_length=255)
    password: CurrentPassword

    @field_validator("email")
    @classmethod
    def _normalize_email(cls, value: str) -> str:
        return normalize_email(value)


class ChangePasswordRequest(BaseModel):
    current_password: CurrentPassword
    new_password: Password

    @field_validator("new_password")
    @classmethod
    def password_strength(cls, value: str) -> str:
        return check_password_strength(value)


class UserResponse(ORMModel):
    id: uuid.UUID
    email: EmailStr
    name: str
    role: str
    created_at: datetime
    plan_expires_at: datetime | None
    has_plan: bool
    # Профайлын зургийн хувилбар. Зураг: `GET /users/{id}/avatar?v={avatar_key}`.
    avatar_key: str | None
    profile_hidden: bool
    show_motivation: bool
    # Бүртгэл устах мөч (хүсэлт гаргаснаас 2 цагийн дараа). NULL бол хүсэлтгүй.
    deletion_scheduled_at: datetime | None
    # `new` — засварлагч зүүн, заавар баруун; `legacy` — заавар дээр, засварлагч доор.
    editor_layout: str
    # Найзаа урих код — хэрэглэгчийн цэс, профайлд харагдана. Бүртгүүлэхэд үүснэ.
    referral_code: str | None


class RegisterResponse(BaseModel):
    # `True` бол имэйл рүү код илгээсэн — `POST /auth/verify-email` хүртэл
    # нэвтрээгүй. `False` бол (баталгаажуулалт унтраалттай) шууд нэвтэрсэн.
    verification_required: bool
    email: EmailStr
    user: UserResponse | None = None


# --- Өөрийн бүртгэл ----------------------------------------------------------


class UpdateAccountRequest(BaseModel):
    name: Name | None = None
    profile_hidden: bool | None = None
    show_motivation: bool | None = None
    editor_layout: EditorLayout | None = None


class ChangeEmailRequest(BaseModel):
    new_email: EmailStr = Field(max_length=255)
    password: CurrentPassword

    @field_validator("new_email")
    @classmethod
    def _normalize_email(cls, value: str) -> str:
        return normalize_email(value)


class ChangeEmailResponse(BaseModel):
    # `True` бол шинэ хаяг руу код илгээсэн — `POST /me/email/confirm`.
    verification_required: bool
    user: UserResponse


class ConfirmEmailRequest(BaseModel):
    code: OtpCode


class DeleteAccountRequest(BaseModel):
    password: CurrentPassword
