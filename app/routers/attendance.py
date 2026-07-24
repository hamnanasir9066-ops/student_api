from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.attendance import (
    AttendanceCreate,
    AttendanceUpdate,
    AttendanceResponse
)

from app.services import attendance_service

router = APIRouter()


# ==========================================
# Get All Attendance
# ==========================================

@router.get(
    "/",
    response_model=list[AttendanceResponse]
)
def get_all_attendance(
    db: Session = Depends(get_db)
):
    return attendance_service.get_all_attendance(db)


# ==========================================
# Get Attendance By ID
# ==========================================

@router.get(
    "/{attendance_id}",
    response_model=AttendanceResponse
)
def get_attendance(
    attendance_id: int,
    db: Session = Depends(get_db)
):
    return attendance_service.get_attendance_by_id(
        attendance_id,
        db
    )


# ==========================================
# Create Attendance
# ==========================================

@router.post(
    "/",
    response_model=AttendanceResponse,
    status_code=status.HTTP_201_CREATED
)
def create_attendance(
    attendance: AttendanceCreate,
    db: Session = Depends(get_db)
):
    return attendance_service.create_attendance(
        attendance,
        db
    )


# ==========================================
# Update Attendance
# ==========================================

@router.put(
    "/{attendance_id}",
    response_model=AttendanceResponse
)
def update_attendance(
    attendance_id: int,
    attendance: AttendanceUpdate,
    db: Session = Depends(get_db)
):
    return attendance_service.update_attendance(
        attendance_id,
        attendance,
        db
    )


# ==========================================
# Delete Attendance
# ==========================================

@router.delete(
    "/{attendance_id}",
    status_code=status.HTTP_200_OK
)
def delete_attendance(
    attendance_id: int,
    db: Session = Depends(get_db)
):
    return attendance_service.delete_attendance(
        attendance_id,
        db
    )