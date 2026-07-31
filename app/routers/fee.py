from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.enums.user_role import UserRole
from app.models.user import User
from app.schemas.fee import (
    FeeCreate,
    FeeUpdate,
    FeeResponse
)
from app.services import fee_service, student_service
from app.utils.oauth2 import get_current_user, require_roles

router = APIRouter()

# Permissions
allow_admin = require_roles(UserRole.ADMIN)
allow_staff = require_roles(UserRole.ADMIN, UserRole.TEACHER)


# ==========================================
# Get Own Fees (Student Self-Service)
# ==========================================

@router.get(
    "/me",
    response_model=list[FeeResponse],
    summary="Get fee details for logged-in student"
)
def get_own_fees(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Returns fee statements belonging to the logged-in student.
    """
    student = student_service.get_student_by_user_id(current_user.id, db)
    return fee_service.get_fees_by_student_id(student.id, db)


# ==========================================
# Get All Fees (Admin & Teacher)
# ==========================================

@router.get(
    "/",
    response_model=list[FeeResponse],
    summary="Get all fee records"
)
def get_all_fees(
    db: Session = Depends(get_db),
    current_user: User = Depends(allow_staff)
):
    """
    Retrieves all fee records. Accessible by Admin and Teacher (view fee status).
    """
    return fee_service.get_all_fees(db)


# ==========================================
# Get Fee By ID (Admin & Teacher)
# ==========================================

@router.get(
    "/{fee_id}",
    response_model=FeeResponse,
    summary="Get fee by ID"
)
def get_fee(
    fee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(allow_staff)
):
    """
    Retrieves fee record by ID. Accessible by Admin and Teacher.
    """
    return fee_service.get_fee_by_id(
        fee_id,
        db
    )


# ==========================================
# Create Fee (Admin Only)
# ==========================================

@router.post(
    "/",
    response_model=FeeResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create fee record"
)
def create_fee(
    fee: FeeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(allow_admin)
):
    """
    Creates a new fee record. Admin access only (Teachers and Students cannot modify fee records).
    """
    return fee_service.create_fee(
        fee,
        db
    )


# ==========================================
# Update Fee (Admin Only)
# ==========================================

@router.put(
    "/{fee_id}",
    response_model=FeeResponse,
    summary="Update fee record"
)
def update_fee(
    fee_id: int,
    fee: FeeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(allow_admin)
):
    """
    Updates a fee record. Admin access only.
    """
    return fee_service.update_fee(
        fee_id,
        fee,
        db
    )


# ==========================================
# Delete Fee (Admin Only)
# ==========================================

@router.delete(
    "/{fee_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete fee record"
)
def delete_fee(
    fee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(allow_admin)
):
    """
    Deletes a fee record. Admin access only.
    """
    return fee_service.delete_fee(
        fee_id,
        db
    )