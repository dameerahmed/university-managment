from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum


class UserRole(str, Enum):
    ADMIN = "admin"
    STUDENT = "student"
    TEACHER = "teacher"


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class UserUpdate_By_Admin(UserUpdate):
    user_name: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    message: Optional[str] = None
    user_name: Optional[str] = None
    email: Optional[EmailStr] = None
    user_role: Optional[UserRole] = None
    user_token: Optional[str] = None

    class Config:
        model_config = {"from_attributes": True}
