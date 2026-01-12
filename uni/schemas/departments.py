from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class DepartmentCreate(BaseModel):
    department_name: str
    department_code: str

    class Config:
        model_config = {"from_attributes": True}


class DepartmentUpdate(BaseModel):
    department_name: Optional[str] = None
    department_code: Optional[str] = None


class MessageResponse(BaseModel):
    detail: str

    class Config:
        model_config = {"from_attributes": True}


class DepartmentResponse(BaseModel):
    department_id: Optional[int] = None
    department_name: Optional[str] = None
    department_code: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        model_config = {"from_attributes": True}


class DepartmentDropdownResponse(BaseModel):
    department_id: int
    department_name: str

    class Config:
        model_config = {"from_attributes": True}
