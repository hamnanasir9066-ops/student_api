from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.enums.user_role import UserRole
from app.models.user import User
from app.schemas.subject import (
    SubjectCreate,
    SubjectUpdate,
    SubjectResponse
)
from app.services import subject_service
from app.utils.oauth2 import get_current_user, require_roles

router = APIRouter()

# Permissions
allow_admin = require_roles(UserRole.ADMIN)
allow_staff = require_roles(UserRole.ADMIN, UserRole.TEACHER)


# ==========================================
# Get All Subjects (Admin & Teacher)
# ==========================================

@router.get(
    "/",
    response_model=list[SubjectResponse],
    summary="Get all subjects"
)
def get_all_subjects(
    db: Session = Depends(get_db),
    current_user: User = Depends(allow_staff)
):
    """
    Retrieves all course subjects. Accessible by Admin and Teacher.
    """
    return subject_service.get_all_subjects(db)


# ==========================================
# Get Subject By ID (Admin & Teacher)
# ==========================================

@router.get(
    "/{subject_id}",
    response_model=SubjectResponse,
    summary="Get subject by ID"
)
def get_subject(
    subject_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(allow_staff)
):
    """
    Retrieves a subject by ID. Accessible by Admin and Teacher.
    """
    return subject_service.get_subject_by_id(
        subject_id,
        db
    )


# ==========================================
# Create Subject (Admin Only)
# ==========================================

@router.post(
    "/",
    response_model=SubjectResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create subject"
)
def create_subject(
    subject: SubjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(allow_admin)
):
    """
    Creates a new subject. Admin access only (Teachers and Students cannot create subjects).
    """
    return subject_service.create_subject(
        subject,
        db
    )


# ==========================================
# Update Subject (Admin Only)
# ==========================================

@router.put(
    "/{subject_id}",
    response_model=SubjectResponse,
    summary="Update subject"
)
def update_subject(
    subject_id: int,
    subject: SubjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(allow_admin)
):
    """
    Updates subject details. Admin access only.
    """
    return subject_service.update_subject(
        subject_id,
        subject,
        db
    )


# ==========================================
# Delete Subject (Admin Only)
# ==========================================

@router.delete(
    "/{subject_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete subject"
)
def delete_subject(
    subject_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(allow_admin)
):
    """
    Deletes a subject. Admin access only (Teachers and Students cannot delete subjects).
    """
    return subject_service.delete_subject(
        subject_id,
        db
    )