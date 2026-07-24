from typing import Optional

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

    model_config = ConfigDict(
        from_attributes=True
    )