from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.enums.user_role import UserRole
from app.models.user import User
from app.schemas.attendance import (
    AttendanceCreate,
    AttendanceUpdate,
    AttendanceResponse
)
from app.services import attendance_service, student_service
from app.utils.oauth2 import get_current_user, require_roles

router = APIRouter()

# Permissions
allow_admin = require_roles(UserRole.ADMIN)
allow_staff = require_roles(UserRole.ADMIN, UserRole.TEACHER)


# ==========================================
# Get Own Attendance (Student Self-Service)
# ==========================================

@router.get(
    "/me",
    response_model=list[AttendanceResponse],
    summary="Get attendance for logged-in student"
)
def get_own_attendance(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Returns attendance history belonging to the logged-in student.
    """
    student = student_service.get_student_by_user_id(current_user.id, db)
    return attendance_service.get_attendance_by_student_id(student.id, db)


# ==========================================
# Get All Attendance (Admin & Teacher)
# ==========================================

@router.get(
    "/",
    response_model=list[AttendanceResponse],
    summary="Get all attendance records"
)
def get_all_attendance(
    db: Session = Depends(get_db),
    current_user: User = Depends(allow_staff)
):
    """
    Retrieves all student attendance records. Accessible by Admin and Teacher.
    """
    return attendance_service.get_all_attendance(db)


# ==========================================
# Get Attendance By ID (Admin & Teacher)
# ==========================================

@router.get(
    "/{attendance_id}",
    response_model=AttendanceResponse,
    summary="Get attendance by ID"
)
def get_attendance(
    attendance_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(allow_staff)
):
    """
    Retrieves attendance record by ID. Accessible by Admin and Teacher.
    """
    return attendance_service.get_attendance_by_id(
        attendance_id,
        db
    )


# ==========================================
# Create Attendance (Admin & Teacher)
# ==========================================

@router.post(
    "/",
    response_model=AttendanceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create attendance record"
)
def create_attendance(
    attendance: AttendanceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(allow_staff)
):
    """
    Marks student attendance. Accessible by Admin and Teacher (Students cannot create attendance).
    """
    return attendance_service.create_attendance(
        attendance,
        db
    )


# ==========================================
# Update Attendance (Admin & Teacher)
# ==========================================

@router.put(
    "/{attendance_id}",
    response_model=AttendanceResponse,
    summary="Update attendance record"
)
def update_attendance(
    attendance_id: int,
    attendance: AttendanceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(allow_staff)
):
    """
    Updates student attendance record. Accessible by Admin and Teacher (Students cannot update attendance).
    """
    return attendance_service.update_attendance(
        attendance_id,
        attendance,
        db
    )


# ==========================================
# Delete Attendance (Admin Only)
# ==========================================

@router.delete(
    "/{attendance_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete attendance record"
)
def delete_attendance(
    attendance_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(allow_admin)
):
    """
    Deletes an attendance record. Admin access only (Teachers and Students cannot delete attendance).
    """
    return attendance_service.delete_attendance(
        attendance_id,
        db
    )