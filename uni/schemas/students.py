from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date, datetime
from uni.schemas.departments import DepartmentResponse


class StudentCreate(BaseModel):
    first_name: str
    last_name: str
    father_name: str
    mother_name: str
    roll_number: str
    batch_id: int
    department_id: int
    date_of_birth: date
    address: str
    phone_number: str
    email: EmailStr
    password: str


class StudentUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    father_name: Optional[str] = None
    mother_name: Optional[str] = None
    roll_number: Optional[str] = None
    batch_id: Optional[int] = None
    department_id: Optional[int] = None
    date_of_birth: Optional[date] = None
    address: Optional[str] = None
    phone_number: Optional[str] = None


class StudentResponse(BaseModel):
    student_id: int
    user_id: int
    first_name: str
    last_name: str
    father_name: str
    mother_name: str
    roll_number: str
    batch_id: int
    department_id: int
    date_of_birth: date
    address: str
    phone_number: str
    created_at: datetime
    updated_at: datetime
    department: Optional[DepartmentResponse] = None

    class Config:
        model_config = {"from_attributes": True}
