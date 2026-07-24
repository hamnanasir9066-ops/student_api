from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.attendance import Attendance
from app.models.student import Student
from app.models.subject import Subject

from app.schemas.attendance import (
    AttendanceCreate,
    AttendanceUpdate
)


# ==========================================
# Get All Attendance
# ==========================================

def get_all_attendance(db: Session):

    return db.query(Attendance).all()


# ==========================================
# Get Attendance By ID
# ==========================================

def get_attendance_by_id(
    attendance_id: int,
    db: Session
):

    attendance = db.query(Attendance).filter(
        Attendance.id == attendance_id
    ).first()

    if attendance is None:
        raise HTTPException(
            status_code=404,
            detail="Attendance record not found"
        )

    return attendance


# ==========================================
# Create Attendance
# ==========================================

def create_attendance(
    attendance: AttendanceCreate,
    db: Session
):

    # Check Student Exists
    student = db.query(Student).filter(
        Student.id == attendance.student_id
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    # Check Subject Exists
    subject = db.query(Subject).filter(
        Subject.id == attendance.subject_id
    ).first()

    if subject is None:
        raise HTTPException(
            status_code=404,
            detail="Subject not found"
        )

    # Prevent Duplicate Attendance
    existing = db.query(Attendance).filter(
        Attendance.student_id == attendance.student_id,
        Attendance.subject_id == attendance.subject_id,
        Attendance.date == attendance.date
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Attendance already marked for this student on this date."
        )

    new_attendance = Attendance(
        student_id=attendance.student_id,
        subject_id=attendance.subject_id,
        date=attendance.date,
        status=attendance.status
    )

    db.add(new_attendance)
    db.commit()
    db.refresh(new_attendance)

    return new_attendance


# ==========================================
# Update Attendance
# ==========================================

def update_attendance(
    attendance_id: int,
    updated_attendance: AttendanceUpdate,
    db: Session
):

    attendance = get_attendance_by_id(
        attendance_id,
        db
    )

    if updated_attendance.date is not None:
        attendance.date = updated_attendance.date

    if updated_attendance.status is not None:
        attendance.status = updated_attendance.status

    db.commit()
    db.refresh(attendance)

    return attendance


# ==========================================
# Delete Attendance
# ==========================================

def delete_attendance(
    attendance_id: int,
    db: Session
):

    attendance = get_attendance_by_id(
        attendance_id,
        db
    )

    db.delete(attendance)
    db.commit()

    return {
        "message": "Attendance deleted successfully"
    }