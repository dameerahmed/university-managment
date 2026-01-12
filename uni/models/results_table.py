from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, func, Enum
from uni.database.connection import Base
from sqlalchemy.orm import relationship
import enum
from uni.database.connection import Base


class Result(Base):
    __tablename__ = "results"

    result_id = Column(Integer, primary_key=True, autoincrement=True, index=True)

    student_id = Column(
        Integer,
        ForeignKey("students.student_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    subject_id = Column(
        Integer,
        ForeignKey("subjects.subject_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    batch_id = Column(
        Integer,
        ForeignKey("batches.batch_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    department_id = Column(
        Integer,
        ForeignKey("departments.department_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    semester = Column(Integer, nullable=False, index=True)  # e.g., 1, 2, 3, 4
    exam_type = Column(String, nullable=False, index=True)

    marks_obtained = Column(Float, nullable=False)
    total_marks = Column(Float, nullable=False)
    grade = Column(String, nullable=True, index=True)

    exam_date = Column(DateTime, nullable=False, index=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    student = relationship("Student", back_populates="results")
    subject = relationship("Subject", back_populates="results")
    batch = relationship("Batch", back_populates="results")
    department = relationship("Department", back_populates="results")
