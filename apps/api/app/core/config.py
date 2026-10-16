"""Application configuration.

Бүх нууц утга environment-ээс уншигдана. Кодонд hardcode хийхийг хориглоно.
"""

import json
from functools import lru_cache
from typing import Annotated, Literal

from pydantic import Field, ValidationInfo, field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict

# Загварын анхдагч дараалал (`ai_*_models`) — `ai_provider`-ийн дагуу. Үнэ нь
# `app/services/ai/prices.py`-д. Хүнд ажил хүчтэйгээс, хөнгөн ажил хямдаас эхэлнэ.
HEAVY_MODEL = "gemini-3.8-flash"
LITE_MODEL = "gemini-3.5-flash-lite"
CHEAPEST_MODEL = "gemini-3.1-flash-lite"
HEAVY_CHAIN = (HEAVY_MODEL, LITE_MODEL, CHEAPEST_MODEL)
LIGHT_CHAIN = (LITE_MODEL, CHEAPEST_MODEL, HEAVY_MODEL)
AI_PROVIDERS = ("openrouter", "gemini", "fake")


def default_chain(provider: str, models: tuple[str, ...]) -> list[str]:
    """`openrouter:google/gemini-…` эсвэл `gemini:gemini-…`."""
    prefix = "google/" if provider == "openrouter" else ""
    return [f"{provider}:{prefix}{model}" for model in models]


def resolved_provider(data: dict[str, object]) -> str:
    """`auto` — OpenRouter-ийн түлхүүр байвал OpenRouter, үгүй бол Google-ийн шууд API."""
    provider = str(data.get("ai_provider") or "auto")
    if provider == "auto":
        return "openrouter" if data.get("openrouter_api_key") else "gemini"
    return provider


def _heavy(data: dict[str, object]) -> list[str]:
    return default_chain(resolved_provider(data), HEAVY_CHAIN)


def _light(data: dict[str, object]) -> list[str]:
    return default_chain(resolved_provider(data), LIGHT_CHAIN)


