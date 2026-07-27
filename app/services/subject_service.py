# pyrefly: ignore [missing-import]
from fastapi import HTTPException, status
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session

from app.models.subject import Subject
from app.models.department import Department
from app.schemas.subject import SubjectCreate, SubjectUpdate


# ==========================================
# Get All Subjects
# ==========================================

def get_all_subjects(db: Session):
    return db.query(Subject).all()


# ==========================================
# Get Subject By ID
# ==========================================

def get_subject_by_id(
    subject_id: int,
    db: Session
):
    subject = db.query(Subject).filter(
        Subject.id == subject_id
    ).first()

    if subject is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found"
        )

    return subject


# ==========================================
# Create Subject
# ==========================================

def create_subject(
    subject: SubjectCreate,
    db: Session
):
    # Check Department Exists
    department = db.query(Department).filter(
        Department.id == subject.department_id
    ).first()

    if department is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found"
        )

    # Check Subject Code Exists
    existing = db.query(Subject).filter(
        Subject.subject_code == subject.code
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Subject with this code already exists."
        )

    new_subject = Subject(
        name=subject.name,
        subject_code=subject.code,
        credit_hours=subject.credit_hours,
        semester=getattr(subject, 'semester', 1),
        department_id=subject.department_id
    )

    db.add(new_subject)
    db.commit()
    db.refresh(new_subject)

    return new_subject


# ==========================================
# Update Subject
# ==========================================

def update_subject(
    subject_id: int,
    subject: SubjectUpdate,
    db: Session
):
    existing_subject = get_subject_by_id(subject_id, db)

    if subject.department_id is not None:
        department = db.query(Department).filter(
            Department.id == subject.department_id
        ).first()

        if department is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Department not found"
            )

    if subject.code is not None and subject.code != existing_subject.subject_code:
        duplicate = db.query(Subject).filter(
            Subject.subject_code == subject.code
        ).first()

        if duplicate:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Subject with this code already exists."
            )

    if subject.name is not None:
        existing_subject.name = subject.name

    if subject.code is not None:
        existing_subject.subject_code = subject.code

    if subject.credit_hours is not None:
        existing_subject.credit_hours = subject.credit_hours

    if subject.department_id is not None:
        existing_subject.department_id = subject.department_id

    db.commit()
    db.refresh(existing_subject)

    return existing_subject


# ==========================================
# Delete Subject
# ==========================================

def delete_subject(
    subject_id: int,
    db: Session
):
    subject = get_subject_by_id(subject_id, db)

    db.delete(subject)
    db.commit()

    return {
        "message": "Subject deleted successfully"
    }