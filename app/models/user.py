from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base
from app.enums.user_role import UserRole


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String(100), unique=True, nullable=False)

    email = Column(String(150), unique=True, nullable=False)

    hashed_password = Column(String(255), nullable=False)

    role = Column(
        Enum(UserRole),
        nullable=False
    )

    is_active = Column(Boolean, default=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    student = relationship(
        "Student",
        back_populates="user",
        uselist=False
    )