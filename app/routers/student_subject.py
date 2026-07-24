from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.student_subject import (
    StudentSubjectCreate,
    StudentSubjectResponse
)

from app.services import student_subject_service

router = APIRouter()


# ==========================================
# Get All Enrollments
# ==========================================

@router.get(
    "/",
    response_model=list[StudentSubjectResponse]
)
def get_all_enrollments(
    db: Session = Depends(get_db)
):
    return student_subject_service.get_all_student_subjects(db)


# ==========================================
# Get Enrollment By ID
# ==========================================

@router.get(
    "/{enrollment_id}",
    response_model=StudentSubjectResponse
)
def get_enrollment(
    enrollment_id: int,
    db: Session = Depends(get_db)
):
    return student_subject_service.get_student_subject_by_id(
        enrollment_id,
        db
    )


# ==========================================
# Enroll Student
# ==========================================

@router.post(
    "/",
    response_model=StudentSubjectResponse,
    status_code=status.HTTP_201_CREATED
)
def enroll_student(
    enrollment: StudentSubjectCreate,
    db: Session = Depends(get_db)
):
    return student_subject_service.enroll_student(
        enrollment,
        db
    )


# ==========================================
# Delete Enrollment
# ==========================================

@router.delete(
    "/{enrollment_id}",
    status_code=status.HTTP_200_OK
)
def delete_enrollment(
    enrollment_id: int,
    db: Session = Depends(get_db)
):
    return student_subject_service.delete_enrollment(
        enrollment_id,
        db
    )