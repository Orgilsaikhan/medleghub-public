"""Нэгдсэн алдааны төрлүүд.

Бүх алдаа `{"detail": {"code": ..., "message": ...}}` хэлбэртэй буцна.
`code` нь frontend-д логик бичихэд, `message` нь хэрэглэгчид харуулахад.
"""

from fastapi import HTTPException, status


class AppError(HTTPException):
    """Бизнес логикийн алдаа. Мессеж нь монгол хэл дээр, хэрэглэгчид харагдана."""

    def __init__(
        self,
        status_code: int,
        code: str,
        message: str,
        headers: dict[str, str] | None = None,
    ) -> None:
        super().__init__(
            status_code=status_code,
            detail={"code": code, "message": message},
            headers=headers,
        )


class NotFoundError(AppError):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(status.HTTP_404_NOT_FOUND, code, message)


class ConflictError(AppError):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(status.HTTP_409_CONFLICT, code, message)


class BadRequestError(AppError):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(status.HTTP_400_BAD_REQUEST, code, message)


class UnauthorizedError(AppError):
    def __init__(
        self,
        code: str = "NOT_AUTHENTICATED",
        message: str = "Нэвтэрнэ үү.",
    ) -> None:
        super().__init__(status.HTTP_401_UNAUTHORIZED, code, message)


class ForbiddenError(AppError):
    def __init__(
        self,
        code: str = "FORBIDDEN",
        message: str = "Танд энэ үйлдлийг хийх эрх байхгүй.",
    ) -> None:
        super().__init__(status.HTTP_403_FORBIDDEN, code, message)


class PaymentRequiredError(AppError):
    """Төлбөрт хичээл — Standard багц шаардлагатай."""

    def __init__(self) -> None:
        super().__init__(
            status.HTTP_402_PAYMENT_REQUIRED,
            "PLAN_REQUIRED",
            "Энэ хичээлийг үзэхийн тулд Standard багц идэвхжүүлнэ үү.",
        )


class RateLimitError(AppError):
    def __init__(self, retry_after: int) -> None:
        super().__init__(
            status.HTTP_429_TOO_MANY_REQUESTS,
            "RATE_LIMITED",
            "Хэт олон хүсэлт илгээлээ. Түр хүлээнэ үү.",
            headers={"Retry-After": str(retry_after)},
        )
