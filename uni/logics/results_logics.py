from fastapi import HTTPException, Depends
from sqlalchemy import select, and_
from uni.utils.error_handler import handle_exception
from uni.models import (
    department_subjects,
    teaching_assignments,
    Result,
    Student,
    Subject,
    Batch,
    Department,
)
from uni.utils.security import role_required
from enum import Enum


# ✅ Exam types as Enum
class ExamType(str, Enum):
    MIDTERM = "MIDTERM"
    FINAL = "FINAL"
    QUIZ = "QUIZ"
    ASSIGNMENT = "ASSIGNMENT"


# ✅ Grade calculation function
def calculate_grade(marks_obtained: float, total_marks: float) -> str:
    percentage = (marks_obtained / total_marks) * 100
    if percentage >= 85:
        return "A"
    elif percentage >= 70:
        return "B"
    elif percentage >= 60:
        return "C"
    elif percentage >= 50:
        return "D"
    return "F"


# ✅ Role-based access decorator


# =========================
# Get all results
# =========================
@role_required(["teacher", "admin"])
async def get_all(batch_name: str, subject_name: str, current_user: dict, exam_type: str, db):
    try:
        result = await db.execute(select(Batch).where(Batch.batch_name == batch_name))
        batch = result.scalars().first()
        if not batch:
            raise HTTPException(status_code=404, detail="Batch not found")

        result = await db.execute(select(Subject).where(Subject.subject_name == subject_name))
        subject = result.scalars().first()
        if not subject:
            raise HTTPException(status_code=404, detail="Subject not found")

        # Teacher-specific check
        if current_user["user_role"] == "teacher":
            stmt = select(teaching_assignments).where(
                and_(
                    teaching_assignments.c.teacher_id == current_user["user_id"],
                    teaching_assignments.c.batch_id == batch.batch_id,
                    teaching_assignments.c.department_id == batch.department_id,
                    teaching_assignments.c.subject_id == subject.subject_id,
                )
            )
            result = await db.execute(stmt)
            assigned = result.first()
            if not assigned:
                raise HTTPException(status_code=403, detail="Access denied")

        query = select(Result).where(
            Result.batch_id == batch.batch_id, Result.subject_id == subject.subject_id
        )

        if exam_type.upper() != "ALL":
            query = query.where(Result.exam_type == exam_type.upper())

        result = await db.execute(query)
        results = result.scalars().all()
        if not results:
            raise HTTPException(status_code=404, detail="No results found")

        return results

    except Exception as e:
        await db.rollback()
        return await handle_exception(db, e, action="get_all_results")


# =========================
# Create result
# =========================
@role_required(["teacher"])
async def create_result(current_user, db, result_data):
    try:
        result = await db.execute(select(Student).where(Student.student_id == result_data.student_id))
        student = result.scalars().first()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        result = await db.execute(select(Subject).where(Subject.subject_id == result_data.subject_id))
        subject = result.scalars().first()
        if not subject:
            raise HTTPException(status_code=404, detail="Subject not found")

        result = await db.execute(select(Batch).where(Batch.batch_id == result_data.batch_id))
        batch = result.scalars().first()
        if not batch:
            raise HTTPException(status_code=404, detail="Batch not found")

        result = await db.execute(select(Department).where(Department.department_id == result_data.department_id))
        department = result.scalars().first()
        if not department:
            raise HTTPException(status_code=404, detail="Department not found")

        # Student must belong to batch/department
        if (
            student.batch_id != result_data.batch_id
            or student.department_id != result_data.department_id
        ):
            raise HTTPException(
                status_code=400,
                detail="Student does not belong to this batch/department",
            )

        # Subject assignment
        stmt = select(department_subjects).where(
            and_(
                department_subjects.c.subject_id == result_data.subject_id,
                department_subjects.c.department_id == result_data.department_id,
            )
        )
        result = await db.execute(stmt)
        assigned_subject = result.first()
        if not assigned_subject:
            raise HTTPException(
                status_code=400, detail="Subject not assigned to this department"
            )

        # Teacher assignment
        stmt = select(teaching_assignments).where(
            and_(
                teaching_assignments.c.teacher_id == current_user["user_id"],
                teaching_assignments.c.subject_id == result_data.subject_id,
                teaching_assignments.c.batch_id == result_data.batch_id,
                teaching_assignments.c.department_id == result_data.department_id,
            )
        )
        result = await db.execute(stmt)
        teacher_assignment = result.first()
        
        if not teacher_assignment:
            raise HTTPException(
                status_code=403, detail="You are not assigned to this subject/batch"
            )

        # Exam type validation
        try:
            exam_type = ExamType(result_data.exam_type.upper())
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid exam type")

        # Marks validation
        if result_data.total_marks <= 0 or result_data.marks_obtained < 0:
            raise HTTPException(status_code=400, detail="Invalid marks")
        if result_data.marks_obtained > result_data.total_marks:
            raise HTTPException(
                status_code=400, detail="Marks obtained cannot exceed total marks"
            )

        # Duplicate check
        stmt = select(Result).where(
            and_(
                Result.student_id == result_data.student_id,
                Result.subject_id == result_data.subject_id,
                Result.exam_type == exam_type.value,
                Result.semester == result_data.semester,
            )
        )
        result = await db.execute(stmt)
        duplicate_result = result.scalars().first()
        
        if duplicate_result:
            raise HTTPException(status_code=400, detail="Duplicate result entry")

        # Grade
        grade = calculate_grade(result_data.marks_obtained, result_data.total_marks)

        new_result = Result(
            student_id=result_data.student_id,
            subject_id=result_data.subject_id,
            batch_id=result_data.batch_id,
            department_id=result_data.department_id,
            semester=result_data.semester,
            exam_type=exam_type.value,
            marks_obtained=result_data.marks_obtained,
            total_marks=result_data.total_marks,
            grade=grade,
            exam_date=result_data.exam_date,
        )

        db.add(new_result)
        await db.commit()
        await db.refresh(new_result)
        return new_result

    except Exception as e:
        await db.rollback()
        return await handle_exception(db, e, action="create_result")