DEFAULT_WHEN_EMPTY = (
    "live_standard_documents_per_month",
    "live_standard_ai_monthly_usd",
    "live_premium_documents_per_month",
    "live_premium_ai_monthly_usd",
    "live_pass_ai_usd",
    "ai_platform_monthly_budget_usd",
    "ai_provider",
    "openrouter_zdr",
)
MODEL_CHAIN_FIELDS = (
    "ai_document_models",
    "ai_guide_models",
    "ai_topic_quiz_models",
    "ai_full_quiz_models",
    "ai_exam_models",
    "ai_models",
)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # --- App ---------------------------------------------------------------
    environment: Literal["development", "test", "production"] = "development"
    app_name: str = "MedlegHub API"
    api_v1_prefix: str = "/api/v1"
    debug: bool = False

    # --- Database ----------------------------------------------------------
    database_url: str = "postgresql+asyncpg://suralts:suralts@localhost:5432/suralts"
    db_echo: bool = False
    db_pool_size: int = 10
    db_max_overflow: int = 20

    # --- Security ----------------------------------------------------------
    # Production дээр заавал .env-ээс дарж бичнэ (доорх validator шалгана).
    jwt_secret: str = "dev-only-insecure-secret-change-me"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60 * 24 * 7  # 7 хоног
    bcrypt_rounds: int = 12

    # --- Auth cookie -------------------------------------------------------
    auth_cookie_name: str = "suralts_token"
    auth_cookie_secure: bool = False
    auth_cookie_samesite: Literal["lax", "strict", "none"] = "lax"
    auth_cookie_domain: str | None = None

    # --- CORS --------------------------------------------------------------
    cors_origins: Annotated[list[str], NoDecode] = Field(
        default_factory=lambda: ["http://localhost:3000"]
    )

    # --- Rate limiting -----------------------------------------------------
    rate_limit_enabled: bool = True
    auth_rate_limit_max: int = 10
    auth_rate_limit_window_seconds: int = 60
    # Cloudflare Worker (medleghub.com) нь `/api/v1` хүсэлтэд зочны жинхэнэ IP-г
    # HMAC-аар гарын үсэг зурж дамжуулна (`app/core/rate_limit.py`,
    # `apps/web/worker/`). Worker-ийн `CLIENT_IP_SECRET`-тэй ИЖИЛ байна. Хоосон бол
    # гарын үсгийг үл тоож, Caddy-ийн харсан TCP хаягаар (Cloudflare) тоолно.
    client_ip_secret: str = ""

    # --- C/C++ хөрвүүлэгч --------------------------------------------------
    # Тусдаа `apps/compiler` үйлчилгээ. API нь кодыг зөвхөн дамжуулна —
    # өөрөө хөрвүүлэхгүй, ажиллуулахгүй.
    compiler_url: str = "http://localhost:8090"
    # Хөрвүүлэгчийн өөрийн хугацаанаас урт — ингэснээр тэр цэвэр 504 буцаана.
    compile_timeout_seconds: float = 30.0
    compile_max_source_bytes: int = 64_000
    compile_rate_limit_max: int = 60
    compile_rate_limit_window_seconds: int = 60

    # --- SQL ажиллуулагч ---------------------------------------------------
    # Тусдаа `apps/sql-runner` үйлчилгээ — MySQL хичээлийн кодыг тусгаарлагдсан
    # сервер дээр ажиллуулна. API нь кодыг зөвхөн дамжуулна.
    sql_runner_url: str = "http://localhost:8091"
    # Ажиллуулагчийн дараалал (10 сек) + ажиллагаа (10 сек)-аас урт — ингэснээр
    # тэр цэвэр 503 эсвэл `timed_out` хариу буцаана.
    sql_run_timeout_seconds: float = 30.0
    sql_run_max_source_bytes: int = 64_000
    sql_run_rate_limit_max: int = 60
    sql_run_rate_limit_window_seconds: int = 60
    # Мөрдөгчийн хэргийн хариулт — нэг хэрэгт 10 минутад. Хүн гараар оролдоход
    # хангалттай, сэжигтнүүдийн жагсаалтыг бүхэлд нь таамаглахад хэтэрхий бага.
    case_answer_rate_limit_max: int = 15
    case_answer_rate_limit_window_seconds: int = 600

    # --- Профайлын зураг ---------------------------------------------------
    avatar_max_upload_bytes: int = 5_000_000
    avatar_rate_limit_max: int = 20
    avatar_rate_limit_window_seconds: int = 600

    # --- Имэйлийн нэг удаагийн код (Supabase Auth) -------------------------
    # Supabase Auth-ийг ЗӨВХӨН имэйлээр код илгээх, шалгахад ашиглана (SMTP,
    # имэйлийн загвар нь Supabase дээр). Нэвтрэлт, хэрэглэгчийн мэдээлэл манай
    # `users` хүснэгтэд хэвээр. URL эсвэл түлхүүр хоосон бол имэйл баталгаажуулалт
    # унтарна (хөгжүүлэлт, CI): бүртгүүлмэгц нэвтэрч, нууц үг сэргээх боломжгүй.
    supabase_url: str = ""
    # Нийтэд ил байж болох publishable (эсвэл хуучин `anon`) түлхүүр.
    supabase_anon_key: str = ""
    # НУУЦ secret (эсвэл хуучин `service_role`) түлхүүр — бүртгэл устгах, имэйл
    # солиход Supabase Auth дахь хуучин бичлэгийг устгана. Хоосон бол тэнд үлдэнэ.
    supabase_service_role_key: str = ""
    supabase_timeout_seconds: float = 15.0
    # Нэг имэйл рүү код илгээх, нэг имэйлийн кодыг шалгах оролдлогын хязгаар.
    otp_send_rate_limit_max: int = 3
    otp_send_rate_limit_window_seconds: int = 600
    otp_verify_rate_limit_max: int = 5
    otp_verify_rate_limit_window_seconds: int = 900

    # --- Бүртгэл устгах ба хадгалах хугацаа -------------------------------
    # Устгах хүсэлтээс хойш бүрмөсөн устгах хүртэлх хугацаа (цуцлах боломжтой).
    account_deletion_delay_seconds: int = 2 * 60 * 60
    # Нууцлалын бодлогод заасан хадгалах хугацаа — `maintenance` ажил мөрдүүлнэ.
    feedback_retention_days: int = 90
    payment_retention_days: int = 365
    # `maintenance` ажил хэр олон удаа ажиллах вэ.
    maintenance_interval_seconds: int = 60

    # --- Санал хүсэлт ------------------------------------------------------
    feedback_rate_limit_max: int = 5
    feedback_rate_limit_window_seconds: int = 3600

    # --- Community ---------------------------------------------------------
    # Хэрэглэгч тус бүрд. Гомдол нь санал хүсэлтийн хязгаарыг хуваалцана.
    community_post_rate_limit_max: int = 5
    community_post_rate_limit_window_seconds: int = 3600
    community_comment_rate_limit_max: int = 30
    community_comment_rate_limit_window_seconds: int = 3600
    # Дүрэм зөрчсөн удаа тутмын түдгэлзүүлэх хоног. Жагсаалт дууссаны дараагийн
    # зөрчил бүрмөсөн. Вэб дүрмийн цонхонд эдгээрийг API-аас уншиж харуулна.
    community_suspension_days: list[int] = [7, 14, 30]

    # --- Standard багц ба Wire төлбөр --------------------------------------
    # https://docs.wire.mn — нэг удаагийн PaymentIntent + hosted checkout.
    # Wire-д автомат сунгалт байхгүй тул төлбөр бүр багцыг нэг сараар сунгана.
    # Анхдагч сарын үнэ — админ `/admin/billing` дээр өөрчилбөл `plan_prices`-ийн
    # сүүлийн мөр давамгайлна.
    plan_price_mnt: int = 24_900
    # Premium-ийн анхдагч сарын үнэ (админ `/admin/billing` дээр өөрчилнө). Premium =
    # Standard + Live-ийн илүү AI хязгаар; Live бүх хэрэглэгчид нээлттэй үед л зарна.
    premium_price_mnt: int = 39_900
    # Нэг удаад 1–`plan_max_months` сар. `plan_free_month_every` сар тутамд
    # 1 сар үнэгүй: 6 сар = 5 сарын үнэ, 12 сар = 10 сарын үнэ.
    plan_max_months: int = 12
    plan_free_month_every: int = 6
    # Админ гараар нэг удаад нэмэх/хасах дээд сар (`POST /billing/grants`) ба
    # `/admin/billing` дээр харуулах гараар хийсэн өөрчлөлтийн тоо.
    plan_max_grant_months: int = 24
    plan_adjustment_history: int = 20
    wire_api_url: str = "https://api.wire.mn"
    # `sk_test_…` эсвэл `sk_live_…`. Хоосон бол төлбөр хүлээн авахгүй (503).
    wire_secret_key: str = ""
    # Webhook endpoint үүсгэхэд нэг л удаа харагдах `whsec_…`. Хоосон бол
    # webhook-ийг хүлээж авахгүй — төлбөрийг буцах хуудас дээрээс шалгана.
    wire_webhook_secret: str = ""
    # Test mode-д `sandbox`. Live-д дашбоардад идэвхжүүлсэн операторуудын id
    # (`qpay`). Live түлхүүртэй үед `sandbox`-ийг хасна (`wire.allowed_operators`);
    # хоосон бол Wire идэвхтэй оператораас автоматаар сонгоно.
    wire_allowed_operators: Annotated[list[str], NoDecode] = Field(
        default_factory=lambda: ["sandbox"]
    )
    wire_timeout_seconds: float = 15.0
    # Төлбөрийн дараа Wire хэрэглэгчийг буцаах frontend-ийн хаяг. Wire зөвхөн
    # HTTPS хаяг хүлээж авдаг — `http://localhost` үед буцах хаяг илгээхгүй.
    site_url: str = "http://localhost:3000"
    checkout_rate_limit_max: int = 10
    checkout_rate_limit_window_seconds: int = 600

    # --- Промо код ба найзаа урих -------------------------------------------
    # Промо кодыг шалгах, идэвхжүүлэх оролдлого хэрэглэгч тус бүрд — кодыг
    # таамаглаж олохоос сэргийлнэ.
    promo_rate_limit_max: int = 10
    promo_rate_limit_window_seconds: int = 600
    # Үнэгүй сарын нэг кодын дээд сар.
    promo_max_free_months: int = 12
    # Урилгын кодоор бүртгүүлсэн шинэ хэрэглэгч нэг төлбөртөө энэ хувийн
    # хөнгөлөлт авна. Промо кодтой нийлэхгүй. Урьсан хүн хөнгөлөлт авахгүй.
    referral_friend_percent_off: int = 10
    # Урьсан найзуудаас `referral_friends_per_reward` нь багц авах бүрд урьсан
    # хүнд `referral_reward_months` сар үнэгүй. Үйлчилгээний нөхцөлийн 10-р
    # хэсэгт эдгээр тоо бичигдсэн — өөрчилбөл хамт шинэчилнэ.
    referral_friends_per_reward: int = 3
    referral_reward_months: int = 1

    # --- MedlegHub Live (AI Study) -----------------------------------------
    # `off` — бүх `/live` зам 404; `admins` — зөвхөн админ (production дээр
    # турших); `all` — нэвтэрсэн бүх хэрэглэгч.
    live_access: Literal["off", "admins", "all"] = "off"
    # Файл задлагч (`apps/extractor`) — PDF, PPTX, DOCX-ийг тусгаарлагдсан
    # контейнерт задлана. API өөрөө итгэлгүй файл задлахгүй.
    extractor_url: str = "http://localhost:8092"
    # Задлагчийн дараалал (20 с) + ажил (45 с)-аас урт — тэр цэвэр алдаа буцаана.
    extractor_timeout_seconds: float = 90.0
    # Эх файлын сан: Cloudflare R2-ийн хувийн bucket (production-д заавал).
    # Хоосон бол хөгжүүлэлт, тестэд `live_storage_dir` хавтас; production-д
    # upload 503 буцаана.
    live_r2_account_id: str = ""
    live_r2_access_key_id: str = ""
    live_r2_secret_access_key: str = ""
    live_r2_bucket: str = ""
    live_r2_timeout_seconds: float = 30.0
    live_storage_dir: str = "var/live-storage"
    # Нэг файлын дээд хэмжээ. Cloudflare Worker хүсэлтийн биеийг санах ойдоо
    # (128 MB) бүтнээр нь барьдаг тул 20 MB-аас бүү өсгө.
    live_max_upload_bytes: int = 20_000_000
    live_max_pages: int = 80
    # PPTX, DOCX, TXT-ийн задалсан текстээс AI руу илгээх дээд хэмжээ.
    live_max_text_chars: int = 400_000
    # Эрх тус бүрийн сарын хязгаар (эзэн 2026-10-01). Live нь зөвхөн Standard,
    # Premium багцтай хэрэглэгчдэд (Premium = Standard дээр илүү AI); багцгүй
    # хэрэглэгчид Live огт нээлттэй биш. AI зардлын сарын хязгаар (USD) бүх ажлын
    # (материал, заавар, тест, таамаг) нийлбэрт үйлчилнэ. Gemini үнэ өөрчлөгдөхөд
    # эдгээрийг (`LIVE_*` орчны хувьсагч) шинэчилнэ. Материалын тоог хэрэглэгчид
    # харуулахгүй — зөвхөн Premium нь хэд дахин их вэ.
    live_standard_documents_per_month: int = 20
    live_standard_ai_monthly_usd: float = 3.0
    live_premium_documents_per_month: int = 60
    live_premium_ai_monthly_usd: float = 7.0
    # Нэг удаагийн Live эрх (эзэн 2026-10-03): багцгүй хэрэглэгч нэг материалыг
    # судална. Анхдагч үнэ — админ `/admin/billing` дээр өөрчилбөл `plan_prices`.
    # Ашиглаагүй эрх хугацаагүй; материалд ашигласнаас хойш `live_pass_access_days`
    # хоног нээлттэй. AI-ийн хязгаар (USD) нь тэр материалын бүх ажлын нийлбэр.
    # Эрх авснаас хойш `live_pass_upgrade_days` хоногийн дотор Standard/Premium
    # авбал эрхийн үнэ тэр төлбөрөөс хасагдана.
    live_pass_price_mnt: int = 4_900
    live_pass_access_days: int = 30
    live_pass_ai_usd: float = 0.75
    live_pass_upgrade_days: int = 7
    # Тестийн асуултын тоо: сэдвийн тест ба бүтэн материалын тест.
    live_topic_quiz_questions: int = 5
    live_full_quiz_questions: int = 15
    # AI ажил захиалах (заавар, тест, таамаг) ба файл оруулах давтамж.
    live_generation_rate_limit_max: int = 30
    live_generation_rate_limit_window_seconds: int = 600
    live_upload_rate_limit_max: int = 10
    live_upload_rate_limit_window_seconds: int = 3600
    # Цаана зэрэг ажиллах AI ажлын тоо ба нэг ажлын оролдлогын дээд тоо.
    live_worker_concurrency: int = 2
    live_job_max_attempts: int = 2

    # --- AI үйлчилгээ ------------------------------------------------------
    # Google Gemini API-ийн түлхүүр. Хоосон бол AI унтарна: материал
    # боловсруулахгүй, 503 `LIVE_AI_NOT_CONFIGURED`.
    gemini_api_key: str = ""
    gemini_api_url: str = "https://generativelanguage.googleapis.com"
    # OpenRouter (https://openrouter.ai) — ижил Gemini загварууд, Google-ийн үнээр
    # (шимтгэл нь кредит худалдан авахад). Google-д виртуал карт ороогүй тул одоохондоо
    # үүгээр (эзэн 2026-10-01). Хоосон бол OpenRouter-ийн загварууд алгасагдана.
    openrouter_api_key: str = ""
    openrouter_api_url: str = "https://openrouter.ai/api/v1"
    # `true` бол зөвхөн мэдээлэл хадгалдаггүй (Zero Data Retention) endpoint руу.
    # Сургалтад ашиглахыг ямагт хориглоно (`data_collection: deny`).
    openrouter_zdr: bool = False
    # Анхдагч загварын дарааллын provider (`ai_*_models` хоосон үед): `openrouter`,
    # `gemini` (Google-ийн шууд API) эсвэл `auto` — OpenRouter-ийн түлхүүр байвал
    # OpenRouter, үгүй бол Gemini.
    ai_provider: Literal["auto", "openrouter", "gemini"] = "auto"
    # Ажил тус бүрийн загварын ДАРААЛАЛ (`provider:model`, таслалаар), `app/services/ai/
    # router.py`. Эхнийх нь үндсэн; тэр хязгаартаа хүрсэн (429), ачаалалтай (503)
    # эсвэл `ai_model_limits`-д ойртсон бол дараагийнх руу шилжинэ. Хөнгөн ажил хямд
    # загвараас, хүнд ажил хүчтэй загвараас эхэлнэ. Хоосон бол тэр ажил унтарна.
    # Загвар бүр `app/services/ai/prices.py`-д үнэтэй байх ёстой. Gemini 2.5
    # загварууд Interactions API дээр 404 өгдөг тул болохгүй.
    ai_document_models: Annotated[list[str], NoDecode] = Field(default_factory=_heavy)
    ai_guide_models: Annotated[list[str], NoDecode] = Field(default_factory=_light)
    ai_topic_quiz_models: Annotated[list[str], NoDecode] = Field(default_factory=_light)
    ai_full_quiz_models: Annotated[list[str], NoDecode] = Field(default_factory=_heavy)
    ai_exam_models: Annotated[list[str], NoDecode] = Field(default_factory=_heavy)
    # Өгвөл БҮХ ажил энэ дарааллыг ашиглана (жишээ нь `fake:local` — түлхүүргүй
    # хуурамч AI, production-д хориотой).
    ai_models: Annotated[list[str], NoDecode] = Field(default_factory=list)
    # Загварын хязгаар (Google AI Studio → Rate limit хуудаснаас): минутын хүсэлт
    # (`rpm`), минутын оролтын токен (`tpm`), 24 цагийн хүсэлт (`rpd`). JSON:
    # `{"gemini:gemini-3.8-flash": {"rpm": 1000, "tpm": 1000000, "rpd": 10000}}`.
    # Өгөөгүй загварыг зөвхөн Google-ийн 429/503 хариугаар хязгаарт хүрсэн гэж үзнэ.
    ai_model_limits: Annotated[dict[str, dict[str, int]], NoDecode] = Field(default_factory=dict)
    # Платформын сарын AI төсөв. 95%-д хүрвэл шинэ AI ажил зогсоно.
    ai_platform_monthly_budget_usd: float = 50.0
    ai_request_retention_days: int = 365

    @field_validator(*DEFAULT_WHEN_EMPTY, mode="before")
    @classmethod
    def _limit_default(cls, value: object, info: ValidationInfo) -> object:
        """Хоосон бол анхдагч — compose тохируулаагүй хувьсагчийг хоосон мөрөөр дамжуулдаг."""
        if isinstance(value, str) and not value.strip():
            return cls.model_fields[str(info.field_name)].get_default(call_default_factory=True)
        return value

    @field_validator(*MODEL_CHAIN_FIELDS, mode="before")
    @classmethod
    def _model_chain(cls, value: object, info: ValidationInfo) -> list[str]:
        """`provider:model` жагсаалт (таслалаар). Буруу бол API эхлэхгүй.

        Хоосон бол анхдагч дараалал — compose тохируулаагүй хувьсагчийг хоосон мөрөөр
        дамжуулдаг. AI-г бүхэлд нь унтраах бол `GEMINI_API_KEY`-г хоосон орхино.
        """
        items = value.split(",") if isinstance(value, str) else list(value or [])  # type: ignore[call-overload]
        chain = [str(item).strip() for item in items if str(item).strip()]
        for route in chain:
            provider, _, model = route.partition(":")
            if provider not in AI_PROVIDERS or not model:
                raise ValueError(
                    "AI загвар `openrouter:<model>`, `gemini:<model>` эсвэл `fake:<нэр>` хэлбэртэй."
                )
        if not chain and info.field_name != "ai_models":
            field = cls.model_fields[str(info.field_name)]
            return field.get_default(call_default_factory=True, validated_data=info.data)
        return chain

    @field_validator("ai_model_limits", mode="before")
    @classmethod
    def _model_limits_json(cls, value: object) -> object:
        if isinstance(value, str):
            return json.loads(value) if value.strip() else {}
        return value

    @field_validator("ai_model_limits")
    @classmethod
    def _model_limits(cls, value: dict[str, dict[str, int]]) -> dict[str, dict[str, int]]:
        for route, limits in value.items():
            if ":" not in route or not set(limits) <= {"rpm", "tpm", "rpd"}:
                raise ValueError('AI_MODEL_LIMITS: `{"gemini:<model>": {"rpm", "tpm", "rpd"}}`.')
        return value

    @field_validator("cors_origins", "wire_allowed_operators", mode="before")
    @classmethod
    def _split_list(cls, value: object) -> object:
        """Жагсаалтыг таслалаар тусгаарлагдсан мөр хэлбэрээр өгөх боломжтой."""
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value

    @property
    def is_production(self) -> bool:
        return self.environment == "production"

    @property
    def email_verification_enabled(self) -> bool:
        return bool(self.supabase_url and self.supabase_anon_key)

    def validate_production_secrets(self) -> None:
        """Production дээр анхдагч нууцтай эхлэхээс сэргийлнэ."""
        if not self.is_production:
            return
        if self.jwt_secret == "dev-only-insecure-secret-change-me" or len(self.jwt_secret) < 32:
            raise RuntimeError(
                "JWT_SECRET production дээр заавал тохируулагдсан, 32+ тэмдэгттэй байх ёстой."
            )
        if not self.auth_cookie_secure:
            raise RuntimeError("AUTH_COOKIE_SECURE production дээр true байх ёстой.")
        if self.client_ip_secret and len(self.client_ip_secret) < 32:
            raise RuntimeError("CLIENT_IP_SECRET тохируулсан бол 32+ тэмдэгттэй байх ёстой.")
        if not self.email_verification_enabled:
            raise RuntimeError(
                "SUPABASE_URL, SUPABASE_ANON_KEY production дээр заавал — имэйл баталгаажуулалт, "
                "нууц үг сэргээх код түүгээр явна."
            )
        # AI-ийн түлхүүр, R2 хоосон байж болно (Live унтарна) — харин хуурамч AI болохгүй.
        routes = [route for name in MODEL_CHAIN_FIELDS for route in getattr(self, name)]
        if any(route.startswith("fake:") for route in routes):
            raise RuntimeError("`fake:` AI загварыг production дээр ашиглахгүй.")


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
