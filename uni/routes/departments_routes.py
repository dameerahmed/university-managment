from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from uni.database.connection import get_db
from uni.schemas.departments import (
    DepartmentCreate,
    DepartmentUpdate,
    DepartmentResponse,
    MessageResponse,
    DepartmentDropdownResponse,
)

from uni.schemas.assosiations.department_subjects import (
    DepartSubjectCreate,
    DepartSubjectResponse,
)

from uni.schemas.batches import BatchResponse
from uni.schemas.students import StudentResponse
from uni.schemas.teachers import TeacherResponse
from uni.schemas.subjects import SubjectResponse
from uni.logics.departments_logics import (
    create,
    get,
    update,
    delete,
    get_all,
    get_department_batches,
    get_department_students,
    get_department_teachers,
    get_department_subjects,
    get_department_subjects,
    assign_subject,
    get_departments_dropdown,
)
from uni.utils.security import is_admin_user


router = APIRouter(
    prefix="/departments", tags=["departments"], dependencies=[Depends(is_admin_user)]
)


@router.post("/create", response_model=DepartmentResponse)
async def create_department(department: DepartmentCreate, db: Session = Depends(get_db)):
    return await create(db, department)


@router.get("/all", response_model=List[DepartmentResponse])
async def get_all_departments(db: Session = Depends(get_db)):
    return await get_all(db)


@router.get("/dropdown", response_model=List[DepartmentDropdownResponse])
async def get_dropdown(db: Session = Depends(get_db)):
    return await get_departments_dropdown(db)


@router.get("/{department_code}", response_model=DepartmentResponse)
async def get_department(department_code: str, db: Session = Depends(get_db)):
    return await get(db, department_code)


@router.put("/{department_code}", response_model=DepartmentResponse)
async def update_department(
    department_code: str, department: DepartmentUpdate, db: Session = Depends(get_db)
):
    return await update(db, department_code, department)


@router.delete("/{department_code}", response_model=MessageResponse)
async def delete_department(department_code: str, db: Session = Depends(get_db)):
    return await delete(db, department_code)


@router.get("/batches/{department_code}", response_model=List[BatchResponse])
async def get_batches(department_code: str, db: Session = Depends(get_db)):
    return await get_department_batches(db, department_code)


@router.get("/students/{department_code}", response_model=List[StudentResponse])
async def get_students(department_code: str, db: Session = Depends(get_db)):
    return await get_department_students(db, department_code)


@router.get("/teachers/{department_code}", response_model=List[TeacherResponse])
async def get_teachers(department_code: str, db: Session = Depends(get_db)):
    return await get_department_teachers(db, department_code)


@router.get("/subjects/{department_code}", response_model=List[SubjectResponse])
async def get_subjects(department_code: str, db: Session = Depends(get_db)):
    return await get_department_subjects(db, department_code)


@router.post("/assign_subject/{department_code}", response_model=DepartSubjectResponse)
async def assign_department_subject(
    department_code: str, subject: DepartSubjectCreate, db: Session = Depends(get_db)
):
    return await assign_subject(db, subject, department_code)



