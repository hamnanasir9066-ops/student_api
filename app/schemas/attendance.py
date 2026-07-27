from datetime import date as date_type
from typing import Optional

# pyrefly: ignore [missing-import]
from pydantic import BaseModel, ConfigDict
from app.enums.attendance_status import AttendanceStatus


# ==========================
# Base Schema
# ==========================

class AttendanceBase(BaseModel):

    date: date_type

    status: AttendanceStatus


# ==========================
# Create Schema
# ==========================

class AttendanceCreate(AttendanceBase):

    student_id: int

    subject_id: int


# ==========================
# Update Schema
# ==========================

class AttendanceUpdate(BaseModel):

    date: Optional[date_type] = None

    status: Optional[AttendanceStatus] = None


# ==========================
# Response Schema
# ==========================

class AttendanceResponse(AttendanceBase):

    id: int

    student_id: int

    subject_id: int

    class Config:
        orm_mode = True
        from_attributes = True