from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.enums.user_role import UserRole
from app.models.user import User
from app.schemas.department import (
    DepartmentCreate,
    DepartmentUpdate,
    DepartmentResponse
)
from app.services import department_service
from app.utils.oauth2 import get_current_user, require_roles

router = APIRouter()

# Permissions
allow_admin = require_roles(UserRole.ADMIN)
allow_staff = require_roles(UserRole.ADMIN, UserRole.TEACHER)


# ==========================================
# Get All Departments (Admin, Teacher & Authenticated)
# ==========================================

@router.get(
    "/",
    response_model=list[DepartmentResponse],
    summary="Get all departments"
)
def get_all_departments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieves all departments. Accessible by authenticated users.
    """
    return department_service.get_all_departments(db)


# ==========================================
# Get Department By ID
# ==========================================

@router.get(
    "/{department_id}",
    response_model=DepartmentResponse,
    summary="Get department by ID"
)
def get_department(
    department_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieves department by ID. Accessible by authenticated users.
    """
    return department_service.get_department_by_id(
        department_id,
        db
    )


# ==========================================
# Create Department (Admin Only)
# ==========================================

@router.post(
    "/",
    response_model=DepartmentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create department"
)
def create_department(
    department: DepartmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(allow_admin)
):
    """
    Creates a new department. Admin access only (Teachers and Students cannot create departments).
    """
    return department_service.create_department(
        department,
        db
    )


# ==========================================
# Update Department (Admin Only)
# ==========================================

@router.put(
    "/{department_id}",
    response_model=DepartmentResponse,
    summary="Update department"
)
def update_department(
    department_id: int,
    department: DepartmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(allow_admin)
):
    """
    Updates department details. Admin access only.
    """
    return department_service.update_department(
        department_id,
        department,
        db
    )


# ==========================================
# Delete Department (Admin Only)
# ==========================================

@router.delete(
    "/{department_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete department"
)
def delete_department(
    department_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(allow_admin)
):
    """
    Deletes a department. Admin access only (Teachers and Students cannot delete departments).
    """
    return department_service.delete_department(
        department_id,
        db
    )