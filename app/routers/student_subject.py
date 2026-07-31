from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.enums.user_role import UserRole
from app.models.user import User
from app.schemas.student_subject import (
    StudentSubjectCreate,
    StudentSubjectResponse
)
from app.services import student_service, student_subject_service
from app.utils.oauth2 import get_current_user, require_roles

router = APIRouter()

# Permissions
allow_admin = require_roles(UserRole.ADMIN)
allow_staff = require_roles(UserRole.ADMIN, UserRole.TEACHER)


# ==========================================
# Get Own Enrolled Subjects (Student Self-Service)
# ==========================================

@router.get(
    "/me",
    response_model=list[StudentSubjectResponse],
    summary="Get enrolled subjects for logged-in student"
)
def get_own_enrollments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Returns all subjects assigned to the logged-in student.
    """
    student = student_service.get_student_by_user_id(current_user.id, db)
    return student_subject_service.get_enrollments_by_student_id(student.id, db)


# ==========================================
# Get All Enrollments (Admin & Teacher)
# ==========================================

@router.get(
    "/",
    response_model=list[StudentSubjectResponse],
    summary="Get all enrollments"
)
def get_all_enrollments(
    db: Session = Depends(get_db),
    current_user: User = Depends(allow_staff)
):
    """
    Retrieves all course enrollments. Accessible by Admin and Teacher.
    """
    return student_subject_service.get_all_student_subjects(db)


# ==========================================
# Get Enrollment By ID (Admin & Teacher)
# ==========================================

@router.get(
    "/{enrollment_id}",
    response_model=StudentSubjectResponse,
    summary="Get enrollment by ID"
)
def get_enrollment(
    enrollment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(allow_staff)
):
    """
    Retrieves a specific enrollment record. Accessible by Admin and Teacher.
    """
    return student_subject_service.get_student_subject_by_id(
        enrollment_id,
        db
    )


# ==========================================
# Enroll Student / Assign Subject (Admin Only)
# ==========================================

@router.post(
    "/",
    response_model=StudentSubjectResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Assign subject to student"
)
def enroll_student(
    enrollment: StudentSubjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(allow_admin)
):
    """
    Assigns a subject to a student. Admin access only.
    """
    return student_subject_service.enroll_student(
        enrollment,
        db
    )


# ==========================================
# Delete Enrollment (Admin Only)
# ==========================================

@router.delete(
    "/{enrollment_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete enrollment"
)
def delete_enrollment(
    enrollment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(allow_admin)
):
    """
    Removes a subject enrollment. Admin access only.
    """
    return student_subject_service.delete_enrollment(
        enrollment_id,
        db
    )