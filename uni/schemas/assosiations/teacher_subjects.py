from pydantic import BaseModel
from typing import Optional


class TeacherSubjectCreate(BaseModel):
    teacher_id: int
    subject_id: int


class TeacherSubjectUpdate(BaseModel):
    teacher_id: Optional[int]
    subject_id: Optional[int]


class TeacherSubjectResponse(BaseModel):
    teacher_id: Optional[int]
    subject_id: Optional[int]

    class Config:
        model_config = {"from_attributes": True}
