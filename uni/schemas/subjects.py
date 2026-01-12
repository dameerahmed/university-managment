from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class SubjectCreate(BaseModel):
    subject_name: str
    description: Optional[str] = None
    credits: int


class SubjectUpdate(BaseModel):
    subject_name: Optional[str] = None
    description: Optional[str] = None
    credits: Optional[int] = None


class SubjectResponse(BaseModel):
    subject_id: Optional[int] = None
    subject_name: Optional[str] = None
    description: Optional[str] = None
    credits: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        model_config = {"from_attributes": True}
