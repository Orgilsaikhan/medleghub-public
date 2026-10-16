"""Enrollment болон ахицын endpoint-ууд."""

import uuid

from fastapi import APIRouter, status

from app.core.deps import CurrentUser, DbSession
from app.schemas.course import CourseProgress
from app.schemas.progress import (
    CaseAnswerRequest,
    CaseAnswerResponse,
    EnrollmentResponse,
    LessonCompleteResponse,
    MyCourse,
)
from app.services import badge_service, case_service, lesson_service, progress_service

router = APIRouter(tags=["progress"])


@router.post(
    "/courses/{course_id}/enroll",
    response_model=EnrollmentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def enroll(course_id: uuid.UUID, db: DbSession, user: CurrentUser) -> EnrollmentResponse:
    return await progress_service.enroll(db, user, course_id)


@router.get("/me/courses", response_model=list[MyCourse])
async def my_courses(db: DbSession, user: CurrentUser) -> list[MyCourse]:
    return await progress_service.my_courses(db, user)


@router.post("/lessons/{lesson_id}/complete", response_model=LessonCompleteResponse)
async def complete_lesson(
    lesson_id: uuid.UUID, db: DbSession, user: CurrentUser
) -> LessonCompleteResponse:
    """Хичээлийг дууссан гэж тэмдэглэнэ.

    Сервер нь хичээл нийтлэгдсэн эсэх, хэрэглэгч сургалтад бүртгүүлсэн эсэхийг
    шалгана — client-ийн мэдээлэлд түшиглэхгүй. Дахин дуудахад төлөв хэвээр.
    """
    lesson = await lesson_service.get_lesson_or_404(db, lesson_id)
    await lesson_service.assert_lesson_accessible(db, lesson, user)
    record, course_id = await progress_service.complete_lesson(db, user, lesson)
    return LessonCompleteResponse(
        lesson_id=lesson.id,
        completed=record.completed,
        completed_at=record.completed_at,
        course_progress=await progress_service.course_progress(db, user, course_id),
        new_badges=await badge_service.sync_badges(db, user),
    )


@router.post("/lessons/{lesson_id}/answer", response_model=CaseAnswerResponse)
async def answer_case(
    lesson_id: uuid.UUID, payload: CaseAnswerRequest, db: DbSession, user: CurrentUser
) -> CaseAnswerResponse:
    """Мөрдөгчийн хэргийн хариултыг шалгана.

    Зөв хариулт хөтөчид хэзээ ч очдоггүй — зөвхөн энд харьцуулна. Зөв бөгөөд
    сурагч бүртгүүлсэн бол хичээл дуусна (`/complete`-тэй ижил: ахиц, тэмдэг).
    """
    lesson = await lesson_service.get_lesson_or_404(db, lesson_id)
    correct, course_id = await case_service.check_answer(db, lesson, user, payload.answer)
    if course_id is None:
        return CaseAnswerResponse(correct=correct, completed=False)
    await progress_service.complete_lesson(db, user, lesson)
    return CaseAnswerResponse(
        correct=True,
        completed=True,
        course_progress=await progress_service.course_progress(db, user, course_id),
        new_badges=await badge_service.sync_badges(db, user),
    )


@router.get("/courses/{course_id}/progress", response_model=CourseProgress)
async def get_course_progress(
    course_id: uuid.UUID, db: DbSession, user: CurrentUser
) -> CourseProgress:
    return await progress_service.course_progress(db, user, course_id)
