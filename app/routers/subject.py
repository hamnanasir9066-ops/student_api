from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.subject import (
    SubjectCreate,
    SubjectUpdate,
    SubjectResponse
)

from app.services import subject_service

router = APIRouter()


# ==========================================
# Get All Subjects
# ==========================================

@router.get(
    "/",
    response_model=list[SubjectResponse]
)
def get_all_subjects(
    db: Session = Depends(get_db)
):
    return subject_service.get_all_subjects(db)


# ==========================================
# Get Subject By ID
# ==========================================

@router.get(
    "/{subject_id}",
    response_model=SubjectResponse
)
def get_subject(
    subject_id: int,
    db: Session = Depends(get_db)
):
    return subject_service.get_subject_by_id(
        subject_id,
        db
    )


# ==========================================
# Create Subject
# ==========================================

@router.post(
    "/",
    response_model=SubjectResponse,
    status_code=status.HTTP_201_CREATED
)
def create_subject(
    subject: SubjectCreate,
    db: Session = Depends(get_db)
):
    return subject_service.create_subject(
        subject,
        db
    )


# ==========================================
# Update Subject
# ==========================================

@router.put(
    "/{subject_id}",
    response_model=SubjectResponse
)
def update_subject(
    subject_id: int,
    subject: SubjectUpdate,
    db: Session = Depends(get_db)
):
    return subject_service.update_subject(
        subject_id,
        subject,
        db
    )


# ==========================================
# Delete Subject
# ==========================================

@router.delete(
    "/{subject_id}",
    status_code=status.HTTP_200_OK
)
def delete_subject(
    subject_id: int,
    db: Session = Depends(get_db)
):
    return subject_service.delete_subject(
        subject_id,
        db
    )