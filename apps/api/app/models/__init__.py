"""SQLAlchemy models.

Alembic-ийн autogenerate бүх model-ыг олохын тулд энд import хийнэ.
"""

from app.models.ai_request import AIRequest
from app.models.announcement import Announcement
from app.models.avatar import UserAvatar
from app.models.badge import UserBadge
from app.models.community_post import (
    CommunityComment,
    CommunityPost,
    CommunityPostLike,
    CommunitySuspension,
)
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.models.enums import (
    AnnouncementAudience,
    AnnouncementKind,
    Category,
    Difficulty,
    FeedbackKind,
    LessonLanguage,
    PaymentStatus,
    PostLanguage,
    PostType,
    PromoKind,
    UserRole,
)
from app.models.feedback import Feedback
from app.models.lesson import Lesson
from app.models.live import (
    LiveBlobDeletion,
    LiveCard,
    LiveCardProgress,
    LiveGeneration,
    LiveMaterial,
    LivePass,
    LiveQuestion,
    LiveQuizAnswer,
    LiveQuizAttempt,
    LiveSubscription,
    LiveTopic,
    LiveTopicProgress,
)
from app.models.module import Module
from app.models.payment import Payment
from app.models.plan_adjustment import PlanAdjustment
from app.models.plan_price import PlanPrice
from app.models.progress import LessonProgress
from app.models.promo_code import PromoCode, PromoRedemption
from app.models.referral import Referral
from app.models.user import User

__all__ = [
    "AIRequest",
    "Announcement",
    "AnnouncementAudience",
    "AnnouncementKind",
    "Category",
    "CommunityComment",
    "CommunityPost",
    "CommunityPostLike",
    "CommunitySuspension",
    "Course",
    "Difficulty",
    "Enrollment",
    "Feedback",
    "FeedbackKind",
    "Lesson",
    "LessonLanguage",
    "LessonProgress",
    "LiveBlobDeletion",
    "LiveCard",
    "LiveCardProgress",
    "LiveGeneration",
    "LiveMaterial",
    "LivePass",
    "LiveQuestion",
    "LiveQuizAnswer",
    "LiveQuizAttempt",
    "LiveSubscription",
    "LiveTopic",
    "LiveTopicProgress",
    "Module",
    "Payment",
    "PaymentStatus",
    "PlanAdjustment",
    "PlanPrice",
    "PostLanguage",
    "PostType",
    "PromoCode",
    "PromoKind",
    "PromoRedemption",
    "Referral",
    "User",
    "UserAvatar",
    "UserBadge",
    "UserRole",
]
