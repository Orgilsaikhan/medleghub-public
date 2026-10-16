import uuid
from typing import Annotated

from pydantic import BaseModel, Field, StringConstraints

from app.schemas.common import ORMModel, Position
from app.schemas.lesson import LessonSummary

Title = Annotated[str, StringConstraints(min_length=2, max_length=200, strip_whitespace=True)]


class ModuleWithLessons(ORMModel):
    id: uuid.UUID
    title: str
    description: str
    position: int
    lessons: list[LessonSummary] = Field(default_factory=list)


class ModuleCreate(BaseModel):
    title: Title
    description: str = Field(default="", max_length=2000)
    position: Position = 0


class ModuleUpdate(BaseModel):
    title: Title | None = None
    description: str | None = Field(default=None, max_length=2000)
    position: Position | None = None