# =========================
# Update result
# =========================
@role_required(["teacher", "admin"])
async def update_result(db, result_id, result_data, current_user):
    try:
        result = await db.execute(select(Result).where(Result.result_id == result_id))
        result_obj = result.scalars().first()
        if not result_obj:
            raise HTTPException(status_code=404, detail="Result not found")

        # Teacher-specific check
        if current_user["user_role"] == "teacher":
            stmt = select(teaching_assignments).where(
                and_(
                    teaching_assignments.c.teacher_id == current_user["user_id"],
                    teaching_assignments.c.subject_id == result_obj.subject_id,
                    teaching_assignments.c.batch_id == result_obj.batch_id,
                    teaching_assignments.c.department_id == result_obj.department_id,
                )
            )
            result = await db.execute(stmt)
            assigned = result.first()
            if not assigned:
                raise HTTPException(
                    status_code=403, detail="You are not assigned to this subject"
                )

        data = result_data.dict()

        # Exam type validation
        try:
            exam_type = ExamType(data["exam_type"].upper())
            data["exam_type"] = exam_type.value
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid exam type")

        # Marks validation
        if data["total_marks"] <= 0 or data["marks_obtained"] < 0:
            raise HTTPException(status_code=400, detail="Invalid marks")
        if data["marks_obtained"] > data["total_marks"]:
            raise HTTPException(
                status_code=400, detail="Marks obtained cannot exceed total marks"
            )

        # Duplicate check (exam_date remains same)
        stmt = select(Result).where(
            and_(
                Result.student_id == data["student_id"],
                Result.subject_id == data["subject_id"],
                Result.batch_id == data["batch_id"],
                Result.department_id == data["department_id"],
                Result.semester == data["semester"],
                Result.exam_type == data["exam_type"],
                Result.exam_date == result_obj.exam_date,
            )
        )
        result = await db.execute(stmt)
        duplicate_result = result.scalars().first()
        
        if duplicate_result and duplicate_result.result_id != result_id:
            raise HTTPException(status_code=400, detail="Duplicate result entry")

        # Grade calculation
        data["grade"] = calculate_grade(data["marks_obtained"], data["total_marks"])

        # Update fields except exam_date
        for key, value in data.items():
            if key != "exam_date":
                setattr(result_obj, key, value)

        await db.commit()
        await db.refresh(result_obj)
        return result_obj

    except Exception as e:
        await db.rollback()
        return await handle_exception(db, e, action="update_result")


# =========================
# Delete result
# =========================
@role_required(["teacher", "admin"])
async def delete_result(db, result_id, current_user):
    try:
        result = await db.execute(select(Result).where(Result.result_id == result_id))
        result_obj = result.scalars().first()
        if not result_obj:
            raise HTTPException(status_code=404, detail="Result not found")

        if current_user["user_role"] == "teacher":
            stmt = select(teaching_assignments).where(
                and_(
                    teaching_assignments.c.teacher_id == current_user["user_id"],
                    teaching_assignments.c.subject_id == result_obj.subject_id,
                    teaching_assignments.c.batch_id == result_obj.batch_id,
                    teaching_assignments.c.department_id == result_obj.department_id,
                )
            )
            result = await db.execute(stmt)
            assigned = result.first()
            if not assigned:
                raise HTTPException(
                    status_code=403, detail="You are not assigned to this subject"
                )

        await db.delete(result_obj)
        await db.commit()
        return {"detail": "Result deleted successfully"}

    except Exception as e:
        await db.rollback()
        return await handle_exception(db, e, action="delete_result")
