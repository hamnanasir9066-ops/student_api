from typing import Optional
from pydantic import BaseModel, ConfigDict


class Token(BaseModel):
    """
    Response schema returned after successful authentication containing JWT access token.
    """
    access_token: str
    token_type: str = "bearer"

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    """
    Schema representing claims extracted from the JWT token payload.
    """
    user_id: Optional[int] = None
    email: Optional[str] = None
    role: Optional[str] = None
