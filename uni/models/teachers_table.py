from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, ForeignKey
from uni.database.connection import Base
from sqlalchemy.orm import relationship


class Teacher(Base):
    __tablename__ = "teachers"

    teacher_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(
        Integer,
        ForeignKey("users.user_id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )
    first_name = Column(String, nullable=False, index=True)
    last_name = Column(String, nullable=False, index=True)
    phone_number = Column(String, nullable=False, index=True)
    address = Column(String, nullable=False, index=True)
    hire_date = Column(DateTime, nullable=False, index=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="teachers")  # Removed incorrect cascade
    departments = relationship(
        "Department",
        secondary="teaching_assignments",
        back_populates="teachers",
        overlaps="subjects,teachers",
    )

    subjects = relationship(
        "Subject",
        secondary="teaching_assignments",
        back_populates="teachers",
        overlaps="departments,teachers",
    )
