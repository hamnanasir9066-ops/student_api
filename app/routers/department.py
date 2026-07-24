from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.department import (
    DepartmentCreate,
    DepartmentUpdate,
    DepartmentResponse
)

from app.services import department_service

router = APIRouter()


# ==========================================
# Get All Departments
# ==========================================

@router.get(
    "/",
    response_model=list[DepartmentResponse]
)
def get_all_departments(
    db: Session = Depends(get_db)
):
    return department_service.get_all_departments(db)


# ==========================================
# Get Department By ID
# ==========================================

@router.get(
    "/{department_id}",
    response_model=DepartmentResponse
)
def get_department(
    department_id: int,
    db: Session = Depends(get_db)
):
    return department_service.get_department_by_id(
        department_id,
        db
    )


# ==========================================
# Create Department
# ==========================================

@router.post(
    "/",
    response_model=DepartmentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_department(
    department: DepartmentCreate,
    db: Session = Depends(get_db)
):
    return department_service.create_department(
        department,
        db
    )


# ==========================================
# Update Department
# ==========================================

@router.put(
    "/{department_id}",
    response_model=DepartmentResponse
)
def update_department(
    department_id: int,
    department: DepartmentUpdate,
    db: Session = Depends(get_db)
):
    return department_service.update_department(
        department_id,
        department,
        db
    )


# ==========================================
# Delete Department
# ==========================================

@router.delete(
    "/{department_id}",
    status_code=status.HTTP_200_OK
)
def delete_department(
    department_id: int,
    db: Session = Depends(get_db)
):
    return department_service.delete_department(
        department_id,
        db
    )