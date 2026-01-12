from fastapi import HTTPException
from sqlalchemy import and_, select
from uni.models import Department, Subject, Batch, Student, Teacher
from uni.models.assosiations import department_subjects
from uni.schemas.assosiations.department_subjects import DepartSubjectResponse
from uni.utils.error_handler import handle_exception


async def get_department_or_404(db, department_code: str):
    try:
        result = await db.execute(select(Department).where(Department.department_code == department_code.upper()))
        department = result.scalars().first()
        if not department:
            raise HTTPException(status_code=404, detail="Department not found")
        return department
    except HTTPException:
        raise
    except Exception as e:
        await handle_exception(db, e, "fetching department")


async def create(db, department):
    try:
        result = await db.execute(select(Department).where(Department.department_name == department.department_name.upper()))
        department_exist = result.scalars().first()
        
        if department_exist:
            raise HTTPException(
                status_code=400, detail="Department name already exists"
            )
        
        result = await db.execute(select(Department).where(Department.department_code == department.department_code.upper()))
        department_code_exist = result.scalars().first()

        if department_code_exist:
            raise HTTPException(
                status_code=400, detail="Department code already exists"
            )
        new_department = Department(
            department_name=department.department_name.upper(),
            department_code=department.department_code.upper(),
        )
        db.add(new_department)
        await db.commit()
        await db.refresh(new_department)
        return new_department
    except HTTPException:
        raise
    except Exception as e:
        await handle_exception(db, e, "creating department")


async def get(db, department_code: str):
    try:
        return await get_department_or_404(db, department_code)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


async def update(db, department_code: str, department_data):
    try:
        department = await get_department_or_404(db, department_code)
        
        result = await db.execute(
            select(Department)
            .where(
                Department.department_name == department_data.department_name.upper(),
                Department.department_name != department.department_name.upper(),
            )
        )
        department_name_exist = result.scalars().first()

        if department_name_exist:
            raise HTTPException(
                status_code=400, detail="Department name already exists"
            )

        result = await db.execute(
            select(Department)
            .where(
                Department.department_code == department_data.department_code.upper(),
                Department.department_code != department.department_code.upper(),
            )
        )
        department_code_exist = result.scalars().first()

        if department_code_exist:
            raise HTTPException(
                status_code=400, detail="Department code already exists"
            )
        if department_data.department_name is not None:
            department.department_name = department_data.department_name.upper()
        if department_data.department_code is not None:
            department.department_code = department_data.department_code.upper()
        await db.commit()
        await db.refresh(department)
        return department
    except HTTPException:
        raise
    except Exception as e:
        await handle_exception(db, e, "updating department")


async def delete(db, department_code: str):
    try:
        department = await get_department_or_404(db, department_code)
        
        # Check for related items using explicit queries
        # Students
        result = await db.execute(select(Student).where(Student.department_id == department.department_id))
        if result.scalars().first():
            raise HTTPException(status_code=400, detail="Department has students")

        # Teachers (via teaching_assignments, but usually teachers belong to department via user or direct link? 
        # Teacher model has 'departments' relationship via 'teaching_assignments'.
        # We check if any teacher is associated with this department.
        stmt = select(Teacher).join(Teacher.departments).where(Department.department_id == department.department_id)
        result = await db.execute(stmt)
        if result.scalars().first():
            raise HTTPException(status_code=400, detail="Department has teachers")

        # Batches
        result = await db.execute(select(Batch).where(Batch.department_id == department.department_id))
        if result.scalars().first():
            raise HTTPException(status_code=400, detail="Department has batches")

        await db.delete(department)
        await db.commit()
        return {"detail": "Department deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        await handle_exception(db, e, "deleting department")


async def get_all(db):
    try:
        result = await db.execute(select(Department))
        departments = result.scalars().all()
        return departments
    except Exception as e:
        await handle_exception(db, e, "fetching all departments")


async def get_department_batches(db, department_code: str):
    try:
        department = await get_department_or_404(db, department_code)
        result = await db.execute(select(Batch).where(Batch.department_id == department.department_id))
        return result.scalars().all()
    except Exception as e:
        await handle_exception(db, e, "fetching department batches")


async def get_department_students(db, department_code: str):
    try:
        department = await get_department_or_404(db, department_code)
        result = await db.execute(select(Student).where(Student.department_id == department.department_id))
        return result.scalars().all()
    except Exception as e:
        await handle_exception(db, e, "fetching department students")


async def get_department_teachers(db, department_code: str):
    try:
        department = await get_department_or_404(db, department_code)
        # Teachers associated via teaching_assignments
        stmt = select(Teacher).join(Teacher.departments).where(Department.department_id == department.department_id)
        result = await db.execute(stmt)
        return result.scalars().all()
    except Exception as e:
        await handle_exception(db, e, "fetching department teachers")


async def get_department_subjects(db, department_code: str):
    try:
        department = await get_department_or_404(db, department_code)
        # Subjects associated via department_subjects
        stmt = select(Subject).join(Subject.departments).where(Department.department_id == department.department_id)
        result = await db.execute(stmt)
        return result.scalars().all()
    except Exception as e:
        await handle_exception(db, e, "fetching department subjects")


async def assign_subject(db, subject_data, department_code: str):
    try:
        department = await get_department_or_404(db, department_code)

        result = await db.execute(select(Subject).where(Subject.subject_id == subject_data.subject_id))
        subject = result.scalars().first()
        
        if not subject:
            raise HTTPException(status_code=404, detail="Subject not found")
        
        stmt = select(department_subjects).where(
            and_(
                department_subjects.c.department_id == department.department_id,
                department_subjects.c.subject_id == subject.subject_id,
            )
        )
        result = await db.execute(stmt)
        existing = result.first()

        if existing:
            raise HTTPException(
                status_code=400, detail="Subject already assigned to department"
            )

        insert_stmt = department_subjects.insert().values(
            department_id=department.department_id, subject_id=subject.subject_id
        )
        await db.execute(insert_stmt)
        await db.commit()

        return DepartSubjectResponse(
            message="Subject assigned successfully",
            department_id=department.department_id,
            subject_id=subject.subject_id,
        )

    except Exception as e:
        await handle_exception(db, e, "assigning subject to department")


async def get_departments_dropdown(db):
    result = await db.execute(
        select(
            Department.department_id.label("department_id"),
            Department.department_name.label("department_name"),
        )
    )
    return result.all()
