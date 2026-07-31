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
from app.utils.oauth2 import get_current_user, require_roles

router = APIRouter()

# Role permissions
allow_admin = require_roles(UserRole.ADMIN)
allow_staff = require_roles(UserRole.ADMIN, UserRole.TEACHER)


# ==========================================
# Get Own Student Profile (Student Self-Service)
# ==========================================

@router.get(
    "/me",
    response_model=StudentResponse,
    summary="Get logged-in student profile"
)
def get_own_student_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Returns the student record belonging to the logged-in student.
    """
    return student_service.get_student_by_user_id(current_user.id, db)


# ==========================================
# Get All Students (Admin & Teacher)
# ==========================================

@router.get(
    "/",
    response_model=list[StudentResponse],
    summary="Get all students"
)
def get_all_students(
    db: Session = Depends(get_db),
    current_user: User = Depends(allow_staff)
):
    """
    Retrieves all student records. Accessible by Admin and Teacher.
    """
    return student_service.get_all_students(db)


# ==========================================
# Get Student By ID (Admin & Teacher)
# ==========================================

@router.get(
    "/{student_id}",
    response_model=StudentResponse,
    summary="Get student by ID"
)
def get_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(allow_staff)
):
    """
    Retrieves a student record by ID. Accessible by Admin and Teacher.
    """
    return student_service.get_student_by_id(
        student_id,
        db
    )


# ==========================================
# Create Student (Admin & Teacher)
# ==========================================

@router.post(
    "/",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create student profile"
)
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(allow_staff)
):
    """
    Creates a new student record linked to a user account. Accessible by Admin and Teacher.
    """
    return student_service.create_student(
        student,
        db
    )


# ==========================================
# Update Student (Admin & Teacher)
# ==========================================

@router.put(
    "/{student_id}",
    response_model=StudentResponse,
    summary="Update student profile"
)
def update_student(
    student_id: int,
    student: StudentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(allow_staff)
):
    """
    Updates student record details. Accessible by Admin and Teacher.
    """
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
    status_code=status.HTTP_200_OK,
    summary="Delete student profile"
)
def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(allow_admin)
):
    """
    Deletes a student record. Admin access only (Teachers cannot delete students).
    """
    return student_service.delete_student(
        student_id,
        db
    )