from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Date,
    DateTime,
    ForeignKey
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    
    roll_number = Column(String(30), unique=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    
    phone = Column(String(20))
    gender = Column(String(20))
    date_of_birth = Column(Date)
    semester = Column(Integer, nullable=False)
    cgpa = Column(Float, default=0.0)
    address = Column(String(255))
    guardian_name = Column(String(100), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Computed Property
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    # Relationships
    user = relationship("User", back_populates="student")
    department_ref = relationship("Department", back_populates="students")


    # Relationship with Attendance
    attendances = relationship(
        "Attendance",
        back_populates="student",
        cascade="all, delete-orphan"
    )

    # Relationship with Marks
    marks = relationship(
        "Mark",
        back_populates="student",
        cascade="all, delete-orphan"
    )

    # Relationship with Fees
    fees = relationship(
        "Fee",
        back_populates="student",
        cascade="all, delete-orphan"
    )

    # Relationship with StudentSubject
    student_subjects = relationship(
        "StudentSubject",
        back_populates="student",
        cascade="all, delete-orphan"
    )