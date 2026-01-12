from pydantic import BaseModel
from typing import Optional


class BatchTeacherCreate(BaseModel):
    batch_id: int
    teacher_id: int


class BatchTeacherUpdate(BaseModel):
    batch_id: Optional[int]
    teacher_id: Optional[int]


class BatchTeacherResponse(BaseModel):
    batch_id: Optional[int]
    teacher_id: Optional[int]

    class Config:
        model_config = {"from_attributes": True}
