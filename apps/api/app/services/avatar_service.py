"""Профайлын зураг.

Хэрэглэгчийн илгээсэн файлыг ХЭЗЭЭ Ч шууд хадгалах, буцаахгүй:

1. Хэмжээг уншихын өмнө хязгаарлана (`avatar_max_upload_bytes`).
2. Pillow-оор тайлна — зөвхөн PNG/JPEG/WebP/GIF, пикселийн тоо хязгаартай
   (decompression bomb: жижиг файл нь санах ойд асар том зураг болж задардаг).
3. 256×256 WebP болгон дахин кодлоно. EXIF (GPS байршил гэх мэт) хасагдана,
   SVG/HTML зэрэг «зураг шиг» файл хэзээ ч хөтөчид хүрэхгүй.

Pillow нь CPU ачаалалтай тул event loop-ыг хаахгүйн тулд thread дээр ажиллана.
"""

import hashlib
import io
import uuid

from fastapi import UploadFile
from PIL import Image, ImageOps, UnidentifiedImageError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.concurrency import run_in_threadpool

from app.core.config import settings
from app.core.errors import AppError, BadRequestError
from app.models.avatar import UserAvatar
from app.models.user import User

SIZE = 256
ALLOWED_FORMATS = {"PNG", "JPEG", "WEBP", "GIF"}
# 256px-ийн зураг хийхэд 40 мегапиксель хангалттай — утасны камер ~12–50 MP.
MAX_PIXELS = 40_000_000


def _invalid() -> BadRequestError:
    return BadRequestError(
        "INVALID_IMAGE", "Зургийг уншиж чадсангүй. PNG, JPEG, WebP эсвэл GIF файл оруулна уу."
    )


def normalize(raw: bytes) -> bytes:
    """Дурын дэмжигдсэн зургийг 256×256 WebP болгоно. Буруу бол `INVALID_IMAGE`."""
    Image.MAX_IMAGE_PIXELS = MAX_PIXELS
    try:
        with Image.open(io.BytesIO(raw)) as image:
            if image.format not in ALLOWED_FORMATS:
                raise _invalid()
            if image.width * image.height > MAX_PIXELS:
                raise _invalid()
            image.load()
            # Утасны зураг хажуу тийш эргэсэн харагдахаас сэргийлнэ.
            image = ImageOps.exif_transpose(image)
            image = image.convert("RGBA" if "A" in image.getbands() else "RGB")
            image = ImageOps.fit(image, (SIZE, SIZE), Image.Resampling.LANCZOS)
            out = io.BytesIO()
            image.save(out, "WEBP", quality=85, method=6)
            return out.getvalue()
    except (UnidentifiedImageError, Image.DecompressionBombError, OSError, ValueError) as exc:
        raise _invalid() from exc


async def _read_limited(upload: UploadFile) -> bytes:
    limit = settings.avatar_max_upload_bytes
    raw = await upload.read(limit + 1)
    if len(raw) > limit:
        raise AppError(
            413,
            "IMAGE_TOO_LARGE",
            f"Зураг хэт том байна. {limit // 1_000_000} MB-аас бага файл оруулна уу.",
        )
    if not raw:
        raise _invalid()
    return raw


async def set_avatar(db: AsyncSession, user: User, upload: UploadFile) -> User:
    data = await run_in_threadpool(normalize, await _read_limited(upload))
    avatar = await db.get(UserAvatar, user.id)
    if avatar is None:
        db.add(UserAvatar(user_id=user.id, data=data))
    else:
        avatar.data = data
    user.avatar_key = hashlib.sha256(data).hexdigest()[:16]
    await db.commit()
    await db.refresh(user)
    return user


async def remove_avatar(db: AsyncSession, user: User) -> User:
    avatar = await db.get(UserAvatar, user.id)
    if avatar is not None:
        await db.delete(avatar)
    user.avatar_key = None
    await db.commit()
    await db.refresh(user)
    return user


async def get_avatar(db: AsyncSession, user_id: uuid.UUID) -> bytes | None:
    return (
        await db.execute(select(UserAvatar.data).where(UserAvatar.user_id == user_id))
    ).scalar_one_or_none()
