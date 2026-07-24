from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
)


class UserBase(BaseModel):

    username: str = Field(..., min_length=3, max_length=100)

    email: EmailStr

    role: str = Field(
        ...,
        pattern="^(admin|teacher|student)$"
    )


class UserCreate(UserBase):

    password: str = Field(
        ...,
        min_length=8,
        max_length=100
    )


class UserLogin(BaseModel):

    email: EmailStr

    password: str


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


class UserResponse(UserBase):

    id: int

    is_active: bool

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )