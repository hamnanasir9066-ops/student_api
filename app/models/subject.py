# pyrefly: ignore [missing-import]
from sqlalchemy import Column, Integer, String, ForeignKey
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import relationship, synonym

from app.database import Base


class Subject(Base):

    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)

    subject_code = Column(
        String(20),
        unique=True,
        nullable=False
    )
    code = synonym("subject_code")

    name = Column(
        String(100),
        nullable=False
    )

    credit_hours = Column(
        Integer,
        nullable=False
    )

    semester = Column(
        Integer,
        nullable=False
    )

    department_id = Column(
        Integer,
        ForeignKey("departments.id"),
        nullable=False
    )

    # Relationship with Department
    department = relationship(
        "Department",
        back_populates="subjects"
    )

    # Relationship with StudentSubject
    student_subjects = relationship(
        "StudentSubject",
        back_populates="subject",
        cascade="all, delete-orphan"
    )

    # Relationship with Attendance
    attendances = relationship(
        "Attendance",
        back_populates="subject",
        cascade="all, delete-orphan"
    )

    # Relationship with Marks
    marks = relationship(
        "Mark",
        back_populates="subject",
        cascade="all, delete-orphan"
    )