from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.mark import Mark
from app.models.student import Student
from app.models.subject import Subject
from app.enums.grade import Grade

from app.schemas.mark import (
    MarkCreate,
    MarkUpdate
)


# ==========================================
# Helper Function
# ==========================================

def calculate_grade(total: float):

    if total >= 90:
        return Grade.A

    elif total >= 85:
        return Grade.A_MINUS

    elif total >= 80:
        return Grade.B_PLUS

    elif total >= 75:
        return Grade.B

    elif total >= 70:
        return Grade.C_PLUS

    elif total >= 65:
        return Grade.C

    elif total >= 60:
        return Grade.D

    return Grade.F


# ==========================================
# Get All Marks
# ==========================================

def get_all_marks(db: Session):

    return db.query(Mark).all()


# ==========================================
# Get Mark By ID
# ==========================================

def get_mark_by_id(mark_id: int, db: Session):

    mark = db.query(Mark).filter(
        Mark.id == mark_id
    ).first()

    if mark is None:
        raise HTTPException(
            status_code=404,
            detail="Mark record not found"
        )

    return mark


# ==========================================
# Create Mark
# ==========================================

def create_mark(mark: MarkCreate, db: Session):

    # Check Student
    student = db.query(Student).filter(
        Student.id == mark.student_id
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    # Check Subject
    subject = db.query(Subject).filter(
        Subject.id == mark.subject_id
    ).first()

    if subject is None:
        raise HTTPException(
            status_code=404,
            detail="Subject not found"
        )

    # Prevent Duplicate Marks
    existing = db.query(Mark).filter(
        Mark.student_id == mark.student_id,
        Mark.subject_id == mark.subject_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Marks already exist for this student and subject."
        )

    total = (
        mark.quiz +
        mark.assignment +
        mark.midterm +
        mark.final
    )

    grade = calculate_grade(total)

    new_mark = Mark(
        student_id=mark.student_id,
        subject_id=mark.subject_id,
        quiz=mark.quiz,
        assignment=mark.assignment,
        midterm=mark.midterm,
        final=mark.final,
        total=total,
        grade=grade
    )

    db.add(new_mark)
    db.commit()
    db.refresh(new_mark)

    return new_mark


# ==========================================
# Update Mark
# ==========================================

def update_mark(
    mark_id: int,
    updated_mark: MarkUpdate,
    db: Session
):

    mark = get_mark_by_id(mark_id, db)

    if updated_mark.quiz is not None:
        mark.quiz = updated_mark.quiz

    if updated_mark.assignment is not None:
        mark.assignment = updated_mark.assignment

    if updated_mark.midterm is not None:
        mark.midterm = updated_mark.midterm

    if updated_mark.final is not None:
        mark.final = updated_mark.final

    # Recalculate Total
    mark.total = (
        mark.quiz +
        mark.assignment +
        mark.midterm +
        mark.final
    )

    # Recalculate Grade
    mark.grade = calculate_grade(mark.total)

    db.commit()
    db.refresh(mark)

    return mark


# ==========================================
# Delete Mark
# ==========================================

def delete_mark(mark_id: int, db: Session):

    mark = get_mark_by_id(mark_id, db)

    db.delete(mark)
    db.commit()

    return {
        "message": "Mark deleted successfully"
    }