from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.enums.fee_status import FeeStatus


# ==========================
# Base Schema
# ==========================

class FeeBase(BaseModel):

    amount: float = Field(
        ...,
        gt=0
    )

    due_date: date

    paid_date: Optional[date] = None

    status: FeeStatus = FeeStatus.PENDING


# ==========================
# Create Schema
# ==========================

class FeeCreate(FeeBase):

    student_id: int


# ==========================
# Update Schema
# ==========================

class FeeUpdate(BaseModel):

    amount: Optional[float] = Field(
        default=None,
        gt=0
    )

    due_date: Optional[date] = None

    paid_date: Optional[date] = None

    status: Optional[FeeStatus] = None


# ==========================
# Response Schema
# ==========================

class FeeResponse(FeeBase):

    id: int

    student_id: int

    class Config:
        orm_mode = True
        from_attributes = True