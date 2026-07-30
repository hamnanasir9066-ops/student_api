from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.user import (
    UserCreate,
    UserUpdate,
    UserResponse
)
from app.services import user_service
from app.utils.oauth2 import get_current_user

router = APIRouter()


# ==========================================
# Get Current Authenticated User Profile
# ==========================================

@router.get(
    "/me",
    response_model=UserResponse
)
def get_me(
    current_user: User = Depends(get_current_user)
):
    """
    Returns the profile of the currently logged-in user.
    """
    return current_user


# ==========================================
# Get All Users (Protected Route)
# ==========================================

@router.get(
    "/",
    response_model=list[UserResponse]
)
def get_all_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
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