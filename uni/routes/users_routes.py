from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from uni.database.connection import get_db

from uni.schemas.users import (
    UserUpdate,
    UserResponse,
    UserLogin,
    UserUpdate_By_Admin,
)
from uni.logics.users_logics import (
    login,
    update,
    delete,
    get,
    get_all,
    update_by_admin,
    get_current_user,
    get_dashboard_stats,
)


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/login", response_model=UserResponse)
async def user_login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    return await login(user, db)


@router.put("/update/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user: UserUpdate, db: AsyncSession = Depends(get_db)):
    return await update(db, user_id, user)


@router.patch("/update_by_admin/{user_id}", response_model=UserResponse)
async def update_user_by_admin(
    user_id: int, user: UserUpdate_By_Admin, db: AsyncSession = Depends(get_db)
):
    return await update_by_admin(db, user_id, user)


@router.delete("/delete/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    return await delete(db, user_id)


@router.get("/get/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    return await get(db, user_id)


@router.get("/get_all", response_model=list[UserResponse])
async def get_all_users(
    current_user: dict = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    return await get_all(db, current_user)


@router.get("/dashboard_stats")
async def dashboard_stats(
    current_user: dict = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    return await get_dashboard_stats(db, current_user)
