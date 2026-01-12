from pydantic import BaseModel
from typing import Optional


class BatchSubjectCreate(BaseModel):
    batch_id: int
    subject_id: int


class BatchSubjectUpdate(BaseModel):
    batch_id: Optional[int]
    subject_id: Optional[int]


class BatchSubjectResponse(BaseModel):
    massage: str
    batch_id: Optional[int] = None
    subject_id: Optional[int] = None

    class Config:
        model_config = {"from_attributes": True}
