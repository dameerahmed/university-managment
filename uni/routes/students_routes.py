from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uni.database.connection import get_db
from uni.schemas.students import StudentCreate, StudentUpdate, StudentResponse
from uni.logics.students_logics import (
    create,
    get,
    update,
    delete,
    get_filtered_students,
    get_class_roll_numbers,
)
from uni.utils.security import get_current_user
from typing import List, Optional
from uni.schemas.frontend import DropdownResponse

router = APIRouter(prefix="/students", tags=["students"])


@router.post("/create", response_model=StudentResponse)
async def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    return await create(db, student)


@router.get("/get/{roll_number}", response_model=StudentResponse)
async def get_student(roll_number: str, db: Session = Depends(get_db)):
    return await get(db, roll_number)


@router.put("/update/{roll_number}", response_model=StudentResponse)
async def update_student(
    roll_number: str, student: StudentUpdate, db: Session = Depends(get_db)
):
    return await update(db, roll_number, student)


@router.delete("/delete/{roll_number}")
async def delete_student(roll_number: str, db: Session = Depends(get_db)):
    return await delete(db, roll_number)


@router.get("/get_all", response_model=list[StudentResponse])
async def get_all_students(db: Session = Depends(get_db)):
    return await get_all(db)


# uni/routers/students.py


@router.get("/", response_model=List[StudentResponse])
async def read_students(
    department_id: Optional[int] = None,
    batch_id: Optional[int] = None,
    roll_number: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return await get_filtered_students(
        db, current_user, department_id, batch_id, roll_number, search
    )


@router.get("/class_roll_numbers", response_model=List[str])
async def get_roll_numbers(
    department_id: int,
    batch_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return await get_class_roll_numbers(department_id, batch_id, db, current_user)
