from typing import Optional

# pyrefly: ignore [missing-import]
from pydantic import BaseModel, ConfigDict, Field


# ==========================
# Base Schema
# ==========================

class SubjectBase(BaseModel):

    name: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    code: str = Field(
        ...,
        min_length=2,
        max_length=20
    )

    credit_hours: int = Field(
        ...,
        ge=1,
        le=6
    )


# ==========================
# Create Schema
# ==========================

class SubjectCreate(SubjectBase):

    department_id: int


# ==========================
# Update Schema
# ==========================

class SubjectUpdate(BaseModel):

    name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    code: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=20
    )

    credit_hours: Optional[int] = Field(
        default=None,
        ge=1,
        le=6
    )

    department_id: Optional[int] = None


# ==========================
# Response Schema
# ==========================

class SubjectResponse(SubjectBase):

    id: int

    department_id: int

    class Config:
        orm_mode = True
        from_attributes = True