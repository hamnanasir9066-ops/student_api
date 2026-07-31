from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.enums.user_role import UserRole
from app.models.user import User
from app.schemas.mark import (
    MarkCreate,
    MarkUpdate,
    MarkResponse
)
from app.services import mark_service, student_service
from app.utils.oauth2 import get_current_user, require_roles

router = APIRouter()

# Permissions
allow_admin = require_roles(UserRole.ADMIN)
allow_staff = require_roles(UserRole.ADMIN, UserRole.TEACHER)


# ==========================================
# Get Own Marks (Student Self-Service)
# ==========================================

@router.get(
    "/me",
    response_model=list[MarkResponse],
    summary="Get marks for logged-in student"
)
def get_own_marks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Returns academic marks belonging to the logged-in student.
    """
    student = student_service.get_student_by_user_id(current_user.id, db)
    return mark_service.get_marks_by_student_id(student.id, db)


# ==========================================
# Get All Marks (Admin & Teacher)
# ==========================================

@router.get(
    "/",
    response_model=list[MarkResponse],
    summary="Get all marks"
)
def get_all_marks(
    db: Session = Depends(get_db),
    current_user: User = Depends(allow_staff)
):
    """
    Retrieves all student mark records. Accessible by Admin and Teacher.
    """
    return mark_service.get_all_marks(db)


# ==========================================
# Get Mark By ID (Admin & Teacher)
# ==========================================

@router.get(
    "/{mark_id}",
    response_model=MarkResponse,
    summary="Get mark by ID"
)
def get_mark(
    mark_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(allow_staff)
):
    """
    Retrieves mark record by ID. Accessible by Admin and Teacher.
    """
    return mark_service.get_mark_by_id(
        mark_id,
        db
    )


# ==========================================
# Create Mark (Admin & Teacher)
# ==========================================

@router.post(
    "/",
    response_model=MarkResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create mark record"
)
def create_mark(
    mark: MarkCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(allow_staff)
):
    """
    Creates a student mark record. Accessible by Admin and Teacher (Students cannot create marks).
    """
    return mark_service.create_mark(
        mark,
        db
    )


# ==========================================
# Update Mark (Admin & Teacher)
# ==========================================

@router.put(
    "/{mark_id}",
    response_model=MarkResponse,
    summary="Update mark record"
)
def update_mark(
    mark_id: int,
    mark: MarkUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(allow_staff)
):
    """
    Updates student mark record. Accessible by Admin and Teacher (Students cannot update marks).
    """
    return mark_service.update_mark(
        mark_id,
        mark,
        db
    )


# ==========================================
# Delete Mark (Admin Only)
# ==========================================

@router.delete(
    "/{mark_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete mark record"
)
def delete_mark(
    mark_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(allow_admin)
):
    """
    Deletes a mark record. Admin access only (Teachers and Students cannot delete marks).
    """
    return mark_service.delete_mark(
        mark_id,
        db
    )