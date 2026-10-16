"""Seed-ээр үүсгэх промо кодууд.

`python -m app.seed` нь кодыг ЗӨВХӨН байхгүй үед нэмнэ — админ `/admin/promo`
дээр хугацааг нь сунгасан, идэвхгүй болгосныг дарж бичихгүй. Кодыг энд
хассан ч өгөгдлийн сангаас устахгүй (админ идэвхгүй болгоно).
"""

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from app.models.enums import PromoKind

ULAANBAATAR = timezone(timedelta(hours=8))


@dataclass(frozen=True)
class SeedPromoCode:
    code: str
    kind: PromoKind
    percent_off: int | None = None
    free_months: int | None = None
    expires_at: datetime | None = None
    max_uses: int | None = None
    note: str | None = None


SEED_PROMO_CODES = (
    SeedPromoCode(
        code="HELLOWORLD2026",
        kind=PromoKind.PERCENT,
        percent_off=20,
        # 2026 оны сүүлийн өдрийн төгсгөл, Улаанбаатарын цагаар.
        expires_at=datetime(2026, 12, 31, 23, 59, 59, tzinfo=ULAANBAATAR),
        note="Нээлтийн промо код — 20% хөнгөлөлт.",
    ),
)
