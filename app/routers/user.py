from fastapi import APIRouter, Depends, status,BackgroundTasks
from sqlalchemy.orm import Session

from app.database import get_db
from app.enums.user_role import UserRole
from app.models.user import User
from app.schemas.user import (
    UserCreate,
    UserUpdate,
    UserPasswordUpdate,
    UserResponse
)
from app.services import user_service
from app.utils.oauth2 import get_current_user, require_roles

router = APIRouter()

# Instantiate admin-only permission dependency
allow_admin = require_roles(UserRole.ADMIN)


# ==========================================
# Get Current Authenticated User Profile (All Roles)
# ==========================================

@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get logged-in user profile"
)
def get_me(
    current_user: User = Depends(get_current_user)
):
    """
    Returns the profile details of the currently authenticated user (Admin, Teacher, or Student).
    """
    return current_user


# ==========================================
# Update Own Password (Self-Service - All Roles)
# ==========================================

@router.put(
    "/me/password",
    summary="Update own password"
)
def update_own_password(
    payload: UserPasswordUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Allows the currently authenticated user to update their account password.
    """
    return user_service.change_user_password(
        user_id=current_user.id,
        new_password=payload.new_password,
        db=db
    )


# ==========================================
# Get All Users (Admin Only)
# ==========================================

@router.get(
    "/",
    response_model=list[UserResponse],
    summary="Get all users"
)
def get_all_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(allow_admin)
):
    """
    Retrieves a list of all registered users in the system. Admin access only.
    """
    return user_service.get_all_users(db)


# ==========================================
# Get User By ID (Admin Only)
# ==========================================

@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Get user by ID"
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(allow_admin)
):
    """
    Retrieves user details by User ID. Admin access only.
    """
    return user_service.get_user_by_id(
        user_id,
        db
    )


# ==========================================
# Create User (Admin Only)
# ==========================================

@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user"
)
def create_user(
    user: UserCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(allow_admin)
):
    return user_service.create_user(
        user=user,
        db=db,
        background_tasks=background_tasks
    )
# ==========================================
# Update User (Admin Only)
# ==========================================

@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Update a user"
)
def update_user(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(allow_admin)
):
    """
    Updates user account details or changes roles. Admin access only.
    """
    return user_service.update_user(
        user_id,
        user,
        db
    )


# ==========================================
# Delete User (Admin Only)
# ==========================================

@router.delete(
    "/{user_id}",
    summary="Delete a user"
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(allow_admin)
):
    """
    Deletes a user account. Admin access only.
    """
    return user_service.delete_user(
        user_id,
        db
    )