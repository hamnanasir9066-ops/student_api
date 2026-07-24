from sqlalchemy import Column, Integer, Float, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship

from app.database import Base
from app.enums.fee_status import FeeStatus


class Fee(Base):

    __tablename__ = "fees"

    id = Column(Integer, primary_key=True, index=True)

    student_id = Column(
        Integer,
        ForeignKey("students.id"),
        nullable=False
    )

    amount = Column(
        Float,
        nullable=False
    )

    due_date = Column(
        Date,
        nullable=False
    )

    paid_date = Column(
        Date,
        nullable=True
    )

    status = Column(
        Enum(FeeStatus),
        nullable=False,
        default=FeeStatus.PENDING
    )

    # Relationship with Student
    student = relationship(
        "Student",
        back_populates="fees"
    )