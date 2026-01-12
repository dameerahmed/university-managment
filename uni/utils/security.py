from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from typing import Optional
from jose import JWTError, jwt  # type: ignore
import os
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
ADMIN_SECRET = os.getenv("ADMIN_SECRET")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    try:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        jwt_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return jwt_token
    except Exception as e:
        print(f"Error creating access token: {e}")
        return None


def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        print(f"JWT Verification Error: {e}")
        return None


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = verify_access_token(token)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
            )

        return {
            "email": payload.get("email"),
            "user_id": payload.get("user_id"),
            "user_role": payload.get("user_role"),
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def is_admin_user(user: dict = Depends(get_current_user)):
    if user["email"] != ADMIN_EMAIL:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access forbidden"
        )
    if user["user_role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access forbidden"
        )

    return True


def role_required(allowed_roles: list):
    def decorator(func):
        def wrapper(*args, **kwargs):
            user = kwargs.get("current_user")
            if not user or user["user_role"] not in allowed_roles:
                raise HTTPException(status_code=403, detail="Access denied")
            return func(*args, **kwargs)

        return wrapper

    return decorator
