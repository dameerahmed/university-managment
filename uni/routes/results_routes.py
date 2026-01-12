from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uni.database.connection import get_db
from uni.schemas.results import ResultCreate, ResultUpdate, ResultResponse
from uni.logics.results_logics import (
    create_result,
    update_result,
    delete_result,
    get_all,
)

from uni.utils.security import get_current_user

router = APIRouter(prefix="/results", tags=["results"])


@router.get(
    "/{batch_name}/{subject_name}/{exam_type}", response_model=list[ResultResponse]
)
async def get_all_results(
    batch_name: str,
    subject_name: str,
    exam_type: str,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return await get_all(batch_name, subject_name, user, exam_type, db)


@router.post("/create", response_model=ResultResponse)
async def create_result(
    result: ResultCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return await create_result(current_user, db, result)


@router.put("/update/{result_id}", response_model=ResultResponse)
async def update_result(
    result_id: int,
    result: ResultUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return await update_result(db, result_id, result, current_user)


@router.delete("/delete/{result_id}")
async def delete_result(
    result_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return await delete_result(db, result_id, current_user)
