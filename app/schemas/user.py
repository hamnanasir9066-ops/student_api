from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# ==========================================
# Base User
# ==========================================

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    role: str = Field(
        ...,
        pattern="^(admin|teacher|student)$"
    )


# ==========================================
# Create User
# ==========================================

class UserCreate(UserBase):
    password: str = Field(
        ...,
        min_length=8,
        max_length=100
    )

    # Student Fields
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    gender: Optional[str] = None
    date_of_birth: Optional[date] = None
    semester: Optional[int] = None
    cgpa: Optional[float] = 0.0
    address: Optional[str] = None
    department_id: Optional[int] = None
    roll_number: Optional[str] = None


# ==========================================
# Login
# ==========================================

class UserLogin(BaseModel):
    email: EmailStr
    password: str


# ==========================================
# Update User
# ==========================================

class UserUpdate(BaseModel):
    username: Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=100
    )

    email: Optional[EmailStr] = None

    password: Optional[str] = Field(
        default=None,
        min_length=8,
        max_length=100
    )

    role: Optional[str] = None
    is_active: Optional[bool] = None


# ==========================================
# Change Password
# ==========================================

class UserPasswordUpdate(BaseModel):
    new_password: str = Field(
        ...,
        min_length=8,
        max_length=100
    )


# ==========================================
# Response
# ==========================================

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)