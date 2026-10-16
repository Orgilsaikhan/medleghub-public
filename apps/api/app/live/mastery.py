"""Сэдвийн эзэмшил ба картын давталт (Leitner).

Эзэмшил (0–100) = заавар уншсан **10** + картууд **40** × (дундаж хайрцаг / 4)
+ тест **50** × (сүүлийн тестийн зөв хувь). Вэб энэ томьёог тайлбарлаж харуулдаг
(`mn.live`) — өөрчилбөл хамт шинэчилнэ.

Карт 0–4 хайрцагтай. «Мэднэ» — дараагийн хайрцаг, «Эргэлзсэн» — хайрцаг
хэвээр (хамгийн багадаа 1), хугацааны тал; «Мэдэхгүй» — 0, 1 минутын дараа.
4-р хайрцаг — эзэмшсэн.
"""

from datetime import datetime, timedelta
from typing import Literal

GUIDE_POINTS = 10
CARD_POINTS = 40
QUIZ_POINTS = 50

MAX_BOX = 4
# Хайрцаг тутмын дараагийн давталт хүртэлх хугацаа.
INTERVALS = {
    0: timedelta(minutes=1),
    1: timedelta(days=1),
    2: timedelta(days=3),
    3: timedelta(days=7),
    4: timedelta(days=16),
}

Rating = Literal["again", "hard", "good"]


def mastery(
    *,
    guide_read: bool,
    box_sum: int,
    card_count: int,
    quiz_correct: int | None,
    quiz_total: int | None,
) -> int:
    """`box_sum` — давтсан картуудын хайрцгийн нийлбэр; давтаагүй карт 0."""
    score = GUIDE_POINTS if guide_read else 0
    if card_count:
        score += CARD_POINTS * box_sum / (MAX_BOX * card_count)
    if quiz_total:
        score += QUIZ_POINTS * (quiz_correct or 0) / quiz_total
    return max(0, min(100, round(score)))


def review(box: int, rating: Rating, now: datetime) -> tuple[int, datetime]:
    """Шинэ хайрцаг ба дараагийн давталтын мөч."""
    if rating == "again":
        return 0, now + INTERVALS[0]
    if rating == "hard":
        new_box = max(1, box)
        return new_box, now + max(timedelta(minutes=10), INTERVALS[new_box] / 2)
    new_box = min(MAX_BOX, box + 1)
    return new_box, now + INTERVALS[new_box]
