from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class ExamType(str, Enum):
    MIDTERM = "MIDTERM"
    FINAL = "FINAL"
    QUIZ = "QUIZ"
    ASSIGNMENT = "ASSIGNMENT"


class ResultCreate(BaseModel):
    student_id: int
    subject_id: int
    batch_id: int
    department_id: int
    semester: int
    exam_type: ExamType
    marks_obtained: float
    total_marks: float
    exam_date: Optional[datetime] = None


class ResultUpdate(BaseModel):
    student_id: Optional[int] = None
    subject_id: Optional[int] = None
    batch_id: Optional[int] = None
    department_id: Optional[int] = None
    semester: Optional[int] = None
    exam_type: Optional[ExamType] = None
    marks_obtained: Optional[float] = None
    total_marks: Optional[float] = None
    exam_date: Optional[datetime] = None


class ResultResponse(BaseModel):
    result_id: Optional[int] = None
    student_id: Optional[int] = None
    subject_id: Optional[int] = None
    batch_id: Optional[int] = None
    department_id: Optional[int] = None
    semester: Optional[int] = None
    exam_type: Optional[ExamType] = None
    marks_obtained: Optional[float] = None
    total_marks: Optional[float] = None
    grade: Optional[str] = None
    exam_date: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        model_config = {"from_attributes": True}
