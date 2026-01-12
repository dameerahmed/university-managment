from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from pydantic import EmailStr


class TeacherCreate(BaseModel):
    first_name: str
    last_name: str
    hire_date: datetime
    email: EmailStr
    password: str
    address: str
    phone_number: str


class TeacherUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    hire_date: Optional[datetime] = None
    address: Optional[str] = None
    phone_number: Optional[str] = None


class TeacherAssign(BaseModel):
    teacher_id: int = None
    department_id: int = None
    batch_id: int = None
    subject_id: int = None
    semester: int = None


class TeacherResponse(BaseModel):
    teacher_id: Optional[int] = None
    user_id: Optional[int] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    hire_date: Optional[datetime] = None
    address: Optional[str] = None
    phone_number: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        model_config = {"from_attributes": True}


class TeacherAssignResponse(BaseModel):
    massage: Optional[str] = None
    teacher_name: Optional[str] = None
    department_code: Optional[str] = None
    batch_name: Optional[str] = None
    subject_name: Optional[str] = None
    semester: Optional[int] = None

    class Config:
        model_config = {"from_attributes": True}
