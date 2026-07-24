from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict
from app.enums.attendance_status import AttendanceStatus


# ==========================
# Base Schema
# ==========================

class AttendanceBase(BaseModel):

    date: date

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

    date: Optional[date] = None

    status: Optional[AttendanceStatus] = None


# ==========================
# Response Schema
# ==========================

class AttendanceResponse(AttendanceBase):

    id: int

    student_id: int

    subject_id: int

    model_config = ConfigDict(from_attributes=True)