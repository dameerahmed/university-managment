from pydantic import BaseModel
from typing import Optional


class DepartSubjectCreate(BaseModel):
    department_id: int
    subject_id: int


class DepartSubjectUpdate(BaseModel):
    department_id: Optional[int]
    subject_id: Optional[int]


class DepartSubjectResponse(BaseModel):
    message: str
    department_id: int
    subject_id: int

    class Config:
        model_config = {"from_attributes": True}
