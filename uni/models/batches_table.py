from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, ForeignKey
from uni.database.connection import Base
from sqlalchemy.orm import relationship


class Batch(Base):
    __tablename__ = "batches"

    batch_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    batch_name = Column(String, unique=True, nullable=False, index=True)
    department_id = Column(
        Integer,
        ForeignKey("departments.department_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    seats_limit = Column(Integer, nullable=False, index=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    department = relationship("Department", back_populates="batches")
    students = relationship(
        "Student", back_populates="batches", cascade="all, delete-orphan"
    )
    subjects = relationship(
        "Subject", secondary="batch_subjects", back_populates="batches"
    )
    results = relationship("Result", back_populates="batch")
