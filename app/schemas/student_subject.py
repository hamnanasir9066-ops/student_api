from typing import Optional

# pyrefly: ignore [missing-import]
from pydantic import BaseModel, ConfigDict


# ==========================
# Base Schema
# ==========================

class StudentSubjectBase(BaseModel):

    student_id: int

    subject_id: int


# ==========================
# Create Schema
# ==========================

class StudentSubjectCreate(StudentSubjectBase):
    pass


# ==========================
# Update Schema
# ==========================

class StudentSubjectUpdate(BaseModel):

    student_id: Optional[int] = None

    subject_id: Optional[int] = None


# ==========================
# Response Schema
# ==========================

class StudentSubjectResponse(StudentSubjectBase):

    id: int

    class Config:
        orm_mode = True
        from_attributes = True