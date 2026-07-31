# pyrefly: ignore [missing-import]
from fastapi import HTTPException
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.utils.security import hash_password


# ==========================================
# Get All Users
# ==========================================

def get_all_users(db: Session):

    return db.query(User).all()


# ==========================================
# Get User By ID
# ==========================================

def get_user_by_id(user_id: int, db: Session):

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


# ==========================================
# Get User By Email
# ==========================================

def get_user_by_email(email: str, db: Session):

    return db.query(User).filter(
        User.email == email
    ).first()


# ==========================================
# Get User By Username
# ==========================================

def get_user_by_username(username: str, db: Session):

    return db.query(User).filter(
        User.username == username
    ).first()


# ==========================================
# Create User
# ==========================================

def create_user(user: UserCreate, db: Session):

    # Check username
    existing_username = get_user_by_username(
        user.username,
        db
    )

    if existing_username:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    # Check email
    existing_email = get_user_by_email(
        user.email,
        db
    )

    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    new_user = User(

        username=user.username,

        email=user.email,

        # Securely hash user password before database storage
        hashed_password=hash_password(user.password),

        role=user.role,

        is_active=True

    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return new_user


# ==========================================
# Update User
# ==========================================

def update_user(
    user_id: int,
    updated_user: UserUpdate,
    db: Session
):

    user = get_user_by_id(
        user_id,
        db
    )

    if updated_user.username is not None:

        existing = db.query(User).filter(
            User.username == updated_user.username,
            User.id != user_id
        ).first()

        if existing:
            raise HTTPException(
                status_code=400,
                detail="Username already exists"
            )

        user.username = updated_user.username

    if updated_user.email is not None:

        existing = db.query(User).filter(
            User.email == updated_user.email,
            User.id != user_id
        ).first()

        if existing:
            raise HTTPException(
                status_code=400,
                detail="Email already exists"
            )

        user.email = updated_user.email

    password = getattr(updated_user, "password", None)

    if password is not None:

        user.hashed_password = hash_password(password)

    if updated_user.role is not None:

        user.role = updated_user.role

    if updated_user.is_active is not None:

        user.is_active = updated_user.is_active

    db.commit()

    db.refresh(user)

    return user


# ==========================================
# Delete User
# ==========================================

def delete_user(
    user_id: int,
    db: Session
):

    get_user_by_id(
        user_id,
        db
    )

    db.query(User).filter(
        User.id == user_id
    ).delete(synchronize_session=False)

    db.commit()

    return {
        "message": "User deleted successfully"
    }


# ==========================================
# Change User Password (Self-Service)
# ==========================================

def change_user_password(
    user_id: int,
    new_password: str,
    db: Session
):
    """
    Updates the password for a specific user ID after hashing it securely.
    Used for user self-service password updates.
    """
    user = get_user_by_id(user_id, db)
    user.hashed_password = hash_password(new_password)
    db.commit()
    db.refresh(user)
    return {"message": "Password updated successfully"}