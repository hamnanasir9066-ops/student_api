from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base
from sqlalchemy import Enum
from app.enums.grade import Grade


class Mark(Base):

    __tablename__ = "marks"

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

    quiz = Column(Float, default=0)

    assignment = Column(Float, default=0)

    midterm = Column(Float, default=0)

    final = Column(Float, default=0)

    total = Column(Float, default=0)
    grade = Column(
    Enum(Grade),
    nullable=False
)

    # Relationship with Student
    student = relationship(
        "Student",
        back_populates="marks"
    )

    # Relationship with Subject
    subject = relationship(
        "Subject",
        back_populates="marks"
    )