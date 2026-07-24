from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Department(Base):

    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), unique=True, nullable=False)

    code = Column(String(20), unique=True, nullable=False)

    hod_name = Column(String(100), nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # One Department -> Many Students
    students = relationship(
        "Student",
        back_populates="department_ref"
    )

    # One Department -> Many Subjects
    subjects = relationship(
        "Subject",
        back_populates="department"
    )