from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Date,
    DateTime,
    func,
    ForeignKey,
)
from uni.database.connection import Base
from sqlalchemy.orm import relationship


class Student(Base):
    __tablename__ = "students"

    student_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(
        Integer,
        ForeignKey("users.user_id"),
        unique=True,
        nullable=False,
        index=True,
    )
    first_name = Column(String, nullable=False, index=True)
    last_name = Column(String, nullable=False, index=True)
    father_name = Column(String, nullable=False, index=True)
    mother_name = Column(String, nullable=False, index=True)
    roll_number = Column(String, unique=True, nullable=False, index=True)
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
    date_of_birth = Column(Date, nullable=False, index=True)
    address = Column(String, nullable=False, index=True)
    phone_number = Column(String, nullable=False, index=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    batches = relationship("Batch", back_populates="students")
    department = relationship("Department", back_populates="students")
    user = relationship(
        "User",
        back_populates="students",
        cascade="all, delete-orphan",
        lazy="joined",
        single_parent=True,
    )

    results = relationship(
        "Result", back_populates="student", cascade="all, delete-orphan"
    )
