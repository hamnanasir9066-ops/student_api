# pyrefly: ignore [missing-import]
from fastapi import Depends, HTTPException, status
# pyrefly: ignore [missing-import]
from fastapi.security import OAuth2PasswordBearer
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.utils.security import decode_access_token

from app.enums.user_role import UserRole

# Define the OAuth2 scheme, directing OpenAPI (Swagger UI) to /auth/login for token generation
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    FastAPI dependency that validates the JWT token from the Authorization header
    and retrieves the corresponding active user from the database.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    user_id: int = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user account"
        )

    return user


class RoleChecker:
    """
    Production-grade Role-Based Access Control (RBAC) dependency.
    Verifies if the authenticated user's role matches any of the allowed roles.
    """
    def __init__(self, allowed_roles: list[UserRole]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user)) -> User:
        user_role = current_user.role
        if isinstance(user_role, str):
            user_role = UserRole(user_role)

        if user_role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {[r.value for r in self.allowed_roles]}"
            )

        return current_user


def require_roles(*allowed_roles: UserRole) -> RoleChecker:
    """
    Convenience helper function to instantiate RoleChecker dependency.
    Example usage in routers:
        current_user: User = Depends(require_roles(UserRole.ADMIN, UserRole.TEACHER))
    """
    return RoleChecker(list(allowed_roles))


