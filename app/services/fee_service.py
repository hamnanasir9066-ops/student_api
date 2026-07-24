from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.fee import Fee
from app.models.student import Student
from app.enums.fee_status import FeeStatus

from app.schemas.fee import (
    FeeCreate,
    FeeUpdate
)


# ==========================================
# Get All Fees
# ==========================================

def get_all_fees(db: Session):

    return db.query(Fee).all()


# ==========================================
# Get Fee By ID
# ==========================================

def get_fee_by_id(
    fee_id: int,
    db: Session
):

    fee = db.query(Fee).filter(
        Fee.id == fee_id
    ).first()

    if fee is None:
        raise HTTPException(
            status_code=404,
            detail="Fee record not found"
        )

    return fee


# ==========================================
# Create Fee
# ==========================================

def create_fee(
    fee: FeeCreate,
    db: Session
):

    # Check Student Exists
    student = db.query(Student).filter(
        Student.id == fee.student_id
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    # Prevent Duplicate Fee Record
    existing = db.query(Fee).filter(
        Fee.student_id == fee.student_id,
        Fee.due_date == fee.due_date
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Fee record already exists for this due date."
        )

    status = FeeStatus.PAID if fee.paid_date else FeeStatus.PENDING

    new_fee = Fee(
        student_id=fee.student_id,
        amount=fee.amount,
        due_date=fee.due_date,
        paid_date=fee.paid_date,
        status=status
    )

    db.add(new_fee)
    db.commit()
    db.refresh(new_fee)

    return new_fee


# ==========================================
# Update Fee
# ==========================================

def update_fee(
    fee_id: int,
    updated_fee: FeeUpdate,
    db: Session
):

    fee = get_fee_by_id(
        fee_id,
        db
    )

    if updated_fee.amount is not None:
        fee.amount = updated_fee.amount

    if updated_fee.due_date is not None:
        fee.due_date = updated_fee.due_date

    if updated_fee.paid_date is not None:
        fee.paid_date = updated_fee.paid_date

    # Automatically Update Status
    if fee.paid_date:
        fee.status = FeeStatus.PAID
    else:
        fee.status = FeeStatus.PENDING

    db.commit()
    db.refresh(fee)

    return fee


# ==========================================
# Delete Fee
# ==========================================

def delete_fee(
    fee_id: int,
    db: Session
):

    fee = get_fee_by_id(
        fee_id,
        db
    )

    db.delete(fee)
    db.commit()

    return {
        "message": "Fee deleted successfully"
    }