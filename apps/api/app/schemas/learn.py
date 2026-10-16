"""Lesson player-ийн нэгдсэн response.

`/learn/:courseSlug/:lessonSlug` хуудас нэг л дуудлагаар бүх шаардлагатай
өгөгдлөө авна: хичээл, curriculum, ахиц, өмнөх/дараагийн холбоос.
"""

import uuid

from pydantic import BaseModel

from app.schemas.course import CourseProgress
from app.schemas.lesson import LessonDetail, LessonLink
from app.schemas.module import ModuleWithLessons


class LearnCourse(BaseModel):
    id: uuid.UUID
    title: str
    slug: str


class LessonPlayerResponse(BaseModel):
    course: LearnCourse
    lesson: LessonDetail
    modules: list[ModuleWithLessons]
    progress: CourseProgress
    enrolled: bool
    previous_lesson: LessonLink | None = None
    next_lesson: LessonLink | None = None
