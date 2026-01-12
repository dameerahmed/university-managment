from pydantic import BaseModel
from typing import Optional


class DepartmentBatchCreate(BaseModel):
    department_id: int
    batch_id: int


class DepartmentBatchUpdate(BaseModel):
    department_id: Optional[int]
    batch_id: Optional[int]


class DepartmentBatchResponse(BaseModel):
    department_id: Optional[int]
    batch_id: Optional[int]

    class Config:
        model_config = {"from_attributes": True}
