from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, ForeignKey
from uni.database.connection import Base
from sqlalchemy.orm import relationship


class Subject(Base):
    __tablename__ = "subjects"

    subject_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    subject_name = Column(String, nullable=False, index=True)
    description = Column(String, nullable=True, index=True)
    credits = Column(Integer, nullable=False, index=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    departments = relationship(
        "Department", secondary="department_subjects", back_populates="subjects"
    )
    batches = relationship(
        "Batch", secondary="batch_subjects", back_populates="subjects"
    )
    teachers = relationship(
        "Teacher",
        secondary="teaching_assignments",
        back_populates="subjects",
        overlaps="departments,teachers",
    )
    results = relationship("Result", back_populates="subject")
