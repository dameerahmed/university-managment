from fastapi import HTTPException
from datetime import datetime
from uni.models import Subject, Teacher, Student, Result
from uni.models import Batch, Department
from sqlalchemy import select, func
from uni.models.assosiations import batch_subjects
from uni.schemas.assosiations.batch_subjects import BatchSubjectResponse
from uni.utils.error_handler import handle_exception


async def get_batch_or_404(db, batch_name: str):
    result = await db.execute(select(Batch).where(Batch.batch_name == batch_name.upper()))
    batch = result.scalars().first()
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")
    return batch


async def get_department_or_404(db, department_id: int):
    result = await db.execute(select(Department).where(Department.department_id == department_id))
    department = result.scalars().first()
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    return department


async def create(db, batch):
    try:
        await get_department_or_404(db, batch.department_id)
        
        result = await db.execute(select(Batch).where(Batch.batch_name == batch.batch_name.upper()))
        batch_name_exist = result.scalars().first()
        
        if batch_name_exist:
            raise HTTPException(status_code=400, detail="Batch name already exists")

        result = await db.execute(select(func.count()).select_from(Batch).where(Batch.department_id == batch.department_id))
        batch_count = result.scalar()
        
        if batch_count >= 4:
            raise HTTPException(
                status_code=400, detail="4 Batches already exist in this department"
            )
        if batch.seats_limit <= 0:
            raise HTTPException(
                status_code=400, detail="Seats limit must be greater than 0"
            )

        new_batch = Batch(
            batch_name=batch.batch_name.upper(),
            department_id=batch.department_id,
            seats_limit=batch.seats_limit,
        )
        db.add(new_batch)
        await db.commit()
        await db.refresh(new_batch)
        return new_batch

    except Exception as e:
        await handle_exception(db, e, "creating batch")


async def update(db, batch_name: str, batch_data):
    try:
        batch = await get_batch_or_404(db, batch_name)
        
        result = await db.execute(
            select(Batch)
            .where(
                Batch.batch_name == batch_data.batch_name.upper(),
                Batch.batch_name != batch_name.upper(),
            )
        )
        batch_name_exist = result.scalars().first()
        
        if batch_name_exist:
            raise HTTPException(status_code=400, detail="Batch name already exists")
        await get_department_or_404(db, batch_data.department_id)

        for key, value in batch_data.dict(exclude_unset=True).items():
            setattr(batch, key, value)

        await db.commit()
        await db.refresh(batch)
        return batch
    except Exception as e:
        await handle_exception(db, e, "updating batch")


async def delete(db, batch_name: str):
    try:
        batch = await get_batch_or_404(db, batch_name)
        await db.delete(batch)
        await db.commit()
        return batch
    except Exception as e:
        await handle_exception(db, e, "deleting batch")


async def get_by_name(db, batch_name: str):
    try:
        batch = await get_batch_or_404(db, batch_name)
        return batch
    except Exception as e:
        await handle_exception(db, e, "getting batch by name")


async def get_batch_teachers(db, batch_name: str):
    try:
        # Teachers are linked to Subjects, and Batches have Subjects.
        # So we find teachers who teach subjects that are in this batch.
        batch = await get_batch_or_404(db, batch_name)
        
        # This query joins Teacher -> Subject -> Batch
        stmt = (
            select(Teacher)
            .join(Teacher.subjects)
            .join(Subject.batches)
            .where(Batch.batch_id == batch.batch_id)
            .distinct()
        )
        result = await db.execute(stmt)
        return result.scalars().all()
    except Exception as e:
        await handle_exception(db, e, "getting batch teachers")


async def get_batch_students(db, batch_name: str):
    try:
        batch = await get_batch_or_404(db, batch_name)
        result = await db.execute(select(Student).where(Student.batch_id == batch.batch_id))
        return result.scalars().all()
    except Exception as e:
        await handle_exception(db, e, "getting batch students")


async def get_batch_subjects(db, batch_name: str):
    try:
        batch = await get_batch_or_404(db, batch_name)
        result = await db.execute(select(Subject).join(Batch.subjects).where(Batch.batch_id == batch.batch_id))
        return result.scalars().all()
    except Exception as e:
        await handle_exception(db, e, "getting batch subjects")


async def get_batch_results(db, batch_name: str):
    try:
        batch = await get_batch_or_404(db, batch_name)
        result = await db.execute(select(Result).where(Result.batch_id == batch.batch_id))
        return result.scalars().all()
    except Exception as e:
        await handle_exception(db, e, "getting batch results")


async def assign_subject(db, batch_name: str, subject_id: int):
    try:
        batch = await get_batch_or_404(db, batch_name)

        result = await db.execute(select(Subject).where(Subject.subject_id == subject_id))
        subject = result.scalars().first()
        if not subject:
            raise HTTPException(status_code=404, detail="Subject not found")

        # Check if subject is already assigned
        # We can check the association table directly or use the relationship query
        check_stmt = select(Batch).join(Batch.subjects).where(
            Batch.batch_id == batch.batch_id,
            Subject.subject_id == subject.subject_id
        )
        result = await db.execute(check_stmt)
        if result.scalars().first():
             raise HTTPException(
                status_code=400, detail="Subject already assigned to batch"
            )

        insert_stmt = batch_subjects.insert().values(
            batch_id=batch.batch_id, subject_id=subject.subject_id
        )
        await db.execute(insert_stmt)
        await db.commit()
        # await db.refresh(batch) # Refresh might not load the new subject immediately without eager load options
        return {
            "detail": f"Subject '{subject.subject_name}' assigned to batch '{batch.batch_name}' successfully"
        }
    except Exception as e:
        await handle_exception(db, e, "assigning subject to batch")


async def get_batches_dropdown(db, department_id: int = None):
    query = select(
        Batch.batch_id.label("batch_id"),
        Batch.batch_name.label("batch_name"),
        Batch.department_id.label("department_id"),
    )
    
    if department_id:
        query = query.where(Batch.department_id == department_id)
        
    result = await db.execute(query)
    return result.all()
