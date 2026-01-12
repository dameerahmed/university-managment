from datetime import date
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from pydantic import EmailStr
from uni.models import User, Student, Department, Batch
from uni.utils.security import hash_password
from uni.utils.error_handler import handle_exception
from sqlalchemy.orm import joinedload


async def create(db: AsyncSession, student):
    try:
        stmt = select(User).where(User.email == student.email)
        result = await db.execute(stmt)
        student_exist = result.scalars().first()

        if student_exist:
            raise HTTPException(status_code=400, detail="Email already registered")

        if student.date_of_birth >= date.today():
            raise HTTPException(status_code=400, detail="Invalid date of birth")

        stmt = select(Department).where(
            Department.department_id == student.department_id
        )
        result = await db.execute(stmt)
        department = result.scalars().first()

        if not department:
            raise HTTPException(status_code=400, detail="Invalid department ID")

        stmt = select(Batch).where(Batch.batch_id == student.batch_id)
        result = await db.execute(stmt)
        batch = result.scalars().first()

        if not batch:
            raise HTTPException(status_code=400, detail="Invalid batch ID")

        if batch.department_id != student.department_id:
            raise HTTPException(
                status_code=400, detail="Batch does not belong to given department"
            )

        stmt = select(Student).where(
            Student.roll_number == student.roll_number,
            Student.batch_id == student.batch_id,
        )
        result = await db.execute(stmt)
        roll_number_exist = result.scalars().first()

        if roll_number_exist:
            raise HTTPException(
                status_code=400, detail="Roll number already exists in this batch"
            )

        count_stmt = (
            select(func.count())
            .select_from(Student)
            .where(Student.batch_id == student.batch_id)
        )
        count_result = await db.execute(count_stmt)
        current_students_count = count_result.scalar()

        if batch.seats_limit <= current_students_count:
            raise HTTPException(status_code=400, detail="Batch seat limit reached")

        user = User(
            email=student.email,
            user_name=f"{student.first_name} {student.last_name}",
            user_role="STUDENT",
            password=hash_password(student.password),
        )
        db.add(user)
        await db.flush()

        new_student = Student(
            user_id=user.user_id,
            first_name=student.first_name,
            last_name=student.last_name,
            father_name=student.father_name,
            mother_name=student.mother_name,
            roll_number=student.roll_number,
            date_of_birth=student.date_of_birth,
            department_id=student.department_id,
            batch_id=student.batch_id,
            address=student.address,
            phone_number=student.phone_number,
        )
        db.add(new_student)
        await db.commit()
        
        # Re-fetch with eager loading for response schema
        stmt = select(Student).options(joinedload(Student.department)).where(Student.student_id == new_student.student_id)
        result = await db.execute(stmt)
        return result.scalars().first()

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating student: {str(e)}")


async def get_student_or_404(db, roll_number: str):
    result = await db.execute(
        select(Student)
        .options(joinedload(Student.department))
        .where(Student.roll_number == roll_number)
    )
    student = result.scalars().first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


async def get(db, roll_number: str):
    try:
        return await get_student_or_404(db, roll_number)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching student: {str(e)}")


async def update(db, roll_number: str, student_data):
    try:
        student = await get_student_or_404(db, roll_number)

        if student_data.date_of_birth:
            if student_data.date_of_birth >= date.today():
                raise HTTPException(status_code=400, detail="Invalid date of birth")
        if student_data.department_id:
            result = await db.execute(
                select(Department).where(
                    Department.department_id == student_data.department_id
                )
            )
            department = result.scalars().first()
            if not department:
                raise HTTPException(status_code=400, detail="Invalid department ID")

        if student_data.batch_id:
            result = await db.execute(
                select(Batch).where(Batch.batch_id == student.batch_id)
            )
            batch = result.scalars().first()

            if not batch:
                raise HTTPException(status_code=400, detail="Invalid batch ID")

        if student_data.roll_number:
            result = await db.execute(
                select(Student).where(
                    Student.roll_number == student_data.roll_number,
                    Student.batch_id == student_data.batch_id,
                )
            )
            roll_number_exist = result.scalars().first()
            if roll_number_exist:
                raise HTTPException(
                    status_code=400, detail="Roll number already exists in this batch"
                )

        # Check seat limit if batch is changing or new student (update logic usually doesn't change batch often but if it does...)
        # Logic here seems to check seat limit of the *current* batch of the student?
        # Line 161 in original was: .filter(Student.batch_id == student_data.batch_id)
        # So it checks the target batch.

        if student_data.batch_id:
            result = await db.execute(
                select(func.count())
                .select_from(Student)
                .where(Student.batch_id == student_data.batch_id)
            )
            count = result.scalar()

            # We need to fetch the batch to get seats_limit if we haven't already
            if "batch" not in locals():
                result = await db.execute(
                    select(Batch).where(Batch.batch_id == student_data.batch_id)
                )
                batch = result.scalars().first()

            if batch.seats_limit <= count:
                raise HTTPException(status_code=400, detail="Batch seat limit reached")

        for key, value in student_data.dict(exclude_unset=True).items():
            setattr(student, key, value)

        await db.commit()
        await db.refresh(student)
        return student
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating student: {str(e)}")


async def delete(db, roll_number: str):
    try:
        student = await get_student_or_404(db, roll_number)
        await db.delete(student)
        await db.commit()
        return {"message": "Student deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting student: {str(e)}")


# uni/logics/students_logics.py


async def get_filtered_students(
    db,
    current_user,
    department_id: int = None,
    batch_id: int = None,
    roll_number: str = None,
    search: str = None,
):
    if current_user["user_role"] != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    query = select(Student).options(
        joinedload(Student.department), joinedload(Student.batches)
    )

    # --- FILTERS ---
    if department_id:
        query = query.where(Student.department_id == department_id)

    if batch_id:
        query = query.where(Student.batch_id == batch_id)

    # Agar specific roll number aaya hai, to bas wahi dikhao
    if roll_number:
        query = query.where(Student.roll_number == roll_number)

    if search:
        search_fmt = f"%{search}%"
        query = query.where(
            (Student.first_name.ilike(search_fmt))
            | (Student.last_name.ilike(search_fmt))
            | (Student.roll_number.ilike(search_fmt))
        )

    result = await db.execute(query)
    return result.scalars().all()


async def get_class_roll_numbers(department_id: int, batch_id: int, db, current_user):
    if current_user["user_role"] != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    stmt = select(Student.roll_number).where(
        Student.department_id == department_id, Student.batch_id == batch_id
    )
    result = await db.execute(stmt)
    return result.scalars().all()
