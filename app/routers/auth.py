from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.auth import Token
from app.services.auth_service import authenticate_user

router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    User login endpoint. Accepts form-data (username/email and password).
    Returns a JWT access token upon successful verification.
    """
    return authenticate_user(db=db, credentials=user_credentials)
