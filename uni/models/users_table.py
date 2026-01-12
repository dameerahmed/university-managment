from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    func,
    Enum,
    ForeignKey,
)
from sqlalchemy.orm import relationship


from uni.database.connection import Base
from uni.schemas.users import UserRole


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_name = Column(String, nullable=False, index=True)
    user_role = Column(Enum(UserRole), nullable=False, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    students = relationship("Student", back_populates="user", uselist=False)

    teachers = relationship(
        "Teacher", back_populates="user", cascade="all, delete-orphan"
    )
