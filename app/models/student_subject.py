from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class StudentSubject(Base):

    __tablename__ = "student_subjects"

    id = Column(Integer, primary_key=True, index=True)

    student_id = Column(
        Integer,
        ForeignKey("students.id"),
        nullable=False
    )

    subject_id = Column(
        Integer,
        ForeignKey("subjects.id"),
        nullable=False
    )

    enrolled_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # Relationship with Student
    student = relationship(
        "Student",
        back_populates="student_subjects"
    )

    # Relationship with Subject
    subject = relationship(
        "Subject",
        back_populates="student_subjects"
    )