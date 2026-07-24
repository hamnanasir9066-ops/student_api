from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.user import (
    UserCreate,
    UserUpdate,
    UserResponse
)

from app.services import user_service

router = APIRouter()


# ==========================================
# Get All Users
# ==========================================

@router.get(
    "/",
    response_model=list[UserResponse]
)
def get_all_users(
    db: Session = Depends(get_db)
):
    return user_service.get_all_users(db)


# ==========================================
# Get User By ID
# ==========================================

@router.get(
    "/{user_id}",
    response_model=UserResponse
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    return user_service.get_user_by_id(
        user_id,
        db
    )


# ==========================================
# Create User
# ==========================================

@router.post(
    "/",
    response_model=UserResponse,
    status_code=201
)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    return user_service.create_user(
        user,
        db
    )


# ==========================================
# Update User
# ==========================================

@router.put(
    "/{user_id}",
    response_model=UserResponse
)
def update_user(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db)
):
    return user_service.update_user(
        user_id,
        user,
        db
    )


# ==========================================
# Delete User
# ==========================================

@router.delete(
    "/{user_id}"
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    return user_service.delete_user(
        user_id,
        db
    )