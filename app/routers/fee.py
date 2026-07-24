from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.fee import (
    FeeCreate,
    FeeUpdate,
    FeeResponse
)

from app.services import fee_service

router = APIRouter()


# ==========================================
# Get All Fees
# ==========================================

@router.get(
    "/",
    response_model=list[FeeResponse]
)
def get_all_fees(
    db: Session = Depends(get_db)
):
    return fee_service.get_all_fees(db)


# ==========================================
# Get Fee By ID
# ==========================================

@router.get(
    "/{fee_id}",
    response_model=FeeResponse
)
def get_fee(
    fee_id: int,
    db: Session = Depends(get_db)
):
    return fee_service.get_fee_by_id(
        fee_id,
        db
    )


# ==========================================
# Create Fee
# ==========================================

@router.post(
    "/",
    response_model=FeeResponse,
    status_code=status.HTTP_201_CREATED
)
def create_fee(
    fee: FeeCreate,
    db: Session = Depends(get_db)
):
    return fee_service.create_fee(
        fee,
        db
    )


# ==========================================
# Update Fee
# ==========================================

@router.put(
    "/{fee_id}",
    response_model=FeeResponse
)
def update_fee(
    fee_id: int,
    fee: FeeUpdate,
    db: Session = Depends(get_db)
):
    return fee_service.update_fee(
        fee_id,
        fee,
        db
    )


# ==========================================
# Delete Fee
# ==========================================

@router.delete(
    "/{fee_id}",
    status_code=status.HTTP_200_OK
)
def delete_fee(
    fee_id: int,
    db: Session = Depends(get_db)
):
    return fee_service.delete_fee(
        fee_id,
        db
    )