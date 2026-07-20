from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import schemas
from ..database import get_db
from ..services import student_service

router = APIRouter()

# -------------------- GET ALL STUDENTS --------------------

@router.get("/", response_model=list[schemas.StudentResponse])
def get_students(db: Session = Depends(get_db)):
    return student_service.get_all_students(db)


# -------------------- GET STUDENT BY ID --------------------

@router.get("/{student_id}", response_model=schemas.StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = student_service.get_student_by_id(student_id, db)

    if student is None:
        return {"message": "Student not found"}

    return student


# -------------------- ADD STUDENT --------------------

@router.post("/", response_model=schemas.StudentResponse)
def add_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    return student_service.create_student(student, db)


# -------------------- UPDATE STUDENT --------------------

@router.put("/{student_id}", response_model=schemas.StudentResponse)
def update_student(student_id: int, updated_student: schemas.StudentCreate, db: Session = Depends(get_db)):
    student = student_service.update_student(student_id, updated_student, db)

    if student is None:
        return {"message": "Student not found"}

    return student


# -------------------- DELETE STUDENT --------------------

@router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    deleted = student_service.delete_student(student_id, db)

    if not deleted:
        return {"message": "Student not found"}

    return {"message": "Student deleted successfully"}