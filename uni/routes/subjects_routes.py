from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uni.database.connection import get_db
from uni.schemas.subjects import SubjectCreate, SubjectUpdate, SubjectResponse
from uni.logics.subjects_logics import create, get, update, delete, get_all

router = APIRouter(prefix="/subjects", tags=["subjects"])


@router.post("/create", response_model=SubjectResponse)
async def create_subject(subject: SubjectCreate, db: Session = Depends(get_db)):
    return await create(db, subject)


@router.get("/get/{subject_id}", response_model=SubjectResponse)
async def get_subject(subject_id: str, db: Session = Depends(get_db)):
    return await get(db, subject_id)


@router.get("/get_all", response_model=list[SubjectResponse])
async def get_all_subjects(db: Session = Depends(get_db)):
    return await get_all(db)


@router.put("/update/{subject_id}", response_model=SubjectResponse)
async def update_subject(
    subject_id: str, subject: SubjectUpdate, db: Session = Depends(get_db)
):
    return await update(db, subject_id, subject)


@router.delete("/delete/{subject_id}")
async def delete_subject(subject_id: str, db: Session = Depends(get_db)):
    return await delete(db, subject_id)
