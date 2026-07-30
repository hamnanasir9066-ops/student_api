from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db

from app.enums.user_role import UserRole
from app.models.user import User
from app.schemas.student import (
    StudentCreate,
    StudentUpdate,
    StudentResponse
)
from app.services import student_service
from app.utils.oauth2 import get_current_user, RoleChecker


router = APIRouter()

# Define role permission instances
allow_admin = RoleChecker([UserRole.ADMIN])
allow_admin_or_teacher = RoleChecker([UserRole.ADMIN, UserRole.TEACHER])


# ==========================================
# Get All Students (Authenticated Users)
# ==========================================

@router.get(
    "/",
    response_model=list[StudentResponse]
)
def get_all_students(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return student_service.get_all_students(db)


# ==========================================
# Get Student By ID (Authenticated Users)
# ==========================================

@router.get(
    "/{student_id}",
    response_model=StudentResponse
)
def get_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return student_service.get_student_by_id(
        student_id,
        db
    )


# ==========================================
# Create Student (Admin & Teacher Only)
# ==========================================

@router.post(
    "/",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(allow_admin_or_teacher)
):
    return student_service.create_student(
        student,
        db
    )


# ==========================================
# Update Student (Admin & Teacher Only)
# ==========================================

@router.put(
    "/{student_id}",
    response_model=StudentResponse
)
def update_student(
    student_id: int,
    student: StudentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(allow_admin_or_teacher)
):
    return student_service.update_student(
        student_id,
        student,
        db
    )


# ==========================================
# Delete Student (Admin Only)
# ==========================================

@router.delete(
    "/{student_id}",
    status_code=status.HTTP_200_OK
)
def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(allow_admin)
):
    return student_service.delete_student(
        student_id,
        db
    )