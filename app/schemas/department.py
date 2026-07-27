from pydantic import BaseModel, ConfigDict, Field
from typing import Optional


# ==========================
# Base Schema
# ==========================

class DepartmentBase(BaseModel):

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

    hod_name: Optional[str] = Field(
        default=None,
        max_length=100
    )


# ==========================
# Create Schema
# ==========================

class DepartmentCreate(DepartmentBase):
    pass


# ==========================
# Update Schema
# ==========================

class DepartmentUpdate(BaseModel):

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

    hod_name: Optional[str] = Field(
        default=None,
        max_length=100
    )


# ==========================
# Response Schema
# ==========================

class DepartmentResponse(DepartmentBase):

    id: int

    class Config:
        orm_mode = True
        from_attributes = True