from sqlalchemy import Column, Integer, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship

from app.database import Base
from app.enums.attendance_status import AttendanceStatus


class Attendance(Base):

    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True)

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

    date = Column(Date, nullable=False)

    status = Column(
        Enum(AttendanceStatus),
        nullable=False
    )

    student = relationship(
        "Student",
        back_populates="attendances"
    )

    subject = relationship(
        "Subject",
        back_populates="attendances"
    )