from datetime import date
from typing import Optional

# pyrefly: ignore [missing-import]
from pydantic import BaseModel, Field, ConfigDict


# ==========================
# Base Schema
# ==========================

class StudentBase(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=100)
    last_name: str = Field(..., min_length=2, max_length=100)

    phone: Optional[str] = Field(default=None, max_length=20)

    gender: Optional[str] = Field(default=None)

    date_of_birth: Optional[date] = None

    semester: int = Field(..., ge=1, le=8)

    cgpa: float = Field(default=0.0, ge=0, le=4)

    address: Optional[str] = Field(default=None, max_length=255)


# ==========================
# Create Schema
# ==========================

class StudentCreate(StudentBase):
    user_id: int

    department_id: int

    roll_number: str = Field(
        ...,
        min_length=5,
        max_length=30
    )


# ==========================
# Update Schema
# ==========================

class StudentUpdate(BaseModel):
    first_name: Optional[str] = Field(default=None, min_length=2, max_length=100)

    last_name: Optional[str] = Field(default=None, min_length=2, max_length=100)

    phone: Optional[str] = Field(default=None, max_length=20)

    gender: Optional[str] = None

    date_of_birth: Optional[date] = None

    semester: Optional[int] = Field(default=None, ge=1, le=8)

    cgpa: Optional[float] = Field(default=None, ge=0, le=4)

    address: Optional[str] = Field(default=None, max_length=255)

    department_id: Optional[int] = None


# ==========================
# Response Schema
# ==========================

class StudentResponse(StudentBase):
    id: int

    user_id: int

    department_id: int

    roll_number: str

    class Config:
        orm_mode = True
        from_attributes = True