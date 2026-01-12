from fastapi import HTTPException
from sqlalchemy import select
from uni.models.subjects_table import Subject


async def get_subject_or_404(db, subject_id: int):
    result = await db.execute(select(Subject).where(Subject.subject_id == subject_id))
    subject = result.scalars().first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    return subject


async def create(db, subject):
    try:
        result = await db.execute(select(Subject).where(Subject.subject_name == subject.subject_name))
        subject_exist = result.scalars().first()
        
        if subject_exist:
            raise HTTPException(status_code=400, detail="Subject already exists")

        new_subject = Subject(
            subject_name=subject.subject_name,
            description=subject.description,
            credits=subject.credits,
        )

        db.add(new_subject)
        await db.commit()
        await db.refresh(new_subject)
        return new_subject
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating subject: {str(e)}")


async def update(db, subject_id, subject_data):
    try:
        subject = await get_subject_or_404(db, subject_id)

        for key, value in subject_data.items():
            setattr(subject, key, value)

        await db.commit()
        await db.refresh(subject)
        return subject
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating subject: {str(e)}")


async def delete(db, subject_id):
    try:
        subject = await get_subject_or_404(db, subject_id)
        await db.delete(subject)
        await db.commit()
        return {"detail": "Subject deleted successfully"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting subject: {str(e)}")


async def get(db, subject_id):
    try:
        return await get_subject_or_404(db, subject_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching subject: {str(e)}")


async def get_all(db):
    try:
        result = await db.execute(select(Subject))
        subjects = result.scalars().all()
        return subjects
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching subjects: {str(e)}"
        )
