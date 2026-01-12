from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    func,
    ForeignKey,
    Table,
)
from uni.database.connection import Base
from sqlalchemy.orm import relationship


class Department(Base):
    __tablename__ = "departments"

    department_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    department_name = Column(String, unique=True, nullable=False, index=True)
    department_code = Column(String, unique=True, nullable=False, index=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    teachers = relationship(
        "Teacher",
        secondary="teaching_assignments",
        back_populates="departments",
        overlaps="subjects,teachers",
    )
    batches = relationship(
        "Batch", back_populates="department", cascade="all, delete-orphan"
    )

    students = relationship(
        "Student", back_populates="department", cascade="all, delete-orphan"
    )

    subjects = relationship(
        "Subject", secondary="department_subjects", back_populates="departments"
    )

    results = relationship("Result", back_populates="department")
