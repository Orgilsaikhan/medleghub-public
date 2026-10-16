"""Live-ийн алдааны код ба монгол мессеж.

HTTP алдаа нь `AppError` (`{"detail": {"code", "message"}}`). Цаана бүтэлгүйтсэн
материал, үүсгэлтийн `error_code` нь ижил кодыг хэрэглэж, мессежийг
`message_for()`-оор API-ийн хариунд нэмнэ.
"""

from fastapi import status

from app.core.config import settings
from app.core.errors import AppError

MESSAGES: dict[str, str] = {
    "LIVE_NOT_FOUND": "Олдсонгүй.",
    "LIVE_PLAN_REQUIRED": (
        "Medleghub Live нь Standard болон Premium багцтай хэрэглэгчдэд зориулагдсан. Нэг "
        "материалыг нэг удаагийн эрхээр ч судалж болно."
    ),
    "LIVE_PASS_USED": (
        "Нэг удаагийн эрхээ ашигласан байна. Шинэ эрх авах эсвэл Standard багцаар үргэлжлүүлнэ үү."
    ),
    "LIVE_PASS_QUOTA_EXCEEDED": (
        "Энэ материалын AI хэрэглээ дууслаа. Бэлэн болсон заавар, карт, тест хэвээр. "
        "Standard багцаар үргэлжлүүлнэ үү."
    ),
    "LIVE_DOCUMENT_LIMIT": (
        "Энэ сард боловсруулах материалын хязгаарт хүрлээ. Дараагийн сарын 1-нд шинэчлэгдэнэ."
    ),
    "LIVE_QUOTA_EXCEEDED": (
        "Энэ сарын AI хэрэглээний хязгаарт хүрлээ. Дараагийн сарын 1-нд шинэчлэгдэнэ."
    ),
    "LIVE_AI_PAUSED": "AI боловсруулалт түр зогссон. Таны материалууд хадгалагдсан.",
    "LIVE_AI_NOT_CONFIGURED": "AI тохиргоо хийгдээгүй байна.",
    "LIVE_STORAGE_NOT_CONFIGURED": "Файлын сан тохируулагдаагүй байна.",
    "LIVE_STORAGE_FAILED": "Файлыг хадгалж чадсангүй. Дахин оролдоно уу.",
    "LIVE_FILE_TOO_LARGE": "Файл {max_mb} MB-аас их байна.",
    "LIVE_FILE_UNSUPPORTED": (
        "Энэ төрлийн файлыг хүлээж авахгүй. PDF, PPTX, DOCX, TXT, MD эсвэл зураг "
        "(PNG, JPG, WEBP) оруулна уу."
    ),
    "LIVE_FILE_MISMATCH": "Файлын агуулга өргөтгөлтэйгөө таарахгүй байна.",
    "LIVE_FILE_EMPTY": "Файл хоосон байна.",
    "LIVE_FILE_ENCRYPTED": (
        "Файл нууц үгээр хамгаалагдсан байна. Хамгаалалтгүй хувилбарыг оруулна уу."
    ),
    "LIVE_FILE_MACRO": (
        "Макро агуулсан файл (.pptm, .docm) хүлээж авахгүй. Энгийн .pptx, .docx эсвэл PDF "
        "болгоод оруулна уу."
    ),
    "LIVE_FILE_LEGACY": (
        "Хуучин .ppt, .doc форматыг дэмжихгүй. .pptx, .docx эсвэл PDF болгож хадгалаад оруулна уу."
    ),
    "LIVE_FILE_CORRUPT": (
        "Файлыг уншиж чадсангүй. Файл эвдэрсэн эсвэл өргөтгөл нь агуулгатайгаа таарахгүй байна."
    ),
    "LIVE_FILE_TOO_COMPLEX": "Файлыг задлахад хэт удлаа. Жижиг хэсгүүдэд хувааж оруулна уу.",
    "LIVE_TOO_MANY_PAGES": "Материал {max_pages} хуудаснаас их байна. Хэсэгчлэн оруулна уу.",
    "LIVE_EMPTY_DOCUMENT": "Материалаас судлах агуулга олдсонгүй.",
    "LIVE_EXTRACTOR_UNAVAILABLE": "Файл задлах үйлчилгээ түр ажиллахгүй байна. Дахин оролдоно уу.",
    "LIVE_AI_FAILED": "AI боловсруулж чадсангүй. Дахин оролдоно уу.",
    "LIVE_AI_BUSY": (
        "AI үйлчилгээ (Google Gemini) одоо хэт ачаалалтай байна. Хэдэн минутын дараа дахин "
        "оролдоно уу."
    ),
    "LIVE_AI_OUTPUT_INVALID": "AI-ийн хариу бүрэн ирсэнгүй. Дахин оролдоно уу.",
    "LIVE_AI_TOO_LONG": "Материал AI-д хэт урт байна. Хэсэгчлэн оруулна уу.",
    "LIVE_INTERRUPTED": "Боловсруулалт тасалдсан. Дахин оролдоно уу.",
    "LIVE_UPLOAD_MISSING": "Файл бүрэн ирээгүй байна. Дахин оруулна уу.",
    "LIVE_MATERIAL_NOT_READY": "Материал хараахан бэлэн болоогүй байна.",
    "LIVE_ALREADY_UPLOADED": "Энэ материалын файл аль хэдийн ирсэн.",
    "LIVE_NOT_RETRYABLE": "Зөвхөн амжилтгүй болсон боловсруулалтыг дахин эхлүүлнэ.",
    "LIVE_ALREADY_ANSWERED": "Энэ асуултад аль хэдийн хариулсан.",
    "LIVE_ATTEMPT_FINISHED": "Энэ оролдлого дууссан.",
    "LIVE_BAD_TOPIC": "Сэдэв буруу байна.",
    "LIVE_BAD_CHOICE": "Хариултын сонголт буруу байна.",
    "LIVE_ADMIN_ALWAYS_PREMIUM": "Админ Premium-ийн бүх эрхтэй — олгох шаардлагагүй.",
}


def message_for(code: str | None, **values: object) -> str | None:
    if code is None:
        return None
    template = MESSAGES.get(code, MESSAGES["LIVE_AI_FAILED"])
    defaults: dict[str, object] = {
        "max_mb": settings.live_max_upload_bytes // 1_000_000,
        "max_pages": settings.live_max_pages,
    }
    return template.format(**{**defaults, **values})


def live_error(status_code: int, code: str, **values: object) -> AppError:
    return AppError(status_code, code, message_for(code, **values) or code)


def not_found() -> AppError:
    return live_error(status.HTTP_404_NOT_FOUND, "LIVE_NOT_FOUND")
