from typing import Optional

# pyrefly: ignore [missing-import]
from pydantic import BaseModel, ConfigDict, Field
from app.enums.grade import Grade


# ==========================
# Base Schema
# ==========================

class MarkBase(BaseModel):

    quiz: float = Field(
        default=0,
        ge=0,
        le=10
    )

    assignment: float = Field(
        default=0,
        ge=0,
        le=20
    )

    midterm: float = Field(
        default=0,
        ge=0,
        le=30
    )

    final: float = Field(
        default=0,
        ge=0,
        le=40
    )


# ==========================
# Create Schema
# ==========================

class MarkCreate(MarkBase):

    student_id: int

    subject_id: int


# ==========================
# Update Schema
# ==========================

class MarkUpdate(BaseModel):

    quiz: Optional[float] = Field(
        default=None,
        ge=0,
        le=10
    )

    assignment: Optional[float] = Field(
        default=None,
        ge=0,
        le=20
    )

    midterm: Optional[float] = Field(
        default=None,
        ge=0,
        le=30
    )

    final: Optional[float] = Field(
        default=None,
        ge=0,
        le=40
    )


# ==========================
# Response Schema
# ==========================

class MarkResponse(MarkBase):

    id: int

    student_id: int

    subject_id: int

    total: float

    grade: str

    class Config:
        orm_mode = True
        from_attributes = True