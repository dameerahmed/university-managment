from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uni.database.connection import get_db
from uni.schemas.batches import BatchResponse, BatchUpdate, BatchCreate, massageResponse, BatchDropdownResponse
from uni.schemas.teachers import TeacherResponse
from uni.schemas.students import StudentResponse
from uni.schemas.results import ResultResponse
from uni.schemas.subjects import SubjectResponse
from uni.schemas.assosiations.batch_subjects import BatchSubjectResponse
from uni.schemas.frontend import DropdownResponse
from uni.utils.security import is_admin_user

from uni.logics.batches_logic import (
    create,
    update,
    delete,
    get_by_name,
    get_batch_teachers,
    get_batch_students,
    get_batch_subjects,
    get_batch_results,
    assign_subject,
    get_batches_dropdown,
)

router = APIRouter(prefix="/batches", tags=["batches"])


@router.post(
    "/create", dependencies=[Depends(is_admin_user)], response_model=BatchResponse
)
async def create_batch(batch: BatchCreate, db: Session = Depends(get_db)):
    return await create(db, batch)


@router.get(
    "/get/{batch_name}",
    dependencies=[Depends(is_admin_user)],
    response_model=BatchResponse,
)
async def get_batch(batch_name: str, db: Session = Depends(get_db)):
    return await get_by_name(db, batch_name)


@router.put(
    "/update/{batch_name}",
    dependencies=[Depends(is_admin_user)],
    response_model=BatchResponse,
)
async def update_batch(batch_name: str, batch: BatchUpdate, db: Session = Depends(get_db)):
    return await update(db, batch_name, batch)


@router.delete("/delete/{batch_name}", dependencies=[Depends(is_admin_user)])
async def delete_batch(batch_name: str, db: Session = Depends(get_db)):
    return await delete(db, batch_name)


@router.get(
    "/get_teachers/{batch_name}",
    dependencies=[Depends(is_admin_user)],
    response_model=list[TeacherResponse],
)
async def get_teachers(batch_name: str, db: Session = Depends(get_db)):
    return await get_batch_teachers(db, batch_name)


@router.get(
    "/get_students/{batch_name}",
    dependencies=[Depends(is_admin_user)],
    response_model=list[StudentResponse],
)
async def get_students(batch_name: str, db: Session = Depends(get_db)):
    return await get_batch_students(db, batch_name)


@router.get(
    "/get_subjects/{batch_name}",
    dependencies=[Depends(is_admin_user)],
    response_model=list[SubjectResponse],
)
async def get_subjects(batch_name: str, db: Session = Depends(get_db)):
    return await get_batch_subjects(db, batch_name)


@router.get(
    "/get_results/{batch_name}",
    dependencies=[Depends(is_admin_user)],
    response_model=list[ResultResponse],
)
async def get_results(batch_name: str, db: Session = Depends(get_db)):
    return await get_batch_results(db, batch_name)


@router.post(
    "/assign_subject/{batch_name}/{subject_id}",
    dependencies=[Depends(is_admin_user)],
    response_model=massageResponse,
)
async def assign_subject_to_batch(
    batch_name: str, subject_id: int, db: Session = Depends(get_db)
):
    return await assign_subject(db, batch_name, subject_id)


@router.get(
    "/dropdown",
    dependencies=[Depends(is_admin_user)],
    response_model=list[BatchDropdownResponse],
)
async def get_dropdown(department_id: int = None, db: Session = Depends(get_db)):
    return await get_batches_dropdown(db, department_id)
