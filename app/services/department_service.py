from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.department import Department
from app.schemas.department import (
    DepartmentCreate,
    DepartmentUpdate
)


# ==========================================
# Get All Departments
# ==========================================

def get_all_departments(db: Session):

    return db.query(Department).all()


# ==========================================
# Get Department By ID
# ==========================================

def get_department_by_id(
    department_id: int,
    db: Session
):

    department = db.query(Department).filter(
        Department.id == department_id
    ).first()

    if department is None:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    return department


# ==========================================
# Get Department By Name
# ==========================================

def get_department_by_name(
    name: str,
    db: Session
):

    return db.query(Department).filter(
        Department.name == name
    ).first()


# ==========================================
# Get Department By Code
# ==========================================

def get_department_by_code(
    code: str,
    db: Session
):

    return db.query(Department).filter(
        Department.code == code
    ).first()


# ==========================================
# Create Department
# ==========================================

def create_department(
    department: DepartmentCreate,
    db: Session
):

    existing_name = get_department_by_name(
        department.name,
        db
    )

    if existing_name:
        raise HTTPException(
            status_code=400,
            detail="Department name already exists"
        )

    existing_code = get_department_by_code(
        department.code,
        db
    )

    if existing_code:
        raise HTTPException(
            status_code=400,
            detail="Department code already exists"
        )

    new_department = Department(
        name=department.name,
        code=department.code,
        hod_name=department.hod_name
    )

    db.add(new_department)

    db.commit()

    db.refresh(new_department)

    return new_department


# ==========================================
# Update Department
# ==========================================

def update_department(
    department_id: int,
    updated_department: DepartmentUpdate,
    db: Session
):

    department = get_department_by_id(
        department_id,
        db
    )

    if updated_department.name is not None:

        existing = db.query(Department).filter(
            Department.name == updated_department.name,
            Department.id != department_id
        ).first()

        if existing:
            raise HTTPException(
                status_code=400,
                detail="Department name already exists"
            )

        department.name = updated_department.name

    if updated_department.code is not None:

        existing = db.query(Department).filter(
            Department.code == updated_department.code,
            Department.id != department_id
        ).first()

        if existing:
            raise HTTPException(
                status_code=400,
                detail="Department code already exists"
            )

        department.code = updated_department.code

    if updated_department.hod_name is not None:

        department.hod_name = updated_department.hod_name

    db.commit()

    db.refresh(department)

    return department


# ==========================================
# Delete Department
# ==========================================

def delete_department(
    department_id: int,
    db: Session
):

    department = get_department_by_id(
        department_id,
        db
    )

    # Business Validation
    if department.students:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete department because students are assigned to it."
        )

    if department.subjects:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete department because subjects are assigned to it."
        )

    db.delete(department)

    db.commit()

    return {
        "message": "Department deleted successfully"
    }