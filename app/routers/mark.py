from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.mark import (
    MarkCreate,
    MarkUpdate,
    MarkResponse
)

from app.services import mark_service

router = APIRouter()


# ==========================================
# Get All Marks
# ==========================================

@router.get(
    "/",
    response_model=list[MarkResponse]
)
def get_all_marks(
    db: Session = Depends(get_db)
):
    return mark_service.get_all_marks(db)


# ==========================================
# Get Mark By ID
# ==========================================

@router.get(
    "/{mark_id}",
    response_model=MarkResponse
)
def get_mark(
    mark_id: int,
    db: Session = Depends(get_db)
):
    return mark_service.get_mark_by_id(
        mark_id,
        db
    )


# ==========================================
# Create Mark
# ==========================================

@router.post(
    "/",
    response_model=MarkResponse,
    status_code=status.HTTP_201_CREATED
)
def create_mark(
    mark: MarkCreate,
    db: Session = Depends(get_db)
):
    return mark_service.create_mark(
        mark,
        db
    )


# ==========================================
# Update Mark
# ==========================================

@router.put(
    "/{mark_id}",
    response_model=MarkResponse
)
def update_mark(
    mark_id: int,
    mark: MarkUpdate,
    db: Session = Depends(get_db)
):
    return mark_service.update_mark(
        mark_id,
        mark,
        db
    )


# ==========================================
# Delete Mark
# ==========================================

@router.delete(
    "/{mark_id}",
    status_code=status.HTTP_200_OK
)
def delete_mark(
    mark_id: int,
    db: Session = Depends(get_db)
):
    return mark_service.delete_mark(
        mark_id,
        db
    )