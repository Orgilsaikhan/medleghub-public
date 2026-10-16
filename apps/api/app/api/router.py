from fastapi import APIRouter

from app.api.v1 import (
    account,
    announcements,
    auth,
    billing,
    community,
    community_posts,
    compiler,
    courses,
    feedback,
    lessons,
    live,
    modules,
    profile,
    progress,
    sql,
)

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(account.router)
api_router.include_router(courses.router)
api_router.include_router(modules.router)
# Lesson router нь `/courses/{slug}` (string) route-ын дараа бүртгэгдэнэ —
# `/courses/{course_slug}/lessons/{lesson_slug}` нь илүү тодорхой зам учир зөрчилгүй.
api_router.include_router(lessons.router)
api_router.include_router(progress.router)
api_router.include_router(profile.router)
api_router.include_router(community.router)
api_router.include_router(community_posts.router)
api_router.include_router(community_posts.admin_router)
api_router.include_router(feedback.router)
api_router.include_router(compiler.router)
api_router.include_router(sql.router)
api_router.include_router(billing.router)
api_router.include_router(announcements.router)
api_router.include_router(live.router)
