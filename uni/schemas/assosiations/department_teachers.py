from pydantic import BaseModel
from typing import Optional


class DepartmentTeacherCreate(BaseModel):
    department_id: int
    teacher_id: int


class DepartmentTeacherUpdate(BaseModel):
    department_id: Optional[int]
    teacher_id: Optional[int]


class DepartmentTeacherResponse(BaseModel):
    department_id: Optional[int]
    teacher_id: Optional[int]

    class Config:
        model_config = {"from_attributes": True}
