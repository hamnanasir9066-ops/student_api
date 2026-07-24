from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.student_subject import StudentSubject
from app.models.student import Student
from app.models.subject import Subject

from app.schemas.student_subject import (
    StudentSubjectCreate
)


# ==========================================
# Get All Enrollments
# ==========================================

def get_all_student_subjects(db: Session):

    return db.query(StudentSubject).all()


# ==========================================
# Get Enrollment By ID
# ==========================================

def get_student_subject_by_id(
    enrollment_id: int,
    db: Session
):

    enrollment = db.query(StudentSubject).filter(
        StudentSubject.id == enrollment_id
    ).first()

    if enrollment is None:
        raise HTTPException(
            status_code=404,
            detail="Enrollment not found"
        )

    return enrollment


# ==========================================
# Enroll Student
# ==========================================

def enroll_student(
    enrollment: StudentSubjectCreate,
    db: Session
):

    # Check Student Exists
    student = db.query(Student).filter(
        Student.id == enrollment.student_id
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    # Check Subject Exists
    subject = db.query(Subject).filter(
        Subject.id == enrollment.subject_id
    ).first()

    if subject is None:
        raise HTTPException(
            status_code=404,
            detail="Subject not found"
        )

    # Prevent Duplicate Enrollment
    existing = db.query(StudentSubject).filter(
        StudentSubject.student_id == enrollment.student_id,
        StudentSubject.subject_id == enrollment.subject_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Student is already enrolled in this subject."
        )

    new_enrollment = StudentSubject(
        student_id=enrollment.student_id,
        subject_id=enrollment.subject_id
    )

    db.add(new_enrollment)

    db.commit()

    db.refresh(new_enrollment)

    return new_enrollment


# ==========================================
# Delete Enrollment
# ==========================================

def delete_enrollment(
    enrollment_id: int,
    db: Session
):

    enrollment = get_student_subject_by_id(
        enrollment_id,
        db
    )

    db.delete(enrollment)

    db.commit()

    return {
        "message": "Enrollment deleted successfully"
    }