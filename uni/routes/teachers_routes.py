from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uni.database.connection import get_db
from uni.schemas.teachers import (
    TeacherCreate,
    TeacherUpdate,
    TeacherResponse,
    TeacherAssign,
    TeacherAssignResponse,
)
from uni.logics.teachers_logics import (
    create,
    get,
    update,
    delete,
    get_all,
    assign_teacher,
)

router = APIRouter(prefix="/teachers", tags=["teachers"])


@router.post("/create", response_model=TeacherResponse)
async def create_teacher(teacher: TeacherCreate, db: Session = Depends(get_db)):
    return await create(db, teacher)


@router.get("/get/{email}", response_model=TeacherResponse)
async def get_teacher(email: str, db: Session = Depends(get_db)):
    return await get(db, email)


@router.put("/update/{email}", response_model=TeacherResponse)
async def update_teacher(email: str, teacher: TeacherUpdate, db: Session = Depends(get_db)):
    return await update(db, email, teacher)


@router.delete("/delete/{email}")
async def delete_teacher(email: str, db: Session = Depends(get_db)):
    return await delete(db, email)


@router.get("/get_all", response_model=list[TeacherResponse])
async def get_all_teachers(db: Session = Depends(get_db)):
    return await get_all(db)


@router.post("/assign", response_model=TeacherAssignResponse)
async def assign_teacher_to_batch(teacher_data: TeacherAssign, db: Session = Depends(get_db)):
    return await assign_teacher(db, teacher_data)
