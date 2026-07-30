from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.auth import Token
from app.utils.security import create_access_token, verify_password


def authenticate_user(db: Session, credentials: OAuth2PasswordRequestForm) -> Token:
    """
    Authenticates a user by email or username, verifies the password,
    and returns a signed JWT access token.
    """
    # 1. Search for user by email or username
    user = db.query(User).filter(
        (User.email == credentials.username) | (User.username == credentials.username)
    ).first()

    # 2. If user doesn't exist, raise 401 Unauthorized exception
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 3. Verify password hash
    if not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 4. Check if account is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User account is inactive"
        )

    # 5. Extract role string (handle Enum or str)
    role_str = user.role.value if hasattr(user.role, "value") else str(user.role)

    # 6. Generate JWT token with sub (user.id) and role
    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "email": user.email,
            "role": role_str
        }
    )

    # 7. Return Token response model
    return Token(access_token=access_token, token_type="bearer")
