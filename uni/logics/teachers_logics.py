from fastapi import HTTPException
from sqlalchemy import select, and_
from uni.models.teachers_table import Teacher
from uni.models.users_table import User
from uni.models.batches_table import Batch
from uni.models.subjects_table import Subject
from uni.models.departments_table import Department
from uni.models.assosiations import teaching_assignments
from uni.schemas.users import UserRole
from uni.schemas.teachers import TeacherAssign
from uni.utils.security import hash_password


async def get_teacher_or_404(db, email: str):
    result = await db.execute(select(Teacher).where(Teacher.email == email))
    teacher = result.scalars().first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return teacher


async def create(db, teacher):
    try:
        result = await db.execute(select(User).where(User.email == teacher.email))
        existing_teacher = result.scalars().first()
        if existing_teacher:
            raise HTTPException(status_code=400, detail="Email already registered")

        user_data = User(
            email=teacher.email,
            user_name=f"{teacher.first_name} {teacher.last_name}",
            user_role=UserRole.TEACHER,
            password=hash_password(teacher.password),
        )
        db.add(user_data)
        await db.flush()

        teacher_data = Teacher(
            user_id=user_data.user_id,
            first_name=teacher.first_name,
            last_name=teacher.last_name,
            hire_date=teacher.hire_date,
            address=teacher.address,
            phone_number=teacher.phone_number,
        )
        db.add(teacher_data)
        await db.commit()

        await db.refresh(user_data)
        await db.refresh(teacher_data)

        return teacher_data
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating teacher: {str(e)}")


async def get(db, email):
    try:
        return await get_teacher_or_404(db, email)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching teacher: {str(e)}")


async def update(db, email, teacher_data):
    try:
        teacher = await get_teacher_or_404(db, email)

        for key, value in teacher_data.items():
            setattr(teacher, key, value)

        await db.commit()
        await db.refresh(teacher)
        return teacher
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating teacher: {str(e)}")


async def delete(db, email):
    try:
        teacher = await get_teacher_or_404(db, email)
        await db.delete(teacher)
        await db.commit()
        return {"detail": "Teacher deleted successfully"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting teacher: {str(e)}")


async def get_all(db):
    try:
        result = await db.execute(select(Teacher))
        teachers = result.scalars().all()
        return teachers
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching teachers: {str(e)}"
        )


async def assign_teacher(db, teacher_data):
    try:
        result = await db.execute(select(Teacher).where(Teacher.teacher_id == teacher_data.teacher_id))
        teacher = result.scalars().first()
        if not teacher:
            raise HTTPException(status_code=404, detail="Teacher not found")

        result = await db.execute(select(Batch).where(Batch.batch_id == teacher_data.batch_id))
        batch = result.scalars().first()
        if not batch:
            raise HTTPException(status_code=404, detail="Batch not found")

        result = await db.execute(select(Department).where(Department.department_id == teacher_data.department_id))
        department = result.scalars().first()
        if not department:
            raise HTTPException(status_code=404, detail="Department not found")

        result = await db.execute(select(Subject).where(Subject.subject_id == teacher_data.subject_id))
        subject = result.scalars().first()
        if not subject:
            raise HTTPException(status_code=404, detail="Subject not found")
        
        # Check explicit relationships or association tables
        # Subject in Department?
        # department.subjects is a relationship. In async we need to load it or check association table.
        # Checking association table is safer/faster.
        stmt = select(teaching_assignments).where(
             and_(
                 teaching_assignments.c.department_id == teacher_data.department_id,
                 teaching_assignments.c.subject_id == teacher_data.subject_id
             )
        )
        # Wait, this checks teaching_assignments. We need to check department_subjects.
        # But wait, original code checked `if subject not in department.subjects`.
        # So we should check `department_subjects` table.
        from uni.models.assosiations import department_subjects
        stmt = select(department_subjects).where(
            and_(
                department_subjects.c.department_id == teacher_data.department_id,
                department_subjects.c.subject_id == teacher_data.subject_id
            )
        )
        result = await db.execute(stmt)
        if not result.first():
             raise HTTPException(
                status_code=400, detail="Subject not assigned to department"
            )

        # Subject in Batch?
        from uni.models.assosiations import batch_subjects
        stmt = select(batch_subjects).where(
            and_(
                batch_subjects.c.batch_id == teacher_data.batch_id,
                batch_subjects.c.subject_id == teacher_data.subject_id
            )
        )
        result = await db.execute(stmt)
        if not result.first():
            raise HTTPException(status_code=400, detail="Subject not assigned to batch")

        stmt = select(teaching_assignments).where(
            and_(
                teaching_assignments.c.subject_id == teacher_data.subject_id,
                teaching_assignments.c.batch_id == teacher_data.batch_id,
                teaching_assignments.c.department_id == teacher_data.department_id,
            )
        )
        result = await db.execute(stmt)
        existing_teacher = result.first()
        
        if existing_teacher:
            raise HTTPException(
                status_code=400, detail="Subject already assigned to another teacher"
            )
            
        stmt = select(teaching_assignments).where(
            and_(
                teaching_assignments.c.teacher_id == teacher_data.teacher_id,
                teaching_assignments.c.subject_id == teacher_data.subject_id,
                teaching_assignments.c.batch_id == teacher_data.batch_id,
                teaching_assignments.c.department_id == teacher_data.department_id,
            )
        )
        result = await db.execute(stmt)
        duplicate_assignment = result.first()

        if duplicate_assignment:
            raise HTTPException(status_code=400, detail="Duplicate teaching assignment")

        assignment = teaching_assignments.insert().values(
            teacher_id=teacher_data.teacher_id,
            subject_id=teacher_data.subject_id,
            batch_id=teacher_data.batch_id,
            department_id=teacher_data.department_id,
            semester=teacher_data.semester,
        )

        await db.execute(assignment)
        await db.commit()
        return {
            "massage": "Teacher assigned to batch successfully",
            "teacher_name": teacher.first_name + " " + teacher.last_name,
            "department_code": department.department_code,
            "batch_name": batch.batch_name, # Fixed: batch.name -> batch.batch_name
            "subject_name": subject.subject_name, # Fixed: subject.name -> subject.subject_name
            "semester": teacher_data.semester,
        }
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=500, detail=f"Error assigning teacher to batch: {str(e)}"
        )
