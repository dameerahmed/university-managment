from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class BatchCreate(BaseModel):
    batch_name: str
    department_id: int
    seats_limit: int


class BatchUpdate(BaseModel):
    batch_name: Optional[str]
    department_id: Optional[int]
    seats_limit: Optional[int]


class massageResponse(BaseModel):
    detail: str

    class Config:
        model_config = {"from_attributes": True}


class BatchResponse(BaseModel):
    batch_id: Optional[int] = None
    batch_name: Optional[str] = None
    department_id: Optional[int] = None
    seats_limit: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        model_config = {"from_attributes": True}


class BatchDropdownResponse(BaseModel):
    batch_id: int
    batch_name: str
    department_id: int

    class Config:
        model_config = {"from_attributes": True}
