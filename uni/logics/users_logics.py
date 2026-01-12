from fastapi import Depends, HTTPException
from sqlalchemy import select, func
import os
from dotenv import load_dotenv
from uni.models.users_table import User
from uni.models.students_table import Student
from uni.models.teachers_table import Teacher
from uni.utils.security import (
    create_access_token,
    get_current_user,
    verify_password,
    hash_password,
)
import asyncio
from uni.utils.security import role_required

load_dotenv()

ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")


async def login(current_user, db):
    try:
        if (
            current_user.email == ADMIN_EMAIL
            and current_user.password == ADMIN_PASSWORD
        ):
            token = create_access_token(
                data={
                    "email": ADMIN_EMAIL,
                    "user_id": 0,
                    "user_role": "admin",
                }
            )
            return {
                "message": "Super Admin Login Successful",
                "user_name": "Super Admin",
                "email": ADMIN_EMAIL,
                "user_role": "admin",
                "user_token": token,
            }
        db_user = await db.execute(select(User).where(User.email == current_user.email))
        db_user = db_user.scalars().first()
        if db_user and verify_password(current_user.password, db_user.password):
            token = create_access_token(
                data={
                    "email": db_user.email,
                    "user_id": db_user.user_id,
                    "user_role": db_user.user_role.value,
                }
            )
            return {
                "message": "Login Successful",
                "user_name": db_user.user_name,
                "email": db_user.email,
                "user_role": db_user.user_role.value,
                "user_token": token,
            }

        raise HTTPException(status_code=400, detail="Invalid email or password")

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def update_by_admin(db, user_id, user):
    try:
        result = await db.execute(select(User).where(User.user_id == user_id))
        db_user = result.scalars().first()
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        if user.email and user.email != db_user.email:
            existing_result = await db.execute(select(User).where(User.email == user.email))
            existing_user = existing_result.scalars().first()
            if existing_user:
                raise HTTPException(status_code=400, detail="Email already registered")
            db_user.email = user.email

        if user.user_name:
            db_user.user_name = user.user_name

        if user.password:
            db_user.password = hash_password(user.password)

        await db.commit()
        await db.refresh(db_user)

        return db_user
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


async def update(db, user_id, user):
    try:
        result = await db.execute(select(User).where(User.user_id == user_id))
        db_user = result.scalars().first()
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        if user.email and user.email != db_user.email:
            existing_result = await db.execute(select(User).where(User.email == user.email))
            existing_user = existing_result.scalars().first()
            if existing_user:
                raise HTTPException(status_code=400, detail="Email already registered")
            db_user.email = user.email

        if user.password:
            db_user.password = hash_password(user.password)

        await db.commit()
        await db.refresh(db_user)

        return db_user
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


async def delete(db, user_id):
    try:
        result = await db.execute(select(User).where(User.user_id == user_id))
        db_user = result.scalars().first()
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        await db.delete(db_user)
        await db.commit()

        return {"message": "User deleted successfully"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


async def get(db, user_id):
    try:
        result = await db.execute(select(User).where(User.user_id == user_id))
        db_user = result.scalars().first()
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        return db_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def get_all(db, current_user):
    try:
        if current_user["user_role"] != "admin":
            raise HTTPException(status_code=403, detail="Not authorized")
        result = await db.execute(select(User))
        users = result.scalars().all()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def get_dashboard_stats(db, current_user):
    try:
        student_count = await db.execute(select(func.count()).select_from(Student))
        teacher_count = await db.execute(select(func.count()).select_from(Teacher))
        user_count = await db.execute(select(func.count()).select_from(User))
        return {
            "total_students": student_count.scalar(),
            "total_teachers": teacher_count.scalar(),
            "total_users": user_count.scalar(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
